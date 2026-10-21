"""Run documents: flaky detection, run summary, flaky report, bundles, gallery, step summary."""

import json
import zipfile
from pathlib import Path

import pytest

from framework.evidence.identity import slugify
from framework.evidence.outputs import build_bundle, render_gallery, step_summary
from framework.evidence.recorder import AttemptRecord, ErrorInfo, RunRecorder

pytestmark = pytest.mark.unit


def attempt(test_id: str, status: str, number: int, error: str | None = None) -> AttemptRecord:
    return AttemptRecord(
        id=test_id,
        title=test_id,
        suite="ui",
        feature_ids=("FEAT-CART-01",),
        tags=("regression",),
        status=status,
        duration_ms=100,
        attempt=number,
        started_at="2026-10-21T00:00:00+00:00",
        error=ErrorInfo("AssertionError", error, "") if error else None,
    )


def test_a_test_that_passes_on_a_retry_is_flaky_not_passed(tmp_path: Path) -> None:
    run = RunRecorder("unit", "abc", "all", tmp_path)
    for record in (
        attempt("A", "retried", 1, "badge showed 1"),
        attempt("A", "passed", 2),
        attempt("B", "passed", 1),
        attempt("C", "retried", 1, "boom"),
        attempt("C", "retried", 2, "boom"),
        attempt("C", "failed", 3, "boom"),
    ):
        run.add(record)

    finals = {r.id: (r.status, r.attempt) for r in run.final_results()}

    assert finals == {"A": ("flaky", 2), "B": ("passed", 1), "C": ("failed", 3)}


def test_writes_the_summary_and_the_flaky_report_in_the_shared_format(tmp_path: Path) -> None:
    run = RunRecorder("unit", "abc", "all", tmp_path)
    run.add(attempt("A", "retried", 1, "badge showed 1"))
    run.add(attempt("A", "passed", 2))
    run.add(attempt("B", "skipped", 1))

    summary = run.write({"os": "test"})

    assert summary["totals"] == {
        "total": 2,
        "passed": 0,
        "failed": 0,
        "skipped": 1,
        "flaky": 1,
        "quarantined": 0,
    }
    written = json.loads((tmp_path / "run-summary.json").read_text("utf-8"))
    assert written["schemaVersion"] == 1
    assert written["repo"] == "Python-pytest-playwright-Dotstrap-Automation"
    assert {"id", "title", "suite", "featureIds", "status", "attempt"} <= written["tests"][0].keys()
    flaky = json.loads((tmp_path / "flaky-report.json").read_text("utf-8"))
    assert flaky["flaky"] == [
        {
            "testId": "A",
            "title": "A",
            "featureIds": ["FEAT-CART-01"],
            "attempts": 2,
            "firstError": "AssertionError: badge showed 1",
        }
    ]


def test_a_failure_bundle_has_every_attempt_a_readme_and_a_zip(tmp_path: Path) -> None:
    run = RunRecorder("unit", "abc", "failures", tmp_path)
    for number in (1, 2):
        directory = tmp_path / "ui" / "shop-checkout" / str(number)
        directory.mkdir(parents=True)
        (directory / "meta.json").write_text("{}", "utf-8")
    final = attempt("tests/ui/test_shop.py::checkout", "failed", 2, "no confirmation")
    final = AttemptRecord(**{**final.__dict__, "evidence_dir": "ui/shop-checkout/2"})

    bundle = build_bundle(run, final)

    assert bundle is not None
    assert (bundle / "attempt-1" / "meta.json").is_file()
    readme = (bundle / "README.md").read_text("utf-8")
    assert "| Attempts | 2 |" in readme
    assert "`attempt-N/trace.zip`" in readme
    with zipfile.ZipFile(bundle.with_suffix(".zip")) as archive:
        assert sorted(archive.namelist()) == [
            "README.md",
            "attempt-1/meta.json",
            "attempt-2/meta.json",
        ]


def test_gallery_data_cannot_close_the_script_element() -> None:
    html = render_gallery({"title": "</script><script>alert(1)</script>\u2028"})

    assert html.startswith("<!doctype html>")
    assert "/*__DATA__*/null" not in html
    assert "</script><script>alert(1)" not in html
    assert "\\u003c/script>" in html
    assert "\u2028" not in html


def test_step_summary_lists_failed_tests() -> None:
    run = RunRecorder("unit", "abc", "failures", Path("unused"))
    finals = [attempt("A", "failed", 1, "expected 2, got 1"), attempt("B", "passed", 1)]
    totals = {"total": 2, "passed": 1, "failed": 1, "skipped": 0, "flaky": 0, "quarantined": 0}

    text = step_summary(run, {"totals": totals, "durationMs": 1500}, finals)

    assert "| 2 | 1 | 1 | 0 | 0 | 0 | 1.5 s |" in text
    assert "- `A`: expected 2, got 1" in text


def test_slugs_are_safe_and_bounded() -> None:
    assert slugify("Shop: a full checkout [chromium]") == "shop-a-full-checkout-chromium"
    assert len(slugify("x" * 200)) <= 90
