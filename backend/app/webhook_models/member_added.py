"""Member added event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation


class MemberAddedEvent(WebhookBase):
    """
    GitHub webhook event for when a user is added as a collaborator to a repository.
    
    Event Type: member
    Action: added
    
    This event occurs when:
    - A user accepts a repository invitation
    - A user is directly added as a collaborator to a repository
    """
    
    action: str = Field(default="added")
    member: User = Field(..., description="The user who was added as a collaborator")
    repository: Repository = Field(..., description="The repository where the event occurred")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "added",
                "member": {
                    "login": "octocat",
                    "id": 1,
                    "node_id": "MDQ6VXNlcjE=",
                    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/octocat",
                    "html_url": "https://github.com/octocat",
                    "type": "User",
                    "site_admin": False
                },
                "repository": {
                    "id": 186853002,
                    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World",
                    "private": False,
                    "fork": False,
                    "url": "https://api.github.com/repos/Codertocat/Hello-World",
                    "html_url": "https://github.com/Codertocat/Hello-World"
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