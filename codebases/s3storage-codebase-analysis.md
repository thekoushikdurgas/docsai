# Contact360 `lambda/s3storage` Codebase Analysis and Task Decomposition

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

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

### Verified as completed in current code

- [x] ✅ Multipart session state is durable (`_multipart_sessions/{upload_id}.json` in S3).
- [x] ✅ Metadata worker function name is environment-driven (`S3_METADATA_WORKER_FUNCTION_NAME`).
- [x] ✅ Metadata updates use optimistic write guards (`IfMatch` / `IfNoneMatch`) with retries.
- [x] ✅ API key protection is enforced on all non-health routes via router dependencies.

### Still open / active risks

#### 1) Missing idempotency contract on upload lifecycle

- [ ] ⬜ Incomplete: `initiate/complete/abort` do not enforce or replay `X-Idempotency-Key`.
- Impact: duplicate completion or client retry storms can create ambiguous final states.

#### 2) Endpoint abstraction leakage

- [ ] 🟡 In Progress: `avatars.py` accesses `storage_service._backend` directly.
- [ ] 🟡 In Progress: `schema.py` uses `S3Backend()` directly for metadata retrieval, bypassing backend abstraction.
- Impact: backend parity (`s3` vs `filesystem`) and testability drift.

#### 3) Multipart complete request coupling risk

- [ ] ⬜ Incomplete: `complete_upload` accepts `bucket_id` separately from upload session identity.
- Impact: caller-side mismatch risk unless session-to-bucket binding is validated server-side.

#### 4) Security/deployment drift risks

- [ ] 🟡 In Progress: app-level CORS allowlist is strict, but SAM `HttpApi` CORS in `template.yaml` still allows `"*"`.
- [ ] ⬜ Incomplete: `samconfig.toml` contains real-looking secret-like values that should be replaced with placeholders.

#### 5) Test coverage gap

- [ ] ⬜ Incomplete: only health tests exist; no multipart lifecycle, metadata worker, or failure-path integration tests.

#### 6) Contract parity and evidence gap

- [ ] 🟡 In Progress: docs/runtime parity checks are partial; endpoint contract evidence is not yet fully closed.

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

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Multipart/session and worker-name contracts are environment-driven in runtime.
- [ ] ⬜ Incomplete: Add idempotency-key contract for upload lifecycle endpoints.
- [ ] 🟡 In Progress: Complete docs/API parity and endpoint matrix sync.
- [ ] 📌 Planned: Add versioned contract and deprecation policy for `8.x` externalization.

### Service pack

- [x] ✅ Durable multipart session persistence is implemented in S3.
- [x] ✅ Metadata optimistic-write guard/retry path is implemented.
- [ ] 🟡 In Progress: Remove direct backend access from endpoint layer (`avatars.py`, `schema.py`).
- [ ] ⬜ Incomplete: Add complete-flow validation that session bucket and request bucket cannot diverge.

### Surface pack

- [x] ✅ Core upload/list/download/analysis route surfaces are available.
- [ ] 🟡 In Progress: Standardize error envelope and retry hints for all caller surfaces.
- [ ] 📌 Planned: Add partner/developer-facing usage examples for `8.x` API consumers.

### Data pack

- [x] ✅ Metadata extraction pipeline writes key file stats and headers.
- [ ] ⬜ Incomplete: Add metadata schema versioning and drift-reconciliation evidence.
- [ ] 📌 Planned: Add full lineage overlays for entitlement/compliance eras (`9.x`, `10.x`).

### Ops pack

- [x] ✅ API-key guard and non-debug CORS allowlist validation exist in runtime config.
- [ ] ⬜ Incomplete: Replace wildcard CORS in SAM template with explicit environment allowlist.
- [ ] ⬜ Incomplete: Expand test suite beyond health checks (multipart lifecycle + failure paths).
- [ ] ⬜ Incomplete: Sanitize local deploy config files to remove secret-like values.
- [ ] 📌 Planned: Add SLO dashboards and error-budget gates for reliability promotion.

## Immediate execution queue (high impact)

- [x] ✅ Durable multipart session store (replace in-memory session map).
- [x] ✅ Environment-driven metadata worker function configuration.
- [x] ✅ Concurrency-safe `metadata.json` update strategy.
- [ ] ⬜ Incomplete: upload lifecycle idempotency contract (`X-Idempotency-Key`) for initiate/complete/abort.
- [ ] 🟡 In Progress: contract parity check between implemented endpoints and `docs/API.md`.
- [ ] 🟡 In Progress: remove endpoint abstraction leakage (`avatars.py` and `schema.py` direct backend usage).
- [ ] ⬜ Incomplete: enforce session-bound bucket validation in multipart complete flow.
- [ ] ⬜ Incomplete: end-to-end integration tests for multipart + metadata worker paths.
- [ ] ⬜ Incomplete: failure-path tests (duplicate complete, missing parts, worker failure, retries).
- [ ] 🟡 In Progress: upload security hardening checklist (auth, CORS, object policy, TTL, deploy-template parity).
- [ ] ⬜ Incomplete: sanitize `samconfig.toml` secret-like values to placeholders.
- [ ] 📌 Planned: SLO baseline and dashboards for storage reliability.

## Suggested owner map

- Platform Storage team: service/data/ops tasks
- API Gateway team: contract/surface integration tasks
- Product surfaces (Dashboard/Extension/Admin): UI and caller-behavior tasks
- Security/Compliance: authz, retention, audit, governance tasks

## Cross-codebase adoption plan (`s3storage` as shared storage control plane)

### Current adoption snapshot

- [x] ✅ `appointment360` (`contact360.io/api`) already routes upload/list/download/schema/avatar flows through `s3storage` client wrappers.
- [ ] 🟡 In Progress: `admin` (`contact360.io/admin`) uses both `s3storage` API calls and direct `boto3` paths (`apps/core/services/s3_service.py`).
- [ ] ⬜ Incomplete: `jobs` (`contact360.io/jobs`) still reads and writes objects directly using `boto3/aioboto3` multipart APIs.
- [ ] 📌 Planned: unify storage contracts for `logs.api`, `emailapis`, `emailcampaign`, and other service exports/imports that can centralize on `s3storage`.

### Shared migration principles

- [ ] 🟡 In Progress: treat `s3storage` as the only service allowed to hold raw bucket credentials for application-level object operations.
- [ ] ⬜ Incomplete: keep one logical contract (`bucket_id`, `file_key`, metadata lineage) across all producers/consumers.
- [ ] ⬜ Incomplete: disallow new direct `boto3/aioboto3` usage in app services unless explicitly approved for internal worker/runtime-only implementation.
- [ ] 📌 Planned: publish a storage capability matrix by era (`2.x` to `10.x`) for imports, exports, campaign artifacts, and compliance evidence.

### Execution pack A - `appointment360` hardening (already integrated)

- [x] ✅ Core upload and storage GraphQL flows use `S3StorageClient`.
- [ ] ⬜ Incomplete: add idempotency-key propagation from GraphQL mutation layer to `s3storage` upload lifecycle endpoints.
- [ ] 🟡 In Progress: normalize caller-side error taxonomy to map `s3storage` failures to deterministic GraphQL error codes.
- [ ] ⬜ Incomplete: add integration tests that assert `appointment360` never falls back to direct S3 writes in upload/avatar paths.
- [ ] 📌 Planned: add contract tests for backward compatibility before `8.x` public API stabilization.

### Execution pack B - `admin` migration to full API mode

- [ ] 🟡 In Progress: keep `apps/admin/services/s3storage_client.py` as the only admin storage access path.
- [ ] ⬜ Incomplete: migrate `apps/core/services/s3_service.py` use cases to `s3storage` endpoints or isolate them behind explicit internal-only adapters.
- [ ] ⬜ Incomplete: remove "no API key required" assumption and align auth model with `s3storage` API key policy.
- [ ] ⬜ Incomplete: align photo/asset upload routes to canonical `s3storage` contracts (prefix rules, metadata updates, audit fields).
- [ ] 📌 Planned: add admin UI evidence links for object lifecycle/audit events per tenant bucket.

### Execution pack C - `jobs` migration (highest impact for consistency)

- [ ] ⬜ Incomplete: replace direct multipart write logic in stream processors with `s3storage` upload lifecycle (`initiate -> part url -> register -> complete/abort`) through a dedicated jobs storage client.
- [ ] ⬜ Incomplete: replace direct object-read helpers with signed download or server-side stream contracts exposed by `s3storage`.
- [ ] ⬜ Incomplete: propagate `bucket_id/file_key` identity instead of raw `bucket/key` when persisting checkpoints and job payloads.
- [ ] ⬜ Incomplete: add resume/idempotency behavior tests for retry/cancel/restart on long-running CSV jobs using `s3storage` state.
- [ ] 📌 Planned: benchmark throughput and part-size tuning after migration to ensure no regression in export pipelines.

### Execution pack D - cross-service governance and release gates

- [ ] ⬜ Incomplete: add repo-wide static check preventing new direct `boto3/aioboto3` imports in non-storage services.
- [ ] 🟡 In Progress: add `docs/codebases/*` dependency tables listing each service's storage integration mode (`direct`, `hybrid`, `s3storage`).
- [ ] ⬜ Incomplete: publish storage migration runbook with rollback steps by service.
- [ ] ⬜ Incomplete: add SLOs for end-to-end storage operations consumed by `appointment360`, `admin`, and `jobs`.
- [ ] 📌 Planned: require "storage control plane compliance" gate in each minor release checklist.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: baseline FastAPI service, bucket/object APIs, backend abstraction, and Lambda deployment are in place.
- [x] ✅ Completed: multipart durability and metadata worker env-driven wiring are implemented.
- [ ] 🟡 In Progress: finalize strict contract evidence and parity checks for foundational endpoint behavior.

### `1.x.x - Contact360 user and billing and credit system`

- [x] ✅ Completed: avatar/photo/resume object class paths exist and are available to caller services.
- [ ] 🟡 In Progress: harden object-class validation policies and caller-level error normalization.
- [ ] ⬜ Incomplete: complete audit-grade actor/source metadata coverage for billing/identity artifact writes.

### `2.x.x - Contact360 email system`

- [x] ✅ Completed: multipart CSV upload lifecycle and metadata extraction pipeline are live.
- [ ] ⬜ Incomplete: enforce idempotency for initiate/complete/abort under client retries.
- [ ] ⬜ Incomplete: complete end-to-end failure-path tests for bulk upload worker flows.

### `3.x.x - Contact360 contact and company data system`

- [ ] 🟡 In Progress: analysis endpoints (schema/preview/stats) provide ingestion-support capabilities.
- [ ] ⬜ Incomplete: add lineage contract linking upload artifacts to downstream ingestion/index runs.
- [ ] 📌 Planned: optimize high-cardinality analysis performance for larger enrichment datasets.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [ ] 🟡 In Progress: extension/salesnavigator storage usage is partially supported through current bucket/key model.
- [ ] ⬜ Incomplete: enforce extension-channel constraints (TTL/prefix/access policy) as explicit contracts.
- [ ] 📌 Planned: add channel-specific observability and provenance evidence for extension-origin objects.

### `5.x.x - Contact360 AI workflows`

- [ ] 📌 Planned: define AI artifact class contracts and access/retention controls.
- [ ] ⬜ Incomplete: add sensitive-object policy guards and immutable storage mode where required.
- [ ] 📌 Planned: add AI lineage overlays (source file -> run -> output artifacts) in metadata contract.

### `6.x.x - Contact360 Reliability and Scaling`

- [x] ✅ Completed: optimistic concurrency for metadata updates and durable multipart session state.
- [ ] ⬜ Incomplete: add explicit upload/metadata SLO implementation and error-budget monitoring.
- [ ] 🟡 In Progress: improve resilience with broader transient failure handling and compatibility tests.

### `7.x.x - Contact360 deployment`

- [x] ✅ Completed: API key boundary and runtime CORS allowlist validation exist in service config.
- [ ] ⬜ Incomplete: align SAM template CORS with runtime strict allowlist model.
- [ ] ⬜ Incomplete: sanitize deploy config files (`samconfig.toml` and related examples) to remove secret-like values.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 🟡 In Progress: endpoint surface is broad enough for API productization, but formal external contract is partial.
- [ ] ⬜ Incomplete: publish version/deprecation contract and compatibility test suite.
- [ ] 📌 Planned: provide SDK-grade usage examples and lifecycle webhook/event contract.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 📌 Planned: define entitlement-aware storage capability matrix and quota policy model.
- [ ] ⬜ Incomplete: implement quota/metering headers and tenant throttling paths.
- [ ] 📌 Planned: add residency/cost attribution overlays and ecosystem support diagnostics.

### `10.x.x - Contact360 email campaign`

- [ ] 📌 Planned: define campaign artifact contracts and reproducibility expectations.
- [ ] ⬜ Incomplete: implement compliance-grade immutability and evidence linkage for campaign objects.
- [ ] 📌 Planned: add final campaign-era governance gates using storage lineage/compliance checks.

## Release gate checklist for each minor

- Contract compatibility validated (and documented).
- Service changes covered by integration and failure-path tests.
- Data lineage/metadata integrity checks passing.
- Ops telemetry and alerts updated for new behavior.
- Rollback plan validated before release promotion.

## 2026 Gap Register (actionable)

### P0
- [x] ✅ `S3S-0.1`: Enforce API auth on all non-health endpoints.
- [x] ✅ `S3S-0.3`: Replace in-memory multipart sessions with durable shared store.
- [x] ✅ `S3S-0.4`: Remove hardcoded metadata worker function name.
- [ ] ⬜ Incomplete: `S3S-0.5` Add idempotency keys for initiate/complete/upload paths.
- [ ] ⬜ Incomplete: `S3S-0.6` Sanitize deployment config (`samconfig.toml`) to remove real-looking secrets.
- [ ] ⬜ Incomplete: `S3S-0.7` Enforce session-bound bucket validation in multipart complete path.

### P1/P2
- [ ] 📌 Planned: `S3S-1.x` Scoped keys, metering, quota headers.
- [ ] 📌 Planned: `S3S-2.x` Object classification and lineage metadata contracts.
- [ ] 🟡 In Progress: `S3S-2.1` Eliminate direct `_backend` access and keep endpoint layer backend-agnostic.
- [ ] 🟡 In Progress: `S3S-2.2` Align SAM CORS policy with runtime allowlist model.

### P3+
- [ ] 📌 Planned: `S3S-3.1` Distributed rate limiting.
- [ ] 📌 Planned: `S3S-4.x` OpenAPI parity and immutable audit events.
- [ ] 📌 Planned: `S3S-5.x` Lifecycle webhooks and campaign evidence bundle support.

