#!/bin/bash

# Integration Service - Sync Pipeline Test
echo "========================================="
echo "Testing Sync Pipeline"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

# Test unified sync endpoint
echo -e "\n1. Testing POST /api/v1/sync/all (trigger full sync)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/sync/all" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Waiting 5 seconds for sync to process..."
sleep 5

echo -e "\n3. Testing GET /api/v1/sync/status (check sync status)..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/sync/status" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n4. Testing individual sync endpoints..."

echo -e "\n   - Triggering Jira sync..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/jira/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n   - Triggering GitHub sync..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n   - Triggering Slack sync..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n   - Triggering Calendar sync..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Sync pipeline tests completed"
