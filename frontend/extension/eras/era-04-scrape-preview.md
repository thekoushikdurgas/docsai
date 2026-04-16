# Era 4 — Scrape & preview

**Goal:** Capped HTML snapshot, optional `/v1/scrape`, page kind.

**Checklist**

- [x] `content.js` — `page_kind`, `htmlSnapshot`, async storage for flags
- [x] `c360_use_scrape_endpoint`, `c360_html_snapshot_max_kb`
- [x] Side panel Preview tab + `c360_last_capture_preview` in SW
- [x] Background routes to `postScrape` when enabled
