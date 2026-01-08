"""Git-related models for GitHub webhooks."""

from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from .user import GitUser


class Commit(BaseModel):
    """Git commit model."""
    
    id: str  # Full SHA
    tree_id: str
    distinct: bool
    message: str
    timestamp: str  # ISO 8601
    url: HttpUrl
    author: GitUser
    committer: GitUser
    added: List[str] = []
    removed: List[str] = []
    modified: List[str] = []


class Pusher(BaseModel):
    """Git pusher model for push events."""
    
    name: str
    email: str