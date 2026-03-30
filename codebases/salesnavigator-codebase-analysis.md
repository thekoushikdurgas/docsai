# Sales Navigator Codebase Analysis (`backend(dev)/salesnavigator`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`backend(dev)/salesnavigator` is Contact360's Sales Navigator ingestion runtime. It receives Sales Navigator profile payloads (or raw HTML for extraction), normalizes/deduplicates them, and persists contacts/companies through Connectra bulk upsert APIs.

---

## Verified completion status from runtime

- [x] ✅ FastAPI + Mangum Lambda runtime is implemented and deployable via SAM.
- [x] ✅ Core endpoints exist: `POST /v1/scrape`, `POST /v1/save-profiles`, `GET /v1/health`, and root `/`.
- [x] ✅ API-key authentication is enforced (`X-API-Key`).
- [x] ✅ Per-key in-memory rate limiting is implemented in dependencies layer.
- [x] ✅ `X-Request-ID` middleware is implemented and echoed on responses.
- [x] ✅ CORS uses env-driven allowlist (`ALLOWED_ORIGINS`) rather than wildcard defaults.
- [x] ✅ Save service deduplicates profiles and performs chunked parallel persistence via Connectra.
- [x] ✅ Connectra client has retry/backoff and adaptive timeout behavior.

## Active risks and gap map

### Contract and docs drift

- [ ] ⬜ Incomplete: docs still mention non-implemented/legacy surfaces in places; runtime is canonical on `/v1/scrape` and `/v1/save-profiles`.
- [ ] 🟡 In Progress: OpenAPI stub exists, but endpoint/response parity enforcement in CI is incomplete.
- [ ] 📌 Planned: publish strict compatibility policy for extension/gateway consumers.

### Auth and governance

- [ ] ⬜ Incomplete: single shared service API key remains (no scoped tenant/user key model).
- [ ] 🟡 In Progress: per-key rate limit is present, but not distributed or durable across warm instances.
- [ ] 📌 Planned: scoped key governance with usage attribution and rotation controls.

### Reliability and data quality

- [ ] 🟡 In Progress: retries/timeouts/chunked processing are implemented for Connectra saves.
- [ ] ⬜ Incomplete: no explicit idempotency token at request/chunk level for replay-safe bulk ingestion.
- [ ] ⬜ Incomplete: dependency on Connectra availability without local queue fallback.
- [ ] ⬜ Incomplete: enrichment depth gaps (`employees_count`, industries, revenue) remain mostly absent from SN source mapping.
- [ ] 📌 Planned: stronger quality gates and reconciliation evidence between ingested profiles and persisted entities.

---

## Cross-service dependency map (release gating)

- [x] ✅ Inbound from extension and Appointment360/gateway for SN save operations.
- [x] ✅ Outbound to `contact360.io/sync` (Connectra) via `/contacts/bulk` and `/companies/bulk`.
- [x] ✅ Shared contract behavior around deterministic UUID mapping and deduplication.
- [ ] 🟡 In Progress: contract parity checks across `docs/backend/apis` and OpenAPI stub.
- [ ] 📌 Planned: campaign pipeline handoff contract for SN-derived audience provenance.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Runtime currently does not rely on direct S3 writes for primary SN ingestion flow.
- [ ] 📌 Planned: if ingestion artifacts/snapshots are introduced, route through `s3storage` control plane by default.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [ ] 🟡 In Progress: service uses Python logging, but unified event schema/correlation with `logs.api` is not complete.
- [ ] ⬜ Incomplete: no full cross-service trace/event envelope alignment across extension -> gateway -> salesnavigator -> connectra.
- [ ] 📌 Planned: canonical structured ingestion events with request IDs and actor context.

---

## Current execution packs (small tasks)

### Contract pack

- [x] ✅ Canonical v1 endpoints are implemented and active.
- [ ] 🟡 In Progress: synchronize README/OpenAPI/docs with runtime-only endpoints.
- [ ] ⬜ Incomplete: endpoint parity test gate in CI for contract drift prevention.
- [ ] ⬜ Incomplete: formal error taxonomy and status compatibility guarantees.
- [ ] 📌 Planned: versioning/deprecation lifecycle for SN ingestion APIs.

### Service pack

- [x] ✅ Deduplication, chunking, and parallel save orchestration are implemented.
- [x] ✅ Connectra client retry/backoff and adaptive timeout paths are implemented.
- [ ] 🟡 In Progress: quality and resilience optimizations for large-batch save behavior.
- [ ] ⬜ Incomplete: idempotency key model for chunk replay safety.
- [ ] 📌 Planned: deeper enrichment and post-save verification/reconciliation jobs.

### Surface pack

- [x] ✅ Supports extension/gateway ingestion surfaces.
- [ ] 🟡 In Progress: response consistency and richer partial-success semantics for UI.
- [ ] ⬜ Incomplete: explicit UX contract for retry/replay-safe outcomes.
- [ ] 📌 Planned: readiness contract for campaign/audience builder integration.

### Data pack

- [x] ✅ Deterministic UUID generation and mapping to contacts/companies are implemented.
- [x] ✅ Deduplication by normalized profile URL/sales URL is implemented.
- [ ] 🟡 In Progress: mapping coverage for metadata and quality indicators.
- [ ] ⬜ Incomplete: lineage-grade provenance fields and persistent audit traceability.
- [ ] 📌 Planned: enrichment pipeline for company-level fields not present in SN payloads.

### Ops pack

- [x] ✅ Lambda deployment scaffolding and health endpoint exist.
- [x] ✅ Request-ID propagation baseline is implemented.
- [ ] 🟡 In Progress: rate-limit behavior currently in-memory and instance-local.
- [ ] ⬜ Incomplete: distributed throttling, SLO dashboarding, and error-budget gates.
- [ ] 📌 Planned: production-grade governance for keys, telemetry, and rollout checks.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ service scaffold, config validation, health route, and Lambda handler are implemented.
- [x] ✅ Connectra integration client and save pipeline baseline are implemented.
- [ ] 🟡 In Progress: foundational documentation parity and contract guardrails.
- [ ] ⬜ Incomplete: enforce runtime-doc parity checks as hard gates.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ auth gate exists with service API key.
- [ ] 🟡 In Progress: usage-limiting controls partially implemented via per-key minute window.
- [ ] ⬜ Incomplete: tenant/user-scoped authn/authz and credit/billing attribution.
- [ ] 📌 Planned: key-to-actor mapping and cost-accountable event emission.

### `2.x.x` - Contact360 email system

- [x] ✅ SN ingestion can provide contact records to downstream email workflows.
- [ ] 🟡 In Progress: preserve email/linkedin field quality for email finder/verifier chain.
- [ ] ⬜ Incomplete: direct handoff contract guarantees and quality thresholds.
- [ ] 📌 Planned: explicit email-readiness status from SN ingest output.

### `3.x.x` - Contact360 contact and company data system

- [x] ✅ contact/company mapping and bulk upsert integration are implemented.
- [x] ✅ deterministic IDs and dedup controls provide stable upsert behavior.
- [ ] 🟡 In Progress: mapping completeness and provenance quality.
- [ ] ⬜ Incomplete: deep lineage model and reconciliation reporting.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [x] ✅ primary era capabilities are implemented (scrape + save profiles).
- [x] ✅ HTML extraction and profile normalization pipeline exists.
- [ ] 🟡 In Progress: hardening around DOM drift and extension payload variant compatibility.
- [ ] ⬜ Incomplete: full contract cleanup for stale docs and deprecated expectations.

### `5.x.x` - Contact360 AI workflows

- [x] ✅ output fields can seed AI workflows (titles, seniority, company context).
- [ ] 🟡 In Progress: AI-quality enrichment and confidence alignment.
- [ ] ⬜ Incomplete: formal AI-ready schema contract and low-quality filtering policy.
- [ ] 📌 Planned: curated AI feature pack from SN-derived signals.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ retries, adaptive timeouts, chunked parallel saves, and request IDs are implemented.
- [ ] 🟡 In Progress: local per-key rate limit is present but not distributed.
- [ ] ⬜ Incomplete: idempotency tokens, replay controls, and failure-budget instrumentation.
- [ ] 📌 Planned: load-profile SLO gates and resilience drills.

### `7.x.x` - Contact360 deployment

- [x] ✅ SAM deployment template and runtime config surface are present.
- [ ] 🟡 In Progress: deployment hardening and config governance.
- [ ] ⬜ Incomplete: scoped key rollout, immutable audit, and compliance gate automation.
- [ ] 📌 Planned: release/runbook standardization across environments.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ private service endpoints and security scheme are defined.
- [ ] 🟡 In Progress: OpenAPI contract exists as stub but needs strict parity governance.
- [ ] ⬜ Incomplete: public/private lifecycle policy and durable quota/usage management.
- [ ] 📌 Planned: external-ready API governance with compatibility tests.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] 🟡 In Progress: integration primitives exist through normalized payload path.
- [ ] ⬜ Incomplete: connector-grade lineage, eventing, and partner observability.
- [ ] 📌 Planned: multi-source ingestion adapters and platformized integration contracts.

### `10.x.x` - Contact360 email campaign

- [ ] 🟡 In Progress: SN ingestion can feed campaign audience building inputs.
- [ ] ⬜ Incomplete: campaign-specific provenance/compliance handoff guarantees.
- [ ] 📌 Planned: dedicated campaign preflight integration with suppression and audit evidence.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: align all docs/OpenAPI references to actual runtime endpoint behavior.
- [ ] ⬜ Incomplete: add idempotency keys for request/chunk replay safety.
- [ ] 🟡 In Progress: harden rate limiting from in-memory windows to distributed controls.
- [ ] ⬜ Incomplete: implement scoped keys and actor-level usage attribution.
- [ ] 🟡 In Progress: improve provenance/lineage payload for downstream audit and campaign usage.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete (`SN-0`): remove contract drift between runtime and docs/OpenAPI.
- [ ] ⬜ Incomplete (`SN-1`): replay-safe idempotency for bulk profile saves.
- [ ] ⬜ Incomplete (`SN-2`): scoped authentication model beyond single shared API key.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress (`SN-3`): distributed and observable rate-limiting controls.
- [ ] 🟡 In Progress (`SN-4`): quality/provenance enrichment for mapped contact/company fields.
- [ ] ⬜ Incomplete (`SN-5`): trace/event schema alignment with cross-service observability.

### P3+ - platform productization

- [ ] 📌 Planned (`SN-6`): external connector contracts and ecosystem ingestion adapters.
- [ ] 📌 Planned (`SN-7`): campaign-grade provenance and compliance handoff pipeline.
