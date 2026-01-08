"""Team member added event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.issues import Team


class TeamMemberAddedEvent(WebhookBase):
    """
    GitHub webhook event for when a member is added to a team.
    
    Event Type: membership
    Action: added
    """
    
    action: str = Field(default="added")
    scope: str = Field(default="team", description="Currently always 'team'")
    member: User = Field(..., description="The user who was added to the team")
    team: Team = Field(..., description="The team to which the member was added")
    organization: Organization = Field(..., description="The organization that owns the team")
    sender: User = Field(..., description="The user who performed the action")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    repository: Optional[Repository] = Field(None, description="Repository info (if applicable)")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "added",
                "scope": "team",
                "member": {
                    "login": "octocat",
                    "id": 1
                },
                "team": {
                    "id": 1,
                    "name": "developers",
                    "slug": "developers"
                }
            }
        }