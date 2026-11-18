from playwright.sync_api import Locator, expect

from Locators.Locator_recruiter import Locator_Recruiter
from Pages.ContactFormPage import ContactFormPage


class Page_Recruiter(ContactFormPage):
    """Actions and fields exposed by the Recruiter screen."""

    @property
    def recruiter_side_menu(self) -> Locator:
        return self.locator(Locator_Recruiter.CLICK_SIDE_MENU_REC)

    def click_recruiter_side_menu(self) -> None:
        self.open_sidebar_page(
            self.recruiter_side_menu,
            "dashboard/recruiter",
        )

    @property
    def add_recruiter_button(self) -> Locator:
        return self.locator(Locator_Recruiter.CLICK_ADD_REC)

    @property
    def search_input(self) -> Locator:
        return self.locator(Locator_Recruiter.SEARCH_INPUT)

    def click_add_recruiter_button(self) -> None:
        self.click_when_visible(self.add_recruiter_button)
        expect(self.create_recruiter_dialog).to_be_visible()

    @property
    def first_name_input(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_FIRST_NAME_REC)

    @property
    def last_name_input(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_LAST_NAME_REC)

    @property
    def email_input(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_EMAIL_REC)

    @property
    def phone_number_input(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_PHONE_REC)

    @property
    def role_type_dropdown(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_ROLE_REC)

    def select_role_type(self, role_type: str) -> None:
        self.select_option_by_label(self.role_type_dropdown, role_type)

    @property
    def team_dropdown(self) -> Locator:
        return self.locator(Locator_Recruiter.ADD_TEAM_REC)

    def select_team(self, team_name: str) -> None:
        self.select_option_by_label(self.team_dropdown, team_name)

    @property
    def create_recruiter_dialog(self) -> Locator:
        return self.first_name_input.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Cancel'] "
            "and .//button[normalize-space()='Create']][1]"
        )

    @property
    def dialog_title(self) -> Locator:
        return self.create_recruiter_dialog.get_by_text("Create Recruiter", exact=True)

    @property
    def cancel_button(self) -> Locator:
        return self.create_recruiter_dialog.locator(Locator_Recruiter.CANCEL_BUTTON)

    @property
    def create_button(self) -> Locator:
        return self.create_recruiter_dialog.locator(Locator_Recruiter.CREATE_BUTTON)

    @property
    def create_success_message(self) -> Locator:
        return self.page.locator(Locator_Recruiter.CREATE_SUCCESS_MESSAGE)

    def validate_create_recruiter_dialog_visible(self) -> None:
        expect(self.create_recruiter_dialog).to_be_visible()

    def validate_create_recruiter_dialog_title(self) -> None:
        expect(self.dialog_title).to_have_text("Create Recruiter")

    def validate_create_recruiter_dialog_labels(self) -> None:
        labels = [
            "FIRST NAME",
            "LAST NAME",
            "EMAIL ID",
            "PHONE NUMBER",
            "ROLE TYPE",
            "Team",
        ]
        for lbl in labels:
            self.assert_label_visible(self.create_recruiter_dialog, lbl)

    def validate_create_recruiter_dialog_action_buttons(self) -> None:
        expect(self.cancel_button).to_be_visible()
        expect(self.create_button).to_be_visible()

    def validate_create_recruiter_dialog(self) -> None:
        """Backward-compatible combined validation for the Create Recruiter dialog."""
        self.validate_create_recruiter_dialog_visible()
        self.validate_create_recruiter_dialog_title()
        self.validate_create_recruiter_dialog_labels()
        self.validate_create_recruiter_dialog_action_buttons()

    def click_cancel_button(self) -> None:
        self.click_when_visible(self.cancel_button)
        expect(self.create_recruiter_dialog).to_be_hidden()

    def validate_recruiter_created_successfully(self, full_name: str) -> None:
        """Assert both the confirmation toast and the created recruiter name are visible."""
        expect(self.create_success_message.first).to_be_visible()
        expect(self.page.get_by_text(full_name, exact=True).first).to_be_visible()

    def create_recruiter(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        role_type: str = "Recruiter",
        team_name: str = "First Lead",
    ) -> str:
        """Fill the recruiter form, submit it, and confirm it is saved."""
        self.fill_contact_details(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.select_role_type(role_type)
        self.select_team(team_name)
        self.click_when_visible(self.create_button)
        expect(self.create_recruiter_dialog).to_be_hidden()
        full_name = f"{first_name} {last_name}"
        self.validate_recruiter_created_successfully(full_name)
        return full_name

    def search_recruiter(self, keyword: str) -> None:
        """Type a keyword and validate the recruiter search field retained the value."""
        if self.search_input.count() == 0:
            raise AssertionError("Recruiter list search field is not present in the current DOM.")
        search_box = self.search_input.first
        expect(search_box).to_be_visible()
        search_box.fill(keyword)
        expect(search_box).to_have_value(keyword)

    def verify_search_result(self, expected_name: str, hidden_names=None) -> None:
        """Verify the expected recruiter remains visible and other names disappear."""
        expect(self.page.get_by_text(expected_name, exact=True).first).to_be_visible()
        if hidden_names:
            for name in hidden_names:
                expect(self.page.get_by_text(name, exact=True)).to_have_count(0)
