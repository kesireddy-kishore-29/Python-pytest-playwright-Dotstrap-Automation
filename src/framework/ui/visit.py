"""A visitor's browser tab on the live site: the page, its console and the requests that failed.
Used by the live smoke, which also names this project in its user agent."""

from dataclasses import dataclass, field

from playwright.sync_api import Page, Request, Response

from framework.evidence.browser import ConsoleWatch

USER_AGENT_SUFFIX = " python-pytest-automation-framework (portfolio smoke test)"


@dataclass
class Visit:
    """A visitor's browser tab: the page, its console, and every request that failed."""

    page: Page
    console: ConsoleWatch
    failed_requests: list[str] = field(default_factory=list)

    def watch_requests(self) -> None:
        self.page.on("response", self._on_response)
        self.page.on("requestfailed", self._on_failed)

    def _on_response(self, response: Response) -> None:
        if response.status >= 400:
            self.failed_requests.append(
                f"{response.status} {response.request.method} {response.url}"
            )

    def _on_failed(self, request: Request) -> None:
        reason = request.failure or "failed"
        # ERR_ABORTED is the browser cancelling its own request (navigation, prefetch).
        if "ERR_ABORTED" not in reason:
            self.failed_requests.append(f"{reason} {request.method} {request.url}")
