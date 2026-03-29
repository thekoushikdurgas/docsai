# SQL and API Documentation

This directory contains database schema, API documentation, and Postman collections for the Appointment360 backend.

## Folder reality snapshot

- Includes service lineage docs for appointment360, connectra, jobs, emailapis, contact_ai, emailcampaign, salesnavigator, mailvetter, s3storage, logsapi, admin, and emailapp.
- Includes supporting `tables/` and `table_data/` READMEs for schema and seed guidance.
- This folder is the primary source for data ownership and cross-service lineage checks.

## Structure

| Directory | Description |
|-----------|-------------|
| **apis/** | GraphQL module documentation (Contacts, Companies, Health, Jobs, etc.) |
| **postman/** | Postman collections for Contact360 and Connectra GraphQL APIs |
| **tables/** | PostgreSQL schema (tables, enums, extensions) |
| **table_data/** | Seed data scripts (e.g., billing plans) |
| **migrations/** | One-off SQL migrations for existing environments (additive / idempotent where noted) |

## Quick References

- **Backend docs hub**: [../README.md](../README.md) — includes **codebase analysis registry** linking each `docs/codebases/*-codebase-analysis.md` to lineage files here.
- **GraphQL modules**: [apis/README.md](apis/README.md)
- **Connectra integration**: [apis/03_CONTACTS_MODULE.md](apis/03_CONTACTS_MODULE.md), [apis/04_COMPANIES_MODULE.md](apis/04_COMPANIES_MODULE.md)
- **Postman setup**: [postman/README.md](postman/README.md)
- **Database schema**: [tables/README.md](tables/README.md) — includes `resume_documents` (resumeai) and `ai_chats` (contact.ai) on the shared PostgreSQL database used by appointment360.
- **Connectra lineage**: [connectra_data_lineage.md](connectra_data_lineage.md) — hybrid PG+ES lineage for contacts/companies/filter facets/jobs.
- **Contact AI (microservice)**: `backend(dev)/contact.ai` — FastAPI Lambda; persists chats in **`ai_chats`** (`user_id` → `users.uuid`, `messages` JSONB). DDL: [tables/ai_chats.sql](tables/ai_chats.sql). Optional additive migration: [migrations/add_ai_chats.sql](migrations/add_ai_chats.sql). Postman: `docs/media/postman/Contact AI Service.postman_collection.json`.
- **Resume AI REST (microservice)**: [apis/29_RESUME_AI_REST_SERVICE.md](../apis/29_RESUME_AI_REST_SERVICE.md) — HTTP API and Postman under `backend(dev)/resumeai/postman/`.
- **Email module**: [apis/15_EMAIL_MODULE.md](apis/15_EMAIL_MODULE.md) – finder/verification (queries) and pattern add (mutations) via Lambda Email API; job-based exports via Jobs module.
- **Jobs module**: [apis/16_JOBS_MODULE.md](apis/16_JOBS_MODULE.md) – scheduler jobs (Tkdjob): create, list, retry; live status/timeline/DAG via `statusPayload`, `timelinePayload`, `dagPayload`.
- **Storage & files**: [apis/07_S3_MODULE.md](apis/07_S3_MODULE.md), [apis/10_UPLOAD_MODULE.md](apis/10_UPLOAD_MODULE.md) – per-user logical buckets via the `s3storage` service (CSV listing, preview, schema, multipart uploads, avatars). Within each logical bucket (`users.bucket`), objects are stored under standard prefixes such as `avatar/`, `upload/`, `photo/`, `resume/`, and `export/`.

## `s3storage` database and lineage notes by era

- `2.x`: bulk upload metadata and file lineage must remain consistent with job orchestration.
- `3.x`: ingestion/export lineage should map storage artifacts to search/enrichment workflows.
- `6.x`: reconciliation checks are required between object storage and metadata state.
- `7.x`+: retention/deletion policy evidence must be available for compliance.
- `10.x`: campaign artifact lineage should support reproducible compliance audits.

Deep reference: [s3storage-codebase-analysis.md](../../codebases/s3storage-codebase-analysis.md).

## Connectra Configuration

- **CONNECTRA_BASE_URL**: Typically `http://host:8080` (Connectra runs on port 8080)
- **CONNECTRA_API_KEY**: Required for Connectra REST API
- Contact queries with denormalized company columns use `company_config.populate` (see [03_CONTACTS_MODULE.md](apis/03_CONTACTS_MODULE.md))

## `connectra` database and lineage notes by era

- `0.x`: bootstrap health/auth/index contract baseline.
- `1.x`: credit and billing usage linkage for heavy query/export paths.
- `2.x`: CSV/job orchestration lineage across import/export flows.
- `3.x`: VQL + dual-store contract (`contacts`, `companies`, `filters`, `filters_data`, `contacts_index`, `companies_index`).
- `4.x`: extension/SN provenance and idempotent upsert lineage.
- `5.x`: AI-readable field exposure and confidence lineage.
- `6.x`: SLO/retry/reconciliation evidence and drift checks.
- `7.x`+: authz/audit/tenant isolation lineage.
- `10.x`: audience/suppression compliance lineage.

Deep reference: [connectra_data_lineage.md](connectra_data_lineage.md).  
Runtime + gap map: [sync-codebase-analysis.md](../../codebases/sync-codebase-analysis.md), [connectra-codebase-analysis.md](../../codebases/connectra-codebase-analysis.md).

## `logs.api` database and lineage notes by era

- logs.api runtime store is S3 CSV objects, not MongoDB.
- Retention and lineage evidence should reference [logsapi_data_lineage.md](logsapi_data_lineage.md).
- Per-era release docs must include logs data-lineage scope when impacted.

Deep reference: [logsapi_data_lineage.md](logsapi_data_lineage.md).  
Runtime + gap map: [logsapi-codebase-analysis.md](../../codebases/logsapi-codebase-analysis.md).

## `emailapis` database and lineage notes by era

- `1.x`: credit-impact traceability for finder/verification requests.
- `2.x`: cache/pattern lineage and bulk job result consistency.
- `3.x`: contact/company enrichment linkage to email identity keys.
- `6.x`: reliability evidence for retries, fallback, and status drift.
- `7.x`+: deployment/audit evidence and retention governance.
- `10.x`: campaign compliance lineage and reproducibility evidence.

Deep reference: [emailapis_data_lineage.md](emailapis_data_lineage.md).  
Runtime + gap map: [emailapis-codebase-analysis.md](../../codebases/emailapis-codebase-analysis.md).

## `jobs` service database and lineage notes by era

- `0.x`: establish `job_node`/`edges`/`job_events` schema and lifecycle status invariants.
- `1.x`: billing/credit traceability in job creation and retry events.
- `2.x`: email bulk stream lineage (`input CSV -> processing checkpoints -> output CSV`).
- `3.x`: Contact360 import/export lineage across scheduler DB, Contact360 Postgres, and OpenSearch.
- `4.x`: extension/SN provenance fields for ingestion-origin jobs.
- `5.x`: AI batch metadata lineage (`model`, `confidence`, `cost`) in `job_response`.
- `6.x`: reliability lineage (idempotency keys, retry reasons, stale recovery evidence).
- `7.x`+: role-aware access, retention, and audit evidence from timeline events.
- `10.x`: campaign compliance evidence bundles from immutable job timelines.

Deep reference: [jobs_data_lineage.md](jobs_data_lineage.md).  
Runtime + gap map: [jobs-codebase-analysis.md](../../codebases/jobs-codebase-analysis.md).

## `contact.ai` service database and lineage notes by era

- `0.x`: `ai_chats` DDL baseline and optional additive migration (`add_ai_chats.sql`); FK to `users.uuid`.
- `1.x`: user-deletion cascade strategy defined; `user_id` referential integrity validated.
- `2.x`: email PII in `analyzeEmailRisk` utility calls — stateless, no DB write; HF data retention reviewed.
- `3.x`: `messages.contacts[]` JSONB sub-schema aligned with Connectra contact index; `parseContactFilters` output is stateless.
- `4.x`: SN contact provenance optionally tagged in `messages.contacts[]` JSONB.
- `5.x`: full `ai_chats` table in production; `model_version` field in message metadata for reproducibility; 100-message cap enforced.
- `6.x`: `version` column on `ai_chats` for optimistic concurrency; TTL archival policy; `updated_at` atomicity.
- `7.x`+: GDPR erasure cascade; audit log emissions to `logs.api`; retention policy documented.
- `9.x`: webhook delivery log and connector audit trail referencing `ai_chats.uuid`.
- `10.x`: `campaign_ai_log` table for campaign AI generation compliance evidence (separate from `ai_chats`).

Deep reference: [contact_ai_data_lineage.md](contact_ai_data_lineage.md).  
Runtime + gap map: [contact-ai-codebase-analysis.md](../../codebases/contact-ai-codebase-analysis.md).

## `email campaign` service database and lineage notes by era

The email campaign service maintains its own isolated PostgreSQL instance separate from the Appointment360/Connectra shared database. Tables: `campaigns`, `recipients`, `suppression_list`, `templates`. Template HTML bodies stored in S3.

- `0.x`: Bootstrap `campaigns`, `recipients`, `suppression_list`, `templates` tables. Fix schema drift (missing `templates` DDL and `recipients.unsub_token`).
- `1.x`: Add `user_id` and `org_id` columns to `campaigns`; credit ledger reference per campaign send.
- `2.x`: Add `bounced_at`, `complaint_at` to `recipients`; index `suppression_list.email` for fast pre-send lookup.
- `3.x`: Add `audience_source`, `segment_id`, `vql_query` to `campaigns`; add `contact_ref_id` to `recipients` for Connectra lineage.
- `4.x`: Add `sn_profile_batch_id` to `campaigns` for SN-sourced audience lineage.
- `5.x`: Add `is_ai_generated`, `ai_prompt`, `ai_model` to `templates` for AI generation audit.
- `6.x`: Add `retry_count` to `recipients`; `last_processed_offset` and `batch_size` to `campaigns` for resume-from-checkpoint.
- `7.x`: Audit log emissions to `logs.api` for campaign create, send complete, unsubscribe events.
- `8.x`: Add `webhook_subscriptions` and `webhook_delivery_log` tables for campaign event webhooks.
- `9.x`: Add `sender_domains` and `entitlements` tables; `integration_suppression_sync` for CRM connector.
- `10.x`: Add `sequences`, `sequence_steps`, `campaign_events`, `campaign_analytics`, `ab_test_variants` tables.

⚠ **Critical schema drift bugs to fix before any production deployment:**
- `templates` table missing from `db/schema.sql`
- `recipients.unsub_token` column missing from `db/schema.sql`

Deep reference: `docs/backend/database/emailcampaign_data_lineage.md`.

## `salesnavigator` service database and lineage notes by era

The Sales Navigator service has **no local database**. All persistence is through Connectra (`/contacts/bulk`, `/companies/bulk`). Data flows into Connectra's PostgreSQL and Elasticsearch indexes.

- `0.x`: UUID5 deterministic contract defined; no active ingest.
- `1.x`: `actor_id`/`org_id` injected into Connectra contact metadata for audit traceability.
- `2.x`: `email`, `email_status`, `mobile_phone` field handling validated; enrichment handoff stub.
- `3.x`: Full field mapping locked; provenance fields (`source=sales_navigator`, `lead_id`, `search_id`, `connection_degree`, `data_quality_score`) written to Connectra.
- `4.x`: Primary delivery era — `data_quality_score` surfaced; `recently_hired`, `is_premium`, `mutual_connections_count` stored in Connectra contact extended attrs.
- `5.x`: `seniority`, `departments`, `about` quality gated for AI context; `data_quality_score` indexed for VQL filter queries.
- `6.x`: Chunk-level idempotency tokens; replay-safe ingest; partial success tracking; CORS hardened.
- `7.x`: Per-tenant API key; immutable audit event per save session (`{event, user_id, org_id, profiles_count, session_id, timestamp}`); GDPR erasure cascade via Connectra.
- `8.x`: Usage counter per key/day in `api_usage` table; rate-limit enforcement against stored usage.
- `9.x`: Tenant-isolated ingestion lineage; connector audit trail (`connector_events` table); webhook delivery log.
- `10.x`: Campaign provenance: `lead_id`/`search_id` carried to campaign audience records; suppression non-overwrite guard.

⚠ **Known field gaps:** `employees_count`, `industries`, `annual_revenue` are always `null` for SN-sourced companies — enrichment required from separate data source.

Deep reference: [salesnavigator_data_lineage.md](salesnavigator_data_lineage.md).  
Runtime + gap map: [salesnavigator-codebase-analysis.md](../../codebases/salesnavigator-codebase-analysis.md).

## `appointment360` (contact360.io/api) database and lineage notes by era

The appointment360 database is the **primary transactional PostgreSQL database** for Contact360. It is shared by `contact360.io/api` and certain cross-service services (e.g. `contact.ai` shares the `ai_chats` table).

- `0.x`: `users` and `token_blacklist` tables. JWT auth, password hash, token blacklist. Bootstrap baseline.
- `1.x`: `credits`, `plans`, `subscriptions`, `payment_submissions`, `activities` tables. Billing and credit system fully modeled. All feature operations must deduct from `credits` and write to `activities`.
- `3.x`: `saved_searches` table. VQL serialization into JSONB. Must stay compatible with ConnectraClient VQL format.
- `5.x`: `ai_chats`, `ai_chat_messages`, `resumes` tables. Shared `ai_chats.uuid` FK may also be used by `contact.ai`. Verify ownership split before 5.x production.
- `8.x`: `api_keys`, `sessions` tables. `totp_secret` column added to `users`. Public API key hash must use SHA-256 and never store raw key.
- `9.x`: `notifications`, `events`, `feature_flags`, `workspaces` tables. Multi-tenant workspace model.
- `10.x`: No new appointment360 tables for campaign data — campaigns/recipients/suppression are owned by the email campaign service DB. `activities` table records campaign_id for traceability.

⚠ **Known gap:** `sql/tables/` DDL files are referenced by `README.md` but missing from the local workspace checkout. Restore or link to shared schema source before any `1.x+` production deployment.

Deep reference: [appointment360_data_lineage.md](appointment360_data_lineage.md).  
Runtime + gap map: [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md).

## `mailvetter` database and lineage notes by era

- `0.x`: baseline verifier operational schema (`jobs`, `results`) and queue->DB flow.
- `1.x`: owner key and plan-attribution lineage for usage and billing reconciliation.
- `2.x`: full score/status/details lineage for single and bulk verification.
- `3.x`: optional contact/company linkage for CRM data consistency.
- `4.x`: extension/SN provenance tagging in verification metadata.
- `5.x`: AI explainability reason-code lineage.
- `6.x`: retry/DLQ and failure event lineage for reliability.
- `7.x`: migration and deployment audit lineage controls.
- `8.x`: scoped key/public-private API audit lineage.
- `9.x`: webhook delivery and connector evidence lineage.
- `10.x`: campaign preflight recipient-level verification lineage.

Deep reference: [mailvetter_data_lineage.md](mailvetter_data_lineage.md).  
Runtime + gap map: [mailvetter-codebase-analysis.md](../../codebases/mailvetter-codebase-analysis.md).

## Frontend and operator UIs (no separate lineage file required here)

When schema or API contracts change, cross-check lineage impact in Appointment360 / Connectra docs above and the matching codebase analysis:

- [admin-codebase-analysis.md](../../codebases/admin-codebase-analysis.md) — DocsAI admin
- [app-codebase-analysis.md](../../codebases/app-codebase-analysis.md) — dashboard
- [root-codebase-analysis.md](../../codebases/root-codebase-analysis.md) — marketing site
- [email-codebase-analysis.md](../../codebases/email-codebase-analysis.md) — mailbox app
- [extension-codebase-analysis.md](../../codebases/extension-codebase-analysis.md) — browser extension
