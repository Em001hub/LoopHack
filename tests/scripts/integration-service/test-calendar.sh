#!/bin/bash

# Integration Service - Google Calendar Integration Test
echo "========================================="
echo "Testing Google Calendar Integration"
echo "========================================="

INTEGRATION_SERVICE_URL="http://localhost:8000"

# Test Calendar endpoints
echo -e "\n1. Testing GET /api/v1/calendar/events..."
curl -X GET "${INTEGRATION_SERVICE_URL}/api/v1/calendar/events?calendar_id=primary" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing POST /api/v1/calendar/sync (trigger sync)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/sync" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing POST /api/v1/calendar/webhook (simulate event update)..."
curl -X POST "${INTEGRATION_SERVICE_URL}/api/v1/calendar/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceState": "exists"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Calendar integration tests completed"
