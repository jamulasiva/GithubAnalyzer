"""Secret scanning alert event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.security import SecretScanningAlert


class SecretScanningAlertEvent(WebhookBase):
    """
    GitHub webhook event for secret scanning alert activities.
    
    Event Type: secret_scanning_alert
    Actions: created, resolved, reopened, revoked
    """
    
    action: str = Field(..., description="Action performed: created, resolved, reopened, revoked")
    
    alert: SecretScanningAlert = Field(..., description="The secret scanning alert")
    
    repository: Repository = Field(..., description="Repository where the alert was found")
    sender: User = Field(..., description="User who performed the action")
    organization: Optional[Organization] = Field(None, description="Organization info (if applicable)")
    installation: Optional[Installation] = Field(None, description="GitHub App installation info")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "created",
                "alert": {
                    "number": 1,
                    "state": "open",
                    "secret_type": "github_personal_access_token",
                    "secret_type_display_name": "GitHub Personal Access Token",
                    "secret": "ghp_****"
                }
            }
        }