class LocatorEditOpening:
    """Locators for Edit Opening flow.

    Prefer stable text and role-based locators. If UI differs, provide DOM
    snippets and these will be tuned.
    """

    JOB_OPENING_SIDE_BUTTON = "a[href='#/dashboard/jobopening']"
    JOB_CARD = "article"

    # 3-dots / More button on a job card (aria-label='More' observed in project)
    CLICK_3DOTS = "xpath=.//button[@aria-label='More']"

    # Edit Opening option in the context menu
    CLICK_EDIT_OPENING = "xpath=//span[normalize-space()='Edit Opening']"

    # Job content editor (jodit editor contenteditable div used elsewhere in project)
    JOB_CONTENT_EDITOR = "(//div[contains(@class,'jodit-wysiwyg') and @contenteditable='true'])[1]"

    # Continue and Update buttons (text-based locators)
    CONTINUE_BUTTON = "xpath=//button[normalize-space()='Continue']"
    UPDATE_OPENING_BUTTON = "xpath=//button[contains(normalize-space(),'Update') or contains(normalize-space(),'Update Opening')]"

    # Success message that should appear after editing
    EDIT_SUCCESS_MESSAGE = "xpath=//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'edited successfully') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'edited successfully.') ]"
