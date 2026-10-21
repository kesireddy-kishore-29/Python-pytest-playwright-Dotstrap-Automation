"""Fixtures shared by every suite. The framework's plugin does the start-up checks, retries,
traceability and evidence (src/framework/evidence/plugin.py)."""

import pytest

# The framework's own checks (fixture teardowns, cleanups) get pytest's assertion messages too.
pytest.register_assert_rewrite("framework")

from framework.config.settings import Settings  # noqa: E402 - after register_assert_rewrite
from framework.evidence.plugin import settings_of  # noqa: E402

pytest_plugins = ["framework.evidence.plugin"]


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    """The validated run configuration."""
    return settings_of(pytestconfig)
