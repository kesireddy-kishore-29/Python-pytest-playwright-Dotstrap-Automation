"""Sauce Demo cart and checkout, on a saved signed-in session."""

import re

import pytest
from playwright.sync_api import Page, expect

from framework.data.factories import a_customer
from framework.data.products import PRODUCTS
from framework.ui.flows import checkout_with
from framework.ui.pages.sauce import CheckoutCompletePage, CheckoutOverviewPage, InventoryPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.feature("FEAT-CART-01")
def test_the_badge_follows_adding_and_removing_items(sauce_page: Page) -> None:
    """Adding and removing items keeps the badge count right."""
    inventory = InventoryPage(sauce_page)
    inventory.open()

    inventory.add_to_cart(PRODUCTS["backpack"])
    inventory.add_to_cart(PRODUCTS["bike_light"])
    expect(inventory.header.cart_badge).to_have_text("2")

    inventory.remove_from_cart(PRODUCTS["backpack"])
    expect(inventory.header.cart_badge).to_have_text("1")

    inventory.remove_from_cart(PRODUCTS["bike_light"])
    expect(inventory.header.cart_badge).to_be_hidden()


@pytest.mark.smoke
@pytest.mark.feature("FEAT-CHECKOUT-01")
def test_a_full_checkout_completes_with_a_confirmation(sauce_page: Page) -> None:
    """A full checkout completes with a confirmation."""
    checkout_with(sauce_page, [PRODUCTS["backpack"]], a_customer())

    CheckoutOverviewPage(sauce_page).finish.click()

    complete = CheckoutCompletePage(sauce_page)
    expect(complete.heading).to_be_visible()
    expect(sauce_page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    complete.back_home.click()
    expect(InventoryPage(sauce_page).header.cart_badge).to_be_hidden()


@pytest.mark.feature("FEAT-CHECKOUT-03")
def test_the_order_summary_adds_up(sauce_page: Page) -> None:
    """The order summary adds up: item total + tax = total."""
    products = [PRODUCTS["backpack"], PRODUCTS["fleece_jacket"], PRODUCTS["onesie"]]

    checkout_with(sauce_page, products, a_customer())

    overview = CheckoutOverviewPage(sauce_page)
    expect(overview.total).to_be_visible()
    item_total, tax, total = overview.amounts()
    assert sorted(overview.item_prices()) == sorted(p.price for p in products)
    assert item_total == sum(p.price for p in products)
    assert tax > 0
    assert total == item_total + tax
