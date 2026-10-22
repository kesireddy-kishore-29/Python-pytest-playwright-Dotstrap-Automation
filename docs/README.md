# Documentation

| Read this | For |
|---|---|
| [test-strategy.md](test-strategy.md) | What is tested and why: markers, targets, fixtures, retries, quarantine, evidence |
| [locator-policy.md](locator-policy.md) | How elements are found in the page objects |
| [known-issues.md](known-issues.md) | What has not run yet and behaviour worth knowing, stated as it is |
| [adr/](adr/) | Five architecture decisions, one page each |
| [examples/](examples/) | Evidence from real runs: Allure overview and categories, run gallery, two failure bundles, the trace viewer |
| [images/](images/) | Images used by the README |

The framework lives in [`../src/framework/`](../src/framework/) (HTTP session and clients,
pydantic models, page objects, the pytest plugin and evidence) and the tests in
[`../tests/`](../tests/) (`api`, `ui`, `live`, `unit`).
