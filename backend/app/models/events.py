"""
Specialized event models for different types of GitHub webhook events.
These provide structured storage for specific event types while maintaining 
the full payload in the main webhook_events table.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, 
    ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RepositoryEvent(Base):
    """Repository events (create, delete, visibility changes, etc.)"""
    
    __tablename__ = "repository_events"
    
    id = Column(Integer, primary_key=True)
    webhook_event_id = Column(Integer, ForeignKey("webhook_events.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    action = Column(String(100), nullable=False)
    changes = Column(JSONB)  # Store what changed (for edited events)
    event_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    webhook_event = relationship("WebhookEvent", back_populates="repository_event")
    repository = relationship("Repository", back_populates="repository_events")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """action IN (
                'created', 'deleted', 'archived', 'unarchived', 'edited', 
                'publicized', 'privatized', 'transferred'
            )""",
            name='repo_event_action_check'
        ),
        Index('idx_repository_events_timestamp', 'event_timestamp'),
    )


class MemberEvent(Base):
    """Member/collaboration events"""
    
    __tablename__ = "member_events"
    
    id = Column(Integer, primary_key=True)
    webhook_event_id = Column(Integer, ForeignKey("webhook_events.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    member_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    permission_level = Column(String(50))
    changes = Column(JSONB)  # Store permission changes
    event_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    webhook_event = relationship("WebhookEvent", back_populates="member_event")
    repository = relationship("Repository", back_populates="member_events")
    organization = relationship("Organization")
    member = relationship("User")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """action IN (
                'added', 'removed', 'edited', 'invited', 'member_invited', 
                'member_added', 'member_removed'
            )""",
            name='member_event_action_check'
        ),
        Index('idx_member_events_timestamp', 'event_timestamp'),
    )


class SecurityEvent(Base):
    """Security events (alerts, scanning, etc.)"""
    
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True)
    webhook_event_id = Column(Integer, ForeignKey("webhook_events.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    alert_type = Column(String(100), nullable=False)
    alert_number = Column(Integer)
    action = Column(String(100), nullable=False)
    state = Column(String(50))
    severity = Column(String(50))
    rule_id = Column(String(255))
    tool_name = Column(String(100))
    secret_type = Column(String(100))
    event_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    webhook_event = relationship("WebhookEvent", back_populates="security_event")
    repository = relationship("Repository", back_populates="security_events")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """alert_type IN (
                'code_scanning_alert', 'dependabot_alert', 'secret_scanning_alert'
            )""",
            name='security_alert_type_check'
        ),
        CheckConstraint(
            """action IN (
                'created', 'fixed', 'dismissed', 'reopened', 'resolved', 'revoked'
            )""",
            name='security_action_check'
        ),
        Index('idx_security_events_timestamp', 'event_timestamp'),
    )


class CodeEvent(Base):
    """Code activity events (push, commits, branches, tags)"""
    
    __tablename__ = "code_events"
    
    id = Column(Integer, primary_key=True)
    webhook_event_id = Column(Integer, ForeignKey("webhook_events.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    event_type = Column(String(100), nullable=False)
    ref_name = Column(String(255))  # branch/tag name
    ref_type = Column(String(20))   # 'branch' or 'tag'
    before_sha = Column(String(255))
    after_sha = Column(String(255))
    commits_count = Column(Integer, default=0)
    distinct_commits_count = Column(Integer, default=0)
    forced = Column(Boolean, default=False)
    event_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    webhook_event = relationship("WebhookEvent", back_populates="code_event")
    repository = relationship("Repository", back_populates="code_events")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """event_type IN ('push', 'create', 'delete', 'fork')""",
            name='code_event_type_check'
        ),
        CheckConstraint(
            """ref_type IN ('branch', 'tag') OR ref_type IS NULL""",
            name='code_ref_type_check'
        ),
        Index('idx_code_events_timestamp', 'event_timestamp'),
    )


class OrganizationMembership(Base):
    """Organization memberships tracking"""
    
    __tablename__ = "organization_memberships"
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50), nullable=False, default="member")
    state = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="memberships")
    user = relationship("User", back_populates="memberships")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """role IN ('member', 'admin', 'billing_manager')""",
            name='membership_role_check'
        ),
        CheckConstraint(
            """state IN ('active', 'pending')""",
            name='membership_state_check'
        ),
        Index('idx_org_memberships_unique', 'organization_id', 'user_id', unique=True),
    )


class RepositoryCollaborator(Base):
    """Repository collaborators tracking"""
    
    __tablename__ = "repository_collaborators"
    
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    permission = Column(String(50), nullable=False, default="read")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    repository = relationship("Repository", back_populates="collaborators")
    user = relationship("User", back_populates="collaborations")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            """permission IN ('read', 'write', 'admin', 'maintain', 'triage')""",
            name='collaborator_permission_check'
        ),
        Index('idx_repo_collaborators_unique', 'repository_id', 'user_id', unique=True),
    )