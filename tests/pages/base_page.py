"""Base Page Object Model with common methods"""
from playwright.sync_api import Page, Locator
from typing import Optional


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url
    
    def navigate(self, path: str = ""):
        """Navigate to a specific path"""
        url = f"{self.base_url}{path}"
        self.page.goto(url)
        return self
    
    def wait_for_element(self, selector: str, timeout: int = 5000) -> Locator:
        """Wait for an element to be visible"""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator
    
    def click(self, selector: str):
        """Click on an element"""
        self.page.click(selector)
        return self
    
    def fill(self, selector: str, text: str):
        """Fill an input field"""
        self.page.fill(selector, text)
        return self
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        return self.page.inner_text(selector)
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.is_visible(selector)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def wait_for_navigation(self):
        """Wait for navigation to complete"""
        self.page.wait_for_load_state("networkidle")
        return self
    
    def take_screenshot(self, name: str):
        """Take a screenshot"""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")
        return self
    
    def reload(self):
        """Reload the page"""
        self.page.reload()
        return self
