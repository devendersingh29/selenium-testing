from playwright.sync_api import Locator, expect

from Locators.Locator_Panel import LocatorsPanel
from Pages.ContactFormPage import ContactFormPage


class PagesPanel(ContactFormPage):
    """Actions and fields exposed by the Panel screen."""

    @property
    def panel_side_menu(self) -> Locator:
        return self.locator(LocatorsPanel.PANEL_SIDE_MENU)

    def click_panel_menu(self) -> None:
        self.open_sidebar_page(self.panel_side_menu, "dashboard/panel")

    @property
    def panel_add_button(self) -> Locator:
        return self.locator(LocatorsPanel.ADD_PANEL_BUTTON)

    def click_add_panel_button(self) -> None:
        self.click_when_visible(self.panel_add_button)
        expect(self.create_panel_dialog).to_be_visible()

    @property
    def first_name_input(self) -> Locator:
        return self.locator(LocatorsPanel.ADD_FIRST_NAME)

    @property
    def create_panel_dialog(self) -> Locator:
        return self.first_name_input.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Cancel'] "
            "and .//button[normalize-space()='Create']][1]"
        )

    @property
    def dialog_title(self) -> Locator:
        return self.create_panel_dialog.get_by_text("Create Panel", exact=True)

    @property
    def cancel_button(self) -> Locator:
        return self.create_panel_dialog.locator(LocatorsPanel.CANCEL_BUTTON)

    @property
    def create_button(self) -> Locator:
        return self.create_panel_dialog.locator(LocatorsPanel.CREATE_BUTTON)

    @property
    def create_success_message(self) -> Locator:
        return self.page.locator(LocatorsPanel.CREATE_SUCCESS_MESSAGE)

    def click_cancel_button(self) -> None:
        self.click_when_visible(self.cancel_button)
        expect(self.create_panel_dialog).to_be_hidden()

    def validate_create_panel_dialog_visible(self) -> None:
        expect(self.create_panel_dialog).to_be_visible()

    def validate_create_panel_dialog_title(self) -> None:
        expect(self.dialog_title).to_have_text("Create Panel")

    def validate_create_panel_dialog_labels(self) -> None:
        labels = [
            "FIRST NAME",
            "LAST NAME",
            "EMAIL ID",
            "PHONE NUMBER",
        ]
        for lbl in labels:
            self.assert_label_visible(self.create_panel_dialog, lbl)

    def validate_create_panel_dialog_action_buttons(self) -> None:
        expect(self.cancel_button).to_be_visible()
        expect(self.create_button).to_be_visible()

    def validate_create_panel_dialog(self) -> None:
        """Backward-compatible combined validation for the Create Panel dialog."""
        self.validate_create_panel_dialog_visible()
        self.validate_create_panel_dialog_title()
        self.validate_create_panel_dialog_labels()
        self.validate_create_panel_dialog_action_buttons()

    @property
    def last_name_input(self) -> Locator:
        return self.locator(LocatorsPanel.ADD_LAST_NAME)

    @property
    def email_input(self) -> Locator:
        return self.locator(LocatorsPanel.ADD_PANEL_EMAIL)

    @property
    def phone_number_input(self) -> Locator:
        return self.locator(LocatorsPanel.ADD_PANEL_NUMBER)

    def validate_panel_created_successfully(self, full_name: str) -> None:
        """Assert both the confirmation message and the created panel name are visible."""
        expect(self.create_success_message.first).to_be_visible()
        expect(self.page.get_by_text(full_name, exact=True).first).to_be_visible()

    def create_panel(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
    ) -> str:
        """Fill the create form, submit it, and confirm the panel is saved."""
        self.fill_contact_details(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.click_when_visible(self.create_button)
        expect(self.create_panel_dialog).to_be_hidden()
        full_name = f"{first_name} {last_name}"
        self.validate_panel_created_successfully(full_name)
        return full_name

