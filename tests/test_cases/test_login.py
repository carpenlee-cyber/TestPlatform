"""Login functionality tests"""
import pytest
from pages.login_page import LoginPage


@pytest.mark.smoke
class TestLogin:
    """Test cases for login functionality"""
    
    def test_successful_login(self, page, base_url):
        """Test successful login with valid credentials"""
        login_page = LoginPage(page, base_url)
        login_page.navigate_to_login()
        login_page.wait_for_login_form()
