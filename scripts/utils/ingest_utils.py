import os
import csv
import json
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime
from threading import Lock
import boto3

# DATA_DIR should point to scripts/data/data (parent's data directory)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

COMPANY_HINT_COLUMNS = {"company", "company_linkedin_url", "employees", "company_name_for_emails"}
CONTACT_HINT_COLUMNS = {"first_name", "last_name", "email", "person_linkedin_url"}

def list_csv_files() -> List[str]:
    if not os.path.isdir(DATA_DIR):
        return []
    return [
        os.path.join(DATA_DIR, name)
        for name in os.listdir(DATA_DIR)
        if name.lower().endswith(".csv")
    ]

def sniff_headers(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader, [])
            return [h.strip() for h in headers]
    except Exception:
        return []

def classify_csv(path: str) -> set:
    """Classify a CSV file based on its headers. Returns a set of types: {'company'}, {'contact'}, {'company', 'contact'}, or {'unknown'}"""
    headers = set(map(str.lower, sniff_headers(path)))
    if not headers:
        return {"unknown"}
    
    types = set()
    if COMPANY_HINT_COLUMNS & headers:
        types.add("company")
    if CONTACT_HINT_COLUMNS & headers:
        types.add("contact")
    
    return types if types else {"unknown"}

def split_companies_contacts(paths: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """Split CSV files into companies, contacts, and unknowns. Files can appear in multiple lists if they contain both types."""
    companies, contacts, unknowns = [], [], []
    for p in paths:
        types = classify_csv(p)
        if "company" in types:
            companies.append(p)
        if "contact" in types:
            contacts.append(p)
        if "unknown" in types:
            unknowns.append(p)
    return companies, contacts, unknowns

def list_s3_csv_objects(s3_client, bucket: str, prefix: str = "") -> List[str]:
    keys: List[str] = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        contents = page.get("Contents", [])
        for obj in contents:
            key = obj.get("Key", "")
            if key.lower().endswith(".csv"):
                keys.append(key)
    return keys

# Error logging
# All error CSVs should live under scripts/data/error with a per-run timestamped filename
_error_lock = Lock()
_error_csv_path: Optional[str] = None
_error_count: int = 0


def _get_error_dir() -> str:
    """
    Return the absolute path to the shared error directory, creating it if needed.

    The directory is `scripts/data/error` relative to this file.
    """
    base_dir = os.path.dirname(__file__)
    error_dir = os.path.join(base_dir, "..", "error")
    os.makedirs(error_dir, exist_ok=True)
    return error_dir


def _get_error_csv_path() -> str:
    """
    Lazily compute and cache the per-run error CSV path.

    The filename format is: error_dd_mm_yy_hh_mm_ss.csv
    """
    global _error_csv_path
    if _error_csv_path is None:
        now = datetime.now()
        filename = now.strftime("error_%d_%m_%y_%H_%M_%S.csv")
        _error_csv_path = os.path.join(_get_error_dir(), filename)
    return _error_csv_path


def log_error(row_data: Dict[str, Any], error_reason: str, error_type: str = "unknown") -> None:
    """
    Log an error row to a timestamped CSV file with thread-safe file writing.

    The CSV has the following columns:
    - timestamp: ISO formatted timestamp of when the error was logged
    - error_type: High-level category for the error (e.g., company, contact_db)
    - row_data: JSON-encoded representation of the problematic row/context
    - error_reason: Human-readable error message
    """
    timestamp = datetime.now().isoformat()
    # Ensure row_data is JSON-serializable; fall back to repr on failure
    try:
        row_json = json.dumps(row_data, ensure_ascii=False)
    except Exception:
        row_json = json.dumps({"unserializable": repr(row_data)}, ensure_ascii=False)

    csv_path = _get_error_csv_path()

    with _error_lock:
        file_exists = os.path.exists(csv_path)
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                # Write header if file is new
                writer.writerow(["timestamp", "error_type", "row_data", "error_reason"])
            writer.writerow([timestamp, error_type, row_json, error_reason])
        global _error_count
        _error_count += 1


def get_error_log_info() -> Tuple[Optional[str], int]:
    """
    Return information about the current error log for this process.

    Returns:
        (error_csv_path, error_count)
        - error_csv_path: absolute path to the timestamped error CSV file,
          or None if no errors have been logged yet.
        - error_count: total number of rows written via log_error() in
          this process so far.
    """
    return (_error_csv_path, _error_count)

