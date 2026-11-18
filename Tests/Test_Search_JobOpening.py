import pytest
from playwright.sync_api import Page

from Pages.Page_Search_JobOpening import PageSearchJobOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.search,
    pytest.mark.read_only,
]


def test_search_job_opening(admin_page: Page) -> None:
    """Search for a job opening by title and verify the result appears.

    Uses the admin_page fixture (already logged in) to open Job Openings and
    perform the search-and-verify flow implemented on the page object.
    """
    search_page = PageSearchJobOpening(admin_page)

    # Navigate to Job Openings list
    search_page.open()

    title = "Auto_QA engineer"

    # Perform search and verify the job appears in results
    search_page.search(title=title)
    search_page.verify_result_heading(title=title)
