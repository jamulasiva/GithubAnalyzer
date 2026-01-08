"""Organization models for GitHub webhooks."""

from typing import Optional

from pydantic import BaseModel, HttpUrl

from .user import User


class Organization(BaseModel):
    """GitHub organization model used across webhook events."""
    
    login: str
    id: int
    node_id: str
    url: HttpUrl
    repos_url: HttpUrl
    events_url: HttpUrl
    hooks_url: HttpUrl
    issues_url: HttpUrl
    members_url: str  # Contains template
    public_members_url: str  # Contains template
    avatar_url: HttpUrl
    description: Optional[str] = ""
    gravatar_id: Optional[str] = ""
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    twitter_username: Optional[str] = None
    is_verified: Optional[bool] = None
    has_organization_projects: Optional[bool] = None
    has_repository_projects: Optional[bool] = None
    public_repos: Optional[int] = None
    public_gists: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    html_url: Optional[HttpUrl] = None
    created_at: Optional[str] = None  # ISO 8601
    updated_at: Optional[str] = None  # ISO 8601
    type: Optional[str] = "Organization"


class Membership(BaseModel):
    """GitHub organization membership model."""
    
    url: HttpUrl
    state: str  # "active", "pending"
    role: str  # "member", "admin"
    organization_url: HttpUrl
    user: User