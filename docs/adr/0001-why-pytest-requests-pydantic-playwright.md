# 1. Why pytest, requests, pydantic and Playwright for Python

- Status: accepted
- Date: 2026-10-21

## Context

These repositories are meant to show range to people hiring for QA and SDET roles. The author
analysed about 980 recent QA/SDET job descriptions (Naukri and Foundit): Java is the most requested
language for test automation, and Python comes next (33 to 42% of jobs). The author's day job is
C# with Selenium; the flagships are in Java (API) and TypeScript (UI), so a Python repository
covers the next language employers ask for.

## Decision

1. pytest 9 as the runner, with its fixtures, markers and plugins (pytest-xdist for parallel
   workers, pytest-rerunfailures for capped retries, allure-pytest for the report).
2. requests behind one session wrapper for HTTP; pydantic 2 for response models and settings
   ([ADR 3](0003-pydantic-for-contracts-and-config.md)).
3. Playwright for Python (sync API) through pytest-playwright for the browser, the same engine and
   version line as the UI flagship (1.64).
4. ruff for lint and format and mypy in strict mode on `src/`, both pinned in `pyproject.toml`,
   the single configuration file.
5. A lite repository: the flagships' scenarios in Python with the same feature IDs, report
   formats and gallery page; triage and healing stay in the flagships.

## Alternatives considered

- **Robot Framework**: its keyword layer hides the Python this repository exists to show.
- **Selenium for Python**: the Java lite repository already shows Selenium; Playwright here runs
  the same engine as the UI flagship, so the two languages can be compared on one engine.
- **httpx**: a fine client with async support; the tests here are synchronous, and requests is the
  better-known library.

## Consequences

- One `pip install -e ".[dev]"` and one `playwright install chromium` set a machine up; CI does the
  same on Python 3.12.
- pytest-playwright already keeps a video, trace and screenshot per attempt; the framework copies
  them into the family's evidence layout and redacts the trace, instead of recording them again.
