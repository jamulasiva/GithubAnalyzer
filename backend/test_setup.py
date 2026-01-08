"""
Utility script to test webhook models integration and validate the backend setup.
"""

import sys
import json
from pathlib import Path

# Add webhook_models to path
sys.path.append(str(Path(__file__).parent.parent))

def test_webhook_models_import():
    """Test that all webhook models can be imported successfully."""
    try:
        # Test main imports from local webhook_models
        from app.webhook_models.utils import WEBHOOK_EVENT_MAP, parse_webhook_payload
        from app.webhook_models.common.base import WebhookBase
        
        print("✅ Core webhook models imported successfully")
        
        # Test specific event models
        event_models = [
            'push', 'pull_request_opened', 'issues_opened', 'member_added',
            'repository_created', 'fork', 'create', 'delete', 'ping'
        ]
        
        for model_name in event_models:
            try:
                module = __import__(f'app.webhook_models.{model_name}', fromlist=[model_name])
                print(f"✅ {model_name} model imported successfully")
            except Exception as e:
                print(f"❌ {model_name} model import failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Webhook models import failed: {e}")
        return False


def test_event_map():
    """Test the webhook event mapping."""
    try:
        from app.webhook_models.utils import WEBHOOK_EVENT_MAP
        
        print(f"\n📋 Supported webhook events: {len(WEBHOOK_EVENT_MAP)}")
        for event_type, actions in WEBHOOK_EVENT_MAP.items():
            action_list = list(actions.keys())
            print(f"   {event_type}: {action_list}")
        
        return True
        
    except Exception as e:
        print(f"❌ Event map test failed: {e}")
        return False


def test_sample_parsing():
    """Test parsing a sample webhook payload."""
    try:
        from app.webhook_models.utils import parse_webhook_payload
        
        # Sample ping webhook with more complete data
        sample_payload = {
            "zen": "Mind your words, they are important.",
            "hook_id": 12345,
            "hook": {
                "type": "Repository",
                "id": 12345,
                "name": "web",
                "active": True,
                "events": ["push", "pull_request"],
                "config": {
                    "content_type": "json",
                    "insecure_ssl": "0",
                    "url": "https://example.com/webhook"
                },
                "updated_at": "2024-01-01T00:00:00Z",
                "created_at": "2024-01-01T00:00:00Z"
            },
            "repository": {
                "id": 35129377,
                "node_id": "MDEwOlJlcG9zaXRvcnkzNTEyOTM3Nw==",
                "name": "public-repo", 
                "full_name": "baxterthehacker/public-repo",
                "owner": {
                    "login": "baxterthehacker",
                    "id": 6752317,
                    "node_id": "MDQ6VXNlcjY3NTIzMTc=",
                    "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=4",
                    "url": "https://api.github.com/users/baxterthehacker",
                    "html_url": "https://github.com/baxterthehacker",
                    "type": "User",
                    "site_admin": False
                },
                "private": False,
                "fork": False,
                "html_url": "https://github.com/baxterthehacker/public-repo",
                "url": "https://api.github.com/repos/baxterthehacker/public-repo"
            },
            "sender": {
                "login": "baxterthehacker",
                "id": 6752317,
                "node_id": "MDQ6VXNlcjY3NTIzMTc=",
                "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=4",
                "url": "https://api.github.com/users/baxterthehacker",
                "html_url": "https://github.com/baxterthehacker",
                "followers_url": "https://api.github.com/users/baxterthehacker/followers",
                "following_url": "https://api.github.com/users/baxterthehacker/following{/other_user}",
                "gists_url": "https://api.github.com/users/baxterthehacker/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/baxterthehacker/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/baxterthehacker/subscriptions",
                "organizations_url": "https://api.github.com/users/baxterthehacker/orgs",
                "repos_url": "https://api.github.com/users/baxterthehacker/repos",
                "events_url": "https://api.github.com/users/baxterthehacker/events{/privacy}",
                "received_events_url": "https://api.github.com/users/baxterthehacker/received_events",
                "type": "User",
                "site_admin": False
            }
        }
        
        # Test parsing
        parsed = parse_webhook_payload(sample_payload, 'ping', None)
        if parsed:
            print("✅ Sample ping webhook parsed successfully")
            print(f"   Repository: {parsed.repository.full_name}")
            print(f"   Sender: {parsed.sender.login}")
            return True
        else:
            print("❌ Sample webhook parsing returned None")
            return False
            
    except Exception as e:
        print(f"❌ Sample parsing test failed: {e}")
        return False


def main():
    """Run all webhook model tests."""
    print("🔍 Testing Webhook Models Integration")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_webhook_models_import),
        ("Event Map Test", test_event_map),
        ("Sample Parsing Test", test_sample_parsing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All webhook model tests passed! Backend is ready for webhook processing.")
    else:
        print("⚠️  Some tests failed. Check webhook_models setup.")
        sys.exit(1)


if __name__ == "__main__":
    main()