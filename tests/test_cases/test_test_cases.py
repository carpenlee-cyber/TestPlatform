"""Test Cases CRUD tests"""
import pytest
from pages.login_page import LoginPage
from pages.test_cases_page import TestCasesPage


@pytest.mark.smoke
class TestTestCasesCRUD:
    """Test cases for test case management CRUD operations"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        """Login before each test"""
        login_page = LoginPage(page, base_url)
        login_page.navigate_to_login()
        login_page.login("admin", "password123")
        login_page.wait_for_navigation()
    
    def test_create_test_case(self, page, base_url):
        """Test creating a new test case"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        initial_count = test_cases_page.get_test_case_count()
        
        test_cases_page.create_test_case(
            title="Test Case - Login Feature",
            description="Verify user can login with valid credentials",
            priority="high",
            status="active"
        )
        test_cases_page.wait_for_table()
        
        assert test_cases_page.get_test_case_count() > initial_count, \
            "Test case count should increase after creation"
    
    def test_read_test_case(self, page, base_url):
        """Test viewing test cases list"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        assert test_cases_page.is_table_visible(), "Test case table should be visible"
        
        # Search for a test case
        test_cases_page.search_test_case("Login")
        
        # Verify search results are displayed
        assert test_cases_page.is_table_visible(), "Search results should be displayed"
    
    def test_update_test_case(self, page, base_url):
        """Test updating an existing test case"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        # Ensure there's at least one test case
        if test_cases_page.get_test_case_count() == 0:
            test_cases_page.create_test_case(
                title="Test Case for Update",
                description="Initial description"
            )
            test_cases_page.wait_for_table()
        
        # Edit the first test case
        test_cases_page.click_edit_first()
        test_cases_page.enter_title("Updated Test Case Title")
        test_cases_page.enter_description("Updated description")
        test_cases_page.select_priority("low")
        test_cases_page.click_save()
        test_cases_page.wait_for_table()
        
        assert test_cases_page.is_table_visible(), "Should return to table after update"
    
    def test_delete_test_case(self, page, base_url):
        """Test deleting a test case"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        # Create a test case to delete
        test_cases_page.create_test_case(
            title="Test Case to Delete",
            description="This will be deleted"
        )
        test_cases_page.wait_for_table()
        
        initial_count = test_cases_page.get_test_case_count()
        
        # Delete the first test case
        test_cases_page.delete_first_test_case()
        test_cases_page.wait_for_table()
        
        assert test_cases_page.get_test_case_count() < initial_count, \
            "Test case count should decrease after deletion"
    
    def test_search_test_case(self, page, base_url):
        """Test searching for test cases"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        # Create a test case with specific title
        test_cases_page.create_test_case(
            title="Searchable Unique Test",
            description="This is for search testing"
        )
        test_cases_page.wait_for_table()
        
        # Search for it
        test_cases_page.search_test_case("Searchable Unique")
        
        assert test_cases_page.is_table_visible(), "Search results should be visible"
    
    def test_cancel_create_test_case(self, page, base_url):
        """Test canceling test case creation"""
        test_cases_page = TestCasesPage(page, base_url)
        test_cases_page.navigate_to_test_cases()
        test_cases_page.wait_for_table()
        
        initial_count =