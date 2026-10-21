"""The API flagship's reference service (Javalin, port 7070): accounts, tokens and credits with
idempotent purchases, rate limits and RFC 7807 errors. Run from the sibling repository."""

import requests

from framework.api.clients.responses import expect, parse
from framework.api.models.reference import Account, Balance, Region, Token
from framework.core.http import ApiSession


class ReferenceClient:
    def __init__(self, session: ApiSession) -> None:
        self._http = session

    def create_account(
        self, handle: str, display_name: str, password: str, region: Region
    ) -> Account:
        response = self._http.post(
            "/v1/accounts",
            json_body={
                "handle": handle,
                "displayName": display_name,
                "password": password,
                "region": region,
            },
        )
        return parse(expect(response, 201), Account)

    def token(self, handle: str, password: str) -> Token:
        response = self._http.post(
            "/v1/auth/token", json_body={"handle": handle, "password": password}
        )
        return parse(expect(response, 200), Token)

    def me(self, token: str | None) -> requests.Response:
        return self._http.get("/v1/accounts/me", headers=self._bearer(token))

    def update_me(self, token: str, display_name: str) -> requests.Response:
        return self._http.patch(
            "/v1/accounts/me", json_body={"displayName": display_name}, headers=self._bearer(token)
        )

    def delete_me(self, token: str) -> requests.Response:
        return self._http.delete("/v1/accounts/me", headers=self._bearer(token))

    def public_profile(self, token: str, handle: str) -> requests.Response:
        """Any account's public profile; the contract requires a signed-in caller."""
        return self._http.get(f"/v1/accounts/{handle}", headers=self._bearer(token))

    def purchase(self, token: str, pack_id: str, idempotency_key: str | None) -> requests.Response:
        headers = self._bearer(token)
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        return self._http.post(
            "/v1/credits/purchases", json_body={"packId": pack_id}, headers=headers
        )

    def balance(self, token: str) -> Balance:
        return parse(
            expect(self._http.get("/v1/credits/balance", headers=self._bearer(token)), 200),
            Balance,
        )

    @staticmethod
    def _bearer(token: str | None) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"} if token is not None else {}
