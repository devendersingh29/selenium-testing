from playwright.sync_api import Locator, expect

from Locators.Locator_Recruiter_Search import LocatorRecruiterSearch
from Pages.BasePage import BasePage


class PageRecruiterSearch(BasePage):
    """Page object for the Recruiter search flow."""

    @property
    def recruiter_side_menu(self) -> Locator:
        return self.locator(LocatorRecruiterSearch.RECRUITER_SIDE_MENU)

    @property
    def search_input(self) -> Locator:
        return self.locator(LocatorRecruiterSearch.SEARCH_INPUT)

    def open(self) -> None:
        """Open the Recruiter setup page and confirm the correct screen loaded."""
        self.open_sidebar_page(self.recruiter_side_menu, "dashboard/recruiter")
        expect(self.page.locator("h1")).to_contain_text("Recruiter Setup")

    def search(self, keyword: str) -> None:
        """Type a keyword and verify the field retained the value."""
        expect(self.search_input).to_be_visible()
        self.search_input.fill(keyword)
        expect(self.search_input).to_have_value(keyword)

    def verify_search_result(self, expected_name: str, hidden_names=None) -> None:
        """Verify the expected recruiter remains visible and other names disappear."""
        expect(self.page.get_by_text(expected_name, exact=True).first).to_be_visible()
        if hidden_names:
            for name in hidden_names:
                expect(self.page.get_by_text(name, exact=True)).to_have_count(0)
