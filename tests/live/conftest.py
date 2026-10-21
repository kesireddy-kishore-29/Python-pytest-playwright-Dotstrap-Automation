"""The live smoke's browser: a plain context with a user agent that names this project, and no
video, no trace and no HAR (never recorded for the live site). Failure evidence is a screenshot,
the page source and the console, kept as a short-lived CI artifact and never committed."""

from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser

from framework.config.live_pages import LivePages
from framework.config.settings import Settings, url
from framework.evidence.browser import ConsoleWatch, capture_page
from framework.evidence.plugin import Attempt, phase_failed
from framework.ui.visit import USER_AGENT_SUFFIX, Visit


@pytest.fixture(scope="session")
def live_pages() -> LivePages:
    return LivePages.load()


@pytest.fixture(scope="session")
def live_user_agent(browser: Browser) -> str:
    context = browser.new_context()
    try:
        return str(context.new_page().evaluate("() => navigator.userAgent")) + USER_AGENT_SUFFIX
    finally:
        context.close()


@pytest.fixture
def visit(
    browser: Browser,
    live_user_agent: str,
    settings: Settings,
    evidence: Attempt,
    request: pytest.FixtureRequest,
) -> Iterator[Visit]:
    context = browser.new_context(base_url=url(settings.live_base_url), user_agent=live_user_agent)
    page = context.new_page()
    tab = Visit(page, ConsoleWatch(page))
    tab.watch_requests()
    yield tab
    if settings.record_mode.keeps(failed=phase_failed(request.node, "setup", "call")):
        capture_page(page, evidence.directory, tab.console)
        page.screenshot(path=evidence.directory / "screenshot.png")
    context.close()
