# Failure evidence

Two bundles from run `py-demo-8` (git `883cb6d92005`, `RECORD_MODE=failures`), each with its own
README naming every file. Both tests fail on purpose; each was retried once and failed again.

## UI: a renamed test id ([ui-missing-element/](ui-missing-element/))

The test adds a product to the cart, then expects the badge under a test id the page does not have
(`cart-count`; the real one is `shopping-cart-badge`): what a renamed attribute looks like to a
test. Allure files it under `LOCATOR_DRIFT` ([categories](../allure/categories.png)).

| File (per attempt) | What it shows |
|---|---|
| `video.webm` | The session in real time, 800×450, 7.6 s and 7.1 s |
| `trace.zip` | Every action, DOM snapshot and request, with cookie and header values masked; checked in `playwright show-trace` ([what the viewer shows](trace-viewer.png)); the same viewer runs at https://trace.playwright.dev |
| `screenshot.png`, `fullpage.png` | The page at failure: the badge shows 1, so the product really is in the cart; only the locator is wrong |
| `page-source.html`, `console.log`, `network.har` | The DOM, the console and the requests (headers and cookies masked) |
| `meta.json` | Test identity, feature ID, attempt, status, environment, git SHA |

## API: an answer that does not match the expectation ([api-wrong-status/](api-wrong-status/))

The test expects a booking that does not exist. Its evidence is `transcript.md` (and the same as
JSON): the call, the status, the correlation ID, the timing and the body, redacted. Allure files it
under `PRODUCT_BUG`.

The trace viewer screenshot is of `ui-missing-element/attempt-2/trace.zip` from this run. Paths in
the trace are relative to the repository, and the viewer's Source tab still shows the test's code.
