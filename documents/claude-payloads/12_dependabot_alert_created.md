# Dependabot Alert Created Event

## Event Type
`dependabot_alert`

## Action
`created`

## Description
This event occurs when Dependabot identifies a new security vulnerability in a repository's dependencies.

## Example Webhook Payload

```json
{
  "action": "created",
  "alert": {
    "number": 1,
    "state": "open",
    "dependency": {
      "package": {
        "ecosystem": "npm",
        "name": "lodash"
      },
      "manifest_path": "package-lock.json",
      "scope": "runtime"
    },
    "security_advisory": {
      "ghsa_id": "GHSA-xxxx-xxxx-xxxx",
      "cve_id": "CVE-2021-12345",
      "summary": "Prototype Pollution in lodash",
      "description": "Versions of lodash before 4.17.21 are vulnerable to prototype pollution.",
      "severity": "high",
      "identifiers": [
        {
          "type": "GHSA",
          "value": "GHSA-xxxx-xxxx-xxxx"
        },
        {
          "type": "CVE",
          "value": "CVE-2021-12345"
        }
      ],
      "references": [],
      "published_at": "2021-02-15T00:00:00Z",
      "updated_at": "2021-02-15T00:00:00Z",
      "withdrawn_at": null
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
    "url": "https://api.github.com/repos/Codertocat/Hello-World/dependabot/alerts/1",
    "html_url": "https://github.com/Codertocat/Hello-World/security/dependabot/1",
    "created_at": "2023-03-17T15:42:05Z",
    "updated_at": "2023-03-17T15:42:05Z",
    "dismissed_at": null,
    "dismissed_by": null,
    "dismissed_reason": null,
    "dismissed_comment": null,
    "fixed_at": null
  },
  "repository": {
    "id": 186853002,
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World"
  },
  "sender": {
    "login": "dependabot[bot]",
    "id": 49699333,
    "type": "Bot"
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
