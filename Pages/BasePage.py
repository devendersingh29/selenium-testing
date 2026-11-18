import re

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Common browser operations shared by all page objects."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def assert_label_visible(self, container: Locator, label: str) -> None:
        """Assert the exact label text is visible, ignoring optional trailing colon or asterisk."""
        variants = [
            label,
            f"{label} :",
            f"{label} *",
            f"{label} * :",
            f"{label}:",
        ]
        expr = " or ".join(f"normalize-space()='{value}'" for value in variants)
        expect(container.locator(f"xpath=.//*[{expr}]").first).to_be_visible()

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.locator(selector).fill(value)

    def click_when_visible(self, element: Locator) -> None:
        """Wait for an element to be visible, then click it."""
        expect(element).to_be_visible()
        element.click()

    def fill_and_verify(self, field: Locator, value: str) -> None:
        """Fill an input and verify that the browser retained its value."""
        expect(field).to_be_visible()
        field.fill(value)
        expect(field).to_have_value(value)

    def open_sidebar_page(self, link: Locator, route: str) -> None:
        """Open a sidebar destination and verify its hash route."""
        expect(link).to_be_visible()
        link.scroll_into_view_if_needed()
        link.click()
        expect(self.page).to_have_url(re.compile(rf".*/#/{re.escape(route)}$"))

    def select_option_by_label(self, dropdown: Locator, label: str) -> None:
        """Select and verify an option in a native HTML select control."""
        if not label.strip():
            raise ValueError("Option label cannot be empty")
        expect(dropdown).to_be_visible()
        dropdown.select_option(label=label)
        expect(dropdown.locator("option:checked")).to_have_text(label)

    def maximize_window(self) -> None:
        """Maximize the Chromium browser window containing this page."""
        cdp_session = self.page.context.new_cdp_session(self.page)
        window_id = cdp_session.send("Browser.getWindowForTarget")["windowId"]
        cdp_session.send(
            "Browser.setWindowBounds",
            {"windowId": window_id, "bounds": {"windowState": "maximized"}},
        )
