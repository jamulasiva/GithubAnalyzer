# Pull Request Opened Event

## Event Type
`pull_request`

## Action
`opened`

## Description
This event occurs related to pull_request activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: pull_request
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "opened",
  "number": 1,
  "pull_request": {
    "id": 1,
    "node_id": "PR_kwDOAA==",
    "number": 1,
    "state": "open",
    "locked": false,
    "title": "Add new feature",
    "user": {
      "login": "octocat",
      "id": 1
    },
    "body": "This PR adds a new feature",
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z",
    "closed_at": null,
    "merged_at": null,
    "merge_commit_sha": null,
    "assignee": null,
    "assignees": [],
    "requested_reviewers": [],
    "requested_teams": [],
    "labels": [],
    "milestone": null,
    "draft": false,
    "head": {
      "label": "octocat:feature-branch",
      "ref": "feature-branch",
      "sha": "abcdef1234567890",
      "user": {
        "login": "octocat",
        "id": 1
      }
    },
    "base": {
      "label": "octocat:main",
      "ref": "main",
      "sha": "fedcba0987654321",
      "user": {
        "login": "octocat",
        "id": 1
      }
    },
    "author_association": "OWNER",
    "auto_merge": null,
    "active_lock_reason": null
  },
  "repository": {
    "id": 186853002,
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World"
  },
  "sender": {
    "login": "octocat",
    "id": 1
  }
}
```

## Key Payload Fields
- Repository information
- Sender/actor information  
- Event-specific data
- Timestamps

## Use Cases
- Event tracking and monitoring
- Automation triggers
- Analytics and reporting
- Audit logging
- Notifications

## API Processing Notes
1. Extract event-specific data from payload
2. Store in appropriate database tables
3. Trigger automated workflows if needed
4. Send notifications to relevant parties
5. Update dashboards and analytics

## Database Schema Considerations
- Store event metadata (type, action, timestamp)
- Store repository and user references
- Store full payload as JSONB for flexibility
- Index on common query fields
