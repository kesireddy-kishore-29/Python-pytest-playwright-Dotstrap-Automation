"""Any public page of the live site, read the way a visitor's browser reads it. Read-only: it
never types, submits or signs in."""

from dataclasses import dataclass
from typing import Any

from playwright.sync_api import Locator, Page, Response


@dataclass(frozen=True)
class SecurityHeaders:
    """The security headers a test checks. The policy (CSP) is reduced to present or absent:
    its text names infrastructure, so it is never kept or printed."""

    strict_transport_security: str
    content_type_options: str
    referrer_policy: str
    permissions_policy: str
    frame_options: str
    has_content_security_policy: bool

    @classmethod
    def of(cls, response: Response) -> "SecurityHeaders":
        headers = response.headers  # lower-case names
        return cls(
            strict_transport_security=headers.get("strict-transport-security", ""),
            content_type_options=headers.get("x-content-type-options", ""),
            referrer_policy=headers.get("referrer-policy", ""),
            permissions_policy=headers.get("permissions-policy", ""),
            frame_options=headers.get("x-frame-options", ""),
            has_content_security_policy="content-security-policy" in headers,
        )


@dataclass(frozen=True)
class Overflow:
    """Page wider than its viewport, and up to five elements that push it out."""

    document_width: int
    viewport_width: int
    offenders: list[str]


_OVERFLOW_SCRIPT = """() => {
  const viewportWidth = document.documentElement.clientWidth;
  const offenders = [];
  for (const el of document.body.querySelectorAll('*')) {
    const rect = el.getBoundingClientRect();
    if (rect.width > 0 && rect.right > viewportWidth + 1) {
      offenders.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '')
        + ' (right edge ' + Math.round(rect.right) + 'px)');
    }
  }
  return { documentWidth: document.documentElement.scrollWidth, viewportWidth,
           offenders: offenders.slice(0, 5) };
}"""


class PublicPage:
    def __init__(self, page: Page) -> None:
        self._page = page
        # A site may have more than one level-1 heading; the first is the page's headline.
        self.heading: Locator = page.get_by_role("heading", level=1).first

    def open(self, path: str) -> Response | None:
        return self._page.goto(path, wait_until="load")

    def use_viewport(self, width: int, height: int = 900) -> None:
        """An exact viewport, as a phone or a small laptop would have it."""
        self._page.set_viewport_size({"width": width, "height": height})

    def viewport_width(self) -> int:
        return int(self._page.evaluate("() => window.innerWidth"))

    def user_agent(self) -> str:
        """What the browser tells the site it is (the live smoke names this project in it)."""
        return str(self._page.evaluate("() => navigator.userAgent"))

    def horizontal_overflow(self) -> Overflow:
        raw: dict[str, Any] = self._page.evaluate(_OVERFLOW_SCRIPT)
        return Overflow(
            document_width=int(raw["documentWidth"]),
            viewport_width=int(raw["viewportWidth"]),
            offenders=[str(o) for o in raw["offenders"]],
        )
