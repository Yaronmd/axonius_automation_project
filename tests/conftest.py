import pytest
from playwright.sync_api import sync_playwright

from pages.main_page import MainPage
from pages.place_page import PlacePage
from pages.reserve_page import ReservePage



@pytest.fixture(scope="session", params=["chromium"])
def browser(request):
    browser_type = request.param
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_type).launch(headless=True, args=["--ignore-certificate-errors","--window-size=1920,1040"])
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="CustomUserAgent/1.0"
    )
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def navigate_to_airbnb_page(main_page:MainPage):
    main_page.navigate_to_airbnb()

@pytest.fixture
def main_page(page):
    return MainPage(page=page)

@pytest.fixture
def place_page(page):
    return PlacePage(page=page)

@pytest.fixture
def reserve_page(page):
    return ReservePage(page=page)