#!/bin/bash

# Integration Service - Slack Integration Test
echo "========================================="
echo "Testing Slack Integration"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

# Test Slack endpoints
echo -e "\n1. Testing GET /api/v1/slack/channels..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/slack/channels" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing GET /api/v1/slack/users..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/slack/users" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing POST /api/v1/slack/sync (trigger sync)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n4. Testing POST /api/v1/slack/webhook (URL verification)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/slack/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "challenge": "test_challenge_123"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Slack integration tests completed"
