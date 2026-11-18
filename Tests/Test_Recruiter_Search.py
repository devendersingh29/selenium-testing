import time

import pytest
from playwright.sync_api import Page

from Pages.Page_Recruiter_Search import PageRecruiterSearch

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.recruiter,
    pytest.mark.search,
    pytest.mark.read_only,
]


def test_recruiter_search_filters_results(admin_page: Page) -> None:
    recruiter_search_page = PageRecruiterSearch(admin_page)
    recruiter_search_page.open()

    keyword = "Second Recruiter"
    recruiter_search_page.search(keyword)
    recruiter_search_page.verify_search_result(
        expected_name="Second Recruiter",
        hidden_names=["First Recruiter", "Second Lead", "Third Recruiter", "First Lead"],
    )


