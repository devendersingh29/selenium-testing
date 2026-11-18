from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from Pages.Page_Recruiter import Page_Recruiter

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.recruiter,
]


def _open_create_recruiter_dialog(admin_page: Page) -> Page_Recruiter:
    recruiter_page = Page_Recruiter(admin_page)
    recruiter_page.click_recruiter_side_menu()
    recruiter_page.click_add_recruiter_button()
    return recruiter_page


@pytest.mark.form
@pytest.mark.read_only
def test_create_recruiter_dialog_visible(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.validate_create_recruiter_dialog_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_create_recruiter_dialog_title(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.validate_create_recruiter_dialog_title()


@pytest.mark.form
@pytest.mark.read_only
def test_create_recruiter_dialog_labels(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.validate_create_recruiter_dialog_labels()


@pytest.mark.form
@pytest.mark.read_only
def test_create_recruiter_dialog_action_buttons(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.validate_create_recruiter_dialog_action_buttons()


@pytest.mark.form
@pytest.mark.read_only
def test_cancel_button_closes_create_recruiter_dialog(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.click_cancel_button()
    expect(recruiter_page.create_recruiter_dialog).to_be_hidden()


@pytest.mark.form
@pytest.mark.read_only
def test_fill_add_recruiter_form(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    recruiter_page.fill_contact_details(
        first_name="Auto",
        last_name="Recruiter",
        email="prakash.lavania+auto.recruiter@walkingtree.tech",
        phone_number="9876543210",
    )
    recruiter_page.select_role_type("Recruiter")
    recruiter_page.select_team("First Lead")


@pytest.mark.create
@pytest.mark.data_mutation
def test_create_recruiter_and_validate_success(admin_page: Page) -> None:
    recruiter_page = _open_create_recruiter_dialog(admin_page)
    time_suffix = datetime.now().strftime("%d%H%M%S")
    full_name = recruiter_page.create_recruiter(
        first_name="Auto",
        last_name="Recruiter",
        email=f"prakash.lavania+AutoRecruiter{time_suffix}@walkingtree.tech",
        phone_number=f"9{time_suffix}{time_suffix[-1:]}",
        role_type="Recruiter",
        team_name="First Lead",
    )
    recruiter_page.validate_recruiter_created_successfully(full_name)
