---
name: Contact360 Docs Overhaul
overview: Comprehensively update all Contact360 documentation files to reflect the actual implementation state, discovered gaps, and pending tasks from the deep codebase analysis of 11 services across the 0.x–10.x roadmap. This covers top-level docs, era folders, backend/frontend subdocs, and codebase analysis files.
todos:
  - id: g1-core-docs
    content: "Update 11 top-level core docs: architecture.md, codebase.md, backend.md, roadmap.md, versions.md, governance.md, audit-compliance.md, version-policy.md, docsai-sync.md, flowchart.md, frontend.md"
    status: completed
  - id: g2-codebase-analysis
    content: Update 10 codebase analysis files in docs/codebases/ with discovered gaps, architecture risks, and era task breakdowns (admin, s3storage, logsapi, emailapis, connectra, appointment360, emailcampaign, mailvetter, salesnavigator, contact-ai)
    status: in_progress
  - id: g3-era-folders
    content: "Update era folder README files and master checklists (docs/0–10): add service states, blocking P0 gaps, and task pack entries for admin/s3storage/logs.api/emailapigo/emailapis"
    status: pending
  - id: g4-era-task-packs
    content: Create/update era task pack files for 5 newly covered services (admin, s3storage, logs.api, emailapigo, emailapis) across all 11 era folders (0–10) — ~55 files
    status: pending
  - id: g5-backend-apis
    content: Update docs/backend/apis/ module docs (15, 17, 22, 23) and create new ADMIN_ERA_TASK_PACKS.md and EMAILAPIGO_ERA_TASK_PACKS.md
    status: pending
  - id: g6-database-lineage
    content: Update 4 data lineage files (emailcampaign, logsapi, s3storage, emailapis) and create admin_data_lineage.md in docs/backend/database/
    status: pending
  - id: g7-endpoint-matrices
    content: Update/create 5 endpoint era matrix JSONs (s3storage, logsapi, appointment360, emailcampaign, admin) in docs/backend/endpoints/
    status: pending
  - id: g8-frontend-docs
    content: Create admin-ui-bindings.md and update 4 existing frontend/docs UI binding files (s3storage, logsapi, salesnavigator, emailapis)
    status: pending
  - id: g9-services-apis
    content: Update 3 services.apis docs (contact.ai, mailvaiter, salesnavigator) to fix stale routes and add admin service API doc
    status: pending
isProject: false
---

# Contact360 Documentation Overhaul Plan

## Context & Scope

Based on deep analysis of 11 codebases (`contact.ai`, `email campaign`, `mailvetter`, `salesnavigator`, `contact360.io/api`, `contact360.io/sync`, `emailapigo`, `emailapis`, `logs.api`, `s3storage`, `contact360.io/admin`), all documentation must be updated to reflect actual implementation state, discovered architecture risks, and era-by-era task completion status.

Total files to modify: ~200+ files across 8 doc groups.

---

## Group 1 — Top-Level Core Docs (11 files)

These are the canonical reference files. All other docs derive from them.

### 1.1 `[docs/architecture.md](docs/architecture.md)`

- Add `contact360.io/admin` (Django/DocsAI) to the service topology diagram and boundary table
- Add `lambda/s3storage` multipart session risk note (in-memory state, no auth middleware)
- Add `lambda/logs.api` storage contract note (S3 CSV, NOT MongoDB — fix stale reference)
- Add `lambda/emailapigo` and `lambda/emailapis` to service map with their dual-DB pattern (PostgreSQL + Redis TTL cache)
- Add cross-service auth gap summary: which services lack API key middleware (s3storage P0)
- Add `backend(dev)/email campaign` DB bugs note (EC-0.2 `DB.Exec` vs `DB.Get` bug)

### 1.2 `[docs/codebase.md](docs/codebase.md)`

- Add `contact360.io/admin` entry with its Django app structure, URL routing map, and service clients
- Update `lambda/s3storage` entry: document `_MULTIPART_SESSIONS` in-memory risk and open CORS
- Update `lambda/logs.api` entry: replace MongoDB with S3 CSV storage truth
- Update `lambda/emailapigo` entry: document hardcoded log API key gap (`EGO-0.4`)
- Update `backend(dev)/email campaign` entry: document `DB.Exec` query bug and missing `templates` table
- Add service→service client dependency matrix (which service calls which)

### 1.3 `[docs/backend.md](docs/backend.md)`

- Add `contact360.io/admin` backend track by era (0.x–10.x) following the same pattern as other services
- Update `lambda/s3storage` era track to mark P0 gaps (no auth, in-memory state)
- Update `lambda/logs.api` era track to fix MongoDB reference
- Update `lambda/emailapigo` era track with hardcoded key gap
- Update `backend(dev)/email campaign` era track with EC-0.x bugs
- Add era task-pack links for `contact360.io/admin`

### 1.4 `[docs/roadmap.md](docs/roadmap.md)`

- Add `contact360.io/admin` cross-era execution stream (0.x–10.x) following the service section pattern
- Update `0.x` completion percentage — mark services that have P0 bugs as "stabilization incomplete"
- Update `1.x` section: mark admin billing UI as "In Progress" (billing views exist, credit audit trail missing)
- Update `6.x` section: mark all services with in-memory rate limiters as "reliability incomplete"
- Update `8.x` section: mark s3storage and admin as "API maturity incomplete"

### 1.5 `[docs/versions.md](docs/versions.md)`

- Add `0.x` era completion notes for each service based on analysis (what's done vs what's blocking)
- Add `1.1.0` in-progress evidence: list which billing/credit flows are working vs gap
- Add `contact360.io/admin` to the `1.x` evidence section
- Update `2.x` planned status with email campaign P0 bugs that block this era
- Mark `6.x` as "blocked by P0 reliability gaps" across s3storage, email campaign, and mailvetter

### 1.6 `[docs/governance.md](docs/governance.md)`

- Add `contact360.io/admin` governance controls section (following the pattern of other services already in file)
  - Controls: secret isolation, route permission tests, idempotency for destructive actions, S3/logs client auth
  - CI baseline checks: auth guard, permission matrix, billing action idempotency, client key rotation
- Add `lambda/emailapigo` governance controls section
  - Controls: hardcoded key rule (P0), CORS rule, migration rule, composite index contract
  - CI checks: auth guard, rate limit, cache upsert, provider fallback chain
- Add `lambda/emailapis` governance controls section
  - Controls: API key rotation, status vocabulary freeze, bulk idempotency, CORS rule
  - CI checks: auth guard, status vocab, bulk endpoint idempotency, provider fallback

### 1.7 `[docs/audit-compliance.md](docs/audit-compliance.md)`

- Add `contact360.io/admin` compliance surface section
  - Audit trail gaps: admin actions (log delete, job retry, billing approve) not emitting immutable events
  - Required: idempotency for ADM-0.4, credit change audit timeline ADM-1.1
- Add `lambda/s3storage` compliance surface section
  - Missing: API auth (S3S-0.1), object lifecycle audit, upload/delete audit events
- Add `lambda/emailapigo`/`lambda/emailapis` compliance section
  - Missing: hardcoded log key (EGO-0.4), no audit trail for bulk verification
- Update `backend(dev)/email campaign` compliance section: add `EC-0.2` bug and missing unsubscribe audit

### 1.8 `[docs/version-policy.md](docs/version-policy.md)`

- Add policy rule: a service with a P0 bug (data corruption, auth bypass, in-memory distributed state) cannot advance past its current era until the P0 is resolved
- Add policy for `contact360.io/admin` releases (Django-specific: migrations, static files, systemd/gunicorn restart)
- Add policy for services with runtime auto-migrations: require explicit migration scripts before `6.x`

### 1.9 `[docs/docsai-sync.md](docs/docsai-sync.md)`

- Add sync rule for `contact360.io/admin`: Django constants files (`roadmap/constants.py`, `architecture/constants.py`) must be updated when `docs/roadmap.md` and `docs/architecture.md` change
- Add sync rule `MV-5` for `emailapigo`: endpoint contract changes must update `emailapigo_endpoint_era_matrix.json`
- Add sync rule for `s3storage`: multipart session state contract changes must update `s3storage-codebase-analysis.md`
- Add sync rule for `logs.api`: storage contract (S3 CSV) change must update `logsapi_data_lineage.md`

### 1.10 `[docs/flowchart.md](docs/flowchart.md)`

- Add `contact360.io/admin` runtime flow diagram (request → middleware stack → RBAC decorator → view → service clients)
- Add `lambda/s3storage` upload flow diagram (single-shot vs multipart, metadata worker trigger, in-memory session risk callout)
- Add `lambda/logs.api` ingest flow (POST → S3 CSV append → background task → TTL cache invalidation)
- Add `lambda/emailapigo` finder pipeline flow (Connectra → pattern → generator → web → IcyPeas fallback chain)
- Update email campaign flow: mark EC-0.2 query bug path with a "BUG" annotation

### 1.11 `[docs/frontend.md](docs/frontend.md)`

- Add `contact360.io/admin` frontend surface: Django templates, Tailwind-built pages, admin views (billing, users, logs, jobs, storage)
- Add admin billing panel bindings: `billing_payments_view`, `billing_qr_upload_view`, `billing_settings_view`
- Add admin integration client bindings: `s3storage_client.py`, `logs_api_client.py`, `admin_client.py`
- Note missing frontend-to-admin auth client gap (S3Storage client lacks API key header `S3S-0.1` counterpart)

---

## Group 2 — Codebase Analysis Files (docs/codebases/)

Each file needs to be updated with the discoveries from the deep analysis session.

### 2.1 `[docs/codebases/admin-codebase-analysis.md](docs/codebases/admin-codebase-analysis.md)`

- Currently only 79 lines — expand to full analysis format
- Add: Django app structure map, middleware stack (5 custom middlewares), RBAC decorators, service clients
- Add: architecture risks (hardcoded LOGS_API_KEY fallback, s3storage client missing auth header, blurry public/private API boundary)
- Add: era-by-era status (ADM-0.x through ADM-10.x gaps) with P0/P1/P2/P3 task breakdown

### 2.2 `[docs/codebases/s3storage-codebase-analysis.md](docs/codebases/s3storage-codebase-analysis.md)`

- Add critical risks section: `_MULTIPART_SESSIONS` in-memory state (S3S-0.3), open CORS, no API auth middleware
- Add era task breakdown (S3S-0.1 through S3S-5.4) with priority labels
- Add service dependency map: `s3storage-metadata-worker` invocation pattern (hardcoded function name S3S-0.4)

### 2.3 `[docs/codebases/logsapi-codebase-analysis.md](docs/codebases/logsapi-codebase-analysis.md)`

- Fix stale MongoDB reference — storage is S3 CSV files (LOG-0.1 truth lock)
- Add: S3 CSV storage architecture, in-memory filter/search, TTL cache pattern
- Add: era task breakdown (LOG-0.1 through LOG-4.4) with priority labels

### 2.4 `[docs/codebases/emailapis-codebase-analysis.md](docs/codebases/emailapis-codebase-analysis.md)`

- Add: fallback chain architecture (Connectra → pattern → generator → web → IcyPeas)
- Add: hardcoded key gap (EPA-0.2 docs security), debug prints (EPA-0.3), status vocab drift
- Add: era task breakdown (EPA-0.1 through EPA-4.4) with priority labels

### 2.5 `[docs/codebases/connectra-codebase-analysis.md](docs/codebases/connectra-codebase-analysis.md)`

- Add: open CORS (SYNC-0.2), no request correlation IDs (SYNC-0.1)
- Add: era task breakdown (SYNC-0.1 through SYNC-3.4) with priority labels

### 2.6 `[docs/codebases/appointment360-codebase-analysis.md](docs/codebases/appointment360-codebase-analysis.md)`

- Add: debug file write bugs (AP-0.1) — `mutations.py`, `queries.py`, `lambda_email_client.py`
- Add: in-memory idempotency/abuse-guard risk for multi-instance (AP-1.2)
- Add: era task breakdown (AP-0.1 through AP-3.3) with priority labels

### 2.7 `[docs/codebases/emailcampaign-codebase-analysis.md](docs/codebases/emailcampaign-codebase-analysis.md)`

- Add: `DB.Exec` vs `DB.Get` bug in `db/queries.go` (EC-0.2) — critical correctness bug
- Add: missing `templates` table in schema (EC-0.1)
- Add: SMTP auth not wired (EC-0.3), hardcoded Redis/DB config (EC-0.4)
- Add: era task breakdown (EC-0.1 through EC-10.3) with priority labels

### 2.8 `[docs/codebases/mailvetter-codebase-analysis.md](docs/codebases/mailvetter-codebase-analysis.md)`

- Add: in-memory rate limiter risk (MV-3), webhook secret fallback (MV-2)
- Add: status vocabulary inconsistency across legacy/v1 routes (MV-1)
- Add: era task breakdown (MV-0 through MV-14) with priority labels

### 2.9 `[docs/codebases/salesnavigator-codebase-analysis.md](docs/codebases/salesnavigator-codebase-analysis.md)`

- Add: docs/code route drift (SN-0.1) — `/v1/scrape`, `/v1/save-profiles` vs documented routes
- Add: no request correlation IDs (SN-1.1), no rate limiting (SN-1.2)
- Add: era task breakdown (SN-0.1 through SN-3.4) with priority labels

### 2.10 `[docs/codebases/contact-ai-codebase-analysis.md](docs/codebases/contact-ai-codebase-analysis.md)`

- Add: provider routing drift (AI-priority-1), message validation gaps (AI-priority-2)
- Add: era task breakdown with P1–P6 priority labels from prior analysis

---

## Group 3 — Era Folder README and Checklist Updates (docs/0–10)

Each era folder needs its README and master checklist updated with the discovered service states.

### 3.1 `docs/0.*/0.x-master-checklist.md`

- Add status column for each service: mark `s3storage`, `email campaign`, `mailvetter` as "P0 gaps exist — stabilization incomplete"
- Add P0 items as blocking checklist items before `0.x` exit gate

### 3.2 `docs/1.*/README.md` and `1.x-master-checklist.md`

- Add `contact360.io/admin` to service coverage table
- Mark admin billing/credit audit trail (ADM-1.1) as incomplete in 1.x

### 3.3 `docs/2.*/README.md`

- Add blocking note: `email campaign` P0 bugs (EC-0.1 to EC-0.4) must be resolved before `2.x` can ship
- Add admin email panel (ADM-2.1) as `2.x` planned item

### 3.4 `docs/6.*/README.md`

- Add "reliability blockers" section listing services with in-memory state that must be resolved
- Services: s3storage (in-memory sessions), mailvetter (in-memory limiter), appointment360 (in-memory abuse guard), emailapigo/emailapis (in-memory cache in serverless)

### 3.5 `docs/7.*/README.md`

- Add admin deployment governance reference: `deploy/DEPLOYMENT_ARCHITECTURE.md`
- Add `s3storage` auth (S3S-0.1) as `7.x` release gate

### 3.6 `docs/8.*/README.md`

- Add `contact360.io/admin` to service coverage for 8.x (public/private API split needed ADM-8.1)
- Add `s3storage` and `logs.api` API maturity tasks

### 3.7 Era Task Pack Updates (per service, per era)

For each of the 11 analyzed services, update the relevant era task packs (in era folders 0–10) to include the specific task IDs from the analysis:

- Add `s3storage` task packs: S3S-0.x → 0.x era, S3S-1.x → 1.x era, etc.
- Add `logs.api` task packs: LOG-0.x → 0.x era, etc.
- Add `contact360.io/admin` task packs: ADM-0.x → 0.x era, etc.
- Add `emailapigo` task packs: EGO-0.x → 0.x era, etc.
- Add `emailapis` task packs: EPA-0.x → 0.x era, etc.

---

## Group 4 — Backend API Docs (docs/backend/apis/)

### 4.1 New files to create:

- `docs/backend/apis/ADMIN_ERA_TASK_PACKS.md` — era task packs for `contact360.io/admin` (ADM-0.1 through ADM-10.2)
- `docs/backend/apis/S3STORAGE_ERA_TASK_PACKS.md` — if not exists, create with S3S-0.1–5.4
- `docs/backend/apis/LOGSAPI_ERA_TASK_PACKS.md` — if not exists, create with LOG-0.1–4.4
- `docs/backend/apis/EMAILAPIGO_ERA_TASK_PACKS.md` — era task packs for `emailapigo` (EGO-0.1–3.4)

### 4.2 Existing files to update:

- `15_EMAIL_MODULE.md` — add mailvetter status vocab freeze note (MV-1), fix legacy route references
- `22_CAMPAIGNS_MODULE.md` — add EC-0.1 to EC-0.4 as blocking bugs; mark module as "incomplete" until P0s fixed
- `23_SALES_NAVIGATOR_MODULE.md` — add SN-0.1 docs drift note, mark routes as canonical
- `17_AI_CHATS_MODULE.md` — add contact.ai route drift note, remove `/api/v2` and `/gemini` stale refs

---

## Group 5 — Backend Database Docs (docs/backend/database/)

### 5.1 `docs/backend/database/emailcampaign_data_lineage.md`

- Add `templates` table (missing from schema — EC-0.1)
- Add `recipients.unsub_token` column (missing — EC-0.1)
- Add bug note: `GetUnsubToken` query uses `DB.Exec` instead of `DB.Get` (EC-0.2)

### 5.2 `docs/backend/database/logsapi_data_lineage.md`

- Replace MongoDB schema references with S3 CSV structure
- Document actual storage format: `logs/{service}/{YYYY}/{MM}/{DD}/logs.csv`
- Add: in-memory TTL cache pattern and stats aggregation fields

### 5.3 `docs/backend/database/s3storage_data_lineage.md`

- Add: `metadata.json` schema (bucket-level metadata object in S3)
- Add: multipart session state gap (in-memory `_MULTIPART_SESSIONS` — reliability risk)
- Add: object classification plan (S3S-2.1: `email_list`, `contact_import`, `campaign_asset`)

### 5.4 `docs/backend/database/admin_data_lineage.md` (new file)

- Document Django admin's databases: SQLite (dev), PostgreSQL (prod), Redis (cache/Django-Q)
- Document external data clients: appointment360 GraphQL, logs.api S3 CSV, tkdjob REST, s3storage REST
- Document auth state: JWT cookies, SuperAdmin cache in Redis

### 5.5 `docs/backend/database/emailapis_data_lineage.md`

- Add: PostgreSQL `email_patterns` and `email_finder_cache` schema
- Add: Redis TTL cache for external provider results
- Add: composite unique index requirement on cache identity (EPA-2.2)

---

## Group 6 — Backend Endpoint Era Matrix JSONs (docs/backend/endpoints/)

### 6.1 `s3storage_endpoint_era_matrix.json`

- Add actual endpoints from router: `/{bucket_id}/objects`, `/objects/info`, `/objects/download-url`, `/objects` (DELETE), `/initiate-csv`, `/{upload_id}/parts/{part_number}`, `/{upload_id}/complete`, `/{upload_id}/abort`, `/csv`, `/photo`, `/resume`, `/{bucket_id}/schema`, `/preview`, `/stats`, `/{bucket_id}`, `/{bucket_id}/{user_id}` (avatar)
- Map each endpoint to its era introduction and auth gap status

### 6.2 `logsapi_endpoint_era_matrix.json`

- Add actual endpoints: `POST /logs`, `POST /logs/batch`, `GET /logs`, `GET /logs/search`, `GET /logs/statistics`, `PUT /logs/{id}`, `DELETE /logs/{id}`, `DELETE /logs/bulk`
- Fix MongoDB reference to S3 CSV storage

### 6.3 `appointment360_endpoint_era_matrix.json`

- Add note for debug file write endpoints (AP-0.1): `jobs mutations`, `email queries`
- Mark rate limit enforcement as P1 gap for all mutation paths

### 6.4 `emailcampaign_endpoint_era_matrix.json` (create if missing)

- Document all campaign service endpoints: `POST /campaign`, `GET /campaigns`, `POST /templates`, `POST /schedule`, `POST /pause`, `GET /campaign/{id}`, `GET /unsub`
- Mark P0 bugs: EC-0.1, EC-0.2, EC-0.3, EC-0.4

### 6.5 Add new `admin_endpoint_era_matrix.json`

- Document all admin web routes and REST API v1 routes
- Mark permission levels per route (super_admin vs admin_or_super_admin vs public)

---

## Group 7 — Frontend Docs (docs/frontend/docs/)

### 7.1 New file: `docs/frontend/docs/admin-ui-bindings.md`

- Document Django admin template surface: billing panel, users panel, logs panel, jobs panel, storage panel
- Document API bindings: `admin_client.py` → GraphQL, `logs_api_client.py` → logs.api, `s3storage_client.py` → s3storage
- Document auth flow: JWT cookie → `Appointment360AuthMiddleware` → `SuperAdminMiddleware` → view
- Note: missing API key on `s3storage_client.py` headers (S3S-0.1 counterpart)

### 7.2 Update `docs/frontend/docs/s3storage-ui-bindings.md`

- Add: multipart upload flow (frontend perspective)
- Add: CSV schema/preview/stats endpoint bindings
- Note: no auth header currently sent from admin s3storage client

### 7.3 Update `docs/frontend/docs/logsapi-ui-bindings.md`

- Fix: replace any MongoDB query references with S3 CSV query API bindings
- Add: bulk delete, search, statistics endpoint bindings

### 7.4 Update `docs/frontend/docs/salesnavigator-ui-bindings.md`

- Add: scrape-and-save flow from extension popup → Lambda SN API → Connectra
- Note: CORS `*` risk for extension-originated requests

### 7.5 Update `docs/frontend/docs/emailapis-ui-bindings.md`

- Add: fallback chain visibility for UI (what status codes map to which fallback level)
- Add: bulk finder/verifier progress polling pattern

---

## Group 8 — Services API Docs (docs/backend/services.apis/)

### 8.1 Update `docs/backend/services.apis/contact.ai.api.md`

- Align to canonical routes: `/api/v1/ai-*` (utility) and `/api/v1/ai/*` (chat)
- Remove stale `/api/v2` and `/gemini` route references

### 8.2 Update `docs/backend/services.apis/mailvaiter.api.md`

- Alias canonical route: `/v1/*` only (mark legacy as deprecated)
- Add status vocabulary table: `pending → processing → completed → failed`

### 8.3 Update `docs/backend/services.apis/salesnavigator.api.md`

- Align docs to implemented routes: `/v1/scrape`, `/v1/save-profiles`, `/v1/health`
- Remove or mark documented-but-missing endpoint references as "planned"
- Add new `contact360.io/admin` service API doc

---

## Execution Priority (order of changes)

```
P0 (correctness/security truth):
  1. codebase analysis files (Group 2) — fix stale info, add gaps
  2. governance.md additions (Group 1.6) — admin, emailapigo, emailapis
  3. audit-compliance.md additions (Group 1.7)
  4. services.apis docs (Group 8) — fix stale routes

P1 (reference accuracy):
  5. architecture.md (Group 1.1)
  6. backend.md admin track (Group 1.3)
  7. roadmap.md admin stream (Group 1.4)
  8. versions.md blocking notes (Group 1.5)

P2 (database/endpoint truth):
  9. database data lineage files (Group 5)
  10. endpoint era matrix JSONs (Group 6)
  11. backend/apis module docs (Group 4)

P3 (era folders and task packs):
  12. Era README files 0–10 (Group 3.1–3.6)
  13. Era task pack files for admin, s3storage, logs.api, emailapigo, emailapis (Group 3.7)

P4 (frontend and flowcharts):
  14. flowchart.md new flows (Group 1.10)
  15. frontend.md admin surface (Group 1.11)
  16. frontend/docs UI binding files (Group 7)
```

---

## Key Files Modified Count

- Top-level docs: **11 files**
- Codebase analysis files: **10 files**
- Era READMEs and checklists: **~20 files**
- Era task packs (new/updated): **~55 files** (5 services × 11 eras)
- Backend API docs: **8 files** (4 new, 4 updated)
- Database lineage docs: **5 files** (1 new, 4 updated)
- Endpoint era matrices: **5 files** (1 new, 4 updated)
- Frontend docs: **5 files** (1 new, 4 updated)
- Services API docs: **4 files** (1 new, 3 updated)

**Total: ~124 files**