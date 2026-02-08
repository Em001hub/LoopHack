# Integration Service - Curl Examples

This document provides curl command examples for testing all Integration Service endpoints.

## Base URL
```bash
INTEGRATION_SERVICE_URL="http://localhost:8000"
```

## Health Check

```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/health"
```

## Jira Integration

### Get Jira Projects
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/jira/projects"
```

### Get Jira Tasks
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/jira/projects/PROJ/tasks"
```

### Trigger Jira Sync
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/sync"
```

### Jira Webhook (Issue Created)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookEvent": "jira:issue_created",
    "issue": {
      "key": "PROJ-123",
      "fields": {
        "summary": "New issue",
        "status": {"name": "To Do"}
      }
    }
  }'
```

### Jira Webhook (Issue Updated)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookEvent": "jira:issue_updated",
    "issue": {
      "key": "PROJ-123",
      "fields": {
        "status": {"name": "In Progress"}
      }
    }
  }'
```

## GitHub Integration

### Get GitHub Repositories
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/github/repositories"
```

### Get GitHub Commits
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/github/repositories/owner/repo/commits"
```

### Get GitHub Pull Requests
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/github/repositories/owner/repo/pulls"
```

### Trigger GitHub Sync
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/sync"
```

### GitHub Webhook (Push Event)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{
    "commits": [
      {
        "id": "abc123",
        "message": "Fix bug",
        "author": {"name": "John Doe"}
      }
    ],
    "repository": {
      "name": "my-repo",
      "full_name": "owner/my-repo"
    }
  }'
```

### GitHub Webhook (Pull Request)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {
      "number": 42,
      "title": "Add new feature",
      "state": "open"
    }
  }'
```

## Slack Integration

### Get Slack Channels
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/slack/channels"
```

### Get Slack Messages
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/slack/channels/C123456/messages"
```

### Get Slack Users
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/slack/users"
```

### Trigger Slack Sync
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/sync"
```

### Slack Webhook (URL Verification)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"
  }'
```

### Slack Webhook (Message Event)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "type": "message",
      "channel": "C123456",
      "user": "U123456",
      "text": "Hello from Slack!"
    }
  }'
```

## Google Calendar Integration

### Get Calendar Events
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/calendar/events?calendar_id=primary"
```

### Trigger Calendar Sync
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/sync"
```

### Calendar Webhook
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceState": "exists"
  }'
```

## Unified Sync

### Trigger Full Sync (All Integrations)
```bash
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/sync/all"
```

### Get Sync Status
```bash
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/sync/status"
```
