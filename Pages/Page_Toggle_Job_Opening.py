import re
from playwright.sync_api import Locator, expect

from Locators.Locator_Toggle_Job_Opening import LocatorToggleJobOpening
from Pages.BasePage import BasePage


class PageToggleJobOpening(BasePage):
    """Page object to manage List/Grid view toggling for Job Openings.

    Follows the project's POM style: small properties for locators and
    clear action/assertion methods that tests use.
    """

    @property
    def job_opening_side_button(self) -> Locator:
        return self.locator(LocatorToggleJobOpening.JOB_OPENING_SIDE_BUTTON)

    @property
    def list_view_button(self) -> Locator:
        return self.page.get_by_role('button', name='List view', exact=True)

    @property
    def grid_view_button(self) -> Locator:
        return self.page.get_by_role('button', name='Grid view', exact=True)

    def open(self) -> None:
        """Navigate to Job Openings page and verify header is present."""
        expect(self.job_opening_side_button).to_be_visible()
        self.job_opening_side_button.click()
        expect(self.page.locator("h1")).to_contain_text("Job Openings")

    def click_list_view(self) -> None:
        """Click the List view control."""
        expect(self.list_view_button).to_be_visible()
        self.list_view_button.click()

    def click_grid_view(self) -> None:
        """Click the Grid view control."""
        expect(self.grid_view_button).to_be_visible()
        self.grid_view_button.click()

    def assert_list_view_active(self) -> None:
        """Assert that List view is active using aria-pressed attribute.

        The application's buttons expose pressed state in the accessibility
        tree (aria-pressed or similar). We verify a truthy value.
        """
        expect(self.list_view_button).to_be_visible()
        # Primary assertion: aria-pressed present and truthy
        expect(self.list_view_button).to_have_attribute(
            "aria-pressed", re.compile(r"^(true|pressed)$", re.I)
        )
        # Secondary assertion: grid button is not pressed
        expect(self.grid_view_button).to_have_attribute(
            "aria-pressed", re.compile(r"^(false|null|0)$", re.I)
        )

    def assert_grid_view_active(self) -> None:
        """Assert that Grid view is active using aria-pressed attribute."""
        expect(self.grid_view_button).to_be_visible()
        expect(self.grid_view_button).to_have_attribute(
            "aria-pressed", re.compile(r"^(true|pressed)$", re.I)
        )
        expect(self.list_view_button).to_have_attribute(
            "aria-pressed", re.compile(r"^(false|null|0)$", re.I)
        )

    def toggle_to_list_view(self) -> None:
        """Click and assert List view is active."""
        self.click_list_view()
        self.assert_list_view_active()

    def toggle_to_grid_view(self) -> None:
        """Click and assert Grid view is active."""
        self.click_grid_view()
        self.assert_grid_view_active()
