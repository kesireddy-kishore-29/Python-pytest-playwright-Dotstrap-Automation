"""Run configuration, validated once at start-up.

Every field can be set by an environment variable of the same name in upper case
(`booker_base_url` -> `BOOKER_BASE_URL`) or in a `.env` file. pydantic reports every invalid value
at once, so a broken CI configuration costs one run, not one run per mistake.
"""

from datetime import datetime
from pathlib import Path
from typing import Annotated

from pydantic import Field, HttpUrl, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from framework.config.record_mode import RecordMode


def _default_run_id() -> str:
    return "local-" + datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


class Settings(BaseSettings):
    """Targets, credentials of the public demo targets, and run switches."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)

    # Public practice API. Its credentials are published in its own documentation.
    booker_base_url: HttpUrl = HttpUrl("https://restful-booker.herokuapp.com")
    booker_username: str = "admin"
    booker_password: SecretStr = SecretStr("password123")

    # Public demo shop. Its credentials are printed on its own sign-in page.
    sauce_base_url: HttpUrl = HttpUrl("https://www.saucedemo.com")
    sauce_username: str = "standard_user"
    sauce_password: SecretStr = SecretStr("secret_sauce")

    # The flagships' self-hosted services; tests that need them skip when they are not running.
    reference_base_url: HttpUrl = HttpUrl("http://localhost:7070")
    app_base_url: HttpUrl = HttpUrl("http://localhost:4173")

    # The author's production site: public pages only (live suite).
    live_base_url: HttpUrl = HttpUrl("https://dotstrap.com")

    record_mode: RecordMode = RecordMode.FAILURES
    run_id: Annotated[str, Field(pattern=r"^[A-Za-z0-9._-]{1,80}$")] = Field(
        default_factory=_default_run_id
    )
    evidence_root: Path = Path("run-evidence")
    test_retries: Annotated[int, Field(ge=0, le=2)] = 2
    connect_timeout_seconds: Annotated[float, Field(gt=0, le=30)] = 5.0
    read_timeout_seconds: Annotated[float, Field(gt=0, le=60)] = 15.0

    @field_validator("booker_base_url", "sauce_base_url", "live_base_url")
    @classmethod
    def _https_for_public_targets(cls, url: HttpUrl) -> HttpUrl:
        if url.scheme != "https":
            raise ValueError("public targets must be reached over https")
        return url

    @property
    def timeout(self) -> tuple[float, float]:
        """(connect, read) timeout for every HTTP call."""
        return (self.connect_timeout_seconds, self.read_timeout_seconds)


def url(base: HttpUrl) -> str:
    """A base URL as a string without the trailing slash pydantic adds."""
    return str(base).rstrip("/")


class ConfigError(ValueError):
    """Raised at start-up with every configuration problem listed."""


def load_settings() -> Settings:
    """Settings from the environment, or a ConfigError naming every invalid value."""
    try:
        return Settings()
    except ValidationError as error:
        problems = [
            f"{'.'.join(str(p) for p in e['loc']).upper()}: {e['msg']}" for e in error.errors()
        ]
        raise ConfigError(
            "Invalid test configuration (environment variables or .env):\n  - "
            + "\n  - ".join(problems)
        ) from error
