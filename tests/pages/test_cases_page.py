from playwright.sync_api import Page, expect


class TestCasesPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost"
        
    def navigate(self):
        """Navigate to test cases page"""
        self.page.goto(f"{self.base_url}/test-cases")
        self.page.wait_for_selector(".test-cases", timeout=10000)
    
    def click_create(self):
        """Click the create new test case button"""
        create_button = self.page.locator('button:has-text("新建用例")')
        create_button.click()
        # Wait for dialog to appear
        self.page.wait_for_selector(".el-dialog", timeout=5000)
    
    def fill_form(self, title: str, priority: str = "MEDIUM"):
        """Fill the test case form"""
        # Fill title
        title_input = self.page.locator('.el-dialog input[type="text"]').first
        title_input.fill(title)
        
        # Select priority from dropdown
        priority_select = self.page.locator('.el-dialog .el-select').first
        priority_select.click()
        
        # Wait for dropdown options and select
        self.page.wait_for_selector(".el-select-dropdown__item", timeout=3000)
        
        # Map priority to Chinese label
        priority_map = {
            "HIGH": "高",
            "MEDIUM": "中",
            "LOW": "低"
        }
        priority_label = priority_map.get(priority, priority)
        option = self.page.locator(f'.el-select-dropdown__item:has-text("{priority_label}")')
        option.click()
    
    def submit(self):
        """Submit the form"""
        submit_button = self.page.locator('.el-dialog__footer button:has-text("确定")')
        submit_button.click()
        # Wait for dialog to close
        self.page.wait_for_timeout(1000)
    
    def get_first_row_title(self) -> str:
        """Get the title of the first row in the table"""
        first_row = self.page.locator(".el-table__row").first
        if first_row.count() > 0:
            title_cell = first_row.locator("td").nth(1)  # Second column is title
            return title_cell.inner_text()
        return ""
    
    def get_row_count(self) -> int:
        """Get the number of rows in the table"""
        return self.page.locator(".el-table__row").count()
    
    def delete_first(self):
        """Delete the first row"""
        first_row = self.page.locator(".el-table__row").first
        if first_row.count() > 0:
            delete_button = first_row.locator('button:has-text("删除")')
            delete_button.click()
            
            # Confirm deletion in message box
            self.page.wait_for_selector(".el-message-box", timeout=3000)
            confirm_button = self.page.locator('.el-message-box__btns button:has-text("确定")')
            confirm_button.click()
            self.page.wait_for_timeout(1000)
