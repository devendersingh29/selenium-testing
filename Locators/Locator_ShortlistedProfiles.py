class LocatorShortlistedProfiles:
    """Locators for Shortlisted profiles button and shortlisted panel.

    These follow the same conventions used by Locator_Submission_JobOpening.py:
    - JOB_OPENING_SIDE_BUTTON: side nav link to the Job Openings page
    - JOB_CARD: a generic job-card container selector
    - SHORTLISTED_BUTTON_IN_CARD: button inside the job card that shows the
      shortlisted counter (e.g. "2 Shortlisted")
    - SHORTLISTED_PANEL_DIALOG: primary dialog/panel selector
    - SHORTLISTED_PANEL_HEADING: heading containing the word 'Shortlist' or
      'Shortlisted'
    - SHORTLIST_ROW_ROLE / SHORTLIST_ROW_FALLBACK: preferred and fallback
      selectors for individual shortlisted candidate rows
    """

    JOB_OPENING_SIDE_BUTTON = "a[href='#/dashboard/jobopening']"
    JOB_CARD = "article"
    JOB_CARD_HEADING = "h3"

    # Example: button text: "3 Shortlisted" or "Shortlisted (3)"
    SHORTLISTED_BUTTON_IN_CARD = "xpath=.//button[contains(normalize-space(), 'Shortlist') or contains(normalize-space(), 'Shortlisted')]"

    # Panel/modal/dialog that appears after clicking the shortlisted button
    SHORTLISTED_PANEL_DIALOG = "xpath=//div[@role='dialog']"
    SHORTLISTED_PANEL_HEADING = (
        "xpath=//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'shortlist')] | "
        "//h3[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'shortlist')]"
    )

    # Preferred: role=listitem
    SHORTLIST_ROW_ROLE = "[role='listitem']"
    # Fallbacks: common list elements or divs with candidate/shortlist classes
    SHORTLIST_ROW_FALLBACK = "xpath=//li | xpath=//div[contains(@class,'shortlist') or contains(@class,'candidate') or contains(@class,'profile')]"
