"""Fails on purpose (marker demo_failure), to show the evidence a UI failure leaves: video,
redacted trace, screenshots, DOM, console and HAR. Never part of a gating run."""

import pytest
from playwright.sync_api import Page, expect

from framework.data.products import PRODUCTS
from framework.ui.pages.demo import DemoPage
from framework.ui.pages.sauce import InventoryPage

pytestmark = [pytest.mark.ui, pytest.mark.demo_failure]


@pytest.mark.feature("FEAT-DEMO-01")
def test_demo_a_renamed_test_id_is_a_missing_element(sauce_page: Page) -> None:
    """demo: a renamed test id is a missing element."""
    inventory = InventoryPage(sauce_page)
    inventory.open()
    inventory.add_to_cart(PRODUCTS["backpack"])

    expect(DemoPage(sauce_page).renamed_cart_badge).to_have_text("1")


@pytest.mark.feature("FEAT-DEMO-01")
def test_demo_a_wrong_expectation_fails_an_assertion(sauce_page: Page) -> None:
    """demo: a wrong expectation fails an assertion."""
    inventory = InventoryPage(sauce_page)
    inventory.open()

    expect(inventory.title).to_have_text("Product catalogue")
