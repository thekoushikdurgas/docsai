#!/usr/bin/env python3
"""
Normalize all media/endpoints/*.json files to conform to endpoints_json_models.md.
- Ensures required and optional keys exist.
- Sets page_count = len(used_by_pages).
- Ensures used_by_pages items have required fields (page_path, page_title, via_service, usage_type, usage_context).
- Skips index.json and endpoints_index.json.
"""
import json
from pathlib import Path

ENDPOINTS_DIR = Path(__file__).resolve().parent.parent / "media" / "endpoints"
SKIP = {"index.json", "endpoints_index.json"}

REQUIRED_TOP = {"_id", "endpoint_id", "endpoint_path", "method", "api_version", "description", "created_at", "updated_at"}
OPTIONAL_DEFAULTS = {
    "endpoint_state": "development",
    "service_file": None,
    "router_file": None,
    "service_methods": [],
    "repository_methods": [],
    "used_by_pages": [],
    "rate_limit": None,
    "graphql_operation": None,
    "sql_file": None,
    "page_count": 0,
    "access_control": None,
    "lambda_services": None,
    "files": None,
    "methods": None,
}
PAGE_USAGE_REQUIRED = {"page_path", "page_title", "via_service", "usage_type", "usage_context"}
VALID_METHODS = {"QUERY", "MUTATION", "GET", "POST", "PUT", "DELETE", "PATCH"}
VALID_USAGE_TYPES = {"primary", "secondary", "conditional", "lazy", "prefetch"}
VALID_USAGE_CONTEXTS = {"data_fetching", "data_mutation", "authentication", "analytics", "realtime", "background"}


def normalize_page_usage(entry: dict) -> dict:
    out = {
        "page_path": entry.get("page_path", ""),
        "page_title": entry.get("page_title", ""),
        "via_service": entry.get("via_service", ""),
        "via_hook": entry.get("via_hook"),
        "usage_type": entry.get("usage_type", "primary"),
        "usage_context": entry.get("usage_context", "data_fetching"),
        "updated_at": entry.get("updated_at"),
    }
    if out["usage_type"] not in VALID_USAGE_TYPES:
        out["usage_type"] = "primary"
    if out["usage_context"] not in VALID_USAGE_CONTEXTS:
        out["usage_context"] = "data_fetching"
    return out


def normalize_endpoint(data: dict) -> dict:
    # Ensure at least one of service_file, router_file (spec requirement)
    if not data.get("service_file") and not data.get("router_file"):
        data["service_file"] = "appointment360/app/graphql/modules/..."

    # Normalize used_by_pages
    used = data.get("used_by_pages")
    if not isinstance(used, list):
        used = []
    data["used_by_pages"] = [normalize_page_usage(e) for e in used]

    # page_count must equal len(used_by_pages)
    data["page_count"] = len(data["used_by_pages"])

    # Add any missing optional keys
    for key, default in OPTIONAL_DEFAULTS.items():
        if key not in data:
            data[key] = default
        if key == "page_count":
            data["page_count"] = len(data["used_by_pages"])

    # Ensure required keys exist
    for key in REQUIRED_TOP:
        if key not in data:
            if key == "_id":
                data["_id"] = data.get("endpoint_id", "unknown") + "-001"
            elif key in ("created_at", "updated_at"):
                data[key] = "2026-01-20T00:00:00.000000+00:00"
            else:
                data[key] = data.get(key, "")

    # Validate method
    if data.get("method") not in VALID_METHODS:
        data["method"] = "QUERY" if "query" in data.get("endpoint_id", "").lower() else "MUTATION"

    # Order keys for consistent output (required first, then optional)
    order = [
        "_id", "endpoint_id", "endpoint_path", "method", "api_version", "description",
        "created_at", "updated_at", "endpoint_state", "service_file", "router_file",
        "service_methods", "repository_methods", "used_by_pages", "rate_limit",
        "graphql_operation", "sql_file", "page_count", "access_control", "lambda_services",
        "files", "methods"
    ]
    return {k: data[k] for k in order if k in data}


def main():
    endpoints_dir = ENDPOINTS_DIR
    if not endpoints_dir.exists():
        print(f"Endpoints dir not found: {endpoints_dir}")
        return
    fixed = 0
    for path in sorted(endpoints_dir.glob("*.json")):
        if path.name in SKIP:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
            data = json.loads(raw)
            normalized = normalize_endpoint(data)
            new_raw = json.dumps(normalized, indent=2, ensure_ascii=False)
            if new_raw != raw:
                path.write_text(new_raw, encoding="utf-8")
                fixed += 1
                print(f"Normalized: {path.name}")
        except Exception as e:
            print(f"Skip {path.name}: {e}")
    print(f"Done. Fixed {fixed} files.")
    # Regenerate index.json from all endpoint files
    rebuild_index()


def rebuild_index():
    """Rebuild media/endpoints/index.json from all endpoint JSON files."""
    endpoints = []
    by_method = {}
    by_api_version = {}
    by_path = {}
    stats = {"total": 0, "by_method": {}, "by_api_version": {}}
    for path in sorted(ENDPOINTS_DIR.glob("*.json")):
        if path.name in SKIP:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            eid = data.get("endpoint_id") or path.stem
            method = data.get("method", "QUERY")
            api_version = data.get("api_version", "graphql")
            path_val = data.get("endpoint_path") or data.get("path", "")
            endpoints.append({
                "endpoint_id": eid,
                "method": method,
                "api_version": api_version,
                "path": path_val,
                "file_name": path.name,
            })
            by_method.setdefault(method, []).append(eid)
            by_api_version.setdefault(api_version, []).append(eid)
            if path_val:
                by_path[path_val] = eid
            stats["total"] += 1
            stats["by_method"][method] = stats["by_method"].get(method, 0) + 1
            stats["by_api_version"][api_version] = stats["by_api_version"].get(api_version, 0) + 1
        except Exception as e:
            print(f"Skip index {path.name}: {e}")
    from datetime import datetime, timezone
    index = {
        "version": "2.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": len(endpoints),
        "endpoints": endpoints,
        "indexes": {"by_method": by_method, "by_api_version": by_api_version, "by_path": by_path},
        "statistics": stats,
    }
    index_path = ENDPOINTS_DIR / "index.json"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Rebuilt {index_path.name}: {len(endpoints)} endpoints.")
    # Rebuild endpoints_index.json (full catalog)
    full_list = []
    for path in sorted(ENDPOINTS_DIR.glob("*.json")):
        if path.name in SKIP:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            full_list.append(normalize_endpoint(data))
        except Exception as e:
            print(f"Skip full index {path.name}: {e}")
    from datetime import datetime, timezone
    full_index = {
        "version": "2.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": len(full_list),
        "endpoints": full_list,
    }
    full_path = ENDPOINTS_DIR / "endpoints_index.json"
    full_path.write_text(json.dumps(full_index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Rebuilt {full_path.name}: {len(full_list)} endpoints.")


if __name__ == "__main__":
    main()
