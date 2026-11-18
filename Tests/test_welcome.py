from playwright.sync_api import Page, expect

import pytest

from Pages.WelcomePage import WelcomePage

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.welcome,
    pytest.mark.smoke,
    pytest.mark.read_only,
]


def test_welcome_page_displays_get_started(page: Page) -> None:
    welcome_page = WelcomePage(page).open()

    expect(page).to_have_title("SmartRecruit")
    expect(welcome_page.get_started_button).to_be_visible()
