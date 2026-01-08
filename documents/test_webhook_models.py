"""
Test script to verify webhook models work correctly.
Run this to test the Pydantic models with sample data.
"""

import json
from webhook_models import MemberAddedEvent, RepositoryCreatedEvent, PushEvent
from webhook_models.utils import parse_webhook_payload


def test_member_added():
    """Test member added event parsing."""
    sample_payload = {
        "action": "added",
        "member": {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "site_admin": False
        },
        "repository": {
            "id": 186853002,
            "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
            "name": "Hello-World",
            "full_name": "Codertocat/Hello-World", 
            "private": False,
            "owner": {
                "login": "Codertocat",
                "id": 21031067,
                "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/Codertocat",
                "html_url": "https://github.com/Codertocat",
                "type": "User",
                "site_admin": False
            },
            "html_url": "https://github.com/Codertocat/Hello-World",
            "description": None,
            "fork": False,
            "url": "https://api.github.com/repos/Codertocat/Hello-World",
            "created_at": "2019-05-15T15:19:25Z",
            "updated_at": "2019-05-15T15:20:41Z",
            "default_branch": "master"
        },
        "sender": {
            "login": "Codertocat",
            "id": 21031067,
            "node_id": "MDQ6VXNlcjIxMDMxMDY3",
            "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/Codertocat",
            "html_url": "https://github.com/Codertocat",
            "type": "User",
            "site_admin": False
        }
    }
    
    # Test direct model instantiation
    event = MemberAddedEvent(**sample_payload)
    print(f"✅ Member Added Event: {event.member.login} added to {event.repository.full_name}")
    
    # Test using utility function
    event2 = parse_webhook_payload(sample_payload, "member", "added")
    print(f"✅ Parsed via utility: {type(event2).__name__}")
    
    return True


def test_push_event():
    """Test push event parsing.""" 
    sample_payload = {
        "ref": "refs/heads/main",
        "before": "0000000000000000000000000000000000000000",
        "after": "abcdef1234567890abcdef1234567890abcdef12",
        "created": False,
        "deleted": False,
        "forced": False,
        "base_ref": None,
        "compare": "https://github.com/Codertocat/Hello-World/compare/000000000000...abcdef123456",
        "commits": [
            {
                "id": "abcdef1234567890abcdef1234567890abcdef12",
                "tree_id": "fedcba0987654321fedcba0987654321fedcba09",
                "distinct": True,
                "message": "Initial commit",
                "timestamp": "2023-03-17T15:42:05Z",
                "url": "https://github.com/Codertocat/Hello-World/commit/abcdef123456",
                "author": {
                    "name": "Codertocat",
                    "email": "codertocat@github.com",
                    "username": "Codertocat"
                },
                "committer": {
                    "name": "Codertocat",
                    "email": "codertocat@github.com",
                    "username": "Codertocat"
                },
                "added": ["README.md"],
                "removed": [],
                "modified": []
            }
        ],
        "head_commit": {
            "id": "abcdef1234567890abcdef1234567890abcdef12",
            "tree_id": "fedcba0987654321fedcba0987654321fedcba09",
            "distinct": True,
            "message": "Initial commit",
            "timestamp": "2023-03-17T15:42:05Z",
            "url": "https://github.com/Codertocat/Hello-World/commit/abcdef123456",
            "author": {
                "name": "Codertocat",
                "email": "codertocat@github.com",
                "username": "Codertocat"
            },
            "committer": {
                "name": "Codertocat",
                "email": "codertocat@github.com",
                "username": "Codertocat"
            },
            "added": ["README.md"],
            "removed": [],
            "modified": []
        },
        "repository": {
            "id": 186853002,
            "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
            "name": "Hello-World",
            "full_name": "Codertocat/Hello-World",
            "private": False,
            "owner": {
                "login": "Codertocat",
                "id": 21031067,
                "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/Codertocat",
                "html_url": "https://github.com/Codertocat",
                "type": "User",
                "site_admin": False
            },
            "html_url": "https://github.com/Codertocat/Hello-World",
            "fork": False,
            "url": "https://api.github.com/repos/Codertocat/Hello-World"
        },
        "pusher": {
            "name": "Codertocat",
            "email": "codertocat@github.com"
        },
        "sender": {
            "login": "Codertocat",
            "id": 21031067,
            "node_id": "MDQ6VXNlcjIxMDMxMDY3",
            "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/Codertocat",
            "html_url": "https://github.com/Codertocat",
            "type": "User",
            "site_admin": False
        }
    }
    
    # Test push event parsing
    event = parse_webhook_payload(sample_payload, "push")
    print(f"✅ Push Event: {len(event.commits)} commit(s) to {event.repository.full_name}")
    print(f"   - Latest commit: {event.head_commit.message}")
    
    return True


if __name__ == "__main__":
    print("Testing GitHub Webhook Pydantic Models...")
    print("=" * 50)
    
    try:
        test_member_added()
        test_push_event()
        print("=" * 50)
        print("🎉 All tests passed! The webhook models are working correctly.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()