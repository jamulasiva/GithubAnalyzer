"""
SQLAlchemy models for the GitHub Audit Platform.
These models correspond to the database schema and webhook Pydantic models.
"""

from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, Text, DateTime, 
    ForeignKey, Index, CheckConstraint, UniqueConstraint, ARRAY
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class Organization(Base):
    """Organization model based on webhook_models/common/organization.py"""
    
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True)
    github_id = Column(BigInteger, unique=True, nullable=False)
    login = Column(String(255), nullable=False)
    node_id = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    repos_url = Column(Text, nullable=False)
    events_url = Column(Text, nullable=False)
    hooks_url = Column(Text, nullable=False)
    issues_url = Column(Text, nullable=False)
    members_url = Column(Text, nullable=False)
    public_members_url = Column(Text, nullable=False)
    avatar_url = Column(Text, nullable=False)
    description = Column(Text)
    name = Column(String(255))
    company = Column(String(255))
    blog = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    twitter_username = Column(String(255))
    is_verified = Column(Boolean, default=False)
    has_organization_projects = Column(Boolean)
    has_repository_projects = Column(Boolean)
    public_repos = Column(Integer)
    public_gists = Column(Integer)
    followers = Column(Integer)
    following = Column(Integer)
    html_url = Column(Text)
    type = Column(String(50), default="Organization")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    github_created_at = Column(DateTime(timezone=True))
    github_updated_at = Column(DateTime(timezone=True))
    
    # Relationships
    repositories = relationship("Repository", back_populates="organization")
    memberships = relationship("OrganizationMembership", back_populates="organization")
    webhook_events = relationship("WebhookEvent", back_populates="organization")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('github_id > 0', name='org_github_id_check'),
        Index('idx_organizations_login', 'login'),
    )


class User(Base):
    """User model based on webhook_models/common/user.py"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    github_id = Column(BigInteger, unique=True, nullable=False)
    login = Column(String(255), nullable=False)
    node_id = Column(String(255), nullable=False)
    avatar_url = Column(Text)
    gravatar_id = Column(String(255))
    url = Column(Text, nullable=False)
    html_url = Column(Text, nullable=False)
    followers_url = Column(Text)
    following_url = Column(Text)
    gists_url = Column(Text)
    starred_url = Column(Text)
    subscriptions_url = Column(Text)
    organizations_url = Column(Text)
    repos_url = Column(Text)
    events_url = Column(Text)
    received_events_url = Column(Text)
    type = Column(String(50), default="User")
    site_admin = Column(Boolean, default=False)
    name = Column(String(255))
    company = Column(String(255))
    blog = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    hireable = Column(Boolean)
    bio = Column(Text)
    twitter_username = Column(String(255))
    public_repos = Column(Integer)
    public_gists = Column(Integer)
    followers = Column(Integer)
    following = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    github_created_at = Column(DateTime(timezone=True))
    github_updated_at = Column(DateTime(timezone=True))
    
    # Relationships
    owned_repositories = relationship("Repository", back_populates="owner")
    memberships = relationship("OrganizationMembership", back_populates="user")
    collaborations = relationship("RepositoryCollaborator", back_populates="user")
    sent_events = relationship("WebhookEvent", back_populates="sender")
    installations_suspended = relationship("Installation", back_populates="suspended_by")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('github_id > 0', name='user_github_id_check'),
        Index('idx_users_login', 'login'),
    )


class Repository(Base):
    """Repository model based on webhook_models/common/repository.py"""
    
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True)
    github_id = Column(BigInteger, unique=True, nullable=False)
    node_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    private = Column(Boolean, default=False)
    html_url = Column(Text, nullable=False)
    description = Column(Text)
    fork = Column(Boolean, default=False)
    url = Column(Text, nullable=False)
    
    # Repository URLs
    archive_url = Column(Text)
    assignees_url = Column(Text)
    blobs_url = Column(Text)
    branches_url = Column(Text)
    clone_url = Column(Text)
    collaborators_url = Column(Text)
    comments_url = Column(Text)
    commits_url = Column(Text)
    compare_url = Column(Text)
    contents_url = Column(Text)
    contributors_url = Column(Text)
    deployments_url = Column(Text)
    downloads_url = Column(Text)
    events_url = Column(Text)
    forks_url = Column(Text)
    git_commits_url = Column(Text)
    git_refs_url = Column(Text)
    git_tags_url = Column(Text)
    git_url = Column(Text)
    hooks_url = Column(Text)
    issue_comment_url = Column(Text)
    issue_events_url = Column(Text)
    issues_url = Column(Text)
    keys_url = Column(Text)
    labels_url = Column(Text)
    languages_url = Column(Text)
    merges_url = Column(Text)
    milestones_url = Column(Text)
    notifications_url = Column(Text)
    pulls_url = Column(Text)
    releases_url = Column(Text)
    ssh_url = Column(Text)
    stargazers_url = Column(Text)
    statuses_url = Column(Text)
    subscribers_url = Column(Text)
    subscription_url = Column(Text)
    tags_url = Column(Text)
    teams_url = Column(Text)
    trees_url = Column(Text)
    
    # Repository metadata
    homepage = Column(String(255))
    size = Column(Integer)
    stargazers_count = Column(Integer)
    watchers_count = Column(Integer)
    language = Column(String(100))
    has_issues = Column(Boolean, default=True)
    has_projects = Column(Boolean, default=True)
    has_wiki = Column(Boolean, default=True)
    has_pages = Column(Boolean, default=False)
    forks_count = Column(Integer)
    archived = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    open_issues_count = Column(Integer)
    license_key = Column(String(50))
    allow_forking = Column(Boolean, default=True)
    is_template = Column(Boolean, default=False)
    topics = Column(ARRAY(Text))
    visibility = Column(String(20), default="public")
    default_branch = Column(String(255), default="main")
    temp_clone_token = Column(String(255))
    allow_squash_merge = Column(Boolean, default=True)
    allow_merge_commit = Column(Boolean, default=True)
    allow_rebase_merge = Column(Boolean, default=True)
    allow_auto_merge = Column(Boolean, default=False)
    delete_branch_on_merge = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    github_created_at = Column(DateTime(timezone=True))
    github_updated_at = Column(DateTime(timezone=True))
    github_pushed_at = Column(DateTime(timezone=True))
    
    # Relationships
    owner = relationship("User", back_populates="owned_repositories")
    organization = relationship("Organization", back_populates="repositories")
    collaborators = relationship("RepositoryCollaborator", back_populates="repository")
    webhook_events = relationship("WebhookEvent", back_populates="repository")
    repository_events = relationship("RepositoryEvent", back_populates="repository")
    member_events = relationship("MemberEvent", back_populates="repository")
    security_events = relationship("SecurityEvent", back_populates="repository")
    code_events = relationship("CodeEvent", back_populates="repository")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('github_id > 0', name='repo_github_id_check'),
        CheckConstraint("visibility IN ('public', 'private', 'internal')", name='repo_visibility_check'),
        Index('idx_repositories_full_name', 'full_name'),
        Index('idx_repositories_owner', 'owner_id'),
        Index('idx_repositories_org', 'organization_id'),
    )


class Installation(Base):
    """Installation model based on webhook_models/common/installation.py"""
    
    __tablename__ = "installations"
    
    id = Column(Integer, primary_key=True)
    github_id = Column(BigInteger, unique=True, nullable=False)
    app_id = Column(Integer, nullable=False)
    app_slug = Column(String(255))
    target_id = Column(Integer)
    target_type = Column(String(50))
    repository_selection = Column(String(20))
    access_tokens_url = Column(Text)
    repositories_url = Column(Text)
    html_url = Column(Text)
    permissions = Column(JSONB)
    events = Column(ARRAY(Text))
    single_file_name = Column(String(255))
    has_multiple_single_files = Column(Boolean, default=False)
    single_file_paths = Column(ARRAY(Text))
    suspended_by_id = Column(Integer, ForeignKey("users.id"))
    suspended_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    suspended_by = relationship("User", back_populates="installations_suspended")
    webhook_events = relationship("WebhookEvent", back_populates="installation")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('github_id > 0', name='install_github_id_check'),
        CheckConstraint("repository_selection IN ('all', 'selected')", name='install_repo_selection_check'),
    )


class WebhookEvent(Base):
    """Main webhook events table storing all GitHub webhook events"""
    
    __tablename__ = "webhook_events"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid())
    delivery_id = Column(String(255), unique=True)
    event_type = Column(String(100), nullable=False)
    event_action = Column(String(100))
    
    # Foreign keys
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    installation_id = Column(Integer, ForeignKey("installations.id"))
    
    # Event metadata
    event_timestamp = Column(DateTime(timezone=True), nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    processing_error = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Store complete payload as JSONB
    payload = Column(JSONB, nullable=False)
    headers = Column(JSONB)
    
    # Computed fields for performance
    sender_login = Column(String(255))
    repository_name = Column(String(255))
    organization_login = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="webhook_events")
    repository = relationship("Repository", back_populates="webhook_events")
    sender = relationship("User", back_populates="sent_events")
    installation = relationship("Installation", back_populates="webhook_events")
    
    # Specialized event relationships
    repository_event = relationship("RepositoryEvent", back_populates="webhook_event", uselist=False)
    member_event = relationship("MemberEvent", back_populates="webhook_event", uselist=False)
    security_event = relationship("SecurityEvent", back_populates="webhook_event", uselist=False)
    code_event = relationship("CodeEvent", back_populates="webhook_event", uselist=False)
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint(
            """event_type IN (
                'member', 'repository', 'push', 'issues', 'pull_request', 
                'team', 'fork', 'create', 'delete', 'issue_comment',
                'pull_request_review', 'ping', 'installation', 'organization',
                'code_scanning_alert', 'dependabot_alert', 'secret_scanning_alert',
                'meta', 'personal_access_token_request'
            )""",
            name='event_type_check'
        ),
        Index('idx_webhook_events_timestamp', 'event_timestamp'),
        Index('idx_webhook_events_type_timestamp', 'event_type', 'event_timestamp'),
        Index('idx_webhook_events_repo_timestamp', 'repository_id', 'event_timestamp'),
        Index('idx_webhook_events_org_timestamp', 'organization_id', 'event_timestamp'),
        Index('idx_webhook_events_sender', 'sender_id'),
        Index('idx_webhook_events_processed', 'processed', 'received_at'),
        Index('idx_webhook_events_delivery', 'delivery_id'),
        Index('idx_webhook_events_payload_gin', 'payload', postgresql_using='gin'),
    )