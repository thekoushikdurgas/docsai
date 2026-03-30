"""Configuration for API endpoint testing and documentation."""

import os
from typing import Optional

# Base API URL
BASE_URL: str = os.getenv("API_BASE_URL", "http://api.contact360.io:8000")

# Test user credentials
TEST_USER_EMAIL: str = os.getenv("TEST_USER_EMAIL", "user@example.com")
TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD", "password123")

# Admin credentials (optional, for testing admin endpoints)
TEST_ADMIN_EMAIL: Optional[str] = os.getenv("TEST_ADMIN_EMAIL")
TEST_ADMIN_PASSWORD: Optional[str] = os.getenv("TEST_ADMIN_PASSWORD")

# Testing configuration
MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "5"))  # Parallel test threads
TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "30"))
RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", "20"))  # requests per minute
RATE_LIMIT_WINDOW: int = 60  # seconds

# Retry configuration
MAX_RETRIES: int = 3
RETRY_DELAY: float = 1.0  # seconds

# Output configuration
OUTPUT_DIR: str = os.path.join(os.path.dirname(__file__), "output")
OUTPUT_CSV_PREFIX: str = "api_endpoints_documentation"
OUTPUT_SUMMARY_JSON: str = "api_endpoints_summary.json"
OUTPUT_ERROR_LOG: str = "api_test_errors.log"

# API version prefixes
API_V1_PREFIX: str = "/api/v1"
API_V2_PREFIX: str = "/api/v2"
API_V3_PREFIX: str = "/api/v3"
API_V4_PREFIX: str = "/api/v4"

# Backend paths
BACKEND_DIR: str = os.path.join(
    os.path.dirname(__file__), "..", "..", "backend"
)
API_ENDPOINTS_DIR: str = os.path.join(BACKEND_DIR, "app", "api")
MAIN_PY_PATH: str = os.path.join(BACKEND_DIR, "app", "main.py")
