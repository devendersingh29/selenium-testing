class LocatorToggleJobOpening:
    """Locators used for toggling Job Openings between List and Grid views.

    These are intentionally simple and rely on stable visible button labels.
    """

    # Sidebar link to Job Openings (stable CSS used elsewhere in the project)
    JOB_OPENING_SIDE_BUTTON = "a[href='#/dashboard/jobopening']"

    # Buttons that toggle view modes. The UI displays exact labels 'List view' and
    # 'Grid view' in the header area — use normalize-space() to match reliably.
    LIST_VIEW_BUTTON = "//button[normalize-space()='List view']"
    GRID_VIEW_BUTTON = "//button[normalize-space()='Grid view']"

    # Generic job card selector (useful for verifying results are present)
    JOB_CARD = "article"
