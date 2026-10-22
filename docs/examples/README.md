# Examples from real runs

Everything here was produced by a run on the build machine (Windows 11, Python 3.13, headless
Chromium); none of it is mocked up. Live-site evidence is never kept here.

| Folder | What | From run |
|---|---|---|
| [allure/](allure/) | `overview.png`: the Allure report of a 52-test run (unit, API, UI) with the two-run trend, environment and feature labels (the README's hero). `categories.png`: the deliberate failures, one category each | `py-allure-6` (after `py-allure-5`), git `ca8c1a39c764`; `py-demo-7` |
| [gallery/](gallery/) | `gallery.png`: the run gallery (the family's shared page) for the deliberate failures | `py-demo-7` |
| [failure-evidence/](failure-evidence/) | Two failure bundles exactly as the run wrote them (the zips left out): a UI one and an API one, plus the redacted trace open in Playwright's trace viewer | `py-demo-7`, git `098481d9ff14` |

Commands:

```bash
rm -rf allure-results
RUN_ID=py-allure-5 pytest -n 4 && scripts/allure-report.sh
cp -r allure-report /tmp/report-5 && rm -rf allure-results
RUN_ID=py-allure-6 pytest -n 4 && scripts/allure-report.sh /tmp/report-5
rm -rf allure-results
RUN_ID=py-demo-7 pytest -m demo_failure; scripts/allure-report.sh    # the run fails on purpose
playwright show-trace <bundle>/attempt-2/trace.zip
```
