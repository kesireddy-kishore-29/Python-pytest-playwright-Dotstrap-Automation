"""Fails on purpose (marker demo_failure), to show the evidence an API failure leaves: the
transcript of every call with redacted headers and bodies. Never part of a gating run."""

import pytest

from framework.api.clients import BookerClient

pytestmark = [pytest.mark.api, pytest.mark.demo_failure]


@pytest.mark.feature("FEAT-DEMO-01")
def test_demo_an_answer_that_does_not_match_the_expectation(booker: BookerClient) -> None:
    """demo: an API answer that does not match the expectation."""
    response = booker.get(999_999_999)

    assert response.status_code == 200, "expected booking 999999999 to exist"
