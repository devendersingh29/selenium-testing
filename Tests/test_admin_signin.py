from playwright.sync_api import Page, expect

import pytest

from Config.config import Config
from Pages.WelcomePage import WelcomePage
from Pages.admin_signin import AdminSignin

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.authentication,
    pytest.mark.admin,
    pytest.mark.smoke,
    pytest.mark.e2e,
    pytest.mark.read_only,
]


def test_admin_login(page: Page) -> None:
    WelcomePage(page).open_organization_signin()
    admin_signin = AdminSignin(page)

    expect(admin_signin.smart_recruit_logo).to_be_visible()
    print("SmartRecruit logo is visible successfully.")
    admin_signin.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
