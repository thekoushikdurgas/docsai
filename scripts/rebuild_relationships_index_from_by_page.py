#!/usr/bin/env python3
"""
Rebuild media/relationship/index.json from by-page files.
Groups relationships by endpoint_path + method.
"""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REL_DIR = Path(__file__).resolve().parent.parent / "media" / "relationship"
REL_BY_PAGE_DIR = REL_DIR / "by-page"
REL_BY_ENDPOINT_DIR = REL_DIR / "by-endpoint"
INDEX_PATH = REL_DIR / "index.json"
REL_INDEX_PATH = REL_DIR / "relationships_index.json"

def main():
    grouped = defaultdict(list)  # (endpoint_path, method) -> [rel objects]
    for p in sorted(REL_BY_PAGE_DIR.glob("*.json")):
        if "_result" in p.name:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            for ep in data.get("endpoints", []):
                key = (ep.get("endpoint_path", ""), ep.get("method", "QUERY"))
                grouped[key].append(ep)
        except Exception as e:
            print(f"Skip {p.name}: {e}")
    rels = []
    for (ep_path, method), pages in sorted(grouped.items(), key=lambda x: (x[0][0], x[0][1])):
        rels.append({
            "endpoint_path": ep_path,
            "method": method,
            "pages": pages,
            "created_at": pages[0].get("created_at", ""),
            "updated_at": pages[0].get("updated_at", ""),
        })
    now = datetime.now(timezone.utc).isoformat()
    total = sum(len(r["pages"]) for r in rels)
    out = {
        "version": "2.0",
        "last_updated": now,
        "total": total,
        "relationships": rels,
    }
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote index.json: {total} relationships, {len(rels)} endpoint groups")

    # Flatten for relationships_index.json (flat list of relationship objects)
    flat = []
    for (ep_path, method), pages in grouped.items():
        flat.extend(pages)
    flat.sort(key=lambda r: (r.get("page_path", ""), r.get("endpoint_path", "")))
    rel_index = {
        "version": "2.0",
        "last_updated": now,
        "total": len(flat),
        "relationships": flat,
    }
    with open(REL_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(rel_index, f, indent=2, ensure_ascii=False)
    print(f"Wrote relationships_index.json: {len(flat)} relationships")

    # Regenerate by-endpoint files (replace all)
    REL_BY_ENDPOINT_DIR.mkdir(parents=True, exist_ok=True)
    new_filenames = set()
    for (ep_path, method), pages in grouped.items():
        op = ep_path.replace("graphql/", "") if ep_path else "Unknown"
        fn = f"graphql_{op}_{method}.json"
        out_path = REL_BY_ENDPOINT_DIR / fn
        obj = {
            "endpoint_path": ep_path,
            "method": method,
            "pages": pages,
            "created_at": pages[0].get("created_at", ""),
            "updated_at": pages[0].get("updated_at", ""),
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
        new_filenames.add(fn)
    # Remove stale by-endpoint files
    for p in REL_BY_ENDPOINT_DIR.glob("*.json"):
        if p.name not in new_filenames and "_result" not in p.name:
            p.unlink()
            print(f"Removed stale {p.name}")
    print(f"Wrote {len(grouped)} by-endpoint files")

if __name__ == "__main__":
    main()
