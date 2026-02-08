#!/bin/bash

# API Gateway Routes Test
echo "========================================="
echo "Testing API Gateway Routes"
echo "========================================="

API_GATEWAY_URL="http://localhost:3000"

# Test project routes
echo -e "\n1. Testing /api/projects endpoint (all sources)..."
curl -X GET "${API_GATEWAY_URL}/api/projects" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n2. Testing /api/projects/jira/projects endpoint..."
curl -X GET "${API_GATEWAY_URL}/api/projects/jira/projects" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n3. Testing /api/projects/github/repositories endpoint..."
curl -X GET "${API_GATEWAY_URL}/api/projects/github/repositories" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n4. Testing /api/projects/slack/channels endpoint..."
curl -X GET "${API_GATEWAY_URL}/api/projects/slack/channels" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n5. Testing /api/projects/calendar/events endpoint..."
curl -X GET "${API_GATEWAY_URL}/api/projects/calendar/events" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Route tests completed"
