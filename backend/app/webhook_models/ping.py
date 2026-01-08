"""Ping event webhook model."""

from typing import Optional, List, Dict, Any

from pydantic import Field, BaseModel

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class Hook(BaseModel):
    """Webhook configuration model."""
    
    type: str
    id: int
    name: str
    active: bool
    events: List[str]
    config: Dict[str, Any]
    updated_at: str  # ISO 8601
    created_at: str  # ISO 8601


class PingEvent(WebhookBase):
    """
    GitHub webhook event sent when a webhook is initially created.
    
    Event Type: ping
    No action field for ping events
    """
    
    # Ping events don't have an action field
    action: Optional[str] = None
    
    zen: str = Field(..., description="Random zen message from GitHub")
    hook_id: int = Field(..., description="ID of the webhook")
    hook: Hook = Field(..., description="Webhook configuration details")
    
    repository: Optional[Repository] = Field(None, description="Repository (for repo webhooks)")
    sender: Optional[User] = Field(None, description="User who created the webhook")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "zen": "Keep it logically awesome.",
                "hook_id": 109948940,
                "hook": {
                    "type": "Repository",
                    "id": 109948940,
                    "name": "web",
                    "active": True,
                    "events": ["push", "pull_request"],
                    "config": {
                        "content_type": "json",
                        "url": "https://example.com/webhooks",
                        "insecure_ssl": "0"
                    }
                }
            }
        }