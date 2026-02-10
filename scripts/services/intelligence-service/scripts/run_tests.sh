#!/bin/bash
# Test Runner Script for Intelligence Service
# Runs all test suites with coverage report

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🧪 ProjectMind Intelligence Service - Test Runner          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Navigate to the service directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo -e "${YELLOW}📁 Working directory: $(pwd)${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest is not installed. Installing...${NC}"
    pip install pytest pytest-cov pytest-asyncio
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo -e "${GREEN}🧪 Running API Endpoint Tests...${NC}"
echo "════════════════════════════════════════════════════════════════"
pytest tests/api/test_all_endpoints.py -v --tb=short || true
echo ""

echo -e "${GREEN}🔗 Running Integration Tests...${NC}"
echo "════════════════════════════════════════════════════════════════"
pytest tests/integration/test_end_to_end.py -v --tb=short || true
echo ""

echo -e "${GREEN}📊 Running All Tests with Coverage...${NC}"
echo "════════════════════════════════════════════════════════════════"
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html --tb=short || true
echo ""

echo -e "${GREEN}✓ Test run complete!${NC}"
echo ""
echo "Coverage report saved to: htmlcov/index.html"
echo ""
echo "To view coverage report:"
echo "  open htmlcov/index.html (macOS)"
echo "  xdg-open htmlcov/index.html (Linux)"
echo "  start htmlcov/index.html (Windows)"
