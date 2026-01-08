#!/usr/bin/env python3
"""
Script to analyze webhook events and diagnose missing relationship data.
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.core.database import get_database
from app.models.core import WebhookEvent
from app.models.events import MemberEvent, RepositoryEvent


def analyze_relationship_data():
    """Analyze webhook events to see what relationship data should exist."""
    
    db_gen = get_database()
    db = next(db_gen)
    
    try:
        print("🔍 Analyzing Relationship Data")
        print("=" * 40)
        
        # Get member and organization events
        member_events = db.query(WebhookEvent).filter(
            WebhookEvent.event_type.in_(['member', 'organization'])
        ).all()
        
        print(f"\n👥 Found {len(member_events)} member/organization webhook events:")
        print("-" * 50)
        
        for event in member_events:
            payload = event.payload
            action = payload.get('action', 'unknown')
            member_data = payload.get('member', {})
            membership_data = payload.get('membership', {})
            
            print(f"\n🔗 Event ID {event.id} ({event.event_type}):")
            print(f"   Action: {action}")
            print(f"   Delivery: {event.delivery_id}")
            print(f"   Org ID: {event.organization_id}")
            print(f"   Repo ID: {event.repository_id}")
            print(f"   Sender ID: {event.sender_id}")
            
            if member_data:
                print(f"   Member: {member_data.get('login', 'unknown')} (ID: {member_data.get('id')})")
            
            if membership_data:
                user = membership_data.get('user', {})
                print(f"   Membership User: {user.get('login', 'unknown')} (ID: {user.get('id')})")
                print(f"   Role: {membership_data.get('role', 'unknown')}")
                print(f"   State: {membership_data.get('state', 'unknown')}")
            
            # Check for permission information
            permission = payload.get('permission')
            if permission:
                print(f"   Permission: {permission}")
        
        # Check existing member events table
        print(f"\n📊 Member Events Table Analysis:")
        print("-" * 30)
        
        db_member_events = db.query(MemberEvent).all()
        print(f"Found {len(db_member_events)} records in member_events table:")
        
        for me in db_member_events:
            print(f"  • Action: {me.action}, Member ID: {me.member_id}, Org ID: {me.organization_id}")
        
        # Check repository events
        print(f"\n📁 Repository Events Analysis:")
        print("-" * 25)
        
        repo_events = db.query(WebhookEvent).filter(
            WebhookEvent.event_type == 'repository'
        ).all()
        
        for event in repo_events:
            payload = event.payload
            action = payload.get('action', 'unknown')
            print(f"  • Repo Event: {action} (ID: {event.id})")
        
        # Analyze what relationships should exist
        print(f"\n💡 Relationship Analysis:")
        print("-" * 22)
        
        # Look for organization members
        org_members = set()
        repo_collaborators = set()
        
        for event in member_events:
            payload = event.payload
            action = payload.get('action', '')
            
            # Extract member information
            member_data = payload.get('member', {})
            membership_data = payload.get('membership', {})
            
            if action in ['member_added', 'added'] and event.organization_id:
                if member_data and member_data.get('id'):
                    org_members.add((event.organization_id, member_data.get('id'), member_data.get('login')))
                elif membership_data and membership_data.get('user', {}).get('id'):
                    user = membership_data['user']
                    org_members.add((event.organization_id, user.get('id'), user.get('login')))
            
            # Repository collaborators
            if action == 'added' and event.repository_id and member_data:
                repo_collaborators.add((event.repository_id, member_data.get('id'), member_data.get('login')))
        
        print(f"Expected Organization Memberships: {len(org_members)}")
        for org_id, user_id, login in org_members:
            print(f"  • Org {org_id} + User {user_id} ({login})")
        
        print(f"\nExpected Repository Collaborators: {len(repo_collaborators)}")
        for repo_id, user_id, login in repo_collaborators:
            print(f"  • Repo {repo_id} + User {user_id} ({login})")
        
        # Check what users exist
        print(f"\n👤 Available Users:")
        print("-" * 15)
        
        from app.models.core import User
        users = db.query(User).all()
        
        for user in users:
            print(f"  • {user.login} (ID: {user.id}, GitHub ID: {user.github_id})")
        
        print("\n" + "=" * 40)
        print("✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    analyze_relationship_data()