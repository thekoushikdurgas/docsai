"""
Local email pattern data ingestion module.

This module handles ingesting email pattern data from local CSV files.
"""

from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import and_
from threading import Lock
from uuid import uuid4, uuid5, NAMESPACE_URL

from ..base import LocalFileIngester
from ...models import EmailPattern, SessionLocal
from ...utils import log_error
from ...utils.email_pattern_extractor import extract_pattern_from_email
from ...config import get_default

# Thread lock for safe concurrent operations
pattern_insert_lock = Lock()

# Defaults used if not overridden by caller
DEFAULT_BATCH_SIZE = get_default("batch_size", 1000)
DEFAULT_MAX_THREADS = get_default("max_threads", 3)


class LocalEmailPatternIngester(LocalFileIngester):
    """Ingester for email pattern data from local CSV files."""
    
    def insert_data(self, data_list: List[Dict]) -> None:
        """Insert email pattern data into the database."""
        if len(data_list) == 0:
            return
        
        server_time = datetime.now(timezone.utc)
        
        # Dictionary to group patterns by (company_uuid, pattern_format)
        # Key: (company_uuid, pattern_format), Value: {pattern_string, contact_count, is_auto_extracted}
        pattern_groups = defaultdict(lambda: {
            "pattern_string": None,
            "contact_count": 0,
            "is_auto_extracted": False,
        })
        
        # First pass: Extract patterns and group by company_uuid + pattern_format
        for data in data_list:
            try:
                # Try to get company_uuid directly, or generate it from company fields
                company_uuid = data.get('company_uuid', '').strip()
                
                # If company_uuid is missing, generate it from company fields (same logic as company.py)
                if not company_uuid:
                    # Get company identifying fields
                    raw_company_name = data.get('company', '').strip() or "_"
                    linkedin_url = data.get('company_linkedin_url', '').strip() or "_"
                    company_name_for_emails = data.get('company_name_for_emails', '').strip() or "_"
                    
                    # Generate deterministic company_uuid using same logic as company.py
                    # Use uuid5(NAMESPACE_URL, hash_str) for consistency across imports
                    hash_str = raw_company_name + linkedin_url + company_name_for_emails
                    company_uuid = str(uuid5(NAMESPACE_URL, hash_str))
                
                # Check if pattern_format is provided directly in CSV
                pattern_format = data.get('pattern_format', '').strip()
                pattern_string = data.get('pattern_string', '').strip() or None
                is_auto_extracted = False
                
                # If pattern_format is not provided, try to extract it from contact data
                if not pattern_format:
                    # Extract pattern from email, first_name, last_name
                    first_name = data.get('first_name', '').strip()
                    last_name = data.get('last_name', '').strip()
                    email = data.get('email', '').strip()
                    
                    if email and first_name and last_name:
                        # Try to extract pattern
                        pattern_result = extract_pattern_from_email(email, first_name, last_name)
                        if pattern_result:
                            pattern_format, extracted_pattern_string = pattern_result
                            # Use extracted pattern_string if not provided
                            if not pattern_string:
                                pattern_string = extracted_pattern_string
                            is_auto_extracted = True
                        else:
                            # Pattern could not be extracted, skip this row
                            continue
                    else:
                        # Missing required fields for pattern extraction, skip this row
                        continue
                else:
                    # Pattern format provided in CSV, check if is_auto_extracted is specified
                    is_auto_str = str(data.get('is_auto_extracted', '')).strip().lower()
                    if is_auto_str in ('true', '1', 'yes', 'y'):
                        is_auto_extracted = True
                
                # Group patterns by (company_uuid, pattern_format) and count contacts
                pattern_key = (company_uuid, pattern_format)
                
                # Increment contact count for this pattern
                pattern_groups[pattern_key]["contact_count"] += 1
                
                # Store pattern_string from first occurrence (or provided value)
                if pattern_string and not pattern_groups[pattern_key]["pattern_string"]:
                    pattern_groups[pattern_key]["pattern_string"] = pattern_string
                
                # Set is_auto_extracted if any row has it as True
                if is_auto_extracted:
                    pattern_groups[pattern_key]["is_auto_extracted"] = True
                    
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing pattern row: {error_msg}")
                log_error(data, error_msg, "email_pattern")
                continue  # Continue processing other rows
        
        # Second pass: Create email pattern records from grouped patterns
        pattern_lst = []
        for (company_uuid, pattern_format), pattern_data in pattern_groups.items():
            try:
                # Generate deterministic pattern UUID
                pattern_hash = company_uuid + pattern_format
                pattern_uuid = str(uuid5(NAMESPACE_URL, pattern_hash))
                
                pattern = {
                    "uuid": pattern_uuid,
                    "company_uuid": company_uuid,
                    "pattern_format": pattern_format,
                    "pattern_string": pattern_data["pattern_string"],
                    "contact_count": pattern_data["contact_count"],
                    "is_auto_extracted": pattern_data["is_auto_extracted"],
                    "created_at": server_time,
                    "updated_at": server_time,
                }
                pattern_lst.append(pattern)
            except Exception as e:
                error_msg = str(e)
                print(f"Error creating pattern record: {error_msg}")
                log_error({"company_uuid": company_uuid, "pattern_format": pattern_format}, error_msg, "email_pattern")
                continue
        
        with SessionLocal() as session:
            try:
                if pattern_lst:
                    # Process patterns in batch: update existing or insert new
                    for pattern_data in pattern_lst:
                        # Check if pattern exists by company_uuid and pattern_format
                        existing = session.query(EmailPattern).filter(
                            and_(
                                EmailPattern.company_uuid == pattern_data['company_uuid'],
                                EmailPattern.pattern_format == pattern_data['pattern_format']
                            )
                        ).first()
                        
                        if existing:
                            # Add batch contact_count to existing count, preserve other fields
                            # Handle NULL contact_count (treat as 0)
                            existing_contact_count = existing.contact_count if existing.contact_count is not None else 0
                            batch_contact_count = pattern_data.get('contact_count', 0) or 0
                            # Add batch count to existing count (not just +1, since we've already counted in batch)
                            existing.contact_count = max(0, existing_contact_count) + batch_contact_count
                            # pattern_string and is_auto_extracted are preserved (not updated)
                            existing.updated_at = datetime.now(timezone.utc)
                        else:
                            # Insert new pattern
                            new_pattern = EmailPattern(**pattern_data)
                            session.add(new_pattern)
                    
                    with pattern_insert_lock:
                        session.commit()
            except Exception as e:
                session.rollback()
                error_msg = f"Database insert error: {str(e)}"
                print(error_msg)
                # Log all rows that failed to insert
                for data in data_list:
                    log_error(data, error_msg, "email_pattern_db")


def ingest_email_patterns_from_local(
    path: str,
    batch_size: int = DEFAULT_BATCH_SIZE,
    max_threads: int = DEFAULT_MAX_THREADS
) -> None:
    """
    Ingest email pattern data from a local CSV file.
    
    Args:
        path: Path to the CSV file
        batch_size: Number of rows to process per batch
        max_threads: Maximum number of concurrent threads
    """
    ingester = LocalEmailPatternIngester(path, batch_size=batch_size, max_threads=max_threads)
    with ingester:
        ingester.ingest()


if __name__ == "__main__":
    # Example single-file run (kept for manual testing)
    ingest_email_patterns_from_local('data/email_patterns.csv')

