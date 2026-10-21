"""The repository's rules, checked like code: traceability, quarantine, and a scan of the
sources for what Checkstyle refuses in the Java repositories (hard waits, raw HTTP or raw
locators in tests, swallowed exceptions)."""

import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from framework.core.waits import WaitTimeoutError, wait_until
from framework.evidence import quarantine
from framework.evidence.identity import FEATURE_ID

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[2]
TODAY = date(2026, 10, 21)
CART = "tests/ui/test_shop.py::test_cart"


def entry(**overrides: Any) -> quarantine.Entry:
    values: dict[str, Any] = {
        "test_id": CART,
        "owner": "@qa-team",
        "reason": "badge lags",
        "expires": "2026-11-01",
        "issue": "#12",
    }
    values.update(overrides)
    return quarantine.Entry(**values)


def test_feature_ids_follow_the_shared_format() -> None:
    assert FEATURE_ID.match("FEAT-CHECKOUT-02")
    assert not FEATURE_ID.match("FEAT-CHECKOUT-2")
    assert not FEATURE_ID.match("feat-checkout-02")


def test_a_valid_quarantine_entry_for_a_quarantined_test_passes() -> None:
    assert quarantine.problems([entry()], [CART], TODAY, every_test_collected=True) == []


def test_quarantine_refuses_ownerless_reasonless_expired_and_unmatched_entries() -> None:
    found = quarantine.problems(
        [entry(owner=" ", reason="", expires="2026-10-20")], [], TODAY, every_test_collected=True
    )

    assert found == [
        f"{CART}: no owner",
        f"{CART}: no reason",
        f"{CART}: expired on 2026-10-20 (fix the test or renew with a reason)",
        f"{CART}: listed in quarantine.json but the test is not quarantined",
    ]
    assert quarantine.problems([], [CART], TODAY, every_test_collected=False) == [
        f"{CART}: marked quarantine but has no quarantine.json entry"
    ]


def test_this_repositorys_quarantine_file_is_readable() -> None:
    entries = quarantine.read(ROOT / "quarantine.json")

    assert (
        quarantine.problems(entries, [], datetime.now(UTC).date(), every_test_collected=False) == []
    )


def test_wait_until_returns_the_first_truthy_value_and_times_out_with_a_description() -> None:
    values = iter([None, False, "ready"])

    assert wait_until("a value", lambda: next(values), timeout=2, interval=0.01) == "ready"
    with pytest.raises(WaitTimeoutError, match=r"waited 0\.05 s for the impossible"):
        wait_until("the impossible", lambda: None, timeout=0.05, interval=0.01)


FORBIDDEN_EVERYWHERE = {
    r"wait_for_timeout\(": "a hard wait in the browser",
    r"except\s*:": "a bare except",
    r"except [A-Za-z]*(Exception|Error)[^:]*:\s*\n\s*pass\b": "a swallowed exception",
}
FORBIDDEN_IN_TESTS = {
    r"\brequests\.(get|post|put|patch|delete|request)\(": "raw HTTP in a test (use a client)",
    r"\.(locator|get_by_[a-z_]+)\(": "a raw locator in a test (use a page object)",
    r"\.goto\(": "navigation in a test (use a page object)",
    r"time\.sleep\(": "a hard wait",
}


def _sources(*folders: str) -> list[Path]:
    return [p for folder in folders for p in (ROOT / folder).rglob("*.py")]


def test_no_hard_waits_bare_excepts_or_swallowed_exceptions() -> None:
    found = [
        f"{path.relative_to(ROOT)}: {why}"
        for path in _sources("src", "tests")
        if path.name != "test_rules.py"
        for pattern, why in FORBIDDEN_EVERYWHERE.items()
        if re.search(pattern, path.read_text("utf-8"))
    ]
    sleeps = [
        str(p.relative_to(ROOT))
        for p in _sources("src")
        if "time.sleep(" in p.read_text("utf-8") and p.name != "waits.py"
    ]

    assert found == []
    assert sleeps == [], "the only pause is the bounded poll in framework/core/waits.py"


def test_tests_use_clients_and_page_objects_only() -> None:
    found = [
        f"{path.relative_to(ROOT)}: {why}"
        for path in _sources("tests")
        if path.parent.name != "unit" and path.name != "conftest.py"
        for pattern, why in FORBIDDEN_IN_TESTS.items()
        if re.search(pattern, path.read_text("utf-8"))
    ]

    assert found == []
