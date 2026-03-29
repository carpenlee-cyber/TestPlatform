import os
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="reports/videos" if os.getenv("RECORD_VIDEO") else None
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def base_url():
    """Return the base URL for the application"""
    return BASE_URL
