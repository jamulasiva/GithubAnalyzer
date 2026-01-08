# Secret Scanning Alert Created

## Event Type
`secret_scanning_alert`

## Action
`created`

## Description
This event occurs related to secret_scanning_alert activities in GitHub repositories.

## Webhook Headers
```
X-GitHub-Event: secret_scanning_alert
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "alert": {
    "number": 1,
    "created_at": "2023-03-17T15:42:05Z",
    "url": "https://api.github.com/repos/Codertocat/Hello-World/secret-scanning/alerts/1",
    "html_url": "https://github.com/Codertocat/Hello-World/security/secret-scanning/1",
    "locations_url": "https://api.github.com/repos/Codertocat/Hello-World/secret-scanning/alerts/1/locations",
    "state": "open",
    "resolution": null,
    "resolved_at": null,
    "resolved_by": null,
    "secret_type": "github_personal_access_token",
    "secret_type_display_name": "GitHub Personal Access Token",
    "secret": "ghp_************************************",
    "push_protection_bypassed": false,
    "push_protection_bypassed_by": null,
    "push_protection_bypassed_at": null,
    "resolution_comment": null
  },
  "repository": {
    "id": 186853002,
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World"
  },
  "sender": {
    "login": "Codertocat",
    "id": 21031067
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
