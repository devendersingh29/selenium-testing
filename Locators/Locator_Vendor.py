
from Locators.common import labeled_input, sidebar_link, text_button


class VendorLocator:
    VENDOR_SIDE_MENU = sidebar_link("Vendor")
    ADD_VENDOR_BUTTON = text_button("Add Vendor")
    ORGANIZATION_INPUT = labeled_input("ORGANIZATION NAME")
    FIRST_NAME_INPUT = labeled_input("FIRST NAME")
    LAST_NAME_INPUT = labeled_input("LAST NAME")
    EMAIL_INPUT = labeled_input("EMAIL ID")
    PHONE_NUMBER_INPUT = labeled_input("PHONE NUMBER")
    CANCEL_BUTTON = text_button("Cancel")
    CREATE_BUTTON = text_button("Create")
    CREATE_SUCCESS_MESSAGE = (
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'vendor created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'created successfully')]"
    )
