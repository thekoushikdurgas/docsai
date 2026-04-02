"""Test API endpoints and measure response times."""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from endpoint_discovery import EndpointInfo
from endpoint_test_config import (
    BASE_URL,
    MAX_RETRIES,
    RATE_LIMIT,
    RATE_LIMIT_WINDOW,
    RETRY_DELAY,
    TEST_ADMIN_EMAIL,
    TEST_ADMIN_PASSWORD,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    TIMEOUT_SECONDS,
)
from api_token import get_access_token, get_tokens


@dataclass
class TestResult:
    """Result of testing an endpoint."""
    endpoint: EndpointInfo
    status_code: Optional[int] = None
    response_time_ms: float = 0.0
    success: bool = False
    error_message: Optional[str] = None
    requires_auth: bool = False
    requires_admin: bool = False
    sla_gate_status: str = "unknown"
    test_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class RateLimiter:
    """Thread-safe rate limiter."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times = []
        self.lock = False  # Simple lock for single-threaded use
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove old requests outside the window
        self.request_times = [
            t for t in self.request_times 
            if (now - t) < self.window_seconds
        ]
        
        # If at limit, wait until oldest request expires
        if len(self.request_times) >= self.max_requests:
            oldest = min(self.request_times)
            wait_time = self.window_seconds - (now - oldest) + 0.1
            if wait_time > 0:
                time.sleep(wait_time)
                # Clean up again after waiting
                now = time.time()
                self.request_times = [
                    t for t in self.request_times 
                    if (now - t) < self.window_seconds
                ]
        
        # Record this request
        self.request_times.append(time.time())


class EndpointTester:
    """Tests API endpoints and measures response times."""
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        admin_token: Optional[str] = None,
        sla_gate: Optional[Any] = None,
        service_id: str = "default",
    ):
        self.access_token = access_token
        self.admin_token = admin_token
        self.sla_gate = sla_gate
        self.service_id = service_id
        self.rate_limiter = RateLimiter(RATE_LIMIT, RATE_LIMIT_WINDOW)
        
        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def test_endpoint(self, endpoint: EndpointInfo) -> TestResult:
        """Test a single endpoint and return the result."""
        result = TestResult(endpoint=endpoint)
        
        # Rate limiting
        self.rate_limiter.wait_if_needed()
        
        # Build URL
        url = urljoin(BASE_URL, endpoint.full_path)
        
        # Prepare headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        # Determine which token to use
        token = None
        if endpoint.full_path.startswith("/api/v2/auth/login") or \
           endpoint.full_path.startswith("/api/v2/auth/register"):
            # Public endpoints, no token needed
            token = None
        elif "/admin/" in endpoint.full_path or endpoint.category.lower() == "billing":
            # Admin endpoints
            token = self.admin_token or self.access_token
        else:
            # Regular authenticated endpoints
            token = self.access_token
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        # Prepare request data
        json_data = None
        params = None
        
        if endpoint.method in ("POST", "PUT", "PATCH"):
            json_data = self._get_minimal_payload(endpoint)
        elif endpoint.method == "GET":
            # Add minimal query params for pagination endpoints
            if "limit" in endpoint.full_path or "offset" in endpoint.full_path:
                params = {"limit": 1, "offset": 0}
            elif "count" in endpoint.full_path:
                # Count endpoints don't need params
                params = {}
        
        # Handle path parameters (UUIDs, etc.)
        url = self._replace_path_params(url, endpoint)
        
        try:
            # Measure response time
            start_time = time.perf_counter()
            
            # Make request
            response = self.session.request(
                method=endpoint.method if endpoint.method != "WEBSOCKET" else "GET",
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=TIMEOUT_SECONDS,
            )
            
            end_time = time.perf_counter()
            result.response_time_ms = (end_time - start_time) * 1000
            result.status_code = response.status_code
            
            # Determine success
            if 200 <= response.status_code < 300:
                result.success = True
            elif response.status_code == 401:
                result.requires_auth = True
                result.error_message = "Unauthorized - authentication required"
            elif response.status_code == 403:
                result.requires_admin = True
                result.error_message = "Forbidden - admin access required"
            elif response.status_code == 404:
                # Might be a path parameter issue
                result.error_message = f"Not found - may require valid path parameters"
            elif response.status_code == 400:
                # Bad request - might be invalid payload, but endpoint exists
                result.success = True  # Endpoint exists
                result.error_message = "Bad request - invalid payload (expected for discovery)"
            elif response.status_code >= 500:
                result.error_message = f"Server error: {response.status_code}"
            else:
                result.error_message = f"HTTP {response.status_code}"
        
        except requests.exceptions.Timeout:
            result.error_message = "Request timeout"
        except requests.exceptions.ConnectionError:
            result.error_message = "Connection error"
        except Exception as e:
            result.error_message = f"Error: {str(e)}"
        
        # Update endpoint info based on result
        endpoint.requires_auth = result.requires_auth
        endpoint.requires_admin = result.requires_admin
        
        if self.sla_gate is not None:
            gate = self.sla_gate.check([result], self.service_id)
            result.sla_gate_status = gate.status
        else:
            result.sla_gate_status = "pass"

        return result
    
    def _get_minimal_payload(self, endpoint: EndpointInfo) -> Dict[str, Any]:
        """Generate minimal valid payload for POST/PUT endpoints."""
        payload = {}
        
        # Auth endpoints
        if "login" in endpoint.full_path:
            payload = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
            }
        elif "register" in endpoint.full_path:
            payload = {
                "email": f"test_{int(time.time())}@example.com",
                "password": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            }
        elif "refresh" in endpoint.full_path:
            # Would need refresh token, skip for now
            payload = {"refresh_token": ""}
        elif "linkedin" in endpoint.full_path.lower():
            if "export" in endpoint.full_path:
                payload = {"urls": ["https://linkedin.com/in/test"]}
            else:
                payload = {"url": "https://linkedin.com/in/test"}
        elif "email" in endpoint.full_path.lower():
            if "finder" in endpoint.full_path:
                payload = {
                    "first_name": "John",
                    "last_name": "Doe",
                    "domain": "example.com",
                }
            elif "verifier" in endpoint.full_path or "single" in endpoint.full_path:
                payload = {"email": "test@example.com"}
            elif "export" in endpoint.full_path:
                payload = {"emails": ["test@example.com"]}
        elif "apollo" in endpoint.full_path.lower():
            if "analyze" in endpoint.full_path:
                payload = {"url": "https://apollo.io/test"}
            elif "contacts" in endpoint.full_path:
                payload = {"filters": {}}
        elif "export" in endpoint.full_path.lower():
            if "contacts" in endpoint.full_path:
                payload = {"filters": {}, "format": "csv"}
            elif "companies" in endpoint.full_path:
                payload = {"filters": {}, "format": "csv"}
        elif "billing" in endpoint.full_path.lower():
            if "subscribe" in endpoint.full_path:
                payload = {"plan_tier": "FreeUser", "period": "monthly"}
            elif "addon" in endpoint.full_path:
                payload = {"package_id": 1, "quantity": 1}
        elif "usage" in endpoint.full_path.lower() and "track" in endpoint.full_path:
            payload = {"feature": "test", "count": 1}
        elif "ai_chat" in endpoint.full_path.lower() or "ai-chat" in endpoint.full_path.lower():
            if "message" in endpoint.full_path:
                payload = {"message": "test"}
            else:
                payload = {"title": "Test Chat"}
        elif "gemini" in endpoint.full_path.lower():
            if "email" in endpoint.full_path:
                payload = {"email": "test@example.com"}
            elif "company" in endpoint.full_path:
                payload = {"company_uuid": "00000000-0000-0000-0000-000000000000"}
        elif "sales_navigator" in endpoint.full_path.lower() or "sales-navigator" in endpoint.full_path.lower():
            payload = {"url": "https://linkedin.com/sales/test"}
        elif "cleanup" in endpoint.full_path.lower():
            # These need UUIDs, will fail but that's ok
            payload = {}
        elif "analysis" in endpoint.full_path.lower():
            # These need UUIDs, will fail but that's ok
            payload = {}
        elif "validation" in endpoint.full_path.lower():
            # These need UUIDs, will fail but that's ok
            payload = {}
        elif "data_pipeline" in endpoint.full_path.lower() or "data-pipeline" in endpoint.full_path.lower():
            payload = {"source": "test"}
        elif "email_pattern" in endpoint.full_path.lower():
            if "analyze" in endpoint.full_path or "import" in endpoint.full_path:
                payload = {"company_uuid": "00000000-0000-0000-0000-000000000000"}
            else:
                payload = {"pattern": "first.last@domain.com", "company_uuid": "00000000-0000-0000-0000-000000000000"}
        elif "bulk" in endpoint.full_path.lower():
            payload = {"data": []}
        
        return payload
    
    def _replace_path_params(self, url: str, endpoint: EndpointInfo) -> str:
        """Replace path parameters with dummy values."""
        # Common UUID pattern
        dummy_uuid = "00000000-0000-0000-0000-000000000000"
        
        # Replace {uuid}, {contact_uuid}, {company_uuid}, etc.
        import re
        url = re.sub(r'\{[^}]*(uuid|id|job_id|export_id|chat_id|pattern_uuid|file_id|tier|package_id|period)[^}]*\}', 
                    dummy_uuid, url)
        
        # Replace {file_type} and {slug} for download endpoints
        url = re.sub(r'\{file_type\}', 'csv', url)
        url = re.sub(r'\{slug\}', 'test', url)
        
        # Replace path parameters like {full_path:path}
        url = re.sub(r'\{[^}]*:path\}', 'test', url)
        
        return url


def authenticate_user() -> Optional[str]:
    """Authenticate and get access token."""
    try:
        token = get_access_token(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        return token
    except Exception as e:
        print(f"Warning: Could not authenticate user: {e}")
        return None


def authenticate_admin() -> Optional[str]:
    """Authenticate admin and get access token."""
    if not TEST_ADMIN_EMAIL or not TEST_ADMIN_PASSWORD:
        return None
    
    try:
        token = get_access_token(TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD)
        return token
    except Exception as e:
        print(f"Warning: Could not authenticate admin: {e}")
        return None
