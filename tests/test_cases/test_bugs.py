import pytest
from pages.bugs_page import BugsPage


class TestBugs:
    """Test cases for bug management"""
    
    def test_create_bug(self, logged_in_page):
        """Test creating a bug"""
        page = logged_in_page
        bugs_page = BugsPage(page)
        
        # Navigate to bugs page
        bugs_page.navigate()
        
        # Get initial row count
        initial_count = bugs_page.get_row_count()
        
        # Create a new bug
        bugs_page.click_create()
        bugs_page.fill_form("Auto Bug " + str(__import__('time').time()), "HIGH")
        bugs_page.submit()
        
        # Wait for table to refresh
        page.wait_for_timeout(2000)
        
        # Assert row count increased by 1
        new_count = bugs_page.get_row_count()
        assert new_count == initial_count + 1, f"Expected row count to increase by 1, got {new_count} vs {initial_count}"
    
    def test_bug_severity_tag(self, logged_in_page):
        """Test that bug severity tag is displayed correctly"""
        page = logged_in_page
        bugs_page = BugsPage(page)
        
        # Navigate to bugs page
        bugs_page.navigate()
        
        # Create a new bug with CRITICAL severity
        bugs_page.click_create()
        bugs_page.fill_form("Severity Test Bug", "CRITICAL")
        bugs_page.submit()
        
        # Wait for table to refresh
        page.wait_for_timeout(2000)
        
        # Assert severity tag is displayed
        severity = bugs_page.get_first_row_severity()
        assert severity != "", "Expected severity to be displayed"
        
        # Assert severity tag has correct type class
        tag_type = bugs_page.get_severity_tag_type()
        assert tag_type == "danger", f"Expected CRITICAL severity to have 'danger' tag type, got '{tag_type}'"
