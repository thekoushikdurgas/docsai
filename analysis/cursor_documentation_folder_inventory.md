# Documentation folder inventory
_Exported on 3/24/2026 at 20:13:41 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Explore the docs folder at d:\code\ayan\contact\docs and produce a COMPLETE inventory. I need:

1. List every file in every subfolder (by folder)
2. Identify duplicated file name patterns (e.g. same service appearing in multiple era folders)
3. List what is inside docs/ideas, docs/media, docs/codebases, docs/frontend, docs/backend subfolders - list every file
4. Count how many files total per era folder (0 through 10)
5. List the root-level .md files (architecture.md, backend.md, etc.)
6. Flag any files that look orphaned or have near-duplicate names

Be very thorough. List every filename you find.

---

**Cursor**


Exploring `d:\code\ayan\contact\docs` with glob searches and directory listings to build a complete inventory.




Listing directories and scanning for non-markdown files.




Gathering top-level structure, per-era file counts, and full listings for manageable folders.




Splitting `media` into subfolders for complete file lists and counting `ideas` files (excluding `.git`).




Here is the inventory from read-only scans of `d:\code\ayan\contact\docs` (glob + grep). Totals come from tool output; a few very large trees are summarized where the tool returned a total count plus truncation.

---

## Overall size

| Scope | File count (approx.) |
|--------|----------------------|
| **Entire `docs/`** (pattern `*.*`) | **4793** |
| **`docs/backend/postman/`** alone | **3134** |
| **`docs/ideas/`** (includes nested `.git` and code) | **606** |
| **`docs/media/`** | **586** |
| **`docs/backend/`** (apis + database + endpoints + postman) | **3424** |

---

## 5. Root-level files in `d:\code\ayan\contact\docs` (direct children)

These are the **`.md` files at the root of `docs/`** (not inside subfolders), as returned by search:

- `architecture.md`
- `audit-compliance.md`
- `backend.md`
- `codebase.md`
- `docsai-sync.md`
- `flowchart.md`
- `frontent.md` (typo — see near-duplicates below)
- `governance.md`
- `roadmap.md`
- `versions.md`
- `VERSION Contact360.md` (note space in filename)

---

## 4. Files per era folder (0–10)

| Era | Folder | Count |
|-----|--------|------:|
| **0** | `0. Foundation and pre-product stabilization and codebase setup` | **21** |
| **1** | `1.  Contact360 user and billing and credit system` (two spaces after `1.`) | **23** |
| **2** | `2. Contact360 email system` | **33** |
| **3** | `3. Contact360 contact and company data system` | **26** |
| **4** | `4. Contact360 Extension and Sales Navigator maturity` | **25** |
| **5** | `5. Contact360 AI workflows` | **23** |
| **6** | `6. Contact360 Reliability and Scaling` | **21** |
| **7** | `7. Contact360 deployment` | **22** |
| **8** | `8. Contact360 public and private apis and endpotints` | **25** |
| **9** | `9. Contact360 Ecosystem integrations and Platform productization` | **29** |
| **10** | `10. Contact360 email campaign` | **27** |
| | **Sum (era folders only)** | **275** |

---

## 2. Duplicated filename patterns (cross-era / services)

Across eras **0–10**, the same **naming patterns** repeat for each product line:

- **`*-<area>-task-pack.md`** with prefixes: 
  `mailvetter-`, `appointment360-`, `salesnavigator-`, `connectra-`, `emailcampaign-`, `contact-ai-`, `jobs-`, `emailapis-`, `logsapi-`, `s3storage-`  
  (exact middle segment varies by era, e.g. `foundation`, `user-billing`, `email-system`, `public-private-apis`, `ecosystem-productization`, etc.)

- **`version_<era>.<minor>.md`** — e.g. `0.0 — Pre-repo baseline.md` … `0.10 — Ship & ops hardening.md` in era 0; `1.0 — User Genesis.md` … `1.10 — Billing and User Ops Exit Gate.md` in era 1; same idea for eras 2–10.

- **`backend/database/*_data_lineage.md`** — one per service (`mailvetter`, `emailapp`, `salesnavigator`, `appointment360`, `emailcampaign`, `contact_ai`, `jobs`, `connectra`, `emailapis`, `logsapi`, `s3storage`).

- **`backend/apis/*_ERA_TASK_PACKS.md`** and **`backend/endpoints/*_endpoint_era_matrix.json`** — same multi-service pattern.

- **`backend/apis/NN_*_MODULE.md`** — numbered module docs (`01_AUTH_MODULE.md` … `29_RESUME_AI_REST_SERVICE.md`).

So duplication is **by design** (matrix of **era × service**), not accidental copies in one folder.

---

## 3 & 1. `docs/codebases` — every file (16)

Path prefix: `d:\code\ayan\contact\docs\codebases\`

- `README.md`
- `admin-codebase-analysis.md`
- `app-codebase-analysis.md`
- `appointment360-codebase-analysis.md`
- `connectra-codebase-analysis.md`
- `contact-ai-codebase-analysis.md`
- `email-codebase-analysis.md`
- `emailapis-codebase-analysis.md`
- `emailcampaign-codebase-analysis.md`
- `extension-codebase-analysis.md`
- `jobs-codebase-analysis.md`
- `logsapi-codebase-analysis.md`
- `mailvetter-codebase-analysis.md`
- `root-codebase-analysis.md`
- `s3storage-codebase-analysis.md`
- `salesnavigator-codebase-analysis.md`

---

## `docs/frontend` — every file (65)

Path prefix: `d:\code\ayan\contact\docs\frontend\`

**Markdown**

- `README.md`
- `components.md`
- `contact-ai-ui-bindings.md`
- `design-system.md`
- `emailapis-ui-bindings.md`
- `hooks-services-contexts.md`
- `jobs-ui-bindings.md`
- `logsapi-ui-bindings.md`
- `s3storage-ui-bindings.md`
- `salesnavigator-ui-bindings.md`

**`frontend/excel/`**

- `README.md`
- `pages_export_2026-03-15 (6) - Dashboard.csv`
- `pages_export_2026-03-15 (6) - Docs.csv`
- `pages_export_2026-03-15 (6) - Marketing.csv`
- `pages_export_2026-03-15 (6) - Product.csv`
- `pages_export_2026-03-15 (6) - Title.csv`

**`frontend/pages/`** — `README.md`, `index.json`, `pages_index.json`, and these `*_page.json` files:

`about_page.json`, `activities_page.json`, `admin_page.json`, `ai_chat_page.json`, `ai_email_writer_page.json`, `analytics_page.json`, `api_docs_page.json`, `billing_page.json`, `campaign_builder_page.json`, `campaign_templates_page.json`, `campaigns_page.json`, `careers_page.json`, `cfo_email_list_page.json`, `chrome_extension_page.json`, `companies_page.json`, `contacts_page.json`, `dashboard_page.json`, `dashboard_pageid_page.json`, `deployment_page.json`, `docs_page.json`, `docs_pageid_page.json`, `email_finder_page.json`, `email_page.json`, `email_verifier_page.json`, `export_page.json`, `files_page.json`, `finder_page.json`, `integrations_page.json`, `jobs_page.json`, `landing_page.json`, `linkedin_page.json`, `live_voice_page.json`, `login_page.json`, `privacy_page.json`, `profile_page.json`, `prospect_finder_page.json`, `refund_page.json`, `register_page.json`, `root_page.json`, `sequences_page.json`, `settings_page.json`, `status_page.json`, `terms_page.json`, `ui_page.json`, `usage_page.json`, `verifier_page.json`

---

## `docs/backend` — by subfolder

### `backend/apis` (38 files) — full list

`README.md`, `MAILVETTER_ERA_TASK_PACKS.md`, `EMAILAPP_ERA_TASK_PACKS.md`, `SALESNAVIGATOR_ERA_TASK_PACKS.md`, `23_SALES_NAVIGATOR_MODULE.md`, `APPOINTMENT360_ERA_TASK_PACKS.md`, `CONTACT_AI_ERA_TASK_PACKS.md`, `25_CAMPAIGN_TEMPLATES_MODULE.md`, `24_SEQUENCES_MODULE.md`, `22_CAMPAIGNS_MODULE.md`, `17_AI_CHATS_MODULE.md`, `15_EMAIL_MODULE.md`, `16_JOBS_MODULE.md`, `JOBS_ERA_TASK_PACKS.md`, `03_CONTACTS_MODULE.md`, `04_COMPANIES_MODULE.md`, `EMAILAPIS_ERA_TASK_PACKS.md`, `LOGSAPI_ERA_TASK_PACKS.md`, `S3STORAGE_ERA_TASK_PACKS.md`, `28_PROFILE_MODULE.md`, `29_RESUME_AI_REST_SERVICE.md`, `27_TWO_FACTOR_MODULE.md`, `26_SAVED_SEARCHES_MODULE.md`, `21_LINKEDIN_MODULE.md`, `20_INTEGRATIONS_MODULE.md`, `19_PAGES_MODULE.md`, `18_ANALYTICS_MODULE.md`, `14_BILLING_MODULE.md`, `13_ADMIN_MODULE.md`, `10_UPLOAD_MODULE.md`, `09_USAGE_MODULE.md`, `11_ACTIVITIES_MODULE.md`, `08_HEALTH_MODULE.md`, `07_S3_MODULE.md`, `05_NOTIFICATIONS_MODULE.md`, `06_WEBHOOKS_MODULE.md`, `02_USERS_MODULE.md`, `01_AUTH_MODULE.md`

### `backend/database` (55 files)

**Root:** `README.md`, `mailvetter_data_lineage.md`, `emailapp_data_lineage.md`, `salesnavigator_data_lineage.md`, `appointment360_data_lineage.md`, `emailcampaign_data_lineage.md`, `contact_ai_data_lineage.md`, `jobs_data_lineage.md`, `connectra_data_lineage.md`, `emailapis_data_lineage.md`, `logsapi_data_lineage.md`, `s3storage_data_lineage.md`

**`database/migrations/`:** `add_ai_chats.sql`, `expand_resume_json_schema_education_certificates.sql`, `add_resume_documents.sql`, `migrate_resume_documents_to_s3_keys.sql`, `add_payment_settings_qr_bucket.sql`

**`database/tables/`:** `README.md`, `enums.sql`, `integrations.sql`, `webhooks.sql`, `campaign_templates.sql`, `campaign_sequences.sql`, `campaigns.sql`, `ai_chats.sql`, `init_schema.sql`, `resume_documents.sql`, `payment_settings.sql`, `user_profiles.sql`, `addon_packages.sql`, `payment_submissions.sql`, `subscription_plan_periods.sql`, `users.sql`, `scheduler_jobs.sql`, `user_scraping.sql`, `notifications.sql`, `saved_searches.sql`, `team_members.sql`, `two_factor.sql`, `api_keys.sql`, `sessions.sql`, `extensions.sql`, `user_activities.sql`, `performance_metrics.sql`, `token_blacklist.sql`, `subscription_plans.sql`, `feature_usage.sql`, `user_history.sql`

**`database/table_data/`:** `README.md`, `user.sql`, `user_profiles.csv`, `billings_inserts.sql`, `subscription_plans.csv`, `subscription_plan_periods.csv`, `addon_packages.csv`

### `backend/endpoints` (197 files)

All are `*.json`. Tool output listed **197 paths**; the set includes:

- Index/matrix: `endpoints_index.json`, `index.json`, `mailvetter_endpoint_era_matrix.json`, `emailapp_endpoint_era_matrix.json`, `appointment360_endpoint_era_matrix.json`, `salesnavigator_endpoint_era_matrix.json`, `emailcampaign_endpoint_era_matrix.json`, `contact_ai_endpoint_era_matrix.json`, `jobs_endpoint_era_matrix.json`, `connectra_endpoint_era_matrix.json`, `emailapis_endpoint_era_matrix.json`, `logsapi_endpoint_era_matrix.json`, `s3storage_endpoint_era_matrix.json`
- REST samples: `mutation_create_template_rest.json`, `mutation_create_campaign_rest.json`, `get_unsub_rest.json`
- Many `query_*_graphql.json`, `mutation_*_graphql.json`, `get_*_graphql.json`, `list_*_graphql.json`, `count_*_graphql.json` — full enumeration is in the workspace grep result for `docs\backend\endpoints\*.json` (197 files).

### `backend/postman` (3134 files)

**Not listed filename-by-filename here** — the index reports **3134** files. Contents include, among others:

- Root: `README.md`, `Email_Runtime_emailapis_emailapigo.postman_collection.json`, `Contact AI Service.postman_collection.json`
- `Resume AI Service1\auth.json`, `Resume AI Service1\vars.json`
- Folders such as `Email Campaign API\`, `Connectra API\`, `Contact360 GraphQL API - Complete\`, plus many third-party-style folders (e.g. names starting with `📌` for xAI, Together AI, etc.)

---

## `docs/media` (586 files) — structure + full list where small

**Root (`docs/media/`):**

- `DASHBOARD_ALIGNMENT.md`
- `ENDPOINTS_AUDIT.md`
- `MEDIA_CONVENTIONS.md`
- `TASK_BREAKDOWN.md`

**`media/json/models` path in search:** `json_models\pages_json_models.md`

**`media/relationship/`:** `index.json`, `relationships_index.json`

**`media/relationship/by-page/` (72 files)** — includes pairs like `about.json` / `about_result.json`, `billing.json` / `billing_result.json`, … through page-specific and admin JSON files (full list appeared in the glob for that folder).

**`media/relationship/by-endpoint/` (102 files)** — `graphql_*_QUERY.json` / `graphql_*_MUTATION.json` for many operations (glob reported 102 files total; first chunk listed ~65, remainder truncated in UI).

**`media/result/` (364 files)** — under `result/postman/` (exported `*_result.json` Postman-related files) and `result/relationship/` (parallel `*_result.json` to relationship analyses).

The remaining **586** total is consistent with: root (4) + json_models (1) + relationship indexes (2) + by-page (72) + by-endpoint (102) + result (364) + any overlap/adjustment from full tree.

---

## `docs/ideas` (606 files)

**Not a flat doc set** — it contains **nested repositories and application code**, including **`.git` directories** (objects, hooks, refs, etc.).

**Top-level areas (from glob):**

- **`ideas/mailvetter/` (231 files)** — includes full `.git` and `emailapis/` tree (e.g. Go under `emailapis/app/mailvetter-bak/...`, Postman JSON, `MAILVAITER_QUICKSTART.md`, `mailvaiter-api-docs.md` — note **Mailvaiter** spelling).
- **`ideas/resume/` (363 files)** — multiple subprojects (`resume-analyzer`, `ai-resume-editor`, `Resume-Roaster`, `Resume_Screening-System`, …), each with their own `.git` and source files (`.py`, `.ts`, `.ipynb`, etc.).

A **complete filename list for all 606 paths** is too long for one message; the scanner reported **606** paths under `docs/ideas` with `**/*`.

---

## 1. Other top-level folders under `docs/` (besides eras and the five you named)

From searches, the main **named** subtrees are:

- Era folders `0.` … `10.`
- `backend/`, `codebases/`, `frontend/`, `media/`, `ideas/`

Plus **root** markdown files listed in section 5.

---

## 6. Orphaned or suspicious / near-duplicate names

**Likely “orphaned” or odd placement**

- **`docs/ideas/`** — embedded **git repos and runtime code**; this is **not** like the rest of `docs/` (specs and analysis). Looks like **vendored or copied projects**, not first-class documentation.
- **Era 2** — many **`cursor_*.md`** files (`cursor_email_system_*`, `cursor_mail_vetter_*`, …): read like **one-off Cursor session exports** next to formal `email_system.md` / task packs.
- **Era 8 folder name:** `... endpotints` — typo for **endpoints**.

**Near-duplicates / confusion**

- **`frontent.md`** (root) vs **`frontend/`** directory — typo; overlaps conceptually with `docs/frontend/`.
- **`codebase.md`** (root) vs **`codebases/`** — same topic, two places.
- **`versions.md`** vs **`VERSION Contact360.md`** — both version-related at root.
- **`index.json`** and **`endpoints_index.json`** in `backend/endpoints/` — related indexing; worth checking whether both are maintained.
- **`media/relationship/...`** vs **`media/result/relationship/...`** — parallel `graphql_*` and `*_result.json` naming (intentional “source vs result” pairing).
- **`ideas/.../huggingfaceService.ts`** appears under **`src/services/`** and **`services/`** in `ai-resume-editor` — duplicate path pattern.
- **Spelling:** **Mailvaiter** / **mailvaiter** in `ideas/mailvetter/emailapis/docs/` vs **Mailvetter** elsewhere.

---

## Era folders — complete file lists (275 files)

Below, paths are under `d:\code\ayan\contact\docs\`. Only the **folder name** is repeated; filenames are complete per era.

### Era 0 (21)

`appointment360-foundation-task-pack.md`, `connectra-foundation-task-pack.md`, `contact-ai-foundation-task-pack.md`, `emailapis-foundation-task-pack.md`, `emailcampaign-foundation-task-pack.md`, `jobs-foundation-task-pack.md`, `logsapi-foundation-task-pack.md`, `mailvetter-foundation-task-pack.md`, `s3storage-foundation-task-pack.md`, `salesnavigator-foundation-task-pack.md`, `0.0 — Pre-repo baseline.md`, `0.1 — Monorepo bootstrap.md`, `0.2 — Schema & migration bedrock.md`, `0.3 — Service mesh contracts.md`, `0.4 — Identity & RBAC freeze.md`, `0.5 — Object storage plane.md`, `0.6 — Async job spine.md`, `0.7 — Search & dual-write substrate.md`, `0.8 — UX shell & docs mirror.md`, `0.9 — Extension channel scaffold.md`, `0.10 — Ship & ops hardening.md`

### Era 1 (23)

`appointment360-user-billing-task-pack.md`, `connectra-user-billing-task-pack.md`, `contact-ai-user-billing-task-pack.md`, `dashboard-search-ux.md`, `emailapis-user-billing-credit-task-pack.md`, `emailcampaign-user-billing-task-pack.md`, `jobs-user-billing-task-pack.md`, `logsapi-user-billing-credit-task-pack.md`, `mailvetter-user-billing-task-pack.md`, `rbac-authz.md`, `s3storage-user-billing-task-pack.md`, `salesnavigator-user-billing-task-pack.md`, `1.0 — User Genesis.md`, `1.1 — Billing Maturity.md`, `1.2 — Analytics Bedrock.md`, `1.3 — Payment Gateway.md`, `1.4 — Usage Ledger.md`, `1.5 — Notification Rail.md`, `1.6 — Admin Control Plane.md`, `1.7 — Security Hardening.md`, `1.8 — Credit Pack Maturity.md`, `1.9 — Identity and Session Hardening.md`, `1.10 — Billing and User Ops Exit Gate.md` (full set: `version_1.0` through `version_1.10`)

### Era 2 (33)

Task packs: `appointment360-`, `connectra-`, `contact-ai-`, `emailapis-`, `emailcampaign-`, `jobs-`, `logsapi-`, `mailvetter-`, `s3storage-`, `salesnavigator-` + `email-system-task-pack.md` (and `emailapis` / `logsapi` / `s3storage` variants as listed in glob).

Plus: `cursor_email_api_system_exploration.md`, `cursor_email_apis_exploration_and_analy.md`, `cursor_email_architecture_and_behavior.md`, `cursor_email_system_architecture_explor.md`, `cursor_email_system_architecture_explor1.md`, `cursor_email_system_exploration_in_admi.md`, `cursor_email_system_exploration_in_mono.md`, `cursor_email_system_exploration_in_mono1.md`, `cursor_email_system_version_docs_enrich.md`, `cursor_contact360_email_integration_exp.md`, `cursor_mail_vetter_codebase_exploration.md`, `email_system.md`, `2.0 — Email Foundation.md`, `2.1 — Finder Engine.md`, … `2.10 — Email System Exit Gate.md`

### Era 3 (26)

Task packs for all services above + `connectra-service.md`, `connectors-commercial.md`, `enrichment-dedup.md`, `vql-filter-taxonomy.md`, `webhooks-replay.md`, `3.0 — Twin Ledger.md`, `3.1 — VQL Engine.md`, … `3.10 — Data Completeness.md`

### Era 4 (25)

All `*-extension-sn-task-pack.md` / `*-extension-salesnav-task-pack.md` variants + `extension-auth.md`, `extension-sync-integrity.md`, `extension-telemetry.md`, `sales-navigator-ingestion.md`, `4.0 — Harbor.md` … `4.10 — Exit Gate.md`

### Era 5 (23)

Task packs + `ai-cost-governance.md`, `ai-workflows.md`, `5.0 — Neural Spine.md` … `5.10 — Connectra Intelligence.md`

### Era 6 (21)

Task packs + `6.0 — Reliability and Scaling era umbrella.md` … `6.10 — Buffer - placeholder minor within the 6x reliability era.md`

### Era 7 (22)

Task packs + `tenant-security-observability.md`, `7.0 — Deployment era baseline lock.md` … `7.10 — Deployment overflow patch buffer inside era 7.md`

### Era 8 (25)

Task packs + `appointment360-api-endpoint-task-pack.md`, `appointment360-service.md`, `mailvetter-public-private-apis-task-pack.md`, `mailvetter-service.md`, `public-api-surface.md`, `slo-idempotency.md`, `8.0 — API Era Foundation.md` … `8.10 — API Era Buffer.md`

### Era 9 (29)

Task packs + `analytics-era-rc.md`, `analytics-platform.md`, `integration-era-rc.md`, `integration-partner-governance.md`, `performance-storage-abuse.md`, `platform-productization.md`, `queue-observability.md`, `reliability-rc-hardening.md`, `9.0 — Ecosystem Foundation.md` … `9.10 — Productization Buffer.md`

### Era 10 (27)

Task packs + `campaign-commercial-compliance.md`, `campaign-deliverability.md`, `campaign-execution-engine.md`, `campaign-foundation.md`, `campaign-observability-release.md`, `emailcampaign-service.md`, `10.0 — Campaign Bedrock.md` … `10.10 — Placeholder Policy.md`

---

### Note on “every filename” for the largest trees

- **`backend/postman` (3134)** and **`ideas` (606)** — tools return **complete counts** but **truncate long file lists** in the UI.
- For **`media/relationship/by-endpoint`** (102 files) and **`media/result`** (364 files), partial lists were shown; the totals **586** / **102** / **364** are from glob totals.

If you need a **machine-readable full path list** for `postman`, `ideas`, or `media`, run locally (e.g. `Get-ChildItem -Recurse -File` in PowerShell) or switch to Agent mode and ask for an export script — in **Ask mode** I cannot run commands or write files.

