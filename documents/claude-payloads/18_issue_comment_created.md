# Issue Comment Created Event

## Event Type
`issue_comment`

## Action
`created`

## Description
This event occurs related to issue_comment activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: issue_comment
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "issue": {
    "id": 1,
    "number": 1,
    "title": "Bug found in feature",
    "user": {
      "login": "octocat",
      "id": 1
    },
    "state": "open"
  },
  "comment": {
    "id": 1,
    "node_id": "IC_kwDOAA==",
    "url": "https://api.github.com/repos/octocat/Hello-World/issues/comments/1",
    "html_url": "https://github.com/octocat/Hello-World/issues/1#issuecomment-1",
    "body": "I can reproduce this issue",
    "user": {
      "login": "octocat",
      "id": 1
    },
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z",
    "author_association": "COLLABORATOR"
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
