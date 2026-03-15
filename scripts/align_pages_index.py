"""
One-off: Align media/pages/pages_index.json with single-page files.
- Removes entries for pages that have no file: billing_success_page, companies_id_page.
- Appends entries for page files that are missing from the index: admin_page, email_page,
  files_page, jobs_page, live_voice_page.
Run from repo root (contact360/docsai) with: python scripts/align_pages_index.py
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCSAI_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = DOCSAI_ROOT / "media" / "pages"
PAGES_INDEX = PAGES_DIR / "pages_index.json"

STALE_PAGE_IDS = {"billing_success_page", "companies_id_page"}
MISSING_PAGE_FILES = [
    "admin_page.json",
    "email_page.json",
    "files_page.json",
    "jobs_page.json",
    "live_voice_page.json",
]


def main() -> int:
    if not PAGES_INDEX.exists():
        print(f"Not found: {PAGES_INDEX}", file=sys.stderr)
        return 1
    data = json.loads(PAGES_INDEX.read_text(encoding="utf-8"))
    if not isinstance(data.get("pages"), list):
        print("pages_index.json has no 'pages' array", file=sys.stderr)
        return 1

    pages = [p for p in data["pages"] if p.get("page_id") not in STALE_PAGE_IDS]
    existing_ids = {p.get("page_id") for p in pages}

    for filename in MISSING_PAGE_FILES:
        path = PAGES_DIR / filename
        if not path.exists():
            print(f"Skip (file missing): {filename}", file=sys.stderr)
            continue
        page_id = path.stem
        if page_id in existing_ids:
            continue
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            pages.append(obj)
            existing_ids.add(page_id)
            print(f"Added: {page_id}")
        except Exception as e:
            print(f"Error loading {filename}: {e}", file=sys.stderr)

    data["pages"] = pages
    data["total"] = len(pages)
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    PAGES_INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written {PAGES_INDEX.name}: total={len(pages)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
