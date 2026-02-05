#!/usr/bin/env python3
"""
Analyze and validate all documentation JSON files.

This script scans all JSON files in docs/pages/, docs/endpoints/, and docs/relationship/
and validates them against their respective schemas.

Refactored to use shared validators and context-aware utilities.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path for Lambda API imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# When run as subprocess with DJANGO_SETTINGS_MODULE (e.g. from docs/operations/analyze), init Django first
if os.environ.get("DJANGO_SETTINGS_MODULE"):
    import django
    django.setup()

# Use context-aware utilities and shared validators
from scripts.utils.context import (
    get_pages_dir,
    get_endpoints_dir,
    get_relationships_dir,
    get_postman_dir,
    get_n8n_dir,
    get_result_dir,
    get_logger,
    get_media_root,
)
from scripts.utils.validators import (
    load_json_file,
    validate_with_schema,
    validate_relationship_by_page,
    validate_relationship_by_endpoint,
    ValidationError,
    get_validator,
)
from scripts.utils.upload_helpers import get_exclude_files

logger = get_logger(__name__)

# Get directories using context-aware utilities
PAGES_DIR = get_pages_dir()
ENDPOINTS_DIR = get_endpoints_dir()
RELATIONSHIPS_DIR = get_relationships_dir()
RELATIONSHIPS_BY_PAGE_DIR = RELATIONSHIPS_DIR / "by-page"
POSTMAN_DIR = get_postman_dir()
N8N_DIR = get_n8n_dir()
RESULT_DIR = get_result_dir()
MEDIA_ROOT = get_media_root()

# Files to exclude from analysis
EXCLUDE_FILES = get_exclude_files()


def _count_pages() -> int:
    """Return number of page JSON files to analyze."""
    if not PAGES_DIR.exists():
        return 0
    files = [
        f for f in PAGES_DIR.glob("*.json")
        if f.name not in EXCLUDE_FILES and not f.name.endswith("_index.json")
    ]
    return len(files)


def _count_endpoints() -> int:
    """Return number of endpoint JSON files to analyze."""
    if not ENDPOINTS_DIR.exists():
        return 0
    files = [
        f for f in ENDPOINTS_DIR.glob("*.json")
        if f.name not in EXCLUDE_FILES and not f.name.endswith("_index.json")
    ]
    return len(files)


def _count_relationships() -> int:
    """Return number of relationship JSON files (by-page + by-endpoint)."""
    if not RELATIONSHIPS_DIR.exists():
        return 0
    by_page = list(RELATIONSHIPS_BY_PAGE_DIR.glob("*.json")) if RELATIONSHIPS_BY_PAGE_DIR.exists() else []
    by_endpoint = [
        f for f in RELATIONSHIPS_DIR.glob("*.json")
        if f.name.startswith("by-endpoint_") and f.name not in EXCLUDE_FILES
    ]
    return len(by_page) + len(by_endpoint)


def _count_json_directory(dir_path: Path, exclude_names: set) -> int:
    """Return number of JSON files under dir_path."""
    if not dir_path.exists():
        return 0
    try:
        return len([f for f in dir_path.rglob("*.json") if f.is_file() and f.name not in exclude_names])
    except Exception:
        return 0


def _write_progress(
    progress_path: str,
    total_files: int,
    current_index: int,
    section: str,
    section_current: int,
    section_total: int,
    current_file: str,
    done: bool = False,
    error: str = None,
) -> None:
    """Write progress JSON to progress_path for UI polling."""
    try:
        payload = {
            "total_files": total_files,
            "current_index": current_index,
            "section": section,
            "section_current": section_current,
            "section_total": section_total,
            "current_file": current_file,
            "done": done,
        }
        if error:
            payload["error"] = error
        Path(progress_path).write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as e:
        logger.warning("Could not write progress file: %s", e)


def analyze_pages(progress_callback=None) -> Dict[str, Any]:
    """Analyze all page JSON files."""
    print("\n" + "=" * 60)
    print("Analyzing Pages")
    print("=" * 60)
    
    if not PAGES_DIR.exists():
        print(f"❌ Pages directory not found: {PAGES_DIR}")
        return {"valid": 0, "invalid": 0, "errors": [], "files": []}
    
    validator = get_validator("pages")
    results = {
        "valid": 0,
        "invalid": 0,
        "errors": [],
        "files": [],
        "duplicate_ids": [],
    }
    
    page_ids = set()
    json_files = [
        f for f in PAGES_DIR.glob("*.json")
        if f.name not in EXCLUDE_FILES and not f.name.endswith("_index.json")
    ]
    
    print(f"\n📁 Found {len(json_files)} page files to analyze\n")
    section_total = len(json_files)

    for idx, file_path in enumerate(sorted(json_files)):
        file_name = file_path.name
        if progress_callback:
            progress_callback("Pages", idx + 1, section_total, file_name)
        data, parse_error = load_json_file(file_path)
        
        if parse_error:
            results["invalid"] += 1
            results["errors"].append({
                "file": file_name,
                "type": "parse_error",
                "error": parse_error,
            })
            print(f"❌ {file_name}: {parse_error}")
            continue
        
        # Validate schema with robust error handling
        is_valid = True
        validation_errors = []
        try:
            if validator and hasattr(validator, 'validate'):
                validation_result = validator.validate(data)
                if isinstance(validation_result, tuple) and len(validation_result) == 2:
                    is_valid, validation_errors = validation_result
                    # Ensure validation_errors is always a list
                    if validation_errors is None:
                        validation_errors = []
                    elif not isinstance(validation_errors, list):
                        validation_errors = list(validation_errors) if validation_errors else []
                else:
                    # Unexpected return format
                    is_valid = True
                    validation_errors = []
            else:
                # Validator not available, skip validation
                is_valid = True
                validation_errors = []
        except Exception as e:
            # If validation fails with exception, log and treat as invalid
            logger.error(f"Validation error for {file_name}: {e}", exc_info=True)
            is_valid = False
            validation_errors = [ValidationError("validation", f"Validation error: {str(e)}")]
        
        # Check for duplicate page_id
        page_id = data.get("page_id") if data else None
        if page_id:
            if page_id in page_ids:
                results["duplicate_ids"].append({
                    "file": file_name,
                    "page_id": page_id,
                })
            else:
                page_ids.add(page_id)
        
        file_result = {
            "file": file_name,
            "valid": is_valid,
            "page_id": page_id,
            "errors": [e.to_dict() for e in (validation_errors or [])],
        }
        results["files"].append(file_result)
        
        if is_valid:
            results["valid"] += 1
            print(f"✅ {file_name}")
        else:
            results["invalid"] += 1
            error_count = len(validation_errors or [])
            print(f"❌ {file_name}: {error_count} validation error(s)")
            if validation_errors:
                for error in validation_errors[:3]:  # Show first 3 errors
                    print(f"   - {error.field}: {error.message}")
                if error_count > 3:
                    print(f"   ... and {error_count - 3} more error(s)")
    
    return results


def analyze_endpoints(progress_callback=None) -> Dict[str, Any]:
    """Analyze all endpoint JSON files."""
    print("\n" + "=" * 60)
    print("Analyzing Endpoints")
    print("=" * 60)
    
    if not ENDPOINTS_DIR.exists():
        print(f"❌ Endpoints directory not found: {ENDPOINTS_DIR}")
        return {"valid": 0, "invalid": 0, "errors": [], "files": []}
    
    validator = get_validator("endpoints")
    results = {
        "valid": 0,
        "invalid": 0,
        "errors": [],
        "files": [],
        "duplicate_ids": [],
    }
    
    endpoint_ids = set()
    json_files = [
        f for f in ENDPOINTS_DIR.glob("*.json")
        if f.name not in EXCLUDE_FILES and not f.name.endswith("_index.json")
    ]
    
    print(f"\n📁 Found {len(json_files)} endpoint files to analyze\n")
    section_total = len(json_files)

    for idx, file_path in enumerate(sorted(json_files)):
        file_name = file_path.name
        if progress_callback:
            progress_callback("Endpoints", idx + 1, section_total, file_name)
        data, parse_error = load_json_file(file_path)
        
        if parse_error:
            results["invalid"] += 1
            results["errors"].append({
                "file": file_name,
                "type": "parse_error",
                "error": parse_error,
            })
            print(f"❌ {file_name}: {parse_error}")
            continue
        
        # Validate schema using shared validator
        is_valid, validation_errors = validate_with_schema(data, "endpoints", validator)
        
        # Check for duplicate endpoint_id
        endpoint_id = data.get("endpoint_id") if data else None
        if endpoint_id:
            if endpoint_id in endpoint_ids:
                results["duplicate_ids"].append({
                    "file": file_name,
                    "endpoint_id": endpoint_id,
                })
            else:
                endpoint_ids.add(endpoint_id)
        
        file_result = {
            "file": file_name,
            "valid": is_valid,
            "endpoint_id": endpoint_id,
            "errors": [e.to_dict() for e in (validation_errors or [])],
        }
        results["files"].append(file_result)
        
        if is_valid:
            results["valid"] += 1
            print(f"✅ {file_name}")
        else:
            results["invalid"] += 1
            error_count = len(validation_errors or [])
            print(f"❌ {file_name}: {error_count} validation error(s)")
            if validation_errors:
                for error in validation_errors[:3]:  # Show first 3 errors
                    print(f"   - {error.field}: {error.message}")
                if error_count > 3:
                    print(f"   ... and {error_count - 3} more error(s)")
    
    return results


def analyze_relationships(progress_callback=None) -> Dict[str, Any]:
    """Analyze all relationship JSON files."""
    print("\n" + "=" * 60)
    print("Analyzing Relationships")
    print("=" * 60)
    
    if not RELATIONSHIPS_DIR.exists():
        print(f"❌ Relationships directory not found: {RELATIONSHIPS_DIR}")
        return {"valid": 0, "invalid": 0, "errors": [], "files": []}
    
    results = {
        "valid": 0,
        "invalid": 0,
        "errors": [],
        "files": [],
        "by_page": {"valid": 0, "invalid": 0},
        "by_endpoint": {"valid": 0, "invalid": 0},
    }
    
    # Analyze by-page relationships
    by_page_files = list(RELATIONSHIPS_BY_PAGE_DIR.glob("*.json")) if RELATIONSHIPS_BY_PAGE_DIR.exists() else []
    by_endpoint_files = [
        f for f in RELATIONSHIPS_DIR.glob("*.json")
        if f.name.startswith("by-endpoint_") and f.name not in EXCLUDE_FILES
    ]
    section_total = len(by_page_files) + len(by_endpoint_files)
    if RELATIONSHIPS_BY_PAGE_DIR.exists():
        print(f"\n📁 Found {len(by_page_files)} by-page relationship files\n")
        
        for idx, file_path in enumerate(sorted(by_page_files)):
            file_name = f"by-page/{file_path.name}"
            if progress_callback:
                progress_callback("Relationships", idx + 1, section_total, file_name)
            data, parse_error = load_json_file(file_path)
            
            if parse_error:
                results["invalid"] += 1
                results["by_page"]["invalid"] += 1
                results["errors"].append({
                    "file": file_name,
                    "type": "parse_error",
                    "error": parse_error,
                })
                print(f"❌ {file_name}: {parse_error}")
                continue
            
            # Validate using shared validator
            is_valid, validation_errors = validate_relationship_by_page(data)
            
            file_result = {
                "file": file_name,
                "type": "by-page",
                "valid": is_valid,
                "errors": [e.to_dict() for e in (validation_errors or [])],
            }
            results["files"].append(file_result)
            
            if is_valid:
                results["valid"] += 1
                results["by_page"]["valid"] += 1
                print(f"✅ {file_name}")
            else:
                results["invalid"] += 1
                results["by_page"]["invalid"] += 1
                error_count = len(validation_errors or [])
                print(f"❌ {file_name}: {error_count} validation error(s)")
                if validation_errors:
                    for error in validation_errors[:3]:
                        print(f"   - {error.field}: {error.message}")
                if error_count > 3:
                    print(f"   ... and {error_count - 3} more error(s)")
    
    # Analyze by-endpoint relationships
    print(f"\n📁 Found {len(by_endpoint_files)} by-endpoint relationship files\n")
    
    for idx, file_path in enumerate(sorted(by_endpoint_files)):
        file_name = file_path.name
        if progress_callback:
            progress_callback("Relationships", len(by_page_files) + idx + 1, section_total, file_name)
        data, parse_error = load_json_file(file_path)
        
        if parse_error:
            results["invalid"] += 1
            results["by_endpoint"]["invalid"] += 1
            results["errors"].append({
                "file": file_name,
                "type": "parse_error",
                "error": parse_error,
            })
            print(f"❌ {file_name}: {parse_error}")
            continue
        
        # Validate using shared validator
        is_valid, validation_errors = validate_relationship_by_endpoint(data)
        
        file_result = {
            "file": file_name,
            "type": "by-endpoint",
            "valid": is_valid,
            "errors": [e.to_dict() for e in (validation_errors or [])],
        }
        results["files"].append(file_result)
        
        if is_valid:
            results["valid"] += 1
            results["by_endpoint"]["valid"] += 1
            print(f"✅ {file_name}")
        else:
            results["invalid"] += 1
            results["by_endpoint"]["invalid"] += 1
            error_count = len(validation_errors or [])
            print(f"❌ {file_name}: {error_count} validation error(s)")
            if validation_errors:
                for error in validation_errors[:3]:
                    print(f"   - {error.field}: {error.message}")
            if error_count > 3:
                print(f"   ... and {error_count - 3} more error(s)")
    
    return results


def _analyze_json_directory(
    dir_path: Path,
    relative_prefix: str,
    label: str,
    exclude_names: set = None,
    progress_callback=None,
) -> Dict[str, Any]:
    """Analyze all JSON files under a directory (parse-only). Returns { valid, invalid, errors[], files[] }."""
    exclude_names = exclude_names or set()
    results = {"valid": 0, "invalid": 0, "errors": [], "files": []}
    if not dir_path.exists():
        print(f"❌ {label} directory not found: {dir_path}")
        return results
    try:
        json_files = [f for f in dir_path.rglob("*.json") if f.is_file() and f.name not in exclude_names]
    except Exception as e:
        logger.warning("Listing %s failed: %s", dir_path, e)
        results["errors"].append({"file": str(dir_path), "type": "list_error", "error": str(e)})
        return results
    print(f"\n📁 Found {len(json_files)} JSON files under {label}\n")
    section_total = len(json_files)
    for idx, file_path in enumerate(sorted(json_files)):
        try:
            rel = file_path.relative_to(dir_path)
            file_name = f"{relative_prefix}/{rel}".replace("\\", "/")
        except ValueError:
            file_name = file_path.name
        if progress_callback:
            progress_callback(label, idx + 1, section_total, file_name)
        data, parse_error = load_json_file(file_path)
        if parse_error:
            results["invalid"] += 1
            results["errors"].append({"file": file_name, "type": "parse_error", "error": parse_error})
            print(f"❌ {file_name}: {parse_error}")
            continue
        results["valid"] += 1
        results["files"].append({"file": file_name, "valid": True, "errors": []})
        print(f"✅ {file_name}")
    return results


def analyze_n8n(progress_callback=None) -> Dict[str, Any]:
    """Analyze all JSON files under media/n8n (parse-only)."""
    print("\n" + "=" * 60)
    print("Analyzing N8N")
    print("=" * 60)
    return _analyze_json_directory(N8N_DIR, "n8n", "N8N", exclude_names=EXCLUDE_FILES, progress_callback=progress_callback)


def analyze_postman(progress_callback=None) -> Dict[str, Any]:
    """Analyze all JSON files under media/postman (parse-only)."""
    print("\n" + "=" * 60)
    print("Analyzing Postman")
    print("=" * 60)
    return _analyze_json_directory(
        POSTMAN_DIR, "postman", "Postman",
        exclude_names=EXCLUDE_FILES | {".DS_Store"},
        progress_callback=progress_callback,
    )


def analyze_result(progress_callback=None) -> Dict[str, Any]:
    """Analyze all JSON files under media/result (parse-only)."""
    print("\n" + "=" * 60)
    print("Analyzing Result")
    print("=" * 60)
    return _analyze_json_directory(RESULT_DIR, "result", "Result", exclude_names=EXCLUDE_FILES, progress_callback=progress_callback)


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze and validate documentation JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON report file path (default: print to console only)",
    )
    
    parser.add_argument(
        "--pages-only",
        action="store_true",
        help="Analyze only pages",
    )
    
    parser.add_argument(
        "--endpoints-only",
        action="store_true",
        help="Analyze only endpoints",
    )
    
    parser.add_argument(
        "--relationships-only",
        action="store_true",
        help="Analyze only relationships",
    )
    parser.add_argument("--n8n-only", action="store_true", help="Analyze only n8n JSON files")
    parser.add_argument("--postman-only", action="store_true", help="Analyze only postman JSON files")
    parser.add_argument("--result-only", action="store_true", help="Analyze only result JSON files")
    parser.add_argument("--progress-file", type=str, default=None, help="Write progress JSON to this path for UI polling")
    
    args = parser.parse_args()
    
    run_pages = not (args.endpoints_only or args.relationships_only or args.n8n_only or args.postman_only or args.result_only)
    run_endpoints = not (args.pages_only or args.relationships_only or args.n8n_only or args.postman_only or args.result_only)
    run_relationships = not (args.pages_only or args.endpoints_only or args.n8n_only or args.postman_only or args.result_only)
    run_n8n = args.n8n_only or not (args.pages_only or args.endpoints_only or args.relationships_only or args.postman_only or args.result_only)
    run_postman = args.postman_only or not (args.pages_only or args.endpoints_only or args.relationships_only or args.n8n_only or args.result_only)
    run_result = args.result_only or not (args.pages_only or args.endpoints_only or args.relationships_only or args.n8n_only or args.postman_only)
    
    # Compute total file count for progress (when --progress-file is set)
    progress_path = (args.progress_file or "").strip() or None
    total_files = 0
    if progress_path:
        if run_pages:
            total_files += _count_pages()
        if run_endpoints:
            total_files += _count_endpoints()
        if run_relationships:
            total_files += _count_relationships()
        if run_n8n:
            total_files += _count_json_directory(N8N_DIR, EXCLUDE_FILES)
        if run_postman:
            total_files += _count_json_directory(POSTMAN_DIR, EXCLUDE_FILES | {".DS_Store"})
        if run_result:
            total_files += _count_json_directory(RESULT_DIR, EXCLUDE_FILES)
    
    current_index = [0]  # use list so closure can mutate
    
    def progress_callback(section: str, section_current: int, section_total: int, current_file: str) -> None:
        current_index[0] += 1
        _write_progress(
            progress_path,
            total_files,
            current_index[0],
            section,
            section_current,
            section_total,
            current_file,
            done=False,
        )
    
    if progress_path:
        _write_progress(progress_path, total_files, 0, "Starting", 0, 0, "", done=False)
    
    print("=" * 60)
    print("Documentation Files Analysis")
    print("=" * 60)
    print(f"\n📂 Media root: {MEDIA_ROOT}")
    
    report = {
        "pages": {},
        "endpoints": {},
        "relationships": {},
        "n8n": {},
        "postman": {},
        "result": {},
        "summary": {},
    }
    
    try:
        if run_pages:
            report["pages"] = analyze_pages(progress_callback if progress_path else None)
        if run_endpoints:
            report["endpoints"] = analyze_endpoints(progress_callback if progress_path else None)
        if run_relationships:
            report["relationships"] = analyze_relationships(progress_callback if progress_path else None)
        if run_n8n:
            report["n8n"] = analyze_n8n(progress_callback if progress_path else None)
        if run_postman:
            report["postman"] = analyze_postman(progress_callback if progress_path else None)
        if run_result:
            report["result"] = analyze_result(progress_callback if progress_path else None)
    except Exception as e:
        if progress_path:
            _write_progress(progress_path, total_files, current_index[0], "", 0, 0, "", done=True, error=str(e))
        raise
    
    pages_summary = report.get("pages", {})
    endpoints_summary = report.get("endpoints", {})
    relationships_summary = report.get("relationships", {})
    n8n_summary = report.get("n8n", {})
    postman_summary = report.get("postman", {})
    result_summary = report.get("result", {})
    
    total_valid = (
        pages_summary.get("valid", 0) + endpoints_summary.get("valid", 0) + relationships_summary.get("valid", 0)
        + n8n_summary.get("valid", 0) + postman_summary.get("valid", 0) + result_summary.get("valid", 0)
    )
    total_invalid = (
        pages_summary.get("invalid", 0) + endpoints_summary.get("invalid", 0) + relationships_summary.get("invalid", 0)
        + n8n_summary.get("invalid", 0) + postman_summary.get("invalid", 0) + result_summary.get("invalid", 0)
    )
    
    report["summary"] = {
        "total_valid": total_valid,
        "total_invalid": total_invalid,
        "total_files": total_valid + total_invalid,
        "pages": {"valid": pages_summary.get("valid", 0), "invalid": pages_summary.get("invalid", 0)},
        "endpoints": {"valid": endpoints_summary.get("valid", 0), "invalid": endpoints_summary.get("invalid", 0)},
        "relationships": {"valid": relationships_summary.get("valid", 0), "invalid": relationships_summary.get("invalid", 0)},
        "n8n": {"valid": n8n_summary.get("valid", 0), "invalid": n8n_summary.get("invalid", 0)},
        "postman": {"valid": postman_summary.get("valid", 0), "invalid": postman_summary.get("invalid", 0)},
        "result": {"valid": result_summary.get("valid", 0), "invalid": result_summary.get("invalid", 0)},
    }
    
    print("\n" + "=" * 60)
    print("Analysis Summary")
    print("=" * 60)
    print(f"  ✅ Valid files:   {total_valid}")
    print(f"  ❌ Invalid files: {total_invalid}")
    print(f"  📄 Total files:    {total_valid + total_invalid}")
    if run_pages:
        print(f"  Pages:        {pages_summary.get('valid', 0)} valid, {pages_summary.get('invalid', 0)} invalid")
    if run_endpoints:
        print(f"  Endpoints:    {endpoints_summary.get('valid', 0)} valid, {endpoints_summary.get('invalid', 0)} invalid")
    if run_relationships:
        print(f"  Relationships: {relationships_summary.get('valid', 0)} valid, {relationships_summary.get('invalid', 0)} invalid")
    if run_n8n:
        print(f"  N8N:          {n8n_summary.get('valid', 0)} valid, {n8n_summary.get('invalid', 0)} invalid")
    if run_postman:
        print(f"  Postman:      {postman_summary.get('valid', 0)} valid, {postman_summary.get('invalid', 0)} invalid")
    if run_result:
        print(f"  Result:       {result_summary.get('valid', 0)} valid, {result_summary.get('invalid', 0)} invalid")
    
    # Check for duplicate IDs
    pages_duplicates = pages_summary.get("duplicate_ids", [])
    endpoints_duplicates = endpoints_summary.get("duplicate_ids", [])
    
    if pages_duplicates:
        print(f"\n  ⚠️  Found {len(pages_duplicates)} duplicate page_id(s)")
        for dup in pages_duplicates[:5]:
            print(f"     - {dup['page_id']} in {dup['file']}")
    
    if endpoints_duplicates:
        print(f"\n  ⚠️  Found {len(endpoints_duplicates)} duplicate endpoint_id(s)")
        for dup in endpoints_duplicates[:5]:
            print(f"     - {dup['endpoint_id']} in {dup['file']}")
    
    if progress_path:
        _write_progress(
            progress_path,
            total_files,
            current_index[0],
            "",
            0,
            0,
            "",
            done=True,
        )
    
    # Save report if output specified
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"\n📄 Report saved to: {output_path}")
    
    print("=" * 60 + "\n")
    
    # Exit with error code if invalid files found
    if total_invalid > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
