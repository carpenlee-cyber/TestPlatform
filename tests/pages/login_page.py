from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost"
        
    def navigate(self):
        """Navigate to login page"""
        self.page.goto(f"{self.base_url}/login")
        self.page.wait_for_selector(".login-container", timeout=10000)
    
    def login(self, username: str, password: str):
        """Perform login with given credentials"""
        # Fill username input - using placeholder attribute
        username_input = self.page.locator('input[placeholder="用户名"]')
        username_input.fill(username)
        
        # Fill password input
        password_input = self.page.locator('input[placeholder="密码"]')
        password_input.fill(password)
        
        # Click login button
        login_button = self.page.locator('button:has-text("登录")')
        login_button.click()
        
        # Wait for navigation or error
        self.page.wait_for_timeout(2000)
    
    def get_error_message(self) -> str:
        """Get error message from ElMessage (appears in DOM as notification)"""
        # Element Plus messages appear as el-message elements
        message = self.page.locator(".el-message--error .el-message__content")
        if message.count() > 0:
            return message.inner_text()
        return ""
    
    def get_validation_error(self) -> str:
        """Get form validation error message"""
        # Element Plus form validation errors appear in el-form-item__error
        error = self.page.locator(".el-form-item__error")
        if error.count() > 0:
            return error.first.inner_text()
        return ""
    
    def is_on_dashboard(self) -> bool:
        """Check if current page is dashboard"""
        return "/dashboard" in self.page.url
