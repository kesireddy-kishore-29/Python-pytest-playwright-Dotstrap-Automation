"""The quarantine rule, the same in every repository of the family: a test marked `quarantine`
needs an entry in quarantine.json with an owner, a reason and an expiry date that has not passed,
and every entry must name a test that really is quarantined. Quarantined tests still run, in
their own non-gating job. Checked at collection by the plugin."""

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    test_id: str
    owner: str
    reason: str
    expires: str
    issue: str = ""


def read(path: Path) -> list[Entry]:
    if not path.is_file():
        return []
    data = json.loads(path.read_text("utf-8"))
    return [
        Entry(
            test_id=str(e.get("testId", "")),
            owner=str(e.get("owner", "")),
            reason=str(e.get("reason", "")),
            expires=str(e.get("expires", "")),
            issue=str(e.get("issue", "")),
        )
        for e in data.get("entries", [])
    ]


def problems(
    entries: list[Entry], quarantined: list[str], today: date, *, every_test_collected: bool
) -> list[str]:
    """Every problem. The "entry without a test" rule needs the whole suite collected."""
    found = []
    for entry in entries:
        name = entry.test_id
        if not entry.owner.strip():
            found.append(f"{name}: no owner")
        if not entry.reason.strip():
            found.append(f"{name}: no reason")
        try:
            expires = date.fromisoformat(entry.expires)
        except ValueError:
            found.append(f"{name}: expires must be YYYY-MM-DD, was '{entry.expires}'")
        else:
            if expires < today:
                found.append(f"{name}: expired on {expires} (fix the test or renew with a reason)")
        if every_test_collected and name not in quarantined:
            found.append(f"{name}: listed in quarantine.json but the test is not quarantined")
    found.extend(
        f"{test_id}: marked quarantine but has no quarantine.json entry"
        for test_id in quarantined
        if all(e.test_id != test_id for e in entries)
    )
    return found
