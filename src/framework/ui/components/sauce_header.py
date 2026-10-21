"""Sauce Demo's header: the cart link with its badge, and the burger menu."""

from playwright.sync_api import Locator, Page


class SauceHeader:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.cart_link: Locator = page.get_by_test_id("shopping-cart-link")
        # A count has no role or name; the test id is the right handle for it.
        self.cart_badge: Locator = page.get_by_test_id("shopping-cart-badge")
        self.menu_button: Locator = page.get_by_role("button", name="Open Menu")

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        """The menu entries are <a> without href, so they have no link role (a finding in
        docs/known-issues.md); the site's test id is the fallback."""
        self.menu_button.click()
        self._page.get_by_test_id("logout-sidebar-link").click()
