# Fork Event

## Event Type
`fork`


## Description
This event occurs related to fork activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: fork
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "forkee": {
    "id": 186853003,
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "owner": {
      "login": "octocat",
      "id": 1
    },
    "private": false,
    "fork": true,
    "created_at": "2023-03-17T15:42:05Z"
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
