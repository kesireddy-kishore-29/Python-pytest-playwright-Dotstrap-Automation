"""Multi-page journeys as single calls. A flow chains page-object calls; it holds no locators and
makes no assertions."""

from collections.abc import Iterable

from playwright.sync_api import Page

from framework.data.factories import Customer
from framework.data.products import Product
from framework.ui.pages.sauce import CartPage, CheckoutInformationPage, InventoryPage


def checkout_with(page: Page, products: Iterable[Product], customer: Customer) -> None:
    """Adds the products, opens the cart, starts checkout and enters the customer. Ends on the
    order overview (or on step one with an error, for an incomplete customer)."""
    inventory = InventoryPage(page)
    inventory.open()
    for product in products:
        inventory.add_to_cart(product)
    inventory.header.open_cart()
    CartPage(page).checkout.click()
    information = CheckoutInformationPage(page)
    information.fill(customer)
    information.continue_button.click()
