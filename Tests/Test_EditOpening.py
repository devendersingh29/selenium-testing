import pytest
from playwright.sync_api import Page

from Pages.Page_EditOpening import PageEditOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.edit,
    pytest.mark.data_mutation,
]


def test_edit_opening_updates_job_content(admin_page: Page) -> None:
    """Edit the first job opening's content and verify success message appears."""
    page = PageEditOpening(admin_page)

    new_content = "This is automated job content"

    # High-level flow implemented in the page object
    page.edit_first_job_content_and_save(new_content)
