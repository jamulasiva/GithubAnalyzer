"""
Entity service for managing GitHub entities (users, repositories, organizations).
Handles creation, updates, and relationships between entities.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Import local webhook models for type hints
from app.webhook_models.common.user import User as WebhookUser
from app.webhook_models.common.repository import Repository as WebhookRepository
from app.webhook_models.common.organization import Organization as WebhookOrganization
from app.webhook_models.common.installation import Installation as WebhookInstallation

from app.core.logging_config import log_database_operation
from app.models.core import User, Repository, Organization, Installation

logger = logging.getLogger(__name__)


class EntityService:
    """Service for managing GitHub entities and their relationships."""
    
    @staticmethod
    def _parse_github_datetime(date_str: Optional[str]) -> Optional[datetime]:
        """Parse GitHub datetime string to datetime object."""
        if not date_str:
            return None
        
        try:
            # Remove 'Z' and add timezone info
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            logger.warning(f"Failed to parse datetime: {date_str}")
            return None
    
    async def ensure_user(self, db: Session, webhook_user: WebhookUser) -> int:
        """
        Ensure user exists in database, create or update as needed.
        
        Args:
            db: Database session
            webhook_user: User data from webhook
            
        Returns:
            User database ID
        """
        try:
            # Check if user exists
            existing_user = db.query(User).filter(User.github_id == webhook_user.id).first()
            
            if existing_user:
                # Update existing user with latest data
                self._update_user_from_webhook(existing_user, webhook_user)
                db.commit()
                logger.debug(f"Updated existing user: {webhook_user.login}")
                return existing_user.id
            
            # Create new user
            new_user = self._create_user_from_webhook(webhook_user)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"Created new user: {webhook_user.login}")
            return new_user.id
            
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Integrity error creating user {webhook_user.login}: {e}")
            # Try to find existing user again (race condition)
            existing_user = db.query(User).filter(User.github_id == webhook_user.id).first()
            if existing_user:
                return existing_user.id
            raise
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ensure user {webhook_user.login}: {e}")
            raise
    
    def _create_user_from_webhook(self, webhook_user: WebhookUser) -> User:
        """Create User model from webhook data."""
        return User(
            github_id=webhook_user.id,
            login=webhook_user.login,
            node_id=webhook_user.node_id,
            avatar_url=webhook_user.avatar_url,
            gravatar_id=webhook_user.gravatar_id or "",
            url=webhook_user.url,
            html_url=webhook_user.html_url,
            followers_url=getattr(webhook_user, 'followers_url', None),
            following_url=getattr(webhook_user, 'following_url', None),
            gists_url=getattr(webhook_user, 'gists_url', None),
            starred_url=getattr(webhook_user, 'starred_url', None),
            subscriptions_url=getattr(webhook_user, 'subscriptions_url', None),
            organizations_url=getattr(webhook_user, 'organizations_url', None),
            repos_url=getattr(webhook_user, 'repos_url', None),
            events_url=getattr(webhook_user, 'events_url', None),
            received_events_url=getattr(webhook_user, 'received_events_url', None),
            type=webhook_user.type,
            site_admin=webhook_user.site_admin or False,
            name=getattr(webhook_user, 'name', None),
            company=getattr(webhook_user, 'company', None),
            blog=getattr(webhook_user, 'blog', None),
            location=getattr(webhook_user, 'location', None),
            email=getattr(webhook_user, 'email', None),
            hireable=getattr(webhook_user, 'hireable', None),
            bio=getattr(webhook_user, 'bio', None),
            twitter_username=getattr(webhook_user, 'twitter_username', None),
            public_repos=getattr(webhook_user, 'public_repos', None),
            public_gists=getattr(webhook_user, 'public_gists', None),
            followers=getattr(webhook_user, 'followers', None),
            following=getattr(webhook_user, 'following', None),
            github_created_at=self._parse_github_datetime(getattr(webhook_user, 'created_at', None)),
            github_updated_at=self._parse_github_datetime(getattr(webhook_user, 'updated_at', None))
        )
    
    def _update_user_from_webhook(self, user: User, webhook_user: WebhookUser):
        """Update existing User model with webhook data."""
        user.login = webhook_user.login
        user.node_id = webhook_user.node_id
        user.avatar_url = webhook_user.avatar_url
        user.gravatar_id = webhook_user.gravatar_id or ""
        user.url = webhook_user.url
        user.html_url = webhook_user.html_url
        user.type = webhook_user.type
        user.site_admin = webhook_user.site_admin or False
        
        # Update optional fields if present
        if hasattr(webhook_user, 'name'):
            user.name = webhook_user.name
        if hasattr(webhook_user, 'email'):
            user.email = webhook_user.email
        # Add other fields as needed
    
    async def ensure_repository(self, db: Session, webhook_repo: WebhookRepository) -> int:
        """
        Ensure repository exists in database, create or update as needed.
        
        Args:
            db: Database session
            webhook_repo: Repository data from webhook
            
        Returns:
            Repository database ID
        """
        try:
            # Check if repository exists
            existing_repo = db.query(Repository).filter(
                Repository.github_id == webhook_repo.id
            ).first()
            
            if existing_repo:
                # Update existing repository
                self._update_repository_from_webhook(existing_repo, webhook_repo)
                db.commit()
                logger.debug(f"Updated existing repository: {webhook_repo.full_name}")
                return existing_repo.id
            
            # Create new repository
            new_repo = self._create_repository_from_webhook(webhook_repo)
            
            # Handle owner relationship
            if webhook_repo.owner:
                owner_id = await self.ensure_user(db, webhook_repo.owner)
                new_repo.owner_id = owner_id
            
            db.add(new_repo)
            db.commit()
            db.refresh(new_repo)
            
            logger.info(f"Created new repository: {webhook_repo.full_name}")
            return new_repo.id
            
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Integrity error creating repository {webhook_repo.full_name}: {e}")
            # Try to find existing repository again
            existing_repo = db.query(Repository).filter(
                Repository.github_id == webhook_repo.id
            ).first()
            if existing_repo:
                return existing_repo.id
            raise
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ensure repository {webhook_repo.full_name}: {e}")
            raise
    
    def _create_repository_from_webhook(self, webhook_repo: WebhookRepository) -> Repository:
        """Create Repository model from webhook data."""
        return Repository(
            github_id=webhook_repo.id,
            node_id=webhook_repo.node_id,
            name=webhook_repo.name,
            full_name=webhook_repo.full_name,
            private=webhook_repo.private,
            html_url=webhook_repo.html_url,
            description=webhook_repo.description,
            fork=webhook_repo.fork,
            url=webhook_repo.url,
            clone_url=getattr(webhook_repo, 'clone_url', None),
            git_url=getattr(webhook_repo, 'git_url', None),
            ssh_url=getattr(webhook_repo, 'ssh_url', None),
            homepage=getattr(webhook_repo, 'homepage', None),
            size=getattr(webhook_repo, 'size', None),
            stargazers_count=getattr(webhook_repo, 'stargazers_count', None),
            watchers_count=getattr(webhook_repo, 'watchers_count', None),
            language=getattr(webhook_repo, 'language', None),
            has_issues=getattr(webhook_repo, 'has_issues', True),
            has_projects=getattr(webhook_repo, 'has_projects', True),
            has_wiki=getattr(webhook_repo, 'has_wiki', True),
            has_pages=getattr(webhook_repo, 'has_pages', False),
            forks_count=getattr(webhook_repo, 'forks_count', None),
            archived=getattr(webhook_repo, 'archived', False),
            disabled=getattr(webhook_repo, 'disabled', False),
            open_issues_count=getattr(webhook_repo, 'open_issues_count', None),
            license_key=None if not hasattr(webhook_repo, 'license') or not webhook_repo.license else webhook_repo.license.get('key'),
            allow_forking=getattr(webhook_repo, 'allow_forking', True),
            is_template=getattr(webhook_repo, 'is_template', False),
            topics=getattr(webhook_repo, 'topics', []),
            visibility=getattr(webhook_repo, 'visibility', 'public'),
            default_branch=getattr(webhook_repo, 'default_branch', 'main'),
            github_created_at=self._parse_github_datetime(getattr(webhook_repo, 'created_at', None)),
            github_updated_at=self._parse_github_datetime(getattr(webhook_repo, 'updated_at', None)),
            github_pushed_at=self._parse_github_datetime(getattr(webhook_repo, 'pushed_at', None))
        )
    
    def _update_repository_from_webhook(self, repo: Repository, webhook_repo: WebhookRepository):
        """Update existing Repository model with webhook data."""
        repo.name = webhook_repo.name
        repo.full_name = webhook_repo.full_name
        repo.private = webhook_repo.private
        repo.description = webhook_repo.description
        repo.fork = webhook_repo.fork
        repo.archived = getattr(webhook_repo, 'archived', False)
        repo.disabled = getattr(webhook_repo, 'disabled', False)
        # Add other fields as needed
    
    async def ensure_organization(self, db: Session, webhook_org: WebhookOrganization) -> int:
        """
        Ensure organization exists in database, create or update as needed.
        
        Args:
            db: Database session
            webhook_org: Organization data from webhook
            
        Returns:
            Organization database ID
        """
        try:
            # Check if organization exists
            existing_org = db.query(Organization).filter(
                Organization.github_id == webhook_org.id
            ).first()
            
            if existing_org:
                # Update existing organization
                self._update_organization_from_webhook(existing_org, webhook_org)
                db.commit()
                logger.debug(f"Updated existing organization: {webhook_org.login}")
                return existing_org.id
            
            # Create new organization
            new_org = self._create_organization_from_webhook(webhook_org)
            db.add(new_org)
            db.commit()
            db.refresh(new_org)
            
            logger.info(f"Created new organization: {webhook_org.login}")
            return new_org.id
            
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Integrity error creating organization {webhook_org.login}: {e}")
            # Try to find existing organization again
            existing_org = db.query(Organization).filter(
                Organization.github_id == webhook_org.id
            ).first()
            if existing_org:
                return existing_org.id
            raise
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ensure organization {webhook_org.login}: {e}")
            raise
    
    def _create_organization_from_webhook(self, webhook_org: WebhookOrganization) -> Organization:
        """Create Organization model from webhook data."""
        return Organization(
            github_id=webhook_org.id,
            login=webhook_org.login,
            node_id=webhook_org.node_id,
            url=webhook_org.url,
            repos_url=webhook_org.repos_url,
            events_url=webhook_org.events_url,
            hooks_url=webhook_org.hooks_url,
            issues_url=webhook_org.issues_url,
            members_url=webhook_org.members_url,
            public_members_url=webhook_org.public_members_url,
            avatar_url=webhook_org.avatar_url,
            description=webhook_org.description or "",
            name=getattr(webhook_org, 'name', None),
            company=getattr(webhook_org, 'company', None),
            blog=getattr(webhook_org, 'blog', None),
            location=getattr(webhook_org, 'location', None),
            email=getattr(webhook_org, 'email', None),
            twitter_username=getattr(webhook_org, 'twitter_username', None),
            is_verified=getattr(webhook_org, 'is_verified', False),
            has_organization_projects=getattr(webhook_org, 'has_organization_projects', None),
            has_repository_projects=getattr(webhook_org, 'has_repository_projects', None),
            public_repos=getattr(webhook_org, 'public_repos', None),
            public_gists=getattr(webhook_org, 'public_gists', None),
            followers=getattr(webhook_org, 'followers', None),
            following=getattr(webhook_org, 'following', None),
            html_url=getattr(webhook_org, 'html_url', None),
            type=webhook_org.type or "Organization",
            github_created_at=self._parse_github_datetime(getattr(webhook_org, 'created_at', None)),
            github_updated_at=self._parse_github_datetime(getattr(webhook_org, 'updated_at', None))
        )
    
    def _update_organization_from_webhook(self, org: Organization, webhook_org: WebhookOrganization):
        """Update existing Organization model with webhook data."""
        org.login = webhook_org.login
        org.description = webhook_org.description or ""
        org.avatar_url = webhook_org.avatar_url
        # Add other fields as needed
    
    async def ensure_installation(self, db: Session, webhook_installation: WebhookInstallation) -> int:
        """
        Ensure installation exists in database, create or update as needed.
        
        Args:
            db: Database session
            webhook_installation: Installation data from webhook
            
        Returns:
            Installation database ID
        """
        try:
            # Check if installation exists
            existing_installation = db.query(Installation).filter(
                Installation.github_id == webhook_installation.id
            ).first()
            
            if existing_installation:
                # Update existing installation
                self._update_installation_from_webhook(existing_installation, webhook_installation)
                db.commit()
                logger.debug(f"Updated existing installation: {webhook_installation.id}")
                return existing_installation.id
            
            # Create new installation
            new_installation = self._create_installation_from_webhook(webhook_installation)
            db.add(new_installation)
            db.commit()
            db.refresh(new_installation)
            
            logger.info(f"Created new installation: {webhook_installation.id}")
            return new_installation.id
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ensure installation {webhook_installation.id}: {e}")
            raise
    
    def _create_installation_from_webhook(self, webhook_installation: WebhookInstallation) -> Installation:
        """Create Installation model from webhook data."""
        # Handle permissions - convert Pydantic model to dict if needed
        permissions = getattr(webhook_installation, 'permissions', {})
        if hasattr(permissions, 'dict'):
            permissions = permissions.dict()
        elif hasattr(permissions, '__dict__'):
            permissions = permissions.__dict__
            
        return Installation(
            github_id=webhook_installation.id,
            app_id=webhook_installation.app_id,
            app_slug=getattr(webhook_installation, 'app_slug', None),
            target_id=getattr(webhook_installation, 'target_id', None),
            target_type=getattr(webhook_installation, 'target_type', None),
            repository_selection=getattr(webhook_installation, 'repository_selection', None),
            access_tokens_url=getattr(webhook_installation, 'access_tokens_url', None),
            repositories_url=getattr(webhook_installation, 'repositories_url', None),
            html_url=getattr(webhook_installation, 'html_url', None),
            permissions=permissions,
            events=getattr(webhook_installation, 'events', [])
        )
    
    def _update_installation_from_webhook(self, installation: Installation, webhook_installation: WebhookInstallation):
        """Update existing Installation model with webhook data."""
        # Handle permissions - convert Pydantic model to dict if needed  
        permissions = getattr(webhook_installation, 'permissions', {})
        if hasattr(permissions, 'dict'):
            permissions = permissions.dict()
        elif hasattr(permissions, '__dict__'):
            permissions = permissions.__dict__
        
        installation.permissions = permissions
        installation.events = getattr(webhook_installation, 'events', [])
        # Add other fields as needed


# Global entity service instance
entity_service = EntityService()