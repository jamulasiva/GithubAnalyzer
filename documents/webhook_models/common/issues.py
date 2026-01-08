"""Issue and Pull Request models for GitHub webhooks."""

from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from .user import User


class Label(BaseModel):
    """GitHub label model."""
    
    id: Optional[int] = None
    node_id: Optional[str] = None
    url: Optional[HttpUrl] = None
    name: str
    color: str
    default: Optional[bool] = None
    description: Optional[str] = None


class Milestone(BaseModel):
    """GitHub milestone model."""
    
    url: HttpUrl
    html_url: HttpUrl
    labels_url: HttpUrl
    id: int
    node_id: str
    number: int
    title: str
    description: Optional[str] = None
    creator: User
    open_issues: int
    closed_issues: int
    state: str  # "open" or "closed"
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    due_on: Optional[str] = None  # ISO 8601
    closed_at: Optional[str] = None  # ISO 8601


class Reactions(BaseModel):
    """GitHub reactions model."""
    
    url: HttpUrl
    total_count: int
    plus_one: int = 0  # +1 reactions
    minus_one: int = 0  # -1 reactions 
    laugh: int = 0
    hooray: int = 0
    confused: int = 0
    heart: int = 0
    rocket: int = 0
    eyes: int = 0

    class Config:
        fields = {
            'plus_one': '+1',
            'minus_one': '-1'
        }


class Issue(BaseModel):
    """GitHub issue model."""
    
    url: HttpUrl
    repository_url: HttpUrl
    labels_url: str  # Contains template
    comments_url: HttpUrl
    events_url: HttpUrl
    html_url: HttpUrl
    id: int
    node_id: str
    number: int
    title: str
    user: User
    labels: List[Label] = []
    state: str  # "open" or "closed"
    locked: bool
    assignee: Optional[User] = None
    assignees: List[User] = []
    milestone: Optional[Milestone] = None
    comments: int
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    closed_at: Optional[str] = None  # ISO 8601
    author_association: str
    active_lock_reason: Optional[str] = None
    body: Optional[str] = None
    reactions: Optional[Reactions] = None
    timeline_url: Optional[HttpUrl] = None
    performed_via_github_app: Optional[dict] = None
    state_reason: Optional[str] = None


class PullRequestBranch(BaseModel):
    """Pull request head/base branch model."""
    
    label: str
    ref: str
    sha: str
    user: User
    repo: Optional["Repository"] = None


class PullRequest(BaseModel):
    """GitHub pull request model."""
    
    url: HttpUrl
    id: int
    node_id: str
    html_url: HttpUrl
    diff_url: HttpUrl
    patch_url: HttpUrl
    issue_url: HttpUrl
    number: int
    state: str  # "open", "closed", "merged"
    locked: bool
    title: str
    user: User
    body: Optional[str] = None
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    closed_at: Optional[str] = None  # ISO 8601
    merged_at: Optional[str] = None  # ISO 8601
    merge_commit_sha: Optional[str] = None
    assignee: Optional[User] = None
    assignees: List[User] = []
    requested_reviewers: List[User] = []
    requested_teams: List["Team"] = []
    labels: List[Label] = []
    milestone: Optional[Milestone] = None
    draft: bool
    commits_url: HttpUrl
    review_comments_url: HttpUrl
    review_comment_url: str  # Contains template
    comments_url: HttpUrl
    statuses_url: HttpUrl
    head: PullRequestBranch
    base: PullRequestBranch
    author_association: str
    auto_merge: Optional[dict] = None
    active_lock_reason: Optional[str] = None


class Team(BaseModel):
    """GitHub team model."""
    
    id: int
    node_id: str
    url: HttpUrl
    html_url: HttpUrl
    name: str
    slug: str
    description: Optional[str] = None
    privacy: str  # "closed" or "secret"
    permission: str  # "pull", "push", "admin", "maintain", "triage"
    members_url: str  # Contains template
    repositories_url: HttpUrl
    parent: Optional["Team"] = None


class Comment(BaseModel):
    """GitHub comment model."""
    
    id: int
    node_id: str
    url: HttpUrl
    html_url: HttpUrl
    body: str
    user: User
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    author_association: str
    reactions: Optional[Reactions] = None


class Review(BaseModel):
    """GitHub pull request review model."""
    
    id: int
    node_id: str
    user: User
    body: Optional[str] = None
    commit_id: str
    submitted_at: str  # ISO 8601
    state: str  # "approved", "changes_requested", "commented", "dismissed"
    html_url: HttpUrl
    pull_request_url: HttpUrl
    author_association: str


# Import Repository here to avoid circular import
from .repository import Repository

# Rebuild models to resolve forward references
PullRequestBranch.model_rebuild()
PullRequest.model_rebuild()
Team.model_rebuild()