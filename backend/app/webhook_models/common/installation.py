"""Installation models for GitHub Apps."""

from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from .user import User


class AppPermissions(BaseModel):
    """GitHub App permissions."""
    
    actions: Optional[str] = None
    administration: Optional[str] = None
    checks: Optional[str] = None
    contents: Optional[str] = None
    deployments: Optional[str] = None
    environments: Optional[str] = None
    issues: Optional[str] = None
    metadata: Optional[str] = None
    packages: Optional[str] = None
    pages: Optional[str] = None
    pull_requests: Optional[str] = None
    repository_hooks: Optional[str] = None
    repository_projects: Optional[str] = None
    secret_scanning_alerts: Optional[str] = None
    secrets: Optional[str] = None
    security_events: Optional[str] = None
    single_file: Optional[str] = None
    statuses: Optional[str] = None
    vulnerability_alerts: Optional[str] = None
    workflows: Optional[str] = None
    members: Optional[str] = None
    organization_administration: Optional[str] = None
    organization_hooks: Optional[str] = None
    organization_plan: Optional[str] = None
    organization_projects: Optional[str] = None
    organization_secrets: Optional[str] = None
    organization_self_hosted_runners: Optional[str] = None
    organization_user_blocking: Optional[str] = None
    team_discussions: Optional[str] = None


class GitHubApp(BaseModel):
    """GitHub App model."""
    
    id: int
    slug: Optional[str] = None
    node_id: str
    owner: User
    name: str
    description: Optional[str] = None
    external_url: str
    html_url: str
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    permissions: AppPermissions
    events: List[str]
    installations_count: Optional[int] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    webhook_secret: Optional[str] = None
    pem: Optional[str] = None


class Installation(BaseModel):
    """GitHub App installation model."""
    
    id: int
    account: User  # The user/org that installed the app
    repository_selection: str  # "selected" or "all"
    access_tokens_url: str
    repositories_url: str
    html_url: str
    app_id: int
    app_slug: Optional[str] = None
    target_id: int
    target_type: str  # "Organization" or "User"
    permissions: AppPermissions
    events: List[str]
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    single_file_name: Optional[str] = None
    has_multiple_single_files: Optional[bool] = None
    single_file_paths: Optional[List[str]] = None
    suspended_by: Optional[User] = None
    suspended_at: Optional[str] = None


class Enterprise(BaseModel):
    """GitHub Enterprise model."""
    
    id: int
    slug: str
    name: str
    node_id: str
    avatar_url: str
    description: Optional[str] = None
    website_url: Optional[str] = None
    html_url: str
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601