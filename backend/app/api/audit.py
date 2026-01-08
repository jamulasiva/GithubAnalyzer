"""
API endpoints for querying GitHub audit data and analytics.
Provides endpoints to retrieve processed webhook data and insights.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.database import get_database
from app.models.core import Organization, Repository, User, Installation, WebhookEvent
from app.models.events import RepositoryEvent, MemberEvent, SecurityEvent, CodeEvent
from app.services.entity_service import entity_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/test")
def test_database_connection():
    """
    Test database connection without any complex queries.
    """
    try:
        from app.core.database import SessionLocal, create_session_factory
        from sqlalchemy import text
        
        if SessionLocal is None:
            SessionLocal = create_session_factory()
            
        if SessionLocal is None:
            return {"status": "error", "message": "Database not configured"}
        
        db = SessionLocal()
        try:
            # Simple test query
            result = db.execute(text("SELECT 1 as test")).fetchone()
            
            # Also test if we can query the organizations table
            org_count = db.execute(text("SELECT COUNT(*) FROM organizations")).fetchone()
            
            return {
                "status": "success", 
                "message": "Database connected",
                "test_result": result[0] if result else None,
                "organizations_count": org_count[0] if org_count else 0
            }
        finally:
            db.close()
            
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}


@router.get("/organizations")
def list_organizations(
    skip: int = Query(0, ge=0, description="Number of organizations to skip"),
    limit: int = Query(50, le=100, description="Number of organizations to return")
):
    """
    List all organizations being monitored.
    Returns basic organization information and activity stats.
    """
    try:
        # Get database session manually to avoid async issues
        from app.core.database import SessionLocal, create_session_factory
        
        if SessionLocal is None:
            SessionLocal = create_session_factory()
            
        if SessionLocal is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        db = SessionLocal()
        try:
            organizations = db.query(Organization).offset(skip).limit(limit).all()
            
            result = []
            for org in organizations:
                # Get basic stats
                repo_count = db.query(Repository).filter(Repository.organization_id == org.id).count()
                event_count = db.query(WebhookEvent).filter(WebhookEvent.organization_id == org.id).count()
                
                result.append({
                    "id": org.id,
                    "login": org.login,
                    "name": org.name,
                    "description": org.description,
                    "public_repos": org.public_repos,
                    "total_repos": repo_count,
                    "webhook_events": event_count,
                    "created_at": org.created_at,
                    "updated_at": org.updated_at
                })
            
            return {
                "organizations": result,
                "total": len(result),
                "skip": skip,
                "limit": limit
            }
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"Error listing organizations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve organizations")


@router.get("/organizations/{org_login}")
def get_organization_details(
    org_login: str = Path(..., description="GitHub organization login"),
    db: Session = Depends(get_database)
):
    """
    Get detailed information about a specific organization.
    Includes repositories, members, and recent activity.
    """
    try:
        org = db.query(Organization).filter(Organization.login == org_login).first()
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Get repositories
        repositories = db.query(Repository).filter(Repository.organization_id == org.id).all()
        
        # Get recent events (last 7 days)
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_events = db.query(WebhookEvent).filter(
            WebhookEvent.organization_id == org.id,
            WebhookEvent.received_at >= recent_date
        ).order_by(WebhookEvent.received_at.desc()).limit(50).all()
        
        # Get event type summary
        event_summary = {}
        for event in recent_events:
            event_key = f"{event.event_type}:{event.event_action}" if event.event_action else event.event_type
            event_summary[event_key] = event_summary.get(event_key, 0) + 1
        
        return {
            "organization": {
                "id": org.id,
                "login": org.login,
                "name": org.name,
                "description": org.description,
                "html_url": org.html_url,
                "public_repos": org.public_repos,
                "created_at": org.created_at,
                "updated_at": org.updated_at
            },
            "repositories": [
                {
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "html_url": repo.html_url,
                    "created_at": repo.created_at
                }
                for repo in repositories
            ],
            "recent_activity": {
                "total_events": len(recent_events),
                "event_types": event_summary,
                "events": [
                    {
                        "id": event.id,
                        "event_type": event.event_type,
                        "action": event.event_action,
                        "repository_name": event.repository_name,
                        "sender_login": event.sender_login,
                        "received_at": event.received_at
                    }
                    for event in recent_events[:10]  # Latest 10 events
                ]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting organization details: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve organization details")


@router.get("/repositories")
def list_repositories(
    db: Session = Depends(get_database),
    organization_login: Optional[str] = Query(None, description="Filter by organization"),
    private: Optional[bool] = Query(None, description="Filter by repository visibility"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100)
):
    """
    List repositories being monitored.
    Can be filtered by organization and visibility.
    """
    try:
        query = db.query(Repository)
        
        # Filter by organization if specified
        if organization_login:
            org = db.query(Organization).filter(Organization.login == organization_login).first()
            if org:
                query = query.filter(Repository.organization_id == org.id)
            else:
                return {"repositories": [], "total": 0}
        
        # Filter by visibility if specified
        if private is not None:
            query = query.filter(Repository.private == private)
        
        repositories = query.offset(skip).limit(limit).all()
        
        result = []
        for repo in repositories:
            # Get recent activity count
            recent_date = datetime.utcnow() - timedelta(days=7)
            event_count = db.query(WebhookEvent).filter(
                WebhookEvent.repository_id == repo.id,
                WebhookEvent.received_at >= recent_date
            ).count()
            
            result.append({
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "private": repo.private,
                "fork": repo.fork,
                "html_url": repo.html_url,
                "stargazers_count": repo.stargazers_count,
                "watchers_count": repo.watchers_count,
                "forks_count": repo.forks_count,
                "recent_events": event_count,
                "created_at": repo.created_at,
                "updated_at": repo.updated_at
            })
        
        return {
            "repositories": result,
            "total": len(result),
            "filters": {
                "organization": organization_login,
                "private": private
            },
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error listing repositories: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve repositories")


@router.get("/events")
def list_webhook_events(
    db: Session = Depends(get_database),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    organization_login: Optional[str] = Query(None, description="Filter by organization"),
    repository_name: Optional[str] = Query(None, description="Filter by repository"),
    sender_login: Optional[str] = Query(None, description="Filter by sender"),
    since: Optional[datetime] = Query(None, description="Events since this timestamp"),
    until: Optional[datetime] = Query(None, description="Events until this timestamp"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500)
):
    """
    List webhook events with filtering capabilities.
    Provides audit trail of all GitHub activities.
    """
    try:
        query = db.query(WebhookEvent)
        
        # Apply filters
        if event_type:
            query = query.filter(WebhookEvent.event_type == event_type)
        
        if organization_login:
            org = db.query(Organization).filter(Organization.login == organization_login).first()
            if org:
                query = query.filter(WebhookEvent.organization_id == org.id)
        
        if repository_name:
            query = query.filter(WebhookEvent.repository_name.ilike(f"%{repository_name}%"))
        
        if sender_login:
            query = query.filter(WebhookEvent.sender_login.ilike(f"%{sender_login}%"))
        
        if since:
            query = query.filter(WebhookEvent.received_at >= since)
        
        if until:
            query = query.filter(WebhookEvent.received_at <= until)
        
        # Order by most recent first
        query = query.order_by(WebhookEvent.received_at.desc())
        
        events = query.offset(skip).limit(limit).all()
        
        result = []
        for event in events:
            result.append({
                "id": event.id,
                "event_type": event.event_type,
                "action": event.event_action,
                "organization_login": event.organization_login,
                "repository_name": event.repository_name,
                "sender_login": event.sender_login,
                "delivery_id": event.delivery_id,
                "received_at": event.received_at,
                "processing_status": event.processed,
                "created_at": event.created_at
            })
        
        return {
            "events": result,
            "total": len(result),
            "filters": {
                "event_type": event_type,
                "organization": organization_login,
                "repository": repository_name,
                "sender": sender_login,
                "since": since,
                "until": until
            },
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error listing events: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve events")


@router.get("/events/{event_id}")
def get_event_details(
    event_id: str = Path(..., description="Webhook event ID"),
    db: Session = Depends(get_database)
):
    """
    Get detailed information about a specific webhook event.
    Includes the full parsed payload and related entities.
    """
    try:
        event = db.query(WebhookEvent).filter(WebhookEvent.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "id": event.id,
            "event_type": event.event_type,
            "action": event.event_action,
            "organization_login": event.organization_login,
            "organization_id": event.organization_id,
            "repository_name": event.repository_name,
            "repository_id": event.repository_id,
            "sender_login": event.sender_login,
            "sender_id": event.sender_id,
            "delivery_id": event.delivery_id,
            "user_agent": event.user_agent,
            "received_at": event.received_at,
            "processing_status": event.processed,
            "error_message": event.error_message,
            "raw_payload": event.raw_payload,
            "parsed_payload": event.parsed_payload,
            "created_at": event.created_at,
            "updated_at": event.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting event details: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve event details")


@router.get("/analytics/summary")
def get_analytics_summary(
    db: Session = Depends(get_database),
    organization_login: Optional[str] = Query(None, description="Filter by organization"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get analytics summary for the specified time period.
    Provides overview of activity, trends, and insights.
    """
    try:
        start_date = datetime.now().replace(tzinfo=datetime.now().astimezone().tzinfo) - timedelta(days=days)
        
        query = db.query(WebhookEvent).filter(WebhookEvent.received_at >= start_date)
        
        # Filter by organization if specified
        if organization_login:
            org = db.query(Organization).filter(Organization.login == organization_login).first()
            if org:
                query = query.filter(WebhookEvent.organization_id == org.id)
        
        events = query.all()
        
        # Calculate analytics
        total_events = len(events)
        unique_repositories = len(set(event.repository_name for event in events if event.repository_name))
        unique_users = len(set(event.sender_login for event in events if event.sender_login))
        
        # Event type distribution
        event_types = {}
        for event in events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        
        # Daily activity (last 7 days)
        daily_activity = {}
        now = datetime.now().replace(tzinfo=datetime.now().astimezone().tzinfo)
        for i in range(7):
            day = now - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            daily_activity[day_str] = 0
        
        for event in events:
            seven_days_ago = now - timedelta(days=7)
            if event.received_at >= seven_days_ago:
                day_str = event.received_at.strftime('%Y-%m-%d')
                if day_str in daily_activity:
                    daily_activity[day_str] += 1
        
        # Top active repositories
        repo_activity = {}
        for event in events:
            if event.repository_name:
                repo_activity[event.repository_name] = repo_activity.get(event.repository_name, 0) + 1
        
        top_repos = sorted(repo_activity.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top active users
        user_activity = {}
        for event in events:
            if event.sender_login:
                user_activity[event.sender_login] = user_activity.get(event.sender_login, 0) + 1
        
        top_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "period": {
                "days": days,
                "start_date": start_date,
                "end_date": datetime.utcnow(),
                "organization": organization_login
            },
            "summary": {
                "total_events": total_events,
                "unique_repositories": unique_repositories,
                "unique_users": unique_users,
                "avg_events_per_day": round(total_events / days, 2)
            },
            "event_types": event_types,
            "daily_activity": daily_activity,
            "top_repositories": [{"name": repo, "events": count} for repo, count in top_repos],
            "top_users": [{"login": user, "events": count} for user, count in top_users]
        }
        
    except Exception as e:
        logger.error(f"Error generating analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate analytics summary")