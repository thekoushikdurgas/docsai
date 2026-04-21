# Admin console backlog (Contact360)

**Doc / code comments:** Prefer module docstrings that name the **phase** (0–11), **gateway
GraphQL** fields used (`admin.*`, `contacts.*`, …), and for Django views a trailing
`@role:` line (`public`, `authenticated`, `admin_or_super_admin`, `super_admin`) matching
the decorator.

Grouped by product phase. Cross-cutting: [`docs/backend/endpoints/contact360.io/ADMIN-MODULE.md`](../../docs/backend/endpoints/contact360.io/ADMIN-MODULE.md), [`docs/codebases/admin.md`](../../docs/codebases/admin.md).

## Backlog execution batches (plan reference)

| Batch | Scope                                                                                            |
| ----- | ------------------------------------------------------------------------------------------------ |
| 1     | Django-only quick wins: architecture + satellite health, legacy apps, SSRF guard, templates stub |
| 2     | Gateway observability: `apiMetadata` build info, analytics / `performanceStats`                  |
| 3     | Gateway governance: `admin` mutation audit + two-person approvals                                |
| 4     | Verticals: `knowledge.*`, jobs DLQ listing, AI SSE proxy, remaining S3 env parity                |

## Resolved in this pass (2026-04-21)

- [x] Contacts explorer (`/admin/ops/contacts-explorer/`) — `contacts.contacts` via operator JWT; pagination. (Org switcher still open.)
- [x] Campaign CQL lab (`/admin/ops/campaign-cql/`) — `campaignSatellite.cqlParse`, `cqlValidate`, `renderTemplatePreview`.
- [x] `ai_agent` non-streaming — `aiChats.*` GraphQL (`createAIChat`, `sendMessage`, list). SSE still TBD.
- [x] System status — `health.apiMetadata` card (name / version / docs).
- [x] Optional `ADMIN_STORAGE_VIA_GATEWAY` — `s3.deleteFile` for `json_store` / `page_builder` deletes with direct API fallback; uploads still direct s3storage.
- [x] Analytics — removed sample Chart.js data; callout for Phase 6 time-series.
- [x] `durgasman` — `/durgasman/import/` wired; legacy `api/analyze` deprecation response.
- [x] Header — safe display when `operator` lacks `name` / `email`.

## Resolved in plan implementation (2026-04-21 b)

- [x] **Batch 1:** Architecture registry columns from `health.satelliteHealth`; `postman_app` documented (not installed); `templates_app` stub clarified; `OperationLog` retained for ops/Phase 6; `durgasman` SSRF guard + `DURGASMAN_ALLOWED_REQUEST_HOSTS`.
- [x] **Batch 2:** `health.apiMetadata.buildSha` / `gitRef` (env `BUILD_SHA`, `GIT_REF`); analytics `performanceTrends` chart + `health.performanceStats` KPIs.
- [x] **Batch 3:** `graphql_audit_events` for all `admin.*` mutations (payload SHA-256 in `detail`); `admin.graphqlAuditEvents` query; two-person rule via `requestDangerousOperationApproval` + `approvalId` on `deleteUser` / `promoteToSuperAdmin` when `REQUIRE_TWO_PERSON_DANGEROUS_ADMIN` or when `approvalId` is supplied.
- [x] **Batch 4:** Gateway `knowledge.*` module + Django knowledge UI; `jobs.deadLetterJobs` (failed scheduler rows); AI SSE (`POST /api/v1/ai-chats/{id}/message/stream` + Django proxy). **Open:** full admin S3 via `s3.*` only (upload/list env) — see Phase 8.

## Phase 0 — Foundation

- [x] Drive `architecture` service table from live `health.satelliteHealth` where possible.
- [x] Remove or fully migrate legacy `apps/postman_app` tree after confirming no external bookmarks. _(Not in `INSTALLED_APPS`; tree kept for migration reference — see `apps/postman_app/README.md`.)_
- [x] `templates_app`: wire to gateway or remove. _(Stub + doc; no `templates` GraphQL module.)_
- [x] `OperationLog` model: use for Phase 6 persisted ops or drop migration. _(Kept — used by documentation ops; see model docstring.)_

## Phase 1 — Users / billing / credits

- [x] Audit log for every `admin.*` mutation (who/when/payload hash). _(`graphql_audit_events` + `admin.graphqlAuditEvents`.)_
- [x] Two-person approval for `deleteUser` and `promoteToSuperAdmin`. _(Optional `approvalId`; enforce with `REQUIRE_TWO_PERSON_DANGEROUS_ADMIN`.)_

## Phase 2 — Email / phone

- [x] Satellite-level retry & dead-letter admin views (via `jobs.*` only). _(`jobs.deadLetterJobs` lists failed scheduler jobs; email-server DLQ still separate.)_

## Phase 3 — Contacts / companies

- [ ] Contacts explorer: org switcher / impersonation when product JWT supports it.

## Phase 4 — Extension / Sales Navigator

- [ ] Extension capture job browser (previews by org) via gateway-only paths.

## Phase 5 — AI

- [x] Knowledge CRUD when `knowledge.*` exists on gateway.
- [x] `ai_agent` streaming — SSE via gateway when same contract as product app.

## Phase 6 — Reliability

- [x] SLO dashboard: `health.performanceStats` + `admin.logStatistics` trends. _(Partial — KPIs + log trend chart.)_
- [x] Real time-series charts on `/analytics/` when metrics series exist on GraphQL. _(Log `performanceTrends` line chart.)_

## Phase 7 — Deployment

- [x] Release badge / build SHA on system status; **per-satellite** version skew (beyond `health.apiMetadata`). _(Build SHA / git ref on metadata; per-satellite version still TODO for satellites.)_

## Phase 8 — APIs / storage

- [ ] `page_builder` / `json_store`: full S3 path via gateway `s3.*` (upload + list + presign); remove `S3STORAGE_*` from admin env.
- [x] Harden `durgasman` execute allowlist (optional URL blocklist for SSRF).

## Phase 9 — Ecosystem

- [ ] Durgasflow execution list via **read-only** gateway query (multi-tenant audit).

## Phase 10 — Campaigns

- [x] CQL lab + template preview UI (`campaignSatellite` GraphQL). _(Campaign service must be configured on gateway.)_

## Phase 11 — Leads / recommendations

- [ ] Admin surfaces when lead-scoring GraphQL exists.
