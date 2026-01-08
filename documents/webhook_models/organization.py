"""Organization event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.organization import Organization, Membership
from .common.installation import Installation


class OrganizationEvent(WebhookBase):
    """
    GitHub webhook event for organization activities.
    
    Event Type: organization
    Actions: member_added, member_removed, member_invited
    """
    
    action: str = Field(..., description="Action performed: member_added, member_removed, member_invited")
    
    membership: Optional[Membership] = Field(None, description="Membership details (for member events)")
    invitation: Optional[dict] = Field(None, description="Invitation details (for invitation events)")
    
    organization: Organization = Field(..., description="Organization details")
    sender: User = Field(..., description="User who performed the action")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "member_added",
                "membership": {
                    "url": "https://api.github.com/orgs/Octocoders/memberships/octocat",
                    "state": "active",
                    "role": "member",
                    "organization_url": "https://api.github.com/orgs/Octocoders"
                },
                "organization": {
                    "login": "Octocoders",
                    "id": 38302899,
                    "url": "https://api.github.com/orgs/Octocoders"
                },
                "sender": {
                    "login": "Codertocat",
                    "id": 21031067
                }
            }
        }