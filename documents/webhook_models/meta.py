"""Meta event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .ping import Hook  # Reuse Hook model from ping.py


class MetaEvent(WebhookBase):
    """
    GitHub webhook event for webhook metadata changes.
    
    Event Type: meta
    Actions: deleted
    """
    
    action: str = Field(..., description="Action performed: deleted")
    
    hook_id: int = Field(..., description="ID of the webhook that was deleted")
    hook: Hook = Field(..., description="Webhook configuration details")
    
    repository: Optional[Repository] = Field(None, description="Repository (for repo webhooks)")
    sender: Optional[User] = Field(None, description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "deleted",
                "hook_id": 109948940,
                "hook": {
                    "type": "Repository",
                    "id": 109948940,
                    "name": "web",
                    "active": True,
                    "events": ["push", "pull_request"]
                }
            }
        }