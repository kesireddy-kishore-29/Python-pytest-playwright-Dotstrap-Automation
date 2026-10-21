"""Sauce Demo sign-in. The only tests that use the form; the others reuse a saved session."""

import re

import pytest
from playwright.sync_api import Page, expect

from framework.config.settings import Settings
from framework.ui.pages.sauce import InventoryPage, LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.feature("FEAT-LOGIN-01")
def test_valid_credentials_reach_the_inventory(signed_out_page: Page, settings: Settings) -> None:
    """Valid credentials reach the inventory."""
    login = LoginPage(signed_out_page)
    login.open()

    login.sign_in(settings.sauce_username, settings.sauce_password.get_secret_value())

    expect(signed_out_page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(signed_out_page).title).to_have_text("Products")


@pytest.mark.feature("FEAT-LOGIN-02")
@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        pytest.param(
            "standard_user", "not-the-password", "do not match any user", id="wrong password"
        ),
        pytest.param("nobody_here", "secret_sauce", "do not match any user", id="unknown user"),
        pytest.param("", "secret_sauce", "Username is required", id="empty username"),
    ],
)
def test_invalid_credentials_are_refused_with_a_specific_message(
    signed_out_page: Page, username: str, password: str, message: str
) -> None:
    """Invalid credentials are refused with a specific message."""
    login = LoginPage(signed_out_page)
    login.open()

    login.sign_in(username, password)

    expect(login.error).to_contain_text(message)
    expect(signed_out_page).not_to_have_url(re.compile("inventory"))


@pytest.mark.feature("FEAT-LOGIN-03")
def test_a_locked_out_user_is_refused(signed_out_page: Page, settings: Settings) -> None:
    """A locked-out user is refused with the lock-out message."""
    login = LoginPage(signed_out_page)
    login.open()

    login.sign_in("locked_out_user", settings.sauce_password.get_secret_value())

    expect(login.error).to_contain_text("this user has been locked out")
