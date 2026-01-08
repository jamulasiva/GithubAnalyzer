# Repository Ruleset Created Event

## Event Type
`repository_ruleset`

## Action
`created`

## Description
This event occurs when a repository ruleset is created. Rulesets are a newer way to enforce repository policies.

## Example Webhook Payload

```json
{
  "action": "created",
  "repository_ruleset": {
    "id": 42,
    "name": "Required CI Checks",
    "target": "branch",
    "source_type": "Repository",
    "source": "Codertocat/Hello-World",
    "enforcement": "active",
    "conditions": {
      "ref_name": {
        "include": [
          "refs/heads/main",
          "refs/heads/develop"
        ],
        "exclude": []
      }
    },
    "rules": [
      {
        "type": "required_status_checks",
        "parameters": {
          "required_status_checks": [
            {
              "context": "build",
              "integration_id": 1
            }
          ]
        }
      }
    ],
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z"
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

## Use Cases
- Security monitoring
- Vulnerability tracking
- Compliance reporting
- Automated remediation
- Alert notifications

## API Processing Notes
1. Extract alert details from payload
2. Store severity and affected components
3. Create tracking tickets
4. Send notifications to security team
5. Trigger automated scans if needed
