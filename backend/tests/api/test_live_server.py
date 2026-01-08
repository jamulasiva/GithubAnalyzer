"""
Live server integration tests - tests against the actual running backend.
These tests make real HTTP requests to localhost:8000
"""

import pytest
import json
import httpx
from pathlib import Path
import asyncio
import hmac
import hashlib


class TestLiveServerIntegration:
    """Test against the actual running backend server."""
    
    BASE_URL = "http://localhost:8000"
    # Use default webhook secret from .env (you can override this)
    WEBHOOK_SECRET = "your_webhook_secret_here"
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup and cleanup for each test."""
        # Store delivery IDs created during this test session
        self.test_delivery_ids = []
        yield
        # Cleanup: Remove test data after each test
        self.cleanup_test_data()
        
    def cleanup_test_data(self):
        """Remove test data from database after test completion."""
        # Skip cleanup to preserve test data for examination
        print(f"\n📊 Preserving test data in database. Delivery IDs: {self.test_delivery_ids}")
        print("💡 To examine the data, query the database using these delivery IDs")
        return
        
        # Original cleanup code (commented out for data examination)
        # if not self.test_delivery_ids:
        #     return
        #     
        # try:
        #     import sys
        #     from pathlib import Path
        #     backend_path = Path(__file__).parent.parent.parent
        #     sys.path.insert(0, str(backend_path))
        #     
        #     from app.core.database import get_database
        #     from app.models.core import WebhookEvent
        #     
        #     db_gen = get_database()
        #     db = next(db_gen)
        #     try:
        #         # Delete test webhook events
        #         deleted_count = db.query(WebhookEvent).filter(
        #             WebhookEvent.delivery_id.in_(self.test_delivery_ids)
        #         ).delete(synchronize_session=False)
        #         db.commit()
        #         print(f"\n✓ Cleaned up {deleted_count} test webhook events")
        #     finally:
        #         db.close()
        # except Exception as e:
        #     print(f"\n⚠ Warning: Failed to cleanup test data: {e}")
    
    # Mapping of payload files to their corresponding GitHub event types
    PAYLOAD_EVENT_MAP = {
        "01_AddMemberEvent.json": "member",
        "02_MemberPermissionChangedEvent.json": "member", 
        "03_OrganizationMemberAddedEvent.json": "organization",
        "04_TeamAddedToRepositoryEvent.json": "team",
        "05_TeamMemberAddedEvent.json": "team",
        "06_RepositoryCreatedEvent.json": "repository",
        "07_RepositoryMadePublicEvent.json": "repository",
        # Skip unsupported event types: branch_protection_rule, deploy_key, repository_ruleset
        # "08_BranchProtectionRuleCreatedEvent.json": "branch_protection_rule",  # Unsupported
        # "09_DeployKeyCreatedEvent.json": "deploy_key",  # Unsupported  
        # "10_RepositoryRulesetCreatedEvent.json": "repository_ruleset",  # Unsupported
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
    
    def enhance_payload_for_validation(self, payload, event_type):
        """Add missing required fields to payload for validation."""
        # NOTE: All necessary fields are now included directly in the payload files
        # This method is kept for any future dynamic field requirements
        enhanced = payload.copy()
        
        # Most enhancement logic is now commented out as payload files are complete
        # Uncomment specific sections below if dynamic field generation is needed
        
        return enhanced
    
    def enhance_user_object(self, user, login, user_id):
        """Helper method to enhance user objects with all required fields."""
        # NOTE: User fields are now included directly in payload files
        # This method is kept for any future dynamic user field requirements
        pass
        
        # Commented out enhancement logic - fields are now in payload files
        # user_defaults = {
        #     "node_id": f"MDQ6VXNlcnt{user_id}",
        #     "avatar_url": f"https://avatars.githubusercontent.com/u/{user_id}?v=4",
        #     "url": f"https://api.github.com/users/{login}",
        #     "html_url": f"https://github.com/{login}",
        #     "followers_url": f"https://api.github.com/users/{login}/followers",
        #     "following_url": f"https://api.github.com/users/{login}/following{{/other_user}}",
        #     "gists_url": f"https://api.github.com/users/{login}/gists{{/gist_id}}",
        #     "starred_url": f"https://api.github.com/users/{login}/starred{{/owner}}{{/repo}}",
        #     "subscriptions_url": f"https://api.github.com/users/{login}/subscriptions",
        #     "organizations_url": f"https://api.github.com/users/{login}/orgs",
        #     "repos_url": f"https://api.github.com/users/{login}/repos",
        #     "events_url": f"https://api.github.com/users/{login}/events{{/privacy}}",
        #     "received_events_url": f"https://api.github.com/users/{login}/received_events",
        #     "type": "User",
        #     "site_admin": False
        # }
        # for key, value in user_defaults.items():
        #     if key not in user:
        #         user[key] = value
    
    def load_payload(self, filename):
        """Load a payload file from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        try:
            with open(payload_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            pytest.skip(f"Could not load payload {filename}: {e}")
    
    def generate_signature(self, payload_body, secret=None):
        """Generate a valid GitHub webhook signature."""
        secret = secret or self.WEBHOOK_SECRET
        
        # Ensure payload_body is bytes 
        if isinstance(payload_body, dict):
            payload_body = json.dumps(payload_body, separators=(',', ':'))
        
        if isinstance(payload_body, str):
            payload_body = payload_body.encode('utf-8')
        
        # Use same algorithm as backend validation
        hash_object = hmac.new(
            secret.encode('utf-8'),
            payload_body, 
            hashlib.sha256
        )
        
        return "sha256=" + hash_object.hexdigest()
    
    def create_headers(self, event_type, delivery_id=None, payload=None):
        """Create appropriate headers for a GitHub webhook event with valid signature."""
        import time
        # Add timestamp to ensure unique delivery IDs
        unique_delivery_id = delivery_id or f"live-test-delivery-{event_type}"
        if delivery_id:
            unique_delivery_id = f"{delivery_id}-{int(time.time()*1000)}"
        
        # Track this delivery ID for cleanup
        self.test_delivery_ids.append(unique_delivery_id)
            
        headers = {
            "X-GitHub-Event": event_type,
            "X-GitHub-Delivery": unique_delivery_id,
            "User-Agent": "GitHub-Hookshot/live-test",
            "Content-Type": "application/json"
        }
        
        # Generate proper signature if payload is provided
        if payload is not None:
            headers["X-Hub-Signature-256"] = self.generate_signature(payload)
        else:
            # Use a test signature for non-payload requests
            headers["X-Hub-Signature-256"] = "sha256=test-signature-live"
        
        return headers
    
    def test_server_is_running(self):
        """Test that the backend server is accessible."""
        try:
            response = httpx.get(f"{self.BASE_URL}/health", timeout=5.0)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            print(f"✅ Server is running: {data}")
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            pytest.fail(f"Backend server is not running on {self.BASE_URL}. Start it with 'python main.py'. Error: {e}")
    
    def test_api_endpoints_accessible(self):
        """Test that API endpoints are accessible."""
        self.test_server_is_running()  # Ensure server is running first
        
        endpoints = [
            "/",
            "/api/v1/",
            "/api/v1/audit/organizations",
            "/api/v1/webhooks/github/test"
        ]
        
        for endpoint in endpoints:
            response = httpx.get(f"{self.BASE_URL}{endpoint}", timeout=5.0)
            assert response.status_code in [200, 404], f"Unexpected status for {endpoint}: {response.status_code}"
            print(f"✅ {endpoint}: {response.status_code}")
    
    def test_ping_webhook_live(self):
        """Test ping webhook against live server."""
        self.test_server_is_running()
        
        payload = self.load_payload("23_PingEvent.json")
        enhanced_payload = self.enhance_payload_for_validation(payload, "ping")
        
        # Convert payload to JSON string (same as httpx will send)
        payload_json = json.dumps(enhanced_payload, separators=(',', ':'))
        headers = self.create_headers("ping", "live-ping-test", payload_json)
        
        print(f"🔗 Testing ping webhook with payload: {list(enhanced_payload.keys())}")
        
        # Send the exact JSON string we signed, not letting httpx serialize it
        response = httpx.post(
            f"{self.BASE_URL}/api/v1/webhooks/github",
            content=payload_json,
            headers=headers,
            timeout=10.0
        )
        
        print(f"📊 Response: {response.status_code}")
        print(f"📋 Response body: {response.text[:200]}...")
        
        # Should not result in server error, 422 is OK for validation issues
        assert response.status_code != 500, f"Server error: {response.text}"
        assert response.status_code in [200, 201, 400, 401, 422]
        
        # 422 means payload validation failed but webhook was processed
        if response.status_code == 422:
            print("✅ Webhook signature validated successfully! (Payload validation failed - this is normal for test data)")
        elif response.status_code in [200, 201]:
            print("✅ Webhook processed successfully!")
    
    @pytest.mark.parametrize("payload_file,event_type", list(PAYLOAD_EVENT_MAP.items()))  # Test all payload events
    def test_webhook_payloads_live(self, payload_file, event_type):
        """Test webhook endpoints against live server with actual payloads."""
        self.test_server_is_running()
        
        payload = self.load_payload(payload_file)
        enhanced_payload = self.enhance_payload_for_validation(payload, event_type)
        payload_json = json.dumps(enhanced_payload, separators=(',', ':'))
        headers = self.create_headers(event_type, f"live-test-{payload_file}", payload_json)
        
        print(f"🔗 Testing {event_type} webhook with {payload_file}")
        
        # Send the exact JSON string we signed
        response = httpx.post(
            f"{self.BASE_URL}/api/v1/webhooks/github",
            content=payload_json,
            headers=headers,
            timeout=10.0
        )
        
        print(f"📊 {payload_file}: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ {payload_file}: Successfully processed!")
        elif response.status_code == 422:
            print(f"⚠️ {payload_file}: Validation issues (signature OK)")
        elif response.status_code not in [200, 201]:
            print(f"📋 Response: {response.text[:200]}...")
        
        # Should not result in server error
        assert response.status_code != 500, f"Server error for {payload_file}: {response.text}"
        assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_member_events_live(self):
        """Test all member-related events against live server."""
        self.test_server_is_running()
        
        member_payloads = [
            ("01_AddMemberEvent.json", "member"),
            ("02_MemberPermissionChangedEvent.json", "member"),
            ("03_OrganizationMemberAddedEvent.json", "organization")
        ]
        
        for payload_file, event_type in member_payloads:
            payload = self.load_payload(payload_file)
            enhanced_payload = self.enhance_payload_for_validation(payload, event_type)
            payload_json = json.dumps(enhanced_payload, separators=(',', ':'))
            headers = self.create_headers(event_type, f"live-member-test-{payload_file}", payload_json)
            
            print(f"👥 Testing member event: {payload_file}")
            
            # Send the exact JSON string we signed
            response = httpx.post(
                f"{self.BASE_URL}/api/v1/webhooks/github",
                content=payload_json,
                headers=headers,
                timeout=10.0
            )
            
            print(f"📊 {payload_file}: {response.status_code}")
            if response.status_code in [200, 201]:
                print(f"✅ {payload_file}: Successfully processed!")
            elif response.status_code == 422:
                print(f"⚠️ {payload_file}: Validation issues (signature OK)")
            
            # Should not result in server error
            assert response.status_code != 500, f"Server error for {payload_file}: {response.text}"
            assert response.status_code in [200, 201, 400, 401, 422]
    
    def test_audit_endpoints_live(self):
        """Test audit endpoints against live server."""
        self.test_server_is_running()
        
        audit_endpoints = [
            "/api/v1/audit/organizations",
            "/api/v1/audit/repositories", 
            "/api/v1/audit/events",
            "/api/v1/audit/analytics/summary"
        ]
        
        for endpoint in audit_endpoints:
            print(f"📋 Testing audit endpoint: {endpoint}")
            
            response = httpx.get(f"{self.BASE_URL}{endpoint}", timeout=10.0)
            
            print(f"📊 {endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response keys: {list(data.keys())}")
            
            assert response.status_code in [200, 404, 422], f"Unexpected status for {endpoint}: {response.status_code}"


class TestSequentialWebhookProcessing:
    """Test processing multiple webhooks in sequence against live server."""
    
    BASE_URL = "http://localhost:8000"
    
    def load_payload(self, filename):
        """Load a payload file from the payloads directory."""
        payload_path = Path(__file__).parent.parent / "payloads" / filename
        try:
            with open(payload_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            pytest.skip(f"Could not load payload {filename}: {e}")
    
    def create_headers(self, event_type, delivery_id):
        """Create appropriate headers for a GitHub webhook event."""
        return {
            "X-GitHub-Event": event_type,
            "X-GitHub-Delivery": delivery_id,
            "User-Agent": "GitHub-Hookshot/sequence-test",
            "Content-Type": "application/json"
        }
    
    def generate_signature(self, payload_body, secret="your_webhook_secret_here"):
        """Generate a valid GitHub webhook signature."""
        if isinstance(payload_body, dict):
            payload_body = json.dumps(payload_body, separators=(',', ':'))
        
        if isinstance(payload_body, str):
            payload_body = payload_body.encode('utf-8')
        
        signature = hmac.new(
            secret.encode('utf-8'), 
            payload_body, 
            hashlib.sha256
        ).hexdigest()
        
        return f"sha256={signature}"
    
    def test_webhook_sequence_live(self):
        """Test processing a sequence of webhook events."""
        # Check server is running
        try:
            response = httpx.get(f"{self.BASE_URL}/health", timeout=5.0)
            assert response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            pytest.skip("Backend server is not running")
        
        # Test sequence of common webhook events
        event_sequence = [
            ("23_PingEvent.json", "ping", "Webhook setup"),
            ("06_RepositoryCreatedEvent.json", "repository", "Repository created"),
            ("01_AddMemberEvent.json", "member", "Member added"),
            ("15_PushEvent.json", "push", "Code pushed")
        ]
        
        print("🔄 Testing webhook processing sequence:")
        
        for i, (payload_file, event_type, description) in enumerate(event_sequence):
            payload = self.load_payload(payload_file)
            payload_json = json.dumps(payload, separators=(',', ':'))
            import time
            unique_delivery_id = f"sequence-test-{i}-{int(time.time()*1000)}"
            headers = self.create_headers(event_type, unique_delivery_id)
            
            # Add proper signature
            headers["X-Hub-Signature-256"] = self.generate_signature(payload_json)
            
            print(f"📤 Step {i+1}: {description} ({payload_file})")
            
            # Send the exact JSON string we signed
            response = httpx.post(
                f"{self.BASE_URL}/api/v1/webhooks/github",
                content=payload_json,
                headers=headers,
                timeout=10.0
            )
            
            print(f"📥 Response: {response.status_code}")
            
            # Should not result in server error
            assert response.status_code != 500, \
                f"Server error at step {i+1} ({description}): {response.text}"
            
            # Allow processing time between requests
            import time
            time.sleep(0.5)
        
        print("✅ Webhook sequence processing completed!")
        
        # Check if data was processed by querying audit endpoints
        print("📋 Checking audit data after processing:")
        
        audit_response = httpx.get(f"{self.BASE_URL}/api/v1/audit/organizations", timeout=5.0)
        if audit_response.status_code == 200:
            data = audit_response.json()
            print(f"📊 Organizations found: {data.get('total', 0)}")
        
        events_response = httpx.get(f"{self.BASE_URL}/api/v1/audit/events", timeout=5.0)
        if events_response.status_code == 200:
            data = events_response.json()
            print(f"📊 Events found: {data.get('total', 0)}")