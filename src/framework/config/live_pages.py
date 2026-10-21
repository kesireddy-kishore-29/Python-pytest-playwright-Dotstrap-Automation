"""The live smoke's page list and expected text: one file to edit when the live site changes."""

import re
from functools import cached_property
from importlib import resources

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LivePage(BaseModel):
    """One public page: its path, and what its title and first heading must say."""

    model_config = ConfigDict(frozen=True)

    path: str
    title: str
    heading: str

    @field_validator("path")
    @classmethod
    def _public_path(cls, path: str) -> str:
        if not path.startswith("/") or path.startswith("/login"):
            raise ValueError(f"'{path}' must start with / and must not be the sign-in page")
        return path

    @field_validator("title", "heading")
    @classmethod
    def _valid_pattern(cls, pattern: str) -> str:
        try:
            re.compile(pattern)
        except re.error as error:
            raise ValueError(f"not a valid pattern: {error}") from error
        return pattern

    @cached_property
    def title_pattern(self) -> re.Pattern[str]:
        return re.compile(self.title, re.IGNORECASE)

    @cached_property
    def heading_pattern(self) -> re.Pattern[str]:
        return re.compile(self.heading, re.IGNORECASE)


class LivePages(BaseModel):
    """The whole list, validated like the rest of the configuration."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    pages: list[LivePage] = Field(min_length=1)
    responsive_pages: list[str]
    widths: list[int]

    @field_validator("widths")
    @classmethod
    def _sane_widths(cls, widths: list[int]) -> list[int]:
        bad = [w for w in widths if not 320 <= w <= 3840]
        if bad:
            raise ValueError(f"widths {bad} must be between 320 and 3840")
        return widths

    @classmethod
    def load(cls) -> "LivePages":
        text = resources.files("framework.config").joinpath("live_pages.json").read_text("utf-8")
        return cls.model_validate_json(text)

    def page(self, path: str) -> LivePage:
        for page in self.pages:
            if page.path == path:
                return page
        raise KeyError(f"No live page {path} in live_pages.json")
