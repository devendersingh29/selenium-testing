import pytest
from playwright.sync_api import Page

from Pages.Page_JO_Schedule import PageJOSchedule

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
    pytest.mark.schedule,
    pytest.mark.data_mutation,
    pytest.mark.e2e,
]


def test_jo_schedule_full_flow(admin_page: Page) -> None:
    """Full JO Schedule flow: setup -> generate -> save -> CBT invite -> confirm."""
    page = PageJOSchedule(admin_page)

    # replace with a valid candidate email in your test environment
    candidate_email = "Prakash.lavania+candidate2@walkingtree.tech"

    page.full_schedule_flow_for_first_job(email=candidate_email)
