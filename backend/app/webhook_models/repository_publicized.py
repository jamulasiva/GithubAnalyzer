"""Repository publicized event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class RepositoryPublicizedEvent(WebhookBase):
    """
    GitHub webhook event for when a repository is made public.
    
    Event Type: repository
    Action: publicized
    """
    
    action: str = Field(..., description="Action performed: publicized")
    
    repository: Repository = Field(..., description="Repository that was made public")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "publicized",
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World",
                    "private": False
                },
                "sender": {
                    "login": "Codertocat",
                    "id": 21031067
                }
            }
        }