"""Deliberately wrong expectations about Sauce Demo, used only by the deliberate-failure demo
(marker demo_failure) to show what evidence a failure leaves. Nothing else may use this."""

from playwright.sync_api import Locator, Page


class DemoPage:
    def __init__(self, page: Page) -> None:
        # A test id the page does not have: what a renamed attribute looks like to a test.
        self.renamed_cart_badge: Locator = page.get_by_test_id("cart-count")
