import requests


def login(api_base_url: str, username: str, password: str) -> str:
    """
    Login via REST API and return token
    
    Args:
        api_base_url: Base URL of the API (e.g., http://localhost:8080)
        username: Username for login
        password: Password for login
        
    Returns:
        JWT token string
    """
    url = f"{api_base_url}/api/auth/login"
    payload = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data.get("token", "")


def create_test_case(api_base_url: str, token: str, title: str, priority: str = "MEDIUM") -> int:
    """
    Create a test case via REST API
    
    Args:
        api_base_url: Base URL of the API
        token: JWT token for authentication
        title: Title of the test case
        priority: Priority level (HIGH, MEDIUM, LOW)
        
    Returns:
        ID of the created test case
    """
    url = f"{api_base_url}/api/test-cases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title,
        "description": "Auto-created test case",
        "steps": "Step 1: Execute test",
        "expectedResult": "Test passes",
        "priority": priority,
        "status": "DRAFT",
        "assignee": "admin"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data.get("id", 0)


def create_bug(api_base_url: str, token: str, title: str, severity: str = "MEDIUM") -> int:
    """
    Create a bug via REST API
    
    Args:
        api_base_url: Base URL of the API
        token: JWT token for authentication
        title: Title of the bug
        severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)
        
    Returns:
        ID of the created bug
    """
    url = f"{api_base_url}/api/bugs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title,
        "description": "Auto-created bug",
        "severity": severity,
        "status": "OPEN",
        "assignee": "admin",
        "reporter": "admin"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data.get("id", 0)


def delete_test_case(api_base_url: str, token: str, test_case_id: int):
    """
    Delete a test case via REST API
    
    Args:
        api_base_url: Base URL of the API
        token: JWT token for authentication
        test_case_id: ID of the test case to delete
    """
    url = f"{api_base_url}/api/test-cases/{test_case_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def delete_bug(api_base_url: str, token: str, bug_id: int):
    """
    Delete a bug via REST API
    
    Args:
        api_base_url: Base URL of the API
        token: JWT token for authentication
        bug_id: ID of the bug to delete
    """
    url = f"{api_base_url}/api/bugs/{bug_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
