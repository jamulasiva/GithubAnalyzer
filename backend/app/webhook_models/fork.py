"""Fork event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class ForkEvent(WebhookBase):
    """
    GitHub webhook event for when a repository is forked.
    
    Event Type: fork
    No action field for fork events
    """
    
    # Fork events don't have an action field
    action: Optional[str] = None
    
    forkee: Repository = Field(..., description="The created fork repository")
    repository: Repository = Field(..., description="The original repository that was forked")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "forkee": {
                    "id": 186853003,
                    "name": "Hello-World",
                    "full_name": "octocat/Hello-World",
                    "fork": True
                },
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World", 
                    "full_name": "Codertocat/Hello-World",
                    "fork": False
                }
            }
        }