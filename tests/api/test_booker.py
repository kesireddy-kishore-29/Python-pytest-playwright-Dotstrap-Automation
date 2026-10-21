"""Restful-Booker, a public practice API: auth, create, read, update, delete, not found.

Where the public target deviates from HTTP semantics, the test asserts what it really does and
says so; each deviation is a finding in docs/known-issues.md.
"""

import pytest

from framework.api.clients import BookerClient, expect, parse
from framework.api.fixture_types import BookingFactory
from framework.api.models.booker import Booking
from framework.config.settings import Settings
from framework.data.factories import a_booking, unique_name

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.feature("FEAT-AUTH-01")
def test_valid_credentials_receive_a_token(booker: BookerClient, settings: Settings) -> None:
    """Valid credentials receive a token."""
    token = booker.token(settings.booker_username, settings.booker_password.get_secret_value())

    assert len(token) >= 10


@pytest.mark.feature("FEAT-AUTH-02")
def test_wrong_credentials_receive_no_token(booker: BookerClient) -> None:
    """Wrong credentials receive no token."""
    response = booker.auth("admin", "wrong-password")

    # Finding: Restful-Booker answers 200 with a reason instead of 401.
    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}


@pytest.mark.feature("FEAT-AUTH-02")
@pytest.mark.parametrize("token", [None, "not-a-real-token"], ids=["no token", "bad token"])
def test_a_write_without_a_valid_token_is_refused(
    booker: BookerClient, bookings: BookingFactory, token: str | None
) -> None:
    """A write without a valid token is refused and changes nothing."""
    keep = unique_name("keep")
    created = bookings(a_booking(firstname=keep))

    refused = booker.update(created.bookingid, a_booking(firstname=unique_name("changed")), token)

    # Finding: 403 for a missing or bad token; HTTP semantics would be 401.
    assert refused.status_code == 403
    assert booker.read(created.bookingid).firstname == keep


@pytest.mark.smoke
@pytest.mark.feature("FEAT-BOOK-01", "FEAT-BOOK-02")
def test_a_created_booking_reads_back_exactly_as_sent(
    booker: BookerClient, bookings: BookingFactory
) -> None:
    """A created booking reads back exactly as sent."""
    sent = a_booking(totalprice=240, additionalneeds="Late check-in")

    created = bookings(sent)

    assert created.booking == sent
    assert booker.read(created.bookingid) == sent


@pytest.mark.feature("FEAT-BOOK-03")
def test_an_update_with_a_token_replaces_the_booking(
    booker: BookerClient, bookings: BookingFactory, booker_token: str
) -> None:
    """An update with a token replaces the booking."""
    created = bookings()
    changed = a_booking(totalprice=99, depositpaid=False, additionalneeds="None")

    updated = parse(expect(booker.update(created.bookingid, changed, booker_token), 200), Booking)

    assert updated == changed
    assert booker.read(created.bookingid) == changed


@pytest.mark.feature("FEAT-BOOK-04")
def test_a_deleted_booking_is_gone(
    booker: BookerClient, bookings: BookingFactory, booker_token: str
) -> None:
    """A deleted booking is gone."""
    created = bookings()

    deleted = booker.delete(created.bookingid, booker_token)

    # Finding: Restful-Booker answers 201 Created to a delete.
    assert deleted.status_code == 201
    assert booker.get(created.bookingid).status_code == 404


@pytest.mark.feature("FEAT-NEG-01")
def test_an_unknown_booking_is_a_404(booker: BookerClient) -> None:
    """An unknown booking is a 404."""
    assert booker.get(999_999_999).status_code == 404
