from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from Pages.Page_Client import PageClient

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.client,
]


def _open_create_client_dialog(admin_page: Page) -> PageClient:
    client_page = PageClient(admin_page)
    client_page.click_client_side_button()
    client_page.click_add_client_button()
    return client_page


@pytest.mark.form
@pytest.mark.read_only
def test_create_client_dialog_visible(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.validate_create_client_dialog_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_create_client_dialog_title(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.validate_create_client_dialog_title()


@pytest.mark.form
@pytest.mark.read_only
def test_create_client_dialog_labels(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.validate_create_client_dialog_labels()


@pytest.mark.form
@pytest.mark.read_only
def test_create_client_dialog_action_buttons(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.validate_create_client_dialog_action_buttons()


@pytest.mark.form
@pytest.mark.read_only
def test_cancel_button_closes_create_client_dialog(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.click_cancel_button()
    expect(client_page.create_client_dialog).to_be_hidden()


@pytest.mark.form
@pytest.mark.read_only
def test_fill_add_client_form(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    client_page.fill_organization("Auto_JPMorgan")
    client_page.fill_contact_details(
        first_name="Paul",
        last_name="Walker",
        email="prakash.lavania+autoclient@walkingtree.tech",
        phone_number="9876543210",
    )


@pytest.mark.create
@pytest.mark.data_mutation
def test_create_client_and_validate_success(admin_page: Page) -> None:
    client_page = _open_create_client_dialog(admin_page)
    time_suffix = datetime.now().strftime("%d%H%M%S")
    organization_name = f"AutoClientCreate{time_suffix}"
    email = f"prakash.lavania+{organization_name}@walkingtree.tech"
    phone_number = f"9{time_suffix}{time_suffix[-1:]}"

    client_page.create_client(
        organization_name=organization_name,
        first_name="Auto",
        last_name="Client",
        email=email,
        phone_number=phone_number,
    )


@pytest.mark.search
@pytest.mark.read_only
def test_client_search_filters_results(admin_page: Page) -> None:
    client_page = PageClient(admin_page)
    client_page.click_client_side_button()

    keyword = "Microsoft_second"
    client_page.search_client(keyword)
    client_page.verify_search_result(keyword, hidden_names=["Microsoft_first"])
