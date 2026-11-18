from abc import ABC, abstractmethod

from playwright.sync_api import Locator

from Pages.BasePage import BasePage


class ContactFormPage(BasePage, ABC):
    """Shared name and contact-field behavior for role setup forms."""

    @property
    @abstractmethod
    def first_name_input(self) -> Locator:
        raise NotImplementedError

    @property
    @abstractmethod
    def last_name_input(self) -> Locator:
        raise NotImplementedError

    @property
    @abstractmethod
    def email_input(self) -> Locator:
        raise NotImplementedError

    @property
    @abstractmethod
    def phone_number_input(self) -> Locator:
        raise NotImplementedError

    def fill_first_name(self, first_name: str) -> None:
        self.fill_and_verify(self.first_name_input, first_name)

    def fill_last_name(self, last_name: str) -> None:
        self.fill_and_verify(self.last_name_input, last_name)

    def fill_email(self, email: str) -> None:
        self.fill_and_verify(self.email_input, email)

    def fill_phone_number(self, phone_number: str) -> None:
        self.fill_and_verify(self.phone_number_input, phone_number)

    def fill_contact_details(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
    ) -> None:
        """Fill the contact fields shared by role setup forms."""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.fill_phone_number(phone_number)

    def get_first_name(self) -> str:
        return self.first_name_input.input_value()
