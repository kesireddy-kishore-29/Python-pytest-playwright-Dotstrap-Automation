"""Page-level evidence and the console-error guard, shared by the UI and live fixtures.

Playwright (through pytest-playwright) keeps the video, the trace and the failure screenshot; this
adds what only the open page can give: the DOM, a full-page screenshot and the console.
"""

import logging
import re
from collections.abc import Sequence
from pathlib import Path

from playwright.sync_api import ConsoleMessage, Error, Page

from framework.core.redaction import redact_text

LOG = logging.getLogger(__name__)


class ConsoleWatch:
    """Every console message and uncaught page error, as text, from the moment it is attached."""

    def __init__(self, page: Page) -> None:
        self.lines: list[str] = []
        self.errors: list[str] = []
        page.on("console", self._on_console)
        page.on("pageerror", self._on_page_error)

    def _on_console(self, message: ConsoleMessage) -> None:
        location = message.location.get("url", "")
        line = f"[{message.type}] {message.text}" + (f" ({location})" if location else "")
        self.lines.append(line)
        if message.type == "error":
            self.errors.append(line)

    def _on_page_error(self, error: Error) -> None:
        line = f"[pageerror] {error.message}"
        self.lines.append(line)
        self.errors.append(line)

    def unexpected_errors(self, allowed: Sequence[re.Pattern[str]]) -> list[str]:
        return [e for e in self.errors if not any(p.search(e) for p in allowed)]


def capture_page(page: Page, directory: Path, console: ConsoleWatch) -> list[str]:
    """Writes page-source.html, fullpage.png and console.log; returns the files written. A
    capture that fails (the page already closed) is logged and skipped, never fatal."""
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    try:
        (directory / "page-source.html").write_text(redact_text(page.content()), encoding="utf-8")
        written.append("page-source.html")
    except Error as error:
        LOG.debug("page source not captured: %s", error.message)
    try:
        page.screenshot(path=directory / "fullpage.png", full_page=True, timeout=10_000)
        written.append("fullpage.png")
    except Error as error:
        LOG.debug("full-page screenshot not captured: %s", error.message)
    text = "\n".join(redact_text(line) for line in console.lines) or "(no console output)"
    (directory / "console.log").write_text(text + "\n", encoding="utf-8")
    written.append("console.log")
    return written
