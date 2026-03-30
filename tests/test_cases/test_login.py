import pytest
from pages.login_page import LoginPage


class TestLogin:
    """Test cases for login functionality"""
    
    def test_successful_login(self, page):
        """Test successful login redirects to dashboard"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("admin", "admin123")
        
        # Assert that we are redirected to dashboard
        assert login_page.is_on_dashboard(), f"Expected to be on dashboard, but URL is {page.url}"
    
    def test_failed_login(self, page):
        """Test failed login shows error message"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("admin", "wrongpassword")
        
        # Assert error message is displayed
        error_message = login_page.get_error_message()
        assert error_message != "" or "Invalid credentials" in page.content() or "登录失败" in page.content(), \
            "Expected error message for failed login"
    
    def test_empty_fields(self, page):
        """Test empty fields show validation error"""
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Click login without filling fields
        login_button = page.locator('button:has-text("登录")')
        login_button.click()
        
        # Wait for validation
        page.wait_for_timeout(500)
        
        # Assert validation error is shown
        validation_error = login_page.get_validation_error()
        assert validation_error != "" or page.locator(".el-form-item__error").count() > 0, \
            "Expected validation error for empty fields"
