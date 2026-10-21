"""Configuration: validated at start-up, every problem at once; the live page list too."""

import pytest
from pydantic import ValidationError

from framework.config.live_pages import LivePage, LivePages
from framework.config.record_mode import RecordMode
from framework.config.settings import ConfigError, Settings, load_settings, url

pytestmark = pytest.mark.unit


def test_defaults_are_valid_and_overridable_by_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RECORD_MODE", "all")
    monkeypatch.setenv("TEST_RETRIES", "0")
    monkeypatch.setenv("RUN_ID", "unit-1")

    settings = load_settings()

    assert settings.record_mode is RecordMode.ALL
    assert settings.test_retries == 0
    assert settings.run_id == "unit-1"
    assert url(settings.booker_base_url) == "https://restful-booker.herokuapp.com"
    assert settings.timeout == (5.0, 15.0)


def test_every_invalid_value_is_reported_at_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RECORD_MODE", "sometimes")
    monkeypatch.setenv("TEST_RETRIES", "5")
    monkeypatch.setenv("RUN_ID", "bad id!")
    monkeypatch.setenv("SAUCE_BASE_URL", "http://www.saucedemo.com")

    with pytest.raises(ConfigError) as error:
        load_settings()

    message = str(error.value)
    for field in ("RECORD_MODE", "TEST_RETRIES", "RUN_ID", "SAUCE_BASE_URL"):
        assert field in message
    assert "https" in message


def test_secrets_are_not_printed() -> None:
    settings = Settings(_env_file=None)  # type: ignore[call-arg]

    assert "secret_sauce" not in repr(settings)
    assert "password123" not in repr(settings)


def test_record_mode_decides_what_is_kept() -> None:
    assert RecordMode.FAILURES.keeps(failed=True)
    assert not RecordMode.FAILURES.keeps(failed=False)
    assert RecordMode.ALL.keeps(failed=False)
    assert not RecordMode.OFF.keeps(failed=True)
    assert RecordMode.FAILURES.playwright_option(failure_value="retain-on-failure") == (
        "retain-on-failure"
    )
    assert RecordMode.ALL.playwright_option(failure_value="only-on-failure") == "on"
    assert RecordMode.OFF.playwright_option(failure_value="only-on-failure") == "off"


def test_the_bundled_live_page_list_is_valid() -> None:
    live = LivePages.load()

    assert len(live.pages) >= 3
    assert all(not p.path.startswith("/login") for p in live.pages)
    assert set(live.responsive_pages) <= {p.path for p in live.pages}
    assert live.widths == [1440, 1024, 768, 390]
    assert live.page("/").heading_pattern.search("ANYONE CAN KNOCK")


def test_the_live_page_list_refuses_the_sign_in_page_and_bad_patterns() -> None:
    with pytest.raises(ValidationError) as error:
        LivePages(
            pages=[
                LivePage(path="/", title="Home", heading="Hi"),
            ],
            responsive_pages=[],
            widths=[200],
        )
    assert "between 320 and 3840" in str(error.value)

    with pytest.raises(ValidationError, match="sign-in page"):
        LivePage(path="/login", title="Sign in", heading="Welcome")
    with pytest.raises(ValidationError, match="not a valid pattern"):
        LivePage(path="/", title="Home", heading="(unclosed")
