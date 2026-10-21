"""The pytest plugin (loaded by tests/conftest.py). In order of a run:

1. Start-up: settings validated (all problems at once); `RECORD_MODE` turned into
   pytest-playwright's --video/--tracing/--screenshot; `TEST_RETRIES` into reruns.
2. Collection: a test without a well-formed feature marker stops the run (traceability).
3. Each attempt: an `evidence` fixture gives it a folder and an API transcript; after teardown the
   attempt keeps or discards its evidence by `RECORD_MODE`, copies pytest-playwright's video,
   trace (redacted) and screenshot, redacts the HAR and writes meta.json.
4. End: the controlling process (also under pytest-xdist) writes run-summary.json,
   flaky-report.json, failure bundles, the gallery and the step summary.
"""

import json
import logging
import os
import platform
import shutil
import subprocess
from collections.abc import Generator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

import pytest
from pytest_rerunfailures import get_reruns_count

from framework.config.record_mode import RecordMode
from framework.config.settings import ConfigError, Settings, load_settings
from framework.core.http import Transcript
from framework.core.redaction import redact_har, redact_text, redact_trace
from framework.evidence import REPO, quarantine
from framework.evidence.identity import TestIdentity, traceability_problems
from framework.evidence.outputs import build_bundle, write_gallery, write_step_summary
from framework.evidence.recorder import AttemptRecord, ErrorInfo, RunRecorder

LOG = logging.getLogger(__name__)

SETTINGS = pytest.StashKey[Settings]()
IDENTITY = pytest.StashKey[TestIdentity]()
ATTEMPT = pytest.StashKey["Attempt"]()
PHASES = pytest.StashKey[dict[str, pytest.TestReport]]()

_PLAYWRIGHT_FILES = {"video": "video.webm", "screenshot": "screenshot.png", "trace": "trace.zip"}


@dataclass
class Attempt:
    """One attempt of one test: where its evidence goes and what it has collected."""

    number: int
    directory: Path
    started_at: str
    transcript: Transcript = field(default_factory=Transcript)
    notes: list[str] = field(default_factory=list)


def settings_of(config: pytest.Config) -> Settings:
    return config.stash[SETTINGS]


def run_dir(settings: Settings) -> Path:
    return (settings.evidence_root / REPO / settings.run_id).resolve()


def _git_sha() -> str:
    if sha := os.environ.get("GITHUB_SHA"):
        return sha[:12]
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],  # noqa: S607 - git from PATH, fixed args
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return out.stdout.strip() or "unknown"


def _retried(report: pytest.TestReport) -> bool:
    """pytest-rerunfailures marks the failed phase of an attempt it will run again as "rerun",
    an outcome pytest's own type does not list."""
    return str(report.outcome) == "rerun"


def _is_worker(config: pytest.Config) -> bool:
    return hasattr(config, "workerinput")


# ---- 1. start-up ------------------------------------------------------------------------------


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    try:
        settings = load_settings()
    except ConfigError as error:
        raise pytest.UsageError(str(error)) from error
    config.stash[SETTINGS] = settings
    # Workers (pytest-xdist) start after this and read the same run ID from the environment.
    os.environ["RUN_ID"] = settings.run_id
    mode = settings.record_mode
    config.option.video = mode.playwright_option(failure_value="retain-on-failure")
    config.option.tracing = mode.playwright_option(failure_value="retain-on-failure")
    config.option.screenshot = mode.playwright_option(failure_value="only-on-failure")
    if config.getoption("reruns", None) is None:
        config.option.reruns = settings.test_retries
    if not _is_worker(config):
        config.pluginmanager.register(
            RunSession(
                RunRecorder(settings.run_id, _git_sha(), mode.value, run_dir(settings)), config
            ),
            "framework-run-session",
        )


# ---- 2. collection ----------------------------------------------------------------------------


def _collected_everything(config: pytest.Config) -> bool:
    """True when the run collects the whole test tree (no paths or node IDs given)."""
    return not config.args or [Path(a).resolve() for a in config.args] == [
        Path(config.rootpath, p).resolve() for p in config.getini("testpaths")
    ]


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    problems = traceability_problems(items)
    if problems:
        raise pytest.UsageError(
            "Traceability check failed; every test needs "
            '@pytest.mark.feature("FEAT-<AREA>-<NN>"):\n  - ' + "\n  - ".join(problems)
        )
    quarantine_problems = quarantine.problems(
        quarantine.read(Path(config.rootpath, "quarantine.json")),
        [item.nodeid for item in items if item.get_closest_marker("quarantine") is not None],
        datetime.now(UTC).date(),
        every_test_collected=_collected_everything(config),
    )
    if quarantine_problems:
        raise pytest.UsageError(
            "Quarantine check failed (quarantine.json):\n  - " + "\n  - ".join(quarantine_problems)
        )
    retries = settings_of(config).test_retries
    for item in items:
        if item.get_closest_marker("unit") is not None:
            item.add_marker(pytest.mark.flaky(reruns=0))  # a flaky unit test is a bug
        elif item.get_closest_marker("demo_failure") is not None:
            item.add_marker(pytest.mark.flaky(reruns=min(1, retries)))
        identity = TestIdentity.of(item)
        item.stash[IDENTITY] = identity
        item.user_properties.extend(
            [
                ("title", identity.title),
                ("suite", identity.suite),
                ("feature_ids", list(identity.feature_ids)),
                ("tags", list(identity.tags)),
            ]
        )


# ---- 3. each attempt --------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def evidence(request: pytest.FixtureRequest) -> Attempt:
    """This attempt's evidence folder and API transcript. Allure labels from the markers."""
    item = request.node
    settings = settings_of(request.config)
    identity = item.stash[IDENTITY]
    number = getattr(item, "execution_count", 1)
    directory = run_dir(settings) / identity.suite / identity.slug / str(number)
    if directory.exists():  # left by an earlier run with the same RUN_ID
        shutil.rmtree(directory)
    attempt = Attempt(number, directory, datetime.now(UTC).isoformat())
    item.stash[ATTEMPT] = attempt
    _allure_labels(identity)
    return attempt


def _allure_labels(identity: TestIdentity) -> None:
    try:
        import allure  # noqa: PLC0415 - optional: absent when allure-pytest is not loaded
    except ImportError:
        return
    allure.dynamic.title(identity.title)  # type: ignore[no-untyped-call]
    for feature_id in identity.feature_ids:
        allure.dynamic.feature(feature_id)  # type: ignore[no-untyped-call]
    for tag in identity.tags:
        allure.dynamic.tag(tag)  # type: ignore[no-untyped-call]


def phase_failed(item: pytest.Item, *phases: str) -> bool:
    """Whether any of the named phases of the current attempt has failed so far."""
    reports = item.stash.get(PHASES, {})
    return any(reports[p].failed for p in phases if p in reports)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    # Outermost wrapper: runs after pytest-playwright has kept or discarded its artifacts.
    report = yield
    report.user_properties.append(("attempt", getattr(item, "execution_count", 1)))
    phases = item.stash.setdefault(PHASES, {})
    if report.when == "setup":
        phases.clear()
    phases[report.when] = report
    if report.when == "teardown":
        try:
            _finish_attempt(item, report, phases)
        # Evidence must never hide the test's own result: any failure here is logged and shown
        # in the report's sections instead of replacing the test's outcome.
        except Exception as error:  # noqa: BLE001
            LOG.warning("evidence for %s not written: %s", item.nodeid, error)
            report.sections.append(("evidence", f"Evidence not written: {error!r}"))
    return report


def _status(item: pytest.Item, phases: dict[str, pytest.TestReport], number: int) -> str:
    if any(r.failed for r in phases.values()):
        reruns = int(get_reruns_count(item) or 0)
        return "retried" if number <= reruns else "failed"
    if any(r.skipped for r in phases.values()):
        return "skipped"
    return "passed"


def _error(phases: dict[str, pytest.TestReport]) -> ErrorInfo | None:
    for when in ("setup", "call", "teardown"):
        report = phases.get(when)
        if report is not None and report.failed:
            return error_info(report)
    return None


def error_info(report: pytest.TestReport) -> ErrorInfo:
    crash = getattr(report.longrepr, "reprcrash", None)
    message = str(getattr(crash, "message", "")) or report.longreprtext.strip().splitlines()[-1]
    head = message.split(":", 1)[0].strip()
    error_type = head if head.replace(".", "").replace("_", "").isalnum() else "Error"
    return ErrorInfo(
        type=error_type,
        message=redact_text(message),
        stack=redact_text(report.longreprtext)[:6000],
    )


def _finish_attempt(
    item: pytest.Item, report: pytest.TestReport, phases: dict[str, pytest.TestReport]
) -> None:
    settings = settings_of(item.config)
    number = getattr(item, "execution_count", 1)
    attempt = item.stash.get(ATTEMPT, None)
    identity = item.stash[IDENTITY]
    directory = (
        attempt.directory
        if attempt is not None
        else run_dir(settings) / identity.suite / identity.slug / str(number)
    )
    status = _status(item, phases, number)
    if not settings.record_mode.keeps(failed=status in ("failed", "retried")):
        shutil.rmtree(directory, ignore_errors=True)
        _remove_empty_parents(directory, run_dir(settings))
        return
    directory.mkdir(parents=True, exist_ok=True)
    if attempt is not None and attempt.transcript.calls:
        attempt.transcript.write(directory)
    _copy_playwright_artifacts(item.config, report, directory)
    har = directory / "network.har"
    if har.is_file():
        har.write_text(
            json.dumps(redact_har(json.loads(har.read_text("utf-8"))), indent=1),
            encoding="utf-8",
        )
    record = AttemptRecord(
        id=identity.test_id,
        title=identity.title,
        suite=identity.suite,
        feature_ids=identity.feature_ids,
        tags=identity.tags,
        status=status,
        duration_ms=int(sum(r.duration for r in phases.values()) * 1000),
        attempt=number,
        started_at=attempt.started_at if attempt else datetime.now(UTC).isoformat(),
        error=_error(phases),
    )
    _write_meta(settings, directory, record, attempt.notes if attempt else [])
    files = sorted(p.name for p in directory.iterdir())
    relative = directory.relative_to(run_dir(settings)).as_posix()
    report.user_properties.extend([("evidence_dir", relative), ("evidence_files", files)])
    _attach_to_allure(directory)


def _remove_empty_parents(directory: Path, root: Path) -> None:
    """Removes the test and suite folders a discarded attempt leaves empty, up to the run."""
    for parent in directory.parents:
        if parent == root or root not in parent.parents:
            return
        try:
            parent.rmdir()  # only succeeds when empty; another attempt's evidence stops it
        except OSError:
            return


def _copy_playwright_artifacts(
    config: pytest.Config, report: pytest.TestReport, directory: Path
) -> None:
    seen: set[str] = set()
    for name, value in report.user_properties:
        kind = str(name).removeprefix("playwright_")
        if kind not in _PLAYWRIGHT_FILES or kind in seen:
            continue
        seen.add(kind)  # the first of each kind; a test with one page has one of each
        source = Path(config.invocation_params.dir, str(value))
        target = directory / _PLAYWRIGHT_FILES[kind]
        if kind == "trace":
            # Playwright writes traces with raw cookies and headers: keep a redacted copy and
            # remove the original, so no unredacted trace is left in its output folder.
            target.write_bytes(redact_trace(source.read_bytes()))
            source.unlink()
        else:
            shutil.copyfile(source, target)


def _write_meta(
    settings: Settings, directory: Path, record: AttemptRecord, notes: list[str]
) -> None:
    meta = {
        "schemaVersion": 1,
        "repo": REPO,
        "runId": settings.run_id,
        "gitSha": _git_sha(),
        "recordMode": settings.record_mode.value,
        "test": record.to_json(),
        "environment": environment(),
        "notes": notes,
    }
    (directory / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def environment() -> dict[str, str]:
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "pytest": metadata.version("pytest"),
        "playwright": metadata.version("playwright"),
        "browser": "chromium (headless)",
    }


def _attach_to_allure(directory: Path) -> None:
    try:
        import allure  # noqa: PLC0415 - optional
    except ImportError:
        return
    kinds = {
        "screenshot.png": allure.attachment_type.PNG,
        "video.webm": allure.attachment_type.WEBM,
        "transcript.md": allure.attachment_type.TEXT,
        "console.log": allure.attachment_type.TEXT,
        "page-source.html": allure.attachment_type.HTML,
    }
    for name, kind in kinds.items():
        path = directory / name
        if path.is_file():
            allure.attach.file(str(path), name=name, attachment_type=kind)  # type: ignore[no-untyped-call]


# ---- 4. the run (controlling process only) ----------------------------------------------------


class RunSession:
    """Gathers every attempt (also from xdist workers) and writes the run documents."""

    def __init__(self, recorder: RunRecorder, config: pytest.Config) -> None:
        self.recorder = recorder
        self.config = config
        self._open: dict[tuple[str, int], list[pytest.TestReport]] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        props: dict[str, Any] = dict(report.user_properties)
        key = (report.nodeid, int(props.get("attempt", 1)))
        self._open.setdefault(key, []).append(report)
        if report.when != "teardown":
            return
        reports = self._open.pop(key)
        if any(_retried(r) for r in reports):
            status = "retried"
        elif any(r.failed for r in reports):
            status = "failed"
        elif any(r.skipped for r in reports):
            status = "skipped"
        else:
            status = "passed"
        failing = next((r for r in reports if r.failed or _retried(r)), None)
        skipped = next((r for r in reports if r.skipped), None)
        error = error_info(failing) if failing is not None else None
        if error is None and skipped is not None and isinstance(skipped.longrepr, tuple):
            error = ErrorInfo(type="Skipped", message=str(skipped.longrepr[2]), stack="")
        self.recorder.add(
            AttemptRecord(
                id=report.nodeid,
                title=str(props.get("title", report.nodeid)),
                suite=str(props.get("suite", "")),
                feature_ids=tuple(props.get("feature_ids", [])),
                tags=tuple(props.get("tags", [])),
                status=status,
                duration_ms=int(sum(r.duration for r in reports) * 1000),
                attempt=key[1],
                started_at=datetime.fromtimestamp(reports[0].start, UTC).isoformat()
                if hasattr(reports[0], "start")
                else datetime.now(UTC).isoformat(),
                error=error,
                evidence_dir=props.get("evidence_dir"),
                evidence_files=tuple(props.get("evidence_files", [])),
            )
        )

    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        if not self.recorder.attempts:
            return
        summary = self.recorder.write(environment())
        finals = self.recorder.final_results()
        if settings_of(self.config).record_mode is not RecordMode.OFF:
            for final in finals:
                if final.status == "failed":
                    build_bundle(self.recorder, final)
        write_gallery(self.recorder, finals)
        write_step_summary(self.recorder, summary, finals)
        self._allure_environment()
        LOG.info("Run summary: %s", self.recorder.run_dir / "run-summary.json")

    def _allure_environment(self) -> None:
        results = self.config.getoption("allure_report_dir", None)
        if not results:
            return
        directory = Path(results)
        directory.mkdir(parents=True, exist_ok=True)
        lines = [f"runId={self.recorder.run_id}", f"gitSha={self.recorder.git_sha}"]
        lines += [f"{k}={v}" for k, v in environment().items()]
        lines.append(f"recordMode={self.recorder.record_mode}")
        (directory / "environment.properties").write_text("\n".join(lines) + "\n", "utf-8")
