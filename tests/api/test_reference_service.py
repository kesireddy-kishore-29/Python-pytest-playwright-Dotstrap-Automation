"""The API flagship's reference service: errors as RFC 7807 problems (401, 404, 422, 429) and an
idempotent purchase. Skipped when the service is not running (it lives in a sibling repository).
"""

import uuid

import pytest
import requests

from framework.api.clients import ReferenceClient, expect, parse
from framework.api.fixture_types import RefAccount
from framework.api.models.reference import Problem, Purchase
from framework.core.waits import wait_until

pytestmark = [pytest.mark.api, pytest.mark.regression]


def _until_rate_limited(reference: ReferenceClient, token: str) -> requests.Response:
    """Calls until the per-token limit answers 429 (60 a window by default; 100 at most)."""
    for _ in range(100):
        response = reference.me(token)
        if response.status_code == 429:
            return response
    raise AssertionError("100 calls in a row were never rate limited")


@pytest.mark.parametrize(
    ("case", "status"),
    [
        pytest.param("no token", 401, marks=pytest.mark.feature("FEAT-AUTHZ-01"), id="401"),
        pytest.param("unknown account", 404, marks=pytest.mark.feature("FEAT-ERR-01"), id="404"),
        pytest.param("empty name", 422, marks=pytest.mark.feature("FEAT-ACCT-02"), id="422"),
        pytest.param("too many calls", 429, marks=pytest.mark.feature("FEAT-RATE-01"), id="429"),
    ],
)
def test_a_refusal_is_a_problem_with_the_right_status(
    reference: ReferenceClient, reference_account: RefAccount, case: str, status: int
) -> None:
    """A refusal is an RFC 7807 problem with the right status."""
    token = reference_account.token
    match case:
        case "no token":
            response = reference.me(None)
        case "unknown account":
            response = reference.public_profile(token, "qa-nobody-" + uuid.uuid4().hex[:8])
        case "empty name":
            response = reference.update_me(token, "")
        case _:
            response = _until_rate_limited(reference, token)

    assert response.status_code == status
    assert response.headers["Content-Type"].startswith("application/problem+json")
    problem = parse(response, Problem)
    assert problem.status == status
    if status == 422:
        assert problem.errors is not None
        assert [e.field for e in problem.errors] == ["displayName"]
    if status == 429:
        assert int(response.headers["Retry-After"]) >= 1
        # ...and the limit lifts when its window ends (the account's cleanup needs it too).
        wait_until(
            "the rate limit to lift",
            lambda: reference.me(token).status_code == 200,
            timeout=20,
            interval=0.5,
        )


@pytest.mark.smoke
@pytest.mark.feature("FEAT-IDEMP-01")
def test_the_same_key_and_body_replays_the_purchase_and_charges_once(
    reference: ReferenceClient, reference_account: RefAccount
) -> None:
    """The same idempotency key and body replays the purchase and charges once."""
    token = reference_account.token
    key = "py-" + uuid.uuid4().hex[:16]

    first = parse(expect(reference.purchase(token, "pack-10", key), 201), Purchase)
    replay = expect(reference.purchase(token, "pack-10", key), 200)

    assert replay.headers["Idempotent-Replayed"] == "true"
    assert parse(replay, Purchase) == first
    assert reference.balance(token).balance == 15, "5 free credits + one pack of 10, not two"
