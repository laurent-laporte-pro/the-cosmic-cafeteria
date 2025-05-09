#!/bin/bash

# Script to run unit tests for the Cosmic Cafeteria API

# Set environment variables for testing
export FLASK_APP="app:app"
export FLASK_DEBUG=0
export FLASK_ENV=testing

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running unit tests for the Cosmic Cafeteria API...${NC}"

# Run the tests with pytest
python -m pytest tests/ -v --cov=src --cov-report=term --cov-report=html:htmlcov/unit

# Check the exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All unit tests passed!${NC}"
    echo "Unit test coverage report generated in htmlcov/ directory"
    echo "Open htmlcov/index.html in a browser to view the detailed report"
else
    echo -e "${RED}Some unit tests failed!${NC}"
    exit 1
fi