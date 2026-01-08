"""Pull request review event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.issues import PullRequest, Review


class PullRequestReviewEvent(WebhookBase):
    """
    GitHub webhook event for pull request review activities.
    
    Event Type: pull_request_review
    Actions: submitted, edited, dismissed
    """
    
    action: str = Field(..., description="Action performed: submitted, edited, dismissed")
    
    review: Review = Field(..., description="The review that was submitted/edited/dismissed")
    pull_request: PullRequest = Field(..., description="The pull request being reviewed")
    repository: Repository = Field(..., description="Repository where the action occurred")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    # Additional fields for specific actions
    changes: Optional[dict] = Field(None, description="Changes made (for edited action)")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "submitted",
                "review": {
                    "id": 1,
                    "user": {"login": "octocat", "id": 1},
                    "body": "Looks good to me!",
                    "state": "approved",
                    "author_association": "COLLABORATOR"
                },
                "pull_request": {
                    "id": 1,
                    "number": 1,
                    "title": "Add new feature",
                    "state": "open"
                },
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World"
                }
            }
        }