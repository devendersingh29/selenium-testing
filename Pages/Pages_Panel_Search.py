from typing import Iterable

from playwright.sync_api import Locator, expect

from Locators.Locator_Panel_Search import LocatorPanelSearch
from Pages.BasePage import BasePage


class PagesPanelSearch(BasePage):
    """Page object for the Panel search flow."""

    @property
    def panel_side_menu(self) -> Locator:
        return self.locator(LocatorPanelSearch.PANEL_SIDE_MENU)

    @property
    def search_input(self) -> Locator:
        return self.locator(LocatorPanelSearch.SEARCH_INPUT)

    def open(self) -> None:
        """Open the Panel setup page and confirm the correct screen is loaded."""
        self.open_sidebar_page(self.panel_side_menu, "dashboard/panel")
        expect(self.page.locator("h1")).to_contain_text("Panel Setup")

    def search(self, keyword: str) -> None:
        """Enter a search keyword and verify the input retains the value."""
        expect(self.search_input).to_be_visible()
        self.search_input.fill(keyword)
        expect(self.search_input).to_have_value(keyword)

    def verify_search_result(
        self,
        expected_name: str,
        hidden_names: Iterable[str] | None = None,
    ) -> None:
        """Verify the expected row remains visible and non-matching entries are filtered out."""
        expect(self.page.get_by_text(expected_name, exact=True).first).to_be_visible()

        if hidden_names:
            for name in hidden_names:
                expect(self.page.get_by_text(name, exact=True)).to_have_count(0)
