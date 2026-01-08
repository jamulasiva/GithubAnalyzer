"""
GitHub webhook API endpoints.
Receives and processes GitHub webhook events using the existing webhook_models.
"""

from fastapi import APIRouter, Request, Header, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.core.database import get_database
from app.services.webhook_service import webhook_receiver_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def receive_github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database),
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_github_delivery: Optional[str] = Header(None, alias="X-GitHub-Delivery"),
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
    user_agent: Optional[str] = Header(None, alias="User-Agent")
):
    """
    Main GitHub webhook endpoint.
    Receives all GitHub webhook events and processes them using existing webhook_models.
    
    Supported Events:
    - member (added, edited)
    - repository (created, publicized, deleted, etc.)
    - push (git push events)
    - issues (opened, closed, etc.)
    - pull_request (opened, closed, merged, etc.)
    - team (added_to_repository)
    - fork (repository forked)
    - create/delete (branch/tag operations)
    - issue_comment (created, edited, deleted)
    - pull_request_review (submitted, edited, dismissed)
    - ping (webhook creation)
    - installation (GitHub App events)
    - organization (member changes)
    - code_scanning_alert (security alerts)
    - dependabot_alert (dependency alerts)
    - secret_scanning_alert (secret detection)
    - meta (webhook management)
    - personal_access_token_request (PAT requests)
    """
    try:
        # Get raw request body for signature validation
        payload_body = await request.body()
        
        # Extract headers for processing
        headers = {
            'x-github-event': x_github_event,
            'x-github-delivery': x_github_delivery,
            'x-hub-signature-256': x_hub_signature_256,
            'user-agent': user_agent
        }
        
        logger.info(f"Received GitHub webhook: {x_github_event} - {x_github_delivery}")
        
        # Process webhook using the service
        result = await webhook_receiver_service.process_webhook(
            payload_body=payload_body,
            headers=headers,
            background_tasks=background_tasks,
            db=db
        )
        
        # Return success response
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error processing webhook {x_github_delivery}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing webhook"
        )


@router.get("/github/events")
async def list_supported_events():
    """
    List all supported GitHub webhook event types.
    Returns the events that can be processed by the webhook receiver.
    """
    # Import the event map from local webhook_models
    from app.webhook_models.utils import WEBHOOK_EVENT_MAP
    
    supported_events = {}
    
    for event_type, actions in WEBHOOK_EVENT_MAP.items():
        supported_events[event_type] = {
            "actions": list(actions.keys()),
            "description": f"GitHub {event_type} webhook events"
        }
    
    return {
        "message": "GitHub Audit Platform - Supported Webhook Events",
        "total_event_types": len(supported_events),
        "events": supported_events,
        "endpoint": "/api/v1/webhooks/github",
        "documentation": "See GitHub Webhooks API documentation for payload details"
    }


@router.get("/github/test")
async def test_webhook_endpoint():
    """
    Test endpoint to verify webhook receiver is working.
    Can be used for health checks or testing webhook connectivity.
    """
    return {
        "status": "ok",
        "message": "GitHub webhook endpoint is ready",
        "endpoint": "/api/v1/webhooks/github",
        "methods": ["POST"],
        "headers_required": [
            "X-GitHub-Event",
            "X-GitHub-Delivery", 
            "X-Hub-Signature-256"
        ]
    }


@router.post("/github/simulate")
async def simulate_webhook_event(
    event_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database),
    event_type: str = Header(..., description="GitHub event type to simulate"),
    delivery_id: Optional[str] = Header(None, description="Simulated delivery ID")
):
    """
    Simulate a webhook event for testing purposes.
    Useful for development and testing without actual GitHub webhooks.
    
    Note: This endpoint bypasses signature validation and should be disabled in production.
    """
    try:
        import json
        from app.core.config import get_settings
        
        settings = get_settings()
        
        # Only allow in development mode
        if not settings.DEBUG:
            raise HTTPException(
                status_code=403,
                detail="Webhook simulation only available in development mode"
            )
        
        # Simulate headers
        headers = {
            'x-github-event': event_type,
            'x-github-delivery': delivery_id or "simulated-delivery",
            'x-hub-signature-256': None,  # Skip signature validation for simulation
            'user-agent': 'GitHub-Hookshot/simulation'
        }
        
        payload_body = json.dumps(event_data).encode('utf-8')
        
        logger.info(f"Simulating GitHub webhook: {event_type}")
        
        # Process the simulated webhook
        result = await webhook_receiver_service.process_webhook(
            payload_body=payload_body,
            headers=headers,
            background_tasks=background_tasks,
            db=db
        )
        
        return {
            "simulation": True,
            "result": result
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error simulating webhook: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to simulate webhook: {e}"
        )