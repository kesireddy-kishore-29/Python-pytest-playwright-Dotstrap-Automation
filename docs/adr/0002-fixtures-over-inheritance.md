# 2. pytest fixtures over base classes

- Status: accepted
- Date: 2026-10-21

## Context

Test frameworks in Java and C# usually share setup through a base test class. In pytest that
pattern fights the tool: fixtures already express what a test needs, with a scope and a teardown,
and compose without a class hierarchy.

## Decision

1. No base test classes. A test asks for what it needs by name: `booker`, `bookings`,
   `reference_account`, `sauce_page`, `app_account`, `visit`.
2. Each fixture has the narrowest scope that is still cheap: the Restful-Booker token and the saved
   Sauce Demo session once per worker (`session`), clients and data per test (`function`).
3. Data fixtures `yield` the data, then delete it **and prove it is gone**: a booking must answer
   404 afterwards, an account's token must stop working, the app account must no longer sign in.
   A cleanup that fails fails the test.
4. Cross-cutting behaviour (evidence, retries, traceability, quarantine) lives in one plugin,
   `framework.evidence.plugin`, loaded by `tests/conftest.py`, not in fixtures each test must
   remember.
5. Fixtures live in the `conftest.py` of the folder that uses them (`tests/api`, `tests/ui`,
   `tests/live`); types they hand to tests live in `src/` so tests never import a conftest.

## Consequences

- A test's signature is its dependency list; reading it says what the test touches.
- Teardown order follows fixture order: the UI page's evidence is captured before its context
  closes, and the HAR is redacted after.
- Fixture scopes interact with pytest-xdist: a `session` fixture runs once per worker, so the
  shop's saved session is created once per worker, not once per run.
