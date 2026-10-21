"""The UI flagship's self-hosted app (sut-ui). Same roles and names as the flagship's page
objects."""

from playwright.sync_api import Page

from framework.ui.components.data_table import DataTable
from framework.ui.components.modal import Modal


class ItemsPage:
    """Items (`/items`): a data table with a confirm-to-delete dialog."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.heading = page.get_by_role("heading", level=1, name="Items")
        self.table = DataTable(page.get_by_role("table"))
        self.confirm_delete = Modal(page, "Delete item?")

    def open(self) -> None:
        self._page.goto("/items")

    def request_delete(self, name: str) -> None:
        """Opens the confirm dialog for a row without confirming it."""
        self.table.row(name).get_by_role("button", name=f"Delete {name}").click()

    def delete(self, name: str) -> None:
        self.request_delete(name)
        self.confirm_delete.confirm()
