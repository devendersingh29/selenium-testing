import time

import pytest
from playwright.sync_api import Page

from Pages.Add_job_opening import AddJobOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.draft,
    pytest.mark.data_mutation,
]


def test_make_and_verify_draft(admin_page: Page) -> None:
    """Create a draft from an existing job opening and verify it appears under Drafts.

    Uses the admin_page fixture to be already logged in and on the dashboard,
    then navigates to Job Openings and performs the draft flow.
    """
    add_job_opening = AddJobOpening(admin_page)

    # Navigate to Job Openings list
    add_job_opening.open_job_openings_from_sidebar()

    # Use a known title that exists in test environment (matches other tests)
    title = "Auto_QA engineer"

    # Make the job a draft and capture its job id
    job_id = add_job_opening.make_job_draft(title=title)

    # Verify the job id shows up on the Draft screen
    add_job_opening.verify_job_in_draft(job_id)


