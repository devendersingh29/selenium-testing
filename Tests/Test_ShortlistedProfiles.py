import time
from playwright.sync_api import Page

import pytest

from Pages.Page_ShortlistedProfiles import PageShortlistedProfiles

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.shortlisted_profiles,
    pytest.mark.read_only,
]


def test_shortlisted_count_matches_for_first_job(admin_page: Page) -> None:
    """Verify shortlisted button count matches the number of shortlisted candidate rows shown for the first job card."""
    page = PageShortlistedProfiles(admin_page)

    # Navigate to Job Openings
    page.open()

    # Validate using tolerant fallback when necessary
    page.verify_shortlisted_count_matches_first()


def test_shortlisted_count_matches_by_title(admin_page: Page) -> None:
    """Verify shortlisted button count matches the number of shortlisted candidate rows for a given job title."""
    page = PageShortlistedProfiles(admin_page)

    # Navigate to Job Openings
    page.open()

    # Replace with a real job title present in your test environment
    title = "Auto_QA engineer"

    # High-level verification that reads button, opens panel, and compares counts
    page.verify_shortlisted_count_matches(title=title)
