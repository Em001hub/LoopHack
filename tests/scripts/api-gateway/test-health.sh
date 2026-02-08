#!/bin/bash

# API Gateway Health Check Test
echo "========================================="
echo "Testing API Gateway Health Endpoint"
echo "========================================="

API_GATEWAY_URL="http://localhost:3000"

# Test health endpoint
echo -e "\n1. Testing /api/health endpoint..."
curl -X GET "${API_GATEWAY_URL}/api/health" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo -e "\n✅ Health check test completed"
