# Member Permission Changed Event

## Event Type
`member`

## Action
`edited`

## Description
This event occurs when a collaborator's permissions on a repository are changed. This includes changes from read to write, write to admin, or any permission level modification.

## Availability
- Repositories
- Organizations
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Members" organization permission.

## When This Event Triggers
- A collaborator's permission level is changed (e.g., from read to write)
- Repository access permissions are modified for an existing member

## Webhook Headers
```
X-GitHub-Event: member
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Payload Structure

### Key Fields
| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Always "edited" for this event |
| `member` | object | The user whose permissions were changed |
| `changes` | object | Contains the old permission level |
| `changes.permission.from` | string | Previous permission level |
| `repository` | object | The repository where the event occurred |
| `sender` | object | The user who performed the action |

## Example Webhook Payload

```json
{
  "action": "edited",
  "changes": {
    "permission": {
      "from": "write",
      "to": "admin"
    }
  },
  "member": {
    "login": "octocat",
    "id": 1,
    "node_id": "MDQ6VXNlcjE=",
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "gravatar_id": "",
    "url": "https://api.github.com/users/octocat",
    "html_url": "https://github.com/octocat",
    "followers_url": "https://api.github.com/users/octocat/followers",
    "following_url": "https://api.github.com/users/octocat/following{/other_user}",
    "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
    "organizations_url": "https://api.github.com/users/octocat/orgs",
    "repos_url": "https://api.github.com/users/octocat/repos",
    "events_url": "https://api.github.com/users/octocat/events{/privacy}",
    "received_events_url": "https://api.github.com/users/octocat/received_events",
    "type": "User",
    "site_admin": false
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
      "node_id": "MDQ6VXNlcjIxMDMxMDY3",
      "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Codertocat",
      "html_url": "https://github.com/Codertocat",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/Codertocat/Hello-World",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/Codertocat/Hello-World",
    "created_at": "2019-05-15T15:19:25Z",
    "updated_at": "2019-05-15T15:20:41Z",
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
    "default_branch": "master"
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
    "description": ""
  }
}
```

## Permission Levels
GitHub repository permissions typically include:
- **read**: Can read and clone the repository
- **triage**: Can manage issues and pull requests without write access
- **write**: Can push to the repository
- **maintain**: Can manage the repository without access to sensitive or destructive actions
- **admin**: Full access to the repository including settings and deletion

## Use Cases
- **Security Auditing**: Track permission escalations
- **Compliance Monitoring**: Ensure permission changes follow approval processes
- **Access Control**: Monitor and alert on admin permission grants
- **Change Tracking**: Maintain history of permission modifications
- **Reporting**: Generate reports on access level changes

## Database Schema Suggestion
```sql
CREATE TABLE member_permission_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    member_login VARCHAR(255) NOT NULL,
    member_id BIGINT NOT NULL,
    old_permission VARCHAR(50),
    new_permission VARCHAR(50),
    repository_name VARCHAR(255) NOT NULL,
    repository_id BIGINT NOT NULL,
    repository_full_name VARCHAR(255) NOT NULL,
    organization_login VARCHAR(255),
    sender_login VARCHAR(255) NOT NULL,
    sender_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL
);
```

## API Processing Notes
1. Extract `changes.permission.from` for the old permission level
2. The current permission level is typically in `changes.permission.to` or needs to be fetched via API
3. Flag permission escalations (e.g., write → admin) for security review
4. Store both old and new permission levels
5. Create alerts for admin permission grants
6. Track who (`sender.login`) made the permission change
