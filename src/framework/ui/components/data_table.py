"""A data table addressed by column header names and row content, never by CSS or a fixed index."""

from playwright.sync_api import Locator


class DataTable:
    def __init__(self, root: Locator) -> None:
        self.root = root

    def rows(self) -> Locator:
        """Body rows: rows that contain cells (the header row has column headers instead)."""
        return self.root.get_by_role("row").filter(has=self.root.page.get_by_role("cell"))

    def row(self, text: str) -> Locator:
        return self.rows().filter(has_text=text)

    def column_index(self, header: str) -> int:
        headers = [h.strip() for h in self.root.get_by_role("columnheader").all_inner_texts()]
        if header not in headers:
            raise LookupError(f'No column "{header}" in {headers}')
        return headers.index(header)

    def cell(self, row_text: str, header: str) -> Locator:
        """The cell under the column called `header`; the position is the header's position."""
        return self.row(row_text).get_by_role("cell").nth(self.column_index(header))
