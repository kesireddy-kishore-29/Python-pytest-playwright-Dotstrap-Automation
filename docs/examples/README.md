# Examples from real runs

Everything here was produced by a run on the build machine (Windows 11, Python 3.13, headless
Chromium); none of it is mocked up. Live-site evidence is never kept here.

| Folder | What | From run |
|---|---|---|
| [allure/](allure/) | `overview.png`: the Allure report of a 52-test run (unit, API, UI) with the two-run trend, environment and feature labels (the README's hero). `categories.png`: the deliberate failures, one category each | `py-allure-4` (after `py-allure-3`), git `b50090d3f62f`; `py-demo-3` |
| [gallery/](gallery/) | `gallery.png`: the run gallery (the family's shared page) for the deliberate failures | `py-demo-4` |
| [failure-evidence/](failure-evidence/) | Two failure bundles exactly as the run wrote them (the zips left out): a UI one and an API one, plus the redacted trace open in Playwright's trace viewer | `py-demo-4`, git `9f48f5466976`; viewer `py-demo-3` |

Commands:

```bash
rm -rf allure-results
RUN_ID=py-allure-3 pytest -n 4 && scripts/allure-report.sh
RUN_ID=py-allure-4 pytest -n 4 && scripts/allure-report.sh <copy of report 3>
RUN_ID=py-demo-4 pytest -m demo_failure          # fails on purpose
playwright show-trace <bundle>/attempt-2/trace.zip
```
