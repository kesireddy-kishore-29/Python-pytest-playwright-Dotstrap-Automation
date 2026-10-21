"""Validated configuration: settings, record mode and the live page list."""

from framework.config.live_pages import LivePage, LivePages
from framework.config.record_mode import RecordMode
from framework.config.settings import Settings, load_settings

__all__ = ["LivePage", "LivePages", "RecordMode", "Settings", "load_settings"]
