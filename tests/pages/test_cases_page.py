"""Test Cases Page Object Model"""
from pages.base_page import BasePage


class TestCasesPage(BasePage):
    """Page object for test cases management page"""
    
    # Selectors
    CREATE_BUTTON = "[data-testid='create-testcase-button']"
    TEST_CASE_TABLE = "[data-testid='testcase-table']"
    TEST_CASE_ROWS = "[data-testid='testcase-row']"
    TITLE_INPUT = "[data-testid='testcase-title-input']"
    DESCRIPTION_INPUT = "[data-testid='testcase-description-input']"
    PRIORITY_SELECT = "[data-testid='testcase-priority-select']"
    STATUS_SELECT = "[data-testid='testcase-status-select']"
    SAVE_BUTTON = "[data-testid='save-testcase-button']"
    CANCEL_BUTTON = "[data-testid='cancel-button']"
    EDIT_BUTTON = "[data-testid='edit-button']"
    DELETE_BUTTON = "[data-testid='delete-button']"
    CONFIRM_DELETE_BUTTON = "[data-testid='confirm-delete-button']"
    SEARCH_INPUT = "[data-testid='search-input']"
    SEARCH_BUTTON = "[data-testid='search-button']"
    
    def navigate_to_test_cases(self):
        """Navigate to test cases page"""
        return self.navigate("/testcases")
    
    def click_create(self):
        """Click create new test case button"""
        self.click(self.CREATE_BUTTON)
        return self
    
    def enter_title(self, title: str):
        """Enter test case title"""
        self.fill(self.TITLE_INPUT, title)
        return self
    
    def enter_description(self, description: str):
        ""