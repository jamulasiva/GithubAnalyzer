"""User models for GitHub webhooks."""

from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class User(BaseModel):
    """GitHub user model used across webhook events."""
    
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: str = ""
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: str  # Contains template
    gists_url: str  # Contains template
    starred_url: str  # Contains template
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: str  # Contains template
    received_events_url: HttpUrl
    type: str  # Usually "User" or "Bot"
    site_admin: bool
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    hireable: Optional[bool] = None
    bio: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: Optional[int] = None
    public_gists: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class GitUser(BaseModel):
    """Git user model for commits and other Git operations."""
    
    name: str
    email: str
    username: Optional[str] = None  # GitHub username if available
    date: Optional[str] = None  # ISO 8601 timestamp


class RepositoryOwner(BaseModel):
    """Repository owner model (can be User or Organization)."""
    
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: str = ""
    url: HttpUrl
    html_url: HttpUrl
    type: str  # "User" or "Organization"
    site_admin: bool
    repos_url: Optional[HttpUrl] = None
    events_url: Optional[str] = None  # Contains template
    received_events_url: Optional[HttpUrl] = None
    
    # Additional fields for organizations
    members_url: Optional[str] = None  # Contains template
    public_members_url: Optional[str] = None  # Contains template
    description: Optional[str] = None