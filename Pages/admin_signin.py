import re

from playwright.sync_api import Locator, expect

from Locators.locator_admin_signin import LocatorAdminSignin
from Pages.BasePage import BasePage


class AdminSignin(BasePage):
    """Actions and elements exposed by the administrator sign-in page."""

    @property
    def login_email(self) -> Locator:
        return self.locator(LocatorAdminSignin.login_email_id)

    @property
    def login_password(self) -> Locator:
        return self.locator(LocatorAdminSignin.login_password)

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role(**LocatorAdminSignin.login_button)

    @property
    def smart_recruit_logo(self) -> Locator:
        """Return the SmartRecruit brand logo displayed in the top-left corner."""
        return self.page.get_by_alt_text(
            LocatorAdminSignin.SMART_RECRUIT_LOGO,
            exact=True,
        ).first

    def enter_email(self, email: str) -> None:
        self.login_email.fill(email)

    def enter_password(self, password: str) -> None:
        self.login_password.fill(password)

    def click_login(self) -> None:
        self.login_button.click()

    def login(self, email: str, password: str) -> None:
        """Sign in and wait until an authenticated dashboard route is open."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        expect(self.page).to_have_url(
            re.compile(r".*/#/dashboard/.*"),
            timeout=30_000,
        )
