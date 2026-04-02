"""
Email Pattern Generator & Validator

This script processes CSV files to:
1. Validate emails using the verification API
2. Extract email patterns by domain (company)
3. Create/update patterns via the email-patterns API
4. Generate comprehensive reports

Usage:
    python email_pattern_generator.py
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlparse

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from api_token import get_tokens, refresh_token

API_TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", os.getenv("TIMEOUT", "300")))


@dataclass
class Contact:
    """Represents a contact with email information."""
    first_name: str
    last_name: str
    domain: str
    email: str
    verification_status: Optional[str] = None
    source_file: Optional[str] = None


@dataclass
class Pattern:
    """Represents an email pattern for a domain."""
    pattern_format: str  # e.g., "first.last", "firstlast"
    pattern_string: str  # e.g., "john.doe", "johndoe"
    contact_count: int
    confidence_score: float
    is_auto_extracted: bool = True
    domain: str = ""
    company_uuid: Optional[str] = None
    pattern_uuid: Optional[str] = None
    api_status: Optional[str] = None
    api_error: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of email validation."""
    email: str
    is_valid: bool
    verification_status: Optional[str]  # valid, invalid, catchall, unknown
    verification_provider: Optional[str]
    verification_error: Optional[str]
    verification_time_ms: float
    pattern_detected: Optional[str] = None
    domain: Optional[str] = None


class RateLimiter:
    """Thread-safe rate limiter using token bucket algorithm."""
    
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times = []
        self.lock = Lock()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        with self.lock:
            now = time.time()
            # Remove requests outside the window
            self.request_times = [t for t in self.request_times if (now - t) <= self.window_seconds]
            
            # If at limit, wait until oldest request expires
            if len(self.request_times) >= self.max_requests:
                wait_time = self.window_seconds - (now - self.request_times[0]) + 0.1
                if wait_time > 0:
                    time.sleep(wait_time)
                    now = time.time()
                    self.request_times = [t for t in self.request_times if (now - t) <= self.window_seconds]
            
            # Record this request
            self.request_times.append(time.time())


class EmailPatternExtractor:
    """Extracts email patterns from contact data."""
    
    def __init__(self, min_pattern_count: int = 3, min_confidence: float = 0.6):
        self.min_pattern_count = min_pattern_count
        self.min_confidence = min_confidence
    
    def extract_pattern_format(self, email: str, first_name: str, last_name: str) -> Optional[str]:
        """
        Extract pattern format from email and names.
        
        Returns pattern format string or None if pattern cannot be determined.
        """
        if not email or '@' not in email:
            return None
        
        local_part = email.split('@')[0].lower().strip()
        first = first_name.lower().strip() if first_name else ""
        last = last_name.lower().strip() if last_name else ""
        
        if not first and not last:
            return None
        
        # Pattern: first.last
        if first and last and local_part == f"{first}.{last}":
            return "first.last"
        
        # Pattern: firstlast
        if first and last and local_part == f"{first}{last}":
            return "firstlast"
        
        # Pattern: first
        if first and local_part == first:
            return "first"
        
        # Pattern: f.last
        if first and last and len(first) > 0 and local_part == f"{first[0]}.{last}":
            return "f.last"
        
        # Pattern: first_last
        if first and last and local_part == f"{first}_{last}":
            return "first_last"
        
        # Pattern: flast
        if first and last and len(first) > 0 and local_part == f"{first[0]}{last}":
            return "flast"
        
        # Pattern: firstl (first + first letter of last)
        if first and last and len(last) > 0 and local_part == f"{first}{last[0]}":
            return "firstl"
        
        # Pattern: f_last
        if first and last and len(first) > 0 and local_part == f"{first[0]}_{last}":
            return "f_last"
        
        # Pattern: last.first
        if first and last and local_part == f"{last}.{first}":
            return "last.first"
        
        # Pattern: lastfirst
        if first and last and local_part == f"{last}{first}":
            return "lastfirst"
        
        # Pattern: l.first (last initial + first)
        if first and last and len(last) > 0 and local_part == f"{last[0]}.{first}":
            return "l.first"
        
        return None
    
    def generate_pattern_string(self, pattern_format: str, first_name: str, last_name: str) -> Optional[str]:
        """Generate pattern string from format and names."""
        first = first_name.lower().strip() if first_name else ""
        last = last_name.lower().strip() if last_name else ""
        
        pattern_map = {
            "first.last": f"{first}.{last}" if first and last else None,
            "firstlast": f"{first}{last}" if first and last else None,
            "first": first if first else None,
            "f.last": f"{first[0]}.{last}" if first and last and len(first) > 0 else None,
            "first_last": f"{first}_{last}" if first and last else None,
            "flast": f"{first[0]}{last}" if first and last and len(first) > 0 else None,
            "firstl": f"{first}{last[0]}" if first and last and len(last) > 0 else None,
            "f_last": f"{first[0]}_{last}" if first and last and len(first) > 0 else None,
            "last.first": f"{last}.{first}" if first and last else None,
            "lastfirst": f"{last}{first}" if first and last else None,
            "l.first": f"{last[0]}.{first}" if first and last and len(last) > 0 else None,
        }
        
        return pattern_map.get(pattern_format)
    
    def analyze_domain_patterns(self, contacts: List[Contact]) -> List[Pattern]:
        """
        Analyze contacts grouped by domain and extract patterns.
        
        Args:
            contacts: List of contacts (should be from same domain)
            
        Returns:
            List of detected patterns with confidence scores
        """
        if not contacts:
            return []
        
        domain = contacts[0].domain
        pattern_counts: Dict[str, int] = defaultdict(int)
        pattern_examples: Dict[str, Tuple[str, str]] = {}  # format -> (pattern_string, email)
        
        # Extract patterns from each contact
        for contact in contacts:
            if not contact.email or '@' not in contact.email:
                continue
            
            pattern_format = self.extract_pattern_format(
                contact.email, contact.first_name, contact.last_name
            )
            
            if pattern_format:
                pattern_counts[pattern_format] += 1
                # Store example pattern string
                pattern_string = self.generate_pattern_string(
                    pattern_format, contact.first_name, contact.last_name
                )
                if pattern_string and pattern_format not in pattern_examples:
                    pattern_examples[pattern_format] = (pattern_string, contact.email)
        
        # Filter patterns by minimum count
        total_contacts = len(contacts)
        patterns = []
        
        for pattern_format, count in pattern_counts.items():
            if count >= self.min_pattern_count:
                confidence = self.calculate_confidence(count, total_contacts)
                if confidence >= self.min_confidence:
                    pattern_string, _ = pattern_examples.get(pattern_format, ("", ""))
                    patterns.append(Pattern(
                        pattern_format=pattern_format,
                        pattern_string=pattern_string,
                        contact_count=count,
                        confidence_score=confidence,
                        is_auto_extracted=True,
                        domain=domain
                    ))
        
        # Sort by contact count (descending)
        patterns.sort(key=lambda p: p.contact_count, reverse=True)
        
        return patterns
    
    def calculate_confidence(self, pattern_count: int, total_count: int) -> float:
        """
        Calculate confidence score for a pattern.
        
        Confidence based on:
        - Frequency: higher count = higher confidence
        - Consistency: % of emails matching pattern
        """
        if total_count == 0:
            return 0.0
        
        # Frequency score (max at 10+ occurrences)
        frequency_score = min(pattern_count / 10.0, 1.0)
        
        # Consistency score (% of emails matching pattern)
        consistency_score = pattern_count / total_count
        
        # Weighted combination
        confidence = (frequency_score * 0.3) + (consistency_score * 0.7)
        
        return round(confidence, 3)


class EmailValidator:
    """Validates emails using the verification API."""
    
    def __init__(self, api_url: str, bearer_token: str, refresh_token: str, rate_limiter: RateLimiter):
        self.api_url = api_url
        self.bearer_token = bearer_token
        self.refresh_token = refresh_token
        self.rate_limiter = rate_limiter
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        self.token_refresh_lock = Lock()
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token."""
        with self.token_refresh_lock:
            try:
                new_access_token, new_refresh_token = refresh_token(self.refresh_token)
                self.bearer_token = new_access_token
                self.refresh_token = new_refresh_token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.bearer_token}',
                })
                return True
            except Exception as e:
                print(f"  ❌ Token refresh failed: {e}")
                return False
    
    def verify_email(self, email: str, retry_count: int = 0, token_refreshed: bool = False) -> ValidationResult:
        """Verify an email address."""
        if not email or '@' not in email:
            return ValidationResult(
                email=email,
                is_valid=False,
                verification_status=None,
                verification_provider=None,
                verification_error="Invalid email format",
                verification_time_ms=0.0
            )
        
        self.rate_limiter.wait_if_needed()
        
        payload = {
            'provider': 'truelist',
            'email': email.lower().strip(),
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=API_TIMEOUT_SECONDS,
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            # Check for 401 Unauthorized
            if response.status_code == 401:
                if not token_refreshed:
                    if self.refresh_access_token():
                        return self.verify_email(email, retry_count, token_refreshed=True)
                return ValidationResult(
                    email=email,
                    is_valid=False,
                    verification_status=None,
                    verification_provider=None,
                    verification_error=f"401 Unauthorized",
                    verification_time_ms=response_time_ms
                )
            
            response.raise_for_status()
            response_data = response.json()
            
            result = response_data.get('result', {})
            status = result.get('status')
            if status:
                status = str(status).lower()
            
            is_valid = status in ['valid', 'catchall']
            
            return ValidationResult(
                email=email,
                is_valid=is_valid,
                verification_status=status,
                verification_provider='truelist',
                verification_error=None,
                verification_time_ms=response_time_ms
            )
        except requests.exceptions.HTTPError as e:
            response_time_ms = (time.time() - start_time) * 1000
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
                if not token_refreshed:
                    if self.refresh_access_token():
                        return self.verify_email(email, retry_count, token_refreshed=True)
            return ValidationResult(
                email=email,
                is_valid=False,
                verification_status=None,
                verification_provider=None,
                verification_error=f"HTTP Error: {str(e)}",
                verification_time_ms=response_time_ms
            )
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                email=email,
                is_valid=False,
                verification_status=None,
                verification_provider=None,
                verification_error=f"Error: {str(e)}",
                verification_time_ms=response_time_ms
            )


class PatternAPIClient:
    """Client for email-patterns API."""
    
    def __init__(self, api_base_url: str, bearer_token: str, refresh_token: str, rate_limiter: RateLimiter):
        self.api_base_url = api_base_url.rstrip('/')
        self.bearer_token = bearer_token
        self.refresh_token = refresh_token
        self.rate_limiter = rate_limiter
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        self.token_refresh_lock = Lock()
        # Cache for company UUID lookups
        self.company_uuid_cache: Dict[str, Optional[str]] = {}
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token."""
        with self.token_refresh_lock:
            try:
                new_access_token, new_refresh_token = refresh_token(self.refresh_token)
                self.bearer_token = new_access_token
                self.refresh_token = new_refresh_token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.bearer_token}',
                })
                return True
            except Exception as e:
                print(f"  ❌ Token refresh failed: {e}")
                return False
    
    def lookup_company_by_domain(self, domain: str) -> Optional[str]:
        """
        Lookup company UUID by domain.
        
        For now, we'll use a simple approach: generate a UUID from domain hash.
        In production, this should query the company API.
        """
        if domain in self.company_uuid_cache:
            return self.company_uuid_cache[domain]
        
        # For testing: use a predefined company UUID or generate from domain
        # In production, query: GET /api/v1/companies/?domain={domain}
        # For now, return None to indicate we need company_uuid from user or API
        self.company_uuid_cache[domain] = None
        return None
    
    def create_pattern(self, company_uuid: str, pattern: Pattern, upsert: bool = False) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create or update an email pattern via API.
        
        Returns:
            (success, pattern_uuid, error_message)
        """
        if not company_uuid:
            return False, None, "Company UUID is required"
        
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.api_base_url}/api/v2/email-patterns/?upsert={str(upsert).lower()}"
        
        payload = {
            'company_uuid': company_uuid,
            'pattern_format': pattern.pattern_format,
            'pattern_string': pattern.pattern_string,
            'contact_count': pattern.contact_count,
            'is_auto_extracted': pattern.is_auto_extracted,
        }
        
        start_time = time.time()
        try:
            response = self.session.post(url, json=payload, timeout=API_TIMEOUT_SECONDS)
            response_time_ms = (time.time() - start_time) * 1000
            
            # Check for 401
            if response.status_code == 401:
                if self.refresh_access_token():
                    return self.create_pattern(company_uuid, pattern, upsert)
                return False, None, "401 Unauthorized and token refresh failed"
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract pattern UUID from response
            pattern_uuid = response_data.get('uuid') or response_data.get('pattern_uuid')
            
            return True, pattern_uuid, None
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('detail', str(e))
                except:
                    error_msg = str(e)
            else:
                error_msg = str(e)
            return False, None, f"HTTP Error: {error_msg}"
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def update_pattern(self, pattern_uuid: str, updates: Dict) -> Tuple[bool, Optional[str]]:
        """Update an existing pattern."""
        if not pattern_uuid:
            return False, "Pattern UUID is required"
        
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.api_base_url}/api/v2/email-patterns/{pattern_uuid}"
        
        start_time = time.time()
        try:
            response = self.session.put(url, json=updates, timeout=API_TIMEOUT_SECONDS)
            
            if response.status_code == 401:
                if self.refresh_access_token():
                    return self.update_pattern(pattern_uuid, updates)
                return False, "401 Unauthorized and token refresh failed"
            
            response.raise_for_status()
            return True, None
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('detail', str(e))
                except:
                    error_msg = str(e)
            else:
                error_msg = str(e)
            return False, f"HTTP Error: {error_msg}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_company_patterns(self, company_uuid: str) -> List[Dict]:
        """Get all patterns for a company."""
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.api_base_url}/api/v2/email-patterns/company/{company_uuid}"
        
        try:
            response = self.session.get(url, timeout=API_TIMEOUT_SECONDS)
            
            if response.status_code == 401:
                if self.refresh_access_token():
                    return self.get_company_patterns(company_uuid)
                return []
            
            response.raise_for_status()
            response_data = response.json()
            
            # Response format may vary, handle both list and dict
            if isinstance(response_data, list):
                return response_data
            elif isinstance(response_data, dict):
                patterns = response_data.get('patterns', [])
                if patterns:
                    return patterns
                # If 'patterns' key doesn't exist, return the whole dict as a list
                return [response_data] if response_data else []
            return []
        except Exception as e:
            print(f"  ⚠️  Warning: Could not fetch patterns for company {company_uuid}: {e}")
            return []


class ReportGenerator:
    """Generates CSV and JSON reports."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_validation_csv(self, results: List[ValidationResult], filename: Optional[str] = None) -> Path:
        """Generate validation report CSV."""
        if filename is None:
            filename = f"email_validation_report_{self.timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'email', 'is_valid', 'verification_status', 'verification_provider',
                'verification_error', 'verification_time_ms', 'pattern_detected', 'domain'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                writer.writerow({
                    'email': result.email,
                    'is_valid': result.is_valid,
                    'verification_status': result.verification_status or '',
                    'verification_provider': result.verification_provider or '',
                    'verification_error': result.verification_error or '',
                    'verification_time_ms': f"{result.verification_time_ms:.2f}",
                    'pattern_detected': result.pattern_detected or '',
                    'domain': result.domain or '',
                })
        
        return filepath
    
    def generate_pattern_csv(self, patterns: List[Pattern], filename: Optional[str] = None) -> Path:
        """Generate pattern analysis CSV."""
        if filename is None:
            filename = f"email_patterns_by_domain_{self.timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'domain', 'pattern_format', 'pattern_string', 'contact_count',
                'confidence_score', 'is_auto_extracted', 'company_uuid',
                'pattern_uuid', 'api_status', 'api_error'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for pattern in patterns:
                writer.writerow({
                    'domain': pattern.domain,
                    'pattern_format': pattern.pattern_format,
                    'pattern_string': pattern.pattern_string,
                    'contact_count': pattern.contact_count,
                    'confidence_score': f"{pattern.confidence_score:.3f}",
                    'is_auto_extracted': pattern.is_auto_extracted,
                    'company_uuid': pattern.company_uuid or '',
                    'pattern_uuid': pattern.pattern_uuid or '',
                    'api_status': pattern.api_status or '',
                    'api_error': pattern.api_error or '',
                })
        
        return filepath
    
    def generate_json_report(self, summary: Dict, filename: Optional[str] = None) -> Path:
        """Generate comprehensive JSON report."""
        if filename is None:
            filename = f"email_pattern_analysis_{self.timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return filepath


class EmailPatternGenerator:
    """Main class for email pattern generation pipeline."""
    
    def __init__(
        self,
        api_base_url: str,
        bearer_token: str,
        refresh_token: str,
        input_dir: Path,
        output_dir: Path,
        min_pattern_count: int = 3,
        min_confidence: float = 0.6,
        max_workers: int = 5,
        max_requests_per_minute: int = 20,
        company_uuid: Optional[str] = None,  # Optional: use same company_uuid for all domains
    ):
        self.api_base_url = api_base_url
        self.bearer_token = bearer_token
        self.refresh_token = refresh_token
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.company_uuid = company_uuid  # If provided, use for all domains
        
        # Initialize components
        self.rate_limiter = RateLimiter(max_requests_per_minute, 60)
        self.pattern_extractor = EmailPatternExtractor(min_pattern_count, min_confidence)
        self.validator = EmailValidator(
            f"{api_base_url}/api/v2/email/single/verifier/",
            bearer_token,
            refresh_token,
            self.rate_limiter
        )
        self.api_client = PatternAPIClient(
            api_base_url,
            bearer_token,
            refresh_token,
            self.rate_limiter
        )
        self.report_generator = ReportGenerator(output_dir)
        
        # Results storage
        self.validation_results: List[ValidationResult] = []
        self.patterns: List[Pattern] = []
        self.domain_contacts: Dict[str, List[Contact]] = defaultdict(list)
        
        # Statistics
        self.stats = {
            'total_contacts': 0,
            'valid_emails': 0,
            'invalid_emails': 0,
            'domains_analyzed': 0,
            'patterns_detected': 0,
            'patterns_created': 0,
            'patterns_failed': 0,
        }
    
    def load_csv_files(self) -> List[Path]:
        """Find all CSV files in input directory."""
        csv_files = sorted(self.input_dir.glob('*.csv'))
        return csv_files
    
    def read_contacts_from_csv(self, csv_file: Path) -> List[Contact]:
        """Read contacts from CSV file."""
        contacts = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    first_name = row.get('first_name', '').strip()
                    last_name = row.get('last_name', '').strip()
                    domain = row.get('domain', '').strip()
                    email = row.get('expected_email', '').strip() or row.get('api_email', '').strip()
                    verification_status = row.get('verification_status', '').strip()
                    source_file = row.get('source_file', csv_file.name)
                    
                    if not email or '@' not in email:
                        continue
                    
                    # Extract domain from email if not provided
                    if not domain and '@' in email:
                        domain = email.split('@')[1].strip()
                    
                    if domain:
                        contact = Contact(
                            first_name=first_name,
                            last_name=last_name,
                            domain=domain.lower(),
                            email=email.lower(),
                            verification_status=verification_status if verification_status else None,
                            source_file=source_file
                        )
                        contacts.append(contact)
        except Exception as e:
            print(f"  ❌ Error reading {csv_file.name}: {e}")
        
        return contacts
    
    def validate_emails(self, contacts: List[Contact], max_workers: int = 5) -> List[ValidationResult]:
        """Validate emails in parallel."""
        results = []
        
        def validate_contact(contact: Contact) -> ValidationResult:
            result = self.validator.verify_email(contact.email)
            result.domain = contact.domain
            return result
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_contact = {
                executor.submit(validate_contact, contact): contact
                for contact in contacts
            }
            
            for future in as_completed(future_to_contact):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    contact = future_to_contact[future]
                    results.append(ValidationResult(
                        email=contact.email,
                        is_valid=False,
                        verification_status=None,
                        verification_provider=None,
                        verification_error=f"Validation exception: {str(e)}",
                        verification_time_ms=0.0,
                        domain=contact.domain
                    ))
        
        return results
    
    def group_contacts_by_domain(self, contacts: List[Contact]) -> Dict[str, List[Contact]]:
        """Group contacts by domain."""
        domain_contacts = defaultdict(list)
        for contact in contacts:
            domain_contacts[contact.domain].append(contact)
        return domain_contacts
    
    def extract_patterns(self, domain_contacts: Dict[str, List[Contact]]) -> List[Pattern]:
        """Extract patterns for each domain."""
        all_patterns = []
        
        for domain, contacts in domain_contacts.items():
            if len(contacts) < self.pattern_extractor.min_pattern_count:
                continue
            
            patterns = self.pattern_extractor.analyze_domain_patterns(contacts)
            all_patterns.extend(patterns)
        
        return all_patterns
    
    def create_patterns_via_api(self, patterns: List[Pattern], upsert: bool = False) -> None:
        """Create patterns via API."""
        for pattern in patterns:
            # Use provided company_uuid or lookup
            company_uuid = self.company_uuid
            if not company_uuid:
                company_uuid = self.api_client.lookup_company_by_domain(pattern.domain)
            
            if not company_uuid:
                pattern.api_status = "skipped"
                pattern.api_error = "Company UUID not available"
                self.stats['patterns_failed'] += 1
                continue
            
            pattern.company_uuid = company_uuid
            success, pattern_uuid, error = self.api_client.create_pattern(company_uuid, pattern, upsert)
            
            if success:
                pattern.pattern_uuid = pattern_uuid
                pattern.api_status = "created"
                self.stats['patterns_created'] += 1
            else:
                pattern.api_status = "failed"
                pattern.api_error = error
                self.stats['patterns_failed'] += 1
    
    def run(self, validate_emails: bool = True, create_patterns: bool = True, max_workers: int = 5, upsert: bool = False):
        """Run the complete pipeline - processes each CSV file separately."""
        print(f"\n{'='*80}")
        print(f"Email Pattern Generator - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Load CSV files
        csv_files = self.load_csv_files()
        if not csv_files:
            print(f"❌ No CSV files found in {self.input_dir}")
            return
        
        print(f"📁 Found {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            print(f"   - {csv_file.name}")
        
        # Process each CSV file separately
        all_file_stats = []
        
        for csv_file in csv_files:
            print(f"\n{'='*80}")
            print(f"📄 Processing: {csv_file.name}")
            print(f"{'='*80}")
            
            # Reset stats for this file
            file_stats = {
                'filename': csv_file.name,
                'total_contacts': 0,
                'valid_emails': 0,
                'invalid_emails': 0,
                'domains_analyzed': 0,
                'patterns_detected': 0,
                'patterns_created': 0,
                'patterns_failed': 0,
            }
            
            # Read contacts from this file
            print(f"\n📖 Reading contacts...")
            contacts = self.read_contacts_from_csv(csv_file)
            file_stats['total_contacts'] = len(contacts)
            print(f"   ✅ {len(contacts)} contacts")
            
            if not contacts:
                print(f"   ⚠️  No valid contacts found, skipping...")
                continue
            
            # Validate emails
            if validate_emails:
                print(f"\n🔍 Validating emails...")
                validation_results = self.validate_emails(contacts, max_workers)
                
                valid_count = sum(1 for r in validation_results if r.is_valid)
                invalid_count = len(validation_results) - valid_count
                file_stats['valid_emails'] = valid_count
                file_stats['invalid_emails'] = invalid_count
                
                print(f"   ✅ Valid: {valid_count}")
                print(f"   ❌ Invalid: {invalid_count}")
            else:
                # Use existing verification_status from CSV
                validation_results = []
                for contact in contacts:
                    is_valid = contact.verification_status in ['valid', 'catchall']
                    validation_results.append(ValidationResult(
                        email=contact.email,
                        is_valid=is_valid,
                        verification_status=contact.verification_status,
                        verification_provider='truelist',
                        verification_error=None,
                        verification_time_ms=0.0,
                        domain=contact.domain
                    ))
                file_stats['valid_emails'] = sum(1 for r in validation_results if r.is_valid)
                file_stats['invalid_emails'] = len(validation_results) - file_stats['valid_emails']
            
            # Filter to only valid emails for pattern extraction
            valid_contacts = [
                contact for contact, result in zip(contacts, validation_results)
                if result.is_valid
            ]
            
            # Group by domain
            print(f"\n📦 Grouping contacts by domain...")
            domain_contacts = self.group_contacts_by_domain(valid_contacts)
            file_stats['domains_analyzed'] = len(domain_contacts)
            print(f"   📊 {len(domain_contacts)} unique domains")
            
            # Extract patterns
            print(f"\n🔎 Extracting email patterns...")
            patterns = self.extract_patterns(domain_contacts)
            file_stats['patterns_detected'] = len(patterns)
            print(f"   ✅ Detected {len(patterns)} patterns")
            
            # Create patterns via API
            if create_patterns and patterns:
                print(f"\n📤 Creating patterns via API...")
                if not self.company_uuid:
                    print(f"   ⚠️  Warning: No company_uuid provided. Patterns will be skipped.")
                    print(f"   💡 Tip: Provide company_uuid parameter or implement company lookup.")
                
                # Create patterns for this file
                for pattern in patterns:
                    company_uuid = self.company_uuid
                    if not company_uuid:
                        company_uuid = self.api_client.lookup_company_by_domain(pattern.domain)
                    
                    if not company_uuid:
                        pattern.api_status = "skipped"
                        pattern.api_error = "Company UUID not available"
                        file_stats['patterns_failed'] += 1
                        continue
                    
                    pattern.company_uuid = company_uuid
                    success, pattern_uuid, error = self.api_client.create_pattern(company_uuid, pattern, upsert)
                    
                    if success:
                        pattern.pattern_uuid = pattern_uuid
                        pattern.api_status = "created"
                        file_stats['patterns_created'] += 1
                    else:
                        pattern.api_status = "failed"
                        pattern.api_error = error
                        file_stats['patterns_failed'] += 1
                
                print(f"   ✅ Created: {file_stats['patterns_created']}")
                print(f"   ❌ Failed: {file_stats['patterns_failed']}")
            
            # Generate per-file reports with same filename
            print(f"\n📊 Generating reports for {csv_file.name}...")
            
            # Output filename is same as input filename
            output_filename = csv_file.name
            
            # Generate validation CSV (same filename)
            validation_csv = self.report_generator.generate_validation_csv(
                validation_results,
                filename=output_filename
            )
            
            # Generate pattern CSV (base name + _patterns.csv)
            pattern_filename = csv_file.stem + '_patterns.csv'
            pattern_csv = self.report_generator.generate_pattern_csv(
                patterns,
                filename=pattern_filename
            )
            
            # Generate JSON report (base name + _analysis.json)
            json_filename = csv_file.stem + '_analysis.json'
            json_summary = {
                'timestamp': datetime.now().isoformat(),
                'source_file': csv_file.name,
                'statistics': file_stats,
                'configuration': {
                    'min_pattern_count': self.pattern_extractor.min_pattern_count,
                    'min_confidence': self.pattern_extractor.min_confidence,
                    'company_uuid': self.company_uuid,
                },
                'validation_summary': {
                    'total': len(validation_results),
                    'valid': file_stats['valid_emails'],
                    'invalid': file_stats['invalid_emails'],
                },
                'pattern_summary': {
                    'total_patterns': len(patterns),
                    'patterns_created': file_stats['patterns_created'],
                    'patterns_failed': file_stats['patterns_failed'],
                    'domains_analyzed': file_stats['domains_analyzed'],
                },
                'patterns_by_domain': {
                    domain: [
                        {
                            'pattern_format': p.pattern_format,
                            'pattern_string': p.pattern_string,
                            'contact_count': p.contact_count,
                            'confidence_score': p.confidence_score,
                        }
                        for p in patterns if p.domain == domain
                    ]
                    for domain in sorted(set(p.domain for p in patterns))
                }
            }
            
            json_report = self.report_generator.generate_json_report(
                json_summary,
                filename=json_filename
            )
            
            print(f"   ✅ Output file: {validation_csv.name}")
            print(f"   ✅ Pattern file: {pattern_csv.name}")
            print(f"   ✅ Analysis file: {json_report.name}")
            
            all_file_stats.append(file_stats)
        
        # Print summary across all files
        print(f"\n{'='*80}")
        print(f"📊 SUMMARY ACROSS ALL FILES")
        print(f"{'='*80}")
        total_contacts = sum(s['total_contacts'] for s in all_file_stats)
        total_valid = sum(s['valid_emails'] for s in all_file_stats)
        total_invalid = sum(s['invalid_emails'] for s in all_file_stats)
        total_domains = sum(s['domains_analyzed'] for s in all_file_stats)
        total_patterns = sum(s['patterns_detected'] for s in all_file_stats)
        total_created = sum(s['patterns_created'] for s in all_file_stats)
        total_failed = sum(s['patterns_failed'] for s in all_file_stats)
        
        print(f"Files Processed:       {len(all_file_stats)}")
        print(f"Total Contacts:        {total_contacts}")
        print(f"Valid Emails:          {total_valid}")
        print(f"Invalid Emails:        {total_invalid}")
        print(f"Domains Analyzed:      {total_domains}")
        print(f"Patterns Detected:     {total_patterns}")
        print(f"Patterns Created:      {total_created}")
        print(f"Patterns Failed:       {total_failed}")
        print(f"{'='*80}\n")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Email Pattern Generator & Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default settings
  python email_pattern_generator.py

  # Use specific company UUID for all domains
  python email_pattern_generator.py --company-uuid "398cce44-233d-5f7c-aea1-e4a6a79df10c"

  # Re-validate all emails
  python email_pattern_generator.py --validate-emails

  # Skip API pattern creation (analysis only)
  python email_pattern_generator.py --no-create-patterns

  # Note: Input/output directories are hardcoded:
  #   Input: scripts/api_test/files/email_finder
  #   Output: scripts/api_test/files/email_pattern

  # Custom pattern detection thresholds
  python email_pattern_generator.py --min-pattern-count 5 --min-confidence 0.7
        """
    )
    
    # API Configuration
    parser.add_argument(
        '--api-url',
        type=str,
        default='http://api.contact360.io:8000',
        help='API base URL (default: http://api.contact360.io:8000)'
    )
    
    
    # Company Configuration
    parser.add_argument(
        '--company-uuid',
        type=str,
        default=None,
        help='Company UUID to use for all domains (optional)'
    )
    
    # Input/Output (hardcoded - not configurable)
    # Input: scripts/api_test/files/email_finder
    # Output: scripts/api_test/files/email_pattern
    
    # Pattern Detection
    parser.add_argument(
        '--min-pattern-count',
        type=int,
        default=3,
        help='Minimum number of contacts required to establish a pattern (default: 3)'
    )
    
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.6,
        help='Minimum confidence score for pattern detection (default: 0.6)'
    )
    
    # Processing Options
    parser.add_argument(
        '--validate-emails',
        action='store_true',
        help='Re-validate all emails via API (default: use existing verification_status from CSV)'
    )
    
    parser.add_argument(
        '--no-create-patterns',
        action='store_true',
        help='Skip creating patterns via API (analysis only)'
    )
    
    parser.add_argument(
        '--max-workers',
        type=int,
        default=5,
        help='Maximum number of worker threads (default: 5)'
    )
    
    parser.add_argument(
        '--max-requests-per-minute',
        type=int,
        default=20,
        help='Maximum API requests per minute (default: 20)'
    )
    
    parser.add_argument(
        '--upsert',
        action='store_true',
        help='Use upsert mode when creating patterns (update if exists)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Configuration
    # Get fresh tokens via login helper
    # NOTE: Replace these with your real test credentials
    EMAIL = 'user@example.com'
    PASSWORD = 'password123'
    print(f'Obtaining access token and refresh token for {EMAIL} ...')
    try:
        bearer_token, refresh_token_value = get_tokens(EMAIL, PASSWORD)
        print('Tokens acquired. Starting pattern generation...')
    except Exception as e:
        print(f'❌ Failed to get tokens: {e}')
        sys.exit(1)
    
    # Hardcoded paths
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'files' / 'email_finder'
    output_dir = script_dir / 'files' / 'email_pattern'
    
    # Validate input directory
    if not input_dir.exists():
        print(f'❌ Input directory does not exist: {input_dir}')
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f'📁 Input directory: {input_dir}')
    print(f'📁 Output directory: {output_dir}')
    
    # Create generator
    generator = EmailPatternGenerator(
        api_base_url=args.api_url,
        bearer_token=bearer_token,
        refresh_token=refresh_token_value,
        input_dir=input_dir,
        output_dir=output_dir,
        min_pattern_count=args.min_pattern_count,
        min_confidence=args.min_confidence,
        max_workers=args.max_workers,
        max_requests_per_minute=args.max_requests_per_minute,
        company_uuid=args.company_uuid,
    )
    
    # Run pipeline
    try:
        generator.run(
            validate_emails=args.validate_emails,
            create_patterns=not args.no_create_patterns,
            max_workers=args.max_workers,
            upsert=args.upsert
        )
    except KeyboardInterrupt:
        print('\n\n⚠️  Interrupted by user')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
