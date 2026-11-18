import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from Config.config import Config
from Pages.WelcomePage import WelcomePage
from Pages.admin_signin import AdminSignin


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    browser_type = getattr(playwright_instance, Config.BROWSER)
    launch_options = {"headless": Config.HEADLESS}
    if Config.BROWSER == "chromium" and Config.BROWSER_CHANNEL:
        launch_options["channel"] = Config.BROWSER_CHANNEL
    browser = browser_type.launch(**launch_options)
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(Config.TIMEOUT)
    yield page
    context.close()


@pytest.fixture
def admin_page(page: Page) -> Page:
    """Return a page signed in with the configured administrator account."""
    WelcomePage(page).open_organization_signin()
    admin_signin = AdminSignin(page)
    admin_signin.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
    admin_signin.maximize_window()
    return page


def pytest_report_header(config):
    return f"Target application: {Config.BASE_URL}"


def pytest_configure(config):
    from pytest_metadata.plugin import metadata_key

    metadata = config.stash.get(metadata_key, None)
    if metadata is not None:
        metadata["Target URL"] = Config.BASE_URL
