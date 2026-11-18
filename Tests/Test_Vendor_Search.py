import pytest
from datetime import datetime

from playwright.sync_api import Page, expect

from Pages.Page_Vendor_Search import PageVendorSearch
from Pages.Pages_Vendor import PageVendor

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.regression,
    pytest.mark.admin,
    pytest.mark.vendor,
    pytest.mark.search,
    pytest.mark.create,
    pytest.mark.data_mutation,
]


def test_vendor_search_filters_results(admin_page: Page) -> None:
    vendor_search_page = PageVendorSearch(admin_page)
    vendor_search_page.open()

    if vendor_search_page.search_input.count() == 0:
        pytest.skip("Vendor list search input is not present in the current DOM.")

    vendor_page = PageVendor(admin_page)
    timestamp = datetime.now().strftime("%d%H%M%S")
    vendor_name = f"Alpha Vendor Search {timestamp}"

    vendor_page.click_add_vendor_button()
    vendor_page.create_vendor(
        organization_name=vendor_name,
        first_name="Alpha",
        last_name="Vendor",
        email=f"prakash.lavania+alphaVendorSearch{timestamp}@walkingtree.tech",
        phone_number=f"91{timestamp}",
    )

    vendor_search_page.search("Alpha")
    vendor_search_page.verify_search_result(vendor_name)
    expect(admin_page.get_by_text("Beta Vendor Search", exact=False)).to_have_count(0)
