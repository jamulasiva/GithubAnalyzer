# Branch Protection Rule Created Event

## Event Type
`branch_protection_rule`

## Action
`created`

## Description
This event occurs when a branch protection rule is created for a repository. Branch protection rules help enforce workflows and protect important branches from unauthorized or accidental changes.

## Availability
- Repositories
- Organizations
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Administration" repository permission.

## When This Event Triggers
- A new branch protection rule is created
- Protection settings are applied to a branch pattern

## Webhook Headers
```
X-GitHub-Event: branch_protection_rule
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "created",
  "rule": {
    "id": 21,
    "repository_id": 186853002,
    "name": "main",
    "created_at": "2023-03-17T15:42:05.000Z",
    "updated_at": "2023-03-17T15:42:05.000Z",
    "pull_request_reviews_enforcement_level": "off",
    "required_approving_review_count": null,
    "dismiss_stale_reviews_on_push": false,
    "require_code_owner_review": false,
    "authorized_dismissal_actors_only": false,
    "ignore_approvals_from_contributors": false,
    "required_status_checks": [],
    "required_status_checks_enforcement_level": "off",
    "strict_required_status_checks_policy": false,
    "signature_requirement_enforcement_level": "off",
    "linear_history_requirement_enforcement_level": "off",
    "admin_enforced": false,
    "allow_force_pushes_enforcement_level": "off",
    "allow_deletions_enforcement_level": "off",
    "merge_queue_enforcement_level": "off",
    "required_deployments_enforcement_level": "off",
    "required_conversation_resolution_level": "off",
    "authorized_actors_only": false,
    "authorized_actor_names": []
  },
  "repository": {
    "id": 186853002,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World",
    "private": false,
    "owner": {
      "login": "Codertocat",
      "id": 21031067,
      "type": "User"
    },
    "html_url": "https://github.com/Codertocat/Hello-World",
    "description": null,
    "fork": false,
    "default_branch": "main"
  },
  "sender": {
    "login": "Codertocat",
    "id": 21031067,
    "type": "User"
  }
}
```

## Branch Protection Settings
- **require_pull_request_reviews**: Require PR reviews before merging
- **required_approving_review_count**: Number of approvals needed
- **dismiss_stale_reviews_on_push**: Dismiss old reviews on new commits
- **require_code_owner_review**: Require review from code owners
- **required_status_checks**: CI/CD checks that must pass
- **strict_required_status_checks**: Branch must be up to date before merge
- **enforce_admins**: Apply rules to administrators
- **require_linear_history**: Prevent merge commits
- **allow_force_pushes**: Allow force pushes
- **allow_deletions**: Allow branch deletion
- **require_signed_commits**: Require verified commits

## Use Cases
- Compliance tracking
- Security policy enforcement
- Audit logging
- Policy validation

## Database Schema Suggestion
```sql
CREATE TABLE branch_protection_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE,
    action VARCHAR(50),
    rule_id BIGINT,
    branch_name VARCHAR(255),
    repository_full_name VARCHAR(255),
    require_reviews BOOLEAN,
    required_approvals INTEGER,
    require_status_checks BOOLEAN,
    enforce_admins BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);
```
