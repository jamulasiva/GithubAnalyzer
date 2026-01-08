# Repository Made Public Event

## Event Type
`repository`

## Action
`publicized`

## Description
This event occurs when a private repository is changed to public visibility. This is a significant security event as it makes previously private code visible to everyone.

## Availability
- Repositories
- Organizations
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Metadata" repository permission.

## When This Event Triggers
- A private repository is converted to public via settings
- Repository visibility is changed from private to public via API

## Webhook Headers
```
X-GitHub-Event: repository
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Example Webhook Payload

```json
{
  "action": "publicized",
  "repository": {
    "id": 186853002,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World",
    "private": false,
    "owner": {
      "login": "Codertocat",
      "id": 21031067,
      "node_id": "MDQ6VXNlcjIxMDMxMDY3",
      "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Codertocat",
      "html_url": "https://github.com/Codertocat",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/Codertocat/Hello-World",
    "description": "My first repository on GitHub!",
    "fork": false,
    "url": "https://api.github.com/repos/Codertocat/Hello-World",
    "created_at": "2019-05-15T15:19:25Z",
    "updated_at": "2019-05-15T15:21:03Z",
    "pushed_at": "2019-05-15T15:20:57Z",
    "git_url": "git://github.com/Codertocat/Hello-World.git",
    "ssh_url": "git@github.com:Codertocat/Hello-World.git",
    "clone_url": "https://github.com/Codertocat/Hello-World.git",
    "svn_url": "https://github.com/Codertocat/Hello-World",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "Ruby",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": true,
    "forks_count": 1,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 2,
    "license": null,
    "forks": 1,
    "open_issues": 2,
    "watchers": 0,
    "default_branch": "master",
    "visibility": "public"
  },
  "organization": {
    "login": "Octocoders",
    "id": 38302899,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjM4MzAyODk5",
    "url": "https://api.github.com/orgs/Octocoders",
    "repos_url": "https://api.github.com/orgs/Octocoders/repos",
    "events_url": "https://api.github.com/orgs/Octocoders/events",
    "hooks_url": "https://api.github.com/orgs/Octocoders/hooks",
    "issues_url": "https://api.github.com/orgs/Octocoders/issues",
    "members_url": "https://api.github.com/orgs/Octocoders/members{/member}",
    "public_members_url": "https://api.github.com/orgs/Octocoders/public_members{/member}",
    "avatar_url": "https://avatars1.githubusercontent.com/u/38302899?v=4",
    "description": "Code with the Octocoders"
  },
  "sender": {
    "login": "Codertocat",
    "id": 21031067,
    "node_id": "MDQ6VXNlcjIxMDMxMDY3",
    "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/Codertocat",
    "html_url": "https://github.com/Codertocat",
    "type": "User",
    "site_admin": false
  }
}
```

## Security Considerations
⚠️ **CRITICAL SECURITY EVENT** - This event requires immediate attention:
- All code, history, and issues are now publicly visible
- Secrets, credentials, and sensitive data are exposed
- Previous commits cannot be hidden (history is public)
- This action cannot be easily undone without consequences

## Use Cases
- **Security Alerts**: Send critical alerts to security teams
- **Secret Scanning**: Immediately scan repository for exposed secrets
- **Compliance Checks**: Verify if publicizing was authorized
- **Audit Logging**: Record who made the repository public and when
- **Incident Response**: Trigger security incident procedures if unauthorized
- **Data Loss Prevention**: Check for sensitive data exposure
- **License Updates**: Update license tracking (no longer consuming private seat)

## Database Schema Suggestion
```sql
CREATE TABLE repository_visibility_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    repository_name VARCHAR(255) NOT NULL,
    repository_id BIGINT NOT NULL,
    repository_full_name VARCHAR(255) NOT NULL,
    previous_visibility VARCHAR(50) DEFAULT 'private',
    current_visibility VARCHAR(50) NOT NULL,
    sender_login VARCHAR(255) NOT NULL,
    sender_id BIGINT NOT NULL,
    organization_login VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    security_scan_completed BOOLEAN DEFAULT FALSE,
    incident_created BOOLEAN DEFAULT FALSE,
    payload JSONB NOT NULL
);
```

## Immediate Actions to Take
1. **Secret Scanning**: Scan entire repository history for:
   - API keys and tokens
   - Database credentials
   - Private keys and certificates
   - AWS/Azure/GCP credentials
   - Passwords and connection strings

2. **Access Review**: Review who made the change
   - Was this authorized?
   - Does the person have authority to publicize?

3. **Content Review**: Check repository for:
   - Proprietary code
   - Customer data
   - Internal documentation
   - Configuration files with sensitive info

4. **Revoke Secrets**: If secrets found:
   - Immediately revoke all exposed credentials
   - Generate new secrets
   - Update systems using those secrets

## API Processing Notes
1. This is a HIGH PRIORITY event - process immediately
2. Record `repository.private` is now `false`
3. Store `repository.visibility` as "public"
4. Create security incident ticket automatically
5. Trigger secret scanning tools
6. Send notifications to security team
7. Update license/seat tracking
8. Consider automatic rollback if unauthorized

## Related Events
- `repository` with action `privatized` - Opposite action
- `public` - Alternative event type for this action
- `repository` with action `created` - If repository was created public
