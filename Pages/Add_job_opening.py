
from datetime import date, timedelta
from pathlib import Path

# from isort.wrap_modes import hanging_indent
# from pip._internal import self_outdated_check
import re

from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError, expect

from Locators.Locator_add_job_opening import AddJobOpeningLocators
from Locators.Locator_Draft_JobOpening import (
    JO_SIDE_MENU,
    DRAFT_JOB_ID,
    CLICK_3DOTS,
    CLICK_EDIT_OPENING,
    CLICK_CONTINUE_BUTTON,
    CLICK_SAVE_AS_DRAFT,
    CLICK_DRAFT,
)
from Pages.BasePage import BasePage


class AddJobOpening(BasePage):
    """Actions and elements exposed by the add job opening page."""

    @property
    def job_opening_side_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Job_opening_side_button)

    def click_job_opening_side_button(self) -> None:
        self.open_sidebar_page(
            self.job_opening_side_button,
            "dashboard/jobopening",
        )

    @property
    def job_opening_cards(self) -> Locator:
        return self.locator(AddJobOpeningLocators.JOB_OPENING_CARD)

    @property
    def list_view_button(self) -> Locator:
        return self.page.get_by_role("button", name="List view", exact=True)

    @property
    def grid_view_button(self) -> Locator:
        return self.page.get_by_role("button", name="Grid view", exact=True)

    @property
    def job_opening_list_table(self) -> Locator:
        return self.page.get_by_role("table")

    def open_list_view(self) -> None:
        """Open List View and verify its selected state and table container."""
        expect(self.list_view_button).to_be_visible()
        if self.list_view_button.get_attribute("aria-pressed") != "true":
            self.list_view_button.click()

        expect(self.list_view_button).to_have_attribute("aria-pressed", "true")
        expect(self.job_opening_list_table).to_be_visible()

    def open_grid_view(self) -> None:
        """Open Grid View and verify its selected state before card interaction."""
        expect(self.grid_view_button).to_be_visible()
        if self.grid_view_button.get_attribute("aria-pressed") != "true":
            self.grid_view_button.click()

        expect(self.grid_view_button).to_have_attribute("aria-pressed", "true")
        expect(self.job_opening_cards.first).to_be_visible()

    def _navigate_to_workflow_stage(
        self,
        stage_name: str,
        expected_url: re.Pattern[str],
        expected_heading: str,
    ) -> None:
        """Open the first available workflow-stage action in List View.

        A Job Opening can have multiple rows with the same workflow stage. The
        first visible stage button is used because this scenario verifies the
        stage navigation itself and does not require a specific job opening.
        """
        self.open_list_view()
        stage_button = self.job_opening_list_table.get_by_role(
            "button",
            name=stage_name,
            exact=True,
        ).first
        expect(stage_button).to_be_visible()
        stage_button.click()

        expect(self.page).to_have_url(expected_url)
        expect(self.page.get_by_role("heading", name=expected_heading)).to_be_visible()

    def navigate_to_cbt_workflow(self) -> None:
        """Navigate from a List View CBT stage to the CBT scheduling screen."""
        self._navigate_to_workflow_stage(
            "CBT",
            re.compile(
                r".*/#/dashboard/jobopening/schedule-interview\\?.*[?&]stage=cbt"
            ),
            "Schedule events",
        )

    def navigate_to_panel_workflow(self) -> None:
        """Navigate from a List View Panel stage to Panel scheduling."""
        self._navigate_to_workflow_stage(
            "Panel",
            re.compile(
                r".*/#/dashboard/jobopening/schedule-interview\\?.*[?&]stage=panel"
            ),
            "Schedule events",
        )

    def verify_card_does_not_flicker_on_edge_hover(self) -> None:
        """Hover the first Job Opening card at its left edge and verify stability.

        The check is based on DOM-backed evidence rather than a successful hover:
        the same card must remain connected, visible, opaque, and geometrically
        stable across consecutive browser animation frames.
        """
        card = self.job_opening_cards.first
        expect(card).to_be_visible()

        card_box = card.bounding_box()
        if card_box is None:
            raise AssertionError("Could not determine the Job Opening card bounds.")

        card.hover(position={"x": 1, "y": card_box["height"] / 2})

        stability = card.evaluate(
            """async element => {
                const readState = () => {
                    const rect = element.getBoundingClientRect();
                    const style = window.getComputedStyle(element);
                    return {
                        connected: element.isConnected,
                        displayed: style.display !== "none",
                        visible: style.visibility !== "hidden",
                        opaque: Number(style.opacity) > 0,
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height,
                    };
                };

                const states = [readState()];
                for (let frame = 0; frame < 2; frame += 1) {
                    await new Promise(window.requestAnimationFrame);
                    states.push(readState());
                }
                return states;
            }"""
        )

        initial_state = stability[0]
        for state in stability:
            if not all(
                (
                    state["connected"],
                    state["displayed"],
                    state["visible"],
                    state["opaque"],
                )
            ):
                raise AssertionError(
                    "Job Opening card was detached or hidden while hovered at its edge."
                )
            if any(
                state[key] != initial_state[key]
                for key in ("x", "y", "width", "height")
            ):
                raise AssertionError(
                    "Job Opening card geometry changed while hovered at its edge."
                )


    @property
    def full_setup_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Full_setup_button)

    def click_full_setup(self) -> None:
        self.click_when_visible(self.full_setup_button)


#job opening form
    @property
    def upload_jd_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Click_Upload_JD)

    @property
    def browse_file_input(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Click_Browser_File_Text)

    @property
    def generate_from_jd_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Generate_From_JD_Button)

    @property
    def back_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Back_Button)

    @property
    def save_as_draft_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Save_As_Draft_Button)

    def upload_jd(self, file_name: str | None = None) -> None:
        """Upload a job-description file stored in the project Resources folder."""
        resources_dir = Path(__file__).resolve().parent.parent / "Resources"

        if file_name is None:
            supported_files = [
                path
                for path in resources_dir.iterdir()
                if path.is_file() and path.suffix.lower() in {".pdf", ".doc", ".docx"}
            ]
            if len(supported_files) != 1:
                raise FileNotFoundError(
                    "Expected exactly one PDF, DOC, or DOCX file in "
                    f"{resources_dir}, but found {len(supported_files)}."
                )
            file_path = supported_files[0]
        else:
            file_path = resources_dir / file_name

        if not file_path.is_file():
            raise FileNotFoundError(f"Upload file not found: {file_path}")

        self.upload_jd_button.click()
        self.browse_file_input.set_input_files(file_path)
        self.generate_from_jd_button.click()
        upload_dialog_title = self.page.get_by_text(
            "Upload Job Description",
            exact=True,
        )
        try:
            upload_dialog_title.wait_for(state="hidden", timeout=30_000)
        except PlaywrightTimeoutError:
            self.page.keyboard.press("Escape")
            upload_dialog_title.wait_for(state="hidden", timeout=5_000)



    @property
    def job_title_add_icon(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Click_job_title_plus_icon)

    @property
    def job_title_input(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_job_title)

    def select_or_create_job_title(self, title: str) -> None:
        """Select an existing job title or create it when it is new."""
        self.job_title_input.fill(title)
        existing_option = self.page.get_by_role("option").filter(
            has_text=title
        ).first
        try:
            existing_option.click(timeout=3_000)
        except PlaywrightTimeoutError:
            self.job_title_add_icon.click()



#add department
    @property
    def Add_Department(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Department)

    def click_add_department(self) -> None:
        self._select_autocomplete(self.Add_Department, "Engineering")


    @property
    def Add_Seniority_level(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Seniority_level)

    def click_add_seniority_level(self) -> None:
        self.Add_Seniority_level.click()
        self.page.get_by_role("option", name="Mid-Level", exact=True).click()

    @property
    def Add_Experience_Max(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Experience_Max)

    def click_add_experience_max(self) -> None:
        self.Add_Experience_Max.fill("5")

    @property
    def Add_Salary_Min(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Salary_Min)

    def click_add_salary_min(self) -> None:
        self.Add_Salary_Min.fill("50000")

    @property
    def Add_Salary_Max(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Salary_Max)

    def click_add_salary_max(self) -> None:
        self.Add_Salary_Max.fill("100000")

    @property
    def Add_Key_responsibilities(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Key_responsibilities)

    def click_add_key_responsibilities(self) -> None:
        self.Add_Key_responsibilities.fill("This is a sample key responsibility.")

    @property
    def add_job_opening_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_job_opening_button)

    def click_add_job_opening(self) -> None:
        self.click_when_visible(self.add_job_opening_button)

    @property
    def continue_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Continue_button)

    def click_continue(self) -> None:
        self.click_when_visible(self.continue_button)

    def validate_job_opening_screen_visible(self) -> None:
        expect(self.page.locator("h1")).to_contain_text("New Job Opening")

    def validate_job_opening_screen_buttons(self) -> None:
        expect(self.upload_jd_button).to_be_visible()
        expect(self.back_button).to_be_visible()
        expect(self.save_as_draft_button).to_be_visible()
        expect(self.continue_button).to_be_visible()
        expect(self.generate_button).to_be_visible()

    def validate_job_opening_screen_fields(self) -> None:
        expect(self.job_title_input).to_be_visible()
        expect(self.Add_Education).to_be_visible()
        expect(self.Add_Department).to_be_visible()
        expect(self.Add_Industry).to_be_visible()
        expect(self.Add_Seniority_level).to_be_visible()
        expect(self.Add_Experience_Min).to_be_visible()
        expect(self.Add_Experience_Max).to_be_visible()
        expect(self.Add_Salary_Min).to_be_visible()
        expect(self.Add_Salary_Max).to_be_visible()
        expect(self.Add_Job_Content).to_be_visible()
        expect(self.Add_Key_responsibilities).to_be_visible()
        expect(self.Add_skills).to_be_visible()
        expect(self.Add_location).to_be_visible()
        expect(self.page.locator(AddJobOpeningLocators.Work_Mode_Onsite)).to_be_visible()
        expect(self.page.locator(AddJobOpeningLocators.Employment_Type_Full_Time)).to_be_visible()
        expect(self.page.locator(AddJobOpeningLocators.Number_Of_Openings)).to_be_visible()

    def validate_job_opening_screen_labels(self) -> None:
        labels = [
            "Job title",
            "Education",
            "Department",
            "Industry / domain",
            "Seniority level",
            "Experience (years)",
            "Salary (LPA)",
            "Job Content",
            "Key responsibilities",
            "Skills",
            "Logistics",
            "Work mode",
            "Total openings",
            "Employment type",
        ]
        for lbl in labels:
            self.assert_label_visible(self.page, lbl)

    def validate_job_opening_screen(self) -> None:
        """Backward-compatible combined validation for the main Job Opening form."""
        self.validate_job_opening_screen_visible()
        self.validate_job_opening_screen_buttons()
        self.validate_job_opening_screen_fields()
        self.validate_job_opening_screen_labels()

    def validate_job_opening_workflow_screen_visible(self) -> None:
        self.assert_label_visible(self.page, "Team Lead")
        self.assert_label_visible(self.page, "RECRUITERS (optional)")
        expect(self.Add_BU).to_be_visible()
        expect(self.target_closure_date).to_be_visible()

    def validate_job_opening_workflow_screen_labels(self) -> None:
        self.assert_label_visible(self.page, "PRIORITY LEVEL")
        self.assert_label_visible(self.page, "Classification")
        self.assert_label_visible(self.page, "Workflow Stages")
        self.assert_label_visible(self.page, "Screening Questions")
        for lbl in ["VENDOR (optional)", "CLIENTS (optional)", "BU (optional)"]:
            self.assert_label_visible(self.page, lbl)

    def validate_job_opening_workflow_screen(self) -> None:
        """Backward-compatible combined validation for workflow step."""
        self.validate_job_opening_workflow_screen_visible()
        self.validate_job_opening_workflow_screen_labels()
    @property
    def Add_Education(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Education)

    def click_add_education(self) -> None:
        self.Add_Education.fill("B.Tech")

    @property
    def Add_Industry(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Industry)

    def click_add_industry(self) -> None:
        self._select_autocomplete(self.Add_Industry, "Information Technology")


    def _select_autocomplete(self, field: Locator, value: str) -> None:
        """Choose a value from a Material UI autocomplete control."""
        field.fill(value)
        matching_option = self.page.get_by_role("option", name=value, exact=True)
        try:
            matching_option.click(timeout=1_500)
        except PlaywrightTimeoutError:
            field.press("Enter")

    @property
    def Add_Experience_Min(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Experience_Min)

    def click_add_experience_min(self) -> None:
        self.Add_Experience_Min.fill("2")

    @property
    def Add_Job_Content(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Job_Content)

    def click_add_job_content(self) -> None:
        self.Add_Job_Content.fill("This is a sample job opening content.")

    @property
    def Add_skills(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Skills)

    def click_add_skills(self)  -> None:
        self.Add_skills.fill("Python")
        self.Add_skills.press("Enter")

    @property
    def Add_location(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_location)

    def click_add_location(self) -> None:
        for location in ("Bengaluru", "Noida"):
            self.Add_location.fill(location)

            listbox = self.page.get_by_role("listbox")
            listbox.wait_for(state="visible")
            listbox.get_by_role("option").filter(has_text=location).first.click()

    def complete_required_job_details(self) -> None:
        """Complete the required work-mode, employment-type, and openings fields."""
        self.click(AddJobOpeningLocators.Work_Mode_Onsite)
        self.click(AddJobOpeningLocators.Employment_Type_Full_Time)
        self.fill(AddJobOpeningLocators.Number_Of_Openings, "5")

    def read_number_of_openings_input(self) -> int:
        """Read and return the integer value from the Number of Openings input."""
        inp = self.locator(AddJobOpeningLocators.Number_Of_Openings)
        expect(inp).to_be_visible()
        # Use evaluate to read value attribute from the input
        val = inp.evaluate("el => el.value")
        try:
            return int(val)
        except Exception:
            raise AssertionError(f"Could not parse Number of Openings input value: '{val}'")

    def read_counter_openings_for_job(self, title: str) -> int:
        """Find the job card by title and read its openings counter."""
        # Locate the job card with the given title
        job_card = self.page.locator(f"article:has-text(\"{title}\")").first
        expect(job_card).to_be_visible()
        # Find the openings pill inside the card
        counter = job_card.locator("xpath=.//span[contains(@class,'jo-card-new__openings-pill')]").first
        expect(counter).to_be_visible()
        text = (counter.text_content() or "").strip()
        # Extract digits
        import re
        m = re.search(r"(\d+)", text)
        if not m:
            raise AssertionError(f"Could not parse openings counter from card text: '{text}'")
        return int(m.group(1))

    def verify_openings_counter_matches_input(self, title: str = "Auto_QA engineer") -> None:
        """Backward-compatible wrapper that reads input and verifies post-creation."""
        expected = self.read_number_of_openings_input()
        return self.verify_openings_counter_matches_expected(expected, title)

    def verify_openings_counter_matches_expected(self, expected: int, title: str = "Auto_QA engineer") -> None:
        """Verify that the job card openings counter matches the provided expected value."""
        # After creating, search and read counter
        self.Search_Job_opening(title)
        actual = self.read_counter_openings_for_job(title)
        if expected != actual:
            raise AssertionError(f"Number of openings mismatch: expected={expected}, card_counter={actual}")
        print(f"Number of openings verified for '{title}': {expected}")

    @property
    def Add_TeamLead(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_TeamLead)

    def select_team_lead(self) -> None:
        """Open the Team Lead dropdown and select its first available option."""
        self._select_first_dropdown_option(self.Add_TeamLead.locator(".."), "Team Lead")


    @property
    def Add_Recruiter(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_Recruiter)

    def select_recruiter(self) -> None:
        """Open the Recruiter dropdown and select its first available option."""
        self._select_first_dropdown_option(self.Add_Recruiter.locator(".."), "Recruiter")

    def _select_first_dropdown_option(self, trigger: Locator, field_name: str) -> None:
        """Open a dropdown and select its first option after asynchronous loading."""
        first_option = self.page.locator("[role='option']:visible").first

        for attempt in range(3):
            trigger.click()
            try:
                first_option.click(timeout=5_000)
                self.page.keyboard.press("Escape")
                self.page.locator("div.MuiPopover-root:visible").wait_for(
                    state="hidden",
                    timeout=5_000,
                )
                return
            except PlaywrightTimeoutError:
                self.page.keyboard.press("Escape")
                if attempt < 2:
                    self.page.wait_for_timeout(1_000)

        raise AssertionError(f"No options were loaded in the {field_name} dropdown.")


    @property
    def Add_BU(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Add_BU)

    def select_business_unit_head(self) -> None:
        self._select_autocomplete(self.Add_BU, "Suman")

    #add closure date

    @property
    def target_closure_date(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Target_Closure_Date)

    def set_target_closure_date(self, days_from_today: int = 10) -> None:
        """Set the native HTML date input to a future calendar date.

        HTML ``input[type=date]`` controls accept ISO dates regardless of the
        localized format displayed by the browser.
        """
        if days_from_today < 0:
            raise ValueError("Closure date cannot be in the past.")

        target_date = date.today() + timedelta(days=days_from_today)
        self.target_closure_date.fill(target_date.isoformat())

    @property
    def select_urgent(self):
        return self.page.locator(AddJobOpeningLocators.Select_Urgent)

    def click_select_urgent(self) -> None:
        self.select_urgent.click()

#add workflow stages
    @property
    def workflow_technical_round_button(self):
        return self.page.locator(AddJobOpeningLocators.Select_Technical_round)
    def select_workflow_technical_round(self) -> None:
        self.workflow_technical_round_button.click()

    @property
    def workflow_hr_round_button(self):
        return self.page.locator(AddJobOpeningLocators.Select_HR_Round)
    def select_workflow_hr_round(self) -> None:
        self.workflow_hr_round_button.click()

    @property
    def workflow_managerial_round_button(self):
        return self.page.locator(AddJobOpeningLocators.Select_Managerial_Round)
    def select_workflow_managerial_round(self) -> None:
        self.workflow_managerial_round_button.click()

    @property
    def generate_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Click_AIGenerate_Button)

    def click_generate_button_JO(self) -> None:
        self.generate_button.click()

    @property
    def submit_job_opening_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Click_Add_Job_Opening_Button_f)

    def click_submit_job_opening(self) -> None:
        self.submit_job_opening_button.click()


    #search the JO for the verification after it's creation
    @property
    def Search_JO(self):
        return self.locator(AddJobOpeningLocators.Search_JobOpening)

    def Search_Job_opening(self, title: str = "Auto_QA engineer"):
        """Search for a job opening by title (default used by tests)."""
        self.Search_JO.fill(title)
        expect(self.page.locator("body")).to_contain_text(title)

    def search_and_verify(self, title: str = "Auto_QA engineer") -> None:
        """Enter the title in search box and verify a matching job card appears.

        Uses a job-card scoped assertion to avoid strict-mode collisions.
        """
        # Fill the search textbox
        self.Search_JO.fill(title)
        # Wait for the result list to update and contain the title
        expect(self.page.locator("body")).to_contain_text(title)

        # Locate the first job card that contains the title and assert its heading
        job_card = self.page.locator(f"article:has-text(\"{title}\")").first
        expect(job_card).to_be_visible()
        # The job title appears as a heading (h3) inside the card
        heading = job_card.locator("h3").first
        expect(heading).to_have_text(title)

    @property
    def Active_status(self) -> Locator:
        """Locator for the ACTIVE status badge on a job card (general use)."""
        return self.locator(AddJobOpeningLocators.Active_status)

    def verify_active_status(self, title: str = "Auto_QA engineer") -> None:
        """Verify a newly created job opening with `title` is marked ACTIVE in the UI.

        This locates the job card containing the given title and asserts its
        status badge shows ACTIVE. Using a job-card-scoped locator avoids
        strict-mode collisions when many ACTIVE badges exist on the page.
        """
        # Locate the job card that includes the job title and check its status
        job_card = self.page.locator(f"article:has-text(\"{title}\")").first
        status_locator = job_card.locator("span.jo-card-new__status.jo-card-new__status--active")
        expect(status_locator).to_be_visible()
        expect(status_locator).to_have_text(re.compile(r"^Active$", re.I))
        print("This is Executed")

    # Verify the ACTIVE status on the newly created Job opening
    @property
    def active_tab(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Active_tab)

    @property
    def inactive_tab(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Inactive_tab)

    @property
    def jo_id(self) -> Locator:
        return self.locator(AddJobOpeningLocators.JO_id)

    @property
    def jo_checkbox(self) -> Locator:
        return self.locator(AddJobOpeningLocators.JO_checkbox)

    @property
    def inactive_button(self) -> Locator:
        return self.locator(AddJobOpeningLocators.INACTIVE_BUTTON)

    @property
    def inactive_success_message(self) -> Locator:
        return self.locator(AddJobOpeningLocators.Inactive_Success_Message)

    def make_job_inactive(self, title: str = "Auto_QA engineer") -> str:
        """Set the first job card matching title to Inactive and return its job-id."""
        self.active_tab.click()
        expect(self.active_tab).to_be_visible()
        expect(self.page.locator(f"article:has-text(\"{title}\")").first).to_be_visible()

        job_card = self.page.locator(f"article:has-text(\"{title}\")").first
        saved_job_id = job_card.locator("p.jo-card-new__job-id").text_content().strip()
        if not saved_job_id:
            raise AssertionError(f"No job-id found for job title: {title}")

        job_card.locator("input[type='checkbox']").check()
        self.inactive_button.click()

        expect(self.page.get_by_text("Job openings updated successfully", exact=False)).to_be_visible()
        return saved_job_id

    def verify_job_inactive_in_list(self, job_id: str) -> None:
        """Verify the saved job-id appears on the Inactive screen."""
        self.inactive_tab.click()
        expect(self.page.locator("body")).to_contain_text(job_id)
        print("Inactive job opening verified")

    # Verify the ACTIVE status on the newly created Job opening

    # Draft flow helpers
    def open_job_openings_from_sidebar(self) -> None:
        """Open Job Openings from the sidebar (for tests that start at dashboard)."""
        expect(self.locator(AddJobOpeningLocators.Job_opening_side_button)).to_be_visible()
        self.locator(AddJobOpeningLocators.Job_opening_side_button).click()
        expect(self.page.locator("h1")).to_contain_text("Job Openings")

    def make_job_draft(self, title: str = "Auto_QA engineer") -> str:
        """Find the job by title, open its menu, choose Edit Opening, continue and save as Draft.

        Returns the saved job-id string.
        """
        # Ensure we're on the job openings list
        self.open_job_openings_from_sidebar()

        job_card = self.page.locator(f"article:has-text(\"{title}\")").first
        expect(job_card).to_be_visible()

        # Read the job id
        job_id_elem = job_card.locator("p.jo-card-new__job-id")
        saved_job_id = job_id_elem.text_content().strip()
        if not saved_job_id:
            raise AssertionError("Could not read job id from the job card")

        # Click the three-dots / More button inside the job card
        more_btn = job_card.locator("button[aria-label='More']")
        expect(more_btn).to_be_visible()
        more_btn.click()

        # Click Edit Opening (menu option)
        self.page.get_by_text("Edit Opening", exact=True).click()

        # Continue through the edit wizard and save as draft
        continue_btn = self.locator(CLICK_CONTINUE_BUTTON)
        expect(continue_btn).to_be_visible()
        continue_btn.click()

        save_draft_btn = self.locator(CLICK_SAVE_AS_DRAFT)
        expect(save_draft_btn).to_be_visible()
        save_draft_btn.click()

        # Allow the app a moment to process and update the list
        self.page.wait_for_timeout(1_000)

        return saved_job_id

    def verify_job_in_draft(self, job_id: str) -> None:
        """Open Draft tab and assert job_id is listed."""
        draft_tab = self.locator(CLICK_DRAFT)
        expect(draft_tab).to_be_visible()
        draft_tab.click()

        # Search body for the job id text
        expect(self.page.locator("body")).to_contain_text(job_id)

    # end of Draft helpers
