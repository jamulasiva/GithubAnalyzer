#!/usr/bin/env python3
"""
Script to reprocess existing webhook events into specialized event tables.
Run this to process webhook events that were stored before the event processing service was added.
"""

import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.core.database import get_database
from app.models.core import WebhookEvent
from app.services.event_processing_service import event_processing_service


async def reprocess_webhook_events():
    """Reprocess existing webhook events into specialized tables."""
    
    db_gen = get_database()
    db = next(db_gen)
    
    try:
        print("🔄 Reprocessing Webhook Events")
        print("=" * 40)
        
        # Get all unprocessed webhook events
        unprocessed_events = db.query(WebhookEvent).filter(
            WebhookEvent.processed == False
        ).all()
        
        print(f"\n📊 Found {len(unprocessed_events)} unprocessed webhook events")
        
        if not unprocessed_events:
            print("✅ All webhook events are already processed!")
            return
        
        # Group by event type
        event_types = {}
        for event in unprocessed_events:
            event_type = event.event_type
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append(event)
        
        print(f"\n📋 Event Types to Process:")
        for event_type, events in event_types.items():
            print(f"  • {event_type}: {len(events)} events")
        
        # Process events
        processed_count = 0
        error_count = 0
        
        print(f"\n🚀 Starting Event Processing:")
        print("-" * 30)
        
        for i, webhook_event in enumerate(unprocessed_events, 1):
            try:
                print(f"Processing {i}/{len(unprocessed_events)}: {webhook_event.event_type} (ID: {webhook_event.id})", end=" ... ")
                
                success = await event_processing_service.process_webhook_event(db, webhook_event)
                
                if success:
                    print("✅")
                    processed_count += 1
                else:
                    print("❌")
                    error_count += 1
                    
            except Exception as e:
                print(f"💥 Error: {e}")
                error_count += 1
        
        print(f"\n📈 Processing Summary:")
        print("-" * 20)
        print(f"  ✅ Successfully processed: {processed_count}")
        print(f"  ❌ Errors: {error_count}")
        print(f"  📊 Total events: {len(unprocessed_events)}")
        
        if processed_count > 0:
            print(f"\n🎉 Successfully processed {processed_count} webhook events!")
            print("💡 Run 'python inspect_test_data.py --tables' to see the updated counts")
        
        print("\n" + "=" * 40)
        print("✅ Reprocessing complete!")
        
    except Exception as e:
        print(f"❌ Error during reprocessing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(reprocess_webhook_events())