#!/usr/bin/env python3
"""
Script to reprocess member and organization events to populate relationship tables.
"""

import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.core.database import get_database
from app.models.core import WebhookEvent
from app.models.events import MemberEvent, OrganizationMembership, RepositoryCollaborator
from app.services.event_processing_service import event_processing_service


async def reprocess_relationships():
    """Reprocess member/organization events to populate relationship tables."""
    
    db_gen = get_database()
    db = next(db_gen)
    
    try:
        print("👥 Reprocessing Member/Organization Events")
        print("=" * 45)
        
        # Get member and organization webhook events
        member_events = db.query(WebhookEvent).filter(
            WebhookEvent.event_type.in_(['member', 'organization'])
        ).all()
        
        print(f"\n📊 Found {len(member_events)} member/organization webhook events")
        
        # Clear existing member events to reprocess them
        print("🧹 Clearing existing member events for reprocessing...")
        db.query(MemberEvent).delete()
        db.query(OrganizationMembership).delete()
        db.query(RepositoryCollaborator).delete()
        db.commit()
        
        # Process events
        processed_count = 0
        error_count = 0
        memberships_created = 0
        collaborators_created = 0
        
        print(f"\n🚀 Reprocessing Events:")
        print("-" * 25)
        
        for i, webhook_event in enumerate(member_events, 1):
            try:
                print(f"Processing {i}/{len(member_events)}: {webhook_event.event_type} - {webhook_event.payload.get('action', 'unknown')} (ID: {webhook_event.id})", end=" ... ")
                
                # Mark as unprocessed to allow reprocessing
                webhook_event.processed = False
                webhook_event.processed_at = None
                webhook_event.processing_error = None
                
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
        
        # Check results
        memberships_created = db.query(OrganizationMembership).count()
        collaborators_created = db.query(RepositoryCollaborator).count()
        member_events_created = db.query(MemberEvent).count()
        
        print(f"\n📈 Reprocessing Results:")
        print("-" * 25)
        print(f"  ✅ Events processed: {processed_count}")
        print(f"  ❌ Errors: {error_count}")
        print(f"  👥 Member events created: {member_events_created}")
        print(f"  🏢 Organization memberships: {memberships_created}")
        print(f"  📁 Repository collaborators: {collaborators_created}")
        
        if memberships_created > 0 or collaborators_created > 0:
            print(f"\n🎉 Successfully created {memberships_created} memberships and {collaborators_created} collaborators!")
            print("💡 Run 'python inspect_test_data.py --tables' to see the updated counts")
        else:
            print(f"\n⚠️ No relationships were created. This might be expected if test data doesn't include membership changes.")
            print("💡 Run 'python analyze_relationships.py' to see what data is available")
        
        print("\n" + "=" * 45)
        print("✅ Relationship reprocessing complete!")
        
    except Exception as e:
        print(f"❌ Error during reprocessing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(reprocess_relationships())