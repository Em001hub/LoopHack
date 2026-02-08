# API Gateway - Curl Examples

This document provides curl command examples for testing all API Gateway endpoints.

## Base URL
```bash
API_GATEWAY_URL="http://localhost:3000"
```

## Health Check

```bash
curl -X GET "${API_GATEWAY_URL}/api/health"
```

## Projects

### Get All Projects (from all sources)
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects"
```

### Jira Projects
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/jira/projects"
```

### Jira Tasks for a Project
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/jira/projects/PROJ/tasks"
```

### GitHub Repositories
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/github/repositories"
```

### GitHub Commits
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/github/repositories/owner/repo/commits"
```

### GitHub Pull Requests
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/github/repositories/owner/repo/pulls"
```

### Slack Channels
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/slack/channels"
```

### Slack Messages
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/slack/channels/C123456/messages"
```

### Slack Users
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/slack/users"
```

### Calendar Events
```bash
curl -X GET "${API_GATEWAY_URL}/api/projects/calendar/events?calendar_id=primary"
```

## Sync Triggers

### Trigger Full Sync (All Integrations)
```bash
curl -X POST "${API_GATEWAY_URL}/api/sync/all"
```

### Trigger Jira Sync
```bash
curl -X POST "${API_GATEWAY_URL}/api/sync/jira"
```

### Trigger GitHub Sync
```bash
curl -X POST "${API_GATEWAY_URL}/api/sync/github"
```

### Trigger Slack Sync
```bash
curl -X POST "${API_GATEWAY_URL}/api/sync/slack"
```

### Trigger Calendar Sync
```bash
curl -X POST "${API_GATEWAY_URL}/api/sync/calendar"
```

### Get Sync Status
```bash
curl -X GET "${API_GATEWAY_URL}/api/sync/status"
```

## Webhooks

### Jira Webhook
```bash
curl -X POST "${API_GATEWAY_URL}/api/webhooks/jira" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookEvent": "jira:issue_created",
    "issue": {
      "key": "PROJ-123",
      "fields": {
        "summary": "New issue"
      }
    }
  }'
```

### GitHub Webhook
```bash
curl -X POST "${API_GATEWAY_URL}/api/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{
    "commits": [
      {"id": "abc123", "message": "Commit message"}
    ]
  }'
```

### Slack Webhook
```bash
curl -X POST "${API_GATEWAY_URL}/api/webhooks/slack" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "type": "message",
      "channel": "C123456",
      "text": "Hello"
    }
  }'
```

### Calendar Webhook
```bash
curl -X POST "${API_GATEWAY_URL}/api/webhooks/calendar" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceState": "exists"
  }'
```
