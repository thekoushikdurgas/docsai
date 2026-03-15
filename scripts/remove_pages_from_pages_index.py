"""Remove the 12 admin/data_search pages from media/pages/pages_index.json."""
import json
import sys
from pathlib import Path

DOCSAI_ROOT = Path(__file__).resolve().parent.parent
PAGES_INDEX = DOCSAI_ROOT / "media" / "pages" / "pages_index.json"

PAGE_IDS_TO_REMOVE = [
    "admin_dashboard_pages_page",
    "admin_dashboard_pages_pageid_page",
    "admin_logs_page",
    "admin_marketing_new_page",
    "admin_marketing_page",
    "admin_marketing_pageid_page",
    "admin_settings_page",
    "admin_statistics_page",
    "admin_system_status_page",
    "admin_user_history_page",
    "admin_users_page",
    "data_search_page",
]

ROUTES_TO_REMOVE = [
    "/admin/dashboard-pages",
    "/admin/dashboard-pages/[pageId]",
    "/admin/logs",
    "/admin/marketing/new",
    "/admin/marketing",
    "/admin/marketing/[pageId]",
    "/admin/settings",
    "/admin/statistics",
    "/admin/system-status",
    "/admin/user-history",
    "/admin/users",
    "/data-search",
]


def main() -> int:
    if not PAGES_INDEX.exists():
        print(f"Error: {PAGES_INDEX} not found")
        return 1

    with open(PAGES_INDEX, encoding="utf-8") as f:
        data = json.load(f)

    remove_set = set(PAGE_IDS_TO_REMOVE)
    routes_set = set(ROUTES_TO_REMOVE)

    # 1. Filter pages array
    original_count = len(data["pages"])
    data["pages"] = [p for p in data["pages"] if p.get("page_id") not in remove_set]
    new_count = len(data["pages"])
    removed = original_count - new_count
    if removed != 12:
        print(f"Warning: expected to remove 12 pages, actually removed {removed}")

    # 2. Update indexes.by_type.dashboard
    if "indexes" in data and "by_type" in data["indexes"] and "dashboard" in data["indexes"]["by_type"]:
        data["indexes"]["by_type"]["dashboard"] = [
            pid for pid in data["indexes"]["by_type"]["dashboard"] if pid not in remove_set
        ]

    # 3. Update indexes.by_route
    if "indexes" in data and "by_route" in data["indexes"]:
        for route in routes_set:
            data["indexes"]["by_route"].pop(route, None)

    # 4. Update indexes.by_status.published
    if "indexes" in data and "by_status" in data["indexes"] and "published" in data["indexes"]["by_status"]:
        data["indexes"]["by_status"]["published"] = [
            pid for pid in data["indexes"]["by_status"]["published"] if pid not in remove_set
        ]

    # 5. Update indexes.by_page_state.published
    if "indexes" in data and "by_page_state" in data["indexes"] and "published" in data["indexes"]["by_page_state"]:
        data["indexes"]["by_page_state"]["published"] = [
            pid for pid in data["indexes"]["by_page_state"]["published"] if pid not in remove_set
        ]

    # 6. Update total and statistics
    data["total"] = new_count
    if "statistics" in data:
        data["statistics"]["total"] = new_count
        if "by_status" in data["statistics"]:
            data["statistics"]["by_status"]["published"] = new_count
        if "by_page_state" in data["statistics"]:
            data["statistics"]["by_page_state"]["published"] = new_count
        if "by_type" in data["statistics"] and "dashboard" in data["statistics"]["by_type"]:
            dash = data["statistics"]["by_type"]["dashboard"]
            dash["total"] = dash.get("total", 0) - removed
            dash["published"] = dash.get("published", 0) - removed

    with open(PAGES_INDEX, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Removed {removed} pages from pages_index.json. Total pages: {new_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
