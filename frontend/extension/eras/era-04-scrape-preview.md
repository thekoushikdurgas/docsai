# Era 4 — Scrape & preview

**Goal:** Capped HTML snapshot, optional GraphQL scrape via API, page kind, preview list.

**Checklist**

- [x] `content.js` — `page_kind` including `public_search` for `linkedin.com/search/`, `htmlSnapshot`, flags
- [x] `c360_use_scrape_endpoint`, `c360_html_snapshot_max_kb`
- [x] Side panel Preview tab — meta (`c360-panel__meta`), profile/company link lists, HTML snippet; `c360_last_capture_preview` in SW; preview helpers in `sidepanel/preview.js`
- [x] Background routes to GraphQL `postScrape` when enabled **and** `page_kind` is Sales Navigator (`sales_*`); otherwise `saveSalesNavigatorProfiles` only
