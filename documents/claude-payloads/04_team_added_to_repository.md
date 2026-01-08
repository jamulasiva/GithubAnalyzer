# Team Added to Repository Event

## Event Type
`team`

## Action
`added_to_repository`

## Description
This event occurs when a team is granted access to a repository. Teams provide a way to manage repository access for groups of organization members.

## Availability
- Organizations
- Enterprises
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Members" organization permission.

## When This Event Triggers
- An organization team is granted access to a repository
- A team's repository access is added through organization settings
- Team permissions are configured for a repository

## Webhook Headers
```
X-GitHub-Event: team
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Payload Structure

### Key Fields
| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Always "added_to_repository" for this event |
| `team` | object | The team that was granted access |
| `repository` | object | The repository to which the team was given access |
| `organization` | object | The organization that owns both the team and repository |
| `sender` | object | The user who performed the action |

## Example Webhook Payload

```json
{
  "action": "added_to_repository",
  "team": {
    "name": "github",
    "id": 3,
    "node_id": "MDQ6VGVhbTM=",
    "slug": "github",
    "description": "Open Source Team",
    "privacy": "secret",
    "url": "https://api.github.com/teams/3",
    "html_url": "https://github.com/orgs/Octocoders/teams/github",
    "members_url": "https://api.github.com/teams/3/members{/member}",
    "repositories_url": "https://api.github.com/teams/3/repos",
    "permission": "push",
    "parent": null
  },
  "repository": {
    "id": 186853002,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
    "name": "Hello-World",
    "full_name": "Octocoders/Hello-World",
    "private": false,
    "owner": {
      "login": "Octocoders",
      "id": 38302899,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjM4MzAyODk5",
      "avatar_url": "https://avatars1.githubusercontent.com/u/38302899?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Octocoders",
      "html_url": "https://github.com/Octocoders",
      "type": "Organization",
      "site_admin": false
    },
    "html_url": "https://github.com/Octocoders/Hello-World",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/Octocoders/Hello-World",
    "created_at": "2019-05-15T15:19:25Z",
    "updated_at": "2019-05-15T15:20:41Z",
    "pushed_at": "2019-05-15T15:20:57Z",
    "git_url": "git://github.com/Octocoders/Hello-World.git",
    "ssh_url": "git@github.com:Octocoders/Hello-World.git",
    "clone_url": "https://github.com/Octocoders/Hello-World.git",
    "svn_url": "https://github.com/Octocoders/Hello-World",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 2,
    "license": null,
    "forks": 0,
    "open_issues": 2,
    "watchers": 0,
    "default_branch": "master"
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
  },
  "installation": {
    "id": 5,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uNQ=="
  }
}
```

## Team Privacy Settings
- **secret**: Only visible to organization owners and members of this team
- **closed**: Visible to all organization members

## Team Permission Levels
- **pull**: Read-only access
- **push**: Read and write access
- **admin**: Full administrative access
- **maintain**: Repository maintenance without sensitive operations
- **triage**: Manage issues and PRs without write access

## Use Cases
- **Access Management**: Track which teams have access to which repositories
- **Security Auditing**: Monitor repository access grants to teams
- **Compliance**: Ensure team access follows organizational policies
- **Reporting**: Generate reports on repository access patterns
- **Notifications**: Alert team leads when their teams get new repository access
- **Access Reviews**: Facilitate periodic access reviews

## Database Schema Suggestion
```sql
CREATE TABLE team_repository_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    team_name VARCHAR(255) NOT NULL,
    team_id BIGINT NOT NULL,
    team_slug VARCHAR(255) NOT NULL,
    team_permission VARCHAR(50) NOT NULL,
    team_privacy VARCHAR(50) NOT NULL,
    repository_name VARCHAR(255) NOT NULL,
    repository_id BIGINT NOT NULL,
    repository_full_name VARCHAR(255) NOT NULL,
    organization_login VARCHAR(255) NOT NULL,
    organization_id BIGINT NOT NULL,
    sender_login VARCHAR(255) NOT NULL,
    sender_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL
);
```

## API Processing Notes
1. Extract `team.slug` for team identification
2. Record `team.permission` for the access level granted
3. Store `repository.full_name` for repository reference
4. Track `team.privacy` to understand team visibility
5. Note that all team members now have access to the repository
6. Consider fetching team members via API if you need individual user tracking
7. Update access control matrices in your system

## Related Events
- `team` with action `removed_from_repository` - When team access is revoked
- `team` with action `edited` - When team settings are modified
- `membership` with action `added` - When individuals join the team
