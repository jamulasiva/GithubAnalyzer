# Deploy Key Created Event

## Event Type
`deploy_key`

## Action
`created`

## Description
This event occurs when a deploy key is added to a repository. Deploy keys are SSH keys that grant access to a single repository, commonly used for deployment automation.

## Availability
- Repositories
- Organizations
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Deployments" repository permission.

## When This Event Triggers
- A new deploy key is added to a repository
- SSH key is configured for deployment access

## Webhook Headers
```
X-GitHub-Event: deploy_key
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "key": {
    "id": 100,
    "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqLw...",
    "url": "https://api.github.com/repos/Codertocat/Hello-World/keys/100",
    "title": "Production Deploy Key",
    "verified": true,
    "created_at": "2023-03-17T15:42:05Z",
    "read_only": false
  },
  "repository": {
    "id": 186853002,
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World",
    "private": false,
    "owner": {
      "login": "Codertocat",
      "id": 21031067,
      "type": "User"
    }
  },
  "sender": {
    "login": "Codertocat",
    "id": 21031067,
    "type": "User"
  }
}
```

## Deploy Key Properties
- **read_only**: If true, key can only read (not write)
- **title**: Descriptive name for the key
- **verified**: Whether the key has been verified
- **key**: The public SSH key (partial in payload)

## Security Considerations
⚠️ Deploy keys provide repository access:
- Monitor who creates deploy keys
- Track read vs write access
- Review key titles for purpose
- Audit key usage regularly
- Rotate keys periodically

## Use Cases
- Deployment access tracking
- Security auditing
- Key management
- Access control monitoring

## Database Schema Suggestion
```sql
CREATE TABLE deploy_key_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE,
    action VARCHAR(50),
    key_id BIGINT,
    key_title VARCHAR(255),
    key_read_only BOOLEAN,
    repository_full_name VARCHAR(255),
    sender_login VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);
```
