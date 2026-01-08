"""Member permission changed event webhook model."""

from typing import Optional, Dict, Any

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class MemberEditedEvent(WebhookBase):
    """
    GitHub webhook event for member permission changes.
    
    Event Type: member
    Action: edited
    """
    
    action: str = Field(..., description="Action performed: edited")
    
    member: User = Field(..., description="The user whose permissions were changed")
    changes: Dict[str, Any] = Field(..., description="Changes made to the member's permissions")
    
    repository: Repository = Field(..., description="Repository where the action occurred")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "edited",
                "member": {
                    "login": "octocat",
                    "id": 1
                },
                "changes": {
                    "permission": {
                        "from": "read",
                        "to": "write"
                    }
                },
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World"
                }
            }
        }