from Config.config import Config
from Locators.WelcomeLocators import WelcomeLocators
from Pages.BasePage import BasePage


class WelcomePage(BasePage):
    """Actions and state exposed by the application welcome page."""

    def open(self) -> "WelcomePage":
        self.navigate(Config.BASE_URL)
        return self

    @property
    def get_started_button(self):
        return self.page.get_by_role(
            "button", name=WelcomeLocators.START_BUTTON, exact=True
        )

    def click_get_started(self) -> None:
        self.get_started_button.click()

    def continue_as_organization(self) -> None:
        self.page.get_by_role(
            "button", name=WelcomeLocators.ORGANIZATION_BUTTON, exact=True
        ).click()

    def open_organization_signin(self) -> None:
        """Open the welcome page and continue to organization sign-in."""
        self.open()
        self.click_get_started()
        self.continue_as_organization()


