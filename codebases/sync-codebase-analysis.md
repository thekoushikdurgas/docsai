# Sync Codebase Analysis (`contact360.io/sync`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`contact360.io/sync` (Connectra runtime) is Contact360's contact/company data plane service. It provides VQL-based querying, parallel upsert pipelines across PostgreSQL and Elasticsearch, filter metadata hydration, and background import/export jobs using S3-backed CSV workflows.

---

## Runtime architecture snapshot

- Runtime: Go (Gin + Cobra + Zerolog).
- Entry points: `main.go`, `cmd/server.go`, `cmd/jobs.go`.
- API modules: `modules/contacts`, `modules/companies`, `modules/common`.
- Query engine: `utilities/query.go` (VQL -> Elasticsearch bool query compiler).
- Data model: PostgreSQL + Elasticsearch dual-store model with repository layer.
- Jobs: polling workers in `jobs/jobs.go` with claim-and-transition status model.
- Middleware: token-bucket rate limiting + API key authentication.

---

## Verified completion status from runtime

- [x] ✅ Contact and company query/count/batch-upsert endpoints are implemented.
- [x] ✅ VQL compiler supports text, keyword, range, sorting, pagination, and cursor/search-after patterns.
- [x] ✅ Parallel write orchestration is implemented for contacts/companies/filter-data upserts.
- [x] ✅ Job runners for `first_time` and `retry` modes are implemented with recovery of in-flight states.
- [x] ✅ API key auth and rate limiter middleware are active in server route chain.
- [x] ✅ Health endpoint and graceful shutdown handling are present.

## Active risks and gap map

### Security and authz model

- [ ] ⬜ Incomplete: authentication is shared `X-API-Key` only; no scoped key, tenant, or role-level authorization.
- [ ] 🟡 In Progress: CORS allowlist is environment-configurable, but governance for production origin policy requires stricter release gates.
- [ ] ⬜ Incomplete: service-level audit and key-rotation evidence is not first-class in runtime contract.

### Logging and observability drift

- [ ] 🟡 In Progress: structured logging exists, but legacy direct output patterns still exist in codebase (`clients/mongo.go` uses `fmt.Println`).
- [ ] ⬜ Incomplete: canonical log-unification path (`logs.api`) is not explicitly integrated as single sink.
- [ ] ⬜ Incomplete: route-level error budget/SLO evidence endpoints are incomplete for platform governance.

### Storage/control-plane drift

- [ ] ⬜ Incomplete: sync runtime still uses direct S3 connections/clients for presigned upload and job file operations.
- [ ] 🟡 In Progress: direct S3 patterns are functional, but Contact360 standard calls for migration toward `s3storage` control plane where possible.
- [ ] 📌 Planned: block new direct storage integrations and enforce mediated storage contracts.

### Product completeness and roadmap gaps

- [ ] 🟡 In Progress: contact/company core is strong, but extension/sales/AI/campaign-specific modules are only partially represented through generic pipelines.
- [ ] ⬜ Incomplete: campaign-specific data orchestration and compliance packs (`10.x.x`) are not complete.
- [ ] 📌 Planned: richer ecosystem/public API lifecycle contracts with versioned boundaries.

---

## Cross-service dependency map (release gating)

- [x] ✅ `contact360.io/sync` <- `contact360.io/api` (Appointment360 gateway consumption).
- [x] ✅ `contact360.io/sync` -> PostgreSQL and Elasticsearch for hybrid read/write behavior.
- [x] ✅ `contact360.io/sync` -> S3 for upload URL generation and CSV job streams.
- [ ] 🟡 In Progress: `contact360.io/sync` -> `lambda/logs.api` canonical logging integration.
- [ ] 🟡 In Progress: `contact360.io/sync` -> `lambda/s3storage` storage-control-plane alignment.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Direct S3 integration currently powers upload and CSV job flows.
- [ ] ⬜ Incomplete: no abstraction layer currently enforces `s3storage` mediation for storage operations.
- [ ] 🟡 In Progress: plan migration of upload URL and job file I/O surfaces to shared storage control plane.
- [ ] 📌 Planned: add CI/release checks preventing new direct S3 call sites.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [x] ✅ Zerolog-based structured logging is widely used.
- [ ] 🟡 In Progress: remove remaining direct output/debug paths (e.g., `fmt.Println` in Mongo command monitor).
- [ ] ⬜ Incomplete: define and enforce canonical `logs.api` event schema for this service.
- [ ] 📌 Planned: include correlation IDs and cross-service trace propagation contract.

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Contact/company/common API contract surface is stable and implemented.
- [ ] 🟡 In Progress: align VQL contract docs with gateway-facing expectations and examples.
- [ ] ⬜ Incomplete: scoped-auth contract (tenant/user/service scope) is missing.
- [ ] ⬜ Incomplete: versioned external/partner API boundary is not finalized.
- [ ] 📌 Planned: campaign and ecosystem contract packs for later eras.

### Service pack

- [x] ✅ Parallel upsert and hybrid query service patterns are implemented.
- [ ] 🟡 In Progress: harden service governance around storage/logging unification.
- [ ] ⬜ Incomplete: remove remaining legacy direct output/log calls.
- [ ] ⬜ Incomplete: migrate direct S3 pathways toward shared storage control plane.
- [ ] 📌 Planned: AI/campaign-specific service modules and orchestration.

### Surface pack

- [x] ✅ Core endpoints for data fetch, count, upload-url, filters, and jobs are available.
- [ ] 🟡 In Progress: improve deterministic error envelopes and operator diagnostics.
- [ ] ⬜ Incomplete: richer status/timeline API for operational UIs and external consumers.
- [ ] ⬜ Incomplete: public-facing endpoint productization docs and guardrails.
- [ ] 📌 Planned: partner-safe endpoint catalog and onboarding surfaces.

### Data pack

- [x] ✅ Dual-store data model (PG + ES) and deterministic UUID-based dedupe are implemented.
- [ ] 🟡 In Progress: improve reconciliation evidence between ES and PG at runtime.
- [ ] ⬜ Incomplete: stronger lineage/audit data for billing/compliance/campaign readiness.
- [ ] ⬜ Incomplete: explicit idempotency evidence on all create-job paths.
- [ ] 📌 Planned: tenant partitioning and compliance lineage upgrades.

### Ops pack

- [x] ✅ Graceful shutdown and in-flight job recovery paths are implemented.
- [ ] 🟡 In Progress: harden runtime SLO/error-budget monitoring and alerting.
- [ ] ⬜ Incomplete: deployment and key-rotation governance evidence is incomplete.
- [ ] ⬜ Incomplete: formal release gate matrix for storage/logging/auth drift not complete.
- [ ] 📌 Planned: multi-tenant scaling policies and workload isolation controls.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ Go service scaffold, middleware chain, hybrid data architecture, and VQL core are established.
- [x] ✅ Core contact/company/common routes and health endpoint exist.
- [ ] 🟡 In Progress: foundational governance docs and release-gate parity need normalization.
- [ ] ⬜ Incomplete: remove residual legacy logging patterns and tighten baseline security posture.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ Service can support usage-aware workflows through gateway orchestration.
- [ ] 🟡 In Progress: add stronger billing/credit attribution evidence in job and request metadata.
- [ ] ⬜ Incomplete: scoped authz model for credit-sensitive operations.
- [ ] 📌 Planned: tenant-aware quota and billing policy enforcement.

### `2.x.x` - Contact360 email system

- [x] ✅ CSV import/export and email-adjacent data pipelines are implemented via jobs.
- [ ] 🟡 In Progress: keep data-plane contracts aligned with email finder/verifier service evolution.
- [ ] ⬜ Incomplete: full storage/logging standardization for email-heavy pipelines.
- [ ] 📌 Planned: richer email campaign data readiness hooks.

### `3.x.x` - Contact360 contact and company data system

- [x] ✅ This is the primary implemented strength era (VQL + dual-store + batch upsert).
- [x] ✅ Filter metadata and count/list pathways are implemented.
- [ ] 🟡 In Progress: strengthen reconciliation and drift-detection automation.
- [ ] ⬜ Incomplete: complete high-fidelity lineage for operational and compliance views.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] 🟡 In Progress: core data APIs can serve extension/sales use cases via gateway.
- [ ] ⬜ Incomplete: explicit extension/sales provenance and diagnostics contracts are limited.
- [ ] 📌 Planned: dedicated sync surfaces for extension/Sales Navigator ingestion quality.

### `5.x.x` - Contact360 AI workflows

- [ ] ⬜ Incomplete: AI-specific data enrichment modules are not first-class in this runtime.
- [ ] 🟡 In Progress: existing hybrid query architecture is reusable for AI contexts.
- [ ] 📌 Planned: AI-ready metadata contracts and enrichment support modules.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ Worker recovery and claim-based job processing provide a resilience baseline.
- [ ] 🟡 In Progress: improve SLO visibility and advanced failure diagnostics.
- [ ] ⬜ Incomplete: full idempotency/replay protections across all write and job-create paths.
- [ ] 📌 Planned: reliability scorecards and chaos/fault tests.

### `7.x.x` - Contact360 deployment

- [x] ✅ Dockerized runtime and CLI command modes are present.
- [ ] 🟡 In Progress: deployment governance around auth/keys/storage/logging still maturing.
- [ ] ⬜ Incomplete: production runbook and release-gate evidence not fully standardized.
- [ ] 📌 Planned: staged rollout and rollback-safe data migration controls.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ Private APIs are operational for internal platform use.
- [ ] 🟡 In Progress: clarify and enforce private/public contract boundaries.
- [ ] ⬜ Incomplete: partner-safe API model, key scopes, and lifecycle versioning.
- [ ] 📌 Planned: productized API docs and compatibility policy.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] 🟡 In Progress: architecture can support ecosystem growth, but governance is partial.
- [ ] ⬜ Incomplete: integration lifecycle controls, quotas, and platform observability are incomplete.
- [ ] 📌 Planned: ecosystem-grade connector and tenant controls.

### `10.x.x` - Contact360 email campaign

- [ ] ⬜ Incomplete: dedicated campaign orchestration/compliance features are not complete in sync runtime.
- [ ] ⬜ Incomplete: campaign evidence pipelines and suppression/compliance contracts are incomplete.
- [ ] 📌 Planned: campaign-ready audience/export safeguards and immutable audit support.
- [ ] 📌 Planned: integrated campaign runtime dependency gates across sync/gateway/jobs.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove residual direct output logging and finish log-unification path.
- [ ] 🟡 In Progress: design and execute direct S3 -> `s3storage` migration plan for sync runtime.
- [ ] ⬜ Incomplete: implement scoped API credentials (tenant/service-level) beyond shared API key.
- [ ] ⬜ Incomplete: add idempotency evidence and duplicate prevention for job creation paths.
- [ ] 🟡 In Progress: introduce reconciliation/lineage evidence checks between Elasticsearch and PostgreSQL.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete: secure auth model hardening beyond shared API key.
- [ ] ⬜ Incomplete: complete storage-control-plane and log-unification compliance for runtime.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress: reconciliation and lineage observability between ES/PG.
- [ ] 🟡 In Progress: standardized error envelopes and SLO readiness for platform operations.
- [ ] 📌 Planned: versioned endpoint governance and partner-safe contract expansion.

### P3+ - platform productization

- [ ] 📌 Planned: AI and ecosystem integration maturity packs.
- [ ] 📌 Planned: full `10.x.x` campaign readiness and compliance controls.
