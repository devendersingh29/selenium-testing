from playwright.sync_api import Page

import pytest

from Pages.Page_Submission_JobOpening import PageSubmissionJobOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.submission,
    pytest.mark.read_only,
]


def test_submission_count_matches_panel(admin_page: Page) -> None:
    """Verify submission button count matches the number of candidate rows shown."""
    page = PageSubmissionJobOpening(admin_page)

    # Open Job Openings list
    page.open()

    title = "Auto_QA engineer"

    # High-level verification that reads button, opens panel, and compares counts
    page.verify_submission_count_matches(title=title)
