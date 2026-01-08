"""Personal access token request event webhook model."""

from typing import Optional, Dict, Any

from pydantic import Field, BaseModel

from .common.base import WebhookBase
from .common.user import User
from .common.organization import Organization
from .common.installation import Installation


class PersonalAccessTokenRequest(BaseModel):
    """Personal access token request model."""
    
    id: int
    owner: User
    permissions_added: Dict[str, Any]
    permissions_upgraded: Dict[str, Any]
    permissions_result: Dict[str, Any]
    repository_selection: str  # "all" or "selected"
    repository_count: Optional[int] = None
    repositories: Optional[list] = None
    created_at: str  # ISO 8601
    token_expired: bool
    token_expires_at: Optional[str] = None  # ISO 8601
    token_last_used_at: Optional[str] = None  # ISO 8601


class PersonalAccessTokenRequestEvent(WebhookBase):
    """
    GitHub webhook event for personal access token request activities.
    
    Event Type: personal_access_token_request
    Actions: created, approved, denied, cancelled
    """
    
    action: str = Field(..., description="Action performed: created, approved, denied, cancelled")
    
    personal_access_token_request: PersonalAccessTokenRequest = Field(..., description="PAT request details")
    
    organization: Organization = Field(..., description="Organization where the request was made")
    sender: User = Field(..., description="User who performed the action")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "created",
                "personal_access_token_request": {
                    "id": 1,
                    "owner": {"login": "octocat", "id": 1},
                    "permissions_added": {
                        "repository": {
                            "contents": "write"
                        }
                    },
                    "repository_selection": "selected"
                }
            }
        }