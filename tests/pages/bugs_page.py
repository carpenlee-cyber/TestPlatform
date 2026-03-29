"""Bugs Page Object Model"""
from pages.base_page import BasePage


class BugsPage(BasePage):
    """Page object for bugs management page"""
    
    # Selectors
    CREATE_BUTTON = "[data-testid='create-bug-button']"
    BUG_TABLE = "[data-testid='bug-table']"
    BUG_ROWS = "[data-testid='bug-row']"
    TITLE_INPUT = "[data-testid='bug-title-input']"
    DESCRIPTION_INPUT = "[data-testid='bug-description-input']"
    SEVERITY_SELECT = "[data-testid='bug-severity-select']"
    PRIORITY_SELECT = "[data-testid='bug-priority-select']"
    STATUS_SELECT = "[data-testid='bug-status-select']"
    ASSIGNEE_SELECT = "[data-testid='bug-assignee-select']"
    SAVE_BUTTON = "[data-testid='save-bug-button']"
    CANCEL_BUTTON = "[data-testid='cancel-button']"
    EDIT_BUTTON = "[data-testid='edit-button']"
    DELETE_BUTTON = "[data-testid='delete-button']"
    CONFIRM_DELETE_BUTTON = "[data-testid='confirm-delete-button']"
    SEARCH_INPUT = "[data-testid='search-input']"
    SEARCH_BUTTON = "[data-testid='search-button']"
    FILTER_STATUS = "[data-testid='filter-status']"
    FILTER_SEVERITY = "[data-testid='filter-severity']"
    
    def navigate_to_bugs(self):
        """Navigate to bugs page"""
        return self.navigate("/bugs")
    
    def click_create(self):
        """Click create new bug button"""
        self.click(self.CREATE_BUTTON)
        return self
    
    def enter_title(self, title: str):
        """Enter bug title"""
        self.fill(self.TITLE_INPUT, title)
        return self
    
    def enter_description(self, description: str):
        """Enter bug description"""
        self.fill(self.DESCRIPTION_INPUT, description)
        return self
    
    def select_severity(self, severity: str):
        """Select bug severity"""
        self.page.select_option(self.SEVERITY_SELECT, severity)
        return self
    
    def select_priority(self, priority: str):
        """Select bug priority"""
        self.page.select_option(self.PRIORITY_SELECT, priority)
        return self
    
    def select_status(self, status: str):
        """Select bug status"""
        self.page.select_option(self.STATUS_SELECT, status)
        return self
    
    def select_assignee(self, assignee: str):
        """Select bug assignee"""
        self.page.select_option(self.ASSIGNEE_SELECT, assignee)
        return self
    
    def click_save(self):
        """Click save button"""
        self.click(self.SAVE_BUTTON)
        return self
    
    def click_cancel(self):
        """Click cancel button"""
        self.click(self.CANCEL_BUTTON)
        return self
    
    def create_bug(self, title: str, description: str, severity: str = "medium", 
                   priority: str = "medium", status: str = "open"):
        """Create a complete bug"""
        self.click_create()
        self.enter_title(title)
        self.enter_description(description)
        self.select_severity(severity)
        self.select_priority(priority)
        self.select_status(status)
        self.click_save()
        return self
    
    def search_bug(self, keyword: str):
        """Search for a bug"""
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def get_bug_count(self) -> int:
        """Get number of bug rows"""
        return self.page.locator(self.BUG_ROWS).count()
    
    def click_edit_first(self):
        """Click edit on first bug"""
        self.page.locator(self.EDIT_BUTTON).first.click()
        return self
    
    def click_delete_first(self):
        """Click delete on first bug"""
        self.page.locator(self.DELETE_BUTTON).first.click()
        return self
    
    def confirm_delete(self):
        """Confirm deletion"""
        self.click(self.CONFIRM_DELETE_BUTTON)
        return self
    
    def delete_first_bug(self):
        """Delete the first bug"""
        self.click_delete_first()
        self.confirm_delete()
        return self
    
    def filter_by_status(self, status: str):
        """Filter bugs by status"""
        self.page.select_option(self.FILTER_STATUS, status)
        return self
    
    def filter_by_severity(self, severity: str):
        """Filter bugs by severity"""
        self.page.select_option(self.FILTER_SEVERITY, severity)
        return self
    
    def wait_for_table(self):
        """Wait for bug table to load"""
        self.wait_for_element(self.BUG_TABLE)
        return self
    
    def is_table_visible(self) -> bool:
        """Check if bug table is visible"""
        return self.is_visible(self.BUG_TABLE)
