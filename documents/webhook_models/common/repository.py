"""Repository models for GitHub webhooks."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl

from .user import RepositoryOwner


class Repository(BaseModel):
    """GitHub repository model used across webhook events."""
    
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: RepositoryOwner
    html_url: HttpUrl
    description: Optional[str] = None
    fork: bool
    url: HttpUrl
    
    # Archive URLs
    archive_url: Optional[str] = None  # Contains template
    assignees_url: Optional[str] = None  # Contains template
    blobs_url: Optional[str] = None  # Contains template
    branches_url: Optional[str] = None  # Contains template
    collaborators_url: Optional[str] = None  # Contains template
    comments_url: Optional[str] = None  # Contains template
    commits_url: Optional[str] = None  # Contains template
    compare_url: Optional[str] = None  # Contains template
    contents_url: Optional[str] = None  # Contains template
    contributors_url: Optional[HttpUrl] = None
    deployments_url: Optional[HttpUrl] = None
    downloads_url: Optional[HttpUrl] = None
    events_url: Optional[HttpUrl] = None
    forks_url: Optional[HttpUrl] = None
    git_commits_url: Optional[str] = None  # Contains template
    git_refs_url: Optional[str] = None  # Contains template
    git_tags_url: Optional[str] = None  # Contains template
    git_url: Optional[str] = None
    issue_comment_url: Optional[str] = None  # Contains template
    issue_events_url: Optional[str] = None  # Contains template
    issues_url: Optional[str] = None  # Contains template
    keys_url: Optional[str] = None  # Contains template
    labels_url: Optional[str] = None  # Contains template
    languages_url: Optional[HttpUrl] = None
    merges_url: Optional[HttpUrl] = None
    milestones_url: Optional[str] = None  # Contains template
    notifications_url: Optional[str] = None  # Contains template
    pulls_url: Optional[str] = None  # Contains template
    releases_url: Optional[str] = None  # Contains template
    ssh_url: Optional[str] = None
    stargazers_url: Optional[HttpUrl] = None
    statuses_url: Optional[str] = None  # Contains template
    subscribers_url: Optional[HttpUrl] = None
    subscription_url: Optional[HttpUrl] = None
    tags_url: Optional[HttpUrl] = None
    teams_url: Optional[HttpUrl] = None
    trees_url: Optional[str] = None  # Contains template
    clone_url: Optional[HttpUrl] = None
    mirror_url: Optional[HttpUrl] = None
    hooks_url: Optional[HttpUrl] = None
    svn_url: Optional[HttpUrl] = None
    
    # Repository properties
    homepage: Optional[str] = None
    size: Optional[int] = None
    stargazers_count: Optional[int] = None
    watchers_count: Optional[int] = None
    language: Optional[str] = None
    has_issues: Optional[bool] = None
    has_projects: Optional[bool] = None
    has_wiki: Optional[bool] = None
    has_pages: Optional[bool] = None
    has_downloads: Optional[bool] = None
    has_discussions: Optional[bool] = None
    forks_count: Optional[int] = None
    archived: Optional[bool] = None
    disabled: Optional[bool] = None
    open_issues_count: Optional[int] = None
    license: Optional[dict] = None  # License object
    allow_forking: Optional[bool] = None
    is_template: Optional[bool] = None
    web_commit_signoff_required: Optional[bool] = None
    topics: Optional[List[str]] = None
    visibility: Optional[str] = None  # "public", "private", "internal"
    forks: Optional[int] = None
    open_issues: Optional[int] = None
    watchers: Optional[int] = None
    default_branch: Optional[str] = None
    
    # Timestamps
    created_at: Optional[str] = None  # ISO 8601
    updated_at: Optional[str] = None  # ISO 8601
    pushed_at: Optional[str] = None  # ISO 8601
    
    # Template repository (if created from template)
    template_repository: Optional["Repository"] = None


class RepositoryLicense(BaseModel):
    """Repository license information."""
    
    key: str
    name: str
    spdx_id: Optional[str] = None
    url: Optional[HttpUrl] = None
    node_id: str


# Avoid circular imports
Repository.model_rebuild()