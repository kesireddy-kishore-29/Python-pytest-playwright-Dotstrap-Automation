"""Hybrid: data seeded through the UI flagship app's API, checked and changed in the browser,
checked again through the API. Skipped when that app is not running."""

import pytest
from playwright.sync_api import Page, expect

from framework.api.fixture_types import AppAccount
from framework.data.factories import unique_name
from framework.ui.pages.app import ItemsPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.feature("FEAT-ITEMS-01")
def test_items_seeded_through_the_api_are_listed_and_one_deleted_in_the_ui_leaves_the_api(
    app_account: AppAccount, app_page: Page
) -> None:
    """Items seeded through the API are listed; one deleted in the UI is gone from the API."""
    keep = app_account.seed(unique_name("keep"), "paused")
    remove = app_account.seed(unique_name("remove"))
    items = ItemsPage(app_page)

    items.open()

    expect(items.table.row(keep.name)).to_be_visible()
    expect(items.table.cell(keep.name, "Status")).to_have_text("paused")
    expect(items.table.cell(keep.name, "Owner")).to_have_text("QA")

    items.delete(remove.name)

    expect(items.table.row(remove.name)).to_have_count(0)
    expect(items.table.row(keep.name)).to_be_visible()
    ids = [item.id for item in app_account.items()]
    assert keep.id in ids
    assert remove.id not in ids
