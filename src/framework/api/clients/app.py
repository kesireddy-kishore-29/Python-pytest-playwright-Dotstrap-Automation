"""The UI flagship's self-hosted app (sut-ui, port 4173): accounts, sessions and items, used to
seed data for hybrid tests and remove it afterwards."""

import requests

from framework.api.clients.responses import expect, parse
from framework.api.models.app import AppItem, AppItemList, ItemStatus
from framework.core.http import ApiSession

SESSION_COOKIE = "sutui_session"


class AppClient:
    def __init__(self, session: ApiSession) -> None:
        self._http = session

    def create_user(self, email: str, password: str) -> None:
        expect(
            self._http.post(
                "/api/users", json_body={"email": email, "password": password, "name": "QA"}
            ),
            201,
        )

    def sign_in(self, email: str, password: str) -> requests.Response:
        return self._http.post("/api/auth/token", json_body={"email": email, "password": password})

    def token(self, email: str, password: str) -> str:
        body = expect(self.sign_in(email, password), 200).json()
        return str(body["token"])

    def create_item(self, token: str, name: str, status: ItemStatus) -> AppItem:
        response = self._http.post(
            "/api/items", json_body={"name": name, "status": status}, headers=self._bearer(token)
        )
        return parse(expect(response, 201), AppItem)

    def items(self, token: str) -> list[AppItem]:
        response = self._http.get("/api/items", headers=self._bearer(token))
        return parse(expect(response, 200), AppItemList).items

    def delete_item(self, token: str, item_id: str) -> None:
        expect(self._http.delete(f"/api/items/{item_id}", headers=self._bearer(token)), 204, 404)

    def delete_me(self, token: str) -> None:
        expect(self._http.delete("/api/users/me", headers=self._bearer(token)), 204)

    @staticmethod
    def _bearer(token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}
