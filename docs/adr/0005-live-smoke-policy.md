# 5. The live smoke is a polite, read-only visitor

- Status: accepted
- Date: 2026-10-21

## Context

The author's own production site, dotstrap.com, is the one target here that real people use. A
status check alone can pass while a client-rendered page shows nothing, so the smoke reads the
rendered page. It must never load the site in a way its owner would mind, and nothing it records
may expose how the site is run.

## Decision

1. Public pages only: no sign-in (`/login` is refused by the page list's validation), no forms, no
   data created, no calls to the backend.
2. One worker (no `-n`), no retries in CI, and a user agent ending in
   ` python-pytest-automation-framework (portfolio smoke test)`; the first check asserts it.
3. Nightly and on demand only, never on pull requests, and never gating: the job continues on
   error and its result feeds a badge.
4. The pages and the text they must show are in one file, `src/framework/config/live_pages.json`.
5. The live browser context is created without pytest-playwright's recorder: no video, no trace,
   no HAR. Failure evidence is a screenshot, the page source and the console, kept 7 days as a
   workflow artifact, never published or committed. The Content-Security-Policy is checked for
   presence only; its text is never stored or printed.

## Consequences

- Four checks, 15 runs in about a minute: 200 and the expected heading (9 pages), no console errors
  or failed requests (every page, one tab), the security headers, no horizontal overflow at 1440,
  1024, 768 and 390 px (3 pages).
- A content change on the site can fail the smoke with no change here; that is a one-file fix.
