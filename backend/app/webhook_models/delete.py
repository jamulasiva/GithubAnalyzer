"""Delete event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class DeleteEvent(WebhookBase):
    """
    GitHub webhook event for when a branch or tag is deleted.
    
    Event Type: delete
    No action field for delete events
    """
    
    # Delete events don't have an action field
    action: Optional[str] = None
    
    ref: str = Field(..., description="The name of the branch or tag that was deleted")
    ref_type: str = Field(..., description="Either 'branch' or 'tag'")
    pusher_type: str = Field(..., description="Either 'user' or 'deploy_key'")
    
    repository: Repository = Field(..., description="Repository where the branch/tag was deleted")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "ref": "feature-branch",
                "ref_type": "branch", 
                "pusher_type": "user",
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World"
                },
                "sender": {
                    "login": "octocat",
                    "id": 1
                }
            }
        }