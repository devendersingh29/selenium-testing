from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from Pages.Pages_Panel import PagesPanel

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.panel,
]


def _open_create_panel_dialog(admin_page: Page) -> PagesPanel:
    panel_page = PagesPanel(admin_page)
    panel_page.click_panel_menu()
    panel_page.click_add_panel_button()
    return panel_page


@pytest.mark.form
@pytest.mark.read_only
def test_create_panel_dialog_visible(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.validate_create_panel_dialog_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_create_panel_dialog_title(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.validate_create_panel_dialog_title()


@pytest.mark.form
@pytest.mark.read_only
def test_create_panel_dialog_labels(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.validate_create_panel_dialog_labels()


@pytest.mark.form
@pytest.mark.read_only
def test_create_panel_dialog_action_buttons(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.validate_create_panel_dialog_action_buttons()


@pytest.mark.form
@pytest.mark.read_only
def test_cancel_button_closes_create_panel_dialog(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.click_cancel_button()
    expect(panel_page.create_panel_dialog).to_be_hidden()


@pytest.mark.form
@pytest.mark.read_only
def test_fill_add_panel_form(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    panel_page.fill_contact_details(
        first_name="Auto",
        last_name="Panel",
        email="prakash.lavania+AutoPanel@walkingtree.tech",
        phone_number="9987656780",
    )


@pytest.mark.create
@pytest.mark.data_mutation
def test_create_panel_and_validate_success(admin_page: Page) -> None:
    panel_page = _open_create_panel_dialog(admin_page)
    time_suffix = datetime.now().strftime("%d%H%M%S")
    full_name = panel_page.create_panel(
        first_name="Auto",
        last_name="Panel",
        email=f"prakash.lavania+AutoPanel{time_suffix}@walkingtree.tech",
        phone_number=f"9{time_suffix}{time_suffix[-1:]}",
    )
    panel_page.validate_panel_created_successfully(full_name)
