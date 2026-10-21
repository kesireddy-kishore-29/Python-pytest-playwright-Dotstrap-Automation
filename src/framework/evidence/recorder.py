"""Collects every attempt of every test and writes the documents shared by the family:
`run-summary.json` (the normalised result) and `flaky-report.json` (tests that passed only on a
retry). Runs in the controlling process, so it also sees every pytest-xdist worker's results."""

import json
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from framework.evidence import REPO


@dataclass(frozen=True)
class ErrorInfo:
    type: str
    message: str
    stack: str


@dataclass(frozen=True)
class AttemptRecord:
    """One finished attempt of one test, as written to meta.json and run-summary.json."""

    id: str
    title: str
    suite: str
    feature_ids: tuple[str, ...]
    tags: tuple[str, ...]
    status: str  # passed | failed | skipped | retried (failed, then run again) | flaky (final)
    duration_ms: int
    attempt: int
    started_at: str
    error: ErrorInfo | None = None
    evidence_dir: str | None = None
    evidence_files: tuple[str, ...] = ()

    @property
    def quarantined(self) -> bool:
        return "quarantine" in self.tags

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "suite": self.suite,
            "featureIds": list(self.feature_ids),
            "tags": list(self.tags),
            "status": self.status,
            "durationMs": self.duration_ms,
            "attempt": self.attempt,
            "quarantined": self.quarantined,
            "startedAt": self.started_at,
        }
        if self.error is not None:
            out["error"] = {
                "type": self.error.type,
                "message": self.error.message,
                "stack": self.error.stack,
            }
        if self.evidence_dir is not None:
            out["evidence"] = {"dir": self.evidence_dir, "files": list(self.evidence_files)}
        return out


@dataclass
class RunRecorder:
    run_id: str
    git_sha: str
    record_mode: str
    run_dir: Path
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    attempts: list[AttemptRecord] = field(default_factory=list)

    def add(self, record: AttemptRecord) -> None:
        self.attempts.append(record)

    def final_results(self) -> list[AttemptRecord]:
        """The last attempt of each test; "flaky" when it passed after a failed attempt."""
        last: dict[str, AttemptRecord] = {}
        count: dict[str, int] = {}
        for record in self.attempts:
            count[record.id] = count.get(record.id, 0) + 1
            if record.id not in last or record.attempt >= last[record.id].attempt:
                last[record.id] = record
        results = [
            replace(r, status="flaky") if r.status == "passed" and count[r.id] > 1 else r
            for r in last.values()
        ]
        return sorted(results, key=lambda r: (r.suite, r.id))

    def first_error(self, test_id: str) -> str:
        for record in self.attempts:
            if record.id == test_id and record.error is not None:
                return f"{record.error.type}: {record.error.message}"
        return ""

    def write(self, environment: dict[str, str]) -> dict[str, Any]:
        """Writes run-summary.json and flaky-report.json; returns the summary written."""
        results = self.final_results()
        finished = datetime.now(UTC)

        def count(status: str) -> int:
            return sum(1 for r in results if r.status == status)

        summary: dict[str, Any] = {
            "schemaVersion": 1,
            "repo": REPO,
            "runId": self.run_id,
            "gitSha": self.git_sha,
            "recordMode": self.record_mode,
            "startedAt": self.started_at.isoformat(),
            "finishedAt": finished.isoformat(),
            "durationMs": int((finished - self.started_at).total_seconds() * 1000),
            "environment": environment,
            "totals": {
                "total": len(results),
                "passed": count("passed"),
                "failed": count("failed"),
                "skipped": count("skipped"),
                "flaky": count("flaky"),
                "quarantined": sum(1 for r in results if r.quarantined),
            },
            "tests": [r.to_json() for r in results],
        }
        flaky = {
            "schemaVersion": 1,
            "repo": REPO,
            "runId": self.run_id,
            "generatedAt": finished.isoformat(),
            "flaky": [
                {
                    "testId": r.id,
                    "title": r.title,
                    "featureIds": list(r.feature_ids),
                    "attempts": r.attempt,
                    "firstError": self.first_error(r.id),
                }
                for r in results
                if r.status == "flaky"
            ],
        }
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / "run-summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        (self.run_dir / "flaky-report.json").write_text(
            json.dumps(flaky, indent=2), encoding="utf-8"
        )
        return summary
