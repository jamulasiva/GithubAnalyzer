"""Installation event webhook model."""

from typing import Optional, List

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class InstallationEvent(WebhookBase):
    """
    GitHub webhook event for GitHub App installation activities.
    
    Event Type: installation
    Actions: created, deleted, suspend, unsuspend, new_permissions_accepted
    """
    
    action: str = Field(..., description="Action performed: created, deleted, suspend, unsuspend, new_permissions_accepted")
    
    installation: Installation = Field(..., description="Installation details")
    repositories: Optional[List[Repository]] = Field(None, description="Repositories affected (for some actions)")
    requester: Optional[User] = Field(None, description="User who requested the installation")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "created",
                "installation": {
                    "id": 1,
                    "account": {
                        "login": "octocat",
                        "id": 1,
                        "type": "User"
                    },
                    "repository_selection": "all",
                    "app_id": 1,
                    "target_id": 1,
                    "target_type": "User"
                },
                "sender": {
                    "login": "octocat",
                    "id": 1
                }
            }
        }