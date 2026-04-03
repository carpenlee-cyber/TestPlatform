from playwright.sync_api import Page, expect


class BugsPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost"
        
    def navigate(self):
        """Navigate to bugs page"""
        self.page.goto(f"{self.base_url}/bugs")
        self.page.wait_for_selector(".bugs-page", timeout=10000)
    
    def click_create(self):
        """Click the add new bug button"""
        add_button = self.page.locator('button:has-text("新增Bug")')
        add_button.click()
        # Wait for dialog to appear
        self.page.wait_for_selector(".el-dialog", timeout=5000)
    
    def fill_form(self, title: str, severity: str = "MEDIUM"):
        """Fill the bug form"""
        # Fill title - first input in dialog
        title_input = self.page.locator('.el-dialog input[type="text"]').first
        title_input.fill(title)
        
        # Select severity from dropdown
        severity_select = self.page.locator('.el-dialog .el-select').first
        severity_select.click()
        
        # Wait for dropdown options
        self.page.wait_for_selector(".el-select-dropdown__item", timeout=3000)
        
        # Select severity option
        option = self.page.locator(f'.el-select-dropdown__item:has-text("{severity}")')
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
            title_cell = first_row.locator("td").first  # First column is title
            return title_cell.inner_text()
        return ""
    
    def get_first_row_severity(self) -> str:
        """Get the severity of the first row"""
        first_row = self.page.locator(".el-table__row").first
        if first_row.count() > 0:
            severity_cell = first_row.locator("td").nth(1)  # Second column is severity
            return severity_cell.inner_text()
        return ""
    
    def get_row_count(self) -> int:
        """Get the number of rows in the table"""
        return self.page.locator(".el-table__row").count()
    
    def get_severity_tag_type(self) -> str:
        """Get the Element Plus tag type for severity (for CSS class validation)"""
        first_row = self.page.locator(".el-table__row").first
        if first_row.count() > 0:
            severity_cell = first_row.locator("td").nth(1)
            tag = severity_cell.locator(".el-tag")
            if tag.count() > 0:
                # Get class attribute to determine tag type
                class_attr = tag.get_attribute("class") or ""
                if "el-tag--danger" in class_attr:
                    return "danger"
                elif "el-tag--warning" in class_attr:
                    return "warning"
                elif "el-tag--info" in class_attr:
                    return "info"
                else:
                    return "default"
        return ""
    
    def delete_first(self):
        """Delete the first row"""
        first_row = self.page.locator(".el-table__row").first
        if first_row.count() > 0:
            delete_button = first_row.locator('button:has-text("删除")')
            delete_button.click()
            
            # Confirm deletion in popconfirm
            self.page.wait_for_selector(".el-popconfirm", timeout=3000)
            confirm_button = self.page.locator('.el-popconfirm__action button:has-text("确定")')
            confirm_button.click()
            self.page.wait_for_timeout(1000)
