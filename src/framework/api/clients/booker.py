"""Restful-Booker, a public practice API (https://restful-booker.herokuapp.com).

Known behaviour of the public target, asserted as it is and recorded in docs/known-issues.md:
DELETE answers 201, a write without a valid token answers 403 (not 401), and wrong credentials
answer 200 with {"reason": "Bad credentials"}. It answers 418 to a multi-value Accept header, so
the session sends exactly `application/json`.
"""

import requests

from framework.api.clients.responses import expect, parse
from framework.api.models.booker import AuthToken, Booking, CreatedBooking
from framework.core.http import ApiSession


class BookerClient:
    def __init__(self, session: ApiSession) -> None:
        self._http = session

    def auth(self, username: str, password: str) -> requests.Response:
        return self._http.post("/auth", json_body={"username": username, "password": password})

    def token(self, username: str, password: str) -> str:
        return parse(expect(self.auth(username, password), 200), AuthToken).token

    def create(self, booking: Booking) -> CreatedBooking:
        response = self._http.post("/booking", json_body=booking.model_dump(mode="json"))
        return parse(expect(response, 200), CreatedBooking)

    def get(self, booking_id: int) -> requests.Response:
        return self._http.get(f"/booking/{booking_id}")

    def read(self, booking_id: int) -> Booking:
        return parse(expect(self.get(booking_id), 200), Booking)

    def update(self, booking_id: int, booking: Booking, token: str | None) -> requests.Response:
        return self._http.put(
            f"/booking/{booking_id}",
            json_body=booking.model_dump(mode="json"),
            headers=self._auth(token),
        )

    def delete(self, booking_id: int, token: str | None) -> requests.Response:
        return self._http.delete(f"/booking/{booking_id}", headers=self._auth(token))

    @staticmethod
    def _auth(token: str | None) -> dict[str, str]:
        return {"Cookie": f"token={token}"} if token is not None else {}
