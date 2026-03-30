"""
Email Single API Test Script (Optimized with Multi-threading and Batch Processing)

This script tests the /api/v2/email/single/ endpoint using data from a CSV file.
It compares the API responses with known email addresses to verify accuracy.

Optimizations:
- Multi-threading for concurrent API calls
- Batch processing for better throughput
- Thread-safe CSV writing
- Connection pooling for HTTP requests
- Smart rate limiting (respects backend limits)
- Retry logic with exponential backoff
- Real-time progress tracking
"""

import csv
import json
import os
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Optional
from urllib.parse import urlparse

import requests
from datetime import datetime

from api_token import get_access_token, get_tokens, refresh_token


@dataclass
class TestResult:
    """Stores the result of a single API test."""
    first_name: str
    last_name: str
    domain: str
    expected_email: str
    api_email: Optional[str]
    api_source: Optional[str]
    api_status: Optional[str]
    api_certainty: Optional[str]
    match: bool
    error: Optional[str]
    response_time_ms: float
    # Email verification fields
    verification_status: Optional[str] = None  # valid, invalid, catchall, unknown
    verification_provider: Optional[str] = None  # bulkmailverifier, truelist
    verification_error: Optional[str] = None
    verification_response_time_ms: float = 0.0
    # Source file tracking
    source_file: Optional[str] = None  # Name of the CSV file this result came from
    # Batch and threading info
    batch_id: Optional[int] = None
    row_index: Optional[int] = None


class RateLimiter:
    """Thread-safe rate limiter using token bucket algorithm."""
    
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times = deque()
        self.lock = Lock()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        with self.lock:
            now = time.time()
            
            # Remove requests outside the window
            while self.request_times and (now - self.request_times[0]) > self.window_seconds:
                self.request_times.popleft()
            
            # If at limit, wait until oldest request expires
            if len(self.request_times) >= self.max_requests:
                wait_time = self.window_seconds - (now - self.request_times[0]) + 0.1
                if wait_time > 0:
                    time.sleep(wait_time)
                    # Clean up again after waiting
                    now = time.time()
                    while self.request_times and (now - self.request_times[0]) > self.window_seconds:
                        self.request_times.popleft()
            
            # Record this request
            self.request_times.append(time.time())


class EmailAPITester:
    """Tests the Email Single API endpoint with multi-threading and batch processing."""
    
    def __init__(
        self,
        api_url: str,
        bearer_token: str,
        refresh_token: str,
        data_dir: str,
        verifier_url: str = None,
        verifier_provider: str = 'truelist',
        max_workers: int = 5,
        batch_size: int = 50,
        max_requests_per_minute: int = 20,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the API tester.
        
        Args:
            api_url: API endpoint URL
            bearer_token: Bearer token for authentication
            refresh_token: Refresh token for token renewal
            data_dir: Directory containing CSV files
            verifier_url: Email verification endpoint URL
            verifier_provider: Verification provider name
            max_workers: Number of worker threads for concurrent processing
            batch_size: Number of rows to process in each batch
            max_requests_per_minute: Maximum API requests per minute (for rate limiting)
            retry_attempts: Number of retry attempts for failed requests
            retry_delay: Initial delay between retries (exponential backoff)
        """
        self.api_url = api_url
        self.bearer_token = bearer_token
        self.refresh_token = refresh_token
        self.data_dir = Path(data_dir)
        self.verifier_url = verifier_url or api_url.replace('/single/', '/single/verifier/')
        self.verifier_provider = verifier_provider
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        
        # Thread-safe collections
        self.results: list[TestResult] = []
        self.results_lock = Lock()
        self.processed_files: list[str] = []
        
        # CSV writing (thread-safe)
        self.csv_file_handle = None
        self.csv_writer = None
        self.csv_output_path = None
        self.csv_lock = Lock()
        
        # Rate limiter
        self.rate_limiter = RateLimiter(max_requests_per_minute, 60)
        
        # Progress tracking
        self.progress_lock = Lock()
        self.completed_count = 0
        self.total_count = 0
        self.error_count = 0
        
        # Token refresh lock (thread-safe token refresh)
        self.token_refresh_lock = Lock()
        
        # Track CSV data in memory (row_id -> CSV row data) for updates
        self.csv_data: dict[str, dict] = {}
        
        # Track initial CSV data count for statistics (before processing starts)
        self.initial_csv_data_count: int = 0
        
        # Create session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using the refresh token.
        Updates both bearer_token and refresh_token, and updates session headers.
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        with self.token_refresh_lock:
            try:
                new_access_token, new_refresh_token = refresh_token(self.refresh_token)
                self.bearer_token = new_access_token
                self.refresh_token = new_refresh_token
                # Update session headers with new token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.bearer_token}',
                })
                print(f"  🔄 Token refreshed successfully")
                return True
            except Exception as e:
                print(f"  ❌ Token refresh failed: {e}")
                return False
    
    def get_row_identifier(self, row: dict) -> str:
        """
        Create a unique identifier for a row to track if it's been processed.
        Uses first_name + last_name + domain (or expected_email if available).
        
        Args:
            row: Dictionary containing CSV row data
            
        Returns:
            str: Unique identifier for the row
        """
        first_name = row.get('First Name', '').strip().lower()
        last_name = row.get('Last Name', '').strip().lower()
        expected_email = row.get('Email', '').strip().lower()
        
        # If we have an email, use it as the primary identifier
        if expected_email and '@' in expected_email:
            return expected_email
        
        # Otherwise, use first_name + last_name + domain
        domain = ""
        if 'Domain' in row:
            domain = row.get('Domain', '').strip().lower()
        elif "@" in expected_email:
            domain = expected_email.split("@", 1)[1].strip().lower()
        else:
            website = row.get('Website', '').strip()
            domain = self.extract_domain(website).lower()
        
        return f"{first_name}|{last_name}|{domain}"
    
    def get_row_identifier_from_csv_row(self, csv_row: dict) -> str:
        """
        Create a unique identifier from a CSV output row.
        
        Args:
            csv_row: Dictionary containing CSV row data from output file
            
        Returns:
            str: Unique identifier for the row
        """
        first_name = csv_row.get('first_name', '').strip().lower()
        last_name = csv_row.get('last_name', '').strip().lower()
        expected_email = csv_row.get('expected_email', '').strip().lower()
        domain = csv_row.get('domain', '').strip().lower()
        
        # Use email if available, otherwise use name+domain
        if expected_email and '@' in expected_email:
            return expected_email
        else:
            return f"{first_name}|{last_name}|{domain}"
    
    def load_existing_csv_data(self, output_csv_path: Path) -> dict[str, dict]:
        """
        Load existing CSV data into dictionary for updates.
        
        Args:
            output_csv_path: Path to the output CSV file
            
        Returns:
            dict: Dictionary mapping row_id to CSV row data
        """
        csv_data = {}
        
        if not output_csv_path.exists():
            return csv_data
        
        try:
            with open(output_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create identifier from output CSV row
                    row_id = self.get_row_identifier_from_csv_row(row)
                    # Store full row data
                    csv_data[row_id] = row
        except Exception as e:
            print(f"  ⚠️  Warning: Could not read existing output file: {e}")
            print(f"  Starting fresh...")
        
        return csv_data
    
    def should_skip_row(self, row: dict) -> bool:
        """
        Check if a row should be skipped (already exists in CSV with match=TRUE).
        
        Args:
            row: Dictionary containing CSV row data from input file
            
        Returns:
            bool: True if row exists in CSV and has match=TRUE, False otherwise
        """
        row_id = self.get_row_identifier(row)
        
        # Check if row exists in CSV data
        if row_id not in self.csv_data:
            return False  # New row, don't skip
        
        # Check if match is TRUE
        existing_row = self.csv_data[row_id]
        match_value = existing_row.get('match', '').strip().upper()
        
        # Skip if match is TRUE
        return match_value == 'TRUE'
    
    def extract_domain(self, website: str) -> str:
        """Extract domain from website URL."""
        if not website:
            return ""
        
        # Clean up the URL
        website = website.strip()
        
        # Add protocol if missing
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        try:
            parsed = urlparse(website)
            domain = parsed.netloc or parsed.path
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain.lower()
        except Exception as e:
            print(f"Error extracting domain from {website}: {e}")
            return ""
    
    def make_api_call(self, first_name: str, last_name: str, domain: str, retry_count: int = 0, token_refreshed: bool = False) -> tuple[dict, float]:
        """
        Make API call to email/single/ endpoint with retry logic and automatic token refresh.
        Returns (response_json, response_time_ms).
        """
        # Rate limiting
        self.rate_limiter.wait_if_needed()
        
        payload = {
            'provider': 'truelist',
            'first_name': first_name,
            'last_name': last_name,
            'domain': domain,
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=30,
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            # Check for 401 Unauthorized - token expired
            if response.status_code == 401:
                # Try to refresh token if we haven't already tried
                if not token_refreshed:
                    if self.refresh_access_token():
                        # Retry the request with new token
                        return self.make_api_call(first_name, last_name, domain, retry_count, token_refreshed=True)
                    else:
                        # Token refresh failed, raise error
                        raise requests.exceptions.HTTPError(
                            f"401 Unauthorized and token refresh failed",
                            response=response
                        )
                else:
                    # Already tried refreshing, still getting 401
                    response.raise_for_status()
            
            response.raise_for_status()
            return response.json(), response_time_ms
        except requests.exceptions.HTTPError as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            # If it's a 401 and we haven't refreshed yet, try refreshing
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
                if not token_refreshed:
                    if self.refresh_access_token():
                        # Retry the request with new token
                        return self.make_api_call(first_name, last_name, domain, retry_count, token_refreshed=True)
            
            # Retry logic with exponential backoff (for non-401 errors or after refresh attempt)
            if retry_count < self.retry_attempts:
                wait_time = self.retry_delay * (2 ** retry_count)
                time.sleep(wait_time)
                return self.make_api_call(first_name, last_name, domain, retry_count + 1, token_refreshed)
            
            raise Exception(f"API call failed after {self.retry_attempts} retries: {str(e)}")
        except requests.exceptions.RequestException as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            # Retry logic with exponential backoff
            if retry_count < self.retry_attempts:
                wait_time = self.retry_delay * (2 ** retry_count)
                time.sleep(wait_time)
                return self.make_api_call(first_name, last_name, domain, retry_count + 1, token_refreshed)
            
            raise Exception(f"API call failed after {self.retry_attempts} retries: {str(e)}")
    
    def verify_email(self, email: str, retry_count: int = 0, token_refreshed: bool = False) -> tuple[Optional[str], Optional[str], Optional[str], float]:
        """
        Verify an email address using the verifier endpoint with retry logic and automatic token refresh.
        Returns (status, provider, error, response_time_ms).
        Status can be: 'valid', 'invalid', 'catchall', 'unknown', or None if error.
        """
        if not email or '@' not in email:
            return None, None, "Invalid email format", 0.0
        
        # Rate limiting
        self.rate_limiter.wait_if_needed()
        
        payload = {
            'provider': self.verifier_provider,
            'email': email.lower().strip(),
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                self.verifier_url,
                json=payload,
                timeout=30,
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            # Check for 401 Unauthorized - token expired
            if response.status_code == 401:
                # Try to refresh token if we haven't already tried
                if not token_refreshed:
                    if self.refresh_access_token():
                        # Retry the request with new token
                        return self.verify_email(email, retry_count, token_refreshed=True)
                    else:
                        # Token refresh failed, return error
                        return None, None, f"401 Unauthorized and token refresh failed", response_time_ms
                else:
                    # Already tried refreshing, still getting 401
                    response.raise_for_status()
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract verification status from response
            result = response_data.get('result', {})
            status = result.get('status')
            
            # Convert status to string if it's an enum-like value
            if status:
                status = str(status).lower()
            
            return status, self.verifier_provider, None, response_time_ms
        except requests.exceptions.HTTPError as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            # If it's a 401 and we haven't refreshed yet, try refreshing
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
                if not token_refreshed:
                    if self.refresh_access_token():
                        # Retry the request with new token
                        return self.verify_email(email, retry_count, token_refreshed=True)
            
            # Retry logic with exponential backoff (for non-401 errors or after refresh attempt)
            if retry_count < self.retry_attempts:
                wait_time = self.retry_delay * (2 ** retry_count)
                time.sleep(wait_time)
                return self.verify_email(email, retry_count + 1, token_refreshed)
            
            return None, None, f"Verification failed after {self.retry_attempts} retries: {str(e)}", response_time_ms
        except requests.exceptions.RequestException as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            # Retry logic with exponential backoff
            if retry_count < self.retry_attempts:
                wait_time = self.retry_delay * (2 ** retry_count)
                time.sleep(wait_time)
                return self.verify_email(email, retry_count + 1, token_refreshed)
            
            return None, None, f"Verification failed after {self.retry_attempts} retries: {str(e)}", response_time_ms
    
    def test_single_row(self, row: dict, source_file: str = None, batch_id: int = None, row_index: int = None) -> TestResult:
        """Test a single row from the CSV.

        Supports multiple CSV formats:
        - Format 1: First Name, Last Name, Email, Website
          - Domain from Email column (e.g. 'suraj@dbaux.com' -> 'dbaux.com')
          - Fallback: Website URL via extract_domain()
        - Format 2: First Name, Last Name, Domain
          - Domain directly from Domain column
        """
        first_name = row.get('First Name', '').strip()
        last_name = row.get('Last Name', '').strip()

        # Expected email from CSV (used for comparison only)
        raw_email = row.get('Email', '').strip()
        expected_email = raw_email.lower()

        # Determine domain based on CSV format
        domain = ""
        
        # Check if CSV has a direct Domain column (Format 2)
        if 'Domain' in row:
            domain = row.get('Domain', '').strip().lower()
        else:
            # Format 1: Extract domain from Email column
            if "@" in raw_email:
                domain_part = raw_email.split("@", 1)[1].strip()
                if domain_part:
                    domain = domain_part.lower()
            
            # Fallback: derive domain from Website column if email domain is unavailable
            if not domain:
                website = row.get('Website', '').strip()
                domain = self.extract_domain(website)
        
        # Initialize result with error state
        result = TestResult(
            first_name=first_name,
            last_name=last_name,
            domain=domain,
            expected_email=expected_email,
            api_email=None,
            api_source=None,
            api_status=None,
            api_certainty=None,
            match=False,
            error=None,
            response_time_ms=0,
            verification_status=None,
            verification_provider=None,
            verification_error=None,
            verification_response_time_ms=0.0,
            source_file=source_file,
            batch_id=batch_id,
            row_index=row_index,
        )
        
        try:
            response_data, response_time_ms = self.make_api_call(first_name, last_name, domain)
            
            result.response_time_ms = response_time_ms
            result.api_email = response_data.get('email')
            result.api_source = response_data.get('source')
            result.api_status = response_data.get('status')
            result.api_certainty = response_data.get('certainty')
            
            # Compare emails (case-insensitive)
            if result.api_email:
                result.match = result.api_email.lower() == expected_email
            
        except Exception as e:
            result.error = str(e)
            with self.progress_lock:
                self.error_count += 1
        
        # Verify the expected email from CSV if it exists
        if expected_email and '@' in expected_email:
            try:
                status, provider, ver_error, ver_time = self.verify_email(expected_email)
                result.verification_status = status
                result.verification_provider = provider
                result.verification_error = ver_error
                result.verification_response_time_ms = ver_time
            except Exception as e:
                result.verification_error = f"Verification exception: {str(e)}"
        
        return result
    
    def find_csv_files(self) -> list[Path]:
        """Find all CSV files in the data directory."""
        csv_files = sorted(self.data_dir.glob('*.csv'))
        return csv_files
    
    def initialize_csv_output(self, source_csv_filename: str):
        """
        Initialize CSV output file for row-by-row updates.
        Output file will have the same name as the source CSV file.
        Loads existing CSV data into memory for updates.
        
        Args:
            source_csv_filename: Name of the source CSV file (e.g., "data.csv")
        """
        # Get the script's directory and create output subdirectory
        script_dir = Path(__file__).parent
        output_dir = script_dir / 'output'
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        # Use the same filename as the source CSV
        self.csv_output_path = output_dir / source_csv_filename
        
        # Load existing CSV data into memory
        file_exists = self.csv_output_path.exists()
        if file_exists:
            print(f"📂 Found existing output file: {self.csv_output_path.name}")
            self.csv_data = self.load_existing_csv_data(self.csv_output_path)
            self.initial_csv_data_count = len(self.csv_data)
            if self.initial_csv_data_count > 0:
                print(f"  ✅ Loaded {self.initial_csv_data_count} existing rows - will update them with latest results")
            else:
                print(f"  ℹ️  File exists but appears empty - starting fresh")
        else:
            self.csv_data = {}
            self.initial_csv_data_count = 0
            print(f"📂 Creating new output file: {self.csv_output_path.name}")
        
        # Don't open file handle yet - we'll rewrite the entire file after each batch
        self.csv_file_handle = None
        self.csv_writer = None
        
        # Define CSV columns in a logical order (needed for rewriting)
        self.csv_fieldnames = [
            # Source file
            'source_file',
            # Input fields
            'first_name',
            'last_name',
            'domain',
            'expected_email',
            # API response fields
            'api_email',
            'api_source',
            'api_status',
            'api_certainty',
            # Match and error status
            'match',
            'error',
            # Performance metrics
            'response_time_ms',
            # Email verification fields
            'verification_status',
            'verification_provider',
            'verification_error',
            'verification_response_time_ms',
        ]
        
        # Print relative path for better readability
        relative_path = self.csv_output_path.relative_to(script_dir)
        print(f"📊 CSV output file initialized: {relative_path}")
        print(f"   (Results will be updated/added and file rewritten after each batch)\n")
    
    def save_result_to_csv(self, result: TestResult):
        """
        Update in-memory CSV data dictionary with test result (thread-safe).
        The actual CSV file will be rewritten after each batch.
        
        Args:
            result: TestResult object to save
        """
        # Convert result to CSV row
        row = {
            'source_file': result.source_file or '',
            'first_name': result.first_name or '',
            'last_name': result.last_name or '',
            'domain': result.domain or '',
            'expected_email': result.expected_email or '',
            'api_email': result.api_email or '',
            'api_source': result.api_source or '',
            'api_status': result.api_status or '',
            'api_certainty': result.api_certainty or '',
            'match': 'TRUE' if result.match else 'FALSE',
            'error': result.error or '',
            'response_time_ms': f"{result.response_time_ms:.2f}" if result.response_time_ms else '',
            'verification_status': result.verification_status or '',
            'verification_provider': result.verification_provider or '',
            'verification_error': result.verification_error or '',
            'verification_response_time_ms': f"{result.verification_response_time_ms:.2f}" if result.verification_response_time_ms else '',
        }
        
        # Get row identifier
        row_id = self.get_row_identifier_from_csv_row(row)
        
        # Thread-safe update of in-memory dictionary
        with self.csv_lock:
            self.csv_data[row_id] = row
    
    def rewrite_csv_file(self):
        """
        Rewrite the entire CSV file from in-memory dictionary (thread-safe).
        This ensures all updates are persisted to disk.
        """
        if not self.csv_output_path:
            return
        
        with self.csv_lock:
            try:
                # Write entire CSV file from dictionary
                with open(self.csv_output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)
                    writer.writeheader()
                    
                    # Sort rows by row_id for consistent ordering
                    sorted_row_ids = sorted(self.csv_data.keys())
                    for row_id in sorted_row_ids:
                        writer.writerow(self.csv_data[row_id])
                    
                    f.flush()
            except Exception as e:
                print(f"  ⚠️  Warning: Could not rewrite CSV file: {e}")
    
    def close_csv_output(self):
        """
        Final rewrite of CSV file and cleanup.
        Ensures all data is persisted before closing.
        """
        # Final rewrite to ensure all data is saved
        self.rewrite_csv_file()
        
        # Cleanup
        self.csv_file_handle = None
        self.csv_writer = None
        
        if self.csv_output_path:
            script_dir = Path(__file__).parent
            relative_path = self.csv_output_path.relative_to(script_dir)
            print(f"📊 CSV output file finalized: {relative_path}")
    
    def process_batch(self, rows: list[tuple[int, dict]], source_file: str, batch_id: int) -> list[TestResult]:
        """
        Process a batch of rows concurrently.
        
        Args:
            rows: List of (row_index, row_dict) tuples
            source_file: Name of the source CSV file
            batch_id: Batch identifier
            
        Returns:
            List of TestResult objects
        """
        batch_results = []
        
        # Process rows in this batch using thread pool
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(rows))) as executor:
            # Submit all tasks
            future_to_row = {
                executor.submit(
                    self.test_single_row,
                    row_dict,
                    source_file,
                    batch_id,
                    row_index
                ): (row_index, row_dict)
                for row_index, row_dict in rows
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_row):
                row_index, row_dict = future_to_row[future]
                try:
                    result = future.result()
                    batch_results.append(result)
                    
                    # Save result immediately (thread-safe) and check if it was an update
                    was_updated = self.save_result_to_csv(result)
                    
                    # Update progress
                    with self.progress_lock:
                        self.completed_count += 1
                        completed = self.completed_count
                        total = self.total_count
                        percentage = (completed / total * 100) if total > 0 else 0
                        
                        # Print progress every 10 completions or on errors
                        if completed % 10 == 0 or result.error:
                            status_parts = []
                            # Indicate if row was updated or is new
                            if was_updated:
                                status_parts.append("🔄 UPDATED")
                            else:
                                status_parts.append("➕ NEW")
                            
                            if result.error:
                                status_parts.append(f"❌ ERROR: {result.error}")
                            elif result.match:
                                status_parts.append(f"✅ MATCH ({result.response_time_ms:.0f}ms)")
                            elif result.api_email:
                                status_parts.append(f"⚠️  MISMATCH")
                            else:
                                status_parts.append(f"❓ NO EMAIL")
                            
                            if result.verification_status:
                                ver_icon = {
                                    'valid': '✅',
                                    'invalid': '❌',
                                    'catchall': '⚠️',
                                    'unknown': '❓'
                                }.get(result.verification_status, '❓')
                                status_parts.append(f"{ver_icon} VERIFY: {result.verification_status.upper()}")
                            
                            print(f"  [{completed}/{total}] ({percentage:.1f}%) {result.first_name} {result.last_name}... {' | '.join(status_parts)}")
                
                except Exception as e:
                    # Handle unexpected errors
                    with self.progress_lock:
                        self.error_count += 1
                    print(f"  ❌ Unexpected error processing row {row_index}: {e}")
        
        # Rewrite CSV file after batch completes to persist all updates
        self.rewrite_csv_file()
        
        return batch_results
    
    def process_csv_file(self, csv_file: Path) -> int:
        """
        Process a single CSV file in batches with multi-threading.
        Creates output files with the same name as the input CSV file.
        Returns the number of rows processed.
        """
        file_name = csv_file.name
        print(f"\n{'='*80}")
        print(f"📁 Processing: {file_name}")
        print(f"{'='*80}")
        
        # Initialize output CSV file for this specific CSV file
        self.initialize_csv_output(file_name)
        
        # Store results for this file separately
        file_results = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                all_rows = list(reader)
            
            total_rows = len(all_rows)
            print(f"📊 Total rows in file: {total_rows}")
            
            # Filter rows: skip rows that exist AND have match=TRUE
            rows_to_process = []
            skipped_matched_count = 0
            existing_unmatched_count = 0
            new_count = 0
            
            for idx, row in enumerate(all_rows):
                row_id = self.get_row_identifier(row)
                
                if self.should_skip_row(row):
                    # Row exists and has match=TRUE, skip it
                    skipped_matched_count += 1
                else:
                    # Row should be processed (new or existing with match=FALSE)
                    rows_to_process.append((idx, row))
                    
                    # Count by type
                    if row_id in self.csv_data:
                        existing_unmatched_count += 1
                    else:
                        new_count += 1
            
            rows_to_process_count = len(rows_to_process)
            
            # Print summary
            print(f"📝 Row analysis:")
            if skipped_matched_count > 0:
                print(f"   ⏭️  Skipped (already matched): {skipped_matched_count} rows")
            if existing_unmatched_count > 0:
                print(f"   🔄 Will update (match=FALSE): {existing_unmatched_count} rows")
            if new_count > 0:
                print(f"   ➕ Will process (new): {new_count} rows")
            
            if rows_to_process_count == 0:
                print(f"✅ All rows already have match=TRUE. Skipping file.")
                return 0
            
            print(f"🔧 Configuration: {self.max_workers} workers, batch size: {self.batch_size}")
            
            # Update total count (only count rows that will be processed)
            with self.progress_lock:
                self.total_count += rows_to_process_count
            
            # Process in batches
            batch_results = []
            num_batches = (rows_to_process_count + self.batch_size - 1) // self.batch_size
            
            for batch_id in range(num_batches):
                start_idx = batch_id * self.batch_size
                end_idx = min(start_idx + self.batch_size, rows_to_process_count)
                batch_rows = rows_to_process[start_idx:end_idx]
                
                # Calculate actual row numbers for display (original index + 1)
                first_original_idx = batch_rows[0][0] + 1 if batch_rows else 0
                last_original_idx = batch_rows[-1][0] + 1 if batch_rows else 0
                
                print(f"\n  📦 Processing batch {batch_id + 1}/{num_batches} (rows {first_original_idx}-{last_original_idx}, {len(batch_rows)} rows)...")
                batch_start_time = time.time()
                
                # Process batch
                results = self.process_batch(batch_rows, file_name, batch_id)
                batch_results.extend(results)
                
                batch_time = time.time() - batch_start_time
                print(f"  ✅ Batch {batch_id + 1} completed in {batch_time:.1f}s ({len(results)} results)")
            
            # Calculate final statistics
            final_csv_data_count = len(self.csv_data)
            actual_new_count = final_csv_data_count - self.initial_csv_data_count
            updated_count = existing_unmatched_count  # Rows that existed with match=FALSE and were updated
            
            # Store results for this file
            file_results = batch_results
            with self.results_lock:
                self.results.extend(batch_results)
            
            print(f"\n✅ Completed: {file_name}")
            if skipped_matched_count > 0:
                print(f"   ⏭️  Skipped (already matched): {skipped_matched_count} rows")
            print(f"   🔄 Updated (match=FALSE): {updated_count} rows")
            print(f"   ➕ New: {actual_new_count} new rows")
            print(f"   📊 Total in output: {final_csv_data_count} rows")
            
            # Save JSON report for this file
            self.save_detailed_report(file_name, file_results)
            
        finally:
            # Always close CSV file for this input file
            self.close_csv_output()
        
        return rows_to_process_count
    
    def run_tests(self):
        """
        Run tests on all CSV files in the data directory with multi-threading.
        """
        print(f"\n{'='*80}")
        print(f"Email Single API Test (Optimized) - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        print(f"📁 Data Directory: {self.data_dir}")
        print(f"🔗 API Endpoint: {self.api_url}")
        print(f"🎯 Provider: truelist (with IcyPeas integration)")
        print(f"🔍 Verifier Endpoint: {self.verifier_url}")
        print(f"🔍 Verifier Provider: {self.verifier_provider}")
        print(f"⚙️  Max Workers: {self.max_workers}")
        print(f"📦 Batch Size: {self.batch_size}")
        print(f"🚦 Rate Limit: {self.rate_limiter.max_requests} requests/minute")
        print(f"🔄 Retry Attempts: {self.retry_attempts}")
        
        # Find all CSV files
        csv_files = self.find_csv_files()
        
        if not csv_files:
            print(f"❌ No CSV files found in {self.data_dir}")
            return
        
        print(f"\n📋 Found {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            print(f"   - {csv_file.name}")
        
        print(f"\n{'='*80}\n")
        
        try:
            start_time = time.time()
            
            # Process each CSV file (each file creates its own output files)
            total_rows_processed = 0
            for csv_file in csv_files:
                rows_in_file = self.process_csv_file(csv_file)
                total_rows_processed += rows_in_file
                self.processed_files.append(csv_file.name)
            
            total_time = time.time() - start_time
            
            print(f"\n{'='*80}")
            print(f"📊 ALL FILES PROCESSED")
            print(f"{'='*80}")
            print(f"Total Files: {len(csv_files)}")
            print(f"Total Rows: {total_rows_processed}")
            print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
            print(f"Average Time per Row: {total_time/total_rows_processed:.2f}s" if total_rows_processed > 0 else "")
            print(f"Throughput: {total_rows_processed/total_time:.2f} rows/second" if total_time > 0 else "")
            print(f"{'='*80}\n")
            
            # Print combined statistics across all files
            self.print_statistics()
            
        finally:
            # Always close session, even if there's an error
            # (CSV files are closed per-file in process_csv_file)
            self.session.close()
    
    def print_statistics(self):
        """Print test statistics."""
        total = len(self.results)
        if total == 0:
            print("No results to display.")
            return
        
        matches = sum(1 for r in self.results if r.match)
        mismatches = sum(1 for r in self.results if r.api_email and not r.match)
        no_email = sum(1 for r in self.results if not r.api_email and not r.error)
        errors = sum(1 for r in self.results if r.error)
        
        avg_response_time = sum(r.response_time_ms for r in self.results) / total
        
        # Verification statistics
        verified_emails = [r for r in self.results if r.expected_email and '@' in r.expected_email]
        verification_total = len(verified_emails)
        verification_valid = sum(1 for r in verified_emails if r.verification_status == 'valid')
        verification_invalid = sum(1 for r in verified_emails if r.verification_status == 'invalid')
        verification_catchall = sum(1 for r in verified_emails if r.verification_status == 'catchall')
        verification_unknown = sum(1 for r in verified_emails if r.verification_status == 'unknown')
        verification_errors = sum(1 for r in verified_emails if r.verification_error)
        avg_verification_time = sum(r.verification_response_time_ms for r in verified_emails) / verification_total if verification_total > 0 else 0
        
        print("📈 TEST STATISTICS")
        print(f"{'='*80}")
        print(f"Total Tests:        {total}")
        print(f"✅ Matches:         {matches} ({matches/total*100:.1f}%)")
        print(f"⚠️  Mismatches:      {mismatches} ({mismatches/total*100:.1f}%)")
        print(f"❓ No Email Found:  {no_email} ({no_email/total*100:.1f}%)")
        print(f"❌ Errors:          {errors} ({errors/total*100:.1f}%)")
        print(f"\n⏱️  Avg Response Time: {avg_response_time:.0f}ms")
        
        # Email Verification Statistics
        if verification_total > 0:
            print(f"\n🔍 EMAIL VERIFICATION STATISTICS")
            print(f"{'='*80}")
            print(f"Total Verified:     {verification_total}")
            print(f"✅ Valid:           {verification_valid} ({verification_valid/verification_total*100:.1f}%)")
            print(f"❌ Invalid:         {verification_invalid} ({verification_invalid/verification_total*100:.1f}%)")
            print(f"⚠️  Catchall:        {verification_catchall} ({verification_catchall/verification_total*100:.1f}%)")
            print(f"❓ Unknown:         {verification_unknown} ({verification_unknown/verification_total*100:.1f}%)")
            print(f"❌ Verify Errors:   {verification_errors} ({verification_errors/verification_total*100:.1f}%)")
            print(f"\n⏱️  Avg Verification Time: {avg_verification_time:.0f}ms")
        
        # Source breakdown
        sources = {}
        for r in self.results:
            if r.api_source:
                sources[r.api_source] = sources.get(r.api_source, 0) + 1
        
        if sources:
            print(f"\n📍 Sources:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"   {source}: {count} ({count/total*100:.1f}%)")
        
        # Certainty breakdown (for IcyPeas results)
        certainties = {}
        for r in self.results:
            if r.api_certainty:
                certainties[r.api_certainty] = certainties.get(r.api_certainty, 0) + 1
        
        if certainties:
            print(f"\n🎯 Certainty Levels:")
            for certainty, count in sorted(certainties.items(), key=lambda x: x[1], reverse=True):
                print(f"   {certainty}: {count} ({count/total*100:.1f}%)")
        
        print(f"{'='*80}\n")
    
    def save_detailed_report(self, source_csv_filename: str, file_results: list[TestResult] = None):
        """
        Save detailed results to a JSON file in the output directory.
        Output file will have the same base name as the source CSV file (with .json extension).
        
        Args:
            source_csv_filename: Name of the source CSV file (e.g., "data.csv")
            file_results: List of TestResult objects for this file (if None, uses all results)
        """
        # Get the script's directory and create output subdirectory
        script_dir = Path(__file__).parent
        output_dir = script_dir / 'output'
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        # Use the same base name as source CSV, but with .json extension (always overwrite)
        source_path = Path(source_csv_filename)
        json_filename = source_path.stem + '.json'
        output_file = output_dir / json_filename
        
        # Use provided results or all results
        results_to_save = file_results if file_results is not None else self.results
        
        report = {
            'test_info': {
                'timestamp': datetime.now().isoformat(),
                'api_url': self.api_url,
                'data_dir': str(self.data_dir),
                'source_file': source_csv_filename,
                'total_tests': len(results_to_save),
                'configuration': {
                    'max_workers': self.max_workers,
                    'batch_size': self.batch_size,
                    'max_requests_per_minute': self.rate_limiter.max_requests,
                    'retry_attempts': self.retry_attempts,
                },
            },
            'statistics': {
                'matches': sum(1 for r in results_to_save if r.match),
                'mismatches': sum(1 for r in results_to_save if r.api_email and not r.match),
                'no_email': sum(1 for r in results_to_save if not r.api_email and not r.error),
                'errors': sum(1 for r in results_to_save if r.error),
                'avg_response_time_ms': sum(r.response_time_ms for r in results_to_save) / len(results_to_save) if results_to_save else 0,
                'verification': {
                    'total_verified': sum(1 for r in results_to_save if r.expected_email and '@' in r.expected_email),
                    'valid': sum(1 for r in results_to_save if r.verification_status == 'valid'),
                    'invalid': sum(1 for r in results_to_save if r.verification_status == 'invalid'),
                    'catchall': sum(1 for r in results_to_save if r.verification_status == 'catchall'),
                    'unknown': sum(1 for r in results_to_save if r.verification_status == 'unknown'),
                    'errors': sum(1 for r in results_to_save if r.verification_error),
                    'avg_verification_time_ms': sum(r.verification_response_time_ms for r in results_to_save if r.verification_response_time_ms > 0) / max(1, sum(1 for r in results_to_save if r.verification_response_time_ms > 0)),
                },
            },
            'results': [
                {
                    'first_name': r.first_name,
                    'last_name': r.last_name,
                    'domain': r.domain,
                    'expected_email': r.expected_email,
                    'api_email': r.api_email,
                    'api_source': r.api_source,
                    'api_status': r.api_status,
                    'api_certainty': r.api_certainty,
                    'match': r.match,
                    'error': r.error,
                    'response_time_ms': r.response_time_ms,
                    'verification_status': r.verification_status,
                    'verification_provider': r.verification_provider,
                    'verification_error': r.verification_error,
                    'verification_response_time_ms': r.verification_response_time_ms,
                    'source_file': r.source_file,
                }
                for r in results_to_save
            ],
        }
        
        # Save to output directory
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Print relative path for better readability
        relative_path = output_file.relative_to(script_dir)
        print(f"💾 Detailed JSON report saved to: {relative_path}")


def main():
    """Main entry point."""
    base = os.getenv("API_BASE_URL", "http://api.contact360.io:8000").rstrip("/")
    API_URL = os.getenv("EMAIL_SINGLE_API_URL", f"{base}/api/v2/email/single/")
    DATA_DIR = os.getenv("EMAIL_SINGLE_DATA_DIR", "data")

    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "5"))
    BATCH_SIZE = int(os.getenv("EMAIL_SINGLE_BATCH_SIZE", "50"))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT", "20"))
    RETRY_ATTEMPTS = int(os.getenv("EMAIL_SINGLE_RETRY_ATTEMPTS", "3"))
    RETRY_DELAY = float(os.getenv("EMAIL_SINGLE_RETRY_DELAY", "1.0"))

    EMAIL = os.getenv("TEST_USER_EMAIL", "user@example.com")
    PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")
    print(f'Obtaining access token and refresh token for {EMAIL} ...')
    bearer_token, refresh_token_value = get_tokens(EMAIL, PASSWORD)
    print('Tokens acquired. Starting tests...')
    
    # Create tester with optimized settings
    tester = EmailAPITester(
        API_URL,
        bearer_token,
        refresh_token_value,
        DATA_DIR,
        max_workers=MAX_WORKERS,
        batch_size=BATCH_SIZE,
        max_requests_per_minute=MAX_REQUESTS_PER_MINUTE,
        retry_attempts=RETRY_ATTEMPTS,
        retry_delay=RETRY_DELAY,
    )
    tester.run_tests()


if __name__ == '__main__':
    main()
