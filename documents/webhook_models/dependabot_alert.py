"""Dependabot alert event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.security import DependabotAlert


class DependabotAlertEvent(WebhookBase):
    """
    GitHub webhook event for Dependabot alert activities.
    
    Event Type: dependabot_alert
    Actions: created, dismissed, fixed, reintroduced, reopened
    """
    
    action: str = Field(..., description="Action performed: created, dismissed, fixed, reintroduced, reopened")
    
    alert: DependabotAlert = Field(..., description="The Dependabot alert")
    
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
                    "dependency": {
                        "package": {"name": "lodash"},
                        "manifest_path": "package.json"
                    },
                    "security_advisory": {
                        "summary": "Prototype pollution in lodash"
                    }
                }
            }
        }