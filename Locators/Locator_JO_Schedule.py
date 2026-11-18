class LocatorJOSchedule:
    """Locators used for Job Opening - Schedule flow.

    These are intentionally conservative: prefer role/text locators and
    use stable attributes where possible. If the real DOM differs, supply
    snippets and locators will be adjusted.
    """

    JOB_OPENING_SIDE_BUTTON = "a[href='#/dashboard/jobopening']"
    JOB_CARD = "article"

    # Schedule button inside job card (may be a button or menu item)
    SCHEDULE_BUTTON_IN_CARD = "xpath=.//button[contains(normalize-space(), 'Schedule') or contains(normalize-space(), 'Schedule Interview') or contains(@aria-label,'Schedule')]"

    # When no candidates in schedule stage, app may show this message
    NO_CANDIDATES_MESSAGE = "xpath=//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'no candidates at this stage') ]"

    # Manage setup and generate controls
    MANAGE_SETUP_BUTTON = "xpath=//button[normalize-space()='Manage setup' or contains(normalize-space(), 'Manage setup')]"
    GENERATE_FULL_SETUP_BUTTON = "xpath=//button[contains(normalize-space(),'Generate full setup') or contains(normalize-space(),'Generate Full Setup')]"

    # Duration inputs inside generate popup
    MIN_DURATION_INPUT = "xpath=//input[@placeholder='Min Duration' or @name='minDuration' or contains(@aria-label,'Min') ]"
    MAX_DURATION_INPUT = "xpath=//input[@placeholder='Max Duration' or @name='maxDuration' or contains(@aria-label,'Max') ]"

    GENERATE_BUTTON = "xpath=//button[normalize-space()='Generate']"
    SAVE_SETUP_BUTTON = "xpath=//button[normalize-space()='Save setup' or normalize-space()='Save Setup']"

    # CBT assessment flow
    CBT_ASSESSMENT_BUTTON = "xpath=//button[contains(normalize-space(), 'CBT') or contains(normalize-space(), 'CBT assessment') or contains(normalize-space(), 'CBT Assessment')]"
    CBT_EMAIL_INPUT = "xpath=//input[@placeholder='candidate@example.com' or contains(@placeholder,'candidate@example.com') ]"
    CBT_START_DATE_INPUT = "xpath=//input[@type='date' and (contains(@placeholder,'Start') or contains(@aria-label,'Start'))]"
    CBT_WINDOW_CLOSE_DATE_INPUT = "xpath=//input[@type='date' and (contains(@placeholder,'Window') or contains(@aria-label,'Window'))]"
    CBT_START_TIME_INPUT = "xpath=//input[@type='time' and (contains(@placeholder,'Start time') or contains(@aria-label,'Start time'))]"
    CBT_END_TIME_INPUT = "xpath=//input[@type='time' and (contains(@placeholder,'End time') or contains(@aria-label,'End time'))]"
    CONFIRM_AND_SEND_BUTTON = "xpath=//button[contains(normalize-space(),'Confirm and send invite') or contains(normalize-space(),'Confirm & Send') or contains(normalize-space(),'Confirm and send')]"

    EVENT_CREATED_MESSAGE = "xpath=//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'event created successfully') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'event created successfully.') ]"
