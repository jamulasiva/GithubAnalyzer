# Pull Request Review Submitted Event

## Event Type
`pull_request_review`

## Action
`submitted`

## Description
This event occurs related to pull_request_review activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: pull_request_review
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "submitted",
  "review": {
    "id": 1,
    "node_id": "PRR_kwDOAA==",
    "user": {
      "login": "octocat",
      "id": 1
    },
    "body": "Looks good to me!",
    "commit_id": "abcdef1234567890",
    "submitted_at": "2023-03-17T15:42:05Z",
    "state": "approved",
    "html_url": "https://github.com/octocat/Hello-World/pull/1#pullrequestreview-1",
    "pull_request_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1",
    "author_association": "COLLABORATOR"
  },
  "pull_request": {
    "id": 1,
    "number": 1,
    "state": "open",
    "title": "Add new feature",
    "user": {
      "login": "octocat",
      "id": 1
    }
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
