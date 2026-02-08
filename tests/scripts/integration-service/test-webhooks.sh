#!/bin/bash

# Integration Service - Webhook Processing Test
echo "========================================="
echo "Testing Webhook Processing"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

echo -e "\n1. Testing Jira webhook..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookEvent": "jira:issue_updated",
    "issue": {
      "key": "PROJ-456",
      "fields": {
        "summary": "Updated issue",
        "status": {"name": "In Progress"}
      }
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing GitHub webhook (pull request)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {
      "number": 42,
      "title": "Add new feature",
      "state": "open"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing Slack webhook (message event)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "type": "message",
      "channel": "C123456",
      "user": "U123456",
      "text": "Hello from Slack!"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n4. Testing Calendar webhook..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceState": "exists"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Webhook processing tests completed"
