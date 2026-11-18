import time

import pytest
from playwright.sync_api import Page

from Pages.Pages_Panel_Search import PagesPanelSearch

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.panel,
    pytest.mark.search,
    pytest.mark.read_only,
]


def test_search_panel_filters_results(admin_page: Page) -> None:
    panel_search_page = PagesPanelSearch(admin_page)
    panel_search_page.open()

    keyword = "Auto"
    expected_name = "Auto Panel"
    hidden_names = ["Second Panel", "Frist Panel"]

    panel_search_page.search(keyword)
    panel_search_page.verify_search_result(expected_name=expected_name, hidden_names=hidden_names)


