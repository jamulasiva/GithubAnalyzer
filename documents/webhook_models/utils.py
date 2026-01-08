"""Webhook utilities for GitHub webhook processing."""

import hashlib
import hmac
from typing import Dict, Type, Union

from .common.base import WebhookBase
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
from .ping import PingEvent
from .installation import InstallationEvent
from .organization import OrganizationEvent
from .code_scanning_alert import CodeScanningAlertEvent
from .dependabot_alert import DependabotAlertEvent
from .secret_scanning_alert import SecretScanningAlertEvent
from .meta import MetaEvent
from .personal_access_token_request import PersonalAccessTokenRequestEvent


# Webhook event routing map
WEBHOOK_EVENT_MAP: Dict[str, Dict[str, Type[WebhookBase]]] = {
    "member": {
        "added": MemberAddedEvent,
        "edited": MemberEditedEvent,
    },
    "repository": {
        "created": RepositoryCreatedEvent,
        "publicized": RepositoryPublicizedEvent,
    },
    "push": {
        None: PushEvent,  # Push events don't have actions
    },
    "issues": {
        "opened": IssuesOpenedEvent,
    },
    "pull_request": {
        "opened": PullRequestOpenedEvent,
    },
    "team": {
        "added_to_repository": TeamMemberAddedEvent,
    },
    "fork": {
        None: ForkEvent,  # Fork events don't have actions
    },
    "create": {
        None: CreateEvent,  # Create events don't have actions
    },
    "delete": {
        None: DeleteEvent,  # Delete events don't have actions
    },
    "issue_comment": {
        "created": IssueCommentEvent,
        "edited": IssueCommentEvent,
        "deleted": IssueCommentEvent,
    },
    "pull_request_review": {
        "submitted": PullRequestReviewEvent,
        "edited": PullRequestReviewEvent,
        "dismissed": PullRequestReviewEvent,
    },
    "ping": {
        None: PingEvent,  # Ping events don't have actions
    },
    "installation": {
        "created": InstallationEvent,
        "deleted": InstallationEvent,
        "suspend": InstallationEvent,
        "unsuspend": InstallationEvent,
        "new_permissions_accepted": InstallationEvent,
    },
    "organization": {
        "member_added": OrganizationEvent,
        "member_removed": OrganizationEvent,
        "member_invited": OrganizationEvent,
    },
    "code_scanning_alert": {
        "created": CodeScanningAlertEvent,
        "fixed": CodeScanningAlertEvent,
        "reopened": CodeScanningAlertEvent,
        "appeared_in_branch": CodeScanningAlertEvent,
        "closed_by_user": CodeScanningAlertEvent,
    },
    "dependabot_alert": {
        "created": DependabotAlertEvent,
        "dismissed": DependabotAlertEvent,
        "fixed": DependabotAlertEvent,
        "reintroduced": DependabotAlertEvent,
        "reopened": DependabotAlertEvent,
    },
    "secret_scanning_alert": {
        "created": SecretScanningAlertEvent,
        "resolved": SecretScanningAlertEvent,
        "reopened": SecretScanningAlertEvent,
        "revoked": SecretScanningAlertEvent,
    },
    "meta": {
        "deleted": MetaEvent,
    },
    "personal_access_token_request": {
        "created": PersonalAccessTokenRequestEvent,
        "approved": PersonalAccessTokenRequestEvent,
        "denied": PersonalAccessTokenRequestEvent,
        "cancelled": PersonalAccessTokenRequestEvent,
    },
    # Add more events as you create them
}


def validate_github_signature(
    payload_body: bytes, 
    signature_header: str, 
    webhook_secret: str
) -> bool:
    """
    Validate GitHub webhook signature.
    
    Args:
        payload_body: Raw webhook payload body
        signature_header: X-Hub-Signature-256 header value  
        webhook_secret: Your webhook secret
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header:
        return False
        
    try:
        # GitHub sends signature as 'sha256=<hash>'
        hash_object = hmac.new(
            webhook_secret.encode('utf-8'),
            payload_body, 
            hashlib.sha256
        )
        expected_signature = "sha256=" + hash_object.hexdigest()
        
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception:
        return False


def get_webhook_model_class(
    event_type: str, 
    action: Union[str, None] = None
) -> Type[WebhookBase]:
    """
    Get the appropriate Pydantic model class for a webhook event.
    
    Args:
        event_type: The X-GitHub-Event header value
        action: The action field from the webhook payload (if present)
        
    Returns:
        Pydantic model class for the event
        
    Raises:
        ValueError: If event type/action combination is not supported
    """
    if event_type not in WEBHOOK_EVENT_MAP:
        raise ValueError(f"Unsupported webhook event type: {event_type}")
    
    event_actions = WEBHOOK_EVENT_MAP[event_type]
    
    if action not in event_actions:
        raise ValueError(
            f"Unsupported action '{action}' for event type '{event_type}'. "
            f"Available actions: {list(event_actions.keys())}"
        )
    
    return event_actions[action]


def parse_webhook_payload(
    payload: dict, 
    event_type: str,
    action: Union[str, None] = None
) -> WebhookBase:
    """
    Parse a webhook payload into the appropriate Pydantic model.
    
    Args:
        payload: Parsed JSON webhook payload
        event_type: The X-GitHub-Event header value
        action: The action field from payload (if present)
        
    Returns:
        Parsed webhook event model
        
    Raises:
        ValueError: If event type/action is not supported
        ValidationError: If payload doesn't match expected schema
    """
    if action is None and "action" in payload:
        action = payload["action"]
    
    model_class = get_webhook_model_class(event_type, action)
    return model_class(**payload)