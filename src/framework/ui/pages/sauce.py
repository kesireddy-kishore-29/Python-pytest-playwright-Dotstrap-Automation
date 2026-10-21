"""Sauce Demo (https://www.saucedemo.com) page objects. The browser context's base URL is the
shop, so pages open by path."""

from decimal import Decimal

from playwright.sync_api import Locator, Page

from framework.data.factories import Customer
from framework.data.products import Product
from framework.ui.components.sauce_header import SauceHeader
from framework.ui.money import money


class LoginPage:
    """Sign-in (`/`)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.submit = page.get_by_role("button", name="Login")
        self.error = page.get_by_test_id("error")

    def open(self) -> None:
        self._page.goto("/")

    def sign_in(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()


class InventoryPage:
    """The product list (`/inventory.html`)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.header = SauceHeader(page)
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")

    def open(self) -> None:
        self._page.goto("/inventory.html")

    def item(self, product: Product) -> Locator:
        return self.items.filter(has_text=product.name)

    def add_to_cart(self, product: Product) -> None:
        self.item(product).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product: Product) -> None:
        self.item(product).get_by_role("button", name="Remove").click()

    def names(self) -> list[str]:
        return self._page.get_by_test_id("inventory-item-name").all_inner_texts()


class CartPage:
    """The cart (`/cart.html`)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.checkout = page.get_by_role("button", name="Checkout")

    def names(self) -> list[str]:
        return self._page.get_by_test_id("inventory-item-name").all_inner_texts()


class CheckoutInformationPage:
    """Checkout step one: who is buying (`/checkout-step-one.html`)."""

    def __init__(self, page: Page) -> None:
        self.first_name = page.get_by_placeholder("First Name")
        self.last_name = page.get_by_placeholder("Last Name")
        self.postal_code = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.error = page.get_by_test_id("error")

    def fill(self, customer: Customer) -> None:
        for field, value in (
            (self.first_name, customer.first_name),
            (self.last_name, customer.last_name),
            (self.postal_code, customer.postal_code),
        ):
            if value is not None:
                field.fill(value)


class CheckoutOverviewPage:
    """Checkout step two: review (`/checkout-step-two.html`)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.item_total = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish = page.get_by_role("button", name="Finish")

    def item_prices(self) -> list[Decimal]:
        texts = self._page.get_by_test_id("inventory-item-price").all_inner_texts()
        return [money(t) for t in texts]

    def amounts(self) -> tuple[Decimal, Decimal, Decimal]:
        """(item total, tax, total) as shown."""
        return (
            money(self.item_total.inner_text()),
            money(self.tax.inner_text()),
            money(self.total.inner_text()),
        )


class CheckoutCompletePage:
    """Order placed (`/checkout-complete.html`)."""

    def __init__(self, page: Page) -> None:
        self.heading = page.get_by_role("heading", name="Thank you for your order!")
        self.back_home = page.get_by_role("button", name="Back Home")
