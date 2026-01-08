"""Common base models for GitHub webhooks."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WebhookHeaders(BaseModel):
    """GitHub webhook delivery headers."""
    
    x_github_event: str = Field(alias="X-GitHub-Event")
    x_github_delivery: str = Field(alias="X-GitHub-Delivery")
    x_hub_signature_256: Optional[str] = Field(None, alias="X-Hub-Signature-256")
    x_github_hook_id: Optional[str] = Field(None, alias="X-GitHub-Hook-ID")
    x_github_hook_installation_target_type: Optional[str] = Field(
        None, alias="X-GitHub-Hook-Installation-Target-Type"
    )
    x_github_hook_installation_target_id: Optional[str] = Field(
        None, alias="X-GitHub-Hook-Installation-Target-ID"
    )
    user_agent: Optional[str] = Field(None, alias="User-Agent")
    content_type: str = Field(default="application/json", alias="Content-Type")

    class Config:
        allow_population_by_field_name = True


class WebhookBase(BaseModel):
    """Base class for all GitHub webhook events."""
    
    action: str
    sender: "User"
    repository: Optional["Repository"] = None
    organization: Optional["Organization"] = None
    installation: Optional["Installation"] = None
    
    class Config:
        # Allow extra fields for future compatibility
        extra = "allow"
        # Use enum values instead of enum objects
        use_enum_values = True


# Forward references for circular imports
from .user import User
from .repository import Repository
from .organization import Organization  
from .installation import Installation

WebhookBase.model_rebuild()