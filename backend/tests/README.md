"""
README for the tests directory.

This directory contains comprehensive tests for the GitHub Audit Platform backend.
"""

# GitHub Audit Platform - Test Suite

This directory contains comprehensive tests for the backend API endpoints and webhook processing.

## Directory Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── api/                     # API endpoint tests
│   ├── test_endpoints.py    # Basic API endpoint tests
│   └── test_webhooks.py     # Webhook processing tests
├── data/                    # Test data and fixtures
├── payloads/                # GitHub webhook payload samples (JSON files)
└── README.md               # This file
```

## Running Tests

### Install Test Dependencies
```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests
```bash
# From the backend directory
pytest tests/

# With verbose output
pytest tests/ -v

# Run specific test file
pytest tests/api/test_endpoints.py

# Run specific test class
pytest tests/api/test_endpoints.py::TestAuditEndpoints

# Run specific test
pytest tests/api/test_endpoints.py::TestAuditEndpoints::test_list_organizations
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report
```

## Test Categories

### 1. API Endpoint Tests (`test_endpoints.py`)
- Health and basic endpoints
- Audit API endpoints (organizations, repositories, events)
- Webhook API endpoints
- Error handling and edge cases
- Pagination and parameter validation

### 2. Webhook Processing Tests (`test_webhooks.py`)
- Webhook payload processing
- Event type validation
- Security features (signatures, user agents)
- Payload structure validation

## Test Data

### Payloads Directory
Add your GitHub webhook payload JSON files to the `payloads/` directory:

```
payloads/
├── sample_push.json
├── sample_member_added.json
├── sample_repository_created.json
├── sample_pull_request.json
└── ...
```

These files should contain actual GitHub webhook payloads for testing different event types.

### Sample Payload Structure
```json
{
  "action": "opened",
  "repository": {
    "id": 123456789,
    "name": "test-repo",
    "full_name": "testorg/test-repo"
  },
  "sender": {
    "login": "testuser",
    "id": 987654321
  }
}
```

## Test Configuration

The test suite uses:
- **FastAPI TestClient** for API endpoint testing
- **SQLite in-memory database** for isolated testing
- **Pytest fixtures** for shared test data
- **Mocked dependencies** to avoid external service calls

## Writing New Tests

### API Endpoint Test Example
```python
def test_new_endpoint(self, test_client: TestClient):
    """Test description."""
    response = test_client.get("/api/v1/new-endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

### Webhook Test Example
```python
def test_webhook_event(self, test_client: TestClient):
    """Test webhook event processing."""
    payload = self.load_test_payload("sample_event.json")
    headers = {
        "X-GitHub-Event": "event_type",
        "X-GitHub-Delivery": "test-delivery-id",
        "X-Hub-Signature-256": "sha256=test-signature"
    }
    
    response = test_client.post(
        "/api/v1/webhooks/github",
        json=payload,
        headers=headers
    )
    assert response.status_code == 200
```

## Notes

- Tests use isolated SQLite databases to avoid affecting production data
- All tests are independent and can run in any order
- Test fixtures automatically handle setup and cleanup
- Mock external dependencies (database, GitHub API) as needed
- Add comprehensive test payloads to improve test coverage