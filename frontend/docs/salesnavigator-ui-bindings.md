# Sales Navigator — Frontend UI Bindings

**Service:** `backend(dev)/salesnavigator`  
**GraphQL module:** `23_SALES_NAVIGATOR_MODULE.md`  
**Primary era:** `4.x` (Extension & Sales Navigator maturity)

---

## UI surface map

### 1. Browser Extension — Sales Navigator Page

**Context:** Extension popup injected on `linkedin.com/sales/search/...` pages.

| UI element | Type | API call | Component |
| --- | --- | --- | --- |
| "Save to Contact360" button | Button | `POST /v1/save-profiles` (via GraphQL `saveSalesNavigatorProfiles`) | `SNSaveButton` |
| "Sync page" CTA (scrape + save) | Button | `POST /v1/scrape` with `save:true` | `SNSyncCTA` |
| Profile count badge ("25 profiles found") | Text/Badge | From extraction result | `SNProfileCountBadge` |
| Save progress bar | Progress bar (indeterminate → determinate) | Loading state during save | `SNSaveProgress` |
| Saved count indicator ("18 saved") | Text | `saved_count` from response | `SNSaveSummaryCard` |
| Created vs. updated split | Text | `contacts_created` / `contacts_updated` | `SNSaveSummaryCard` |
| Error toast | Toast notification | `errors[]` in response | `SNErrorToast` |
| Error drawer (detail) | Drawer/Modal | Failed profiles list | `SNErrorDrawer` |
| Retry button | Button | Re-call save | `SNRetryButton` |
| Data quality badge per profile | Badge (green/yellow/red) | `data_quality_score` | `DataQualityBadge` |
| Already-in-Contact360 indicator | Badge/Checkbox state | UUID match returned | `AlreadySavedBadge` |
| Select all / deselect all | Checkbox | Client-side selection | `ProfileSelectAll` |
| Individual profile checkbox | Checkbox | Per-profile selection | `ProfileCheckbox` |
| SN search context header | Text | `search_context.search_id` | `SNSearchContextHeader` |
| Pagination info ("Page 2 of 8") | Text | `pagination` from metadata | `SNPaginationInfo` |

---

### 2. Dashboard — SN Ingestion Panel

**Context:** `/contacts/import` or `/settings/integrations/sales-navigator` page.

| UI element | Type | API call | Component |
| --- | --- | --- | --- |
| Manual profiles upload textarea | Input (textarea) | `POST /v1/save-profiles` | `SNManualUploadInput` |
| Upload button | Button | `POST /v1/save-profiles` | `SNUploadButton` |
| Sync history table | Table | `GET /contacts?source=sales_navigator` (Connectra) | `SNSyncHistoryTable` |
| Sync session detail row | Row | Session metadata | `SNSyncSessionRow` |
| Last synced timestamp | Text | `created_at` | `SNLastSyncedAt` |
| Ingestion stats card | Card | `saved_count`, `errors`, `data_quality_avg` | `SNIngestionStatsCard` |
| Source filter chip | Filter chip | `source=sales_navigator` on contacts search | `SNSourceFilterChip` |
| "Recently imported from SN" section | Section header | Contacts with `source=sales_navigator` sort newest | `SNRecentImportSection` |

---

### 3. Contact Row / Contact Detail Page

**Context:** Contacts table and individual contact detail page.

| UI element | Type | Source | Component |
| --- | --- | --- | --- |
| "Source: Sales Navigator" badge | Badge | `contact.source` | `ContactSourceBadge` |
| SN profile URL link | Link | `contact.linkedin_sales_url` | `SNProfileLink` |
| LinkedIn URL link | Link | `contact.linkedin_url` | `LinkedInProfileLink` |
| Seniority chip | Chip | `contact.seniority` | `SeniorityChip` |
| Department chip(s) | Chip(s) | `contact.departments[]` | `DepartmentChips` |
| Connection degree badge | Badge | `contact.connection_degree` | `ConnectionDegreeBadge` |
| Recently hired indicator | Icon/Badge | `contact.recently_hired` | `RecentlyHiredBadge` |
| Data quality score bar | Progress bar (thin) | `contact.data_quality_score` | `DataQualityBar` |

---

### 4. Contacts Table — Filters and Search

| UI element | Type | Mapping | Component |
| --- | --- | --- | --- |
| Source filter: "Sales Navigator" | Radio/Checkbox filter | `source=sales_navigator` | `ContactSourceFilter` |
| Seniority filter | Checkbox multi-select | `seniority` enum | `SeniorityFilter` |
| Department filter | Checkbox multi-select | `departments[]` | `DepartmentFilter` |
| Connection degree filter | Radio group | `connection_degree` | `ConnectionDegreeFilter` |
| "Imported from SN" date range | Date range input | `created_at` with source filter | `SNImportDateRange` |

---

## Hook map

| Hook | Responsibility | API call |
| --- | --- | --- |
| `useSaveProfiles(profiles)` | Save profile array to Contact360 | `POST /v1/save-profiles` |
| `useScrapeAndSave(html, options)` | Parse HTML + save | `POST /v1/scrape` |
| `useSNSyncStatus()` | Poll sync result + loading/error state | Local state |
| `useSNHistory()` | Load SN ingestion history | Connectra contacts filter |
| `useSNProfileCount(html)` | Count profiles in HTML without saving | `POST /v1/scrape` (`save:false`) |
| `useContactSourceFilter(source)` | Apply source filter in contacts table | Connectra VQL |

---

## Progress bar states

| State | Progress value | Message |
| --- | --- | --- |
| Idle | 0 | — |
| Extracting (HTML parse) | 20% | "Extracting profiles…" |
| Deduplicating | 40% | "Deduplicating…" |
| Saving to Contact360 | 60–90% | "Saving profiles…" |
| Complete (success) | 100% | "X profiles saved" |
| Complete (partial error) | 100% (amber) | "X saved, Y failed" |
| Error | — | Error toast / drawer |

---

## Checkbox and radio button usage

| Element | Purpose | Values |
| --- | --- | --- |
| Profile checkboxes | Select profiles from SN page to save | Per-profile boolean |
| Select-all checkbox | Toggle all profiles on page | All / None / Indeterminate |
| Source filter radio | Filter contacts by data source | `all` / `sales_navigator` / `organic` |
| Connection degree radio | Filter by SN connection level | `1st` / `2nd` / `3rd` |
| Save options checkbox | "Include metadata" when scraping | true/false |

---

## Era delivery schedule

| Era | UI deliverables |
| --- | --- |
| `0.x` | No user-facing UI; service stubs only |
| `1.x` | Auth/actor context in save calls; no visual change |
| `2.x` | Email field coverage indicator in profile preview |
| `3.x` | Contact detail badges: source, seniority, department; contact filter chips |
| `4.x` | **Full extension popup UI**: save button, progress bar, error drawer, retry, quality badge; dashboard ingestion panel |
| `5.x` | AI-ready field coverage badge; "SN contacts eligible for AI" indicator |
| `6.x` | Partial-save UX (saved/failed split); retry-after feedback; loading state improvements |
| `7.x` | Role-gated save actions; audit log view |
| `8.x` | API quota display for SN usage; rate limit feedback UX |
| `9.x` | Connector health card; integration status panel |
| `10.x` | Campaign audience builder: SN-sourced segment filter; provenance badge |

---

## Cross-references

- Codebase: `docs/codebases/salesnavigator-codebase-analysis.md`
- GraphQL module: `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`
- Era task packs: `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- Data lineage: `docs/backend/database/salesnavigator_data_lineage.md`

## Implementation status snapshot

- Implemented: auth/session binding (`graphqlSession.js`), Lambda transport (`lambdaClient.js`), profile merge/dedup (`profileMerger.js`), and backend save/scrape contracts.
- Pending: full popup/content shell bindings (`manifest.json`, popup UI actions, content script lifecycle wiring).

## 2026 addendum

- Primary integration flow: extension popup -> SN scrape/save action -> Lambda SN API -> Connectra upsert.
- CORS wildcard policy is a known risk and should be reflected in reliability/security UX notes.
