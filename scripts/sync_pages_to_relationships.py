#!/usr/bin/env python3
"""
Sync page uses_endpoints to relationship by-page files.
Reads media/pages/*.json and writes media/relationship/by-page/*.json.
Optionally fills endpoint_reference and postman_reference from media/endpoints and media/postman.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

PAGES_DIR = Path(__file__).resolve().parent.parent / "media" / "pages"
REL_BY_PAGE_DIR = Path(__file__).resolve().parent.parent / "media" / "relationship" / "by-page"
ENDPOINTS_INDEX = Path(__file__).resolve().parent.parent / "media" / "endpoints" / "index.json"
POSTMAN_CONFIG = Path(__file__).resolve().parent.parent / "media" / "postman" / "contact360.json"
CONFIG_ID = "contact360"

# Route to by-page filename: /companies/[id] -> companies_[id], /dashboard -> dashboard
def load_endpoint_index() -> dict[tuple[str, str], str]:
    """(endpoint_path, method) -> endpoint_id."""
    if not ENDPOINTS_INDEX.is_file():
        return {}
    data = json.loads(ENDPOINTS_INDEX.read_text(encoding="utf-8"))
    return {(ep.get("path", ""), ep.get("method", "QUERY")): ep.get("endpoint_id", "") for ep in data.get("endpoints", []) if ep.get("path") and ep.get("endpoint_id")}


def load_postman_mappings() -> dict[str, dict]:
    """endpoint_id -> { mapping_id, config_id }."""
    if not POSTMAN_CONFIG.is_file():
        return {}
    data = json.loads(POSTMAN_CONFIG.read_text(encoding="utf-8"))
    return {m.get("endpoint_id", ""): {"mapping_id": m.get("mapping_id", ""), "config_id": CONFIG_ID} for m in data.get("endpoint_mappings", []) if m.get("endpoint_id") and m.get("mapping_id")}


def route_to_filename(route: str) -> str:
    if not route or route == "/":
        return "root"
    # /companies/[id] -> companies_[id], /admin/marketing -> admin_marketing
    parts = route.strip("/").split("/")
    return "_".join(parts)

def page_to_relationship_endpoint(
    page_path: str, ep: dict, path_to_eid: dict[tuple[str, str], str], eid_to_postman: dict[str, dict]
) -> dict:
    """Convert page uses_endpoints item to EnhancedRelationship format."""
    op = ep.get("endpoint_path", "").replace("graphql/", "")
    method = ep.get("method", "QUERY")
    rel_id = f"{page_path.strip('/').replace('/', '_')}_graphql_{op}_{method}"
    if rel_id.startswith("_"):
        rel_id = rel_id[1:]
    endpoint_path = ep.get("endpoint_path", "")
    endpoint_id = path_to_eid.get((endpoint_path, method))
    endpoint_reference = None
    if endpoint_id:
        endpoint_reference = {
            "endpoint_id": endpoint_id,
            "endpoint_path": endpoint_path,
            "method": method,
            "api_version": ep.get("api_version", "graphql"),
        }
    postman_reference = eid_to_postman.get(endpoint_id) if endpoint_id else None
    return {
        "_id": rel_id,
        "relationship_id": rel_id,
        "state": "development",
        "access_control": None,
        "page_reference": None,
        "endpoint_reference": endpoint_reference,
        "connection": None,
        "files": None,
        "data_flow": None,
        "postman_reference": postman_reference,
        "dependencies": None,
        "performance": None,
        "metadata": None,
        "page_path": page_path,
        "endpoint_path": endpoint_path,
        "method": method,
        "api_version": ep.get("api_version", "graphql"),
        "via_service": ep.get("via_service", ""),
        "via_hook": ep.get("via_hook"),
        "usage_type": ep.get("usage_type", "primary"),
        "usage_context": ep.get("usage_context", "data_fetching"),
        "created_at": "2026-02-03T00:00:00.000000+00:00",
        "updated_at": "2026-02-03T00:00:00.000000+00:00",
    }

def sync_page(
    page_path: str,
    page_data: dict,
    path_to_eid: dict[tuple[str, str], str],
    eid_to_postman: dict[str, dict],
) -> bool:
    """Sync one page to by-page relationship file. Writes even when uses_endpoints is empty."""
    meta = page_data.get("metadata", {})
    route = meta.get("route", page_path)
    if not route:
        return False
    uses = meta.get("uses_endpoints", [])
    fn = route_to_filename(route)
    out_path = REL_BY_PAGE_DIR / f"{fn}.json"
    endpoints = [
        page_to_relationship_endpoint(route, ep, path_to_eid, eid_to_postman) for ep in uses
    ]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "+00:00"
    obj = {
        "page_path": route,
        "endpoints": endpoints,
        "created_at": now,
        "updated_at": now,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path.name} ({len(endpoints)} endpoints)")
    return True

def main():
    path_to_eid = load_endpoint_index()
    eid_to_postman = load_postman_mappings()
    for p in sorted(PAGES_DIR.glob("*.json")):
        if p.name in ("index.json", "pages_index.json",):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            meta = data.get("metadata", {})
            if meta.get("status") == "archived":
                print(f"Skip archived {p.name}")
                continue
            route = meta.get("route")
            if route is not None:
                sync_page(route, data, path_to_eid, eid_to_postman)
        except Exception as e:
            print(f"Skip {p.name}: {e}")

if __name__ == "__main__":
    main()
