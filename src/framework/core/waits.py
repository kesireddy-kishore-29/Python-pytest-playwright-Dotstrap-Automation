"""The one bounded poll for conditions outside the browser (an API state, a rate-limit window).

Browser waits are Playwright's web-first assertions. Everything else that must wait polls a
condition here with a deadline and a description; a fixed sleep anywhere else is refused by
ruff (TID251) and by tests/unit/test_policies.py.
"""

import time
from collections.abc import Callable


class WaitTimeoutError(AssertionError):
    """The condition did not become true before the deadline."""


def wait_until[T](
    description: str,
    probe: Callable[[], T | None],
    *,
    timeout: float,
    interval: float = 0.25,
) -> T:
    """Calls `probe` until it returns something other than None or False, then returns it.

    Raises WaitTimeoutError naming `description` and the last value seen.
    """
    deadline = time.monotonic() + timeout
    last: T | None = None
    while True:
        last = probe()
        if last is not None and last is not False:
            return last
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise WaitTimeoutError(f"waited {timeout:g} s for {description}; last value: {last!r}")
        # The only pause in the framework: between polls of a bounded wait.
        time.sleep(min(interval, remaining))  # noqa: TID251
