"""Run-level outputs built from the recorder: failure bundles, the gallery page and the step
summary (also appended to the GitHub job summary when the run is in Actions)."""

import json
import os
import shutil
import zipfile
from importlib import resources
from pathlib import Path
from typing import Any

from framework.evidence.recorder import AttemptRecord, RunRecorder

_PLACEHOLDER = "/*__DATA__*/null"
# Built from code points so no editor or shell can turn the escape into the character itself.
_ESCAPED_LT = chr(0x5C) + "u003c"  # the six characters <
_NEWLINE = chr(0x0A)

_BUNDLE_README = """# Failure bundle: {title}

| | |
|---|---|
| Test | `{test_id}` |
| Features | {features} |
| Run | `{run_id}` (git `{git_sha}`) |
| Attempts | {attempts} |
| Error | `{error}` |

## What is in here

| File | What it is | How to open |
|---|---|---|
{files}

A file appears only when the test produced it: API tests have a transcript, UI tests the rest.
"""

_BUNDLE_FILES = (
    ("video.webm", "The browser session (UI tests)", "Any browser or video player"),
    (
        "trace.zip",
        "Playwright trace: every action, DOM snapshot and request (redacted)",
        "https://trace.playwright.dev",
    ),
    ("screenshot.png", "The page when the test failed", "An image viewer"),
    ("fullpage.png", "The whole page when the test failed", "An image viewer"),
    ("page-source.html", "The DOM when the test failed (redacted)", "A browser or editor"),
    ("console.log", "The browser console (redacted)", "A text editor"),
    (
        "network.har",
        "Every request and response (headers and cookies masked)",
        "A HAR viewer or Chrome DevTools",
    ),
    ("transcript.md", "Every API call with bodies (API tests; redacted)", "A Markdown viewer"),
    ("meta.json", "Test identity, features, environment, git SHA", "A JSON viewer"),
)


def build_bundle(run: RunRecorder, final: AttemptRecord) -> Path | None:
    """`<run>/failure-bundles/<slug>/` with every kept attempt and a README, plus a zip."""
    if final.evidence_dir is None:
        return None
    test_dir = run.run_dir / Path(final.evidence_dir).parent
    bundle = run.run_dir / "failure-bundles" / test_dir.name
    attempts = sorted(p for p in test_dir.iterdir() if p.is_dir()) if test_dir.is_dir() else []
    bundle.mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        shutil.copytree(attempt, bundle / f"attempt-{attempt.name}", dirs_exist_ok=True)
    (bundle / "README.md").write_text(
        _BUNDLE_README.format(
            title=final.title,
            test_id=final.id,
            features=", ".join(final.feature_ids),
            run_id=run.run_id,
            git_sha=run.git_sha,
            attempts=len(attempts),
            error=final.error.type if final.error else "",
            files=_file_rows(),
        ),
        encoding="utf-8",
    )
    with zipfile.ZipFile(bundle.with_suffix(".zip"), "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(bundle.rglob("*")):
            if file.is_file():
                archive.write(file, file.relative_to(bundle).as_posix())
    return bundle


def render_gallery(data: dict[str, Any]) -> str:
    """The family's shared gallery page with this run's data; the template is byte-identical."""
    template = resources.files("framework.evidence").joinpath("templates/gallery.html")
    html = template.read_text("utf-8")
    # json.dumps escapes every non-ASCII character (U+2028 and U+2029 included, which a JavaScript
    # string cannot hold raw); "<" is escaped too, so the data cannot close the script element.
    payload = json.dumps(data).replace("<", _ESCAPED_LT)
    return html.replace(_PLACEHOLDER, payload)


def _file_rows() -> str:
    return _NEWLINE.join(f"| `attempt-N/{f}` | {what} | {how} |" for f, what, how in _BUNDLE_FILES)


def write_gallery(run: RunRecorder, finals: list[AttemptRecord]) -> Path:
    tests = []
    for final in finals:
        attempts = []
        if final.evidence_dir is not None:
            test_dir = run.run_dir / Path(final.evidence_dir).parent
            for attempt_dir in sorted(test_dir.iterdir()) if test_dir.is_dir() else []:
                meta = attempt_dir / "meta.json"
                if not meta.is_file():
                    continue
                attempts.append(
                    {
                        "attempt": int(attempt_dir.name),
                        "status": json.loads(meta.read_text("utf-8"))["test"]["status"],
                        "dir": attempt_dir.relative_to(run.run_dir).as_posix(),
                        "files": sorted(p.name for p in attempt_dir.iterdir()),
                    }
                )
        tests.append(
            {
                "title": final.title,
                "suite": final.suite,
                "status": final.status,
                "durationMs": final.duration_ms,
                "featureIds": list(final.feature_ids),
                "attempts": attempts,
            }
        )
    data = {
        "repo": "Python-pytest-playwright-Dotstrap-Automation",
        "runId": run.run_id,
        "recordMode": run.record_mode,
        "base": "",
        "tests": tests,
    }
    out = run.run_dir / "gallery.html"
    out.write_text(render_gallery(data), encoding="utf-8")
    return out


def step_summary(run: RunRecorder, summary: dict[str, Any], finals: list[AttemptRecord]) -> str:
    t = summary["totals"]
    lines = [
        f"## Python-pytest-playwright-Dotstrap-Automation · `{run.run_id}`",
        "",
        "| Total | Passed | Failed | Flaky | Skipped | Quarantined | Duration |",
        "|---|---|---|---|---|---|---|",
        (
            f"| {t['total']} | {t['passed']} | {t['failed']} | {t['flaky']} | {t['skipped']} "
            f"| {t['quarantined']} | {summary['durationMs'] / 1000:.1f} s |"
        ),
        "",
    ]
    failed = [f for f in finals if f.status == "failed"]
    if failed:
        lines += [f"<details><summary>{len(failed)} failed test(s)</summary>", ""]
        for f in failed:
            message = f.error.message.strip().splitlines()[0] if f.error else ""
            lines.append(f"- `{f.id}`: {message[:160]}")
        lines += ["", "</details>", ""]
    lines.append(
        f"Evidence: `run-evidence/Python-pytest-playwright-Dotstrap-Automation/{run.run_id}/` "
        "(gallery.html, failure-bundles/)"
    )
    return "\n".join(lines) + "\n"


def write_step_summary(
    run: RunRecorder, summary: dict[str, Any], finals: list[AttemptRecord]
) -> None:
    text = step_summary(run, summary, finals)
    (run.run_dir / "summary.md").write_text(text, encoding="utf-8")
    github = os.environ.get("GITHUB_STEP_SUMMARY")
    if github:
        with Path(github).open("a", encoding="utf-8") as out:
            out.write(text)
