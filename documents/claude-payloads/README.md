# GitHub Webhook Events Documentation

This repository contains comprehensive documentation for GitHub webhook events that will be processed by your webhook application.

## 📋 Overview

This collection includes **25 webhook event types** organized by priority, complete with:
- Detailed event descriptions
- Full webhook payload examples
- Database schema suggestions
- API processing notes
- Use cases and best practices

## 🎯 Event Categories

### Priority 1: Repository Access Management (5 events)
Critical events for tracking repository access and permissions:

| # | Event | File | Description |
|---|-------|------|-------------|
| 01 | **Member Added** | `01_member_added.md` | When a collaborator is added to a repository |
| 02 | **Member Permission Changed** | `02_member_permission_changed.md` | When collaborator permissions are modified |
| 03 | **Organization Member Added** | `03_organization_member_added.md` | When someone is added to the organization |
| 04 | **Team Added to Repository** | `04_team_added_to_repository.md` | When a team gets repository access |
| 05 | **Team Member Added** | `05_team_member_added.md` | When someone joins a team |

### Priority 2: Repository Lifecycle (2 events)
Events related to repository creation and visibility changes:

| # | Event | File | Description |
|---|-------|------|-------------|
| 06 | **Repository Created** | `06_repository_created.md` | When a new repository is created |
| 07 | **Repository Made Public** | `07_repository_publicized.md` | When a private repository is made public |

### Priority 3: Security & Compliance (7 events)
Critical security and compliance monitoring events:

| # | Event | File | Description |
|---|-------|------|-------------|
| 08 | **Branch Protection Rule Created** | `08_branch_protection_created.md` | When branch protection rules are set |
| 09 | **Deploy Key Created** | `09_deploy_key_created.md` | When deploy keys are added |
| 10 | **Repository Ruleset Created** | `10_repository_ruleset_created.md` | When repository rulesets are configured |
| 11 | **Code Scanning Alert Created** | `11_code_scanning_alert_created.md` | When code scanning detects issues |
| 12 | **Dependabot Alert Created** | `12_dependabot_alert_created.md` | When Dependabot finds vulnerabilities |
| 13 | **Personal Access Token Request** | `13_personal_access_token_request_created.md` | When fine-grained tokens are requested |
| 14 | **Secret Scanning Alert Created** | `14_secret_scanning_alert_created.md` | When secrets are detected in code |

### Priority 4: Development Activity (3 events)
Core development workflow events:

| # | Event | File | Description |
|---|-------|------|-------------|
| 15 | **Push Event** | `15_push.md` | When commits are pushed to a repository |
| 16 | **Pull Request Opened** | `16_pull_request_opened.md` | When a new pull request is created |
| 17 | **Issue Opened** | `17_issues_opened.md` | When a new issue is created |

### Priority 5: Communication & Collaboration (2 events)
Events related to comments and reviews:

| # | Event | File | Description |
|---|-------|------|-------------|
| 18 | **Issue Comment Created** | `18_issue_comment_created.md` | When comments are added to issues/PRs |
| 19 | **Pull Request Review Submitted** | `19_pull_request_review_submitted.md` | When PR reviews are submitted |

### Priority 6: Git Operations (3 events)
Git-level operations:

| # | Event | File | Description |
|---|-------|------|-------------|
| 20 | **Create Branch Event** | `20_create_branch.md` | When branches or tags are created |
| 21 | **Delete Branch Event** | `21_delete_branch.md` | When branches or tags are deleted |
| 22 | **Fork Event** | `22_fork.md` | When a repository is forked |

### Priority 7: System & Administrative (3 events)
System-level and administrative events:

| # | Event | File | Description |
|---|-------|------|-------------|
| 23 | **Ping Event** | `23_ping.md` | When webhooks are configured (test event) |
| 24 | **Meta Event** | `24_meta.md` | When webhooks are deleted |
| 25 | **Installation Created** | `25_installation_created.md` | When GitHub Apps are installed |

## 🏗️ Application Architecture

### Recommended Tech Stack

```
┌─────────────────────────────────────────┐
│         GitHub Webhook Events           │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Webhook Receiver API (Node.js)      │
│  - Express.js for HTTP server           │
│  - Webhook signature verification       │
│  - Event routing and validation         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Event Processing Layer              │
│  - Event type detection                 │
│  - Data transformation                  │
│  - Business logic execution             │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Database Layer (PostgreSQL)         │
│  - Event storage with JSONB             │
│  - Structured tables per event type     │
│  - Audit logging                        │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Analytics Dashboard (React)         │
│  - Real-time event monitoring           │
│  - Access tracking visualizations       │
│  - Security alerts and reports          │
└─────────────────────────────────────────┘
```

### Database Schema Overview

Each event type should have:
1. **Core event table** - Structured data specific to the event
2. **Raw payload storage** - JSONB column for complete payload
3. **Audit metadata** - Timestamps, processing status, etc.

Example structure:
```sql
CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_action VARCHAR(100),
    repository_id BIGINT,
    repository_name VARCHAR(255),
    organization_id BIGINT,
    sender_id BIGINT,
    sender_login VARCHAR(255),
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL,
    INDEX idx_event_type (event_type),
    INDEX idx_repository (repository_id),
    INDEX idx_created_at (created_at)
);
```

## 🔐 Security Considerations

### Webhook Signature Verification

Always verify webhook signatures using HMAC SHA-256:

```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
    const hmac = crypto.createHmac('sha256', secret);
    const digest = 'sha256=' + hmac.update(payload).digest('hex');
    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(digest)
    );
}
```

### Critical Security Events

These events require **immediate attention**:
- 🔴 Repository Made Public (`repository.publicized`)
- 🔴 Secret Scanning Alert Created (`secret_scanning_alert.created`)
- 🟠 Dependabot Alert Created (`dependabot_alert.created`)
- 🟠 Code Scanning Alert Created (`code_scanning_alert.created`)
- 🟠 Deploy Key Created (`deploy_key.created`)
- 🟠 Personal Access Token Request (`personal_access_token_request.created`)

## 📊 Dashboard Features

### Recommended Analytics Views

1. **Access Management Dashboard**
   - Recent member additions
   - Permission changes timeline
   - Team access matrix
   - Access anomaly detection

2. **Security Dashboard**
   - Active security alerts
   - Secret scanning results
   - Dependency vulnerabilities
   - Branch protection compliance

3. **Activity Dashboard**
   - Push frequency
   - Pull request metrics
   - Issue tracking
   - Repository creation trends

4. **Audit Dashboard**
   - Complete event log
   - User activity tracking
   - Repository access history
   - Compliance reports

## 🚀 Implementation Guide

### Step 1: Set Up Webhook Receiver

```javascript
const express = require('express');
const crypto = require('crypto');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/webhooks/github', async (req, res) => {
    // Verify signature
    const signature = req.headers['x-hub-signature-256'];
    const payload = JSON.stringify(req.body);
    
    if (!verifySignature(payload, signature, process.env.WEBHOOK_SECRET)) {
        return res.status(401).send('Invalid signature');
    }
    
    // Extract event info
    const eventType = req.headers['x-github-event'];
    const deliveryId = req.headers['x-github-delivery'];
    
    // Process event
    await processWebhookEvent(eventType, req.body, deliveryId);
    
    res.status(200).send('OK');
});
```

### Step 2: Create Event Processors

```javascript
async function processWebhookEvent(eventType, payload, deliveryId) {
    // Store raw event
    await storeRawEvent(eventType, payload, deliveryId);
    
    // Route to specific handler
    switch(eventType) {
        case 'member':
            await handleMemberEvent(payload);
            break;
        case 'repository':
            await handleRepositoryEvent(payload);
            break;
        case 'push':
            await handlePushEvent(payload);
            break;
        // ... handle other events
        default:
            console.log(`Unhandled event type: ${eventType}`);
    }
}
```

### Step 3: Implement Event Handlers

```javascript
async function handleMemberEvent(payload) {
    const { action, member, repository, sender } = payload;
    
    if (action === 'added') {
        await db.query(`
            INSERT INTO member_events 
            (event_id, action, member_login, repository_name, sender_login, payload)
            VALUES ($1, $2, $3, $4, $5, $6)
        `, [
            generateEventId(),
            action,
            member.login,
            repository.full_name,
            sender.login,
            JSON.stringify(payload)
        ]);
        
        // Send notification
        await sendNotification({
            type: 'member_added',
            member: member.login,
            repository: repository.full_name
        });
    }
}
```

## 🔍 Querying and Analysis

### Common Queries

**Find all security events in last 24 hours:**
```sql
SELECT event_type, event_action, repository_name, created_at
FROM webhook_events
WHERE event_type IN (
    'code_scanning_alert',
    'dependabot_alert',
    'secret_scanning_alert'
)
AND created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;
```

**Track access changes for a repository:**
```sql
SELECT event_type, event_action, sender_login, created_at
FROM webhook_events
WHERE repository_name = 'org/repo'
AND event_type IN ('member', 'team', 'membership')
ORDER BY created_at DESC;
```

**Generate access audit report:**
```sql
SELECT 
    date_trunc('day', created_at) as date,
    event_type,
    COUNT(*) as event_count
FROM webhook_events
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY date, event_type
ORDER BY date DESC;
```

## 📚 Additional Resources

- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)

## 🤝 Contributing

To add new event types:
1. Copy an existing event markdown template
2. Update the event type, action, and payload
3. Add database schema recommendations
4. Document use cases and processing notes
5. Update this README with the new event

## 📝 License

This documentation is provided for internal use in building the GitHub webhook monitoring system.

---

**Last Updated:** January 2026
**Total Events Documented:** 25
**Priority Levels:** 7
