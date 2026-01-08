"""Create event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class CreateEvent(WebhookBase):
    """
    GitHub webhook event for when a branch or tag is created.
    
    Event Type: create
    No action field for create events
    """
    
    # Create events don't have an action field
    action: Optional[str] = None
    
    ref: str = Field(..., description="The name of the branch or tag that was created")
    ref_type: str = Field(..., description="Either 'branch' or 'tag'")
    master_branch: str = Field(..., description="The name of the default branch")
    description: Optional[str] = Field(None, description="The optional description for this branch/tag")
    pusher_type: str = Field(..., description="Either 'user' or 'deploy_key'")
    
    repository: Repository = Field(..., description="Repository where the branch/tag was created")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "ref": "feature-branch",
                "ref_type": "branch",
                "master_branch": "main",
                "description": None,
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