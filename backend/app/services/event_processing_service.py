"""
Event processing service for creating specialized event records.
Handles the extraction and storage of structured data from webhook events.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.core import WebhookEvent
from app.models.events import (
    RepositoryEvent, MemberEvent, SecurityEvent, CodeEvent,
    OrganizationMembership, RepositoryCollaborator
)

logger = logging.getLogger(__name__)


class EventProcessingService:
    """Service for processing webhook events into specialized event records."""
    
    def __init__(self):
        pass
    
    async def process_webhook_event(self, db: Session, webhook_event: WebhookEvent) -> bool:
        """
        Process a webhook event and create specialized event records.
        
        Args:
            db: Database session
            webhook_event: Stored webhook event to process
            
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            event_type = webhook_event.event_type
            payload = webhook_event.payload
            
            logger.info(f"Processing {event_type} event (ID: {webhook_event.id})")
            
            # Route to appropriate processing function
            if event_type == "repository":
                await self._process_repository_event(db, webhook_event, payload)
            elif event_type == "member":
                await self._process_member_event(db, webhook_event, payload)
            elif event_type == "organization":
                await self._process_organization_event(db, webhook_event, payload)
            elif event_type in ["code_scanning_alert", "dependabot_alert", "secret_scanning_alert"]:
                await self._process_security_event(db, webhook_event, payload)
            elif event_type in ["push", "create", "delete", "fork"]:
                await self._process_code_event(db, webhook_event, payload)
            else:
                logger.debug(f"No specialized processing for event type: {event_type}")
            
            # Mark webhook event as processed
            webhook_event.processed = True
            webhook_event.processed_at = datetime.now(timezone.utc)
            db.commit()
            
            logger.info(f"Successfully processed {event_type} event (ID: {webhook_event.id})")
            return True
            
        except Exception as e:
            db.rollback()
            webhook_event.processing_error = str(e)
            webhook_event.retry_count = (webhook_event.retry_count or 0) + 1
            db.commit()
            logger.error(f"Failed to process event {webhook_event.id}: {e}")
            return False
    
    async def _process_repository_event(
        self, 
        db: Session, 
        webhook_event: WebhookEvent, 
        payload: Dict[str, Any]
    ):
        """Process repository events (created, deleted, archived, etc.)"""
        action = payload.get("action", "")
        
        # Create repository event record
        repo_event = RepositoryEvent(
            webhook_event_id=webhook_event.id,
            repository_id=webhook_event.repository_id,
            action=action,
            changes=payload.get("changes", {}),
            event_timestamp=webhook_event.event_timestamp
        )
        
        db.add(repo_event)
        logger.debug(f"Created repository event: {action}")
    
    async def _process_member_event(
        self, 
        db: Session, 
        webhook_event: WebhookEvent, 
        payload: Dict[str, Any]
    ):
        """Process member events (added, removed, permission changes)"""
        action = payload.get("action", "")
        member_data = payload.get("member", {})
        membership_data = payload.get("membership", {})
        
        # Extract member information from different payload structures
        member_github_id = None
        member_login = None
        permission_level = payload.get("permission")
        
        # Get member info from member field (repository member events)
        if member_data:
            member_github_id = member_data.get("id")
            member_login = member_data.get("login")
        
        # Get member info from membership field (organization member events)
        elif membership_data and membership_data.get("user"):
            user = membership_data["user"]
            member_github_id = user.get("id")
            member_login = user.get("login")
            # Get role from membership for org events
            if not permission_level:
                permission_level = membership_data.get("role", "member")
        
        # Find the actual user ID in our database
        member_id = None
        if member_github_id:
            from app.models.core import User
            user_record = db.query(User).filter(User.github_id == member_github_id).first()
            if user_record:
                member_id = user_record.id
            else:
                logger.warning(f"User with GitHub ID {member_github_id} not found in database")
        
        # Create member event record
        member_event = MemberEvent(
            webhook_event_id=webhook_event.id,
            repository_id=webhook_event.repository_id,
            organization_id=webhook_event.organization_id,
            member_id=member_id,
            action=action,
            permission_level=permission_level,
            changes=payload.get("changes", {}),
            event_timestamp=webhook_event.event_timestamp
        )
        
        db.add(member_event)
        
        # Handle relationship updates based on action and context
        if member_id:
            # Organization membership events
            if action in ["member_added", "added"] and webhook_event.organization_id:
                await self._update_organization_membership(
                    db, webhook_event.organization_id, member_id, permission_level or "member", "active"
                )
                logger.info(f"Added organization membership: org={webhook_event.organization_id}, user={member_id}")
            
            elif action in ["member_removed", "removed"] and webhook_event.organization_id:
                await self._remove_organization_membership(
                    db, webhook_event.organization_id, member_id
                )
                logger.info(f"Removed organization membership: org={webhook_event.organization_id}, user={member_id}")
            
            # Repository collaborator events  
            if action == "added" and webhook_event.repository_id:
                await self._update_repository_collaborator(
                    db, webhook_event.repository_id, member_id, permission_level or "read"
                )
                logger.info(f"Added repository collaborator: repo={webhook_event.repository_id}, user={member_id}")
            
            elif action == "removed" and webhook_event.repository_id:
                await self._remove_repository_collaborator(
                    db, webhook_event.repository_id, member_id
                )
                logger.info(f"Removed repository collaborator: repo={webhook_event.repository_id}, user={member_id}")
        
        logger.debug(f"Created member event: {action}, member_id: {member_id}")
    
    async def _process_organization_event(
        self, 
        db: Session, 
        webhook_event: WebhookEvent, 
        payload: Dict[str, Any]
    ):
        """Process organization events"""
        action = payload.get("action", "")
        
        # Organization events are typically membership-related
        # Process them as member events
        await self._process_member_event(db, webhook_event, payload)
        
        logger.debug(f"Created organization event: {action}")
    
    async def _process_security_event(
        self, 
        db: Session, 
        webhook_event: WebhookEvent, 
        payload: Dict[str, Any]
    ):
        """Process security events (code scanning, dependabot, secret scanning)"""
        action = payload.get("action", "")
        alert_data = payload.get("alert", {})
        
        # Extract security-specific fields
        alert_number = alert_data.get("number")
        state = alert_data.get("state")
        severity = None
        rule_id = None
        tool_name = None
        secret_type = None
        
        # Extract severity based on alert type
        if webhook_event.event_type == "code_scanning_alert":
            rule = alert_data.get("rule", {})
            severity = rule.get("severity")
            rule_id = rule.get("id")
            tool_name = alert_data.get("tool", {}).get("name")
        elif webhook_event.event_type == "dependabot_alert":
            security_advisory = alert_data.get("security_advisory", {})
            severity = security_advisory.get("severity")
        elif webhook_event.event_type == "secret_scanning_alert":
            secret_type = alert_data.get("secret_type")
        
        # Create security event record
        security_event = SecurityEvent(
            webhook_event_id=webhook_event.id,
            repository_id=webhook_event.repository_id,
            alert_type=webhook_event.event_type,
            alert_number=alert_number,
            action=action,
            state=state,
            severity=severity,
            rule_id=rule_id,
            tool_name=tool_name,
            secret_type=secret_type,
            event_timestamp=webhook_event.event_timestamp
        )
        
        db.add(security_event)
        logger.debug(f"Created security event: {webhook_event.event_type} - {action}")
    
    async def _process_code_event(
        self, 
        db: Session, 
        webhook_event: WebhookEvent, 
        payload: Dict[str, Any]
    ):
        """Process code events (push, create, delete, fork)"""
        event_type = webhook_event.event_type
        
        # Extract code-specific fields
        ref_name = None
        ref_type = None
        before_sha = None
        after_sha = None
        commits_count = 0
        distinct_commits_count = 0
        forced = False
        
        if event_type == "push":
            ref_name = payload.get("ref", "").replace("refs/heads/", "").replace("refs/tags/", "")
            before_sha = payload.get("before")
            after_sha = payload.get("after")
            commits = payload.get("commits", [])
            commits_count = len(commits)
            distinct_commits_count = len(set(commit.get("id") for commit in commits if commit.get("id")))
            forced = payload.get("forced", False)
            ref_type = "branch"  # Most pushes are to branches
            
        elif event_type in ["create", "delete"]:
            ref_name = payload.get("ref")
            ref_type = payload.get("ref_type")  # "branch" or "tag"
            
        elif event_type == "fork":
            # Fork events don't have ref information
            pass
        
        # Create code event record
        code_event = CodeEvent(
            webhook_event_id=webhook_event.id,
            repository_id=webhook_event.repository_id,
            event_type=event_type,
            ref_name=ref_name,
            ref_type=ref_type,
            before_sha=before_sha,
            after_sha=after_sha,
            commits_count=commits_count,
            distinct_commits_count=distinct_commits_count,
            forced=forced,
            event_timestamp=webhook_event.event_timestamp
        )
        
        db.add(code_event)
        logger.debug(f"Created code event: {event_type}")
    
    async def _update_organization_membership(
        self,
        db: Session,
        organization_id: int,
        user_id: int,
        role: str = "member",
        state: str = "active"
    ):
        """Update or create organization membership record."""
        try:
            # Check if membership already exists
            membership = db.query(OrganizationMembership).filter(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.user_id == user_id
            ).first()
            
            if membership:
                # Update existing membership
                membership.role = role
                membership.state = state
                membership.updated_at = datetime.now(timezone.utc)
                logger.debug(f"Updated existing organization membership: org={organization_id}, user={user_id}")
            else:
                # Create new membership
                membership = OrganizationMembership(
                    organization_id=organization_id,
                    user_id=user_id,
                    role=role,
                    state=state
                )
                db.add(membership)
                logger.debug(f"Created new organization membership: org={organization_id}, user={user_id}")
            
        except Exception as e:
            logger.error(f"Failed to update organization membership: {e}")
    
    async def _remove_organization_membership(
        self,
        db: Session,
        organization_id: int,
        user_id: int
    ):
        """Remove organization membership record."""
        try:
            membership = db.query(OrganizationMembership).filter(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.user_id == user_id
            ).first()
            
            if membership:
                db.delete(membership)
                logger.debug(f"Removed organization membership: org={organization_id}, user={user_id}")
            
        except Exception as e:
            logger.error(f"Failed to remove organization membership: {e}")
    
    async def _update_repository_collaborator(
        self,
        db: Session,
        repository_id: int,
        user_id: int,
        permission: str = "read"
    ):
        """Update or create repository collaborator record."""
        try:
            # Check if collaborator already exists
            collaborator = db.query(RepositoryCollaborator).filter(
                RepositoryCollaborator.repository_id == repository_id,
                RepositoryCollaborator.user_id == user_id
            ).first()
            
            if collaborator:
                # Update existing collaborator
                collaborator.permission = permission
                collaborator.updated_at = datetime.now(timezone.utc)
                logger.debug(f"Updated existing repository collaborator: repo={repository_id}, user={user_id}")
            else:
                # Create new collaborator
                collaborator = RepositoryCollaborator(
                    repository_id=repository_id,
                    user_id=user_id,
                    permission=permission
                )
                db.add(collaborator)
                logger.debug(f"Created new repository collaborator: repo={repository_id}, user={user_id}")
            
        except Exception as e:
            logger.error(f"Failed to update repository collaborator: {e}")
    
    async def _remove_repository_collaborator(
        self,
        db: Session,
        repository_id: int,
        user_id: int
    ):
        """Remove repository collaborator record."""
        try:
            collaborator = db.query(RepositoryCollaborator).filter(
                RepositoryCollaborator.repository_id == repository_id,
                RepositoryCollaborator.user_id == user_id
            ).first()
            
            if collaborator:
                db.delete(collaborator)
                logger.debug(f"Removed repository collaborator: repo={repository_id}, user={user_id}")
            
        except Exception as e:
            logger.error(f"Failed to remove repository collaborator: {e}")


# Global service instance
event_processing_service = EventProcessingService()