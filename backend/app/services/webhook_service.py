"""
Webhook receiver service for GitHub events.
Integrates with existing webhook_models package for validation and parsing.
"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

# Import our local webhook models
from app.webhook_models.utils import validate_github_signature, parse_webhook_payload, WEBHOOK_EVENT_MAP
from app.webhook_models.common.base import WebhookBase

from app.core.config import get_settings
from app.core.database import get_supabase_client
from app.core.logging_config import log_webhook_event, log_database_operation
from app.models.core import WebhookEvent, Organization, User, Repository, Installation
from app.services.entity_service import EntityService
from app.services.event_processing_service import event_processing_service

logger = logging.getLogger(__name__)


class WebhookReceiverService:
    """Service for receiving and processing GitHub webhooks."""
    
    def __init__(self):
        self.settings = get_settings()
        self.entity_service = EntityService()
    
    async def validate_webhook_signature(
        self, 
        payload_body: bytes, 
        signature_header: Optional[str]
    ) -> bool:
        """
        Validate GitHub webhook signature using existing webhook_models utility.
        
        Args:
            payload_body: Raw webhook payload body
            signature_header: X-Hub-Signature-256 header value
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.settings.GITHUB_WEBHOOK_SECRET:
            logger.warning("GitHub webhook secret not configured - signature validation disabled")
            return True
        
        if not signature_header:
            logger.error("Missing webhook signature header")
            return False
        
        try:
            is_valid = validate_github_signature(
                payload_body,
                signature_header,
                self.settings.GITHUB_WEBHOOK_SECRET
            )
            
            if not is_valid:
                logger.error("Invalid webhook signature")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Signature validation error: {e}")
            return False
    
    async def parse_webhook_event(
        self,
        payload: Dict[str, Any],
        event_type: str,
        action: Optional[str] = None
    ) -> WebhookBase:
        """
        Parse webhook payload using existing webhook_models.
        
        Args:
            payload: Parsed JSON webhook payload
            event_type: GitHub event type (X-GitHub-Event header)
            action: Action field from payload
            
        Returns:
            Parsed webhook event model
            
        Raises:
            HTTPException: If event type/action is not supported or validation fails
        """
        try:
            # Use existing webhook_models parsing
            webhook_event = parse_webhook_payload(payload, event_type, action)
            logger.info(f"Successfully parsed {event_type} event with action: {action}")
            return webhook_event
            
        except ValueError as e:
            logger.error(f"Unsupported webhook event: {e}")
            logger.error(f"Failed payload: {json.dumps(payload, indent=2) if isinstance(payload, dict) else str(payload)}")
            raise HTTPException(status_code=422, detail=f"Unsupported event type: {e}")
            
        except Exception as e:
            logger.error(f"Webhook parsing error: {e}")
            logger.error(f"Failed payload: {json.dumps(payload, indent=2) if isinstance(payload, dict) else str(payload)}")
            raise HTTPException(status_code=400, detail=f"Invalid webhook payload: {e}")
    
    async def store_webhook_event(
        self,
        db: Session,
        webhook_event: WebhookBase,
        raw_payload: Dict[str, Any],
        headers: Dict[str, str],
        delivery_id: Optional[str],
        event_type: str
    ) -> WebhookEvent:
        """
        Store webhook event in database with entity relationships.
        
        Args:
            db: Database session
            webhook_event: Parsed webhook event model
            raw_payload: Original JSON payload
            headers: Request headers
            delivery_id: GitHub delivery ID
            
        Returns:
            Stored webhook event record
        """
        try:
            # Extract event timestamp
            event_timestamp = datetime.now(timezone.utc)
            if hasattr(webhook_event, 'created_at') and webhook_event.created_at:
                # Try to parse GitHub timestamp if available
                try:
                    event_timestamp = datetime.fromisoformat(webhook_event.created_at.replace('Z', '+00:00'))
                except:
                    pass
            
            # Ensure entities exist and get their IDs
            organization_id = None
            repository_id = None
            sender_id = None
            installation_id = None
            
            if hasattr(webhook_event, 'organization') and webhook_event.organization:
                organization_id = await self.entity_service.ensure_organization(db, webhook_event.organization)
            
            if hasattr(webhook_event, 'repository') and webhook_event.repository:
                repository_id = await self.entity_service.ensure_repository(db, webhook_event.repository)
            
            if hasattr(webhook_event, 'sender') and webhook_event.sender:
                sender_id = await self.entity_service.ensure_user(db, webhook_event.sender)
            
            if hasattr(webhook_event, 'installation') and webhook_event.installation:
                installation_id = await self.entity_service.ensure_installation(db, webhook_event.installation)
            
            # Create webhook event record
            db_webhook_event = WebhookEvent(
                delivery_id=delivery_id,
                event_type=event_type,
                event_action=getattr(webhook_event, 'action', None),
                organization_id=organization_id,
                repository_id=repository_id,
                sender_id=sender_id,
                installation_id=installation_id,
                event_timestamp=event_timestamp,
                payload=raw_payload,
                headers=headers,
                processed=False
            )
            
            db.add(db_webhook_event)
            db.commit()
            db.refresh(db_webhook_event)
            
            logger.info(f"Stored webhook event {event_type} with ID {db_webhook_event.id}")
            return db_webhook_event
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to store webhook event: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to store event: {e}")
    
    async def trigger_real_time_update(self, webhook_event: WebhookEvent):
        """
        Trigger real-time updates via Supabase for dashboard subscriptions.
        
        Args:
            webhook_event: Stored webhook event
        """
        try:
            supabase = get_supabase_client()
            if not supabase:
                logger.warning("Supabase client not available - real-time updates disabled")
                return
            
            # Publish real-time event to Supabase
            # This will be received by frontend dashboard subscriptions
            channel_name = f"webhook_events:{webhook_event.repository_id or 'global'}"
            
            event_data = {
                "id": webhook_event.id,
                "event_type": webhook_event.event_type,
                "event_action": webhook_event.event_action,
                "event_timestamp": webhook_event.event_timestamp.isoformat(),
                "repository_name": webhook_event.repository_name,
                "organization_login": webhook_event.organization_login,
                "sender_login": webhook_event.sender_login
            }
            
            # Note: Supabase real-time broadcasting happens automatically
            # through database triggers and RLS policies
            logger.info(f"Real-time update triggered for event {webhook_event.id}")
            
        except Exception as e:
            logger.error(f"Failed to trigger real-time update: {e}")
            # Don't raise exception - real-time is not critical
    
    async def process_webhook(
        self,
        payload_body: bytes,
        headers: Dict[str, str],
        background_tasks: BackgroundTasks,
        db: Session
    ) -> Dict[str, Any]:
        """
        Main webhook processing pipeline.
        
        Args:
            payload_body: Raw request body
            headers: Request headers
            background_tasks: FastAPI background tasks
            db: Database session
            
        Returns:
            Processing result
        """
        # Extract headers
        event_type = headers.get('x-github-event')
        delivery_id = headers.get('x-github-delivery')
        signature = headers.get('x-hub-signature-256')
        
        # Enhanced logging for webhook processing start
        log_webhook_event(
            event_type or "unknown",
            delivery_id or "no-delivery-id", 
            f"🔄 Starting webhook processing | Headers: {list(headers.keys())}"
        )
        
        if not event_type:
            log_webhook_event("unknown", delivery_id or "no-delivery-id", "❌ Missing X-GitHub-Event header", "ERROR")
            raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")
        
        # Validate signature
        log_webhook_event(event_type, delivery_id, "🔐 Validating webhook signature", "DEBUG")
        is_valid = await self.validate_webhook_signature(payload_body, signature)
        if not is_valid:
            log_webhook_event(event_type, delivery_id, "❌ Invalid webhook signature", "ERROR")
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        log_webhook_event(event_type, delivery_id, "✅ Webhook signature validated", "DEBUG")
        
        # Parse payload
        try:
            payload = json.loads(payload_body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Parse webhook event using existing models
        action = payload.get('action')
        webhook_event = await self.parse_webhook_event(payload, event_type, action)
        
        # Store in database
        db_webhook_event = await self.store_webhook_event(
            db, webhook_event, payload, dict(headers), delivery_id, event_type
        )
        
        # Add background tasks
        background_tasks.add_task(self.trigger_real_time_update, db_webhook_event)
        background_tasks.add_task(self.process_event_async, db_webhook_event.id)
        
        return {
            "status": "received",
            "event_id": db_webhook_event.id,
            "event_type": event_type,
            "action": action,
            "delivery_id": delivery_id,
            "processed": False
        }
    
    async def process_event_async(self, event_id: int):
        """
        Background processing of webhook events.
        This processes events into specialized event tables and performs additional enrichment.
        
        Args:
            event_id: Database ID of the webhook event
        """
        try:
            logger.info(f"Starting background processing for event {event_id}")
            
            # Get database session for background processing
            from app.core.database import get_database
            db_gen = get_database()
            db = next(db_gen)
            
            try:
                # Get the webhook event
                webhook_event = db.query(WebhookEvent).filter(WebhookEvent.id == event_id).first()
                if not webhook_event:
                    logger.error(f"Webhook event {event_id} not found")
                    return
                
                # Process the event into specialized tables
                success = await event_processing_service.process_webhook_event(db, webhook_event)
                
                if success:
                    logger.info(f"Successfully processed event {event_id} into specialized tables")
                else:
                    logger.warning(f"Failed to process event {event_id} into specialized tables")
                
                # Additional background processing can be added here:
                # 1. Event enrichment with GitHub API
                # 2. Security analysis
                # 3. Compliance checking
                # 4. Alert generation
                # 5. Analytics updates
                
            finally:
                db.close()
            
            logger.info(f"Completed background processing for event {event_id}")
            
        except Exception as e:
            logger.error(f"Background processing failed for event {event_id}: {e}")


# Global service instance
webhook_receiver_service = WebhookReceiverService()