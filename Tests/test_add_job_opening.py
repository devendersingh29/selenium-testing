from collections.abc import Callable

import pytest
from playwright.sync_api import Page

from Pages.Add_job_opening import AddJobOpening

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.job_opening,
]


def _open_job_opening_form(admin_page: Page) -> AddJobOpening:
    add_job_opening = AddJobOpening(admin_page)
    add_job_opening.click_job_opening_side_button()
    add_job_opening.click_add_job_opening()
    add_job_opening.click_full_setup()
    add_job_opening.click_continue()
    return add_job_opening


@pytest.mark.form
@pytest.mark.read_only
def test_job_opening_screen_visible(admin_page: Page) -> None:
    add_job_opening = _open_job_opening_form(admin_page)
    add_job_opening.validate_job_opening_screen_visible()


@pytest.mark.form
@pytest.mark.read_only
def test_job_opening_screen_buttons(admin_page: Page) -> None:
    add_job_opening = _open_job_opening_form(admin_page)
    add_job_opening.validate_job_opening_screen_buttons()


@pytest.mark.form
@pytest.mark.read_only
def test_job_opening_screen_fields(admin_page: Page) -> None:
    add_job_opening = _open_job_opening_form(admin_page)
    add_job_opening.validate_job_opening_screen_fields()


@pytest.mark.form
@pytest.mark.read_only
def test_job_opening_screen_labels(admin_page: Page) -> None:
    add_job_opening = _open_job_opening_form(admin_page)
    add_job_opening.validate_job_opening_screen_labels()


@pytest.mark.read_only
def test_job_opening_card_does_not_flicker_on_edge_hover(admin_page: Page) -> None:
    """Verify a Job Opening card remains stable when its edge is hovered."""
    add_job_opening = AddJobOpening(admin_page)
    add_job_opening.click_job_opening_side_button()
    add_job_opening.open_grid_view()

    add_job_opening.verify_card_does_not_flicker_on_edge_hover()
    print("Card is not flickering")


@pytest.mark.read_only
@pytest.mark.view_toggle
@pytest.mark.parametrize(
    "navigate_to_stage",
    [
        AddJobOpening.navigate_to_cbt_workflow,
        AddJobOpening.navigate_to_panel_workflow,
    ],
    ids=["cbt", "panel"],
)
def test_hiring_workflow_stage_navigates_from_list_view(
    admin_page: Page,
    navigate_to_stage: Callable[[AddJobOpening], None],
) -> None:
    """Verify each available List View workflow stage opens its schedule."""
    add_job_opening = AddJobOpening(admin_page)
    add_job_opening.click_job_opening_side_button()

    navigate_to_stage(add_job_opening)


@pytest.mark.create
@pytest.mark.data_mutation
@pytest.mark.e2e
def test_add_job_opening(admin_page: Page) -> None:
    add_job_opening = _open_job_opening_form(admin_page)
    add_job_opening.validate_job_opening_screen()

    add_job_opening.upload_jd()
    add_job_opening.select_or_create_job_title("Auto_QA engineer")
    add_job_opening.click_add_education()
    add_job_opening.click_add_department()
    add_job_opening.click_add_industry()
    add_job_opening.click_add_seniority_level()
    add_job_opening.click_add_experience_min()
    add_job_opening.click_add_experience_max()
    add_job_opening.click_add_salary_min()
    add_job_opening.click_add_salary_max()
    add_job_opening.click_add_job_content()
    add_job_opening.click_add_key_responsibilities()
    add_job_opening.click_add_skills()
    add_job_opening.click_add_location()
    add_job_opening.complete_required_job_details()
    # capture the number-of-openings value before leaving the form
    expected_openings = add_job_opening.read_number_of_openings_input()
    add_job_opening.click_continue()

    add_job_opening.validate_job_opening_workflow_screen()

    add_job_opening.select_team_lead()
    add_job_opening.select_recruiter()
    add_job_opening.select_business_unit_head()
    add_job_opening.set_target_closure_date()
    add_job_opening.click_select_urgent()
    add_job_opening.select_workflow_technical_round()
    add_job_opening.select_workflow_hr_round()
    add_job_opening.select_workflow_managerial_round()
    add_job_opening.click_submit_job_opening()

    # Search Job opening validation if "Auto_QA engineer" available on the screen or not
    add_job_opening.Search_Job_opening()

    # Verify the newly created job opening shows ACTIVE status
    add_job_opening.verify_active_status()

    # Verify the number-of-openings input value is reflected on the job card
    add_job_opening.verify_openings_counter_matches_expected(expected_openings, title="Auto_QA engineer")

    # Inactivate the same job opening and verify it appears on the Inactive tab
    job_id = add_job_opening.make_job_inactive()
    add_job_opening.verify_job_inactive_in_list(job_id)
