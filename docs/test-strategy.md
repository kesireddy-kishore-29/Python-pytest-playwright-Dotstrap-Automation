# Test strategy

What this repository tests, where, and the rules every test follows. It is the Python lite member
of a family of four; the flagships carry the wider strategy (contract, resilience, visual,
accessibility, triage, healing).

## Targets

| Target | What only it can give | Gating? |
|---|---|---|
| [Restful-Booker](https://restful-booker.herokuapp.com) (public practice API) | A real third-party API with auth and CRUD, and its quirks | Smoke gates pull requests; all of it nightly |
| The API flagship's reference service (port 7070) | Behaviour a public API will not give on demand: RFC 7807 errors, 422, 429 with recovery, idempotency | Nightly, when checked out; skipped otherwise |
| [Sauce Demo](https://www.saucedemo.com) (public practice shop) | A real third-party UI: sign-in, cart, checkout | Smoke gates pull requests; all of it nightly |
| The UI flagship's app (`sut-ui`, port 4173) | Data we own: seed through its API, check the page, delete and prove it gone | Nightly, when checked out; skipped otherwise |
| [dotstrap.com](https://dotstrap.com) public pages | The author's production site, read the way a visitor's browser reads it | Never ([ADR 5](adr/0005-live-smoke-policy.md)) |

## What runs where

| Command | Contents | Runs |
|---|---|---|
| `pytest -m unit` | 36 framework tests, no outside network, no browser | Every push (CI `quality`) |
| `pytest -m smoke -n 2` | 5: a token, a booking read back, an idempotent purchase, sign-in, a full checkout | Every push and pull request |
| `pytest -n 4` | Unit, API and UI: 58 tests (live, deliberate failures and quarantine are left out by default) | Locally |
| nightly | API and UI with retries, every test recorded | Nightly |
| `pytest -m live` | 4 checks, 15 runs, one worker | Nightly and on demand, never gating |
| `pytest -m demo_failure` | 3 tests that fail on purpose (1 API, 2 UI) | On demand |
| `pytest -m quarantine` | Quarantined tests (none today) | Nightly when there are any, never gating |

## Rules every test follows

- **Traceable**: every test outside `tests/unit` has `@pytest.mark.feature("FEAT-…")`; collection
  stops otherwise (exit code 4). The IDs are shared with the other repositories.
- **Own data, cleaned and verified**: bookings, reference-service accounts and app accounts are
  created per test and deleted afterwards, and the fixture proves they are gone (404, a dead token,
  a refused sign-in). A cleanup that fails fails the test.
- **No order dependence**: nothing a test needs is created by another test; tests run in parallel
  on pytest-xdist workers.
- **No hard waits**: ruff refuses `time.sleep`; a unit test refuses `wait_for_timeout`. The one
  pause is `wait_until`, a bounded poll with a description (used once, for a rate-limit window).
- **Clients and page objects only**: tests never call `requests` or a locator directly (checked by
  a unit test); see the [locator policy](locator-policy.md).
- **Contracts**: responses are parsed into strict pydantic models before any assertion
  ([ADR 3](adr/0003-pydantic-for-contracts-and-config.md)).
- **Public targets as they are**: where Restful-Booker deviates from HTTP semantics (201 for a
  delete, 403 instead of 401, 200 with "Bad credentials"), the test asserts what it does and says
  so; the deviations are findings in the [known issues](known-issues.md).

## Flaky tests and quarantine

- A failed test is retried at most twice (`TEST_RETRIES` lowers it; the demo retries once; unit
  tests never). A test that passes on a retry is reported as **flaky** in `run-summary.json` and
  `flaky-report.json`, never as a plain pass.
- A test that keeps flaking gets the `quarantine` marker **and** an entry in `quarantine.json`
  with an owner, a reason, an expiry date and an issue. Collection stops when a quarantined test
  has no valid entry or an entry has expired. Quarantined tests still run, in their own
  non-gating step.

## Evidence

`RECORD_MODE` decides what each attempt keeps: `failures` (default), `all` (nightly), `off`. It
drives pytest-playwright's `--video`, `--tracing` and `--screenshot`. Kept per attempt: UI tests
`video.webm`, `trace.zip` (redacted; the raw one is deleted), `screenshot.png`, `fullpage.png`,
`page-source.html`, `console.log`, `network.har` (redacted); API tests `transcript.json` and
`transcript.md` (redacted); all `meta.json`. Per run: `run-summary.json`, `flaky-report.json`,
`gallery.html`, `summary.md` and a failure bundle per failed test. The live smoke keeps no video,
trace or HAR.
