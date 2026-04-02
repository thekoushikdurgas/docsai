"""Ingest API test failures into Pinecone (vector-backed memory)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .client import get_api_index


# Default reports location (matches existing CLI in `docs/scripts/cli/commands/*`):
# `docs/scripts/test_reports`
REPORTS_DIR_DEFAULT = Path(__file__).resolve().parents[1] / "test_reports"
REPORT_TS_RE = re.compile(r"^test_results_(\d{8}_\d{6})$")


def _parse_report_timestamp(stem: str) -> Optional[datetime]:
    m = REPORT_TS_RE.match(stem)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def _batch(records: List[Dict[str, Any]], batch_size: int) -> Iterable[List[Dict[str, Any]]]:
    for i in range(0, len(records), batch_size):
        yield records[i : i + batch_size]


def _get_result_field(result: Dict[str, Any], key: str, default: Any = "") -> Any:
    val = result.get(key, default)
    return default if val is None else val


def _failure_to_record(*, result: Dict[str, Any], endpoint_key: str, profile: str) -> Dict[str, Any]:
    method = str(_get_result_field(result, "method", "")).strip()
    endpoint = str(_get_result_field(result, "endpoint", "")).strip()
    category = str(_get_result_field(result, "category", "Unknown")).strip()
    api_version = str(_get_result_field(result, "api_version", "v1")).strip()
    status_code = _get_result_field(result, "status_code", "")
    success = bool(result.get("success", False))
    error_message = str(_get_result_field(result, "error_message", "")).strip()
    test_timestamp = str(_get_result_field(result, "test_timestamp", "")).strip()

    # Text content (integrated embeddings uses the `content` field)
    status_str = str(status_code) if status_code is not None else ""
    error_part = error_message if error_message else "(no error_message)"
    content = (
        f"{method} {endpoint} - {status_str}. "
        f"Category: {category}. API {api_version}. "
        f"Error: {error_part}"
    ).strip()

    record_seed = f"{endpoint_key}::{test_timestamp}"
    record_id = hashlib.sha256(record_seed.encode("utf-8")).hexdigest()

    return {
        "_id": record_id,
        "content": content,
        "text": content,
        # Flat metadata only
        "endpoint_key": endpoint_key,
        "method": method,
        "api_version": api_version,
        "category": category,
        "status_code": str(status_code) if status_code is not None else "",
        "success": success,
        "profile": profile,
    }


def ingest_api(
    *,
    profile: str,
    days: Optional[int] = None,
    reports_dir: Optional[Path] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Ingest failure records from `test_reports/*.json` into:
    - namespace: `profile_<profile>`
    """

    idx = get_api_index()

    reports_root = reports_dir or REPORTS_DIR_DEFAULT
    namespace = f"profile_{profile}"

    if not reports_root.exists():
        raise RuntimeError(f"Reports directory not found: {reports_root}")

    now = datetime.now()
    cutoff = (now - timedelta(days=days)) if days is not None else None

    report_files: List[Path] = sorted(reports_root.glob("test_results_*.json"))
    latest_path = reports_root / "test_results_latest.json"
    if latest_path.exists() and latest_path not in report_files:
        report_files.append(latest_path)

    summary: Dict[str, Any] = {
        "namespace": namespace,
        "profile": profile,
        "days": days,
        "dry_run": dry_run,
        "files_processed": 0,
        "failures_upserted": 0,
        "upsert_batches": 0,
        "errors": [],
    }

    all_records: List[Dict[str, Any]] = []
    for report_file in report_files:
        ts = _parse_report_timestamp(report_file.stem.replace(".json", ""))
        if cutoff is not None:
            if ts is None:
                # Can't determine age (e.g. latest); skip if the user asked for a window.
                continue
            if ts < cutoff:
                continue

        try:
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except Exception as e:
            summary["errors"].append({"file": report_file.name, "error": str(e)})
            continue

        detailed_results = report_data.get("detailed_results", [])
        if not isinstance(detailed_results, list):
            continue

        summary["files_processed"] += 1

        for i, result in enumerate(detailed_results):
            if not isinstance(result, dict):
                continue

            success = bool(result.get("success", False))
            if success:
                continue

            method = str(result.get("method") or "").strip()
            endpoint = str(result.get("endpoint") or "").strip()
            if not method or not endpoint:
                # If the report uses the older schema, try to infer.
                endpoint_obj = result.get("endpoint") or {}
                if isinstance(endpoint_obj, dict):
                    method = str(endpoint_obj.get("method") or method).strip()
                    endpoint = str(endpoint_obj.get("full_path") or endpoint).strip()

            endpoint_key = f"{method} {endpoint}".strip()
            if not endpoint_key:
                continue

            try:
                rec = _failure_to_record(result=result, endpoint_key=endpoint_key, profile=profile)
                all_records.append(rec)
            except Exception:
                # Skip malformed entries.
                continue

    # Upsert in batches of <=96 records.
    for batch in _batch(all_records, 96):
        summary["upsert_batches"] += 1
        summary["failures_upserted"] += len(batch)
        if not dry_run and batch:
            idx.upsert_records(namespace, batch)

    # Mandatory indexing delay: wait after writes before any immediate reads/searches.
    if not dry_run:
        time.sleep(10)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest API test failures into Pinecone.")
    parser.add_argument("--profile", required=True, help="CLI profile name (e.g. default, admin, etc).")
    parser.add_argument("--days", type=int, default=None, help="Only ingest reports from last N days.")
    parser.add_argument("--reports-dir", default=None, help="Override reports directory.")
    parser.add_argument("--dry-run", action="store_true", help="Chunk and compute records only.")
    args = parser.parse_args()

    reports_dir = Path(args.reports_dir) if args.reports_dir else None
    summary = ingest_api(
        profile=args.profile,
        days=args.days,
        reports_dir=reports_dir,
        dry_run=bool(args.dry_run),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

