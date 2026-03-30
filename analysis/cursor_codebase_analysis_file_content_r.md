# Codebase analysis file content retrieval
_Exported on 3/26/2026 at 17:08:18 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their FULL content. Report each file's path header then content.

1. d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md
2. d:\code\ayan\contact\docs\codebases\logsapi-codebase-analysis.md
3. d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md
4. d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md
5. d:\code\ayan\contact\docs\codebases\admin-codebase-analysis.md
6. d:\code\ayan\contact\docs\codebases\root-codebase-analysis.md
7. d:\code\ayan\contact\docs\codebases\extension-codebase-analysis.md
8. d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md

Focus especially on the era 8.x sections and "Known gaps" sections.

---

**Cursor**


Reading all eight analysis files in parallel.




Below is the **full text** of each file, in order, with a path line before each block.  

**Note on headings:** Only `s3storage-codebase-analysis.md` uses a **“Gaps and risks observed”** section. The others use **“Key findings and risks”** (or equivalent); `extension-codebase-analysis.md` and `email-codebase-analysis.md` use **task** sections instead of a “Known gaps” title.

---

## 1. `d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md`

```markdown
# Contact360 `lambda/s3storage` Codebase Analysis and Task Decomposition

This document is a deep analysis of the `lambda/s3storage` service in Contact360 and a version-aligned execution breakdown across `0.x.x` to `10.x.x`.

## Purpose and role in Contact360

`s3storage` is the storage control plane for Contact360 file artifacts. It provides:

- bucket namespace initialization
- file upload/download/list/delete APIs
- multipart upload orchestration for large CSV files
- CSV schema/preview/stats analysis
- asynchronous metadata extraction and `metadata.json` maintenance
- avatar/photo/resume storage paths

This service directly supports product flows in dashboard, API gateway, jobs, extension, and future campaign/integration systems.

## Current architecture snapshot

## Service and API layer

- Entrypoint: `lambda/s3storage/app/main.py`
- Framework: FastAPI + Mangum (Lambda adapter)
- Router: `lambda/s3storage/app/api/v1/router.py`
- Endpoint groups:
  - `health`
  - `buckets`
  - `files`
  - `uploads`
  - `analysis` (schema/preview/stats/metadata)
  - `avatars`

## Backend abstraction

- Service facade: `lambda/s3storage/app/services/storage_service.py`
- Concrete backends: `lambda/s3storage/app/services/storage_backends.py`
  - `S3Backend`
  - `FilesystemBackend`
- Config selector:
  - `S3STORAGE_STORAGE_BACKEND=s3|filesystem`
  - loaded through `lambda/s3storage/app/core/config.py`

## Data and key model

Logical bucket model is prefix-based in a single S3 bucket:

- `{bucket_id}/avatar/`
- `{bucket_id}/upload/`
- `{bucket_id}/photo/`
- `{bucket_id}/export/`
- `{bucket_id}/metadata.json`

This model is aligned with Contact360 multi-surface file usage and downstream ingestion.

## Async metadata pipeline

- Upload complete triggers worker lambda invocation:
  - `s3storage-metadata-worker`
- Worker handler:
  - `lambda/s3storage/app/utils/worker.py`
- Metadata computation:
  - `lambda/s3storage/app/utils/metadata_job.py`
- Metadata persistence:
  - `lambda/s3storage/app/utils/update_bucket_metadata.py`

## Deployment

- AWS SAM template:
  - `lambda/s3storage/template.yaml`
- Two lambda functions:
  - API function
  - metadata worker function

## Strengths observed

- Clean backend abstraction (`StorageService` + backend protocol).
- Good endpoint surface coverage for product needs.
- Multipart upload flow exists end-to-end.
- Metadata worker decouples upload path from expensive file analysis.
- CSV analysis endpoints support preview/schema/stats UX.
- Service can run in S3 and filesystem modes for different environments.

## Gaps and risks observed

## 1) Multipart session state is not durable

`S3Backend` stores multipart sessions in `_MULTIPART_SESSIONS` in-process memory.

Risk:

- session loss on restart/cold start
- no horizontal-scaling safety
- inconsistent behavior across concurrent instances

## 2) Hardcoded worker function name

`uploads.py` invokes `FunctionName="s3storage-metadata-worker"` directly.

Risk:

- poor environment portability
- deployment drift across dev/stage/prod

## 3) Metadata write race risk

`update_bucket_metadata` follows read-modify-write without optimistic locking/version checks.

Risk:

- lost updates under parallel writes
- metadata corruption or dropped entries

## 4) Contract/documentation drift potential

`docs/API.md` references metadata-init behavior. Endpoint implementation should stay explicitly aligned with docs and tested as a contract.

## 5) Security defaults need tightening for scale

CORS in app is permissive (`*`) and endpoint-level auth is expected upstream.

Risk:

- policy ambiguity and accidental overexposure in direct deployments

## Contact360 era mapping (`0.x.x` to `10.x.x`)

This section translates your version policy into concrete, small task packs for `s3storage`.

## `0.x.x` - Foundation and pre-product stabilization and codebase setup

### Goal

Stabilize service boundaries and baseline deployment primitives.

### Small tasks

- Contract:
  - freeze endpoint naming and payload shape for core storage operations
  - define canonical logical key taxonomy and folder semantics
- Service:
  - finalize backend interface behavior parity (`s3` vs `filesystem`)
  - standardize error contract (`StorageError` mapping)
- Data:
  - define canonical `metadata.json` schema v1
  - add explicit metadata schema version field
- Ops:
  - baseline health checks and deployment outputs in SAM
  - add smoke test for bucket create -> upload -> list -> download-url

## `1.x.x` - Contact360 user and billing and credit system

### Goal

Support user identity assets and billing artifacts with robust policy controls.

### Small tasks

- Contract:
  - define object-class policy matrix (`avatar`, `photo`, `resume`, `upload`)
  - define content-type and size rules per class
- Service:
  - enforce path-specific validation for billing/identity uploads
  - add idempotency behavior for delete and overwrite flows
- Surface:
  - align gateway/dashboard callers to new validation and error semantics
- Data:
  - attach actor/source metadata for auditability
- Ops:
  - add abuse/rate monitoring for upload endpoints used in billing journeys

## `2.x.x` - Contact360 email system

### Goal

Harden bulk CSV upload and metadata flow powering finder/verifier pipelines.

### Small tasks

- Contract:
  - freeze multipart API contract (`initiate`, `parts`, `register`, `complete`, `abort`)
  - define retry-safe completion semantics
- Service:
  - replace in-memory multipart session store with durable shared state
  - add checksum/etag consistency guards
- Surface:
  - standardize client retry behavior for dashboard and gateway
- Data:
  - guarantee metadata freshness SLA after complete/upload
  - add metadata reconciliation command for upload vs metadata drift
- Ops:
  - full E2E resilience tests for partial failures and resume

## `3.x.x` - Contact360 contact and company data system

### Goal

Make storage artifacts first-class inputs for Connectra and enrichment pipelines.

### Small tasks

- Contract:
  - define dataset artifact classes for contacts/companies import/export
  - define naming/versioning policy for ingestion files
- Service:
  - optimize preview/schema/stats for high-cardinality files
  - improve delimiter/encoding robustness and malformed-row handling
- Surface:
  - expose ingestion-ready metadata fields to gateway consumers
- Data:
  - add lineage links upload -> ingestion run -> index operation
- Ops:
  - quality checks and anomaly alerts for ingestion metadata

## `4.x.x` - Contact360 Extension and Sales Navigator maturity

### Goal

Support extension-origin artifacts with tight access controls and observability.

### Small tasks

- Contract:
  - define extension-safe URL TTL and access constraints
  - define extension channel-specific object prefixes
- Service:
  - add stricter auth context checks for extension-origin operations
  - improve download URL policy granularity by object class
- Surface:
  - expose extension-friendly error and retry semantics
- Data:
  - store provenance tags (`source=extension|salesnavigator`)
- Ops:
  - channel-level telemetry and triage views

## `5.x.x` - Contact360 AI workflows

### Goal

Support AI artifacts with governance and lineage guarantees.

### Small tasks

- Contract:
  - define AI artifact types (prompt/input/output/intermediate)
  - define retention and access policy contract for sensitive AI artifacts
- Service:
  - enforce object-class limits and policy guards for AI paths
  - enable immutable artifact write mode where needed
- Surface:
  - expose explicit retrieval semantics for AI consumers
- Data:
  - track source-file linkage and model-run lineage metadata
- Ops:
  - audit trails for sensitive AI artifact reads/writes

## `6.x.x` - Contact360 Reliability and Scaling

### Goal

Make storage workflows reliably scalable under multi-tenant production load.

### Small tasks

- Contract:
  - formalize idempotency keys for complete/abort/update metadata operations
  - define SLO contracts for upload and metadata freshness
- Service:
  - implement durable multipart session store
  - add optimistic concurrency or CAS strategy for `metadata.json` updates
  - add resilient backoff/retry wrappers for S3 transient failures
- Surface:
  - publish retry-safe client guidance for all callers
- Data:
  - implement periodic reconciliation (S3 objects vs metadata entries)
- Ops:
  - create SLO dashboard: upload success, complete latency, metadata lag
  - define error budget and incident runbook

## `7.x.x` - Contact360 deployment

### Goal

Bring deployment governance, authz hardening, and compliance controls.

### Small tasks

- Contract:
  - define service-to-service auth contract and tenant policy enforcement contract
- Service:
  - enforce authentication/authorization at endpoint boundary
  - remove hardcoded worker function names; use environment-driven routing
- Surface:
  - align gateway/admin integrations with role-based restrictions
- Data:
  - implement policy-controlled retention/deletion hooks per object class
- Ops:
  - add compliance evidence artifacts and deployment security checklist

## `8.x.x` - Contact360 public and private apis and endpoints

### Goal

Prepare storage APIs as stable versioned internal/public interfaces.

### Small tasks

- Contract:
  - define API versioning and deprecation policy for storage endpoints
  - define event/webhook contract for object lifecycle
- Service:
  - emit lifecycle events (upload complete/delete/update) with replay-safe IDs
  - add compatibility tests for old/new contract variants
- Surface:
  - provide docs and SDK examples for partner/internal consumers
- Data:
  - event lineage linking object actions to consumers and outcomes
- Ops:
  - compatibility gate and observability for partner-facing reliability

## `9.x.x` - Contact360 Ecosystem integrations and Platform productization

### Goal

Productize storage capabilities with entitlements, quotas, and tenant economics.

### Small tasks

- Contract:
  - define entitlement-aware storage capability matrix by plan
- Service:
  - enforce quotas (size/object count/rate) and tenant throttling
  - add policy engine hooks for plan and integration controls
- Surface:
  - expose admin diagnostics for quota and policy failures
- Data:
  - add cost attribution and residency metadata overlays
- Ops:
  - SLA reporting and support escalation pathways

## `10.x.x` - Contact360 email campaign

### Goal

Support campaign-scale artifact lifecycle with compliance-grade reproducibility.

### Small tasks

- Contract:
  - define campaign artifact contracts (audiences, suppressions, templates, evidence)
  - define reproducibility contract for campaign execution artifacts
- Service:
  - optimize high-throughput read/write paths for campaign engines
  - enforce immutability for compliance-critical campaign artifacts
- Surface:
  - provide stable retrieval semantics for campaign observability/support tooling
- Data:
  - store consent/opt-out/suppression lineage evidence references
- Ops:
  - final compliance and governance gate for campaign-era readiness

## Immediate execution queue (high impact)

1. Durable multipart session store (replace in-memory session map).
2. Environment-driven metadata worker function configuration.
3. Concurrency-safe `metadata.json` update strategy.
4. Contract parity check between implemented endpoints and `docs/API.md`.
5. End-to-end integration tests for multipart + metadata worker paths.
6. Failure-path tests (duplicate complete, missing parts, worker failure, retries).
7. Upload security hardening checklist (auth, CORS, object policy, TTL).
8. SLO baseline and dashboards for storage reliability.

## Suggested owner map

- Platform Storage team: service/data/ops tasks
- API Gateway team: contract/surface integration tasks
- Product surfaces (Dashboard/Extension/Admin): UI and caller-behavior tasks
- Security/Compliance: authz, retention, audit, governance tasks

## Release gate checklist for each minor

- Contract compatibility validated (and documented).
- Service changes covered by integration and failure-path tests.
- Data lineage/metadata integrity checks passing.
- Ops telemetry and alerts updated for new behavior.
- Rollback plan validated before release promotion.

```

---

## 2. `d:\code\ayan\contact\docs\codebases\logsapi-codebase-analysis.md`

```markdown
# logs.api codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`lambda/logs.api` is a FastAPI logging service that stores log records in S3 CSV objects and provides CRUD/query/search/statistics endpoints for operational and audit use-cases across Contact360.

## Runtime architecture

- Entrypoint: `lambda/logs.api/app/main.py`
- Routing: `app/api/v1/endpoints/logs.py`, `app/api/v1/endpoints/health.py`
- Service layer: `app/services/log_service.py`
- Data repository: `app/models/log_repository.py`
- Storage client: `app/clients/s3.py`
- Caching and telemetry: `app/utils/query_cache.py`, `query_monitor.py`, `cache_metrics.py`
- Deployment contract: `lambda/logs.api/template.yaml`

## Key findings and risks

1. Documentation drift: multiple docs still describe MongoDB, but implementation is S3 CSV.
2. Security risk: static API key pattern is used across service-to-service calls and examples.
3. Query scalability risk: heavy range scans on CSV objects can become expensive at higher traffic.
4. Cache consistency risk: in-memory cache is per-instance and not globally coherent.
5. Compliance risk: docs and evidence packs must clearly tie retention and audit behavior to deployed policy.

## API contract snapshot

- `POST /logs`, `POST /logs/batch`
- `GET /logs`, `GET /logs/search`, `GET /logs/{log_id}`
- `PUT /logs/{log_id}`, `DELETE /logs/{log_id}`
- `POST /logs/delete`, `DELETE /logs`
- `GET /health`, `GET /health/info`

## Era-by-era task packs (Contract / Service / Surface / Data / Ops)

### 0.x Foundation
- Contract: define health and write/read baseline envelope for logs.api.
- Service: stabilize S3 CSV write/read path and startup health checks.
- Surface: wire baseline health visibility in internal tooling (no user-facing UI dependency).
- Data: define object naming convention, timestamp normalization, and minimal schema.
- Ops: smoke tests and startup checklist for local and Lambda environments.

### 1.x User/Billing/Credit
- Contract: define auth, billing, and credit event logging schema.
- Service: ensure gateway writes user lifecycle events with request/tenant/user IDs.
- Surface: activity indicators for user and billing flows.
- Data: event lineage to billing and usage modules.
- Ops: abuse monitoring for repeated auth/payment failures.

### 2.x Email system
- Contract: email finder/verifier job-event schema and status transitions.
- Service: high-volume batch write path for job progress and completion events.
- Surface: progress bars and job timelines in results/bulk pages.
- Data: retention and query windows for high-throughput logs.
- Ops: alerting for verifier/finder failure spikes.

### 3.x Contacts/Companies
- Contract: contact/company enrichment and dedupe log contract.
- Service: query filters by service, workspace, and operation class.
- Surface: searchable operational log panels for data support flows.
- Data: lineage tie-back to search/enrichment operations.
- Ops: anomaly checks on dedupe/enrichment failure clusters.

### 4.x Extension/Sales Navigator
- Contract: extension ingestion/sync event schema.
- Service: extension source tagging and provenance fields.
- Surface: extension telemetry and sync diagnostics panels.
- Data: source-of-truth tags for extension-generated events.
- Ops: replay diagnostics for ingestion regressions.

### 5.x AI workflows
- Contract: AI prompt, tool, and response telemetry schema.
- Service: log write guards for sensitive payload minimization.
- Surface: AI debug traces and troubleshooting views for internal teams.
- Data: retention segmentation for AI-sensitive telemetry.
- Ops: cost and error anomaly dashboards from logs.api aggregates.

### 6.x Reliability and scaling
- Contract: SLO/error-budget evidence contract from logs.
- Service: optimize query paths, cache metrics, and streaming thresholds.
- Surface: reliability dashboards with log-derived indicators.
- Data: rollup patterns for long-window metrics.
- Ops: runbooks for hot partitions, cache churn, and query timeout spikes.

### 7.x Deployment
- Contract: deployment/audit event contract and retention guarantees.
- Service: environment-aware logging (release, region, service version).
- Surface: admin audit and release diagnostics views.
- Data: verify 90-day retention policy evidence and exceptions.
- Ops: deployment gate requiring logging health and retention proof.

### 8.x Public/Private APIs
- Contract: API access/audit event schema for partner/public traffic.
- Service: endpoint- and key-scoped query support for investigations.
- Surface: API log viewer with filter presets and export affordances.
- Data: lineage for webhook/public endpoint events.
- Ops: compatibility and incident triage workflows tied to logs.

### 9.x Ecosystem integrations
- Contract: connector and tenant governance event schema.
- Service: tenant-scoped filtering and entitlement-aware querying.
- Surface: tenant activity feeds and integration diagnostics.
- Data: cross-service event correlation via trace/request IDs.
- Ops: SLA and partner incident evidence generation.

### 10.x Email campaign
- Contract: campaign compliance and send lifecycle event schema.
- Service: immutable audit-relevant logging for campaign lifecycle.
- Surface: campaign audit timelines and compliance review panels.
- Data: retention and legal-hold compatible evidence paths.
- Ops: campaign RC gates backed by log-derived quality and compliance checks.
```

---

## 3. `d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md`

```markdown
# emailapis / emailapigo codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`lambda/emailapis` (Python FastAPI) and `lambda/emailapigo` (Go Gin) are Contact360's dual-runtime email execution services for finder, verifier, pattern add, and web-search fallback flows. They sit behind Appointment360 GraphQL and power both interactive and bulk email workloads.

## Runtime architecture

- Python entrypoint: `lambda/emailapis/app/main.py`
- Python router: `lambda/emailapis/app/api/v1/router.py`
- Go entrypoint: `lambda/emailapigo/main.go`
- Go router: `lambda/emailapigo/internal/api/router.go`
- Finder services: `app/services/email_finder_service.py`, `internal/services/email_finder_service.go`
- Verifier services: `app/services/email_verification_service.py`, `internal/services/email_verification_service.go`
- Pattern services: `app/services/email_pattern_service.py`, `internal/services/email_pattern_service.go`
- Data repositories: cache + pattern repositories in both runtimes

## API contract snapshot

- `POST /email/finder/`
- `POST /email/finder/bulk`
- `POST /email/single/verifier/`
- `POST /email/bulk/verifier/`
- `POST /email-patterns/add`
- `POST /email-patterns/add/bulk`
- `POST /web/web-search`
- `GET /health`, `GET /`

## Data model and persistence

### `email_finder_cache`
- Identity keys: `first_name`, `last_name`, `domain` (case-insensitive)
- Result fields: `email_found`, `email_source`
- Constraints: unique identity + lookup index
- Role: short-path cache hit before provider fanout

### `email_patterns`
- Keys: `uuid`, `company_uuid`, `domain`
- Pattern fields: `pattern_format`, `pattern_string`
- Metrics: `contact_count`, `success_rate`, `error_rate`
- Role: learned pattern persistence used by finder flows

## Provider orchestration and behavior

### Finder flow (both runtimes)
1. Cache lookup (`email_finder_cache`)
2. Parallel provider candidates:
   - Connectra
   - Pattern service
   - Generator
3. Race verification of candidates
4. Fallback discovery:
   - Web search
   - IcyPeas
5. Return normalized list and source attribution

### Verifier flow
- Python defaults commonly reference `truelist` + `icypeas`
- Go health and runtime prefer `mailvetter` + `icypeas` (`mailvetter_configured` check)
- Bulk paths use concurrency controls and stagger/timeout behavior

## Key findings and cross-service risks

1. Provider drift risk: Python/docs often reference `truelist`; Go runtime prioritizes `mailvetter`.
2. Status semantic drift risk: `valid`/`invalid`/`catchall`/`unknown` interpretation can differ across app, api, and runtime mapping.
3. Observability gap: correlation across app -> api -> jobs -> lambda is not consistently documented with one trace contract.
4. Contract drift risk: endpoint and payload assumptions in docs may lag runtime changes.
5. Bulk correctness risk: partial-batch error mapping and retry semantics require explicit cross-layer contract tests.

## Era-by-era task packs (Contract / Service / Surface / Data / Ops)

### 0.x Foundation
- Contract: freeze base endpoint envelope and health diagnostics keys.
- Service: stabilize startup/middleware/error translation in both runtimes.
- Surface: document baseline finder/verifier UI states for core shell.
- Data: lock cache/pattern table schema baseline.
- Ops: add smoke checks for Python and Go runtimes.

### 1.x User/Billing/Credit
- Contract: align credit-impact operation contract at GraphQL boundary.
- Service: guarantee non-blocking logging around credit-aware paths.
- Surface: show clear credit impact and error messaging in email flows.
- Data: capture request-to-credit lineage fields.
- Ops: alert on credit deduction anomalies for email operations.

### 2.x Email system
- Contract: unify provider naming and status semantics for finder/verifier.
- Service: harden bulk fanout, verification race, and fallback behavior.
- Surface: lock Finder/Verifier tabs, mapping modals, progress UX contract.
- Data: enforce cache/pattern lineage quality and mutation evidence.
- Ops: baseline bulk latency/failure dashboards and RC criteria.

### 3.x Contact/Company data
- Contract: align Connectra identity keys and enrichment payload shape.
- Service: improve domain-first lookup behavior and deterministic candidate merge.
- Surface: improve contact/company email hydration consistency.
- Data: map email lineage to contact/company enrichment paths.
- Ops: add drift checks between enrichment and email status outcomes.

### 4.x Extension/Sales Navigator
- Contract: define extension-origin email query metadata fields.
- Service: support source-tagged extension lookups safely.
- Surface: expose extension sync status and retry diagnostics.
- Data: provenance tagging for extension-triggered email actions.
- Ops: replay/debug runbook for extension ingestion regressions.

### 5.x AI workflows
- Contract: define AI-assisted finder/verifier payload boundaries.
- Service: expose safe utility endpoints for AI orchestration.
- Surface: bind assistant panel results to canonical email statuses.
- Data: track AI-assisted decision lineage with confidence mapping.
- Ops: monitor AI-assisted failure and quality regressions.

### 6.x Reliability and scaling
- Contract: SLO/error-budget evidence for email endpoints.
- Service: optimize bulk concurrency, timeouts, retries, and circuit behavior.
- Surface: reliability indicators and retry UX consistency.
- Data: long-window trend rollups for status distribution drift.
- Ops: runbooks for provider degradation and fallback storms.

### 7.x Deployment
- Contract: release/deployment metadata in health and diagnostics docs.
- Service: enforce environment parity checks (keys, DB, provider readiness).
- Surface: deployment-safe admin indicators for email runtime readiness.
- Data: retain deployment evidence and rollback context.
- Ops: pre-release gate requiring email runtime health proof.

### 8.x Public/private APIs
- Contract: versioned private/public email contract policy.
- Service: key-scoped behaviors and partner-safe error envelopes.
- Surface: API docs and integration UX reflect canonical contract.
- Data: audit lineage for partner/public email operations.
- Ops: compatibility gates and incident triage playbooks.

### 9.x Ecosystem integrations
- Contract: connector-ready email capability contract.
- Service: tenant-aware throttles and entitlement-safe behaviors.
- Surface: integration controls for email capability toggles.
- Data: cross-service trace IDs for partner investigations.
- Ops: SLA evidence generation for integration channels.

### 10.x Email campaign
- Contract: campaign send/compliance email verification contract.
- Service: immutable verification evidence for campaign lifecycle.
- Surface: campaign audit timelines and compliance controls.
- Data: retention/legal-hold ready campaign email artifacts.
- Ops: campaign release gate tied to deliverability and compliance checks.
```

---

## 4. `d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md`

```markdown
# contact360.io/app codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`contact360.io/app` is the authenticated Contact360 dashboard. It is a Next.js 16 + React 19 + TypeScript app that drives core product workflows (auth, billing/credits, email finder/verifier, contacts/companies, jobs/files, admin, AI, integrations) over GraphQL.

## Runtime architecture

- Root layout and providers: `contact360.io/app/app/layout.tsx`
- Authenticated gate/layout: `contact360.io/app/app/(dashboard)/layout.tsx`
- Core shell: `contact360.io/app/src/components/layout/MainLayout.tsx`, `Sidebar.tsx`
- GraphQL client: `contact360.io/app/src/lib/graphqlClient.ts`
- Config and environment: `contact360.io/app/src/lib/config.ts`
- Contexts: `src/context/AuthContext.tsx`, `RoleContext.tsx`, `ThemeContext.tsx`, `DashboardPageContext.tsx`

## UI/UX inventory

### Pages and route groups

- Auth pages: login/register/session-related routes
- Dashboard pages: billing, usage, contacts, companies, email tools, files, jobs, profile, analytics, admin, AI, integrations
- Layout patterns: `MainLayout`, `DashboardPageLayout`, `DataPageLayout`, `ToolPageLayout`

### UI primitives and controls

- Components exported from `src/components/ui/index.ts`: `Button`, `Input`, `Tabs`, `Badge`, `Modal`, `ConfirmModal`, `Alert`, `Popover`
- Progress bars: upload and usage/credit surfaces (`UploadProgressBar` and layout alerts)
- Checkbox/radio usage: table row selection and profile

