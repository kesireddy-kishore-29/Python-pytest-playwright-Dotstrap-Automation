"""Read-only smoke of the author's own production site, dotstrap.com: public pages only, no
sign-in, no forms, no writes, one worker, a user agent that names this project. Nightly and on
demand, never on pull requests, never gating. Pages and expected text: live_pages.json."""

import re

import pytest
from playwright.sync_api import expect

from framework.config.live_pages import LivePages
from framework.ui.pages.live import PublicPage, SecurityHeaders
from framework.ui.visit import USER_AGENT_SUFFIX, Visit

pytestmark = [pytest.mark.live, pytest.mark.ui]

LIVE = LivePages.load()


@pytest.mark.feature("FEAT-LIVE-01")
@pytest.mark.parametrize("path", [page.path for page in LIVE.pages])
def test_a_public_page_answers_200_and_shows_its_heading(visit: Visit, path: str) -> None:
    """A public page answers 200 and shows its heading."""
    expected = LIVE.page(path)
    public = PublicPage(visit.page)

    response = public.open(path)

    assert response is not None
    assert response.status == 200
    expect(visit.page).to_have_title(expected.title_pattern)
    expect(public.heading).to_have_text(expected.heading_pattern)
    assert public.user_agent().endswith(USER_AGENT_SUFFIX)


@pytest.mark.feature("FEAT-LIVE-02")
def test_no_public_page_logs_a_console_error_or_fails_a_request(visit: Visit) -> None:
    """No public page logs a console error or fails a request."""
    public = PublicPage(visit.page)

    for page in LIVE.pages:
        public.open(page.path)
        expect(public.heading).to_be_visible()

    assert visit.console.errors == []
    assert visit.failed_requests == []


@pytest.mark.feature("FEAT-LIVE-03")
def test_the_site_sends_the_security_headers(visit: Visit) -> None:
    """The site sends the expected security headers."""
    response = PublicPage(visit.page).open("/")
    assert response is not None

    headers = SecurityHeaders.of(response)

    assert re.match(r"max-age=\d{6,}", headers.strict_transport_security)
    assert headers.content_type_options == "nosniff"
    assert headers.referrer_policy != ""
    assert headers.permissions_policy != ""
    assert headers.has_content_security_policy, "Content-Security-Policy is missing"
    assert re.match(r"SAMEORIGIN|DENY", headers.frame_options)


@pytest.mark.feature("FEAT-LIVE-05")
@pytest.mark.parametrize("width", LIVE.widths)
def test_the_responsive_pages_have_no_horizontal_overflow(visit: Visit, width: int) -> None:
    """The responsive pages have no horizontal overflow at this width."""
    public = PublicPage(visit.page)
    public.use_viewport(width)

    problems = []
    for path in LIVE.responsive_pages:
        public.open(path)
        overflow = public.horizontal_overflow()
        if public.viewport_width() != width:
            problems.append(f"{path}: the viewport is not {width} px wide")
        if overflow.document_width > overflow.viewport_width:
            problems.append(
                f"{path}: {overflow.document_width} px wide in a {overflow.viewport_width} px "
                f"viewport, pushed out by {overflow.offenders}"
            )

    assert problems == []
