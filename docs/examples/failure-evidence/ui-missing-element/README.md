# Failure bundle: demo: a renamed test id is a missing element [chromium]

| | |
|---|---|
| Test | `tests/ui/test_deliberate_failures.py::test_demo_a_renamed_test_id_is_a_missing_element[chromium]` |
| Features | FEAT-DEMO-01 |
| Run | `py-demo-8` (git `883cb6d92005`) |
| Attempts | 2 |
| Error | `AssertionError` |

## What is in here

| File | What it is | How to open |
|---|---|---|
| `attempt-N/video.webm` | The browser session (UI tests) | Any browser or video player |
| `attempt-N/trace.zip` | Playwright trace: every action, DOM snapshot and request (redacted) | https://trace.playwright.dev |
| `attempt-N/screenshot.png` | The page when the test failed | An image viewer |
| `attempt-N/fullpage.png` | The whole page when the test failed | An image viewer |
| `attempt-N/page-source.html` | The DOM when the test failed (redacted) | A browser or editor |
| `attempt-N/console.log` | The browser console (redacted) | A text editor |
| `attempt-N/network.har` | Every request and response (headers and cookies masked) | A HAR viewer or Chrome DevTools |
| `attempt-N/transcript.md` | Every API call with bodies (API tests; redacted) | A Markdown viewer |
| `attempt-N/meta.json` | Test identity, features, environment, git SHA | A JSON viewer |

A file appears only when the test produced it: API tests have a transcript, UI tests the rest.
