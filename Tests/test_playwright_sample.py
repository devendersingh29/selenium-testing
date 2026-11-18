import pytest

pytestmark = [
    pytest.mark.playwright,
    pytest.mark.ui,
    pytest.mark.sample,
]


def test_example(page):
    """Simple pytest-playwright smoke test: open example.com and check title."""
    page.goto("https://example.com")
    assert "Example Domain" in page.title()
