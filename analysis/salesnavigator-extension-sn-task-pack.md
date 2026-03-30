# Sales Navigator — 4.x Extension & Sales Navigator Maturity Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `4.x` — Contact360 Extension and Sales Navigator Maturity  
**Status:** PRIMARY DELIVERY ERA — full feature complete

---

## Contract track

- [ ] Lock final API contract for `POST /v1/save-profiles` and `POST /v1/scrape`
- [ ] Fix documentation drift: remove `POST /v1/scrape-html-with-fetch` from `docs/api.md` (not implemented) OR implement it
- [ ] Clarify `POST /v1/scrape` active status in `README.md` (README incorrectly states scraping is removed)
- [ ] Define error response structure: `{success: false, errors: [{profile_url, message}]}`
- [ ] Define partial-success semantics: `saved_count > 0` with non-empty `errors[]` is valid
- [ ] Lock `ScrapeHtmlRequest` max HTML size (10 MB) as tested and documented
- [ ] Freeze `SaveProfilesRequest` max profiles (1000) with rejection behavior documented

## Service track

- [ ] Harden HTML extraction across multiple SN DOM variants:
  - [ ] Standard search results page
  - [ ] Account map view
  - [ ] People tab on company page
- [ ] Optimize extraction for 25-profile search result pages (primary extension use case)
- [ ] Validate deduplication correctness: same `profile_url` → single record, best-completeness kept
- [ ] Fix `convert_sales_nav_url_to_linkedin()` coverage — document when PLACEHOLDER is returned
- [ ] Implement extraction fallback for missing fields (graceful null, not error)
- [ ] Add `X-Request-ID` correlation header to all responses
- [ ] Test chunk boundary behavior: exactly 500, 501, 1000 profiles

## Surface track

### Extension popup UI (primary deliverable)

- [ ] `SNSaveButton` — "Save to Contact360" button with loading state
- [ ] `SNSyncCTA` — "Sync Page" button (scrape + save)
- [ ] `SNProfileCountBadge` — "25 profiles found"
- [ ] `SNSaveProgress` — progress bar: idle → extracting (20%) → dedup (40%) → saving (60–90%) → done (100%)
- [ ] `SNSaveSummaryCard` — shows saved count, created/updated split
- [ ] `SNErrorToast` — quick error notification
- [ ] `SNErrorDrawer` — detailed failed profiles list with reason
- [ ] `SNRetryButton` — retry after partial failure
- [ ] `DataQualityBadge` — per-profile quality indicator (green/yellow/red)
- [ ] `AlreadySavedBadge` — show if profile UUID already in Contact360
- [ ] `ProfileCheckbox` + `ProfileSelectAll` — selective save
- [ ] `ConnectionDegreeBadge` — 1st/2nd/3rd degree indicator

### Dashboard SN panel

- [ ] `SNIngestionPanel` — `/contacts/import` tab with SN section
- [ ] `SNSyncHistoryTable` — past SN sync sessions with stats
- [ ] `SNIngestionStatsCard` — saved count, quality average, error rate
- [ ] `SNSourceFilterChip` — filter contacts by `source=sales_navigator`

## Data track

- [ ] Confirm provenance fields written per profile: `lead_id`, `search_id`, `data_quality_score`, `connection_degree`, `recently_hired`, `is_premium`
- [ ] Add `source="sales_navigator"` tag on all contacts from this service
- [ ] Validate `data_quality_score` computation accuracy (70% required + 30% optional weighted)
- [ ] Dedup evidence: log `duplicate_count` per save session

## Ops track

- [ ] P95 latency target: `save-profiles` for 25 profiles < 3s; for 100 profiles < 5s
- [ ] CloudWatch alarm: `save-profiles` Lambda timeout rate > 1%
- [ ] Lambda timeout tuning: current 60s sufficient for 1000 profiles; confirm under load
- [ ] Test: 1000-profile batch end-to-end in staging
- [ ] Deploy via SAM to staging + production
- [ ] Extension CSP check: confirm Lambda API domain is allowed in extension manifest

---

**P0 action items (must complete before release):**

1. Fix doc drift: `scrape-html-with-fetch` in `docs/api.md`
2. Fix README scraping ambiguity
3. Add `X-Request-ID` correlation header

---

**References:**
- [docs/frontend/salesnavigator-ui-bindings.md](../frontend/salesnavigator-ui-bindings.md)
- [docs/backend/database/salesnavigator_data_lineage.md](../backend/database/salesnavigator_data_lineage.md)
- [docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json](../backend/endpoints/salesnavigator_endpoint_era_matrix.json)
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- `docs/frontend/salesnavigator-ui-bindings.md`
- `docs/backend/database/salesnavigator_data_lineage.md`

---

## Extension surface contributions (era sync)

### Era 4.x — Extension & Sales Navigator Maturity

**`extension/contact360` full reliability and UX hardening:**
- `utils/lambdaClient.js` — retry with exponential back-off + jitter; adaptive timeout per retry; request queueing
- `auth/graphqlSession.js` — proactive 5-min token refresh buffer for uninterrupted scrape sessions
- `utils/profileMerger.js` — HTML vs deep-scrape variant support; per-field merge with completeness-based tie-breaking

**Extension popup UI contract (to be implemented in popup layer):**
- Progress bar: idle → extracting (20%) → dedup (40%) → saving (60–90%) → done (100%)
- Profile count badge (deduplicated vs raw)
- Error toast for failed batches with retry CTA
- Token status indicator (active / expired)
- Sync status panel (saved / errored counts)

**Tasks:**
- [ ] Wire `lambdaClient.saveProfiles()` to popup progress bar update events
- [ ] Implement `SNRetryButton` backed by retry logic in `lambdaClient`
- [ ] Confirm adaptive timeout values under Lambda cold-start conditions
- [ ] Test proactive token refresh in long scrape sessions (30+ min)