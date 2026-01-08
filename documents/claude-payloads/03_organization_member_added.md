# Organization Member Added Event

## Event Type
`organization`

## Action
`member_added`

## Description
This event occurs when a user is added to a GitHub organization. This happens when someone accepts an invitation to join the organization or is directly added by an organization owner.

## Availability
- Organizations
- Enterprises
- GitHub Apps

## Required Permissions
GitHub App must have at least **read-level** access for the "Members" organization permission.

## When This Event Triggers
- A user accepts an organization invitation
- An organization owner directly adds a user to the organization
- A user's membership becomes active

## Webhook Headers
```
X-GitHub-Event: organization
X-GitHub-Delivery: <unique-delivery-id>
X-Hub-Signature-256: <signature>
Content-Type: application/json
```

## Payload Structure

### Key Fields
| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Always "member_added" for this event |
| `membership` | object | Details about the user's membership |
| `membership.user` | object | The user who was added |
| `membership.role` | string | The role assigned (member or admin) |
| `organization` | object | The organization to which the user was added |
| `sender` | object | The user who performed the action |

## Example Webhook Payload

```json
{
  "action": "member_added",
  "membership": {
    "url": "https://api.github.com/orgs/Octocoders/memberships/octocat",
    "state": "active",
    "role": "member",
    "organization_url": "https://api.github.com/orgs/Octocoders",
    "user": {
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
    }
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
  },
  "installation": {
    "id": 5,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uNQ=="
  }
}
```

## Organization Roles
- **member**: Regular organization member with default permissions
- **admin**: Organization administrator with full control

## Membership States
- **active**: User has accepted and is active in the organization
- **pending**: User has been invited but hasn't accepted yet

## Use Cases
- **Onboarding Tracking**: Monitor new organization members
- **Access Auditing**: Track when users gain organization access
- **Notifications**: Send welcome messages or setup instructions
- **License Management**: Track seat usage for paid plans
- **Security Monitoring**: Alert on unexpected member additions
- **Analytics**: Track organization growth over time

## Database Schema Suggestion
```sql
CREATE TABLE organization_member_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_login VARCHAR(255) NOT NULL,
    user_id BIGINT NOT NULL,
    membership_role VARCHAR(50) NOT NULL,
    membership_state VARCHAR(50) NOT NULL,
    organization_login VARCHAR(255) NOT NULL,
    organization_id BIGINT NOT NULL,
    sender_login VARCHAR(255) NOT NULL,
    sender_id BIGINT NOT NULL,
    enterprise_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL
);
```

## API Processing Notes
1. Extract `membership.user.login` for the new member
2. Record `membership.role` to distinguish between members and admins
3. Check `membership.state` - usually "active" for this event
4. Store `organization.login` for organization identification
5. Track `sender.login` for who added the member
6. Update license/seat tracking systems if applicable
7. Trigger onboarding workflows for new members

## Related Events
- `organization` with action `member_invited` - When invitation is sent
- `organization` with action `member_removed` - When member is removed
- `membership` with action `added` - When member is added to a team
