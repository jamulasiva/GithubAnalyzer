"""Issues opened event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.issues import Issue


class IssuesOpenedEvent(WebhookBase):
    """
    GitHub webhook event for when an issue is opened.
    
    Event Type: issues
    Action: opened
    """
    
    action: str = Field(default="opened")
    issue: Issue = Field(..., description="The issue that was opened")
    repository: Repository = Field(..., description="The repository where the event occurred")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "opened",
                "issue": {
                    "id": 1,
                    "number": 1,
                    "title": "Bug found in feature",
                    "state": "open",
                    "body": "I found a bug in the new feature..."
                }
            }
        }