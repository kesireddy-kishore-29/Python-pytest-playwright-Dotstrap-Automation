"""Stable names for a test: ID, title, suite, evidence slug, feature IDs and tags."""

import re
from dataclasses import dataclass
from pathlib import Path

import pytest

FEATURE_ID = re.compile(r"^FEAT-[A-Z0-9]+-\d{2}$")
TAG_MARKERS = ("smoke", "regression", "api", "ui", "live", "demo_failure", "quarantine")


def slugify(text: str, limit: int = 90) -> str:
    """Lower case, hyphenated, bounded: safe in paths on every operating system."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit].rstrip("-")


@dataclass(frozen=True)
class TestIdentity:
    __test__ = False  # not a test class, whatever pytest's name rules say

    test_id: str
    title: str
    suite: str
    slug: str
    feature_ids: tuple[str, ...]
    tags: tuple[str, ...]

    @classmethod
    def of(cls, item: pytest.Item) -> "TestIdentity":
        relative = Path(item.path).resolve().relative_to(Path(item.config.rootpath).resolve())
        parts = relative.parts
        suite = parts[1] if len(parts) > 2 and parts[0] == "tests" else relative.stem
        function = getattr(item, "function", None)
        doc = (function.__doc__ or "").strip().splitlines() if function else []
        base_name = item.name.split("[", 1)[0]
        title = doc[0].rstrip(".") if doc else base_name.removeprefix("test_").replace("_", " ")
        callspec = getattr(item, "callspec", None)
        if callspec is not None:
            title += f" [{callspec.id}]"
        features = tuple(fid for marker in item.iter_markers("feature") for fid in marker.args)
        tags = tuple(tag for tag in TAG_MARKERS if item.get_closest_marker(tag) is not None)
        return cls(
            test_id=item.nodeid,
            title=title,
            suite=suite,
            slug=slugify(
                f"{relative.stem.removeprefix('test_')}-{item.name.removeprefix('test_')}"
            ),
            feature_ids=features,
            tags=tags,
        )


def traceability_problems(items: list[pytest.Item]) -> list[str]:
    """Every test outside tests/unit needs at least one well-formed feature ID."""
    problems = []
    for item in items:
        if item.get_closest_marker("unit") is not None:
            continue
        ids = [fid for marker in item.iter_markers("feature") for fid in marker.args]
        if not ids:
            problems.append(f"{item.nodeid} has no @pytest.mark.feature")
        problems.extend(
            f"{item.nodeid} has a malformed feature ID '{fid}'"
            for fid in ids
            if not isinstance(fid, str) or not FEATURE_ID.match(fid)
        )
    return problems
