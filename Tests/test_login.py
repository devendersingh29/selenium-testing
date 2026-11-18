from playwright.sync_api import Page, expect

import pytest

from Pages.Signin import SigninPage
from Pages.WelcomePage import WelcomePage

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.signup,
    pytest.mark.form,
    pytest.mark.read_only,
]


def test_user_can_complete_organization_signup_form(page: Page) -> None:
    welcome_page = WelcomePage(page).open()
    signin_page = SigninPage(page)

    welcome_page.click_get_started()
    expect(signin_page.organization_signup_link).to_be_visible()

    signin_page.open_organization_signup()
    signin_page.fill_organization_signup_form(
        organization_name="Prakash Ent",
        first_name="Prakash",
        last_name="Automation",
        email="prakash.lavania@walkingtree.tech",
        mobile_number="7799592281",
        designation="Admin",
    )

    expect(signin_page.organization_name_input).to_have_value("Prakash Ent")
    expect(signin_page.first_name_input).to_have_value("Prakash")
    expect(signin_page.last_name_input).to_have_value("Automation")
    expect(signin_page.email_input).to_have_value("prakash.lavania@walkingtree.tech")
    expect(signin_page.mobile_number_input).to_have_value("7799592281")
    expect(signin_page.designation_input).to_have_value("Admin")
