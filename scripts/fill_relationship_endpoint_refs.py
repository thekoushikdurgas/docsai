#!/usr/bin/env python3
"""
Fill endpoint_reference and postman_reference in media/relationship/by-page/*.json.
Uses media/endpoints/index.json for path+method -> endpoint_id and
media/postman/contact360.json for endpoint_id -> mapping_id, config_id.
Run from repo root or docsai: python scripts/fill_relationship_endpoint_refs.py [--write]
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DOCSAI_ROOT = SCRIPT_DIR.parent
REL_BY_PAGE_DIR = DOCSAI_ROOT / "media" / "relationship" / "by-page"
ENDPOINTS_INDEX = DOCSAI_ROOT / "media" / "endpoints" / "index.json"
POSTMAN_CONFIG = DOCSAI_ROOT / "media" / "postman" / "contact360.json"
CONFIG_ID = "contact360"


# Aliases: relationship endpoint_path (in by-page) -> canonical path in endpoints index
PATH_ALIASES = {
    "graphql/PerformanceMetrics": "graphql/GetPerformanceMetrics",
    "graphql/CompanyQuery": "graphql/QueryCompanies",
    "graphql/CompanyFilters": "graphql/GetCompanyFilters",
    "graphql/CompanyContacts": "graphql/GetCompanyContacts",
    "graphql/ContactQuery": "graphql/QueryContacts",
    "graphql/ContactCount": "graphql/CountContacts",
    "graphql/Exports": "graphql/ListExports",
    "graphql/S3ListFiles": "graphql/ListS3Files",
    "graphql/ExportByLinkedInUrls": "graphql/ExportLinkedIn",
    "graphql/SearchByLinkedInUrl": "graphql/SearchLinkedIn",
    "graphql/FindEmailsBulk": "graphql/FindEmails",
    "graphql/VerifyEmailsBulk": "graphql/VerifyBulkEmails",
    "graphql/GetPage": "graphql/GetDashboardPage",
}


def load_endpoint_index() -> dict[tuple[str, str], str]:
    """(endpoint_path, method) -> endpoint_id."""
    if not ENDPOINTS_INDEX.is_file():
        return {}
    data = json.loads(ENDPOINTS_INDEX.read_text(encoding="utf-8"))
    out = {}
    for ep in data.get("endpoints", []):
        path = ep.get("path", "")
        method = ep.get("method", "QUERY")
        eid = ep.get("endpoint_id", "")
        if path and eid:
            out[(path, method)] = eid
    return out


def resolve_endpoint_id(path_to_eid: dict, endpoint_path: str, method: str) -> str | None:
    """Resolve endpoint_id, using aliases if needed."""
    path = endpoint_path
    key = (path, method)
    if key in path_to_eid:
        return path_to_eid[key]
    path = PATH_ALIASES.get(path, path)
    key = (path, method)
    return path_to_eid.get(key)


def load_postman_mappings() -> dict[str, dict]:
    """endpoint_id -> { mapping_id, config_id }."""
    if not POSTMAN_CONFIG.is_file():
        return {}
    data = json.loads(POSTMAN_CONFIG.read_text(encoding="utf-8"))
    out = {}
    for m in data.get("endpoint_mappings", []):
        eid = m.get("endpoint_id", "")
        mid = m.get("mapping_id", "")
        if eid and mid:
            out[eid] = {"mapping_id": mid, "config_id": CONFIG_ID}
    return out


def main() -> None:
    write = "--write" in sys.argv
    if not REL_BY_PAGE_DIR.is_dir():
        print(f"By-page dir not found: {REL_BY_PAGE_DIR}")
        sys.exit(1)

    path_to_eid = load_endpoint_index()
    eid_to_postman = load_postman_mappings()
    print(f"Loaded {len(path_to_eid)} endpoint path+method -> endpoint_id, {len(eid_to_postman)} postman mappings")

    updated_files = 0
    updated_entries = 0
    no_endpoint_id = []

    for path in sorted(REL_BY_PAGE_DIR.glob("*.json")):
        if "_result" in path.name:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Skip {path.name}: {e}")
            continue

        endpoints = data.get("endpoints", [])
        if not endpoints:
            continue

        changed = False
        for entry in endpoints:
            ep_path = entry.get("endpoint_path", "")
            method = entry.get("method", "QUERY")
            endpoint_id = resolve_endpoint_id(path_to_eid, ep_path, method)
            if not endpoint_id:
                no_endpoint_id.append((path.name, ep_path, method))
                continue

            ref = {
                "endpoint_id": endpoint_id,
                "endpoint_path": ep_path,
                "method": method,
                "api_version": entry.get("api_version", "graphql"),
            }
            if entry.get("endpoint_reference") != ref:
                entry["endpoint_reference"] = ref
                changed = True
                updated_entries += 1

            postman_ref = eid_to_postman.get(endpoint_id)
            if postman_ref and entry.get("postman_reference") != postman_ref:
                entry["postman_reference"] = postman_ref
                changed = True
            elif not postman_ref and entry.get("postman_reference") is not None:
                entry["postman_reference"] = None
                changed = True

        if changed and write:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            updated_files += 1
            print(f"Updated {path.name} ({len(endpoints)} endpoints)")
        elif changed:
            updated_files += 1
            print(f"[DRY-RUN] Would update {path.name}")

    print(f"\nUpdated {updated_files} by-page files, {updated_entries} endpoint_reference entries")
    if no_endpoint_id:
        print(f"No endpoint_id for {len(no_endpoint_id)} entries (first 15):")
        for fn, ep, m in no_endpoint_id[:15]:
            print(f"  {fn}  {ep}  {m}")
    if not write and updated_files:
        print("\nRun with --write to apply changes.")


if __name__ == "__main__":
    main()
