# Jobs Codebase Analysis (`contact360.io/jobs`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`contact360.io/jobs` is Contact360's asynchronous execution engine (TKD Job scheduler). It manages long-running, retryable workflows for email export/verify/pattern import, Contact360 import/export, and DAG execution states (`job_node`, `edges`, `job_events`) that upstream surfaces consume through Appointment360.

---

## Runtime architecture snapshot

- Runtime: FastAPI + async SQLAlchemy + PostgreSQL + Kafka + async worker pool.
- Control planes: scheduler (`app/workers/scheduler.py`), consumer (`app/workers/consumer.py`), workers (`app/workers/worker_pool.py`).
- API layer: `app/api/main.py`, `app/api/v1/routes/jobs.py`, `app/api/v1/routes/metrics.py`.
- Processor registry: `app/processors/registry.py` with stream processors.
- Data/repo layer: `app/models/*`, `app/repositories/*`, `app/services/job_service.py`.
- Dependencies: S3, email API, Contact360 Postgres/OpenSearch, Kafka.

---

## Verified completion status from runtime

- [x] ✅ Job lifecycle and DAG orchestration are implemented with status transitions and dependency degree handling.
- [x] ✅ Retry model is explicit (`retry` status path), with retry interval and run-after scheduling.
- [x] ✅ Timeline/event tracking exists through `job_events` and timeline endpoints.
- [x] ✅ Health (`/health`, `/health/live`, `/health/ready`) and metrics (`/api/v1/metrics`, `/stats`) are implemented.
- [x] ✅ Core stream processors exist for email finder, email verify, email pattern import, and Contact360 import/export.
- [x] ✅ Stale `processing` recovery loop exists in scheduler for resilience.

## Active risks and gap map

### Security and governance gaps

- [ ] ⬜ Incomplete: authentication is single shared `X-API-Key` without scoped service/user/tenant authorization.
- [ ] 🟡 In Progress: rate limiting middleware exists, but governance policy for high-risk endpoints is not fully versioned/documented.
- [ ] ⬜ Incomplete: partner/public API hardening for future ecosystem access is not complete.

### Logging and observability drift

- [ ] ⬜ Incomplete: production processors still contain raw `print()` statements in critical paths (`email_finder_export_stream`, `email_verify_export_stream`).
- [ ] 🟡 In Progress: structured metrics/events exist, but full canonical log unification to `logs.api` is incomplete.
- [ ] ⬜ Incomplete: cross-service trace correlation and log schema normalization are not fully enforced.

### Storage/control-plane drift

- [ ] ⬜ Incomplete: jobs service still performs direct S3 client operations (`boto3`/`aioboto3`) rather than fully mediated `s3storage` control-plane calls.
- [ ] 🟡 In Progress: checkpointed multipart logic is robust, but storage governance is split between direct S3 and shared storage-service strategy.
- [ ] 📌 Planned: migrate all new file/object operations to `s3storage` contracts with strict release gates.

### Reliability and product scope gaps

- [ ] 🟡 In Progress: stale-job recovery exists, but degree-decrement failures can still block downstream DAG progress.
- [ ] ⬜ Incomplete: idempotent submission keys for duplicate prevention are not consistently enforced at job creation APIs.
- [ ] ⬜ Incomplete: campaign-specific processor set (`10.x.x`) is not implemented yet.
- [ ] 📌 Planned: AI and campaign orchestration packs with stronger quota and cost controls.

---

## Cross-service dependency map (release gating)

- [x] ✅ `contact360.io/jobs` <- `contact360.io/api` (job creation/status orchestration).
- [x] ✅ `contact360.io/jobs` -> `lambda/emailapis` / `lambda/emailapigo` (email find/verify processing).
- [x] ✅ `contact360.io/jobs` -> S3 object storage (input/output CSV artifacts).
- [x] ✅ `contact360.io/jobs` -> Contact360 Postgres/OpenSearch for import/export pipelines.
- [ ] 🟡 In Progress: `contact360.io/jobs` -> `lambda/logs.api` canonical runtime logging.
- [ ] 🟡 In Progress: `contact360.io/jobs` -> `lambda/s3storage` as canonical storage control plane.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Existing direct S3 operations are well-structured (multipart, checkpoint resume, head/list/object flows).
- [ ] ⬜ Incomplete: direct `boto3`/`aioboto3` usage still exists in jobs clients/processors.
- [ ] 🟡 In Progress: migration design needed to route upload/download/session operations through `s3storage`.
- [ ] 📌 Planned: block any new direct S3 usage with policy and CI checks.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [x] ✅ Structured logging framework and metrics collector are present.
- [ ] ⬜ Incomplete: raw `print()` remains in email stream processors.
- [ ] 🟡 In Progress: centralize event and error emission into `logs.api` sink schema for all worker stages.
- [ ] 📌 Planned: remove local-only logging patterns and enforce structured logger adapters.

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core job/DAG API contracts and schema models are implemented.
- [ ] 🟡 In Progress: align retry/idempotency semantics across docs, Appointment360, and jobs endpoints.
- [ ] ⬜ Incomplete: add submission idempotency key contract for create endpoints.
- [ ] ⬜ Incomplete: campaign processor contracts for `10.x.x` are absent.
- [ ] 📌 Planned: publish partner-safe public/private contract boundaries.

### Service pack

- [x] ✅ Scheduler, consumer, worker pool, processors, and repository layers are functional.
- [ ] 🟡 In Progress: harden dependent degree decrement and blocked-DAG recovery pathways.
- [ ] ⬜ Incomplete: remove `print()` and complete structured logging migration.
- [ ] ⬜ Incomplete: migrate direct S3 calls to `s3storage` control plane abstractions.
- [ ] 📌 Planned: add AI/campaign job processor modules.

### Surface pack

- [x] ✅ Status, timeline, dag, retry, and metrics endpoints are present for UI/API consumers.
- [ ] 🟡 In Progress: improve deterministic error envelopes for downstream surfaces.
- [ ] ⬜ Incomplete: expose richer progress metadata for campaign/large-batch operational UX.
- [ ] ⬜ Incomplete: add operator-level diagnostics endpoints for blocked DAG paths.
- [ ] 📌 Planned: partner and ecosystem-facing job controls.

### Data pack

- [x] ✅ `job_node`, `edges`, `job_events` and checkpoint metadata patterns are implemented.
- [ ] 🟡 In Progress: strengthen lineage from inputs -> processing -> outputs across all job types.
- [ ] ⬜ Incomplete: standardize audit evidence fields for billing/credits/campaign compliance.
- [ ] ⬜ Incomplete: enforce idempotent duplicate suppression evidence at persistence layer.
- [ ] 📌 Planned: tenant-partition and campaign-compliance data models.

### Ops pack

- [x] ✅ Health/readiness/liveness + metrics endpoints and recovery loops are available.
- [ ] 🟡 In Progress: tighten SLO/error-budget definitions and alerting thresholds.
- [ ] ⬜ Incomplete: deployment runbook gates for scheduler/consumer/worker coordination are incomplete.
- [ ] ⬜ Incomplete: controlled backpressure and queue overflow strategy needs formalization.
- [ ] 📌 Planned: multi-tenant workload fairness and autoscaling policy.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ Base scheduler architecture, DAG validation, and worker execution model are established.
- [x] ✅ Core DB schema and API routes are in place.
- [ ] 🟡 In Progress: normalize foundational governance docs with runtime semantics (retry/status transitions).
- [ ] ⬜ Incomplete: replace remaining ad-hoc logs and direct infrastructure shortcuts.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ Hooks for usage/billing metadata can flow via job payloads.
- [ ] 🟡 In Progress: attach stricter billing/credit consumption metadata to all relevant jobs.
- [ ] ⬜ Incomplete: scoped authz model (beyond shared API key) for billing-sensitive operations.
- [ ] 📌 Planned: tenant-level budget enforcement and reconciliation exports.

### `2.x.x` - Contact360 email system

- [x] ✅ Email finder/verify/pattern import streaming processors are implemented.
- [x] ✅ Multipart checkpoint/resume flow is present for large CSV jobs.
- [ ] 🟡 In Progress: improve provider-unified semantics and deterministic status mapping.
- [ ] ⬜ Incomplete: remove raw `print()` and complete logs/storage unification in email paths.

### `3.x.x` - Contact360 contact and company data system

- [x] ✅ Contact360 import/export and VQL validation endpoints exist.
- [ ] 🟡 In Progress: harden lineage consistency across Postgres/OpenSearch write and replay paths.
- [ ] ⬜ Incomplete: complete dedupe/conflict evidence and replay safety guarantees.
- [ ] 📌 Planned: richer provenance linking for contact/company mutations.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] 🟡 In Progress: extension/sales-origin jobs are partially represented through shared contracts.
- [ ] ⬜ Incomplete: explicit source-tagged processing tracks and diagnostics are incomplete.
- [ ] 📌 Planned: dedicated extension/sales ingestion packs with drift monitoring.

### `5.x.x` - Contact360 AI workflows

- [ ] ⬜ Incomplete: AI-specific batch orchestration processors are not fully implemented.
- [ ] 🟡 In Progress: foundational queue/worker architecture is ready for AI packs.
- [ ] 📌 Planned: AI job envelopes (cost/confidence/model metadata) and guardrails.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ Recovery loops, retry scheduling, and metrics surfaces provide a reliability base.
- [ ] 🟡 In Progress: tune blocked-DAG handling and queue backpressure controls.
- [ ] ⬜ Incomplete: fully distributed idempotency and duplicate suppression controls.
- [ ] 📌 Planned: formal SLOs, chaos tests, and autoscaling playbooks.

### `7.x.x` - Contact360 deployment

- [x] ✅ Deployable API/scheduler/consumer CLI paths are present.
- [ ] 🟡 In Progress: deployment guardrails for coordinated component startup/shutdown.
- [ ] ⬜ Incomplete: release checklist for key rotation, scoped auth, and storage/log gates.
- [ ] 📌 Planned: progressive deployment strategy with workload migration safety.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ Private API surfaces for job operations are established.
- [ ] 🟡 In Progress: endpoint contract hardening and version/deprecation policy.
- [ ] ⬜ Incomplete: partner/public-safe credentials and callback/webhook model not finalized.
- [ ] 📌 Planned: productized external API layer with compatibility tests.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] 🟡 In Progress: current architecture can support ecosystem integrations but governance is partial.
- [ ] ⬜ Incomplete: tenant-aware quotas/fairness and integration lifecycle controls are incomplete.
- [ ] 📌 Planned: platform-grade orchestration controls and partner observability.

### `10.x.x` - Contact360 email campaign

- [ ] ⬜ Incomplete: campaign send/orchestration processors and lifecycle endpoints are missing.
- [ ] ⬜ Incomplete: campaign compliance and immutable audit bundles are incomplete.
- [ ] 📌 Planned: campaign execution timeline + delivery verification + suppression controls.
- [ ] 📌 Planned: campaign release gates linking billing, logs, storage, and compliance evidence.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove all `print()` in processors and route logs through structured/canonical logging.
- [ ] 🟡 In Progress: design and execute direct S3 -> `s3storage` migration for jobs file operations.
- [ ] ⬜ Incomplete: add idempotency key enforcement for create-job endpoints.
- [ ] ⬜ Incomplete: harden auth model from shared API key to scoped service/tenant credentials.
- [ ] 🟡 In Progress: improve DAG blocked-path handling and observability for downstream failures.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete: eliminate raw `print()` and finalize logging unification (`logs.api` compatible pipeline).
- [ ] ⬜ Incomplete: establish secure/scoped auth strategy beyond shared `X-API-Key`.
- [ ] ⬜ Incomplete: complete storage control-plane migration path to `s3storage`.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress: add idempotent submission + duplicate suppression for create flows.
- [ ] 🟡 In Progress: improve blocked-DAG and degree-decrement failure remediation paths.
- [ ] 📌 Planned: expand operational diagnostics and release-gate coverage.

### P3+ - platform productization

- [ ] 📌 Planned: AI orchestration job packs and governance controls.
- [ ] 📌 Planned: full campaign (`10.x.x`) processors, compliance timelines, and platform-facing APIs.
