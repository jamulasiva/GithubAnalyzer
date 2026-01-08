"""
GitHub Webhook Models

Pydantic models for parsing GitHub webhook payloads.
Each event type has its own module with specific models.
Common models are located in the `common` package.

This package provides comprehensive webhook parsing for GitHub events,
equivalent to XMLBeans functionality for Java but using Pydantic.

Usage:
    from webhook_models import parse_webhook_payload
    from webhook_models.utils import validate_github_signature
    
    # Validate signature
    if validate_github_signature(payload_body, signature, secret):
        # Parse webhook payload
        event = parse_webhook_payload(payload_dict, "member", "added")
        
    # Or use specific model directly
    from webhook_models import MemberAddedEvent
    event = MemberAddedEvent(**payload_dict)
"""

from .common.base import WebhookHeaders, WebhookBase
from .common.user import User, GitUser, RepositoryOwner
from .common.repository import Repository, RepositoryLicense
from .common.organization import Organization, Membership
from .common.installation import Installation, GitHubApp, AppPermissions, Enterprise
from .common.git import Commit, Pusher
from .common.issues import (
    Label, Reactions, Milestone, Comment, Review, Issue, 
    PullRequest, PullRequestBranch, Team
)
from .common.security import (
    Rule, Tool, Location, CodeScanningInstance, CodeScanningAlert,
    DependabotAlert, SecretScanningAlert
)

# Event models
from .member_added import MemberAddedEvent
from .member_permission_changed import MemberEditedEvent
from .repository_created import RepositoryCreatedEvent
from .repository_publicized import RepositoryPublicizedEvent
from .push import PushEvent
from .issues_opened import IssuesOpenedEvent
from .pull_request_opened import PullRequestOpenedEvent
from .team_member_added import TeamMemberAddedEvent
from .fork import ForkEvent
from .create import CreateEvent
from .delete import DeleteEvent
from .issue_comment import IssueCommentEvent
from .pull_request_review import PullRequestReviewEvent
from .ping import PingEvent, Hook
from .installation import InstallationEvent
from .organization import OrganizationEvent
from .code_scanning_alert import CodeScanningAlertEvent
from .dependabot_alert import DependabotAlertEvent
from .secret_scanning_alert import SecretScanningAlertEvent
from .meta import MetaEvent
from .personal_access_token_request import PersonalAccessTokenRequestEvent

# Utilities
from .utils import (
    validate_github_signature, 
    get_webhook_model_class, 
    parse_webhook_payload,
    WEBHOOK_EVENT_MAP
)

# Utilities
from .utils import validate_github_signature, parse_webhook_payload, get_webhook_model_class

__all__ = [
    # Common models
    "WebhookHeaders",
    "WebhookBase", 
    "User",
    "GitUser",
    "RepositoryOwner",
    "Repository",
    "RepositoryLicense",
    "Organization", 
    "Installation",
    "GitHubApp",
    "AppPermissions",
    "Enterprise",
    "Commit",
    "Pusher",
    
    # Event models
    "MemberAddedEvent",
    "RepositoryCreatedEvent", 
    "PushEvent",
    
    # Utilities
    "validate_github_signature",
    "parse_webhook_payload",
    "get_webhook_model_class",
]