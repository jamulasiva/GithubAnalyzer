"""Pull request opened event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.issues import PullRequest


class PullRequestOpenedEvent(WebhookBase):
    """
    GitHub webhook event for when a pull request is opened.
    
    Event Type: pull_request
    Action: opened
    """
    
    action: str = Field("opened", const=True)
    number: int = Field(..., description="The pull request number")
    pull_request: PullRequest = Field(..., description="The pull request that was opened")
    repository: Repository = Field(..., description="The repository where the event occurred")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "opened",
                "number": 1,
                "pull_request": {
                    "id": 1,
                    "number": 1,
                    "title": "Add new feature",
                    "state": "open",
                    "body": "This PR adds a new feature"
                }
            }
        }