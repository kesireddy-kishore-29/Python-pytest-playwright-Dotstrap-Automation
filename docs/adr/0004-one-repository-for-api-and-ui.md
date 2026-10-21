# 4. One repository for API and UI tests

- Status: accepted
- Date: 2026-10-21

## Context

The family keeps one stack per repository: the API flagship in Java, the UI flagship in
TypeScript, Selenium in Java. Python teams usually keep API and UI tests together, sharing
fixtures, data factories and the HTTP client the UI tests use to seed data.

## Decision

1. API and UI tests share this repository, one framework package (`src/framework`) and one
   pytest configuration. Markers (`api`, `ui`, `smoke`, `live`, `demo_failure`, `quarantine`,
   `unit`) select what runs.
2. The hybrid test uses the same `ApiSession` and client layer as the API tests to seed and remove
   data, and Playwright to check the page in between.
3. Evidence is per test, whatever the kind: API tests keep a transcript; UI tests keep video,
   trace, screenshots, DOM, console and HAR; a hybrid test keeps both.

## Consequences

- One install, one lint and type configuration, one report: an API failure and a UI failure look
  the same in the run summary, the gallery and Allure.
- The default `pytest` run covers unit, API and UI tests together (52 tests); CI's smoke and the
  nightly select by marker.
