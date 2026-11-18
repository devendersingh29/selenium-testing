from playwright.sync_api import Locator, expect

from Locators.Locator_Manager import LocatorManager
from Pages.ContactFormPage import ContactFormPage


class PageManager(ContactFormPage):
    """Actions and fields exposed by the Manager screen."""

    @property
    def manager_side_button(self) -> Locator:
        return self.locator(LocatorManager.SIDE_MENU)

    def click_manager_side_button(self) -> None:
        self.open_sidebar_page(self.manager_side_button, "dashboard/manager")

    @property
    def add_manager_button(self) -> Locator:
        return self.locator(LocatorManager.ADD_BUTTON)

    @property
    def search_input(self) -> Locator:
        return self.locator(LocatorManager.SEARCH_INPUT)

    def click_add_manager_button(self) -> None:
        self.click_when_visible(self.add_manager_button)
        expect(self.create_manager_dialog).to_be_visible()

    @property
    def create_manager_dialog(self) -> Locator:
        title = self.page.get_by_text("Create Manager", exact=True)
        return title.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Cancel'] "
            "and .//button[normalize-space()='Create']][1]"
        )

    @property
    def create_success_message(self) -> Locator:
        return self.page.locator(LocatorManager.CREATE_SUCCESS_MESSAGE)

    @property
    def dialog_title(self) -> Locator:
        return self.create_manager_dialog.get_by_text(
            "Create Manager",
            exact=True,
        )

    @property
    def form_textboxes(self) -> Locator:
        return self.create_manager_dialog.get_by_role(
            "textbox",
            name="Enter",
            exact=True,
        )

    @property
    def first_name_input(self) -> Locator:
        return self.form_textboxes.nth(0)

    @property
    def last_name_input(self) -> Locator:
        return self.form_textboxes.nth(1)

    @property
    def email_input(self) -> Locator:
        return self.form_textboxes.nth(2)

    @property
    def phone_number_input(self) -> Locator:
        return self.form_textboxes.nth(3)

    @property
    def designation_input(self) -> Locator:
        return self.form_textboxes.nth(4)

    def fill_designation(self, designation: str) -> None:
        self.fill_and_verify(self.designation_input, designation)

    @property
    def reporting_to_dropdown(self) -> Locator:
        return self.create_manager_dialog.get_by_role("combobox")

    def select_first_reporting_to(self) -> None:
        """Select the first enabled, non-placeholder Reporting To option."""
        expect(self.create_manager_dialog).to_be_visible()
        options = self.reporting_to_dropdown.locator("option:not([disabled])")

        for index in range(options.count()):
            option = options.nth(index)
            option_value = option.get_attribute("value")
            if option_value:
                self.reporting_to_dropdown.select_option(value=option_value)
                expect(self.reporting_to_dropdown).to_have_value(option_value)
                return

        raise AssertionError("Reporting To dropdown has no selectable options")

    def validate_create_manager_dialog_visible(self) -> None:
        expect(self.create_manager_dialog).to_be_visible()

    def validate_create_manager_dialog_title(self) -> None:
        expect(self.dialog_title).to_have_text("Create Manager")

    def validate_create_manager_dialog_labels(self) -> None:
        labels = [
            "FIRST NAME",
            "LAST NAME",
            "EMAIL ID",
            "PHONE NUMBER",
            "DESIGNATION",
            "REPORTING TO",
        ]
        for lbl in labels:
            self.assert_label_visible(self.create_manager_dialog, lbl)

    def validate_create_manager_dialog(self) -> None:
        """Backward-compatible combined validation for the Create Manager dialog."""
        self.validate_create_manager_dialog_visible()
        self.validate_create_manager_dialog_title()
        self.validate_create_manager_dialog_labels()

    @property
    def cancel_button(self) -> Locator:
        return self.create_manager_dialog.locator(LocatorManager.CANCEL_BUTTON)

    @property
    def create_button(self) -> Locator:
        return self.create_manager_dialog.locator(LocatorManager.CREATE_BUTTON)

    def click_cancel_button(self) -> None:
        """Click the cancel button on the Create Manager dialog and verify it closes."""
        self.click_when_visible(self.cancel_button)
        expect(self.create_manager_dialog).to_be_hidden()

    def get_manager_success_message(self) -> str:
        """Capture and validate the top-right success toast message after manager creation."""
        success_message = self.create_success_message.last
        expect(success_message).to_be_visible()
        message_text = success_message.inner_text().strip()
        message_text = message_text.replace("\u200b", "").replace("\r", " ").replace("\n", " ")
        message_text = " ".join(message_text.split())
        assert "manager created successfully" in message_text.lower()
        return message_text

    def validate_manager_created_successfully(self, full_name: str) -> None:
        """Assert the toast and the created manager row are both visible on the screen."""
        success_message = self.get_manager_success_message()
        assert success_message
        expect(self.page.get_by_text(full_name, exact=True).first).to_be_visible()

    def create_manager(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        designation: str,
    ) -> str:
        """Fill the create form, submit it, and verify the manager is saved."""
        self.fill_contact_details(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.fill_designation(designation)
        self.select_first_reporting_to()
        self.click_when_visible(self.create_button)
        expect(self.create_manager_dialog).to_be_hidden()
        full_name = f"{first_name} {last_name}"
        self.validate_manager_created_successfully(full_name)
        return full_name

    def search_manager(self, keyword: str) -> None:
        """Apply the manager search filter if the list exposes a search box."""
        if self.search_input.count() == 0:
            raise AssertionError("Manager list search field is not present in the current DOM.")
        search_box = self.search_input.first
        expect(search_box).to_be_visible()
        search_box.fill(keyword)
        expect(search_box).to_have_value(keyword)

    def verify_search_result(self, expected_name: str, hidden_names=None) -> None:
        """Verify the search result is visible and unrelated values are filtered out."""
        expect(self.page.get_by_text(expected_name, exact=True).first).to_be_visible()
        if hidden_names:
            for name in hidden_names:
                expect(self.page.get_by_text(name, exact=True)).to_have_count(0)
