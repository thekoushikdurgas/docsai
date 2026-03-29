# Backend Docs Index

Master index for backend contract, endpoint, lineage, and validation documentation.

## Scope

- Covers Appointment360 GraphQL, service APIs, endpoint metadata, data lineage, and Postman validation assets.
- Aligns backend docs to era-based delivery (`0.x` to `10.x`).

## Parity with `docs/codebases/`

- **`docs/backend/**`** is the **contract authority**: GraphQL modules, REST route tables, endpoint JSON matrices, lineage, and Postman wiring.
- **`docs/codebases/*-codebase-analysis.md`** is the **runtime + risk register**: verified behavior, gaps, storage/log migration maps, and era-tagged execution queues.
- When you update either side, sync the other in the same change set when routes, auth, data stores, or era ownership shift.

## Codebase analysis registry

Use this map when updating runtime code: start from the matching `docs/codebases/*-codebase-analysis.md`, then touch the listed backend artifacts in the same change set.

| Codebase analysis | Runtime path / surface | Primary `docs/backend` touchpoints |
| --- | --- | --- |
| [admin-codebase-analysis.md](../codebases/admin-codebase-analysis.md) | `contact360.io/admin` (DocsAI) | `apis/13_ADMIN_MODULE.md`, `appointment360_data_lineage.md`, `services.apis/admin.api.md`, gateway integration notes in `docs/frontend.md` |
| [app-codebase-analysis.md](../codebases/app-codebase-analysis.md) | `contact360.io/app` (dashboard) | GraphQL modules consumed by the app (`apis/01`–`28` as applicable), `07_S3_MODULE.md`, `10_UPLOAD_MODULE.md`, `16_JOBS_MODULE.md`, `endpoints/*_graphql.json` + `appointment360_endpoint_era_matrix.json`, `postman/` per-module collections |
| [appointment360-codebase-analysis.md](../codebases/appointment360-codebase-analysis.md) | `contact360.io/api` | All `apis/*_MODULE.md` for schema parity, `appointment360_endpoint_era_matrix.json`, `appointment360_data_lineage.md` |
| [connectra-codebase-analysis.md](../codebases/connectra-codebase-analysis.md) | `contact360.io/sync` (Connectra / data plane) | `apis/03_CONTACTS_MODULE.md`, `apis/04_COMPANIES_MODULE.md`, `connectra_endpoint_era_matrix.json`, `connectra_data_lineage.md` |
| [sync-codebase-analysis.md](../codebases/sync-codebase-analysis.md) | `contact360.io/sync` (same service; normalized analysis) | Same row as Connectra; prefer this file for era-tagged gaps when both exist |
| [contact-ai-codebase-analysis.md](../codebases/contact-ai-codebase-analysis.md) | `backend(dev)/contact.ai` | `apis/17_AI_CHATS_MODULE.md`, `contact_ai_endpoint_era_matrix.json`, `contact_ai_data_lineage.md`, `services.apis/contact.ai.api.md`, Postman: `docs/media/postman/Contact AI Service.postman_collection.json` |
| [email-codebase-analysis.md](../codebases/email-codebase-analysis.md) | `contact360.io/email` (mailbox UI) | `apis/15_EMAIL_MODULE.md` (product email APIs), IMAP/security notes in `docs/frontend.md` / mailbox docs; no separate GraphQL module for IMAP |
| [emailapis-codebase-analysis.md](../codebases/emailapis-codebase-analysis.md) | `lambda/emailapis`, `lambda/emailapigo` | `apis/15_EMAIL_MODULE.md`, `emailapis_endpoint_era_matrix.json`, `emailapis_data_lineage.md` |
| [emailcampaign-codebase-analysis.md](../codebases/emailcampaign-codebase-analysis.md) | `backend(dev)/email campaign` | `apis/22_CAMPAIGNS_MODULE.md`, `24_SEQUENCES_MODULE.md`, `25_CAMPAIGN_TEMPLATES_MODULE.md`, `emailcampaign_endpoint_era_matrix.json`, `emailcampaign_data_lineage.md`, `services.apis/emailcampaign.api.md` |
| [extension-codebase-analysis.md](../codebases/extension-codebase-analysis.md) | `extension/contact360` | `apis/21_LINKEDIN_MODULE.md`, `apis/23_SALES_NAVIGATOR_MODULE.md`, related `endpoints/*graphql.json`, `salesnavigator_endpoint_era_matrix.json` |
| [jobs-codebase-analysis.md](../codebases/jobs-codebase-analysis.md) | `contact360.io/jobs` | `apis/16_JOBS_MODULE.md`, `jobs_endpoint_era_matrix.json`, `jobs_data_lineage.md` |
| [logsapi-codebase-analysis.md](../codebases/logsapi-codebase-analysis.md) | `lambda/logs.api` | Admin log queries in `apis/13_ADMIN_MODULE.md`, `logsapi_endpoint_era_matrix.json`, `logsapi_data_lineage.md` |
| [mailvetter-codebase-analysis.md](../codebases/mailvetter-codebase-analysis.md) | `backend(dev)/mailvetter` | `apis/15_EMAIL_MODULE.md` (verifier integration), `mailvetter_endpoint_era_matrix.json`, `mailvetter_data_lineage.md`, `services.apis/mailvetter.api.md` |
| [root-codebase-analysis.md](../codebases/root-codebase-analysis.md) | `contact360.io/root` (marketing) | `apis/19_PAGES_MODULE.md` (public pages), marketing GraphQL usage, `postman/` where marketing calls gateway |
| [s3storage-codebase-analysis.md](../codebases/s3storage-codebase-analysis.md) | `lambda/s3storage` | `apis/07_S3_MODULE.md`, `apis/10_UPLOAD_MODULE.md`, `s3storage_endpoint_era_matrix.json`, `Storage_Backend_s3storage.postman_collection.json` |
| [salesnavigator-codebase-analysis.md](../codebases/salesnavigator-codebase-analysis.md) | `backend(dev)/salesnavigator` | `apis/23_SALES_NAVIGATOR_MODULE.md`, `salesnavigator_endpoint_era_matrix.json`, `salesnavigator_data_lineage.md`, `services.apis/salesnavigator.api.md` |

**Frontend-only surfaces** (no dedicated REST doc in `services.apis/`): `admin`, `app`, `root`, `email`, `extension` — still require backend contract updates when GraphQL modules, endpoint JSON, or Postman examples change.

## Folder map

- `apis/` — GraphQL module and service contract docs (`01`–`29`, era task packs).
- `database/` — Lineage, data ownership, drift playbooks, table references.
- `endpoints/` — Operation JSON and `*_endpoint_era_matrix.json` inventories (`endpoints_index.json` aggregates GraphQL ops; supplemental matrices cover REST/Lambda services).
- `postman/` — Canonical Contact360 collections and reference imports (see `postman/README.md`).
- `services.apis/` — Service hubs: GraphQL gateway (`appointment360.api.md`), Connectra/jobs/storage/logs/email workers, plus REST-heavy docs (Contact AI, Sales Navigator, Mailvetter, Admin, email campaign). See [services.apis/README.md](services.apis/README.md).

## Folder reality snapshot

- `apis/` includes module docs (`01` through `29`) plus multiple `*_ERA_TASK_PACKS.md` indexes.
- `database/` includes service-specific lineage docs and drift playbooks.
- `endpoints/` stores operation JSON metadata, `endpoints_index.json`, and service-era matrix files (including `contact_ai`, `salesnavigator`, `mailvetter`, `emailcampaign`, `jobs`, `s3storage`, `logsapi`, and others).
- `postman/` includes canonical Contact360 collections and large imported reference packs.

## Core maintenance workflow

1. Update runtime behavior in code.
2. Sync module contract docs in `apis/`.
3. Sync endpoint metadata in `endpoints/` (including `supplemental_indexes` in `endpoints_index.json` when a new service matrix is added).
4. Sync lineage impact in `database/`.
5. Sync validation artifacts in `postman/`.
6. Sync `services.apis/` when standalone REST contracts change.
7. Update `docs/codebases/<service>-codebase-analysis.md` when the change is cross-cutting (auth, S3 control plane, logs.api, new risks).
8. Update roadmap/version status when scope changes (`docs/roadmap.md`, `docs/versions.md`).

## Small-task breakdown

- `Task 1 - Contract`: validate module docs vs runtime handlers.
- `Task 2 - Endpoint`: update operation metadata and auth/rbac fields.
- `Task 3 - Data`: update tables/lineage impacts and ownership notes.
- `Task 4 - Validation`: refresh Postman checks and sample payloads.
- `Task 5 - Governance`: enforce docs sync runbook and release evidence.
- `Task 6 - Codebases`: reflect the same facts in `docs/codebases/` analyses when gaps or era tasks move.

## Cross-links

- `docs/README.md`
- `docs/backend.md`
- `docs/architecture.md`
- `docs/docsai-sync.md`
- `docs/codebases/README.md`
- `docs/roadmap.md`
- `docs/versions.md`
- `docs/backend/apis/README.md`
- `docs/backend/endpoints/README.md`
- `docs/backend/database/README.md`
- `docs/backend/postman/README.md`
- `docs/backend/services.apis/README.md`
