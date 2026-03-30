# Contact AI Codebase Analysis (`backend(dev)/contact.ai`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`backend(dev)/contact.ai` is Contact360's AI inference service for chat and AI utilities. It provides user-scoped chat sessions, streaming replies, email risk analysis, company summaries, and natural-language filter parsing consumed via Appointment360 and dashboard/extension surfaces.

---

## Runtime architecture snapshot

- Runtime: FastAPI + async SQLAlchemy + Mangum Lambda handler.
- API surface: `/api/v1/ai-chats/*` and `/api/v1/ai/*` plus `/health` and `/`.
- AI engine: Hugging Face chat-completions router with retries and fallback model candidates.
- Data: PostgreSQL `ai_chats` persistence with JSON message history.
- Middleware: permissive CORS, compression, monitoring/rate middleware.
- Auth: `X-API-Key` and `X-User-ID` headers for protected endpoints.

---

## Verified completion status from runtime

- [x] ✅ Chat CRUD endpoints with user ownership checks are implemented.
- [x] ✅ Sync and SSE streaming chat response endpoints are implemented.
- [x] ✅ AI utility endpoints exist for email risk, company summary, and filter parsing.
- [x] ✅ Health endpoint uses cached DB status with background refresh path.
- [x] ✅ HF model fallback/retry logic is implemented in service layer.
- [x] ✅ Lambda deployment wiring exists in `template.yaml`.

## Active risks and gap map

### Security and secrets posture

- [ ] ⬜ Incomplete: CORS is wildcard (`allow_origins=["*"]`) and needs hardened environment allowlists.
- [ ] ⬜ Incomplete: single shared API key model remains; scoped service/tenant keys are not implemented.
- [ ] ⬜ Incomplete: committed local configuration still contains sensitive real-looking DB values (`.env`, `samconfig.toml`) and must be sanitized.
- [ ] 🟡 In Progress: route-level auth is present, but full governance and rotation policy evidence is incomplete.

### Contract drift and integration quality

- [ ] 🟡 In Progress: docs contain legacy path references (`/api/v2/gemini/...`) while runtime is `/api/v1/ai/...`.
- [ ] ⬜ Incomplete: strict schema validation for `messages` JSON payload remains limited (free-form JSONB risk).
- [ ] ⬜ Incomplete: model-selection contract parity between gateway enums and HF model IDs needs stronger enforcement.
- [ ] 📌 Planned: publish explicit private/public API boundary and compatibility policy.

### Reliability and observability

- [ ] 🟡 In Progress: cached health and retries exist, but full SLO/error-budget monitoring is incomplete.
- [ ] ⬜ Incomplete: SSE error semantics under Lambda timeout/network interruption are not fully hardened.
- [ ] ⬜ Incomplete: distributed tracing/correlation across gateway -> contact.ai -> model provider is incomplete.
- [ ] 📌 Planned: archival/retention lifecycle for stale chats and audit evidence.

---

## Cross-service dependency map (release gating)

- [x] ✅ `contact360.io/api` -> `backend(dev)/contact.ai` for chat and utility AI operations.
- [x] ✅ `backend(dev)/contact.ai` -> PostgreSQL (`ai_chats` table and ownership data).
- [x] ✅ `backend(dev)/contact.ai` -> Hugging Face router for LLM calls.
- [ ] 🟡 In Progress: fallback/provider governance and model-catalog controls.
- [ ] 📌 Planned: campaign-runtime integration (`backend(dev)/email campaign`) for AI content generation paths.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ Contact AI runtime currently has no direct S3 data-path dependency for core features.
- [ ] 📌 Planned: if chat artifacts/prompts/attachments are introduced, enforce `s3storage` mediation by default.

## Log-unification migration map (`local logs/print/console` -> `logs.api`)

- [x] ✅ Service uses centralized logger utility for most runtime paths.
- [ ] 🟡 In Progress: standardize all error/event emission into canonical logs ingestion path.
- [ ] ⬜ Incomplete: end-to-end trace IDs and log schema compatibility with `logs.api` are incomplete.
- [ ] 📌 Planned: AI operation audit events (model, latency, fallback reason) routed to canonical logging.

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core REST contracts for chats and AI utilities are implemented.
- [ ] 🟡 In Progress: align docs and consumers to `/api/v1/ai/*` and `/api/v1/ai-chats/*` only.
- [ ] ⬜ Incomplete: enforce strict message/contact payload schema and validation guarantees.
- [ ] ⬜ Incomplete: model enum mapping contract checks between gateway and contact.ai.
- [ ] 📌 Planned: versioning/deprecation policy for externalized AI endpoints.

### Service pack

- [x] ✅ Chat orchestration, HF retries/fallback, and streaming behavior are implemented.
- [ ] 🟡 In Progress: harden fallback semantics and user-visible failure reasons.
- [ ] ⬜ Incomplete: scoped authz and usage policy enforcement in service layer.
- [ ] ⬜ Incomplete: formal retention/archival strategy for chat history.
- [ ] 📌 Planned: campaign-specific generation services and reusable AI task packs.

### Surface pack

- [x] ✅ Endpoints support dashboard AI chat, utility AI, and streamed responses.
- [ ] 🟡 In Progress: improve deterministic error responses for frontend/extension surfaces.
- [ ] ⬜ Incomplete: consistency of response contracts across streaming/non-streaming paths.
- [ ] ⬜ Incomplete: explicit endpoint readiness metadata for UI fallback decisions.
- [ ] 📌 Planned: public developer-facing AI utility documentation surface.

### Data pack

- [x] ✅ `ai_chats` persistence and repository patterns are established.
- [ ] 🟡 In Progress: improve data lineage and ownership integrity checks.
- [ ] ⬜ Incomplete: strict JSONB schema and migration-safe constraints.
- [ ] ⬜ Incomplete: audit-grade event data model for AI outputs and moderation/compliance.
- [ ] 📌 Planned: campaign-linked AI generation evidence tables and retention controls.

### Ops pack

- [x] ✅ Lambda deployment templates and health checks are present.
- [ ] 🟡 In Progress: improve runtime metrics and operational alerting granularity.
- [ ] ⬜ Incomplete: distributed tracing and cross-service correlation in production.
- [ ] ⬜ Incomplete: secrets hygiene and environment hardening across local/deploy files.
- [ ] 📌 Planned: release gates for model rollout, rollback, and provider failover.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ Service scaffold, DB integration, and health/runtime basics are implemented.
- [x] ✅ Lambda-compatible FastAPI deployment pattern established.
- [ ] 🟡 In Progress: harden foundational config and secrets discipline.
- [ ] ⬜ Incomplete: remove legacy/deprecated contract references from docs and tests.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ User-scoped chat ownership via `X-User-ID` flow is present.
- [ ] 🟡 In Progress: connect AI usage events to billing/credit enforcement pathways.
- [ ] ⬜ Incomplete: enforce scoped API credentials and tenant boundaries.
- [ ] 📌 Planned: quota-aware AI usage controls and credit accounting interfaces.

### `2.x.x` - Contact360 email system

- [x] ✅ Email risk analysis endpoint is operational.
- [ ] 🟡 In Progress: align output schema and confidence semantics with email system consumers.
- [ ] ⬜ Incomplete: stronger deterministic validation for risk-analysis payloads and errors.
- [ ] 📌 Planned: deeper email workflow integration with campaign prep and verification flows.

### `3.x.x` - Contact360 contact and company data system

- [x] ✅ Filter parsing and company summary endpoints are implemented.
- [ ] 🟡 In Progress: tighten contract with Connectra filter taxonomy and company data surfaces.
- [ ] ⬜ Incomplete: schema-safe contact payload constraints in chat messages.
- [ ] 📌 Planned: richer contact/company enrichment outputs and provenance fields.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] 🟡 In Progress: current APIs can support extension/SN contexts via gateway.
- [ ] ⬜ Incomplete: dedicated extension-optimized AI contracts and response envelopes.
- [ ] 📌 Planned: SN/extension context-aware AI task templates.

### `5.x.x` - Contact360 AI workflows

- [x] ✅ This is the primary completed era: chat, streaming, and utility AI endpoints are live.
- [x] ✅ HF model routing with fallback/retries exists.
- [ ] 🟡 In Progress: model-contract parity and operational explainability hardening.
- [ ] ⬜ Incomplete: advanced workflow chaining and structured agentic operations.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ Cached DB health and retry scaffolding are implemented.
- [ ] 🟡 In Progress: improve latency/error SLO instrumentation and alert readiness.
- [ ] ⬜ Incomplete: robust SSE timeout/reconnect strategy for Lambda edge conditions.
- [ ] 📌 Planned: traceability and failover scorecards with provider-level KPIs.

### `7.x.x` - Contact360 deployment

- [x] ✅ SAM/Lambda deployment path exists.
- [ ] 🟡 In Progress: deployment and secret hardening policy maturity.
- [ ] ⬜ Incomplete: blue/green and canary controls for model/provider changes.
- [ ] 📌 Planned: release gate automation for config contract checks.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ Private API pathing exists and is structured.
- [ ] 🟡 In Progress: formal private/public boundary and docs consistency.
- [ ] ⬜ Incomplete: scoped keys, versioning guarantees, and rate-limit headers for external consumption.
- [ ] 📌 Planned: productized AI API governance and compatibility policy.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] 🟡 In Progress: integration-ready primitives exist but governance is partial.
- [ ] ⬜ Incomplete: webhook/event integration model and connector lifecycle controls.
- [ ] 📌 Planned: ecosystem-grade integration contracts and observability.

### `10.x.x` - Contact360 email campaign

- [ ] 🟡 In Progress: contact.ai already provides building blocks (email risk + generation-friendly chat).
- [ ] ⬜ Incomplete: dedicated campaign generation endpoint and compliance evidence workflow.
- [ ] 📌 Planned: full campaign AI orchestration with audit-friendly output lineage.
- [ ] 📌 Planned: campaign-scale load testing and policy controls.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: sanitize committed secrets and remove real-looking credentials from local/deploy configs.
- [ ] 🟡 In Progress: normalize docs/tests to canonical `/api/v1/ai*` contracts only.
- [ ] ⬜ Incomplete: enforce strict message schema validation and model enum mapping checks.
- [ ] ⬜ Incomplete: harden CORS and scoped auth policy for production.
- [ ] 🟡 In Progress: improve SSE failure handling and trace correlation for runtime debugging.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [ ] ⬜ Incomplete: secrets/config hygiene (`.env`, `samconfig.toml`, templates) and key rotation readiness.
- [ ] ⬜ Incomplete: strict contract parity and schema validation for chat payloads.
- [ ] ⬜ Incomplete: scoped authentication model beyond global API key.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress: observability upgrades (SLOs, traces, consistent error envelopes).
- [ ] 🟡 In Progress: provider fallback transparency and model mapping governance.
- [ ] 📌 Planned: retention/audit model for long-lived AI interactions.

### P3+ - platform productization

- [ ] 📌 Planned: ecosystem integration APIs and connector governance.
- [ ] 📌 Planned: campaign-grade AI generation + compliance evidence integration.
