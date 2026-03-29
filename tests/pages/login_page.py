"""Login Page Object Model"""
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page"""
    
    # Selectors
    USERNAME_INPUT = "[data-testid='username-input']"
    PASSWORD_INPUT = "[data-testid='password-input']"
    LOGIN_BUTTON = "[data-testid='login-button']"
    ERROR_MESSAGE = "[data-testid='error-message']"
    LOGOUT_BUTTON = "[data-testid='logout-button']"
    USER_MENU = "[data-testid='user-menu']"
    
    def navigate_to_login(self):
        """Navigate to login page"""
        return self.navigate("/login")
    
    def enter_username(self, username: str):
        """Enter username"""
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """Enter password"""
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_visible(self.USER_MENU) or self.is_visible(self.LOGOUT_BUTTON)
    
    def click_logout(self):
        """Click logout button"""
        if self.is_visible(self.USER_MENU):
            self.click(self.USER_MENU)
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def wait_for_login_form(self):
        """Wait for login form to be ready"""
        self.wait_for_element(self.USERNAME_INPUT)
        self.wait_for_element(self.PASSWORD_INPUT)
        return self
