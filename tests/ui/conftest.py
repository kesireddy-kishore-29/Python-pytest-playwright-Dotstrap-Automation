"""UI fixtures: a saved signed-in session, pages with a console-error guard and page-level
evidence, and a throwaway account on the UI flagship's app for the hybrid test."""

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, expect

from framework.api.clients import AppClient, reachable
from framework.api.clients.app import SESSION_COOKIE
from framework.api.fixture_types import AppAccount
from framework.config.record_mode import RecordMode
from framework.config.settings import Settings, url
from framework.core.http import ApiSession
from framework.data.factories import unique_email
from framework.evidence.browser import ConsoleWatch, capture_page
from framework.evidence.plugin import Attempt, phase_failed
from framework.ui.pages.sauce import LoginPage

# Sauce Demo answers 404 to a direct load of its pages (a single-page-app fallback) while still
# rendering them, and Chrome logs it. That exact message, and nothing else, is allowed.
SAUCE_DEEP_LINK_404 = re.compile(
    r"status of 404 \(\) \(https://www\.saucedemo\.com/[a-z-]+\.html(\?[^)]*)?\)$"
)


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright: Playwright) -> None:
    """Both targets publish `data-test` attributes; get_by_test_id reads that one."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def browser_context_args(
    browser_context_args: dict[str, Any], settings: Settings, evidence: Attempt
) -> dict[str, Any]:
    """pytest-playwright's context options plus a HAR per attempt (redacted when kept)."""
    args = dict(browser_context_args)
    if settings.record_mode is not RecordMode.OFF:
        evidence.directory.mkdir(parents=True, exist_ok=True)
        args["record_har_path"] = str(evidence.directory / "network.har")
        args["record_har_content"] = "omit"
    return args


def _open_page(
    context: BrowserContext,
    request: pytest.FixtureRequest,
    settings: Settings,
    evidence: Attempt,
    allowed_console_errors: list[re.Pattern[str]],
) -> Iterator[Page]:
    page = context.new_page()
    console = ConsoleWatch(page)
    yield page
    unexpected = console.unexpected_errors(allowed_console_errors)
    failed = phase_failed(request.node, "setup", "call") or bool(unexpected)
    if settings.record_mode.keeps(failed=failed):
        capture_page(page, evidence.directory, console)
    assert not unexpected, f"console errors during the test: {unexpected}"


# ---- Sauce Demo ---------------------------------------------------------------------------------


@pytest.fixture(scope="session")
def sauce_session(
    browser: Browser, settings: Settings, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Signs in through the form once per worker and saves the session (storage state)."""
    context = browser.new_context(base_url=url(settings.sauce_base_url))
    page = context.new_page()
    login = LoginPage(page)
    login.open()
    login.sign_in(settings.sauce_username, settings.sauce_password.get_secret_value())
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    path = tmp_path_factory.mktemp("auth") / "sauce.json"
    context.storage_state(path=path)
    context.close()
    return path


@pytest.fixture
def sauce_page(
    new_context: Any,
    sauce_session: Path,
    request: pytest.FixtureRequest,
    settings: Settings,
    evidence: Attempt,
) -> Iterator[Page]:
    """A page already signed in to Sauce Demo (the saved session; no form)."""
    context = new_context(base_url=url(settings.sauce_base_url), storage_state=sauce_session)
    yield from _open_page(context, request, settings, evidence, [SAUCE_DEEP_LINK_404])


@pytest.fixture
def signed_out_page(
    new_context: Any, request: pytest.FixtureRequest, settings: Settings, evidence: Attempt
) -> Iterator[Page]:
    """A Sauce Demo page with no session, for the sign-in tests."""
    context = new_context(base_url=url(settings.sauce_base_url))
    yield from _open_page(context, request, settings, evidence, [SAUCE_DEEP_LINK_404])


# ---- the UI flagship's app (self-hosted, port 4173) --------------------------------------------


@pytest.fixture
def app_account(settings: Settings, evidence: Attempt) -> Iterator[AppAccount]:
    base = url(settings.app_base_url)
    if not reachable(f"{base}/api/health"):
        pytest.skip(
            f"The UI flagship's app is not reachable at {base} "
            "(start it with: cd ui-automation-framework && npm run sut)"
        )
    session = ApiSession("sut-ui", base, settings.timeout, evidence.transcript)
    client = AppClient(session)
    email = unique_email()
    password = f"pw-{email}"
    client.create_user(email, password)
    account = AppAccount(client, email, password, client.token(email, password), [])
    yield account
    for item_id in account.seeded:
        client.delete_item(account.token, item_id)
    left = [i.id for i in account.items() if i.id in account.seeded]
    assert left == [], f"seeded items not deleted: {left}"
    client.delete_me(account.token)
    assert client.sign_in(email, password).status_code == 401, "test account still signs in"
    session.close()


@pytest.fixture
def app_page(
    new_context: Any,
    app_account: AppAccount,
    request: pytest.FixtureRequest,
    settings: Settings,
    evidence: Attempt,
) -> Iterator[Page]:
    """A page of the UI flagship's app, signed in as the test's account (session cookie)."""
    base = url(settings.app_base_url)
    state = {
        "cookies": [
            {
                "name": SESSION_COOKIE,
                "value": app_account.token,
                "domain": urlsplit(base).hostname,
                "path": "/",
                "expires": -1,
                "httpOnly": True,
                "secure": False,
                "sameSite": "Lax",
            }
        ],
        "origins": [],
    }
    context = new_context(base_url=base, storage_state=state)
    yield from _open_page(context, request, settings, evidence, [])
