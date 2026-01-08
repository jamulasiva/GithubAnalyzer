"""Issue comment event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.issues import Issue, Comment


class IssueCommentEvent(WebhookBase):
    """
    GitHub webhook event for issue comment activities.
    
    Event Type: issue_comment
    Actions: created, edited, deleted
    """
    
    action: str = Field(..., description="Action performed: created, edited, deleted")
    
    issue: Issue = Field(..., description="The issue the comment was made on")
    comment: Comment = Field(..., description="The comment that was created/edited/deleted")
    repository: Repository = Field(..., description="Repository where the action occurred")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    # Additional fields for edited action
    changes: Optional[dict] = Field(None, description="Changes made (for edited action)")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "created",
                "issue": {
                    "id": 1,
                    "number": 1,
                    "title": "Bug found in feature",
                    "state": "open"
                },
                "comment": {
                    "id": 1,
                    "body": "I can reproduce this issue",
                    "author_association": "COLLABORATOR"
                },
                "repository": {
                    "id": 186853002,
                    "name": "Hello-World",
                    "full_name": "Codertocat/Hello-World"
                }
            }
        }