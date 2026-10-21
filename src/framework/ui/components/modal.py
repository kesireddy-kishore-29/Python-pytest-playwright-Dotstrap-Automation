"""A modal dialog, found by its role and accessible name."""

from playwright.sync_api import Locator, Page


class Modal:
    def __init__(self, page: Page, name: str) -> None:
        self.root: Locator = page.get_by_role("dialog", name=name)

    def confirm(self, label: str = "Delete") -> None:
        self.root.get_by_role("button", name=label, exact=True).click()

    def cancel(self) -> None:
        self.root.get_by_role("button", name="Cancel", exact=True).click()
