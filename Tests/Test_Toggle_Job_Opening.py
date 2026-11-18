from playwright.sync_api import Page

import pytest

from Pages.Page_Toggle_Job_Opening import PageToggleJobOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.view_toggle,
    pytest.mark.read_only,
]


def test_toggle_list_grid_view(admin_page: Page) -> None:
    """Toggle Job Openings between List and Grid view and verify active states."""
    page = PageToggleJobOpening(admin_page)

    # Navigate to Job Openings
    page.open()

    # Switch to List view and verify
    page.toggle_to_list_view()
    print("List view is active.")

    # Switch to Grid view and verify
    page.toggle_to_grid_view()
    print("Grid view is active.")
