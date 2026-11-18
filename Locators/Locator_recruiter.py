
from Locators.common import labeled_input, labeled_select, sidebar_link, text_button


class Locator_Recruiter:
    CLICK_SIDE_MENU_REC = sidebar_link("Recruiter")
    CLICK_ADD_REC = text_button("Add Recruiter")
    SEARCH_INPUT = "//input[(contains(@placeholder, 'Search') or @aria-label='Search' or @name='Search')]"
    ADD_FIRST_NAME_REC = labeled_input("FIRST NAME")
    ADD_LAST_NAME_REC = labeled_input("LAST NAME")
    ADD_EMAIL_REC = labeled_input("EMAIL ID")
    ADD_PHONE_REC = labeled_input("PHONE NUMBER")
    ADD_ROLE_REC = labeled_select("ROLE TYPE")
    ADD_TEAM_REC = "(//*[normalize-space()='Team * :' or normalize-space()='Team :' or normalize-space()='Team']/following::select[1])[1]"
    CANCEL_BUTTON = text_button("Cancel")
    CREATE_BUTTON = text_button("Create")
    CREATE_SUCCESS_MESSAGE = (
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'recruiter created successfully') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'created successfully')]"
    )
