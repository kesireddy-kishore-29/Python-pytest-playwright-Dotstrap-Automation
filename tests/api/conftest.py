"""API fixtures: one client per target, wired to the test's transcript, and data that cleans up
after itself and proves it is gone."""

from collections.abc import Iterator

import pytest

from framework.api.clients import BookerClient, ReferenceClient, expect, reachable
from framework.api.fixture_types import BookingFactory, RefAccount
from framework.api.models.booker import Booking, CreatedBooking
from framework.config.settings import Settings, url
from framework.core.http import ApiSession
from framework.data.factories import a_booking, unique_name
from framework.evidence.plugin import Attempt

# ---- Restful-Booker (public practice API) ------------------------------------------------------


@pytest.fixture
def booker(settings: Settings, evidence: Attempt) -> Iterator[BookerClient]:
    session = ApiSession(
        "restful-booker", url(settings.booker_base_url), settings.timeout, evidence.transcript
    )
    yield BookerClient(session)
    session.close()


@pytest.fixture(scope="session")
def booker_token(settings: Settings) -> str:
    """One token per worker: signing in is not what most tests are about."""
    session = ApiSession("restful-booker", url(settings.booker_base_url), settings.timeout)
    try:
        return BookerClient(session).token(
            settings.booker_username, settings.booker_password.get_secret_value()
        )
    finally:
        session.close()


@pytest.fixture
def bookings(booker: BookerClient, booker_token: str) -> Iterator[BookingFactory]:
    """Creates bookings for the test; afterwards deletes each one and proves it is gone."""
    created: list[int] = []

    def create(booking: Booking | None = None) -> CreatedBooking:
        result = booker.create(booking or a_booking())
        created.append(result.bookingid)
        return result

    yield create
    for booking_id in created:
        if booker.get(booking_id).status_code == 404:
            continue  # the test deleted it itself
        expect(booker.delete(booking_id, booker_token), 201)  # Restful-Booker answers 201
        assert booker.get(booking_id).status_code == 404, f"booking {booking_id} not cleaned up"


# ---- the API flagship's reference service (self-hosted, port 7070) -----------------------------


@pytest.fixture(scope="session")
def reference_available(settings: Settings) -> None:
    if not reachable(f"{url(settings.reference_base_url)}/health"):
        pytest.skip(
            f"The API flagship's reference service is not reachable at "
            f"{url(settings.reference_base_url)} "
            "(start it from restassured-testng-api-Dotstrap-Automation)"
        )


@pytest.fixture
def reference(
    settings: Settings, evidence: Attempt, reference_available: None
) -> Iterator[ReferenceClient]:
    session = ApiSession(
        "reference-service",
        url(settings.reference_base_url),
        settings.timeout,
        evidence.transcript,
    )
    yield ReferenceClient(session)
    session.close()


@pytest.fixture
def reference_account(reference: ReferenceClient) -> Iterator[RefAccount]:
    """A fresh account for this test; deleted afterwards, and its token proven dead."""
    handle = unique_name("py")
    password = f"pw-{handle}"
    reference.create_account(handle, "Python QA", password, "eu")
    token = reference.token(handle, password).access_token
    yield RefAccount(handle, token)
    expect(reference.delete_me(token), 204)
    assert reference.me(token).status_code == 401, f"account {handle} still answers"
