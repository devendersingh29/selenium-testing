

import os


class Config:
    BASE_URL = os.getenv("SMARTRECRUIT_BASE_URL") or "https://qa.thesmartrecruit.ai/#/session/welcome"
    BROWSER = "chromium"
    BROWSER_CHANNEL = os.getenv("PLAYWRIGHT_CHANNEL", "chrome")
    HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() not in {
        "0",
        "false",
        "no",
    }
    TIMEOUT = 30000
    ADMIN_EMAIL = os.getenv("SMARTRECRUIT_ADMIN_EMAIL", "")
    ADMIN_PASSWORD = os.getenv("SMARTRECRUIT_ADMIN_PASSWORD", "")
