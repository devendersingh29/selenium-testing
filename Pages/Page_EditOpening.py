import time
from typing import Optional

from playwright.sync_api import Locator, expect

from Locators.Locator_EditOpening import LocatorEditOpening
from Pages.BasePage import BasePage


class PageEditOpening(BasePage):
    """Page object for editing a job opening.

    Methods follow project patterns: small, test-friendly actions and
    robust, Playwright-friendly assertions.
    """

    def open(self) -> None:
        """Navigate to Job Openings page and assert it loaded."""
        expect(self.locator(LocatorEditOpening.JOB_OPENING_SIDE_BUTTON)).to_be_visible()
        self.locator(LocatorEditOpening.JOB_OPENING_SIDE_BUTTON).click()
        expect(self.page.locator("h1")).to_contain_text("Job Openings")

    def _get_first_job_card(self) -> Locator:
        card = self.page.locator(LocatorEditOpening.JOB_CARD).first
        expect(card).to_be_visible()
        return card

    def click_more_on_first_job(self) -> None:
        card = self._get_first_job_card()
        more = card.locator(LocatorEditOpening.CLICK_3DOTS).first
        expect(more).to_be_visible()
        more.click()

    def click_edit_opening_in_menu(self) -> None:
        opt = self.page.locator(LocatorEditOpening.CLICK_EDIT_OPENING).first
        expect(opt).to_be_visible()
        opt.click()

    def set_job_content(self, content: str) -> None:
        """Set the Job Content in the rich-text editor (jodit).

        Uses element.evaluate to set innerHTML which is reliable for contenteditable.
        """
        editor = self.page.locator(LocatorEditOpening.JOB_CONTENT_EDITOR).first
        expect(editor).to_be_visible()
        # focus then set content
        editor.click()
        # Use evaluate on the element to set HTML/text
        editor.evaluate("(el, html) => { el.innerHTML = html; }", content)

    def click_continue(self) -> None:
        btn = self.page.locator(LocatorEditOpening.CONTINUE_BUTTON).first
        expect(btn).to_be_visible()
        btn.click()

    def click_update_opening(self) -> None:
        btn = self.page.locator(LocatorEditOpening.UPDATE_OPENING_BUTTON).first
        expect(btn).to_be_visible()
        btn.click()

    def expect_edit_success_message(self) -> None:
        # Prefer Playwright's get_by_text to locate the exact success string
        # Use exact=False to allow trailing punctuation like '!'
        msg = self.page.get_by_text("Edited Successfully", exact=False).first
        expect(msg).to_be_visible(timeout=10_000)

    def edit_first_job_content_and_save(self, new_content: str) -> None:
        """High-level helper: open menu -> edit opening -> set content -> continue -> update -> assert success."""
        self.open()
        self.click_more_on_first_job()
        self.click_edit_opening_in_menu()
        # editor appears inside modal/flow -- set content
        self.set_job_content(new_content)
        self.click_continue()
        self.click_update_opening()
        self.expect_edit_success_message()
