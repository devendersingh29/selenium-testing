from playwright.sync_api import Locator, expect

from Locators.Locator_Client import ClientLocator
from Pages.ContactFormPage import ContactFormPage


class PageClient(ContactFormPage):
    """Actions and fields exposed by the Client screen."""

    @property
    def client_side_button(self) -> Locator:
        return self.locator(ClientLocator.SIDE_MENU)

    def click_client_side_button(self) -> None:
        self.open_sidebar_page(
            self.client_side_button,
            "dashboard/masters/client",
        )

    @property
    def add_client_button(self) -> Locator:
        return self.locator(ClientLocator.ADD_BUTTON)

    @property
    def search_input(self) -> Locator:
        return self.locator(ClientLocator.SEARCH_INPUT)

    def click_add_client_button(self) -> None:
        self.click_when_visible(self.add_client_button)
        expect(self.create_client_dialog).to_be_visible()

    @property
    def organization_input(self) -> Locator:
        return self.locator(ClientLocator.ORGANIZATION_INPUT)

    def fill_organization(self, organization_name: str) -> None:
        self.fill_and_verify(self.organization_input, organization_name)

    @property
    def first_name_input(self) -> Locator:
        return self.locator(ClientLocator.FIRST_NAME_INPUT)

    @property
    def last_name_input(self) -> Locator:
        return self.locator(ClientLocator.LAST_NAME_INPUT)

    @property
    def email_input(self) -> Locator:
        return self.locator(ClientLocator.EMAIL_INPUT)

    @property
    def phone_number_input(self) -> Locator:
        return self.locator(ClientLocator.PHONE_NUMBER_INPUT)

    @property
    def create_client_dialog(self) -> Locator:
        # Find the dialog container by locating the title and walking up to the dialog
        title = self.page.get_by_text("Create Client", exact=True)
        return title.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Cancel'] "
            "and .//button[normalize-space()='Create']][1]"
        )

    @property
    def dialog_title(self) -> Locator:
        return self.create_client_dialog.get_by_text("Create Client", exact=True)

    @property
    def cancel_button(self) -> Locator:
        return self.create_client_dialog.locator(ClientLocator.CANCEL_BUTTON)

    @property
    def create_button(self) -> Locator:
        return self.create_client_dialog.locator(ClientLocator.CREATE_BUTTON)

    @property
    def create_success_message(self) -> Locator:
        return self.page.locator(ClientLocator.CREATE_SUCCESS_MESSAGE)

    def validate_create_client_dialog_visible(self) -> None:
        expect(self.create_client_dialog).to_be_visible()

    def validate_create_client_dialog_title(self) -> None:
        expect(self.dialog_title).to_have_text("Create Client")

    def validate_create_client_dialog_labels(self) -> None:
        labels = [
            "ORGANIZATION NAME",
            "FIRST NAME",
            "LAST NAME",
            "EMAIL ID",
            "PHONE NUMBER",
        ]
        for lbl in labels:
            self.assert_label_visible(self.create_client_dialog, lbl)

    def validate_create_client_dialog_action_buttons(self) -> None:
        expect(self.cancel_button).to_be_visible()
        expect(self.create_button).to_be_visible()

    def validate_create_client_dialog(self) -> None:
        """Backward-compatible combined validation for the Create Client dialog."""
        self.validate_create_client_dialog_visible()
        self.validate_create_client_dialog_title()
        self.validate_create_client_dialog_labels()
        self.validate_create_client_dialog_action_buttons()

    def click_cancel_button(self) -> None:
        self.click_when_visible(self.cancel_button)
        expect(self.create_client_dialog).to_be_hidden()

    def validate_client_created_successfully(self, organization_name: str) -> None:
        """Verify the confirmation alert is visible and the created record appears."""
        expect(self.create_success_message.first).to_be_visible()
        expect(self.page.get_by_text(organization_name, exact=True).first).to_be_visible()

    def create_client(
        self,
        *,
        organization_name: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
    ) -> str:
        """Fill the form, click Create, and verify successful save."""
        self.fill_organization(organization_name)
        self.fill_contact_details(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.click_when_visible(self.create_button)
        expect(self.create_client_dialog).to_be_hidden()
        self.validate_client_created_successfully(organization_name)
        return organization_name

    def search_client(self, keyword: str) -> None:
        """Type a keyword, validate the search box value, and wait for filtered results."""
        expect(self.search_input).to_be_visible()
        self.search_input.fill(keyword)
        expect(self.search_input).to_have_value(keyword)
        expect(self.page.locator("body")).to_contain_text(keyword)

    def verify_search_result(self, expected_name: str, hidden_names=None) -> None:
        """Verify the expected row is visible and unrelated names are filtered out."""
        expect(self.page.get_by_text(expected_name, exact=True).first).to_be_visible()
        if hidden_names:
            for name in hidden_names:
                expect(self.page.get_by_text(name, exact=True)).to_have_count(0)
