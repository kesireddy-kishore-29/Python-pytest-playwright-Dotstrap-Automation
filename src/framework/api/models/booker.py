"""Restful-Booker's contract. Strict models: an extra or missing field is a contract change."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class BookingDates(_Strict):
    checkin: date
    checkout: date


class Booking(_Strict):
    firstname: str
    lastname: str
    totalprice: int = Field(ge=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str | None = None


class CreatedBooking(_Strict):
    bookingid: int = Field(gt=0)
    booking: Booking


class AuthToken(_Strict):
    token: str = Field(min_length=10)
