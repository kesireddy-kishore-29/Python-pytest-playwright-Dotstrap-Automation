# Known issues and limits

Everything below is stated as it is. Where something was not run, it says so.

## Not verified yet

| What | State |
|---|---|
| **GitHub Actions** | `ci.yml` and `nightly.yml` pass actionlint 1.7.12 with shellcheck 0.11.0 but have **never run on GitHub**: the repository had no remote while it was built. Not yet exercised: Python 3.12 (everything ran on 3.13 locally), Chromium on Linux, building the API flagship's service and starting the UI flagship's app in the nightly, artifact hand-off to the publish job, GitHub Pages, the live badge. |
| **Flagship services in CI** | The reference-service tests and the hybrid test run only when the repository variables `FLAGSHIP_OWNER`, `API_FLAGSHIP_REF` and `UI_FLAGSHIP_REF` are set; otherwise they skip. Verified locally against both services. |
| **Browsers** | Chromium only. Firefox and WebKit are not wired in (pytest-playwright's `--browser` would add them). |
| **Operating systems** | Run on Windows 11 only. |

## Behaviour to know about

- **Badges and links assume the GitHub account `kesireddy-kishore-29`.** Until the first workflow
  runs there, the badges show no status; nothing here claims a CI result.
- **Public targets change on their own schedule.** Restful-Booker is shared with everyone on the
  internet; Sauce Demo and dotstrap.com change their pages. A failure may be theirs. The live page list is one file,
  [`live_pages.json`](../src/framework/config/live_pages.json).
- **`test-results/` holds pytest-playwright's own copies** of videos and screenshots. Its raw traces
  are deleted once a redacted copy is in the evidence folder. The folder is ignored by git and never
  uploaded by CI.
- **allure-pytest appends to `allure-results/`.** Delete it before a local run to report that run
  alone; CI always starts clean. The report script needs Java (the Allure 2 generator).
- **Retries and parallel workers**: pytest-rerunfailures reruns a failed test on the same worker;
  each attempt keeps its own evidence folder and pytest-playwright output folder (`-retryN`).

## Findings against the public targets

Restful-Booker (the tests assert what it really does and say so):
- `DELETE /booking/{id}` answers **201 Created**, not 200 or 204.
- A write without a token or with a bad one answers **403**, where HTTP semantics would be 401.
- Wrong credentials answer **200** with `{"reason": "Bad credentials"}` instead of 401.
- It answers **418** to a multi-value `Accept` header, so the client sends exactly
  `application/json` (found in the API flagship; the same client rule here).

Sauce Demo:
- Loading a page directly answers **HTTP 404** while still rendering it; Chrome logs the 404 as a
  console error, and the console guard allows exactly that message.
- The menu entries are `<a>` elements **without `href`**, so they have no link role.

## Defects found in this framework while building it (all fixed)

- **Raw cookies in Playwright traces**: the hybrid test's trace held the app's session cookie 15
  times. Traces are now redacted before they are kept, and pytest-playwright's raw copy is deleted.
  Checked: no cookie value left, and the redacted trace still opens in Playwright's trace viewer
  ([screenshot](examples/failure-evidence/trace-viewer.png)).
- **The local user name in traces**: Playwright records its video folder (a temp path under the
  user's home) in each trace. Home paths now lose the user name. Found before any trace was
  committed.
- **One failure, two Allure categories**: a failed text expectation's call log matched the
  locator-drift pattern too. Each deliberate failure now lands in exactly one category.
- **A shell heredoc turned escapes into characters** while editing: the six-character JSON escape
  for `<` became a plain `<` (the gallery's guard against a closing script tag silently became a
  no-op) and a newline escape became a real line break. The line break was caught by ruff, the
  no-op on review; the escape is now built from code points and a unit test guards it.
- Duplicate test-module names in two folders broke collection with pytest's default import mode;
  the repository uses `--import-mode=importlib`.
