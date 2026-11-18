
from Locators.common import labeled_input, sidebar_link, text_button


class LocatorsPanel:
    PANEL_SIDE_MENU = sidebar_link("Panel")
    ADD_PANEL_BUTTON = text_button("Add Panel")
    ADD_FIRST_NAME = labeled_input("FIRST NAME")
    ADD_LAST_NAME = labeled_input("LAST NAME")
    ADD_PANEL_EMAIL = labeled_input("EMAIL ID")
    ADD_PANEL_NUMBER = labeled_input("PHONE NUMBER")
    CANCEL_BUTTON = text_button("Cancel")
    CREATE_BUTTON = text_button("Create")
    CREATE_SUCCESS_MESSAGE = (
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'panel member created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'panel created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'created successfully')]"
    )
