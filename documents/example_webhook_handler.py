"""
Example FastAPI webhook handler using the Pydantic models.

This demonstrates how to use the webhook models in a real FastAPI application.
"""

from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from typing import Optional
import json

from webhook_models.utils import validate_github_signature, parse_webhook_payload
from webhook_models.member_added import MemberAddedEvent
from webhook_models.repository_created import RepositoryCreatedEvent
from webhook_models.push import PushEvent

app = FastAPI(title="GitHub Webhook Handler")

# Your webhook secret from GitHub
WEBHOOK_SECRET = "your-webhook-secret-here"


@app.post("/webhook")
async def handle_github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_github_delivery: str = Header(..., alias="X-GitHub-Delivery"),
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
):
    """
    Handle GitHub webhook events with automatic validation and parsing.
    """
    # Get raw body for signature validation
    body = await request.body()
    
    # Validate webhook signature
    if not validate_github_signature(body, x_hub_signature_256, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Parse into appropriate Pydantic model
    try:
        webhook_event = parse_webhook_payload(payload, x_github_event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Payload validation error: {str(e)}")
    
    # Process the event in background
    background_tasks.add_task(process_webhook_event, webhook_event, x_github_delivery)
    
    return {"status": "accepted", "delivery_id": x_github_delivery}


async def process_webhook_event(event: WebhookBase, delivery_id: str):
    """
    Process webhook events based on their type.
    This runs in the background after responding to GitHub.
    """
    if isinstance(event, MemberAddedEvent):
        await handle_member_added(event, delivery_id)
    elif isinstance(event, RepositoryCreatedEvent):
        await handle_repository_created(event, delivery_id)
    elif isinstance(event, PushEvent):
        await handle_push_event(event, delivery_id)
    else:
        print(f"Unhandled event type: {type(event).__name__}")


async def handle_member_added(event: MemberAddedEvent, delivery_id: str):
    """Handle member added events."""
    print(f"[{delivery_id}] New collaborator: {event.member.login} "
          f"added to {event.repository.full_name} by {event.sender.login}")
    
    # Example: Save to database
    # await save_member_event_to_db(event)
    
    # Example: Send notification
    # await send_slack_notification(f"New collaborator {event.member.login} added!")


async def handle_repository_created(event: RepositoryCreatedEvent, delivery_id: str):
    """Handle repository created events."""
    print(f"[{delivery_id}] New repository: {event.repository.full_name} "
          f"created by {event.sender.login}")
    
    # Example: Initialize repository monitoring
    # await setup_repo_monitoring(event.repository)


async def handle_push_event(event: PushEvent, delivery_id: str):
    """Handle push events."""
    commit_count = len(event.commits)
    print(f"[{delivery_id}] Push to {event.repository.full_name}:{event.ref} "
          f"by {event.pusher.name} - {commit_count} commit(s)")
    
    # Example: Trigger CI/CD pipeline
    # await trigger_pipeline(event)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)