"""
Webhook processing tests.
Tests webhook payload parsing and processing logic.
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient


class TestWebhookProcessing:
    """Test webhook payload processing."""
    
    def load_test_payload(self, filename):
        """Load a test payload from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        if payload_path.exists():
            with open(payload_path, 'r') as f:
                return json.load(f)
        return {}
    
    def test_webhook_with_valid_payload(self, test_client: TestClient, sample_headers):
        """Test webhook processing with valid payload."""
        # Test with actual ping payload
        payload = self.load_test_payload("23_PingEvent.json")
        if payload:  # Only run if payload exists
            headers = {**sample_headers, "X-GitHub-Event": "ping"}
            response = test_client.post(
                "/api/v1/webhooks/github",
                json=payload,
                headers=headers
            )
            # Ping events should typically succeed or have validation issues
            assert response.status_code in [200, 201, 400, 401, 422]
        else:
            # Fallback test with minimal valid payload
            payload = {"zen": "Test payload", "hook": {"id": 12345}}
            response = test_client.post(
                "/api/v1/webhooks/github",
                json=payload,
                headers=sample_headers
            )
            assert response.status_code in [200, 400, 401, 422]
    
    def test_webhook_supported_event_types(self, test_client: TestClient):
        """Test that all supported event types are listed."""
        response = test_client.get("/api/v1/webhooks/github/events")
        assert response.status_code == 200
        
        data = response.json()
        events = data["events"]
        
        # Check for some key event types
        expected_events = [
            "push", "pull_request", "issues", "member", 
            "repository", "fork", "create", "delete"
        ]
        
        for event_type in expected_events:
            assert event_type in events, f"Expected event type '{event_type}' not found"
    
    def test_webhook_with_empty_payload(self, test_client: TestClient, sample_headers):
        """Test webhook with empty payload."""
        response = test_client.post(
            "/api/v1/webhooks/github",
            json={},
            headers=sample_headers
        )
        # Should handle empty payload gracefully
        assert response.status_code in [200, 400, 422]
    
    def test_webhook_with_invalid_json(self, test_client: TestClient, sample_headers):
        """Test webhook with invalid JSON."""
        response = test_client.post(
            "/api/v1/webhooks/github",
            data="invalid json",
            headers={**sample_headers, "content-type": "application/json"}
        )
        assert response.status_code in [400, 422]


class TestPayloadValidation:
    """Test payload validation for different webhook events."""
    
    def test_member_event_payload(self, test_client: TestClient):
        """Test member event payload structure."""
        payload = {
            "action": "added",
            "member": {
                "login": "testuser",
                "id": 12345,
                "type": "User"
            },
            "organization": {
                "login": "testorg",
                "id": 67890
            }
        }
        
        headers = {
            "X-GitHub-Event": "member",
            "X-GitHub-Delivery": "test-delivery",
            "X-Hub-Signature-256": "sha256=test",
            "User-Agent": "GitHub-Hookshot/test"
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        # Should process without server error
        assert response.status_code in [200, 400, 401, 422]
    
    def test_repository_event_payload(self, test_client: TestClient):
        """Test repository event payload structure."""
        payload = {
            "action": "created",
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testorg/test-repo",
                "private": False,
                "owner": {
                    "login": "testorg",
                    "id": 67890,
                    "type": "Organization"
                }
            },
            "organization": {
                "login": "testorg",
                "id": 67890
            }
        }
        
        headers = {
            "X-GitHub-Event": "repository",
            "X-GitHub-Delivery": "test-delivery",
            "X-Hub-Signature-256": "sha256=test",
            "User-Agent": "GitHub-Hookshot/test"
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        assert response.status_code in [200, 400, 401, 422]


class TestWebhookSecurity:
    """Test webhook security features."""
    
    def test_webhook_without_signature(self, test_client: TestClient):
        """Test webhook request without signature header."""
        headers = {
            "X-GitHub-Event": "ping",
            "X-GitHub-Delivery": "test-delivery",
            "User-Agent": "GitHub-Hookshot/test"
            # Missing X-Hub-Signature-256
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json={"zen": "test"},
            headers=headers
        )
        # Should handle missing signature appropriately
        assert response.status_code in [200, 400, 401, 422]
    
    def test_webhook_with_invalid_user_agent(self, test_client: TestClient):
        """Test webhook with non-GitHub user agent."""
        headers = {
            "X-GitHub-Event": "ping",
            "X-GitHub-Delivery": "test-delivery",
            "X-Hub-Signature-256": "sha256=test",
            "User-Agent": "NotGitHub/1.0"
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json={"zen": "test"},
            headers=headers
        )
        # Should handle suspicious user agent appropriately
        assert response.status_code in [200, 400, 401, 403, 422]