#!/usr/bin/env python3
"""
Script to inspect webhook test data stored in the database.
Run this after running live server tests to see what data was saved.
"""

import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.core.database import get_database
from app.models.core import WebhookEvent, Organization, Repository, User, Installation
from app.models.events import (
    RepositoryEvent, MemberEvent, SecurityEvent, CodeEvent,
    OrganizationMembership, RepositoryCollaborator
)


def get_all_table_counts(db):
    """Get total record counts for all tables in the system."""
    
    table_counts = {}
    
    try:
        # Core models from app.models.core
        table_counts['Core Tables'] = {
            'Organizations': db.query(Organization).count(),
            'Users': db.query(User).count(), 
            'Repositories': db.query(Repository).count(),
            'Installations': db.query(Installation).count(),
            'Webhook Events': db.query(WebhookEvent).count()
        }
        
        # Event models from app.models.events
        table_counts['Event Tables'] = {
            'Repository Events': db.query(RepositoryEvent).count(),
            'Member Events': db.query(MemberEvent).count(),
            'Security Events': db.query(SecurityEvent).count(),
            'Code Events': db.query(CodeEvent).count()
        }
        
        # Relationship models
        table_counts['Relationship Tables'] = {
            'Organization Memberships': db.query(OrganizationMembership).count(),
            'Repository Collaborators': db.query(RepositoryCollaborator).count()
        }
        
    except Exception as e:
        print(f"⚠️ Error querying table counts: {e}")
        return {}
    
    return table_counts


def inspect_test_data():
    """Inspect webhook test data in the database."""
    
    # Get database session
    db_gen = get_database()
    db = next(db_gen)
    
    try:
        print("🔍 Inspecting Webhook Test Data")
        print("=" * 50)
        
        # Get all webhook events with 'live-test' in delivery_id
        test_events = db.query(WebhookEvent).filter(
            WebhookEvent.delivery_id.like('%live-test%')
        ).all()
        
        print(f"\n📊 Found {len(test_events)} test webhook events:")
        print("-" * 30)
        
        event_types = {}
        for event in test_events:
            event_type = event.event_type
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append(event)
        
        # Display events by type
        for event_type, events in event_types.items():
            print(f"\n🔗 {event_type.upper()} Events ({len(events)}):")
            for event in events:
                print(f"  • ID: {event.id}")
                print(f"    Delivery ID: {event.delivery_id}")
                print(f"    Created: {event.created_at}")
                print(f"    Processed: {'✅' if event.processed_at else '❌'}")
                print(f"    Status: {'✅ Processed' if event.processed else '⏳ Pending'}")
                if hasattr(event, 'processing_error') and event.processing_error:
                    print(f"    Error: {event.processing_error[:100]}...")
                if hasattr(event, 'retry_count') and event.retry_count > 0:
                    print(f"    Retries: {event.retry_count}")
                print()
        
        # Get comprehensive table counts
        print("\n📊 Complete Database Overview:")
        print("=" * 40)
        
        table_counts = get_all_table_counts(db)
        
        for category, tables in table_counts.items():
            print(f"\n🗂️  {category}:")
            print("-" * (len(category) + 5))
            for table_name, count in tables.items():
                status_icon = "✅" if count > 0 else "⚪"
                print(f"  {status_icon} {table_name}: {count:,}")
        
        # Calculate totals
        total_core = sum(table_counts.get('Core Tables', {}).values())
        total_events = sum(table_counts.get('Event Tables', {}).values()) 
        total_relationships = sum(table_counts.get('Relationship Tables', {}).values())
        grand_total = total_core + total_events + total_relationships
        
        print(f"\n📈 Summary:")
        print(f"  • Core Records: {total_core:,}")
        print(f"  • Event Records: {total_events:,}")
        print(f"  • Relationship Records: {total_relationships:,}")
        print(f"  • Total Records: {grand_total:,}")
        
        # Check related data
        print("\n📋 Recent Test Data Sample:")
        print("-" * 30)
        
        # Organizations
        org_count = db.query(Organization).count()
        print(f"Organizations: {org_count}")
        
        # Repositories  
        repo_count = db.query(Repository).count()
        print(f"Repositories: {repo_count}")
        
        # Users
        user_count = db.query(User).count()
        print(f"Users: {user_count}")
        
        # Sample of recent organizations
        recent_orgs = db.query(Organization).order_by(Organization.created_at.desc()).limit(5).all()
        if recent_orgs:
            print(f"\n🏢 Recent Organizations:")
            for org in recent_orgs:
                print(f"  • {org.login} (ID: {org.github_id})")
        
        # Sample of recent repositories
        recent_repos = db.query(Repository).order_by(Repository.created_at.desc()).limit(5).all()
        if recent_repos:
            print(f"\n📁 Recent Repositories:")
            for repo in recent_repos:
                print(f"  • {repo.full_name} (ID: {repo.github_id})")
        
        # Sample of recent users
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        if recent_users:
            print(f"\n👤 Recent Users:")
            for user in recent_users:
                print(f"  • {user.login} (ID: {user.github_id})")
        
        print("\n" + "=" * 50)
        print("✅ Inspection complete!")
        
        # Provide cleanup command
        print("\n💡 To clean up test data later, run:")
        print("python -c \"")
        print("from app.core.database import get_database")
        print("from app.models.core import WebhookEvent")
        print("db = next(get_database())")
        print("count = db.query(WebhookEvent).filter(WebhookEvent.delivery_id.like('%live-test%')).delete()")
        print("db.commit()")
        print("print(f'Deleted {count} test events')")
        print("\"")
        
    except Exception as e:
        print(f"❌ Error inspecting data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def show_all_table_counts():
    """Show total record counts for all tables in the system."""
    
    db_gen = get_database()
    db = next(db_gen)
    
    try:
        print("🗂️  Complete Database Table Overview")
        print("=" * 50)
        
        table_counts = get_all_table_counts(db)
        
        for category, tables in table_counts.items():
            print(f"\n📋 {category}:")
            print("-" * (len(category) + 6))
            for table_name, count in tables.items():
                status_icon = "✅" if count > 0 else "⚪"
                print(f"  {status_icon} {table_name:<25} : {count:>8,}")
        
        # Calculate totals
        total_core = sum(table_counts.get('Core Tables', {}).values())
        total_events = sum(table_counts.get('Event Tables', {}).values()) 
        total_relationships = sum(table_counts.get('Relationship Tables', {}).values())
        grand_total = total_core + total_events + total_relationships
        
        print(f"\n📈 Database Summary:")
        print("-" * 20)
        print(f"  • Core Records: {total_core:>15,}")
        print(f"  • Event Records: {total_events:>14,}")
        print(f"  • Relationship Records: {total_relationships:>7,}")
        print(f"  • {'─' * 25}")
        print(f"  • Total Records: {grand_total:>13,}")
        
        print("\n" + "=" * 50)
        print("✅ Table overview complete!")
        
    except Exception as e:
        print(f"❌ Error showing table counts: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    # Check if user wants to see all table counts
    if len(sys.argv) > 1 and sys.argv[1] == "--tables":
        show_all_table_counts()
    else:
        inspect_test_data()