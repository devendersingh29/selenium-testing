
from Locators.common import sidebar_link, text_button


class LocatorManager:
    SIDE_MENU = sidebar_link("Manager")
    ADD_BUTTON = text_button("Add Manager")
    SEARCH_INPUT = "//input[(contains(@placeholder, 'Search') or @aria-label='Search' or @name='Search')]"
    CANCEL_BUTTON = text_button("Cancel")
    CREATE_BUTTON = text_button("Create")
    CREATE_SUCCESS_MESSAGE = (
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'manager created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'created successfully')]"
    )

    