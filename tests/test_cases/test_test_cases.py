import pytest
from pages.test_cases_page import TestCasesPage


class TestTestCases:
    """Test cases for test case management"""
    
    def test_create_and_delete_test_case(self, logged_in_page):
        """Test creating and then deleting a test case"""
        page = logged_in_page
        test_cases_page = TestCasesPage(page)
        
        # Navigate to test cases page
        test_cases_page.navigate()
        
        # Get initial row count
        initial_count = test_cases_page.get_row_count()
        
        # Create a new test case
        test_cases_page.click_create()
        test_cases_page.fill_form("Auto Test Case " + str(__import__('time').time()), "HIGH")
        test_cases_page.submit()
        
        # Wait for table to refresh
        page.wait_for_timeout(2000)
        
        # Assert row count increased by 1
        new_count = test_cases_page.get_row_count()
        assert new_count == initial_count + 1, f"Expected row count to increase by 1, got {new_count} vs {initial_count}"
        
        # Delete the test case we just created (first row)
        test_cases_page.delete_first()
        
        # Wait for table to refresh
        page.wait_for_timeout(2000)
        
        # Assert row count decreased by 1
        final_count = test_cases_page.get_row_count()
        assert final_count == initial_count, f"Expected row count to return to initial, got {final_count} vs {initial_count}"
