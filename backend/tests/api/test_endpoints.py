"""
API endpoint tests for the GitHub Audit Platform.
"""

import pytest
import json
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health and basic endpoints."""
    
    def test_health_endpoint(self, test_client: TestClient):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
    
    def test_root_endpoint(self, test_client: TestClient):
        """Test the root endpoint."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestAuditEndpoints:
    """Test audit API endpoints."""
    
    def test_api_info(self, test_client: TestClient):
        """Test the API info endpoint."""
        response = test_client.get("/api/v1/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "endpoints" in data
    
    def test_list_organizations(self, test_client: TestClient):
        """Test listing organizations."""
        response = test_client.get("/api/v1/audit/organizations")
        assert response.status_code == 200
        data = response.json()
        assert "organizations" in data
        assert "total" in data
        assert isinstance(data["organizations"], list)
    
    def test_list_organizations_with_pagination(self, test_client: TestClient):
        """Test organizations endpoint with pagination parameters."""
        response = test_client.get("/api/v1/audit/organizations?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        assert data["limit"] == 10
    
    def test_list_repositories(self, test_client: TestClient):
        """Test listing repositories."""
        response = test_client.get("/api/v1/audit/repositories")
        assert response.status_code == 200
        data = response.json()
        assert "repositories" in data
    
    def test_list_webhook_events(self, test_client: TestClient):
        """Test listing webhook events."""
        response = test_client.get("/api/v1/audit/events")
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
    
    def test_analytics_summary(self, test_client: TestClient):
        """Test analytics summary endpoint."""
        response = test_client.get("/api/v1/audit/analytics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data


class TestWebhookEndpoints:
    """Test webhook API endpoints."""
    
    def test_list_supported_events(self, test_client: TestClient):
        """Test listing supported webhook events."""
        response = test_client.get("/api/v1/webhooks/github/events")
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
        assert "total_event_types" in data
    
    def test_webhook_test_endpoint(self, test_client: TestClient):
        """Test webhook test endpoint."""
        response = test_client.get("/api/v1/webhooks/github/test")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "endpoint" in data
    
    def test_webhook_endpoint_missing_headers(self, test_client: TestClient):
        """Test webhook endpoint with missing required headers."""
        response = test_client.post("/api/v1/webhooks/github", json={})
        # Should fail due to missing required headers
        assert response.status_code == 422  # Unprocessable Entity


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_invalid_organization(self, test_client: TestClient):
        """Test getting details for non-existent organization."""
        response = test_client.get("/api/v1/audit/organizations/non-existent-org")
        assert response.status_code == 404
    
    def test_invalid_event_id(self, test_client: TestClient):
        """Test getting details for non-existent event."""
        response = test_client.get("/api/v1/audit/events/non-existent-event-id")
        assert response.status_code == 404
    
    def test_invalid_pagination_parameters(self, test_client: TestClient):
        """Test invalid pagination parameters."""
        # Negative skip should fail
        response = test_client.get("/api/v1/audit/organizations?skip=-1")
        assert response.status_code == 422
        
        # Too large limit should fail
        response = test_client.get("/api/v1/audit/organizations?limit=1000")
        assert response.status_code == 422