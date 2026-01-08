"""Push event webhook model."""

from typing import List, Optional

from pydantic import Field, HttpUrl

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.git import Commit, Pusher


class PushEvent(WebhookBase):
    """
    GitHub webhook event for push operations.
    
    Event Type: push
    No action field for push events
    
    This event occurs when:
    - Commits are pushed to a repository branch
    - A branch is created
    - A branch is deleted (deleted=true)
    """
    
    # Push events don't have an action field
    action: Optional[str] = None
    
    # Push-specific fields
    ref: str = Field(..., description="The full git ref that was pushed")
    before: str = Field(..., description="SHA of the most recent commit before the push")
    after: str = Field(..., description="SHA of the most recent commit after the push")
    created: bool = Field(..., description="Whether this push created the ref")
    deleted: bool = Field(..., description="Whether this push deleted the ref")
    forced: bool = Field(..., description="Whether this push was a force push")
    base_ref: Optional[str] = Field(None, description="Base ref for the push")
    compare: HttpUrl = Field(..., description="URL showing changes in this push")
    commits: List[Commit] = Field(..., description="Array of commits pushed")
    head_commit: Optional[Commit] = Field(None, description="The most recent commit")
    
    # Standard webhook fields
    repository: Repository = Field(..., description="The repository where the event occurred")
    pusher: Pusher = Field(..., description="The user who pushed the commits")
    sender: User = Field(..., description="The user who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "ref": "refs/heads/main",
                "before": "0000000000000000000000000000000000000000",
                "after": "abcdef1234567890abcdef1234567890abcdef12",
                "created": False,
                "deleted": False,
                "forced": False,
                "base_ref": None,
                "compare": "https://github.com/Codertocat/Hello-World/compare/000000000000...abcdef123456",
                "commits": [
                    {
                        "id": "abcdef1234567890abcdef1234567890abcdef12",
                        "tree_id": "fedcba0987654321fedcba0987654321fedcba09",
                        "distinct": True,
                        "message": "Initial commit",
                        "timestamp": "2023-03-17T15:42:05Z",
                        "url": "https://github.com/Codertocat/Hello-World/commit/abcdef123456",
                        "author": {
                            "name": "Codertocat",
                            "email": "codertocat@github.com",
                            "username": "Codertocat"
                        },
                        "committer": {
                            "name": "Codertocat", 
                            "email": "codertocat@github.com",
                            "username": "Codertocat"
                        },
                        "added": ["README.md"],
                        "removed": [],
                        "modified": []
                    }
                ],
                "pusher": {
                    "name": "Codertocat",
                    "email": "codertocat@github.com"
                }
            }
        }