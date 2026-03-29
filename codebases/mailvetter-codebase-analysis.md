# Mailvetter Codebase Analysis (`backend(dev)/mailvetter`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`backend(dev)/mailvetter` is Contact360's deep email-verification engine for synchronous and async bulk checks. It runs as split API/worker Go services with Redis queueing and PostgreSQL result persistence, and is the verification backbone for email quality before downstream outreach and campaign execution.

---

## Verified completion status from runtime

- [x] ✅ Auth-protected v1 verifier API is implemented (`/v1/emails/validate`, `/v1/emails/validate-bulk`, `/v1/jobs/:job_id`, `/v1/jobs/:job_id/results`).
- [x] ✅ Bulk ingestion pipeline exists: dedupe -> create job -> enqueue Redis tasks -> worker execution.
- [x] ✅ Worker writes result rows and transactional job progress counters.
- [x] ✅ Webhook dispatch with HMAC signature and retry loop is implemented.
- [x] ✅ Result export supports JSON and CSV.
- [x] ✅ Job retention cleanup loop (30-day delete) is implemented in worker runtime.
- [x] ✅ Rate-limit headers are emitted and plan-aware rate limiting logic is present.

## Active risks and gap map

### Contract and API surface

- [ ] ⬜ Incomplete: legacy endpoints (`/verify`, `/upload`, `/status`, `/results`) are still live, causing contract drift.
- [ ] 🟡 In Progress: v1 routes are operational, but full deprecation gates and migration messaging for legacy consumers are missing.
- [ ] ⬜ Incomplete: status lifecycle is effectively `pending/completed`; explicit `failed` and `completed_with_errors` paths are not fully formalized.
- [ ] 📌 Planned: canonical OpenAPI contract + parity test suite for all v1 endpoints.

### Auth, multitenancy, and security

- [ ] ⬜ Incomplete: auth middleware still supports fallback to single shared `API_SECRET_KEY`.
- [ ] ⬜ Incomplete: webhook secret falls back to API secret, weakening separation of duties.
- [ ] 🟡 In Progress: API-key plan controls exist, but tenant-level key governance and rotation policy are incomplete.
- [ ] 📌 Planned: scoped service/tenant key model aligned with Contact360 private APIs.

### Reliability and ops

- [ ] 🟡 In Progress: Redis-backed limiter exists, but operationally hardened distributed limits and outage behavior need completion.
- [ ] ⬜ Incomplete: no idempotency key/duplicate-submission guard on bulk job creation.
- [ ] ⬜ Incomplete: schema migrations run at service startup in runtime, increasing deploy risk.
- [ ] ⬜ Incomplete: worker and API logs rely on `fmt/log` and are not fully unified with `logs.api` governance.
- [ ] 📌 Planned: cross-service trace propagation and SLO/error-budget evidence.

---

## Cross-service dependency map (release gating)

- [x] ✅ `contact360.io/api` and related backend services can consume mailvetter verification APIs.
- [x] ✅ `mailvetter` depends on Redis (`tasks:verify`) for async task transport.
- [x] ✅ `mailvetter` depends on PostgreSQL (`jobs`, `results`) for state and payload storage.
- [x] ✅ webhook callbacks provide outbound integration points for async completion events.
- [ ] 🟡 In Progress: formalized consumer contract mapping in `docs/backend/apis` and endpoint matrix.
- [ ] 📌 Planned: campaign-runtime verification orchestration contract with `backend(dev)/email campaign`.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Core mailvetter runtime currently centers on DB + Redis and does not require direct S3 for primary verification pipeline.
- [ ] 📌 Planned: if export artifacts move to object storage, enforce `s3storage` control-plane mediation instead of direct SDK writes.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [ ] ⬜ Incomplete: API and worker use `fmt.Printf`, `log.Println`, `log.Printf` extensively in runtime code.
- [ ] 🟡 In Progress: some operational metadata exists, but structured log schema and correlation IDs are incomplete.
- [ ] 📌 Planned: emit canonical verification/audit events to `logs.api` with trace and tenant context.

---

## Current execution packs (small tasks)

### Contract pack

- [x] ✅ Core v1 endpoint set and response shapes are implemented.
- [ ] 🟡 In Progress: route canonicalization around `/v1/*` with documented migration path.
- [ ] ⬜ Incomplete: decommission legacy endpoints and static legacy route dependencies.
- [ ] ⬜ Incomplete: status-state contract hardening (`pending`, `processing`, `completed`, `failed`, optional `completed_with_errors`).
- [ ] 📌 Planned: endpoint parity tests plus generated OpenAPI as canonical truth.

### Service pack

- [x] ✅ Bulk job service and worker execution model are implemented.
- [x] ✅ verification scoring and detail payload generation are implemented.
- [ ] 🟡 In Progress: plan-aware limits and concurrency controls are partially mature.
- [ ] ⬜ Incomplete: idempotency keys and duplicate-bulk safeguards.
- [ ] 📌 Planned: richer failure taxonomy and retry/requeue policy controls.

### Surface pack

- [x] ✅ JSON/CSV results and progress endpoints are available.
- [ ] 🟡 In Progress: consumer-facing consistency between job state and result payload semantics.
- [ ] ⬜ Incomplete: legacy static UI remains coupled to deprecated endpoints.
- [ ] 📌 Planned: standardized UI integration contracts for dashboard, extension, and campaign surfaces.

### Data pack

- [x] ✅ `jobs` and `results` schema plus indices are in place.
- [x] ✅ result JSON payload capture exists.
- [ ] 🟡 In Progress: retention logic exists, but policy-level governance and evidence are incomplete.
- [ ] ⬜ Incomplete: migration discipline (separate migration pipeline) and schema version governance.
- [ ] 📌 Planned: lineage model linking verification jobs to contacts/campaign recipients.

### Ops pack

- [x] ✅ graceful worker shutdown and cleanup loops are implemented.
- [ ] 🟡 In Progress: rate limiting and webhook retries exist, but production observability is incomplete.
- [ ] ⬜ Incomplete: secrets hardening and auth/webhook secret separation.
- [ ] ⬜ Incomplete: full structured logging and cross-service trace propagation.
- [ ] 📌 Planned: release gates and runbooks for high-volume verification events.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ service bootstrap, API+worker split, Redis/Postgres plumbing, and core schema creation are implemented.
- [x] ✅ baseline health route and runtime startup flow are implemented.
- [ ] 🟡 In Progress: foundational hardening for migration discipline and structured operations.
- [ ] ⬜ Incomplete: remove legacy compatibility debt from bootstrap runtime.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ API-key plan framework exists and is used for limits.
- [ ] 🟡 In Progress: owner-key usage patterns partially support tenancy accounting.
- [ ] ⬜ Incomplete: billing/credit-grade usage attribution and scoped key governance.
- [ ] 📌 Planned: integration to centralized Contact360 credit and entitlement system.

### `2.x.x` - Contact360 email system

- [x] ✅ primary verification era is operational: single/bulk verification and job result retrieval.
- [x] ✅ SMTP/DNS/disposable/catch-all signal pipeline is implemented.
- [ ] 🟡 In Progress: contract tightening for status taxonomy and deterministic failure envelopes.
- [ ] ⬜ Incomplete: idempotency + bulk duplicate protections.

### `3.x.x` - Contact360 contact and company data system

- [x] ✅ result payload includes rich verification evidence in JSON for downstream mapping.
- [ ] 🟡 In Progress: partial linkage readiness to contact/company records.
- [ ] ⬜ Incomplete: explicit lineage references between verification result and contact/entity IDs.
- [ ] 📌 Planned: first-class contract for contact/company-integrated verification workflows.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] 🟡 In Progress: APIs can serve extension/SN ingress through upstream services.
- [ ] ⬜ Incomplete: explicit anti-abuse and provenance contract for extension-originated bulk jobs.
- [ ] 📌 Planned: extension/SN verification orchestration templates and source tagging.

### `5.x.x` - Contact360 AI workflows

- [x] ✅ verifier already produces explainable signals useful for AI scoring layers.
- [ ] 🟡 In Progress: alignment of score-details schema for AI consumers.
- [ ] ⬜ Incomplete: formal AI-ready output contract and confidence normalization policy.
- [ ] 📌 Planned: verifier outputs wired as first-class features in AI workflow packs.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ worker concurrency control, queue polling backoff, graceful shutdown, and cleanup loops are implemented.
- [ ] 🟡 In Progress: Redis-backed limiting and retry behavior provide partial resilience.
- [ ] ⬜ Incomplete: full idempotency, failure-state handling, and SLO/error-budget instrumentation.
- [ ] 📌 Planned: chaos/load testing and capacity gates for high-volume batches.

### `7.x.x` - Contact360 deployment

- [x] ✅ containerized deployment shape exists (API/worker/Redis/Postgres compositions).
- [ ] 🟡 In Progress: deployment readiness with existing startup migration behavior.
- [ ] ⬜ Incomplete: explicit migration pipeline and blue/green-safe rollout controls.
- [ ] 📌 Planned: hardened production runbooks and secret management policy.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ private authenticated endpoint model exists.
- [ ] 🟡 In Progress: rate limit headers and plan controls are present but governance is partial.
- [ ] ⬜ Incomplete: public/private API formalization, scoped key models, and strict contract publishing.
- [ ] 📌 Planned: full v1 OpenAPI plus compatibility guarantees.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [x] ✅ webhook callback mechanism provides integration primitive.
- [ ] 🟡 In Progress: retry/signed delivery exists but ecosystem governance is partial.
- [ ] ⬜ Incomplete: partner-grade webhook observability, replay tooling, and contract lifecycle.
- [ ] 📌 Planned: integration marketplace-grade connector patterns.

### `10.x.x` - Contact360 email campaign

- [x] ✅ verification job outputs can serve campaign recipient preflight checks.
- [ ] 🟡 In Progress: campaign systems can consume validity scores and summary outputs.
- [ ] ⬜ Incomplete: dedicated campaign preflight contract and verification gating policies.
- [ ] 📌 Planned: full campaign orchestration with recipient-level verification evidence and suppression flows.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove legacy API routes and lock v1 as canonical.
- [ ] ⬜ Incomplete: decouple `WEBHOOK_SECRET_KEY` from API secret fallback.
- [ ] ⬜ Incomplete: add idempotency keys and duplicate-submission protection for bulk jobs.
- [ ] 🟡 In Progress: complete distributed limiter hardening and outage behavior strategy.
- [ ] ⬜ Incomplete: move migrations out of runtime startup into controlled pipeline.
- [ ] 🟡 In Progress: standardize status model and add explicit failed/completed_with_errors semantics.
- [ ] ⬜ Incomplete: migrate runtime logging to unified structured schema (`logs.api` aligned).

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete (`MV-0`): freeze canonical API on `/v1/*` and retire legacy endpoint usage.
- [ ] ⬜ Incomplete (`MV-1`): normalize lifecycle vocabulary (`pending|processing|completed|failed|completed_with_errors`).
- [ ] ⬜ Incomplete (`MV-2`): remove webhook-secret fallback to API secret.
- [ ] ⬜ Incomplete (`MV-3`): implement idempotent bulk-job creation + replay-safe submission.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress (`MV-4`): distributed rate-limit behavior and operator visibility hardening.
- [ ] 🟡 In Progress (`MV-5`): migration discipline with explicit, pre-deploy migration stage.
- [ ] ⬜ Incomplete (`MV-6`): log + trace correlation across API, worker, and downstream consumers.

### P3+ - platform productization

- [ ] 📌 Planned (`MV-7`): webhook ecosystem reliability tooling (replay, DLQ, delivery metrics).
- [ ] 📌 Planned (`MV-8`): campaign preflight orchestration contracts with policy gates.
- [ ] 📌 Planned (`MV-9`): OpenAPI parity and endpoint contract tests for all v1 routes.
