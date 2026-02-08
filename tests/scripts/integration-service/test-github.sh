#!/bin/bash

# Integration Service - GitHub Integration Test
echo "========================================="
echo "Testing GitHub Integration"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

# Test GitHub endpoints
echo -e "\n1. Testing GET /api/v1/github/repositories..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/github/repositories" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing POST /api/v1/github/sync (trigger sync)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing POST /api/v1/github/webhook (simulate push event)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/github/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=test" \
  -d '{
    "commits": [
      {"id": "abc123", "message": "Test commit"}
    ],
    "repository": {
      "name": "test-repo",
      "full_name": "user/test-repo"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ GitHub integration tests completed"
