"""Types the API fixtures hand to tests, so tests can annotate them without importing conftest."""

from collections.abc import Callable
from dataclasses import dataclass, field

from framework.api.clients.app import AppClient
from framework.api.models.app import AppItem, ItemStatus
from framework.api.models.booker import CreatedBooking

BookingFactory = Callable[..., CreatedBooking]
"""Creates a booking (a default one, or the one given) that the fixture deletes afterwards."""


@dataclass(frozen=True)
class RefAccount:
    """A throwaway account on the reference service, deleted after the test."""

    handle: str
    token: str


@dataclass
class AppAccount:
    """A throwaway account on the UI flagship's app. `seed` creates items that the fixture
    deletes, and checks are gone, after the test."""

    client: AppClient
    email: str
    password: str
    token: str
    seeded: list[str] = field(default_factory=list)

    def seed(self, name: str, status: ItemStatus = "active") -> AppItem:
        item = self.client.create_item(self.token, name, status)
        self.seeded.append(item.id)
        return item

    def items(self) -> list[AppItem]:
        return self.client.items(self.token)
