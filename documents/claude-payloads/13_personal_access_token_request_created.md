# Personal Access Token Request Created

## Event Type
`personal_access_token_request`

## Action
`created`

## Description
This event occurs related to personal_access_token_request activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: personal_access_token_request
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "personal_access_token_request": {
    "id": 1,
    "owner": {
      "login": "octocat",
      "id": 1,
      "type": "User"
    },
    "permissions_added": {
      "organization": {
        "members": "read"
      },
      "repository": {
        "contents": "write",
        "pull_requests": "write"
      }
    },
    "permissions_upgraded": {},
    "permissions_result": {
      "organization": {
        "members": "read"
      },
      "repository": {
        "contents": "write",
        "pull_requests": "write"
      }
    },
    "repository_selection": "all",
    "repositories_url": "https://api.github.com/orgs/Octocoders/personal-access-token-requests/1/repositories",
    "created_at": "2023-03-17T15:42:05Z",
    "token_expired": false,
    "token_expires_at": "2024-03-17T15:42:05Z",
    "token_last_used_at": null
  },
  "organization": {
    "login": "Octocoders",
    "id": 38302899
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
