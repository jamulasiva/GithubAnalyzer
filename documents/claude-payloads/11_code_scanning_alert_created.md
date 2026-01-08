# Code Scanning Alert Created Event

## Event Type
`code_scanning_alert`

## Action
`created`

## Description
This event occurs when code scanning detects a potential security vulnerability or code quality issue.

## Example Webhook Payload

```json
{
  "action": "created",
  "alert": {
    "number": 1,
    "created_at": "2023-03-17T15:42:05Z",
    "url": "https://api.github.com/repos/Codertocat/Hello-World/code-scanning/alerts/1",
    "html_url": "https://github.com/Codertocat/Hello-World/security/code-scanning/1",
    "state": "open",
    "dismissed_by": null,
    "dismissed_at": null,
    "dismissed_reason": null,
    "rule": {
      "id": "js/sql-injection",
      "severity": "error",
      "description": "SQL injection",
      "name": "SQL injection",
      "full_description": "Building a SQL query from user-controlled data allows SQL injection."
    },
    "tool": {
      "name": "CodeQL",
      "version": "2.11.6"
    },
    "most_recent_instance": {
      "ref": "refs/heads/main",
      "analysis_key": ".github/workflows/codeql-analysis.yml:analyze",
      "environment": "{}",
      "state": "open",
      "commit_sha": "abcdef1234567890",
      "location": {
        "path": "app/controllers/users_controller.rb",
        "start_line": 42,
        "end_line": 42,
        "start_column": 10,
        "end_column": 50
      }
    }
  },
  "ref": "refs/heads/main",
  "commit_oid": "abcdef1234567890",
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
