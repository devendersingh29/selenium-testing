from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from Pages.Pages_Vendor import PageVendor

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.vendor,
]


def _open_create_vendor_dialog(admin_page: Page) -> PageVendor:
    vendor_page = PageVendor(admin_page)
    vendor_page.click_vendor_side_menu()
    vendor_page.click_add_vendor_button()
    return vendor_page


@pytest.mark.form
@pytest.mark.read_only
def test_create_vendor_dialog_visible(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.validate_create_vendor_dialog_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_create_vendor_dialog_title(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.validate_create_vendor_dialog_title()


@pytest.mark.form
@pytest.mark.read_only
def test_create_vendor_dialog_labels(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.validate_create_vendor_dialog_labels()


@pytest.mark.form
@pytest.mark.read_only
def test_create_vendor_dialog_action_buttons(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.validate_create_vendor_dialog_action_buttons()


@pytest.mark.form
@pytest.mark.read_only
def test_cancel_button_closes_create_vendor_dialog(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.click_cancel_button()
    expect(vendor_page.create_vendor_dialog).to_be_hidden()


@pytest.mark.form
@pytest.mark.read_only
def test_fill_add_vendor_form(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    vendor_page.fill_organization("JP Morgan")
    vendor_page.fill_contact_details(
        first_name="Michael",
        last_name="Jackson",
        email="prakash.lavania+auto.vendor@walkingtree.tech",
        phone_number="1234512340",
    )


@pytest.mark.create
@pytest.mark.data_mutation
def test_create_vendor_and_validate_success(admin_page: Page) -> None:
    vendor_page = _open_create_vendor_dialog(admin_page)
    time_suffix = datetime.now().strftime("%d%H%M%S")
    organization_name = f"Auto Vendor {time_suffix}"
    success_message = vendor_page.create_vendor(
        organization_name=organization_name,
        first_name="Auto",
        last_name="Vendor",
        email=f"prakash.lavania+AutoVendor{time_suffix}@walkingtree.tech",
        phone_number=f"9{time_suffix}{time_suffix[-1:]}",
    )
    vendor_page.validate_vendor_created_successfully(organization_name)

    # Force stdout to show in the console even under pytest capture settings.
    print("\n===== VENDOR CREATION SUCCESS =====")
    print(f"Top-right notification: {success_message}")
    print(f"Vendor created successfully: {organization_name}")
    print("===================================\n")
