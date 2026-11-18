from playwright.sync_api import Locator

from Locators.SigninLocator import SigninLocator
from Pages.BasePage import BasePage


class SigninPage(BasePage):
    """Actions and elements for choosing and completing organization sign-up."""

    @property
    def organization_signup_link(self) -> Locator:
        return self.locator(SigninLocator.ORG_SIGNUP_URL)

    @property
    def organization_name_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_NAME)

    @property
    def first_name_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_NAME_FIRST)

    @property
    def last_name_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_NAME_LAST)

    @property
    def email_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_EMAIL)

    @property
    def mobile_number_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_MOBILE_NUMBER)

    @property
    def designation_input(self) -> Locator:
        return self.locator(SigninLocator.ORG_DESIGNATION)

    def open_organization_signup(self) -> None:
        self.organization_signup_link.click()

    def click_login_button(self) -> None:
        self.locator(SigninLocator.ORG_LOGIN_BUTTON).click()



    def fill_organization_signup_form(self,
        organization_name: str,
        first_name: str,
        last_name: str,
        email: str,
        mobile_number: str,
        designation: str,
    ) -> None:
        self.organization_name_input.fill(organization_name)
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.mobile_number_input.fill(mobile_number)
        self.designation_input.fill(designation)
