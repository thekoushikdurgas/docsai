# Email Campaign Codebase Analysis (`backend(dev)/email campaign`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`backend(dev)/email campaign` is Contact360's campaign execution backend for `10.x.x`. It handles campaign enqueueing, async recipient processing, SMTP dispatch, template rendering from S3, unsubscribe token validation, suppression checks, and per-recipient status tracking.

---

## Runtime architecture snapshot

- Runtime: Go (Gin API + Asynq worker + Redis).
- Entry points: `cmd/main.go` (API), `cmd/worker/main.go` (worker).
- Core APIs: `api/handlers.go`, `template/handlers.go`.
- Worker logic: `worker/campaign_worker.go`, `worker/email_worker.go`.
- Data/storage: PostgreSQL schema (`db/schema.sql`) + S3 template store.
- Security hooks: admin API-key middleware (`api/middleware.go`) + unsubscribe JWT flow (`utils/token.go`).

---

## Verified completion status from runtime

- [x] ✅ Campaign queueing and async execution path are implemented (`/campaign` -> Asynq task -> worker send loop).
- [x] ✅ Template CRUD and preview routes are implemented with S3-backed HTML storage.
- [x] ✅ Schema includes `campaigns`, `recipients`, `templates`, and `suppression_list` tables.
- [x] ✅ Recipient-level status updates (`sent`, `failed`, `unsubscribed`) are implemented in worker flow.
- [x] ✅ Unsubscribe token validation and suppression-list insertion flow are implemented.
- [x] ✅ SMTP authentication wiring exists (`smtp.PlainAuth`).

## Active risks and gap map

### Security and access control

- [ ] 🟡 In Progress: `RequireAdminAPIKey` exists, but route-level enforcement completeness for all sensitive endpoints must be verified and standardized.
- [ ] ⬜ Incomplete: no tenant/user-scoped authorization model; current control is static admin key.
- [ ] ⬜ Incomplete: audit-grade auth event logging and key-rotation governance are not fully represented.

### Campaign behavior and delivery guarantees

- [ ] ⬜ Incomplete: campaign terminal state currently marks `completed` after workers finish even when some recipients fail (no `completed_with_errors` state).
- [ ] 🟡 In Progress: suppression checks are active, but advanced deliverability controls (warmup/throttling/bounce taxonomy) are limited.
- [ ] ⬜ Incomplete: recipient source is CSV-filepath centric and not fully integrated with Connectra segment/VQL audience contracts.

### Logging and observability drift

- [ ] ⬜ Incomplete: worker path still uses direct `log.Println`/`fmt.Printf` output in critical send paths.
- [ ] 🟡 In Progress: structured operational data exists in DB status fields, but canonical `logs.api` unification is incomplete.
- [ ] ⬜ Incomplete: open/click/reply analytics events and webhook emission are not complete.

### Queue and architecture drift

- [ ] 🟡 In Progress: Asynq queue is the active path, while `queue/reddis_queue.go` remains as legacy/parallel queue code and risks drift.
- [ ] ⬜ Incomplete: explicit idempotency keys for campaign creation/send replay prevention are not fully enforced.
- [ ] 📌 Planned: campaign orchestration expansion (sequences, A/B, scheduling policy) for full `10.x` scope.

---

## Cross-service dependency map (release gating)

- [x] ✅ `backend(dev)/email campaign` <- gateway/dashboard surfaces (campaign create and status consumption).
- [x] ✅ `backend(dev)/email campaign` -> PostgreSQL for campaign/recipient/template/suppression state.
- [x] ✅ `backend(dev)/email campaign` -> S3 for template HTML storage.
- [x] ✅ `backend(dev)/email campaign` -> Redis/Asynq for async processing.
- [ ] 🟡 In Progress: `backend(dev)/email campaign` -> `lambda/logs.api` canonical logging pipeline.
- [ ] 📌 Planned: deeper linkage to `contact360.io/sync`/segment services for audience sourcing.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Template storage integration with S3 is fully functional.
- [ ] ⬜ Incomplete: service currently uses direct S3 SDK operations instead of a unified `s3storage` control-plane path.
- [ ] 🟡 In Progress: define migration strategy for template/object ops through standard storage service contracts.
- [ ] 📌 Planned: enforce no-new direct storage usage policy for future endpoints.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [x] ✅ Core DB-side status transitions provide baseline operational traceability.
- [ ] ⬜ Incomplete: direct runtime output (`log.Println`, `fmt.Printf`) remains in API/worker paths.
- [ ] 🟡 In Progress: normalize campaign events (`queued/sending/sent/failed/unsubscribed`) into canonical logs schema.
- [ ] 📌 Planned: add campaign webhook + logs sink integration for ecosystem/reporting.

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core campaign/template/unsubscribe endpoint contracts are implemented.
- [ ] 🟡 In Progress: align contract semantics for partial failures and terminal campaign statuses.
- [ ] ⬜ Incomplete: add idempotency key requirements for create/enqueue operations.
- [ ] ⬜ Incomplete: define partner/public-safe campaign API versioning and webhook contracts.
- [ ] 📌 Planned: sequence/A-B contract layer for advanced campaign runtime.

### Service pack

- [x] ✅ Async worker + SMTP send pipeline + template renderer are implemented.
- [ ] 🟡 In Progress: improve failure taxonomy and deterministic retry behavior.
- [ ] ⬜ Incomplete: remove legacy queue drift and converge on one queue architecture.
- [ ] ⬜ Incomplete: harden audience ingestion beyond filesystem CSV path.
- [ ] 📌 Planned: AI-assisted template and sequence service modules.

### Surface pack

- [x] ✅ Operational routes exist for campaign create, stats, mailbox, templates, and unsubscribe.
- [ ] 🟡 In Progress: strengthen route protection and admin-only access boundaries.
- [ ] ⬜ Incomplete: campaign analytics/event surfaces (open/click/reply) are incomplete.
- [ ] ⬜ Incomplete: unified campaign status diagnostics endpoints are limited.
- [ ] 📌 Planned: productized campaign lifecycle APIs for orchestration UI.

### Data pack

- [x] ✅ Schema parity for core tables currently exists in `db/schema.sql`.
- [x] ✅ `recipients.unsub_token` and `templates` table are present.
- [ ] 🟡 In Progress: enhance data lineage for recipient lifecycle and suppression reasons.
- [ ] ⬜ Incomplete: campaign evidence model for compliance and audit exports is incomplete.
- [ ] 📌 Planned: tenant partitioning and policy-aware retention strategy.

### Ops pack

- [x] ✅ Two-process deployment model (API + worker) with queue decoupling is established.
- [ ] 🟡 In Progress: improve deliverability controls (rate warmup/throttle/bounce strategy).
- [ ] ⬜ Incomplete: route-level SLOs and production alerting policy are incomplete.
- [ ] ⬜ Incomplete: release gate matrix for auth/storage/log/idempotency is incomplete.
- [ ] 📌 Planned: deployment runbooks with staged campaign safety checks.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ Service scaffold, schema, queue integration, and health route are implemented.
- [x] ✅ API and worker binaries are separated for asynchronous execution.
- [ ] 🟡 In Progress: normalize foundational governance and release checks.
- [ ] ⬜ Incomplete: fully standardized secure operational defaults.

### `1.x.x` - Contact360 user and billing and credit system

- [ ] 🟡 In Progress: campaign sends can be linked from higher-level billing contexts.
- [ ] ⬜ Incomplete: direct credit pre-check and deduction controls inside campaign runtime are incomplete.
- [ ] ⬜ Incomplete: tenant/user-scoped authz model for paid plan enforcement is incomplete.
- [ ] 📌 Planned: campaign-volume credit policy and billing evidence export.

### `2.x.x` - Contact360 email system

- [x] ✅ SMTP send flow and template rendering are implemented.
- [x] ✅ suppression and unsubscribe plumbing exist.
- [ ] 🟡 In Progress: harden SMTP deliverability behavior and retry strategy.
- [ ] ⬜ Incomplete: richer inbox/sent feedback loop and bounce categorization.

### `3.x.x` - Contact360 contact and company data system

- [ ] 🟡 In Progress: campaign recipient ingestion can consume CSV data.
- [ ] ⬜ Incomplete: full Connectra segment/VQL audience integration is incomplete.
- [ ] ⬜ Incomplete: provenance and sync linkage with contact/company systems is limited.
- [ ] 📌 Planned: audience-source unification and lineage controls.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] ⬜ Incomplete: no direct first-class extension/Sales Navigator audience flow in runtime.
- [ ] 📌 Planned: extension and SN sourced recipient pipelines with provenance.
- [ ] 📌 Planned: sales-triggered campaign automation hooks.

### `5.x.x` - Contact360 AI workflows

- [ ] ⬜ Incomplete: AI-assisted campaign drafting/subject optimization is not complete.
- [ ] 🟡 In Progress: template rendering architecture can host AI-generated content.
- [ ] 📌 Planned: AI workflow APIs for copy, personalization, and send recommendations.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ Async queue architecture establishes base scaling model.
- [ ] 🟡 In Progress: improve resilience for partial failures and queue retry semantics.
- [ ] ⬜ Incomplete: strict idempotency and replay-safe send guarantees not complete.
- [ ] 📌 Planned: SLO/error-budget and deliverability guardrail automation.

### `7.x.x` - Contact360 deployment

- [x] ✅ Separate API/worker deployment topology exists.
- [ ] 🟡 In Progress: deployment runbooks and secret management hardening.
- [ ] ⬜ Incomplete: comprehensive production release gates for campaign safety.
- [ ] 📌 Planned: progressive rollout and rollback-safe campaign controls.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ Private API surface exists for campaign operations.
- [ ] 🟡 In Progress: endpoint hardening and contract version policy.
- [ ] ⬜ Incomplete: public/partner-safe API boundaries and webhook guarantees are incomplete.
- [ ] 📌 Planned: API productization for campaign orchestration.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] 🟡 In Progress: architecture can support ecosystem events via queue + DB state.
- [ ] ⬜ Incomplete: connector lifecycle, quotas, and integration observability are incomplete.
- [ ] 📌 Planned: ecosystem-grade event/webhook framework and partner controls.

### `10.x.x` - Contact360 email campaign

- [x] ✅ Core campaign engine (send + template + unsubscribe + recipient states) is implemented.
- [ ] 🟡 In Progress: close gap for partial-failure lifecycle and advanced analytics.
- [ ] ⬜ Incomplete: full sequence/A-B/testing/compliance intelligence surface is incomplete.
- [ ] 📌 Planned: complete campaign productization with compliance-grade evidence bundle.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove direct `log.Println`/`fmt.Printf` worker logging and unify to canonical structured sink.
- [ ] 🟡 In Progress: enforce admin auth middleware consistently on all sensitive campaign/template operations.
- [ ] ⬜ Incomplete: implement idempotency keys for campaign create/enqueue.
- [ ] ⬜ Incomplete: add `completed_with_errors` status and explicit partial-failure policy.
- [ ] 🟡 In Progress: replace CSV-filepath-only audience source with Connectra segment/VQL source integration.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete: complete auth hardening and route protection policy.
- [ ] ⬜ Incomplete: complete logging unification and remove ad-hoc output paths.
- [ ] ⬜ Incomplete: idempotent send safety for replay/duplicate prevention.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress: partial-failure campaign lifecycle + retry semantics.
- [ ] 🟡 In Progress: audience-source integration with contact/company systems.
- [ ] 📌 Planned: webhook/event analytics and observability contracts.

### P3+ - platform productization

- [ ] 📌 Planned: AI-assisted campaign content and optimization loops.
- [ ] 📌 Planned: full `10.x.x` sequence/A-B/compliance product suite.
