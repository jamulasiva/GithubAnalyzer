# Team Member Added Event

## Event Type
`membership`

## Action
`added`

## Description
This event occurs when an organization member is added to a team. Teams allow organizations to group members and manage their access to repositories.

## Availability
- Organizations
- Enterprises
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Members" organization permission.

## When This Event Triggers
- A user is added to a team
- An organization member joins a team
- Team membership is granted to a user

## Webhook Headers
```
X-GitHub-Event: membership
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Payload Structure

### Key Fields
| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Always "added" for this event |
| `scope` | string | Currently always "team" |
| `member` | object | The user who was added to the team |
| `team` | object | The team to which the member was added |
| `organization` | object | The organization that owns the team |
| `sender` | object | The user who performed the action |

## Example Webhook Payload

```json
{
  "action": "added",
  "scope": "team",
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
  "installation": {
    "id": 5,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uNQ=="
  },
  "enterprise": {
    "id": 1,
    "slug": "github",
    "name": "GitHub",
    "node_id": "MDEwOkVudGVycHJpc2Ux",
    "avatar_url": "https://avatars.githubusercontent.com/b/1?v=4",
    "description": null,
    "website_url": null,
    "html_url": "https://github.com/enterprises/github",
    "created_at": "2019-05-14T19:31:12Z",
    "updated_at": "2019-05-14T19:31:12Z"
  }
}
```

## Team Roles
Team members can have different roles:
- **member**: Regular team member
- **maintainer**: Can manage team settings and membership

Note: The team-level role is different from the organization-level role.

## Use Cases
- **Access Tracking**: Monitor when users gain team membership
- **Team Analytics**: Track team growth and composition changes
- **Notifications**: Notify team maintainers of new members
- **Onboarding**: Trigger team-specific onboarding processes
- **Security Auditing**: Track access changes through team membership
- **Reporting**: Generate team membership reports
- **Repository Access**: Since teams have repository access, this indirectly grants repository access

## Database Schema Suggestion
```sql
CREATE TABLE team_membership_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    scope VARCHAR(50) NOT NULL,
    member_login VARCHAR(255) NOT NULL,
    member_id BIGINT NOT NULL,
    team_name VARCHAR(255) NOT NULL,
    team_id BIGINT NOT NULL,
    team_slug VARCHAR(255) NOT NULL,
    team_privacy VARCHAR(50) NOT NULL,
    team_permission VARCHAR(50),
    organization_login VARCHAR(255) NOT NULL,
    organization_id BIGINT NOT NULL,
    sender_login VARCHAR(255) NOT NULL,
    sender_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL
);
```

## API Processing Notes
1. Extract `member.login` for the user added to the team
2. Record `team.slug` for team identification
3. Store `team.privacy` to understand team visibility
4. The `scope` field is currently always "team"
5. Consider fetching team repositories via API to determine what access this user now has
6. Update user-repository access matrices based on team membership
7. Send notifications to team maintainers if configured

## Important Considerations
- Adding a user to a team grants them access to all repositories the team has access to
- The permission level is determined by the team's permission on each repository
- Parent teams: If the team has a parent, check the `team.parent` field
- This event does NOT directly show which repositories the user can now access

## Related Events
- `membership` with action `removed` - When a member is removed from a team
- `team` with action `added_to_repository` - When a team gets repository access
- `team` with action `created` - When a new team is created
