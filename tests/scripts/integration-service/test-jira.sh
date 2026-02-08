#!/bin/bash

# Integration Service - Jira Integration Test
echo "========================================="
echo "Testing Jira Integration"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

# Test Jira endpoints
echo -e "\n1. Testing GET /api/v1/jira/projects..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/jira/projects" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing POST /api/v1/jira/sync (trigger sync)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing POST /api/v1/jira/webhook (simulate webhook)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookEvent": "jira:issue_created",
    "issue": {
      "key": "TEST-123",
      "fields": {
        "summary": "Test Issue"
      }
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Jira integration tests completed"
