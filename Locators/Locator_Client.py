


from Locators.common import sidebar_link, text_button


class ClientLocator:
    SIDE_MENU = sidebar_link("Client")
    ADD_BUTTON = text_button("Add Client")
    SEARCH_INPUT = "//input[@placeholder='Search clients or organizations']"
    ORGANIZATION_INPUT = "//input[@name='create-client-organizationName']"
    FIRST_NAME_INPUT = "//input[@name='create-client-firstName']"
    LAST_NAME_INPUT = "//input[@name='create-client-lastName']"
    EMAIL_INPUT = "//input[@name='create-client-emailId']"
    PHONE_NUMBER_INPUT = "//input[@name='create-client-phoneNumber']"
    CANCEL_BUTTON = text_button("Cancel")
    CREATE_BUTTON = text_button("Create")
    CREATE_SUCCESS_MESSAGE = (
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'client created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'created successfully')]"
    )
