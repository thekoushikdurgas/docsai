"""
Lightweight test for centralized error logging.

This test exercises the log_error helper directly and verifies that calling it
results in a timestamped CSV being created under the shared error directory
with at least the header row and one data row.

Usage (from repo root):
    python -m scripts.data.tests.test_error_logging
"""

import os
import csv
from typing import Optional

from ..utils import ingest_utils
from ..utils import log_error


def _find_error_file() -> Optional[str]:
    """
    Best-effort helper to locate the current error CSV based on ingest_utils.
    """
    path, count = ingest_utils.get_error_log_info()
    if path and os.path.isfile(path):
        return path
    return None


def run_error_logging_smoke_test() -> bool:
    """
    Run a simple smoke test for the centralized error logger.

    Returns:
        True if the test passes, False otherwise.
    """
    # Log a couple of synthetic errors
    log_error({"row": 1, "context": "test_error_logging"}, "first test error", "test")
    log_error({"row": 2, "context": "test_error_logging"}, "second test error", "test")

    error_path = _find_error_file()
    if error_path is None:
        print("✗ No error file found after logging errors.")
        return False

    print(f"Located error log: {error_path}")

    # Inspect the CSV to ensure it has at least a header and one row
    with open(error_path, "r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))

    if not reader:
        print("✗ Error CSV is empty.")
        return False

    header = reader[0]
    expected_header = ["timestamp", "error_type", "row_data", "error_reason"]
    if header != expected_header:
        print(f"✗ Unexpected header: {header} (expected {expected_header})")
        return False

    if len(reader) < 2:
        print("✗ Error CSV does not contain any data rows.")
        return False

    print("✓ Centralized error logging smoke test passed.")
    return True


if __name__ == "__main__":
    ok = run_error_logging_smoke_test()
    raise SystemExit(0 if ok else 1)


