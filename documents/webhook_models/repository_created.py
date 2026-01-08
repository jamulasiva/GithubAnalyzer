"""Repository created event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class RepositoryCreatedEvent(WebhookBase):
    """
    GitHub webhook event for when a repository is created.
    
    Event Type: repository
    Action: created
    
    This event occurs when:
    - A new repository is created
    - A repository is created from a template
    - A repository is forked (separate fork event also exists)
    """
    
    action: str = Field("created", const=True)
    repository: Repository = Field(..., description="The newly created repository")
    sender: User = Field(..., description="The user who created the repository")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "created",
                "repository": {
                    "id": 186853002,
                    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World",
                    "private": False,
                    "fork": False,
                    "url": "https://api.github.com/repos/Codertocat/Hello-World",
                    "html_url": "https://github.com/Codertocat/Hello-World",
                    "description": "A new repository",
                    "created_at": "2019-05-15T15:19:25Z",
                    "updated_at": "2019-05-15T15:20:41Z",
                    "default_branch": "main"
                },
                "sender": {
                    "login": "Codertocat",
                    "id": 21031067,
                    "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                    "type": "User",
                    "site_admin": False
                }
            }
        }