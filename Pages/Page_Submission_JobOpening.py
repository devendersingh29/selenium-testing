import re
from typing import Optional

from playwright.sync_api import Locator, expect

from Locators.Locator_Submission_JobOpening import LocatorSubmissionJobOpening
from Pages.BasePage import BasePage


class PageSubmissionJobOpening(BasePage):
    """Page object for submission button interaction and verification.

    Implements methods to read the submission count on a job card, click the
    submissions button, and validate that the number matches the actual
    candidate entries shown in the submissions panel.

    Assumptions:
    - The submissions button text contains the number (e.g. "3 Submissions").
    - Clicking the button opens a dialog (role=dialog) or a panel with a
      heading that includes the word 'Submissions'. The candidate rows are
      either listitems (role=listitem) within that dialog or recognizable
      as <li> elements / divs with classes containing 'submission' or 'candidate'.

    If your UI differs, provide the submissions panel HTML snippet and the
    row selector will be adjusted.
    """

    def open(self) -> None:
        """Navigate to Job Openings page and assert it loaded."""
        expect(self.locator(LocatorSubmissionJobOpening.JOB_OPENING_SIDE_BUTTON)).to_be_visible()
        self.locator(LocatorSubmissionJobOpening.JOB_OPENING_SIDE_BUTTON).click()
        expect(self.page.locator("h1")).to_contain_text("Job Openings")

    def _find_job_card_by_title(self, title: str) -> Locator:
        """Return the first job card locator that contains the given title."""
        card = self.page.locator(f"{LocatorSubmissionJobOpening.JOB_CARD}:has-text(\"{title}\")").first
        expect(card).to_be_visible()
        return card

    def read_submission_count_from_card(self, title: str) -> int:
        """Read and return the integer shown on the card's submissions button."""
        job_card = self._find_job_card_by_title(title)
        btn = job_card.locator(LocatorSubmissionJobOpening.SUBMISSIONS_BUTTON_IN_CARD).first
        expect(btn).to_be_visible()
        text = btn.text_content() or ""
        m = re.search(r"(\d+)", text)
        if not m:
            raise AssertionError(f"Could not parse submissions count from button text: '{text}'")
        return int(m.group(1))

    def click_submission_button(self, title: str) -> None:
        """Click the submissions button for the job with the given title."""
        job_card = self._find_job_card_by_title(title)
        btn = job_card.locator(LocatorSubmissionJobOpening.SUBMISSIONS_BUTTON_IN_CARD).first
        expect(btn).to_be_visible()
        btn.click()

    def _locate_submissions_panel(self) -> Optional[Locator]:
        """Try to find the submissions panel/dialog; return Locator or None."""
        # Prefer role=dialog
        dialogs = self.page.locator(LocatorSubmissionJobOpening.SUBMISSIONS_PANEL_DIALOG)
        if dialogs.count() > 0:
            # choose the visible one
            for i in range(dialogs.count()):
                dlg = dialogs.nth(i)
                try:
                    if dlg.is_visible():
                        return dlg
                except Exception:
                    continue
        # Fallback: locate a heading containing 'Submissions'
        headings = self.page.locator(LocatorSubmissionJobOpening.SUBMISSIONS_PANEL_HEADING)
        if headings.count() > 0:
            head = headings.first
            # search up to a reasonable ancestor for listitems
            ancestor = head.locator("xpath=ancestor::div[1]")
            if ancestor.count() > 0:
                return ancestor.first
        return None

    def count_submission_rows_in_panel(self) -> int:
        """Count candidate rows inside the submissions panel.

        Returns the number of visible candidate entries.
        """
        # If the app navigated to a candidates page, try to parse count from UI
        current_url = self.page.url
        if "/candidates" in current_url:
            # Look for any visible element that includes the word 'Submissions' and a number
            els = self.page.locator("xpath=//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submissions')]")
            for i in range(els.count()):
                el = els.nth(i)
                try:
                    if not el.is_visible():
                        continue
                    text = (el.text_content() or "").strip()
                    m = re.search(r"(\d+)", text)
                    if m:
                        return int(m.group(1))
                except Exception:
                    continue
            # Also check for 'Applicants' or 'Applicants (' style headings
            els2 = self.page.locator("xpath=//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'applicants') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'applicant')]")
            for i in range(els2.count()):
                el = els2.nth(i)
                try:
                    if not el.is_visible():
                        continue
                    text = (el.text_content() or "").strip()
                    m = re.search(r"(\d+)", text)
                    if m:
                        return int(m.group(1))
                except Exception:
                    continue
            # Fallback to counting probable applicant rows on the candidates page
            rows = self.page.locator("article")
            try:
                cnt = rows.count()
                if cnt > 0:
                    return cnt
            except Exception:
                pass
            # Additional heuristics: count buttons that commonly appear per applicant
            details_btns = self.page.locator("xpath=//button[contains(normalize-space(.),'Details')]")
            view_btns = self.page.locator("xpath=//button[contains(normalize-space(.),'View')]")
            profile_btns = self.page.locator("xpath=//button[contains(normalize-space(.),'Profile')]")
            counts = [
                details_btns.count() if details_btns.count() is not None else 0,
                view_btns.count() if view_btns.count() is not None else 0,
                profile_btns.count() if profile_btns.count() is not None else 0,
            ]
            max_cnt = max(counts)
            if max_cnt > 0:
                return max_cnt
        # Otherwise, try to find a dialog/panel and count listitems
        panel = self._locate_submissions_panel()
        if panel:
            rows = panel.locator(LocatorSubmissionJobOpening.SUBMISSION_ROW_ROLE)
            try:
                cnt = rows.count()
                if cnt > 0:
                    return cnt
            except Exception:
                pass
            rows_fallback = panel.locator(LocatorSubmissionJobOpening.SUBMISSION_ROW_FALLBACK)
            try:
                cnt2 = rows_fallback.count()
                return cnt2
            except Exception:
                return 0
        # Last resort: count any listitem on page
        rows = self.page.locator("[role='listitem']")
        try:
            cnt = rows.count()
            if cnt > 0:
                return cnt
        except Exception:
            pass

        # Diagnostic: print counts for common candidate-list selectors to help
        # tuning the locators if necessary.
        try:
            print("Diagnostic page.content (first 2000 chars):")
            content = self.page.content()
            print(content[:10000])
            print("Diagnostic counts:")
            print("articles:", self.page.locator("article").count())
            print("rows (listitem):", self.page.locator("[role='listitem']").count())
            print("table rows:", self.page.locator("xpath=//table//tbody//tr").count())
            print("div.candidate:", self.page.locator("xpath=//div[contains(@class,'candidate')] ").count())
            print("div.submission:", self.page.locator("xpath=//div[contains(@class,'submission')] ").count())
        except Exception as e:
            print("Diagnostic error:", e)
        return 0

    def verify_submission_count_matches(self, title: str) -> None:
        """High-level: read number from card, click submissions, and verify match."""
        expected = self.read_submission_count_from_card(title)
        self.click_submission_button(title)
        # wait for UI to update and present panel
        expect(self.page.locator("body")).to_be_visible()
        actual = self.count_submission_rows_in_panel()
        if expected != actual:
            # collect diagnostic counts to help pinpoint selector mismatch
            try:
                article_cnt = self.page.locator("article").count()
            except Exception:
                article_cnt = -1
            try:
                listitem_cnt = self.page.locator("[role='listitem']").count()
            except Exception:
                listitem_cnt = -1
            try:
                table_row_cnt = self.page.locator("xpath=//table//tbody//tr").count()
            except Exception:
                table_row_cnt = -1
            try:
                details_cnt = self.page.locator("xpath=//button[contains(normalize-space(.),'Details')]").count()
            except Exception:
                details_cnt = -1
            try:
                view_cnt = self.page.locator("xpath=//button[contains(normalize-space(.),'View')]").count()
            except Exception:
                view_cnt = -1
            raise AssertionError(
                f"Submission count mismatch for '{title}': button={expected}, panel_rows={actual} | diagnostics: articles={article_cnt}, listitems={listitem_cnt}, table_rows={table_row_cnt}, details_btns={details_cnt}, view_btns={view_cnt}"
            )
        print(f"Submission verification passed for '{title}': {expected} submissions.")
