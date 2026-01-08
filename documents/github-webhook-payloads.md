# GitHub Webhook Payloads - Complete Reference

This document provides comprehensive JSON payload examples for all webhook events supported by our GitHub audit platform. These payloads show the exact structure and data that GitHub sends to our webhook endpoints, organized by priority and functionality.

## Table of Contents

1. [Webhook Headers & Verification](#webhook-headers--verification)
2. [Priority 1: Repository Access Management](#priority-1-repository-access-management-events)
3. [Priority 2: Repository Lifecycle](#priority-2-repository-lifecycle-events)
4. [Priority 3: Security & Compliance](#priority-3-security-and-compliance-events)
5. [Priority 4: Development Activity](#priority-4-development-activity-events)
6. [Priority 5: Communication & Collaboration](#priority-5-communication--collaboration-events)
7. [Priority 6: Git Operations](#priority-6-git-operations-events)
8. [Priority 7: System & Administrative](#priority-7-system--administrative-events)
9. [Common Payload Fields](#common-payload-fields)
10. [Database Mapping Guidelines](#database-mapping-guidelines)

## Webhook Headers & Verification

All webhook payloads include these HTTP headers for authentication and identification:

```http
POST /webhook HTTP/1.1
Host: your-webhook-url.com
X-GitHub-Event: member
X-GitHub-Delivery: 72d3162e-cc78-11e3-81ab-4c9367dc0958
X-Hub-Signature-256: sha256=d57c68ca6f92289e6987922ff26938930f6e66a2d161ef06abdf1859230aa23c
User-Agent: GitHub-Hookshot/044aadd
Content-Type: application/json
Content-Length: 6615
X-GitHub-Hook-ID: 292430182
X-GitHub-Hook-Installation-Target-ID: 79929171
X-GitHub-Hook-Installation-Target-Type: repository
```

### Signature Verification

**Critical**: Always verify webhook signatures using HMAC SHA-256 with your webhook secret:

```python
import hmac
import hashlib

def verify_signature(payload_body, signature_header, webhook_secret):
    signature = hmac.new(
        webhook_secret.encode('utf-8'), 
        payload_body, 
        hashlib.sha256
    ).hexdigest()
    expected_signature = f"sha256={signature}"
    return hmac.compare_digest(expected_signature, signature_header)
```

---

## Priority 1: Repository Access Management Events

### 1. Member Event (Repository Collaborator Changes)

**Event:** `member`
**Actions:** `added`, `removed`, `edited`
**Description:** Triggered when repository collaborators are added, removed, or have permissions changed.

#### Member Added Payload
```json
{
  "action": "added",
  "member": {
    "login": "johndoe",
    "id": 12345678,
    "node_id": "MDQ6VXNlcjEyMzQ1Njc4",
    "avatar_url": "https://github.com/images/error/johndoe_happy.gif",
    "gravatar_id": "",
    "url": "https://api.github.com/users/johndoe",
    "html_url": "https://github.com/johndoe",
    "followers_url": "https://api.github.com/users/johndoe/followers",
    "following_url": "https://api.github.com/users/johndoe/following{/other_user}",
    "gists_url": "https://api.github.com/users/johndoe/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/johndoe/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/johndoe/subscriptions",
    "organizations_url": "https://api.github.com/users/johndoe/orgs",
    "repos_url": "https://api.github.com/users/johndoe/repos",
    "events_url": "https://api.github.com/users/johndoe/events{/privacy}",
    "received_events_url": "https://api.github.com/users/johndoe/received_events",
    "type": "User",
    "site_admin": false
  },
  "changes": {
    "permission": {
      "from": null
    }
  },
  "repository": {
    "id": 35129377,
    "node_id": "MDEwOlJlcG9zaXRvcnkzNTEyOTM3Nw==",
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "owner": {
      "login": "baxterthehacker",
      "id": 6752317,
      "node_id": "MDQ6VXNlcjY3NTIzMTc=",
      "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
      "gravatar_id": "",
      "url": "https://api.github.com/users/baxterthehacker",
      "html_url": "https://github.com/baxterthehacker",
      "type": "User",
      "site_admin": false
    },
    "private": false,
    "html_url": "https://github.com/baxterthehacker/public-repo",
    "description": "This your first repo!",
    "fork": false,
    "url": "https://api.github.com/repos/baxterthehacker/public-repo",
    "created_at": "2015-05-05T23:40:12Z",
    "updated_at": "2015-05-05T23:40:12Z",
    "pushed_at": "2015-05-05T23:40:27Z",
    "git_url": "git://github.com/baxterthehacker/public-repo.git",
    "ssh_url": "git@github.com:baxterthehacker/public-repo.git",
    "clone_url": "https://github.com/baxterthehacker/public-repo.git",
    "svn_url": "https://github.com/baxterthehacker/public-repo",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "open_issues_count": 0,
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master",
    "permissions": {
      "admin": false,
      "push": false,
      "pull": true
    }
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "node_id": "MDQ6VXNlcjY3NTIzMTc=",
    "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
    "gravatar_id": "",
    "url": "https://api.github.com/users/baxterthehacker",
    "html_url": "https://github.com/baxterthehacker",
    "type": "User",
    "site_admin": false
  }
}
```

#### Member Permission Changed Payload
```json
{
  "action": "edited",
  "member": {
    "login": "johndoe",
    "id": 12345678,
    "type": "User",
    "site_admin": false
  },
  "changes": {
    "permission": {
      "from": "read",
      "to": "write"
    }
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false,
    "permissions": {
      "admin": false,
      "push": true,
      "pull": true
    }
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 2. Organization Event (Organization Membership Changes)

**Event:** `organization`
**Actions:** `member_added`, `member_removed`, `member_invited`
**Description:** Triggered when organization membership changes.

#### Organization Member Added Payload
```json
{
  "action": "member_added",
  "membership": {
    "url": "https://api.github.com/orgs/github/memberships/baxterthehacker",
    "state": "active",
    "role": "member",
    "organization_url": "https://api.github.com/orgs/github",
    "user": {
      "login": "baxterthehacker",
      "id": 6752317,
      "node_id": "MDQ6VXNlcjY3NTIzMTc=",
      "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
      "type": "User",
      "site_admin": false
    }
  },
  "organization": {
    "login": "github",
    "id": 872781,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjg3Mjc4MQ==",
    "url": "https://api.github.com/orgs/github",
    "repos_url": "https://api.github.com/orgs/github/repos",
    "events_url": "https://api.github.com/orgs/github/events",
    "hooks_url": "https://api.github.com/orgs/github/hooks",
    "issues_url": "https://api.github.com/orgs/github/issues",
    "members_url": "https://api.github.com/orgs/github/members{/member}",
    "public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
    "avatar_url": "https://github.com/images/error/github_happy.gif",
    "description": "A great organization",
    "gravatar_id": "",
    "name": "github",
    "company": "GitHub",
    "blog": "https://github.com/blog",
    "location": "San Francisco",
    "email": "octocat@github.com",
    "has_organization_projects": true,
    "has_repository_projects": true,
    "public_repos": 2,
    "public_gists": 1,
    "followers": 20,
    "following": 0,
    "html_url": "https://github.com/github",
    "created_at": "2008-05-11T04:37:31Z",
    "type": "Organization"
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 3. Team Event (Team Management)

**Event:** `team`
**Actions:** `created`, `deleted`, `edited`, `added_to_repository`, `removed_from_repository`
**Description:** Triggered when teams are managed or their repository access changes.

#### Team Added to Repository Payload
```json
{
  "action": "added_to_repository",
  "team": {
    "name": "justice-league",
    "id": 1234567,
    "node_id": "MDQ6VGVhbTEyMzQ1Njc=",
    "slug": "justice-league",
    "description": "A great team.",
    "privacy": "closed",
    "url": "https://api.github.com/teams/1234567",
    "html_url": "https://github.com/orgs/github/teams/justice-league",
    "members_url": "https://api.github.com/teams/1234567/members{/member}",
    "repositories_url": "https://api.github.com/teams/1234567/repos",
    "permission": "write",
    "created_at": "2017-07-14T16:53:42Z",
    "updated_at": "2017-07-14T16:53:42Z",
    "members_count": 3,
    "repos_count": 10,
    "organization": {
      "login": "github",
      "id": 872781,
      "type": "Organization"
    },
    "parent": null
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "github/public-repo",
    "private": false,
    "permissions": {
      "admin": false,
      "push": true,
      "pull": true
    }
  },
  "organization": {
    "login": "github",
    "id": 872781,
    "type": "Organization"
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 4. Membership Event (Team Membership Changes)

**Event:** `membership`
**Actions:** `added`, `removed`
**Description:** Triggered when users are added to or removed from teams.

#### Team Member Added Payload
```json
{
  "action": "added",
  "scope": "team",
  "member": {
    "login": "baxterthehacker",
    "id": 6752317,
    "node_id": "MDQ6VXNlcjY3NTIzMTc=",
    "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
    "type": "User",
    "site_admin": false
  },
  "team": {
    "name": "justice-league",
    "id": 1234567,
    "slug": "justice-league",
    "description": "A great team.",
    "privacy": "closed",
    "permission": "write",
    "url": "https://api.github.com/teams/1234567",
    "members_url": "https://api.github.com/teams/1234567/members{/member}",
    "repositories_url": "https://api.github.com/teams/1234567/repos",
    "members_count": 4,
    "repos_count": 10
  },
  "organization": {
    "login": "github",
    "id": 872781,
    "type": "Organization"
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

## Priority 2: Repository Lifecycle Events

### 5. Repository Event (Repository Management)

**Event:** `repository`
**Actions:** `created`, `deleted`, `archived`, `unarchived`, `privatized`, `publicized`, `transferred`
**Description:** Triggered when repositories are created, deleted, or have settings changed.

#### Repository Created Payload
```json
{
  "action": "created",
  "repository": {
    "id": 35129377,
    "node_id": "MDEwOlJlcG9zaXRvcnkzNTEyOTM3Nw==",
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "owner": {
      "login": "baxterthehacker",
      "id": 6752317,
      "type": "User",
      "site_admin": false
    },
    "private": false,
    "html_url": "https://github.com/baxterthehacker/public-repo",
    "description": "This your first repo!",
    "fork": false,
    "url": "https://api.github.com/repos/baxterthehacker/public-repo",
    "created_at": "2015-05-05T23:40:12Z",
    "updated_at": "2015-05-05T23:40:12Z",
    "pushed_at": "2015-05-05T23:40:27Z",
    "git_url": "git://github.com/baxterthehacker/public-repo.git",
    "ssh_url": "git@github.com:baxterthehacker/public-repo.git",
    "clone_url": "https://github.com/baxterthehacker/public-repo.git",
    "svn_url": "https://github.com/baxterthehacker/public-repo",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 0,
    "license": null,
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master",
    "permissions": {
      "admin": true,
      "push": true,
      "pull": true
    }
  },
  "organization": {
    "login": "github",
    "id": 872781,
    "type": "Organization"
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 6. Public Event (Repository Visibility Change)

**Event:** `public`
**Description:** Triggered when a private repository is made public.

#### Repository Made Public Payload
```json
{
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false,
    "html_url": "https://github.com/baxterthehacker/public-repo",
    "description": "This your first repo!",
    "created_at": "2015-05-05T23:40:12Z",
    "updated_at": "2015-05-05T23:40:12Z",
    "permissions": {
      "admin": true,
      "push": true,
      "pull": true
    }
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

## Priority 3: Security and Compliance Events

### 7. Branch Protection Rule Event

**Event:** `branch_protection_rule`
**Actions:** `created`, `edited`, `deleted`
**Description:** Triggered when branch protection rules are modified.

#### Branch Protection Rule Created Payload
```json
{
  "action": "created",
  "rule": {
    "id": 12345,
    "repository_id": 35129377,
    "name": "main",
    "created_at": "2022-01-01T12:00:00Z",
    "updated_at": "2022-01-01T12:00:00Z",
    "pull_request_reviews_enforcement_level": "non_admins",
    "required_status_checks_enforcement_level": "non_admins",
    "strict_required_status_checks_policy": true,
    "dismiss_stale_reviews_on_push": true,
    "require_code_owner_review": true,
    "required_approving_review_count": 2,
    "restrictions_push_access": ["teams"],
    "restrictions_users": [],
    "restrictions_teams": ["justice-league"],
    "restrictions_apps": [],
    "required_status_checks": [
      {
        "context": "continuous-integration",
        "app_id": null
      }
    ]
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 8. Deploy Key Event

**Event:** `deploy_key`
**Actions:** `created`, `deleted`
**Description:** Triggered when deploy keys are added or removed.

#### Deploy Key Created Payload
```json
{
  "action": "created",
  "key": {
    "id": 123456,
    "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...",
    "url": "https://api.github.com/repos/baxterthehacker/public-repo/keys/123456",
    "title": "Production Deploy Key",
    "verified": true,
    "created_at": "2022-01-01T12:00:00Z",
    "read_only": true,
    "added_by": "baxterthehacker"
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### Repository Ruleset Event

**Event:** `repository_ruleset`  
**Actions:** `created`, `edited`, `deleted`  
**Description:** Triggered when repository rulesets are created, edited, or deleted.

#### Repository Ruleset Created Payload
```json
{
  "action": "created",
  "repository_ruleset": {
    "id": 456789,
    "name": "main-branch-protection",
    "target": "branch",
    "source_type": "Repository",
    "source": "orgname/audit-platform",
    "enforcement": "active",
    "bypass_actors": [
      {
        "actor_id": 987654321,
        "actor_type": "OrganizationAdmin",
        "bypass_mode": "always"
      }
    ],
    "rules": [
      {
        "type": "required_status_checks",
        "parameters": {
          "strict_required_status_checks_policy": true,
          "required_status_checks": [
            {
              "context": "security-scan",
              "integration_id": 12345
            }
          ]
        }
      },
      {
        "type": "pull_request",
        "parameters": {
          "dismiss_stale_reviews_on_push": true,
          "require_code_owner_review": true,
          "required_approving_review_count": 2
        }
      }
    ],
    "conditions": {
      "ref_name": {
        "include": ["refs/heads/main"],
        "exclude": []
      }
    },
    "created_at": "2024-01-15T16:00:00Z",
    "updated_at": "2024-01-15T16:00:00Z"
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "security-admin",
    "id": 567890,
    "type": "User"
  }
}
```

**Database Mapping:** `security_events` table with fields: `ruleset_id`, `action`, `repository_id`, `sender_id`

### Code Scanning Alert Event

**Event:** `code_scanning_alert`  
**Actions:** `created`, `fixed`, `dismissed`  
**Description:** Triggered when code scanning alerts are created, fixed, or dismissed.

#### Code Scanning Alert Created Payload
```json
{
  "action": "created",
  "alert": {
    "number": 1,
    "created_at": "2024-01-15T17:00:00Z",
    "updated_at": "2024-01-15T17:00:00Z",
    "url": "https://api.github.com/repos/orgname/audit-platform/code-scanning/alerts/1",
    "html_url": "https://github.com/orgname/audit-platform/security/code-scanning/1",
    "state": "open",
    "fixed_at": null,
    "dismissed_by": null,
    "dismissed_at": null,
    "dismissed_reason": null,
    "rule": {
      "id": "js/sql-injection",
      "severity": "error",
      "description": "Database query built from user-controlled sources",
      "name": "js/sql-injection",
      "full_description": "Building a database query from user-controlled sources is vulnerable to insertion of malicious SQL code by the user.",
      "tags": ["security", "external/cwe/cwe-89"]
    },
    "tool": {
      "name": "CodeQL",
      "guid": null,
      "version": "2.15.1"
    },
    "most_recent_instance": {
      "ref": "refs/heads/main",
      "analysis_key": "v1.0.0-20240115170000",
      "environment": "production",
      "state": "open",
      "commit_sha": "abc123def456",
      "message": {
        "text": "Potential SQL injection vulnerability"
      },
      "location": {
        "path": "src/database/queries.js",
        "start_line": 42,
        "end_line": 42,
        "start_column": 15,
        "end_column": 30
      },
      "classifications": ["test"]
    }
  },
  "ref": "refs/heads/main",
  "commit_oid": "abc123def456",
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "github-actions[bot]",
    "id": 41898282,
    "type": "Bot"
  }
}
```

**Database Mapping:** `security_events` table with fields: `alert_number`, `rule_id`, `alert_state`, `repository_id`

### Dependabot Alert Event

**Event:** `dependabot_alert`  
**Actions:** `created`, `fixed`, `dismissed`  
**Description:** Triggered when Dependabot alerts are created, fixed, or dismissed.

#### Dependabot Alert Created Payload
```json
{
  "action": "created",
  "alert": {
    "number": 5,
    "state": "open",
    "dependency": {
      "package": {
        "ecosystem": "npm",
        "name": "lodash"
      },
      "manifest_path": "package.json",
      "scope": "runtime"
    },
    "security_advisory": {
      "ghsa_id": "GHSA-jf85-cpcp-j695",
      "cve_id": "CVE-2021-23337",
      "summary": "Command Injection in lodash",
      "description": "lodash versions prior to 4.17.21 are vulnerable to Command Injection via the template function.",
      "vulnerabilities": [
        {
          "package": {
            "ecosystem": "npm",
            "name": "lodash"
          },
          "severity": "high",
          "vulnerable_version_range": "< 4.17.21",
          "first_patched_version": {
            "identifier": "4.17.21"
          }
        }
      ],
      "severity": "high",
      "cvss": {
        "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "score": 9.8
      },
      "published_at": "2021-02-15T11:10:00Z",
      "updated_at": "2021-02-15T11:10:00Z"
    },
    "security_vulnerability": {
      "package": {
        "ecosystem": "npm",
        "name": "lodash"
      },
      "severity": "high",
      "vulnerable_version_range": "< 4.17.21",
      "first_patched_version": {
        "identifier": "4.17.21"
      }
    },
    "url": "https://api.github.com/repos/orgname/audit-platform/dependabot/alerts/5",
    "html_url": "https://github.com/orgname/audit-platform/security/dependabot/5",
    "created_at": "2024-01-15T18:00:00Z",
    "updated_at": "2024-01-15T18:00:00Z",
    "dismissed_at": null,
    "dismissed_by": null,
    "dismissed_reason": null,
    "dismissed_comment": null,
    "fixed_at": null
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "dependabot[bot]",
    "id": 49699333,
    "type": "Bot"
  }
}
```

**Database Mapping:** `security_events` table with fields: `alert_number`, `ghsa_id`, `alert_state`, `repository_id`

### Personal Access Token Request Event

**Event:** `personal_access_token_request`  
**Actions:** `created`, `approved`, `denied`  
**Description:** Triggered when fine-grained personal access token requests are created, approved, or denied.

#### Personal Access Token Request Created Payload
```json
{
  "action": "created",
  "personal_access_token_request": {
    "id": 345678901,
    "owner": {
      "login": "external-contractor",
      "id": 234567,
      "type": "User"
    },
    "permissions_added": {
      "repository": {
        "contents": "read",
        "metadata": "read",
        "pull_requests": "read"
      },
      "organization": {
        "members": "read"
      }
    },
    "permissions_upgraded": {},
    "permissions_result": {
      "repository": {
        "contents": "read",
        "metadata": "read",
        "pull_requests": "read"
      },
      "organization": {
        "members": "read"
      }
    },
    "repository_selection": "selected",
    "repository_count": 1,
    "repositories": [
      {
        "full_name": "orgname/audit-platform",
        "id": 123456789,
        "name": "audit-platform",
        "node_id": "R_kgDOABCDEFG"
      }
    ],
    "created_at": "2024-01-15T23:00:00Z",
    "token_expired": false,
    "token_expires_at": "2024-04-15T23:00:00Z",
    "token_last_used_at": null,
    "reason": "Need access to read repository contents for security audit"
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "external-contractor",
    "id": 234567,
    "type": "User"
  }
}
```

**Database Mapping:** `access_control_events` table with fields: `token_request_id`, `action`, `organization_id`, `sender_id`

---

## Priority 5: Communication & Collaboration Events

### Issue Comment Event

**Event:** `issue_comment`  
**Actions:** `created`, `edited`, `deleted`  
**Description:** Triggered when a comment is created, edited, or deleted on an issue or pull request.

#### Issue Comment Created Payload
```json
{
  "action": "created",
  "issue": {
    "url": "https://api.github.com/repos/orgname/audit-platform/issues/15",
    "repository_url": "https://api.github.com/repos/orgname/audit-platform",
    "number": 15,
    "title": "Implement user authentication",
    "user": {
      "login": "product-manager",
      "id": 678901,
      "type": "User"
    },
    "state": "open",
    "locked": false,
    "assignee": {
      "login": "developer",
      "id": 123456,
      "type": "User"
    },
    "assignees": [
      {
        "login": "developer",
        "id": 123456,
        "type": "User"
      }
    ],
    "milestone": null,
    "comments": 3,
    "created_at": "2024-01-14T10:00:00Z",
    "updated_at": "2024-01-15T19:00:00Z",
    "closed_at": null,
    "author_association": "MEMBER",
    "body": "We need to implement OAuth2 authentication for the audit platform."
  },
  "comment": {
    "url": "https://api.github.com/repos/orgname/audit-platform/issues/comments/567890123",
    "html_url": "https://github.com/orgname/audit-platform/issues/15#issuecomment-567890123",
    "issue_url": "https://api.github.com/repos/orgname/audit-platform/issues/15",
    "id": 567890123,
    "node_id": "IC_kwDOABCDEFG4IjY3",
    "user": {
      "login": "developer",
      "id": 123456,
      "type": "User"
    },
    "created_at": "2024-01-15T19:00:00Z",
    "updated_at": "2024-01-15T19:00:00Z",
    "author_association": "COLLABORATOR",
    "body": "I'll start working on the OAuth2 integration using Supabase Auth. ETA is 3 days."
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "developer",
    "id": 123456,
    "type": "User"
  }
}
```

**Database Mapping:** `collaboration_activities` table with fields: `comment_id`, `issue_number`, `repository_id`, `sender_id`

### Pull Request Review Event

**Event:** `pull_request_review`  
**Actions:** `submitted`, `edited`, `dismissed`  
**Description:** Triggered when a pull request review is submitted, edited, or dismissed.

#### Pull Request Review Submitted Payload
```json
{
  "action": "submitted",
  "review": {
    "id": 789012345,
    "node_id": "PRR_kwDOABCDEFG4LzQ5",
    "user": {
      "login": "senior-developer",
      "id": 789012,
      "type": "User"
    },
    "body": "Great implementation! Just one suggestion about error handling.",
    "commit_id": "def456abc123",
    "submitted_at": "2024-01-15T20:00:00Z",
    "state": "approved",
    "html_url": "https://github.com/orgname/audit-platform/pull/8#pullrequestreview-789012345",
    "pull_request_url": "https://api.github.com/repos/orgname/audit-platform/pulls/8",
    "author_association": "COLLABORATOR"
  },
  "pull_request": {
    "url": "https://api.github.com/repos/orgname/audit-platform/pulls/8",
    "id": 890123456,
    "number": 8,
    "state": "open",
    "locked": false,
    "title": "Add OAuth2 authentication",
    "user": {
      "login": "developer",
      "id": 123456,
      "type": "User"
    },
    "body": "Implements OAuth2 authentication using Supabase Auth as requested in #15",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T20:00:00Z",
    "closed_at": null,
    "merged_at": null,
    "merge_commit_sha": null,
    "assignee": null,
    "assignees": [],
    "requested_reviewers": [],
    "requested_teams": [],
    "head": {
      "label": "orgname:feature/oauth2-auth",
      "ref": "feature/oauth2-auth",
      "sha": "def456abc123"
    },
    "base": {
      "label": "orgname:main",
      "ref": "main",
      "sha": "abc123def456"
    },
    "author_association": "COLLABORATOR",
    "draft": false,
    "merged": false,
    "mergeable": true,
    "rebaseable": true,
    "mergeable_state": "clean",
    "comments": 2,
    "review_comments": 1,
    "commits": 5,
    "additions": 150,
    "deletions": 20,
    "changed_files": 8
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "senior-developer",
    "id": 789012,
    "type": "User"
  }
}
```

**Database Mapping:** `collaboration_activities` table with fields: `review_id`, `pull_request_number`, `review_state`, `repository_id`, `sender_id`

---

**Event:** `secret_scanning_alert`
**Actions:** `created`, `reopened`, `resolved`
**Description:** Triggered when secret scanning detects or resolves secrets.

#### Secret Scanning Alert Created Payload
```json
{
  "action": "created",
  "alert": {
    "number": 42,
    "created_at": "2022-01-01T12:00:00Z",
    "updated_at": "2022-01-01T12:00:00Z",
    "url": "https://api.github.com/repos/baxterthehacker/public-repo/secret-scanning/alerts/42",
    "html_url": "https://github.com/baxterthehacker/public-repo/security/secret-scanning/42",
    "state": "open",
    "resolution": null,
    "resolved_at": null,
    "resolved_by": null,
    "secret_type": "github_personal_access_token",
    "secret_type_display_name": "GitHub Personal Access Token",
    "secret": "ghp_************************************",
    "repository": {
      "id": 35129377,
      "name": "public-repo",
      "full_name": "baxterthehacker/public-repo"
    },
    "push_protection_bypassed": false,
    "push_protection_bypassed_by": null,
    "push_protection_bypassed_at": null
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false
  },
  "sender": {
    "login": "github",
    "id": 9919,
    "type": "User",
    "site_admin": true
  }
}
```

## Priority 4: Development Activity Events

### 10. Push Event

**Event:** `push`
**Description:** Triggered when commits are pushed to repository.

#### Push Event Payload
```json
{
  "ref": "refs/heads/main",
  "before": "95790bf891e76f994c2c59f4436dbd83b36fb7f0",
  "after": "a10867b14bb761a232cd80139fbd4c0d33264240",
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "compare": "https://github.com/baxterthehacker/public-repo/compare/95790bf891e7...a10867b14bb7",
  "commits": [
    {
      "id": "a10867b14bb761a232cd80139fbd4c0d33264240",
      "tree_id": "365df30b5bc88766ad4c2a85dd85bfe7a445d6c0",
      "distinct": true,
      "message": "Update README.md",
      "timestamp": "2015-05-05T23:40:15-04:00",
      "url": "https://github.com/baxterthehacker/public-repo/commit/a10867b14bb761a232cd80139fbd4c0d33264240",
      "author": {
        "name": "Baxter the Hacker",
        "email": "baxter@hacker.org",
        "username": "baxterthehacker"
      },
      "committer": {
        "name": "Baxter the Hacker",
        "email": "baxter@hacker.org",
        "username": "baxterthehacker"
      },
      "added": [],
      "removed": [],
      "modified": ["README.md"]
    }
  ],
  "head_commit": {
    "id": "a10867b14bb761a232cd80139fbd4c0d33264240",
    "tree_id": "365df30b5bc88766ad4c2a85dd85bfe7a445d6c0",
    "distinct": true,
    "message": "Update README.md",
    "timestamp": "2015-05-05T23:40:15-04:00",
    "url": "https://github.com/baxterthehacker/public-repo/commit/a10867b14bb761a232cd80139fbd4c0d33264240",
    "author": {
      "name": "Baxter the Hacker",
      "email": "baxter@hacker.org",
      "username": "baxterthehacker"
    },
    "committer": {
      "name": "Baxter the Hacker",
      "email": "baxter@hacker.org",
      "username": "baxterthehacker"
    },
    "added": [],
    "removed": [],
    "modified": ["README.md"]
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false,
    "default_branch": "main"
  },
  "pusher": {
    "name": "baxterthehacker",
    "email": "baxter@hacker.org"
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 11. Pull Request Event

**Event:** `pull_request`
**Actions:** `opened`, `closed`, `merged`, `reopened`, `assigned`, `review_requested`
**Description:** Triggered for pull request activity.

#### Pull Request Opened Payload
```json
{
  "action": "opened",
  "number": 1,
  "pull_request": {
    "id": 34778301,
    "number": 1,
    "state": "open",
    "title": "Update the README with new information",
    "user": {
      "login": "baxterthehacker",
      "id": 6752317,
      "type": "User",
      "site_admin": false
    },
    "body": "This is a pretty simple change that we need to pull into main.",
    "created_at": "2015-05-05T23:40:27Z",
    "updated_at": "2015-05-05T23:40:27Z",
    "closed_at": null,
    "merged_at": null,
    "merge_commit_sha": null,
    "assignee": null,
    "assignees": [],
    "requested_reviewers": [],
    "requested_teams": [],
    "labels": [],
    "milestone": null,
    "commits_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1/commits",
    "review_comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1/comments",
    "review_comment_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/comments{/number}",
    "comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/1/comments",
    "statuses_url": "https://api.github.com/repos/baxterthehacker/public-repo/statuses/0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
    "head": {
      "label": "baxterthehacker:changes",
      "ref": "changes",
      "sha": "0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
      "user": {
        "login": "baxterthehacker",
        "id": 6752317,
        "type": "User"
      },
      "repo": {
        "id": 35129377,
        "name": "public-repo",
        "full_name": "baxterthehacker/public-repo"
      }
    },
    "base": {
      "label": "baxterthehacker:main",
      "ref": "main",
      "sha": "9353195a19e45482665306e466c832c46560532d",
      "user": {
        "login": "baxterthehacker",
        "id": 6752317,
        "type": "User"
      },
      "repo": {
        "id": 35129377,
        "name": "public-repo",
        "full_name": "baxterthehacker/public-repo"
      }
    },
    "_links": {
      "self": {
        "href": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1"
      },
      "html": {
        "href": "https://github.com/baxterthehacker/public-repo/pull/1"
      }
    },
    "merged": false,
    "mergeable": null,
    "mergeable_state": "unknown",
    "merged_by": null,
    "comments": 0,
    "review_comments": 0,
    "maintainer_can_modify": false,
    "commits": 1,
    "additions": 1,
    "deletions": 1,
    "changed_files": 1
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

### 12. Issues Event

**Event:** `issues`
**Actions:** `opened`, `closed`, `assigned`, `labeled`, `edited`
**Description:** Triggered for issue activity.

#### Issue Opened Payload
```json
{
  "action": "opened",
  "issue": {
    "id": 73464126,
    "number": 2,
    "title": "Spelling error in the README file",
    "user": {
      "login": "baxterthehacker",
      "id": 6752317,
      "type": "User",
      "site_admin": false
    },
    "labels": [],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [],
    "milestone": null,
    "comments": 0,
    "created_at": "2015-05-05T23:40:28Z",
    "updated_at": "2015-05-05T23:40:28Z",
    "closed_at": null,
    "body": "It looks like you accidentally spelled 'commit' with two 't's.",
    "url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2",
    "html_url": "https://github.com/baxterthehacker/public-repo/issues/2"
  },
  "repository": {
    "id": 35129377,
    "name": "public-repo",
    "full_name": "baxterthehacker/public-repo",
    "private": false
  },
  "sender": {
    "login": "baxterthehacker",
    "id": 6752317,
    "type": "User",
    "site_admin": false
  }
}
```

## Priority 6: Git Operations Events

### Create Event (Branch/Tag Creation)

**Event:** `create`  
**Description:** Triggered when a Git branch or tag is created.

#### Create Branch Event Payload
```json
{
  "action": null,
  "ref": "refs/heads/feature-branch",
  "ref_type": "branch",
  "master_branch": "main",
  "description": "Repository for managing audit platform",
  "pusher_type": "user",
  "repository": {
    "id": 123456789,
    "node_id": "R_kgDOABCDEFG",
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjk4NzY1NDMyMQ==",
      "avatar_url": "https://avatars.githubusercontent.com/u/987654321?v=4",
      "type": "Organization"
    },
    "html_url": "https://github.com/orgname/audit-platform",
    "default_branch": "main",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-15T14:30:00Z"
  },
  "organization": {
    "login": "orgname",
    "id": 987654321,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjk4NzY1NDMyMQ==",
    "url": "https://api.github.com/orgs/orgname",
    "repos_url": "https://api.github.com/orgs/orgname/repos",
    "avatar_url": "https://avatars.githubusercontent.com/u/987654321?v=4"
  },
  "sender": {
    "login": "developer",
    "id": 123456,
    "node_id": "MDQ6VXNlcjEyMzQ1Ng==",
    "avatar_url": "https://avatars.githubusercontent.com/u/123456?v=4",
    "type": "User",
    "site_admin": false
  }
}
```

**Database Mapping:** `git_operations` table with fields: `ref`, `ref_type`, `repository_id`, `sender_id`

### Delete Event (Branch/Tag Deletion)

**Event:** `delete`  
**Description:** Triggered when a Git branch or tag is deleted.

#### Delete Branch Event Payload
```json
{
  "action": null,
  "ref": "refs/heads/obsolete-feature",
  "ref_type": "branch",
  "pusher_type": "user",
  "repository": {
    "id": 123456789,
    "node_id": "R_kgDOABCDEFG",
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321,
    "avatar_url": "https://avatars.githubusercontent.com/u/987654321?v=4"
  },
  "sender": {
    "login": "developer",
    "id": 123456,
    "node_id": "MDQ6VXNlcjEyMzQ1Ng==",
    "avatar_url": "https://avatars.githubusercontent.com/u/123456?v=4",
    "type": "User"
  }
}
```

**Database Mapping:** `git_operations` table with fields: `ref`, `ref_type`, `repository_id`, `sender_id`

### Fork Event

**Event:** `fork`  
**Description:** Triggered when someone forks a repository.

#### Fork Event Payload
```json
{
  "action": null,
  "forkee": {
    "id": 234567890,
    "node_id": "R_kgDOABCDEFH",
    "name": "audit-platform",
    "full_name": "forker/audit-platform",
    "private": false,
    "owner": {
      "login": "forker",
      "id": 345678,
      "node_id": "MDQ6VXNlcjM0NTY3OA==",
      "avatar_url": "https://avatars.githubusercontent.com/u/345678?v=4",
      "type": "User"
    },
    "html_url": "https://github.com/forker/audit-platform",
    "description": "Forked from orgname/audit-platform",
    "fork": true,
    "created_at": "2024-01-15T15:30:00Z",
    "updated_at": "2024-01-15T15:30:00Z",
    "clone_url": "https://github.com/forker/audit-platform.git",
    "default_branch": "main"
  },
  "repository": {
    "id": 123456789,
    "node_id": "R_kgDOABCDEFG",
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    },
    "forks_count": 1,
    "stargazers_count": 5
  },
  "organization": {
    "login": "orgname",
    "id": 987654321,
    "avatar_url": "https://avatars.githubusercontent.com/u/987654321?v=4"
  },
  "sender": {
    "login": "forker",
    "id": 345678,
    "node_id": "MDQ6VXNlcjM0NTY3OA==",
    "type": "User"
  }
}
```

**Database Mapping:** `repository_activities` table with fields: `forkee_id`, `repository_id`, `sender_id`

---

## Priority 7: System & Administrative Events

### Ping Event (Webhook Configuration Test)

**Event:** `ping`  
**Description:** Triggered when a new webhook is created to confirm proper configuration.

#### Ping Event Payload
```json
{
  "zen": "Mind your words, they are important.",
  "hook_id": 234567890,
  "hook": {
    "type": "Repository",
    "id": 234567890,
    "name": "web",
    "active": true,
    "events": [
      "push",
      "pull_request",
      "member",
      "repository"
    ],
    "config": {
      "content_type": "json",
      "insecure_ssl": "0",
      "url": "https://audit-platform.example.com/webhooks/github"
    },
    "updated_at": "2024-01-15T21:00:00Z",
    "created_at": "2024-01-15T21:00:00Z",
    "url": "https://api.github.com/repos/orgname/audit-platform/hooks/234567890",
    "test_url": "https://api.github.com/repos/orgname/audit-platform/hooks/234567890/test",
    "ping_url": "https://api.github.com/repos/orgname/audit-platform/hooks/234567890/pings",
    "last_response": {
      "code": null,
      "status": "unused",
      "message": null
    }
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "webhook-admin",
    "id": 901234,
    "type": "User"
  }
}
```

**Database Mapping:** `system_events` table with fields: `hook_id`, `repository_id`, `sender_id`

### Meta Event (Webhook Deletion)

**Event:** `meta`  
**Actions:** `deleted`  
**Description:** Triggered when a webhook is deleted.

#### Meta Event Payload
```json
{
  "action": "deleted",
  "hook_id": 234567890,
  "hook": {
    "type": "Repository",
    "id": 234567890,
    "name": "web",
    "active": true,
    "events": [
      "push",
      "pull_request",
      "member",
      "repository"
    ],
    "config": {
      "content_type": "json",
      "insecure_ssl": "0",
      "url": "https://old-audit-platform.example.com/webhooks/github"
    },
    "updated_at": "2024-01-15T22:00:00Z",
    "created_at": "2024-01-10T10:00:00Z"
  },
  "repository": {
    "id": 123456789,
    "name": "audit-platform",
    "full_name": "orgname/audit-platform",
    "private": true,
    "owner": {
      "login": "orgname",
      "id": 987654321,
      "type": "Organization"
    }
  },
  "organization": {
    "login": "orgname",
    "id": 987654321
  },
  "sender": {
    "login": "webhook-admin",
    "id": 901234,
    "type": "User"
  }
}
```

**Database Mapping:** `system_events` table with fields: `hook_id`, `action`, `repository_id`, `sender_id`

### Installation Events (GitHub App Management)

**Event:** `installation`  
**Actions:** `created`, `deleted`, `suspended`, `unsuspended`  
**Description:** Triggered when a GitHub App is installed, uninstalled, suspended, or unsuspended.

#### Installation Created Event Payload
```json
{
  "action": "created",
  "installation": {
    "id": 12345678,
    "account": {
      "login": "orgname",
      "id": 987654321,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjk4NzY1NDMyMQ==",
      "type": "Organization"
    },
    "repository_selection": "selected",
    "access_tokens_url": "https://api.github.com/app/installations/12345678/access_tokens",
    "repositories_url": "https://api.github.com/installation/repositories",
    "html_url": "https://github.com/organizations/orgname/settings/installations/12345678",
    "app_id": 123456,
    "target_id": 987654321,
    "target_type": "Organization",
    "permissions": {
      "contents": "read",
      "metadata": "read",
      "pull_requests": "write",
      "repository_hooks": "write",
      "organization_administration": "read",
      "members": "read"
    },
    "events": [
      "push",
      "pull_request",
      "member",
      "repository",
      "organization"
    ],
    "created_at": "2024-01-16T00:00:00Z",
    "updated_at": "2024-01-16T00:00:00Z",
    "single_file_name": null,
    "has_multiple_single_files": false,
    "single_file_paths": [],
    "app_slug": "github-audit-platform",
    "suspended_by": null,
    "suspended_at": null
  },
  "repositories": [
    {
      "id": 123456789,
      "node_id": "R_kgDOABCDEFG",
      "name": "audit-platform",
      "full_name": "orgname/audit-platform",
      "private": true
    }
  ],
  "requester": {
    "login": "org-admin",
    "id": 345678,
    "type": "User"
  },
  "sender": {
    "login": "org-admin",
    "id": 345678,
    "type": "User"
  }
}
```

**Database Mapping:** `installation_events` table with fields: `installation_id`, `action`, `target_id`, `sender_id`

---

All webhook payloads include these common fields:

### Repository Object
```json
{
  "id": 35129377,
  "node_id": "MDEwOlJlcG9zaXRvcnkzNTEyOTM3Nw==",
  "name": "public-repo",
  "full_name": "baxterthehacker/public-repo",
  "private": false,
  "html_url": "https://github.com/baxterthehacker/public-repo",
  "description": "This your first repo!",
  "fork": false,
  "url": "https://api.github.com/repos/baxterthehacker/public-repo",
  "created_at": "2015-05-05T23:40:12Z",
  "updated_at": "2015-05-05T23:40:12Z",
  "pushed_at": "2015-05-05T23:40:27Z",
  "default_branch": "main",
  "permissions": {
    "admin": false,
    "push": false,
    "pull": true
  }
}
```

### Organization Object (when applicable)
```json
{
  "login": "github",
  "id": 872781,
  "node_id": "MDEyOk9yZ2FuaXphdGlvbjg3Mjc4MQ==",
  "url": "https://api.github.com/orgs/github",
  "avatar_url": "https://github.com/images/error/github_happy.gif",
  "description": "A great organization",
  "name": "github",
  "company": "GitHub",
  "blog": "https://github.com/blog",
  "location": "San Francisco",
  "email": "octocat@github.com",
  "type": "Organization"
}
```

### User Object (sender and actor fields)
```json
{
  "login": "baxterthehacker",
  "id": 6752317,
  "node_id": "MDQ6VXNlcjY3NTIzMTc=",
  "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
  "gravatar_id": "",
  "url": "https://api.github.com/users/baxterthehacker",
  "html_url": "https://github.com/baxterthehacker",
  "type": "User",
  "site_admin": false
}
```

## Database Mapping Notes

### Database Mapping Guidelines

#### Core Database Tables

Based on all webhook events, the following database tables should be implemented:

##### **github_events** (Raw Event Storage)
```sql
CREATE TABLE github_events (
    id BIGSERIAL PRIMARY KEY,
    delivery_id UUID UNIQUE NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(50),
    payload JSONB NOT NULL,
    signature_verified BOOLEAN NOT NULL DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    repository_id BIGINT,
    organization_id BIGINT,
    sender_id BIGINT
);
```

##### **audit_events** (Processed Audit Trail)
```sql
CREATE TABLE audit_events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(50),
    actor_login VARCHAR(255) NOT NULL,
    actor_id BIGINT NOT NULL,
    target_type VARCHAR(50),
    target_id BIGINT,
    repository_id BIGINT,
    organization_id BIGINT,
    description TEXT,
    metadata JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

##### Additional Specialized Tables
- **repository_access_events**: Track collaborator changes
- **security_events**: Security alerts and policy changes  
- **git_operations**: Branch, tag, and commit operations
- **collaboration_activities**: Issues, PRs, comments, reviews
- **system_events**: Webhook and installation management
- **access_control_events**: Token requests and permissions

#### Key Field Mappings

1. **Event Identification**
   - `X-GitHub-Event` header: Event type
   - `X-GitHub-Delivery` header: Unique delivery ID
   - `action`: Specific action within event type

2. **Actor/User Information**
   - `sender.login`: Username who triggered the event
   - `sender.id`: GitHub user ID
   - `sender.type`: User type (User, Bot, etc.)

3. **Target Information**
   - `repository.id`: Repository ID
   - `repository.name`: Repository name
   - `repository.full_name`: Full repository path
   - `organization.login`: Organization name (if applicable)

4. **Permission Changes**
   - `changes` object: Contains before/after values
   - `member.login`: User being added/removed
   - `team.name`: Team being modified
   - `permissions` object: Current permission levels

5. **Timestamps**
   - All events include `created_at` or event-specific timestamp fields
   - Format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)

#### Validation Requirements

1. **Webhook Signature Verification**
   - Use `X-Hub-Signature-256` header
   - Verify against webhook secret using HMAC SHA-256

2. **Delivery ID Tracking**
   - Store `X-GitHub-Delivery` to prevent duplicate processing
   - Use for webhook delivery status tracking

3. **Rate Limiting Awareness**
   - GitHub webhooks have a 25MB payload limit
   - Large events may be capped or split

#### Processing Strategy

1. **Raw Storage**: Store all payloads in `github_events` with signature verification
2. **Event Classification**: Parse and route to specialized tables
3. **Audit Trail**: Create immutable audit records
4. **Alert Generation**: Monitor for security events and policy violations

This comprehensive payload reference provides complete coverage for implementing robust webhook processing in our GitHub audit platform, handling everything from basic access management to advanced security monitoring.