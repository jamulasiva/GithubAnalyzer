"""Code scanning alert event webhook model."""

from typing import Optional

from pydantic import Field

from .common.base import WebhookBase
from .common.user import User
from .common.repository import Repository
from .common.organization import Organization
from .common.installation import Installation
from .common.security import CodeScanningAlert


class CodeScanningAlertEvent(WebhookBase):
    """
    GitHub webhook event for code scanning alert activities.
    
    Event Type: code_scanning_alert
    Actions: created, fixed, reopened, appeared_in_branch, closed_by_user
    """
    
    action: str = Field(..., description="Action performed: created, fixed, reopened, appeared_in_branch, closed_by_user")
    
    alert: CodeScanningAlert = Field(..., description="The code scanning alert")
    ref: str = Field(..., description="The Git reference of the code scanning alert")
    commit_oid: str = Field(..., description="The commit SHA of the code scanning alert")
    
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
                    "rule": {
                        "id": "js/sql-injection",
                        "severity": "error",
                        "description": "SQL injection"
                    },
                    "tool": {
                        "name": "CodeQL",
                        "version": "2.11.6"
                    }
                },
                "ref": "refs/heads/main",
                "commit_oid": "abcdef1234567890"
            }
        }