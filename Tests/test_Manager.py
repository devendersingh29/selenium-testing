from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from Pages.Manager import PageManager

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.manager,
]


def _open_create_manager_dialog(admin_page: Page) -> PageManager:
    manager_page = PageManager(admin_page)
    manager_page.click_manager_side_button()
    manager_page.click_add_manager_button()
    return manager_page


@pytest.mark.form
@pytest.mark.read_only
def test_create_manager_dialog_visible(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    manager_page.validate_create_manager_dialog_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_create_manager_dialog_title(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    manager_page.validate_create_manager_dialog_title()


@pytest.mark.form
@pytest.mark.read_only
def test_create_manager_dialog_labels(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    manager_page.validate_create_manager_dialog_labels()


@pytest.mark.form
@pytest.mark.read_only
def test_cancel_button_closes_create_manager_dialog(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    manager_page.click_cancel_button()
    expect(manager_page.create_manager_dialog).to_be_hidden()


@pytest.mark.form
@pytest.mark.read_only
def test_fill_add_manager_form(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    manager_page.fill_contact_details(
        first_name="Auto",
        last_name="Manager",
        email="prakash.lavania+manager+Auto@walkingtree.tech",
        phone_number="0123456789",
    )
    manager_page.fill_designation("Auto Manager")
    manager_page.select_first_reporting_to()


@pytest.mark.create
@pytest.mark.data_mutation
def test_create_manager_and_validate_success(admin_page: Page) -> None:
    manager_page = _open_create_manager_dialog(admin_page)
    time_suffix = datetime.now().strftime("%d%H%M%S")
    full_name = manager_page.create_manager(
        first_name="Auto",
        last_name="Manager",
        email=f"prakash.lavania+AutoManager{time_suffix}@walkingtree.tech",
        phone_number=f"9{time_suffix}{time_suffix[-1:]}",
        designation=f"Auto Manager {time_suffix}",
    )
    success_message = manager_page.get_manager_success_message()
    print(f"Top-right notification: {success_message}")
    print(f"Manager created successfully: {full_name}")
    manager_page.validate_manager_created_successfully(full_name)


@pytest.mark.search
@pytest.mark.read_only
def test_manager_search_filters_results(admin_page: Page) -> None:
    manager_page = PageManager(admin_page)
    manager_page.click_manager_side_button()

    if manager_page.search_input.count() == 0:
        pytest.skip("Manager list search input is not present in the current DOM.")

    keyword = "Second"
    manager_page.search_manager(keyword)
    manager_page.verify_search_result("Second Manager", hidden_names=["First Manager"])
