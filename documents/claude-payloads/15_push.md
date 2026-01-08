# Push Event

## Event Type
`push`


## Description
This event occurs related to push activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: push
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "ref": "refs/heads/main",
  "before": "0000000000000000000000000000000000000000",
  "after": "abcdef1234567890abcdef1234567890abcdef12",
  "repository": {
    "id": 186853002,
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World"
  },
  "pusher": {
    "name": "Codertocat",
    "email": "codertocat@github.com"
  },
  "sender": {
    "login": "Codertocat",
    "id": 21031067
  },
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "compare": "https://github.com/Codertocat/Hello-World/compare/000000000000...abcdef123456",
  "commits": [
    {
      "id": "abcdef1234567890abcdef1234567890abcdef12",
      "tree_id": "fedcba0987654321fedcba0987654321fedcba09",
      "distinct": true,
      "message": "Initial commit",
      "timestamp": "2023-03-17T15:42:05Z",
      "url": "https://github.com/Codertocat/Hello-World/commit/abcdef1234567890abcdef1234567890abcdef12",
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
      "added": [
        "README.md"
      ],
      "removed": [],
      "modified": []
    }
  ],
  "head_commit": {
    "id": "abcdef1234567890abcdef1234567890abcdef12",
    "tree_id": "fedcba0987654321fedcba0987654321fedcba09",
    "distinct": true,
    "message": "Initial commit",
    "timestamp": "2023-03-17T15:42:05Z",
    "url": "https://github.com/Codertocat/Hello-World/commit/abcdef1234567890abcdef1234567890abcdef12",
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
    "added": [
      "README.md"
    ],
    "removed": [],
    "modified": []
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
