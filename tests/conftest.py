import pytest
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="session")
def browser():
    """Session-level browser fixture using Playwright chromium"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=os.getenv("HEADLESS", "true").lower() == "true")
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Function-level page fixture with viewport 1920x1080"""
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """Fixture that returns a page already logged in"""
    from pages.login_page import LoginPage
    
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("admin", "admin123")
    return page
