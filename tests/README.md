# Test Platform Automation Tests

This directory contains Playwright-based automated tests for the TestPlatform application.

## Setup

1. Install dependencies:
```bash
pip install pytest playwright requests python-dotenv
playwright install chromium
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration if needed.

## Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest test_cases/test_login.py
```

Run in headed mode (visible browser):
```bash
HEADLESS=false pytest
```

## Project Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── pages/                   # Page Object Models
│   ├── login_page.py
│   ├── test_cases_page.py
│   └── bugs_page.py
├── test_cases/              # Test cases
│   ├── test_login.py
│   ├── test_test_cases.py
│   └── test_bugs.py
├── utils/                   # Utility functions
│   └── api_helper.py
└── .env.example             # Environment variables template
```

## Page Objects

The tests use the Page Object Model pattern for maintainability:
- `LoginPage`: Handles login page interactions
- `TestCasesPage`: Handles test case management page
- `BugsPage`: Handles bug management page

## API Helper

`utils/api_helper.py` provides direct REST API calls for:
- User authentication
- Test case CRUD operations
- Bug CRUD operations
