# Examples from real runs

Everything here was produced by a run on the build machine (Windows 11, Python 3.13, headless
Chromium); none of it is mocked up. Live-site evidence is never kept here.

| Folder | What | From run |
|---|---|---|
| [allure/](allure/) | `overview.png`: the Allure report of a 58-test run (unit, API, UI) with the two-run trend, environment and feature labels (the README's hero). `categories.png`: the deliberate failures, one category each | `py-allure-8` (after `py-allure-7`), git `883cb6d92005`; `py-demo-8` |
| [gallery/](gallery/) | `gallery.png`: the run gallery (the family's shared page) for the deliberate failures | `py-demo-8` |
| [failure-evidence/](failure-evidence/) | Two failure bundles exactly as the run wrote them (the zips left out): a UI one and an API one, plus the redacted trace open in Playwright's trace viewer | `py-demo-8`, git `883cb6d92005` |

Commands:

```bash
rm -rf allure-results
RUN_ID=py-allure-7 pytest -n 4 && scripts/allure-report.sh
cp -r allure-report /tmp/report-7 && rm -rf allure-results
RUN_ID=py-allure-8 pytest -n 4 && scripts/allure-report.sh /tmp/report-7
rm -rf allure-results
RUN_ID=py-demo-8 pytest -m demo_failure; scripts/allure-report.sh    # the run fails on purpose
playwright show-trace <bundle>/attempt-2/trace.zip
```
