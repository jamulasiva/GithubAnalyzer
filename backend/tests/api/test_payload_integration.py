"""
Comprehensive webhook payload tests using actual GitHub webhook samples.
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient


class TestWebhookPayloads:
    """Test webhook processing with actual GitHub payload samples."""
    
    # Mapping of payload files to their corresponding GitHub event types
    PAYLOAD_EVENT_MAP = {
        "01_AddMemberEvent.json": "member",
        "02_MemberPermissionChangedEvent.json": "member", 
        "03_OrganizationMemberAddedEvent.json": "organization",
        "04_TeamAddedToRepositoryEvent.json": "team_add",
        "05_TeamMemberAddedEvent.json": "team",
        "06_RepositoryCreatedEvent.json": "repository",
        "07_RepositoryMadePublicEvent.json": "repository",
        "08_BranchProtectionRuleCreatedEvent.json": "branch_protection_rule",
        "09_DeployKeyCreatedEvent.json": "deploy_key",
        "10_RepositoryRulesetCreatedEvent.json": "repository_ruleset",
        "11_CodeScanningAlertCreatedEvent.json": "code_scanning_alert",
        "12_DependabotAlertCreatedEvent.json": "dependabot_alert",
        "13_PersonalAccessTokenRequestCreated.json": "personal_access_token_request",
        "14_SecretScanningAlertCreated.json": "secret_scanning_alert",
        "15_PushEvent.json": "push",
        "16_PullRequestOpenedEvent.json": "pull_request",
        "17_IssueOpenedEvent.json": "issues",
        "19_PullRequestReviewSubmittedEvent.json": "pull_request_review",
        "20_CreateBranchEvent.json": "create",
        "21_DeleteBranchEvent.json": "delete", 
        "22_ForkEvent.json": "fork",
        "23_PingEvent.json": "ping",
        "24_Meta_WebhookDeleted_Event.json": "meta",
        "25_InstallationCreatedEvent.json": "installation"
    }
    
    def load_payload(self, filename):
        """Load a payload file from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        try:
            with open(payload_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            pytest.skip(f"Could not load payload {filename}: {e}")
    
    def create_headers(self, event_type, delivery_id=None):
        """Create appropriate headers for a GitHub webhook event."""
        return {
            "X-GitHub-Event": event_type,
            "X-GitHub-Delivery": delivery_id or f"test-delivery-{event_type}",
            "X-Hub-Signature-256": "sha256=test-signature",
            "User-Agent": "GitHub-Hookshot/test"
        }
    
    @pytest.mark.parametrize("payload_file,event_type", PAYLOAD_EVENT_MAP.items())
    def test_webhook_with_specific_payload(self, test_client: TestClient, payload_file, event_type):
        """Test webhook endpoint with each specific payload type."""
        payload = self.load_payload(payload_file)
        headers = self.create_headers(event_type, f"test-{payload_file}")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        # Should not result in server error (500)
        assert response.status_code != 500, f"Server error with payload {payload_file}"
        # Accept various response codes based on processing/validation
        assert response.status_code in [200, 201, 400, 401, 422], \
            f"Unexpected status code {response.status_code} for {payload_file}"
    
    def test_member_added_event(self, test_client: TestClient):
        """Test member added event specifically."""
        payload = self.load_payload("01_AddMemberEvent.json")
        headers = self.create_headers("member", "member-added-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        assert response.status_code in [200, 201, 400, 401, 422]
        if response.status_code == 200:
            # If successful, check response structure
            data = response.json()
            assert "status" in data or "message" in data
    
    def test_repository_created_event(self, test_client: TestClient):
        """Test repository created event specifically."""
        payload = self.load_payload("06_RepositoryCreatedEvent.json")
        headers = self.create_headers("repository", "repo-created-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_push_event(self, test_client: TestClient):
        """Test push event specifically."""
        payload = self.load_payload("15_PushEvent.json")
        headers = self.create_headers("push", "push-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_pull_request_opened_event(self, test_client: TestClient):
        """Test pull request opened event specifically."""
        payload = self.load_payload("16_PullRequestOpenedEvent.json")
        headers = self.create_headers("pull_request", "pr-opened-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_security_alert_events(self, test_client: TestClient):
        """Test security-related alert events."""
        security_payloads = [
            "11_CodeScanningAlertCreatedEvent.json",
            "12_DependabotAlertCreatedEvent.json", 
            "14_SecretScanningAlertCreated.json"
        ]
        
        event_types = [
            "code_scanning_alert",
            "dependabot_alert",
            "secret_scanning_alert"
        ]
        
        for payload_file, event_type in zip(security_payloads, event_types):
            payload = self.load_payload(payload_file)
            headers = self.create_headers(event_type, f"security-test-{event_type}")
            
            response = test_client.post(
                "/api/v1/webhooks/github",
                json=payload,
                headers=headers
            )
            
            assert response.status_code in [200, 201, 400, 401, 422], \
                f"Failed for security event {event_type}"
    
    def test_ping_event(self, test_client: TestClient):
        """Test ping event (webhook setup verification)."""
        payload = self.load_payload("23_PingEvent.json")
        headers = self.create_headers("ping", "ping-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        # Ping events should typically succeed
        assert response.status_code in [200, 201], \
            f"Ping event failed with status {response.status_code}"
    
    def test_installation_event(self, test_client: TestClient):
        """Test GitHub App installation event."""
        payload = self.load_payload("25_InstallationCreatedEvent.json")
        headers = self.create_headers("installation", "installation-test")
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=payload,
            headers=headers
        )
        
        assert response.status_code in [200, 201, 400, 401, 422]


class TestPayloadValidation:
    """Test payload validation and structure."""
    
    def load_payload(self, filename):
        """Load a payload file from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        try:
            with open(payload_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            pytest.skip(f"Could not load payload {filename}: {e}")
    
    def test_all_payloads_are_valid_json(self):
        """Test that all payload files contain valid JSON."""
        payload_dir = Path(__file__).parent.parent / "payloads"
        json_files = list(payload_dir.glob("*.json"))
        
        assert len(json_files) > 0, "No JSON payload files found"
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {json_file.name}: {e}")
    
    def test_payload_required_fields(self):
        """Test that payloads contain expected GitHub webhook fields."""
        # Test a few key payloads for required fields
        test_cases = [
            ("01_AddMemberEvent.json", ["action", "member", "organization"]),
            ("06_RepositoryCreatedEvent.json", ["action", "repository"]),
            ("15_PushEvent.json", ["ref", "commits", "repository"]),
            ("16_PullRequestOpenedEvent.json", ["action", "pull_request", "repository"]),
            ("23_PingEvent.json", ["zen", "hook"]),
        ]
        
        for payload_file, required_fields in test_cases:
            payload = self.load_payload(payload_file)
            
            for field in required_fields:
                assert field in payload, \
                    f"Required field '{field}' missing in {payload_file}"
    
    def test_payload_sender_field(self):
        """Test that most payloads have a sender field."""
        # Most GitHub webhooks include a sender field
        payloads_with_sender = [
            "01_AddMemberEvent.json",
            "06_RepositoryCreatedEvent.json",
            "15_PushEvent.json",
            "16_PullRequestOpenedEvent.json",
            "17_IssueOpenedEvent.json",
        ]
        
        for payload_file in payloads_with_sender:
            payload = self.load_payload(payload_file)
            assert "sender" in payload, f"Sender field missing in {payload_file}"
            
            # Sender should have login and id
            sender = payload["sender"]
            assert "login" in sender, f"Sender login missing in {payload_file}"
            assert "id" in sender, f"Sender id missing in {payload_file}"


class TestWebhookIntegration:
    """Integration tests for webhook processing workflow."""
    
    def load_payload(self, filename):
        """Load a payload file from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        try:
            with open(payload_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            pytest.skip(f"Could not load payload {filename}: {e}")
    
    def test_webhook_processing_workflow(self, test_client: TestClient):
        """Test complete webhook processing workflow."""
        # Test with a simple ping event first
        ping_payload = self.load_payload("23_PingEvent.json")
        ping_headers = {
            "X-GitHub-Event": "ping",
            "X-GitHub-Delivery": "workflow-test-ping",
            "X-Hub-Signature-256": "sha256=test-signature",
            "User-Agent": "GitHub-Hookshot/test"
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=ping_payload,
            headers=ping_headers
        )
        
        # Ping should work
        assert response.status_code in [200, 201]
        
        # Now test with a repository event
        repo_payload = self.load_payload("06_RepositoryCreatedEvent.json")
        repo_headers = {
            "X-GitHub-Event": "repository",
            "X-GitHub-Delivery": "workflow-test-repo",
            "X-Hub-Signature-256": "sha256=test-signature",
            "User-Agent": "GitHub-Hookshot/test"
        }
        
        response = test_client.post(
            "/api/v1/webhooks/github",
            json=repo_payload,
            headers=repo_headers
        )
        
        # Repository event should be processed
        assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_multiple_events_sequence(self, test_client: TestClient):
        """Test processing multiple different events in sequence."""
        event_sequence = [
            ("23_PingEvent.json", "ping"),
            ("06_RepositoryCreatedEvent.json", "repository"),
            ("01_AddMemberEvent.json", "member"),
            ("15_PushEvent.json", "push")
        ]
        
        for i, (payload_file, event_type) in enumerate(event_sequence):
            payload = self.load_payload(payload_file)
            headers = {
                "X-GitHub-Event": event_type,
                "X-GitHub-Delivery": f"sequence-test-{i}",
                "X-Hub-Signature-256": "sha256=test-signature",
                "User-Agent": "GitHub-Hookshot/test"
            }
            
            response = test_client.post(
                "/api/v1/webhooks/github",
                json=payload,
                headers=headers
            )
            
            # Each event should be processed without server error
            assert response.status_code != 500, \
                f"Server error in sequence for {event_type} (step {i})"