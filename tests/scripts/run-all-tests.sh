#!/bin/bash

# Master Test Runner
echo "========================================="
echo "ProjectMind - Master Test Runner"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track test results
PASSED=0
FAILED=0

# Function to run a test script
run_test() {
    local test_name=$1
    local test_script=$2
    
    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    if bash "$test_script"; then
        echo -e "${GREEN}✅ PASSED: ${test_name}${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAILED: ${test_name}${NC}"
        ((FAILED++))
    fi
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "\n========================================="
echo "Phase 1: API Gateway Tests"
echo "========================================="

run_test "API Gateway Health Check" "${SCRIPT_DIR}/api-gateway/test-health.sh"
run_test "API Gateway Routes" "${SCRIPT_DIR}/api-gateway/test-routes.sh"

echo -e "\n========================================="
echo "Phase 2: Integration Service Tests"
echo "========================================="

run_test "Jira Integration" "${SCRIPT_DIR}/integration-service/test-jira.sh"
run_test "GitHub Integration" "${SCRIPT_DIR}/integration-service/test-github.sh"
run_test "Slack Integration" "${SCRIPT_DIR}/integration-service/test-slack.sh"
run_test "Calendar Integration" "${SCRIPT_DIR}/integration-service/test-calendar.sh"

echo -e "\n========================================="
echo "Phase 3: Sync Pipeline Tests"
echo "========================================="

run_test "Sync Pipeline" "${SCRIPT_DIR}/integration-service/test-sync.sh"

echo -e "\n========================================="
echo "Phase 4: Webhook Processing Tests"
echo "========================================="

run_test "Webhook Processing" "${SCRIPT_DIR}/integration-service/test-webhooks.sh"

echo -e "\n========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo -e "Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
