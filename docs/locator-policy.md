# Locator policy

A locator is an assertion about how a person finds something on the page. The best one fails only
when a person would also be lost, and survives every change that a person would not notice. This
is the UI flagship's policy, applied with Playwright for Python.

## Order of preference

| Rank | Locator | Use it for | Example in this repository |
|---|---|---|---|
| 1 | `get_by_role(role, name=...)` | Anything with a role: buttons, headings, tables, rows, cells, dialogs | `page.get_by_role("dialog", name="Delete item?")` |
| 2 | `get_by_placeholder`, `get_by_label`, `get_by_text` | Form fields; text that is the thing itself | `page.get_by_placeholder("Username")` |
| 3 | `get_by_test_id` (`data-test`) | Things with no role or name a person relies on: a count, a price, a title, a total; and third-party markup we cannot change | `page.get_by_test_id("shopping-cart-badge")` |
| — | CSS or XPath | Never | |

In `src/framework/ui` today: 20 role locators, 5 placeholder locators, 14 test-id lookups (13 on
Sauce Demo, one deliberately wrong in the demo page), no CSS and no XPath. `get_by_test_id` reads
`data-test`, which both targets publish.

## Rules

- **Locators live in page objects and components.** Tests read `inventory.add_to_cart(product)`
  and assert on page-object attributes with Playwright's `expect`; a unit test scans `tests/` and
  fails on any `.locator(`, `get_by_…(` or `.goto(` there.
- **Scope instead of a fixed index.** A product's button is found inside the product's card
  (`items.filter(has_text=name).get_by_role("button", name="Add to cart")`); a table cell under
  the column whose header has that name (`DataTable.cell`). Two positions are used where the
  position is the meaning: the cell index computed from the header row, and, on the live site,
  the first level-1 heading.
- **Exact names for buttons in dialogs** (`exact=True`), so "Delete" never matches "Delete item".
- **Web-first assertions** (`expect(locator).to_have_text(...)`) that wait for the state; no fixed
  waits (`wait_for_timeout` is refused by the same scan, `time.sleep` by ruff).

## When a third party gets in the way

Sauce Demo's menu entries are `<a>` elements without `href`, so they have no link role; the header
component uses their test id, and a comment says why. A finding against the site
([known issues](known-issues.md)), not a licence to use test ids for convenience.

## Same as the other repositories

The UI flagship uses the same ranks and, where it uses a test id, the same one. The Selenium
repository cannot search by role (Selenium has no role locator); it uses test ids first and checks
roles and names afterwards.
