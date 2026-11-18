from playwright.sync_api import Locator, expect

from Locators.Locator_Vendor import VendorLocator
from Pages.ContactFormPage import ContactFormPage


class PageVendor(ContactFormPage):
    """Actions and fields exposed by the Vendor screen."""

    @property
    def vendor_side_menu(self) -> Locator:
        return self.locator(VendorLocator.VENDOR_SIDE_MENU)

    def click_vendor_side_menu(self) -> None:
        self.open_sidebar_page(self.vendor_side_menu, "dashboard/vendor")

    @property
    def add_vendor_button(self) -> Locator:
        return self.locator(VendorLocator.ADD_VENDOR_BUTTON)

    def click_add_vendor_button(self) -> None:
        self.click_when_visible(self.add_vendor_button)
        expect(self.create_vendor_dialog).to_be_visible()

    @property
    def organization_input(self) -> Locator:
        return self.locator(VendorLocator.ORGANIZATION_INPUT)

    @property
    def create_vendor_dialog(self) -> Locator:
        return self.organization_input.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Cancel'] "
            "and .//button[normalize-space()='Create']][1]"
        )

    @property
    def dialog_title(self) -> Locator:
        return self.create_vendor_dialog.get_by_text("Create Vendor", exact=True)

    @property
    def cancel_button(self) -> Locator:
        return self.create_vendor_dialog.locator(VendorLocator.CANCEL_BUTTON)

    @property
    def create_button(self) -> Locator:
        return self.create_vendor_dialog.locator(VendorLocator.CREATE_BUTTON)

    @property
    def create_success_message(self) -> Locator:
        return self.page.get_by_text("Vendor created successfully", exact=False)

    @property
    def first_name_input(self) -> Locator:
        return self.locator(VendorLocator.FIRST_NAME_INPUT)

    @property
    def last_name_input(self) -> Locator:
        return self.locator(VendorLocator.LAST_NAME_INPUT)

    @property
    def email_input(self) -> Locator:
        return self.locator(VendorLocator.EMAIL_INPUT)

    @property
    def phone_number_input(self) -> Locator:
        return self.locator(VendorLocator.PHONE_NUMBER_INPUT)

    def click_cancel_button(self) -> None:
        self.click_when_visible(self.cancel_button)
        expect(self.create_vendor_dialog).to_be_hidden()

    def fill_organization(self, organization_name: str) -> None:
        self.fill_and_verify(self.organization_input, organization_name)

    def validate_create_vendor_dialog_visible(self) -> None:
        expect(self.create_vendor_dialog).to_be_visible()

    def validate_create_vendor_dialog_title(self) -> None:
        expect(self.dialog_title).to_have_text("Create Vendor")

    def validate_create_vendor_dialog_labels(self) -> None:
        labels = [
            "ORGANIZATION NAME",
            "FIRST NAME",
            "LAST NAME",
            "EMAIL ID",
            "PHONE NUMBER",
        ]
        for lbl in labels:
            self.assert_label_visible(self.create_vendor_dialog, lbl)

    def validate_create_vendor_dialog_action_buttons(self) -> None:
        expect(self.cancel_button).to_be_visible()
        expect(self.create_button).to_be_visible()

    def validate_create_vendor_dialog(self) -> None:
        """Backward-compatible combined validation for the Create Vendor dialog."""
        self.validate_create_vendor_dialog_visible()
        self.validate_create_vendor_dialog_title()
        self.validate_create_vendor_dialog_labels()
        self.validate_create_vendor_dialog_action_buttons()

    def get_vendor_success_message(self) -> str:
        """Capture the top-right success notification text after vendor creation."""
        success_message = self.create_success_message.last
        expect(success_message).to_be_visible()
        message_text = success_message.inner_text().strip()
        message_text = message_text.replace("\u200b", "").replace("\r", " ").replace("\n", " ")
        message_text = " ".join(message_text.split())
        assert "vendor created successfully" in message_text.lower()
        return message_text

    def validate_vendor_created_successfully(self, organization_name: str) -> None:
        """Verify the save toast appears and the created vendor is visible in the list."""
        success_message = self.get_vendor_success_message()
        assert success_message
        assert "vendor created successfully" in success_message.lower()
        expect(self.page.get_by_text(organization_name, exact=True).first).to_be_visible()

    def create_vendor(
        self,
        *,
        organization_name: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
    ) -> str:
        """Fill the form, click Create, and confirm the vendor is available on the screen."""
        self.fill_organization(organization_name)
        self.fill_contact_details(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.click_when_visible(self.create_button)
        expect(self.create_vendor_dialog).to_be_hidden()
        message_text = self.get_vendor_success_message()
        self.validate_vendor_created_successfully(organization_name)
        return message_text
