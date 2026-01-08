# Issue Opened Event

## Event Type
`issues`

## Action
`opened`

## Description
This event occurs related to issues activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: issues
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "opened",
  "issue": {
    "id": 1,
    "node_id": "I_kwDOAA==",
    "number": 1,
    "title": "Bug found in feature",
    "user": {
      "login": "octocat",
      "id": 1
    },
    "labels": [],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [],
    "milestone": null,
    "comments": 0,
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z",
    "closed_at": null,
    "author_association": "OWNER",
    "active_lock_reason": null,
    "body": "I found a bug in the new feature...",
    "reactions": {
      "+1": 0,
      "-1": 0,
      "laugh": 0,
      "hooray": 0,
      "confused": 0,
      "heart": 0,
      "rocket": 0,
      "eyes": 0
    },
    "timeline_url": "https://api.github.com/repos/octocat/Hello-World/issues/1/timeline",
    "state_reason": null
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
