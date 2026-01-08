# GitHub Webhook Events & API Endpoints for Repository & Access Management

**Date:** January 2, 2026  
**Purpose:** Complete mapping of GitHub webhook events and API endpoints required for audit platform

## Core Webhook Events for Audit Platform

### 🏢 **Organization & Repository Management Events**

#### Repository Lifecycle Events
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **repository** | `created`, `deleted`, `archived`, `unarchived`, `privatized`, `publicized`, `transferred`, `renamed`, `edited` | **HIGH** | Repository lifecycle changes | `/webhooks/github/repository` | [Repository Created](./github-webhook-payloads.md#5-repository-event-repository-management) |
| **public** | Repository visibility changed to public | **HIGH** | Repository made public | `/webhooks/github/repository` | [Repository Made Public](./github-webhook-payloads.md#6-public-event-repository-visibility-change) |
| **create** | Branch/tag creation | **MEDIUM** | Git ref created | `/webhooks/github/branch-tag` | [Create Event](./github-webhook-additional-payloads.md#create-event-payload) |
| **delete** | Branch/tag deletion | **MEDIUM** | Git ref deleted | `/webhooks/github/branch-tag` | [Delete Event](./github-webhook-additional-payloads.md#delete-event-payload) |
| **fork** | Repository forked | **MEDIUM** | Repository forked | `/webhooks/github/repository` | [Fork Event](./github-webhook-additional-payloads.md#fork-event-payload) |

#### Organization Events
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **organization** | `deleted`, `renamed`, `member_added`, `member_removed`, `member_invited` | **HIGH** | Organization membership changes | `/webhooks/github/organization` | [Organization Member Added](./github-webhook-payloads.md#2-organization-event-organization-membership-changes) |
| **membership** | `added`, `removed` | **HIGH** | Team membership changes | `/webhooks/github/membership` | [Team Member Added](./github-webhook-payloads.md#4-membership-event-team-membership-changes) |

### 👥 **Access Management & Collaboration Events**

#### Repository Collaborators
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **member** | `added`, `removed`, `edited` | **CRITICAL** | Repository collaborator changes | `/webhooks/github/collaborators` | [Member Added/Edited](./github-webhook-payloads.md#1-member-event-repository-collaborator-changes) |
| **team** | `added_to_repository`, `removed_from_repository`, `created`, `deleted`, `edited` | **HIGH** | Team repository access changes | `/webhooks/github/teams` | [Team Added to Repository](./github-webhook-payloads.md#3-team-event-team-management) |
| **team_add** | Team added to repository | **HIGH** | Team granted repo access | `/webhooks/github/teams` | [Team Added to Repository](./github-webhook-additional-payloads.md#team-add-event) |

#### Permission & Security Changes
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **deploy_key** | `created`, `deleted` | **HIGH** | SSH deploy keys management | `/webhooks/github/security` | [Deploy Key Created](./github-webhook-payloads.md#8-deploy-key-event) |
| **personal_access_token_request** | `approved`, `cancelled`, `created`, `denied` | **HIGH** | PAT requests for orgs | `/webhooks/github/security` | [PAT Request Created](./github-webhook-additional-payloads.md#personal-access-token-request-event-payload) |

### 🛡️ **Security & Configuration Events**

#### Branch Protection & Repository Rules
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **branch_protection_rule** | `created`, `edited`, `deleted` | **HIGH** | Branch protection changes | `/webhooks/github/security` | [Branch Protection Rule Created](./github-webhook-payloads.md#7-branch-protection-rule-event) |
| **branch_protection_configuration** | `disabled` | **HIGH** | Branch protection disabled | `/webhooks/github/security` | [Branch Protection Disabled](./github-webhook-additional-payloads.md#branch-protection-configuration-event) |
| **repository_ruleset** | `created`, `edited`, `deleted` | **HIGH** | Repository ruleset changes | `/webhooks/github/security` | [Repository Ruleset Created](./github-webhook-additional-payloads.md#repository-ruleset-event-payload) |

#### Security Alerts
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **code_scanning_alert** | `created`, `fixed`, `dismissed` | **MEDIUM** | Code scanning alerts | `/webhooks/github/security` | [Code Scanning Alert Created](./github-webhook-additional-payloads.md#code-scanning-alert-event-payload) |
| **secret_scanning_alert** | `created`, `resolved` | **HIGH** | Secret scanning alerts | `/webhooks/github/security` | [Secret Scanning Alert Created](./github-webhook-payloads.md#9-secret-scanning-alert-event) |
| **dependabot_alert** | `created`, `dismissed`, `fixed` | **MEDIUM** | Dependabot alerts | `/webhooks/github/security` | [Dependabot Alert Created](./github-webhook-additional-payloads.md#dependabot-alert-event-payload) |
| **security_and_analysis** | Security features enabled/disabled | **HIGH** | Security settings changes | `/webhooks/github/security` | Available in GitHub Docs |

### 📝 **Activity & Development Events**

#### Code Activity
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **push** | Code pushed to repository | **MEDIUM** | Code changes | `/webhooks/github/activity` | [Push Event](./github-webhook-payloads.md#10-push-event) |
| **pull_request** | `opened`, `closed`, `merged`, `assigned`, `unassigned` | **MEDIUM** | Pull request activity | `/webhooks/github/activity` | [Pull Request Opened](./github-webhook-payloads.md#11-pull-request-event) |
| **issues** | `opened`, `closed`, `assigned`, `unassigned` | **LOW** | Issue activity | `/webhooks/github/activity` | [Issue Opened](./github-webhook-payloads.md#12-issues-event) |
| **release** | `published`, `unpublished`, `created` | **MEDIUM** | Release management | `/webhooks/github/activity` | [Release Published](./github-webhook-additional-payloads.md#release-event) |

#### Comments & Reviews
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **issue_comment** | `created`, `edited`, `deleted` | **LOW** | Issue/PR comments | `/webhooks/github/activity` | [Issue Comment Created](./github-webhook-additional-payloads.md#issue-comment-event-payload) |
| **pull_request_review** | `submitted`, `dismissed` | **MEDIUM** | PR reviews | `/webhooks/github/activity` | [Pull Request Review Submitted](./github-webhook-additional-payloads.md#pull-request-review-event-payload) |
| **commit_comment** | `created` | **LOW** | Commit comments | `/webhooks/github/activity` | [Commit Comment Created](./github-webhook-additional-payloads.md#commit-comment-event) |

### 🔧 **Installation & App Management Events**

#### GitHub App Events
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **installation** | `created`, `deleted`, `suspend`, `unsuspend` | **MEDIUM** | App installation changes | `/webhooks/github/installation` | [Installation Created](./github-webhook-additional-payloads.md#installation-event-payload) |
| **installation_repositories** | `added`, `removed` | **MEDIUM** | App repo access changes | `/webhooks/github/installation` | [Installation Repositories Added](./github-webhook-additional-payloads.md#installation-repositories-event-payload) |

### 📊 **Meta Events**

#### System Events
| Event | Actions | Priority | Description | Webhook Endpoints | Payload Reference |
|-------|---------|----------|-------------|-------------------|------------------|
| **ping** | Webhook test | **LOW** | Webhook validation | `/webhooks/github/ping` | [Ping Event](./github-webhook-additional-payloads.md#ping-event-payload) |
| **meta** | `deleted` | **LOW** | Webhook deleted | `/webhooks/github/meta` | [Meta Event](./github-webhook-additional-payloads.md#meta-event-payload) |

## Required API Endpoints for Data Enrichment

### Repository Management APIs
```
GET /repos/{owner}/{repo}                          # Repository details
GET /repos/{owner}/{repo}/collaborators            # Repository collaborators
GET /repos/{owner}/{repo}/teams                   # Repository teams
GET /repos/{owner}/{repo}/branches                # Repository branches
GET /repos/{owner}/{repo}/topics                  # Repository topics
GET /repos/{owner}/{repo}/contributors            # Repository contributors
```

### Organization APIs
```
GET /orgs/{org}                                   # Organization details
GET /orgs/{org}/members                           # Organization members
GET /orgs/{org}/teams                             # Organization teams
GET /orgs/{org}/repos                             # Organization repositories
GET /orgs/{org}/audit-log                         # Organization audit log (Enterprise)
```

### User & Access APIs
```
GET /users/{username}                             # User details
GET /user/orgs                                    # User organizations
GET /user/repos                                   # User repositories
GET /repos/{owner}/{repo}/collaborators/{username} # Collaborator permissions
```

### Security & Configuration APIs
```
GET /repos/{owner}/{repo}/branches/{branch}/protection    # Branch protection
GET /repos/{owner}/{repo}/rulesets                       # Repository rulesets
GET /repos/{owner}/{repo}/vulnerability-alerts           # Vulnerability alerts
GET /repos/{owner}/{repo}/secret-scanning/alerts         # Secret scanning alerts
GET /repos/{owner}/{repo}/code-scanning/alerts          # Code scanning alerts
```

## Webhook Endpoint Structure

### Proposed FastAPI Webhook Endpoints

```python
# Repository & Organization Events
POST /webhooks/github/repository      # Repository lifecycle events
POST /webhooks/github/organization    # Organization events

# Access Management Events
POST /webhooks/github/collaborators   # Repository collaborator changes
POST /webhooks/github/teams          # Team and membership changes
POST /webhooks/github/membership     # Organization membership changes

# Security Events
POST /webhooks/github/security       # Security-related events
POST /webhooks/github/branch-tag     # Branch/tag creation/deletion

# Activity Events
POST /webhooks/github/activity       # Development activity events

# Installation & Meta Events
POST /webhooks/github/installation   # GitHub App installation events
POST /webhooks/github/ping          # Webhook validation
POST /webhooks/github/meta           # Meta events
```

### Webhook Headers for Validation

```python
# Required headers for webhook validation
X-GitHub-Event: event_type
X-GitHub-Delivery: unique_delivery_id
X-Hub-Signature-256: hmac_signature
X-GitHub-Hook-ID: webhook_id
X-GitHub-Hook-Installation-Target-Type: target_type
X-GitHub-Hook-Installation-Target-ID: target_id
User-Agent: GitHub-Hookshot/{version}
```

## Event Processing Priority

### Critical Events (Real-time Processing)
- Repository collaborator changes (`member`)
- Organization membership changes (`organization`, `membership`)
- Security configuration changes (`branch_protection_rule`, `repository_ruleset`)
- Access token requests (`personal_access_token_request`)

### High Priority Events (< 5 minutes)
- Repository lifecycle (`repository`, `public`)
- Team access changes (`team`, `team_add`)
- Security alerts (`secret_scanning_alert`, `security_and_analysis`)
- Deploy key management (`deploy_key`)

### Medium Priority Events (< 30 minutes)
- Development activity (`push`, `pull_request`, `release`)
- Branch/tag changes (`create`, `delete`)
- Installation changes (`installation`, `installation_repositories`)

### Low Priority Events (< 2 hours)
- Comments and discussions (`issue_comment`, `commit_comment`)
- Issue tracking (`issues`)
- Meta events (`ping`, `meta`)

## Database Storage Strategy

### Event Storage Schema
```sql
-- Main events table
CREATE TABLE github_webhook_events (
    id BIGSERIAL PRIMARY KEY,
    event_id UUID UNIQUE NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(50),
    delivery_id VARCHAR(100) NOT NULL,
    
    -- Source information
    organization_id INTEGER REFERENCES organizations(id),
    repository_id INTEGER REFERENCES repositories(id),
    sender_id INTEGER REFERENCES users(id),
    
    -- Event payload and metadata
    payload JSONB NOT NULL,
    headers JSONB,
    
    -- Processing information
    processed_at TIMESTAMP WITH TIME ZONE,
    processing_status VARCHAR(20) DEFAULT 'pending',
    processing_error TEXT,
    
    -- Timestamps
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for efficient querying
CREATE INDEX idx_events_type_time ON github_webhook_events(event_type, event_timestamp DESC);
CREATE INDEX idx_events_org_time ON github_webhook_events(organization_id, event_timestamp DESC) WHERE organization_id IS NOT NULL;
CREATE INDEX idx_events_repo_time ON github_webhook_events(repository_id, event_timestamp DESC) WHERE repository_id IS NOT NULL;
CREATE INDEX idx_events_processing ON github_webhook_events(processing_status, received_at);
```

### Audit Trail Views
```sql
-- Repository access changes view
CREATE VIEW repository_access_audit AS
SELECT 
    e.event_timestamp,
    e.event_type,
    e.action,
    r.full_name as repository,
    o.login as organization,
    u.login as actor,
    e.payload->'member'->>'login' as affected_user,
    e.payload->'member'->>'role' as permission_level
FROM github_webhook_events e
LEFT JOIN repositories r ON e.repository_id = r.id
LEFT JOIN organizations o ON e.organization_id = o.id
LEFT JOIN users u ON e.sender_id = u.id
WHERE e.event_type IN ('member', 'team', 'membership', 'organization')
ORDER BY e.event_timestamp DESC;
```

This comprehensive mapping provides the foundation for implementing a robust GitHub audit platform that captures all critical repository and access management events while maintaining efficient processing and storage patterns.

## Additional Resources

- **[Core Webhook Payloads](./github-webhook-payloads.md)** - Detailed JSON payload examples for main audit events
- **[Additional Webhook Payloads](./github-webhook-additional-payloads.md)** - Supplementary payload examples for security, system, and extended events
- **[Implementation Roadmap](./implementation-roadmap.md)** - Complete 8-week implementation plan
- **[Technology Stack](./technology-stack.md)** - Technology choices and configuration guide