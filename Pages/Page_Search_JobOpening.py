from playwright.sync_api import Locator, expect

from Locators.Locator_Search_JobOpening import LocatorSearchJobOpening
from Pages.BasePage import BasePage


class PageSearchJobOpening(BasePage):
    """Page object for searching job openings and verifying results."""

    @property
    def job_opening_side_button(self) -> Locator:
        return self.locator(LocatorSearchJobOpening.JOB_OPENING_SIDE_BUTTON)

    @property
    def search_input(self) -> Locator:
        return self.locator(LocatorSearchJobOpening.SEARCH_INPUT)

    def open(self) -> None:
        """Navigate to Job Openings from the sidebar and assert the page opened."""
        expect(self.job_opening_side_button).to_be_visible()
        self.job_opening_side_button.click()
        expect(self.page.locator("h1")).to_contain_text("Job Openings")

    def search(self, title: str) -> None:
        """Enter title into the search box and wait for results to update."""
        expect(self.search_input).to_be_visible()
        self.search_input.fill(title)
        # wait for the body to include the title text
        expect(self.page.locator("body")).to_contain_text(title)

    def verify_result_heading(self, title: str) -> None:
        """Verify the first job card contains the expected title as its heading."""
        job_card = self.page.locator(f"{LocatorSearchJobOpening.JOB_CARD}:has-text(\"{title}\")").first
        expect(job_card).to_be_visible()
        heading = job_card.locator(LocatorSearchJobOpening.JOB_CARD_HEADING).first
        expect(heading).to_have_text(title)
        print(f"Search successful: job opening '{title}' found and verified.")
