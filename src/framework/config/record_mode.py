"""How much evidence a run keeps. The same three values in every repository of the family."""

from enum import StrEnum


class RecordMode(StrEnum):
    """`failures` (pull requests, default), `all` (nightly and local analysis), `off`."""

    FAILURES = "failures"
    ALL = "all"
    OFF = "off"

    def keeps(self, *, failed: bool) -> bool:
        """Whether an attempt with this outcome keeps its evidence."""
        return self is RecordMode.ALL or (self is RecordMode.FAILURES and failed)

    def playwright_option(self, *, failure_value: str) -> str:
        """The pytest-playwright option for this mode (--video, --tracing or --screenshot)."""
        return {RecordMode.ALL: "on", RecordMode.FAILURES: failure_value, RecordMode.OFF: "off"}[
            self
        ]
