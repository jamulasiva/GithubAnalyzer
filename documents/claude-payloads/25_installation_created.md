# Installation Created Event

## Event Type
`installation`

## Action
`created`

## Description
This event occurs related to installation activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: installation
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "installation": {
    "id": 1,
    "account": {
      "login": "octocat",
      "id": 1,
      "type": "User"
    },
    "repository_selection": "all",
    "access_tokens_url": "https://api.github.com/app/installations/1/access_tokens",
    "repositories_url": "https://api.github.com/installation/repositories",
    "html_url": "https://github.com/settings/installations/1",
    "app_id": 1,
    "target_id": 1,
    "target_type": "User",
    "permissions": {
      "metadata": "read",
      "contents": "read",
      "issues": "write"
    },
    "events": [
      "push",
      "pull_request"
    ],
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z",
    "single_file_name": null
  },
  "repositories": [
    {
      "id": 186853002,
      "name": "Hello-World",
      "full_name": "octocat/Hello-World",
      "private": false
    }
  ],
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
