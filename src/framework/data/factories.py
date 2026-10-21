"""Factories. Every identity a test creates starts with `qa-`, so a sweeper can find and remove
anything a crashed run left behind; a random suffix keeps parallel workers apart."""

import uuid
from dataclasses import dataclass, replace
from datetime import date, timedelta
from typing import Any

from framework.api.models.booker import Booking, BookingDates


def unique_name(label: str) -> str:
    """`qa-<label>-<8 hex>`."""
    return f"qa-{label}-{uuid.uuid4().hex[:8]}"


def unique_email() -> str:
    """An address on the reserved `.test` domain, which the UI flagship's app requires."""
    return f"{unique_name('user')}@example.test"


def a_booking(**overrides: Any) -> Booking:
    """A valid booking two weeks from now; any field can be overridden."""
    checkin = date.today() + timedelta(days=14)  # noqa: DTZ011 - a calendar date, not an instant
    values: dict[str, Any] = {
        "firstname": unique_name("guest"),
        "lastname": "Lovelace",
        "totalprice": 240,
        "depositpaid": True,
        "bookingdates": BookingDates(checkin=checkin, checkout=checkin + timedelta(days=3)),
        "additionalneeds": "Breakfast",
    }
    values.update(overrides)
    return Booking(**values)


@dataclass(frozen=True)
class Customer:
    """Who is checking out on Sauce Demo. `None` leaves the field empty."""

    first_name: str | None
    last_name: str | None
    postal_code: str | None

    def without(self, field: str) -> "Customer":
        return replace(self, **{field: None})


def a_customer() -> Customer:
    return Customer(first_name="Ada", last_name="Lovelace", postal_code="560001")
