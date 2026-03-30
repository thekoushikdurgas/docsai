# DocsAI Sync Runbook

## Purpose

DocsAI uses hardcoded constants for architecture and roadmap views. This runbook defines mandatory sync rules between markdown docs and DocsAI constants.

## Sync rules

1. If `docs/docs/architecture.md` changes, update `contact360.io/admin/apps/architecture/constants.py` in the same change set.
2. If `docs/docs/roadmap.md` changes, update `contact360.io/admin/apps/roadmap/constants.py` in the same change set.
3. If **`docs/docs/backend-language-strategy.md`** changes, update any language/stack bullets mirrored in DocsAI architecture constants or internal admin copy in the same change set.
4. If release taxonomy/policy changes in `docs/docs/version-policy.md`, verify corresponding roadmap/version entries still match.
5. When the **canonical Go/EC2 service list** changes (new `EC2/*.server/` satellites, module paths, or migration inventory), update **`contact360.io/admin/apps/architecture/constants.py`** (`CONTACT360_PROJECT_STRUCTURE`, `CONTACT360_SERVICES`, and related tech bullets) in the same change set as **`docs/docs/architecture.md`**.
6. When **EC2 HTTP routes** change, update **`docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md`** and, on cutover, the matching **`docs/backend/endpoints/*_endpoint_era_matrix.json`** files.

## Update checklist

- Architecture updates:
  - Update folder/service names and descriptions in `docs/docs/architecture.md`.
  - Mirror those changes in `contact360.io/admin/apps/architecture/constants.py`.
  - Verify data-flow labels still match the architecture narrative.

- Roadmap updates:
  - Update stage details in `docs/docs/roadmap.md` (`status`, `depends_on`, `risk`, `definition_of_done`, `kpi`, `ships_in`).
  - Mirror stage additions/updates in `contact360.io/admin/apps/roadmap/constants.py`.
  - Ensure every stage still maps to a release in `docs/docs/versions.md`.

- Versioning updates:
  - Update policy in `docs/docs/version-policy.md` when versioning rules change.
  - Update release entries in `docs/docs/versions.md` with scope and stage mapping.
  - Confirm cross-links between roadmap and versions remain valid.

## Verification steps (DocsAI UI)

1. Open DocsAI architecture dashboard and confirm structure/service cards reflect the latest `constants.py`.
2. Open DocsAI roadmap dashboard and confirm stage list, statuses, and feature bullets match the roadmap constants.
3. Spot-check at least one updated stage from each of:
   - `1.x` user/billing/credit baseline,
   - `2.x` email system,
   - `3.x` contact and company data (Connectra),
   - `4.x` extension and Sales Navigator,
   - `5.x` AI workflows.
4. If mismatch appears, treat constants files as stale and re-sync before finalizing release docs.
5. For admin governance updates, verify the documented state of `settings_view` forms (placeholder vs wired) remains synchronized.
6. For reliability updates touching admin operations, keep migration status of `_analyze_jobs`, `_generate_json_jobs`, and `_upload_jobs` explicit (in-memory vs database; optional Redis only if `USE_REDIS_CACHE=True`).

## Release hygiene note

Do not ship docs-only version updates unless roadmap and DocsAI mirrors are synchronized.

## Deep sync workflow for staged execution

For every minor release stage (`X.Y.0`), process docs in this order:

1. Update `docs/roadmap.md` stage metadata and task bullets.
2. Mirror the same stage in `contact360.io/admin/apps/roadmap/constants.py`.
3. Add/update release record in `docs/versions.md` with `roadmap_mapping`.
4. If service ownership changes, update `docs/architecture.md` and its constants mirror.

## Small-task packet template (use per stage)

- **Task 1: Contract update**
  - Update stage or release contract text in markdown.
  - Mirror contract labels/fields in DocsAI constants.
- **Task 2: Ownership update**
  - Ensure `owner`, affected services, and UI surface are explicit.
  - Verify traceability row exists in roadmap.
- **Task 3: Verification update**
  - Confirm DocsAI page renders the new stage content.
  - Confirm release entry references the same stage id(s).

## Drift prevention rules

- No stage may be marked `completed` in docs unless constants are updated in the same change set.
- If roadmap stage ids change, update all `Roadmap mapping` references in `docs/versions.md`.
- Treat `docs/architecture.md` ownership tables as the canonical source for service responsibility.

## Governance era docs (supplementary)

Era-specific operational docs are indexed in `docs/governance.md` and enforced by `.github/workflows/ci.yml` (`test -f docs/...`). When you add a new governance-tracked doc:

1. Add the file under `docs/`.
2. Add a bullet to `docs/governance.md`.
3. Add `test -f "docs/<filename>"` to `.github/workflows/ci.yml`.
4. Append an entry to `CONTACT360_GOVERNANCE_DOC_INDEX` in `contact360.io/admin/apps/architecture/constants.py` so DocsAI can surface the path (optional but recommended for release hygiene).

## Extended docs sync scope

When extending docs beyond roadmap/constants, keep these files aligned:

- `docs/backend.md` with `docs/architecture.md` (service list, datastores, gateway pattern). Backend-only renames (lambda folder, health notes) should be reflected here without duplicating the full product architecture doc.
- `docs/frontend.md` with `docs/architecture.md` and `docs/codebase.md` when dashboard, marketing, DocsAI, extension, or email-app paths and ownership change (filename in-repo is `frontend.md`).
- If `contact360.io/email` route/security behavior changes, update `docs/codebases/email-codebase-analysis.md` in the same change set.
- Bulk/billing GraphQL and job-service contracts: keep `contact360.io/api/sql/apis/14_BILLING_MODULE.md`, `16_JOBS_MODULE.md`, and gateway code in sync; reflect release status in `docs/versions.md` and `docs/roadmap.md`.
- `docs/codebase.md` with `docs/architecture.md` repository and service naming.
- `docs/commands/*.md` with `docs/architecture.md`, `docs/governance.md`, and `docs/version-policy.md` when operational command contracts, service paths, or release cut practices change.
- `docs/frontend/README.md` / `docs/frontend/pages/README.md` with `docs/frontend.md` and `docs/version-policy.md` when page inventory or era-to-surface mapping changes.
- `docs/flowchart.md` with `docs/roadmap.md` stage flow and service sequence.
- `docs/versions/version_*.md` with `docs/versions.md` and `docs/roadmap.md` when a planned minor’s scope or owner changes.
- `docs/version-policy.md` planning rules with `docs/versions.md` entry format.
- Canonical path naming for extension and service folders (for example `extension/contact360360`, no stale `extention/*` aliases in active sections).
- **Service register:** `docs/architecture.md` → *Service register (canonical)* must match on-disk services (`contact360.io/*`, `lambda/*`, `backend(dev)/*` as applicable) and be mirrored in `contact360.io/admin/apps/architecture/constants.py` (`CONTACT360_PROJECT_STRUCTURE`, `CONTACT360_SERVICES`). When adding or removing a service row, update `docs/codebase.md`, `docs/flowchart.md`, and the *Feature-to-service traceability matrix* in `docs/roadmap.md` if that service appears there.
- **Release vs horizon:** If you change how majors `7.x`–`10.x` are described, align `docs/versions.md` (planning alignment blurb), `docs/roadmap.md`, `docs/architecture.md` (*Planning horizon*), and `docs/version-policy.md` (*Major themes*).
- **Version scheme canonical source:** `docs/version-policy.md` is the single source of truth for major era theme names. When an era is renamed, update `docs/roadmap.md` section headers, `docs/versions.md` release index, `docs/architecture.md` execution architecture table, `docs/flowchart.md` era strip, `docs/codebase.md` deep breakdown, and `docs/governance.md` version era summary — in that order.

## `s3storage` sync additions (mandatory for storage-related updates)

When storage behavior changes in `lambda/s3storage/`, keep these docs aligned in the same change set:

1. `docs/codebases/s3storage-codebase-analysis.md` (deep analysis + era task packs).
2. `docs/architecture.md` (`s3storage` role in execution architecture and service register).
3. `docs/roadmap.md` (stage-level storage implications, especially `2.4`, `6.6`, `8.x`, `10.x`).
4. `docs/versions.md` (release scope and owner mappings touching storage behavior).
5. `docs/flowchart.md` (multipart and metadata-worker flow updates when contract changes).

If storage contract changes affect APIs/endpoints, also update:

- `docs/backend/apis/07_S3_MODULE.md`
- `docs/backend/endpoints/*.json` entries for upload/download/multipart operations
- `docs/backend/postman/Storage_Backend_s3storage.postman_collection.json`

For any change to `docs/versions/version_*.md`, verify these sections are present and filled with concrete storage evidence (not placeholders):

- `Backend API and Endpoint Scope`
- `Database and Data Lineage Scope`
- `Frontend UX Surface Scope`


## Extended backend module sync additions

- add new backend module docs to sync checklist

## Extended sync checklist for inventory docs

When updating release/roadmap scopes, also verify:

1. `docs/backend/apis/*.md` module metadata (era, introduced_in, frontend binding, data stores touched).
2. `docs/backend/endpoints/*.json` endpoint metadata (`era`, `introduced_in`, `deprecated_in`, `frontend_page_bindings`, `db_tables_read`, `db_tables_write`, `auth_required`, `rbac_roles`, `rate_limited`).
3. `docs/frontend/pages/*.json` page metadata (`era`, `introduced_in`, tabs, UI element inventory, hooks/services/contexts, graphql bindings, flow identifiers).
4. `docs/versions/version_*.md` six mandatory scope/evidence sections are present and synced to roadmap and versions index.

## `logs.api` sync additions

- Any logs.api architecture/contract update must be mirrored in DocsAI architecture and roadmap constants when stage metadata or service ownership changes.
- Per-minor files `docs/versions/version_*.md` must include concrete logging evidence in backend/data/frontend scope blocks for logging-impacting minors.
- Docs reviews must validate that logs.api storage backend references remain S3 CSV (not MongoDB) unless code changes the backend implementation.

## Admin navigation/deploy/graph sync additions

When updating `contact360.io/admin` controls, synchronize these docs in the same change set.

### SIDEBAR_MENU sync rule

If `contact360.io/admin/apps/core/navigation.py` (`SIDEBAR_MENU`) changes:

1. Update `docs/frontend.md` (DocsAI admin surfaces section and navigation context).
2. Update `docs/codebases/admin-codebase-analysis.md` (navigation inventory).
3. Validate affected stage/era references in `docs/roadmap.md` and `docs/versions.md` if route ownership moved.

### Admin deployment sync rule

If any `contact360.io/admin/deploy/*.sh` behavior or usage changes:

1. Update `docs/governance.md` (Admin deployment governance section).
2. Update relevant release notes in `docs/versions.md` when deployment or runbook expectations change.
3. Re-verify DocsAI deployment references in this runbook.

### Admin graph viewer sync rule

If either graph component changes:

- `contact360.io/admin/static/js/components/relationship-graph-viewer.js`
- `contact360.io/admin/static/js/components/graph.js`

Then update:

1. `docs/frontend/components.md` (admin graph component catalog).
2. `docs/flowchart.md` (admin documentation dashboard and graph data-flow diagrams).
3. `docs/codebases/admin-codebase-analysis.md` (graph architecture notes).

## Email runtime sync rule

If `emailapis` / `emailapigo` contract behavior changes, update these docs in the same change set:

- `docs/codebases/emailapis-codebase-analysis.md`
- `docs/governance.md`
- `docs/backend/apis/15_EMAIL_MODULE.md`
- `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`

## Jobs runtime sync rule

If `contact360.io/jobs/` contract behavior changes, update these docs in the same change set:

- `docs/codebases/jobs-codebase-analysis.md`
- `docs/backend/apis/16_JOBS_MODULE.md`
- `docs/backend/apis/JOBS_ERA_TASK_PACKS.md`
- `docs/backend/database/jobs_data_lineage.md`
- `docs/frontend/jobs-ui-bindings.md`
- `docs/roadmap.md`, `docs/versions.md`, and `docs/architecture.md` where cross-era/service ownership is affected

DocsAI verification additions:

1. In DocsAI architecture view, verify TKD Job data ownership and flow text mirrors markdown.
2. In DocsAI roadmap view, verify jobs cross-era stream references are present for relevant eras.
3. Spot-check at least one jobs-linked stage in `2.x`, `3.x`, `6.x`, and `10.x`.

## Contact AI runtime sync rule

If `backend(dev)/contact.ai` contract behavior changes (routes, auth, model IDs, streaming format), update these docs in the same change set:

- `docs/codebases/contact-ai-codebase-analysis.md`
- `docs/backend/apis/17_AI_CHATS_MODULE.md`
- `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`
- `docs/backend/database/contact_ai_data_lineage.md`
- `docs/frontend/contact-ai-ui-bindings.md`
- `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`
- `docs/roadmap.md`, `docs/versions.md`, and `docs/architecture.md` where cross-era/service ownership is affected

If `ModelSelection` enum values change:

- Update `docs/backend/apis/17_AI_CHATS_MODULE.md` ModelSelection table.
- Update `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md` enum table.
- Update `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json` `model_selection_enum` field.
- Update `LambdaAIClient` mapping shim in `contact360.io/api/app/clients/lambda_ai_client.py`.

DocsAI verification additions for contact.ai:

1. In DocsAI architecture view, verify Contact AI data ownership and flow text mirrors `docs/architecture.md`.
2. In DocsAI roadmap view, verify contact.ai cross-era stream references are present for `5.x`, `6.x`, `8.x`, and `10.x`.
3. Spot-check AI chat features section in `5.x` era docs for alignment with `docs/codebases/contact-ai-codebase-analysis.md`.

---

## Extension sync rules

### Rule EXT-1 — Extension module paths
Any reference to extension auth, client, or merger modules must use the canonical path `extension/contact360/{auth|utils}/`:

- `extension/contact360/auth/graphqlSession.js`
- `extension/contact360/utils/lambdaClient.js`
- `extension/contact360/utils/profileMerger.js`

If documentation references `extention/` (old spelling) or different module paths, it must be updated to the canonical form above.

### Rule EXT-2 — Lambda SN API endpoint
All documentation of the profile save endpoint must use:
```
POST /v1/save-profiles
```
Do not document this as `/save-profiles`, `/profiles/save`, or any other variant without an explicit versioning note.

### Rule EXT-3 — Token storage keys
Documentation of token storage must always refer to the two canonical keys:

- `accessToken`
- `refreshToken`

Both keys must be documented as stored in `chrome.storage.local` (never `storage.sync`). If key names change in `graphqlSession.js`, the following docs must be updated in the same PR:

- `docs/codebases/extension-codebase-analysis.md`
- `docs/audit-compliance.md` (token audit section)
- `docs/governance.md` (token security rules)

### Rule EXT-4 — Extension era tagging
Extension contributions must be tagged with their primary era in all docs:

- Auth/token lifecycle → era `1.x`
- Profile capture and dedup → era `3.x`
- SN maturity and reliability patterns → era `4.x`
- API governance → era `8.x`

---

## Sales Navigator service sync rules

### Rule SN-1 — REST API contract drift
If any route in `backend(dev)/salesnavigator/app/api/v1/endpoints/` changes (added, renamed, removed), update these docs atomically in the same PR:

- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`
- `docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`
- `backend(dev)/salesnavigator/docs/api.md` (the service's own API reference)

### Rule SN-2 — Docs drift prevention
`docs/api.md` in the service repo must ONLY document routes that are actually implemented. If `POST /v1/scrape-html-with-fetch` is documented but not implemented, it must be removed from docs or implemented before the next release. This rule is a P0 gate for `4.x` release.

### Rule SN-3 — UUID contract
Any change to `generate_contact_uuid()` or `generate_company_uuid()` in `app/services/sales_navigator/utils.py` must update:

- `docs/backend/database/salesnavigator_data_lineage.md`
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md` (UUID generation section)

UUID contract changes are breaking — require migration evidence before production deployment.

### Rule SN-4 — Field mapping changes
Any change to `app/services/mappers.py` (new fields, renamed fields, seniority/department logic) must update:

- `docs/backend/database/salesnavigator_data_lineage.md` (field table)
- `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md` (field mapping section)

### Rule SN-5 — Era task pack sync
For every era task pack for `salesnavigator`, the corresponding era folder file must be consistent with `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`.

DocsAI verification additions for salesnavigator:

1. In DocsAI architecture view, verify Sales Navigator service is listed under `4.x` era services with correct path `backend(dev)/salesnavigator/`.
2. In DocsAI roadmap view, verify `4.x` stage mentions SN ingestion reliability and extension UX.
3. Verify `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md` has no undocumented gap between actual routes and documented routes.

---

## Email app sync rules

### Rule EMAIL-1 — Route inventory sync
When routes are added/renamed in `contact360.io/email/src/app/`, update:

- `docs/codebases/email-codebase-analysis.md`
- `docs/frontend.md`
- relevant era task-pack docs

### Rule EMAIL-2 — Endpoint contract sync
When fetch endpoints change in `contact360.io/email`, update:

- `docs/backend/endpoints/emailapp_endpoint_era_matrix.json`
- `docs/backend/database/emailapp_data_lineage.md`
- `docs/backend/apis/EMAILAPP_ERA_TASK_PACKS.md`

### Rule EMAIL-3 — Security sync
Any change to localStorage credential/session behavior in `imap-context.tsx` must update:

- `docs/audit-compliance.md`
- `docs/governance.md`
- `docs/codebases/email-codebase-analysis.md`

## Mailvetter service sync rules

### Rule MV-1 — API contract drift
If any route changes under `backend(dev)/mailvetter/app/mailvetter-bak/internal/api/` or handlers, update atomically in the same PR:

- `docs/codebases/mailvetter-codebase-analysis.md`
- `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`
- `docs/backend/postman/README.md` (mailvetter checklist)
- `docs/backend/apis/15_EMAIL_MODULE.md` (gateway verifier contract references)

### Rule MV-2 — Canonical path policy
`/v1/*` is canonical for all new consumers. Legacy `/verify|/upload|/status|/results` are compatibility-only and must be marked deprecated in docs.

### Rule MV-3 — Scoring contract sync
Any scoring/status change in `internal/validator/scoring.go` must update:

- `docs/codebases/mailvetter-codebase-analysis.md`
- `docs/backend/database/mailvetter_data_lineage.md`
- `docs/frontend.md` verifier status mapping section

### Rule MV-4 — Data schema sync
Any `jobs`/`results` schema change in `internal/store/db.go` must update:

- `docs/backend/database/mailvetter_data_lineage.md`
- `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`
- affected era task packs (`docs/0...10/mailvetter-*-task-pack.md`)

## Admin and service sync extensions

### Rule ADM-1 — Constants and canonical docs sync
Any material update to admin architecture/roadmap behavior must synchronize:

- `docs/architecture.md`
- `docs/roadmap.md`
- `contact360.io/admin/apps/architecture/constants.py`
- `contact360.io/admin/apps/roadmap/constants.py`

### Rule EGO-1 — Endpoint matrix sync
Any `lambda/emailapigo` endpoint contract change must update:

- `docs/backend/endpoints/emailapigo_endpoint_era_matrix.json`
- `docs/backend/apis/EMAILAPIGO_ERA_TASK_PACKS.md`
- related era task packs in `docs/0...10/`

### Rule S3S-1 — Multipart contract sync
Any multipart session/state contract update in `lambda/s3storage` must update:

- `docs/codebases/s3storage-codebase-analysis.md`
- `docs/backend/database/s3storage_data_lineage.md`
- `docs/backend/endpoints/s3storage_endpoint_era_matrix.json`

### Rule LOG-1 — Storage contract sync
Any logs storage contract update in `lambda/logs.api` must update:

- `docs/codebases/logsapi-codebase-analysis.md`
- `docs/backend/database/logsapi_data_lineage.md`
- `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`


## AI Workspace Logs & Sync Activity

- [Cursor Documentation File Ex](analysis/cursor_contact360_documentation_file_ex.md)
- [Cursor Directory Exploration](analysis/cursor_directory_exploration_and_file_c.md)
- [Cursor Content Retrieval 1](analysis/cursor_documentation_content_retrieval1.md)
- [Cursor Content Retrieval](analysis/cursor_documentation_file_content_retri.md)
- [Cursor Folder Exploration](analysis/cursor_documentation_folder_exploration.md)
- [Cursor Structure Exploration](analysis/cursor_documentation_structure_explorat.md)
- [Cursor File Content & Label](analysis/cursor_file_content_retrieval_and_label.md)
