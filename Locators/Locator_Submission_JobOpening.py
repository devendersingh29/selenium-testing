class LocatorSubmissionJobOpening:
    """Locators related to the Submission button and submission details panel.

    Note: The app's DOM for the submission details panel may vary; the
    locators below provide reasonable, non-fragile defaults. If the
    submission panel uses different element names/classes/roles in your
    environment, provide a short DOM snippet and the locators will be
    adjusted accordingly.
    """

    JOB_OPENING_SIDE_BUTTON = "a[href='#/dashboard/jobopening']"
    JOB_CARD = "article"
    JOB_CARD_HEADING = "h3"

    # Submissions button inside a job card (e.g., "0 Submissions", "3 Submissions")
    # This is intended to be used with job_card.locator(...)
    SUBMISSIONS_BUTTON_IN_CARD = "xpath=.//button[contains(normalize-space(), 'Submissions')]"

    # Primary: submissions panel/modal/dialog that appears after clicking the button
    # We look for a role=dialog or an element containing the word 'Submissions' as a heading
    SUBMISSIONS_PANEL_DIALOG = "xpath=//div[@role='dialog']"
    SUBMISSIONS_PANEL_HEADING = "xpath=//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submissions')] | //h3[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submissions')]"

    # Rows/items inside the submissions panel; prefer role=listitem if available
    SUBMISSION_ROW_ROLE = "[role='listitem']"
    # Fallback generic row selectors (li or divs commonly used)
    SUBMISSION_ROW_FALLBACK = "xpath=//li | xpath=//div[contains(@class,'submission') or contains(@class,'candidate') ]"
