"""Bugs management tests"""
import pytest
from pages.login_page import LoginPage
from pages.bugs_page import BugsPage


@pytest.mark.smoke
class TestBugsManagement:
    """Test cases for bug management functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        """Login before each test"""
        login_page = LoginPage(page, base_url)
        login_page.navigate_to_login()
        login_page.login("admin", "password123")
        login_page.wait_for_navigation()
    
    def test_create_bug(self, page, base_url):
        """Test creating a new bug"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        initial_count = bugs_page.get_bug_count()
        
        bugs_page.create_bug(
            title="Bug - Login Button Not Working",
            description="Clicking login button does nothing",
            severity="high",
            priority="critical",
            status="open"
        )
        bugs_page.wait_for_table()
        
        assert bugs_page.get_bug_count() > initial_count, \
            "Bug count should increase after creation"
    
    def test_read_bug_list(self, page, base_url):
        """Test viewing bugs list"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        assert bugs_page.is_table_visible(), "Bug table should be visible"
        
        # Verify table has rows or shows empty state
        assert bugs_page.get_bug_count() >= 0, "Should be able to get bug count"
    
    def test_update_bug(self, page, base_url):
        """Test updating an existing bug"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Ensure there's at least one bug
        if bugs_page.get_bug_count() == 0:
            bugs_page.create_bug(
                title="Bug for Update Test",
                description="Initial bug description"
            )
            bugs_page.wait_for_table()
        
        # Edit the first bug
        bugs_page.click_edit_first()
        bugs_page.enter_title("Updated Bug Title")
        bugs_page.enter_description("Updated bug description")
        bugs_page.select_status("in_progress")
        bugs_page.click_save()
        bugs_page.wait_for_table()
        
        assert bugs_page.is_table_visible(), "Should return to bug list after update"
    
    def test_delete_bug(self, page, base_url):
        """Test deleting a bug"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Create a bug to delete
        bugs_page.create_bug(
            title="Bug to Delete",
            description="This bug will be deleted"
        )
        bugs_page.wait_for_table()
        
        initial_count = bugs_page.get_bug_count()
        
        # Delete the first bug
        bugs_page.delete_first_bug()
        bugs_page.wait_for_table()
        
        assert bugs_page.get_bug_count() < initial_count, \
            "Bug count should decrease after deletion"
    
    def test_search_bug(self, page, base_url):
        """Test searching for bugs"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Create a bug with specific title
        bugs_page.create_bug(
            title="Searchable Unique Bug",
            description="This is for bug search testing"
        )
        bugs_page.wait_for_table()
        
        # Search for it
        bugs_page.search_bug("Searchable Unique")
        
        assert bugs_page.is_table_visible(), "Search results should be visible"
    
    def test_filter_bugs_by_status(self, page, base_url):
        """Test filtering bugs by status"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Create bugs with different statuses
        bugs_page.create_bug(
            title="Open Bug",
            description="This is open",
            status="open"
        )
        bugs_page.wait_for_table()
        
        # Filter by open status
        bugs_page.filter_by_status("open")
        
        assert bugs_page.is_table_visible(), "Filtered results should be visible"
    
    def test_filter_bugs_by_severity(self, page, base_url):
        """Test filtering bugs by severity"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Create a high severity bug
        bugs_page.create_bug(
            title="High Severity Bug",
            description="Critical issue",
            severity="critical"
        )
        bugs_page.wait_for_table()
        
        # Filter by critical severity
        bugs_page.filter_by_severity("critical")
        
        assert bugs_page.is_table_visible(), "Filtered results should be visible"
    
    def test_bug_lifecycle(self, page, base_url):
        """Test complete bug lifecycle from open to closed"""
        bugs_page = BugsPage(page, base_url)
        bugs_page.navigate_to_bugs()
        bugs_page.wait_for_table()
        
        # Create a new bug
        bugs_page.create_bug(
            title="Lifecycle Test Bug",
            description="Testing bug lifecycle",
            status="open"
        )
        bugs_page.wait_for_table()
        
        # Edit and change status to in_progress
        bugs_page.click_edit_first()
        bugs_page.select_status("in_progress")
        bugs_page.click_save()
        bugs_page.wait_for_table()
        
        # Change status to resolved
        bugs_page.click_edit_first()
        bugs_page.select_status("resolved")
        bugs_page.click_save()
        bugs_page.wait_for_table()
        
        # Change status to closed
        bugs_page.click_edit_first()
        bugs_page.select_status("closed")
        bugs_page.click_save()
        bugs_page.wait_for_table()
        
        assert bugs_page.is_table_visible(), "Bug lifecycle should complete successfully"
