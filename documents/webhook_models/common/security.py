"""Security-related models for GitHub webhooks."""

from typing import Optional, Dict, Any, List

from pydantic import BaseModel, HttpUrl

from .user import User


class Rule(BaseModel):
    """Code scanning rule model."""
    
    id: str
    severity: str  # "error", "warning", "note"
    description: str
    name: str
    full_description: Optional[str] = None
    tags: Optional[List[str]] = []


class Tool(BaseModel):
    """Code scanning tool model."""
    
    name: str
    version: Optional[str] = None


class Location(BaseModel):
    """Code location model."""
    
    path: str
    start_line: int
    end_line: int
    start_column: int
    end_column: int


class CodeScanningInstance(BaseModel):
    """Code scanning alert instance model."""
    
    ref: str
    analysis_key: str
    environment: str
    state: str
    commit_sha: str
    location: Location


class CodeScanningAlert(BaseModel):
    """Code scanning alert model."""
    
    number: int
    created_at: str  # ISO 8601
    updated_at: Optional[str] = None  # ISO 8601
    url: HttpUrl
    html_url: HttpUrl
    state: str  # "open", "dismissed", "fixed"
    fixed_at: Optional[str] = None  # ISO 8601
    dismissed_by: Optional[User] = None
    dismissed_at: Optional[str] = None  # ISO 8601
    dismissed_reason: Optional[str] = None
    dismissed_comment: Optional[str] = None
    rule: Rule
    tool: Tool
    most_recent_instance: CodeScanningInstance
    instances_url: HttpUrl


class DependabotAlert(BaseModel):
    """Dependabot alert model."""
    
    number: int
    state: str  # "auto_dismissed", "dismissed", "fixed", "open"
    dependency: Dict[str, Any]
    security_advisory: Dict[str, Any]
    security_vulnerability: Dict[str, Any]
    url: HttpUrl
    html_url: HttpUrl
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    dismissed_at: Optional[str] = None  # ISO 8601
    dismissed_by: Optional[User] = None
    dismissed_reason: Optional[str] = None
    dismissed_comment: Optional[str] = None
    fixed_at: Optional[str] = None  # ISO 8601
    auto_dismissed_at: Optional[str] = None  # ISO 8601


class SecretScanningAlert(BaseModel):
    """Secret scanning alert model."""
    
    number: int
    created_at: str  # ISO 8601
    updated_at: Optional[str] = None  # ISO 8601
    url: HttpUrl
    html_url: HttpUrl
    locations_url: HttpUrl
    state: str  # "open", "resolved"
    resolution: Optional[str] = None
    resolved_at: Optional[str] = None  # ISO 8601
    resolved_by: Optional[User] = None
    resolution_comment: Optional[str] = None
    secret_type: str
    secret_type_display_name: str
    secret: str
    repository: Optional["Repository"] = None
    push_protection_bypassed: Optional[bool] = None
    push_protection_bypassed_by: Optional[User] = None
    push_protection_bypassed_at: Optional[str] = None  # ISO 8601