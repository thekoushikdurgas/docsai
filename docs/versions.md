# Contact360 Release History

This file tracks meaningful releases only. It does not enumerate empty placeholder versions.

**Planning alignment:** Near-term cuts (`1.x`–`6.x`) are the default execution horizon. Strategic eras (`7.x`–`10.x`) are defined in `docs/roadmap.md` and `docs/architecture.md` (*Planning horizon*). Foundation (`0.x`) minors use `docs/0. Foundation and pre-product stabilization and codebase setup/0.* — <Title>.md`. Other optional per-minor stubs may live under `docs/versions/version_*.md` when that folder is used. A major moving to `in_progress` here should still have matching roadmap stages and owners.

**Documentation index:** `docs/architecture.md` (system boundaries), `docs/codebase.md` (repo map), `docs/backend.md` (gateway + services), `docs/frontend.md` (dashboard, marketing, DocsAI, extension), `docs/flowchart.md` (diagrams), `docs/version-policy.md` (version policy). **Foundation era (`0.x`):** minors as `docs/0. Foundation and pre-product stabilization and codebase setup/0.N — <Title>.md`, with **Micro-gate** + **Service task slices** in each codenamed patch file `0.N.P — <Codename>.md` in the same folder. **Reliability era (`6.x`):** minors `docs/6. Contact360 Reliability and Scaling/6.N — <Title>.md` with the same **Micro-gate** + **Service task slices** pattern in `6.N.P — <Codename>.md`. **Deployment era (`7.x`):** minors `docs/7. Contact360 deployment/7.N — <Title>.md` with **Micro-gate** + **Service task slices** in `7.N.P — <Codename>.md`. **Public/private API era (`8.x`):** minors `docs/8. Contact360 public and private apis and endpoints/8.N — <Title>.md` with **Micro-gate** + **Service task slices** in `8.N.P — <Codename>.md`. **Ecosystem / productization era (`9.x`):** minors `docs/9. Contact360 Ecosystem integrations and Platform productization/9.N — <Title>.md` with **Micro-gate** + **Service task slices** in `9.N.P — <Codename>.md`. **Email campaign era (`10.x`):** minors `docs/10. Contact360 email campaign/10.N — <Title>.md` with **Micro-gate** + **Service task slices** in `10.N.P — <Codename>.md`. Optional generic stubs may also appear as `docs/versions/version_*.md` when present.

**Path convention:** Product code lives under **`contact360.io/`** (e.g. `app/` = dashboard, `api/` = Appointment360, `admin/` = DocsAI). Per-minor stubs may still mention legacy names such as `contact360/dashboard` — treat them as **`contact360.io/app/`** unless a release note says otherwise.

## Patch document convention

Patch docs are named `X.Y.Z — <Codename>.md` and live alongside the minor docs inside the same era folder.
Eras `6.x`–`10.x` patches embed **Micro-gate** + **Service task slices** (through email campaign/compliance scope for `10.x`).

## Unreleased (next cut)

- **Target:** `1.1.0`
- **Status:** released
- **Released on:** 2026-03-27
- **Summary:** Complete bulk validation hardening and billing flow operationalization.
- **Planned stage mapping:** `1.3` (billing), `2.4` (bulk processing)
- **Owner:** Product + Platform Engineering
- **Docs / infra note (2026-03):** EC2 Go satellite scaffolds (`EC2/s3storage.server`, `EC2/ai.server`, `EC2/log.server`, `EC2/extension.server`, `EC2/job.server` module rename) landed; hub docs updated. Era task folders received a structural CLI pass (`python cli.py fill-tasks` / `dedup-tasks` / `rename-docs` per era). Per-task **evidence** bullets should follow `docs/docs/task-evidence-template.md` before promoting era status to `completed`.

---

## Release index

| Version | Status | Released/Target | Summary |
| --- | --- | --- | --- |
| `0.10.9` | released | completed | **Foundation handoff complete** — all `0.x` patch gates closed |
| `0.1.0` | released | historical | **Monorepo bootstrap** — internal foundation baseline |
| `1.0.0` | released | historical | Contact360 MVP baseline — auth, credits, email core |
| `1.1.0` | released | 2026-03-27 | Bulk + billing maturity |
| `1.2.0` | planned | upcoming | Analytics, notifications, admin controls, security baseline |
| `2.0.0` | planned | TBD | Email system era — finder, verifier, results, bulk |
| `3.0.0` | planned | TBD | Contact and company data system era |
| `4.0.0` | planned | TBD | Extension and Sales Navigator maturity era |
| `5.0.0` | planned | TBD | AI workflows era |
| `6.0.0` | planned | TBD | Reliability and Scaling era |
| `7.0.0` | planned | TBD | Deployment era |
| `8.0.0` | planned | TBD | Public and private APIs era |
| `9.0.0` | planned | TBD | Ecosystem integrations and Platform productization era |
| `10.0.0` | planned | TBD | Email campaign era |

---

## Release entries

### `0.1.0`

- **Status:** released
- **Released on:** historical
- **Codename:** Monorepo bootstrap
- **Summary:** Initial monorepo, service skeletons, and product foundation setup.
- **Scope:** Base app/service directories, early integration scaffolding, CI pipelines, DocsAI bootstrap, and bootstrapping flows.
- **Roadmap mapping:** pre-v1 foundation work
- **Owner:** Platform Engineering
- **Planning detail:** `docs/0. Foundation and pre-product stabilization and codebase setup/0.1 — Monorepo bootstrap.md`

### `0.10.9`

- **Status:** released
- **Released on:** 2026-03-27
- **Codename:** Handoff
- **Summary:** Foundation completion gate closed; Contact360 approved to proceed with `1.x` execution.
- **Scope:** Finalized `0.x` micro-gate/evidence closure across contract, service, surface/frontend, data, and ops tracks.
- **Roadmap mapping:** `0.x` foundation exit gate
- **Owner:** Platform Engineering
- **Planning detail:** `docs/0. Foundation and pre-product stabilization and codebase setup/0.10.9 — Handoff.md`

### Foundation era minors (`0.0`–`0.10` planning companions)

Shipped releases in `versions.md` still follow the “no empty placeholder versions” rule. The table below names each **foundation minor theme** (codename) and links the canonical stub under the era folder. Use the **Micro-gate reference** in each minor doc and the per-patch **Micro-gate** / **Service task slices** in each `0.N.P — <Codename>.md` file for shared release evidence.

| Minor | Codename |
| --- | --- |
| `0.0` | Pre-repo baseline |
| `0.1` | Monorepo bootstrap |
| `0.2` | Schema & migration bedrock |
| `0.3` | Service mesh contracts |
| `0.4` | Identity & RBAC freeze |
| `0.5` | Object storage plane |
| `0.6` | Async job spine |
| `0.7` | Search & dual-write substrate |
| `0.8` | UX shell & docs mirror |
| `0.9` | Extension channel scaffold |
| `0.10` | Ship & ops hardening (**foundation exit gate** before `1.x` pressure) |

Stub files: `docs/0. Foundation and pre-product stabilization and codebase setup/0.N — <Title>.md` for each minor `N` above, plus ten `0.N.P — <Codename>.md` patch files per minor with merged service backlog slices.

### `1.0.0`

- **Status:** released
- **Released on:** active MVP baseline
- **Summary:** Core Contact360 user journey from signup to finder/verifier/results.
- **Scope:** Authentication, credits core behavior, email finder/verifier engines, and results experience.
- **Roadmap mapping:** `1.1`, `1.2`, `2.1`, `2.2`, `2.3`
- **Owner:** Product + Core Engineering
- **Reference:** `docs/roadmap.md#stage-11---user-and-authentication-system`

### `1.1.0`

- **Status:** released
- **Released on:** 2026-03-27
- **Summary:** Bulk processing and billing flow readiness.
- **Scope:** CSV bulk operations hardening and payment/credit-pack processing improvements; dashboard `/settings` currently redirects to `/profile` and remains a tracked gap for dedicated settings UX.
- **Roadmap mapping:** `1.3`, `2.4`
- **Owner:** Product + Payments/Data Pipeline teams
- **Reference:** `docs/roadmap.md#stage-13---billing-and-payments`

### `1.2.0`

- **Status:** planned
- **Target window:** post-`1.1.0`
- **Summary:** Minimal analytics and platform safeguards for production behavior.
- **Scope:** User analytics view, notifications, admin control panel, baseline security.
- **Roadmap mapping:** `1.4`, `1.5`, `1.6`, `1.7`
- **Owner:** Product + Platform Engineering
- **Reference:** `docs/roadmap.md#stage-14---analytics-for-the-user-minimal`

### `2.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Contact360 email system era — dedicated email feature completeness.
- **Scope:** Email finder engine (pattern generation, Go high-throughput path, provider fallback), verification engine (Mailvetter, DNS/SMTP/SPF/DMARC), results surface, bulk CSV processing, and `contact360.io/email` mailbox surface security hardening (tokenized mailbox sessions replacing plaintext credential transport).
- **Roadmap mapping:** `2.1` to `2.4`
- **Owner:** Email Engineering

### `2.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Email finder engine production maturity.
- **Scope:** Multi-pattern email generation, Go worker path, and credit deduction.
- **Roadmap mapping:** `2.1`
- **Owner:** Email Engineering

### `2.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Email verification engine production maturity.
- **Scope:** Mailvetter integration, SMTP/DNS/SPF/DMARC scoring, and confidence normalization.
- **Roadmap mapping:** `2.2`
- **Owner:** Email Engineering + Mailvetter

### `2.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Results engine and audit history.
- **Scope:** Best result surface, confidence display, and activity log quality.
- **Roadmap mapping:** `2.3`
- **Owner:** Email Engineering + Dashboard

### `2.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Bulk processing validation hardening.
- **Scope:** CSV upload, streaming checkpoint, multipart S3, and job processors.
- **Roadmap mapping:** `2.4`
- **Owner:** Data Pipeline + Storage

### `3.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Contact and company data system era — Connectra intelligence expansion.
- **Scope:** VQL filters, enrichment quality, deduplication, and advanced search UX.
- **Roadmap mapping:** `3.1` to `3.4`
- **Owner:** Search/Data Engineering

### `3.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Advanced search filters and VQL.
- **Scope:** VQL parser maturity, advanced contacts/companies filter taxonomy.
- **Roadmap mapping:** `3.1`
- **Owner:** Connectra Engineering

### `3.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Enrichment and deduplication.
- **Scope:** Duplicate profile reduction and enrichment completeness improvements.
- **Roadmap mapping:** `3.2`
- **Owner:** Data Engineering

### `3.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Search quality and performance.
- **Scope:** Index refresh stability, relevance tuning, and latency SLO.
- **Roadmap mapping:** `3.3`
- **Owner:** Connectra Engineering

### `3.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Dashboard search UX expansion.
- **Scope:** Advanced filtering UX and search-to-export conversion flows.
- **Roadmap mapping:** `3.4`
- **Owner:** Dashboard + Search

### `4.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension and Sales Navigator maturity era.
- **Scope:** Extension auth/session hardening, ingestion stability, sync integrity, and telemetry. Sales Navigator Lambda backend paths are complete through 4.2; extension shell delivery (manifest/background/content/popup) remains planned for 4.5-4.7.
- **Roadmap mapping:** `4.1` to `4.4`
- **Owner:** Extension + Integrations Engineering

### `4.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension auth and session hardening.
- **Scope:** Token refresh, session lifecycle, and stable authenticated extension state.
- **Roadmap mapping:** `4.1`
- **Owner:** Extension Engineering

### `4.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Sales Navigator ingestion optimization.
- **Scope:** Ingestion accuracy and throughput against Sales Navigator source data.
- **Roadmap mapping:** `4.2`
- **Owner:** Sales Navigator Engineering

### `4.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Sync integrity and conflict handling.
- **Scope:** Deterministic conflict resolution and idempotent sync.
- **Roadmap mapping:** `4.3`
- **Owner:** Extension + Data Engineering

### `4.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension telemetry and reliability.
- **Scope:** Error shipping to logs.api and ingestion status UX.
- **Roadmap mapping:** `4.4`
- **Owner:** Extension Engineering + Platform

### `5.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** AI workflows era — Contact AI integrated into user journeys.
- **Scope:** `contact.ai` integration, HF streaming, Gemini utilities, confidence controls, and prompt governance.
- **Roadmap mapping:** `5.1` to `5.4`
- **Owner:** AI Platform Team

### `5.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Contact AI integration in dashboard journeys.
- **Scope:** AI-assisted user workflow actions in core surfaces.
- **Roadmap mapping:** `5.1`
- **Owner:** AI Platform + Dashboard

### `5.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Confidence and explainability controls.
- **Scope:** Confidence/explanation metadata exposed and usable in UI.
- **Roadmap mapping:** `5.2`
- **Owner:** AI Platform

### `5.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** AI usage limits and cost controls.
- **Scope:** Quota enforcement and cost guardrails for AI features.
- **Roadmap mapping:** `5.3`
- **Owner:** AI Platform + Finance Ops

### `5.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Prompt versioning and governance.
- **Scope:** Prompt lifecycle management and rollback readiness.
- **Roadmap mapping:** `5.4`
- **Owner:** AI Platform

### `6.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Reliability and Scaling era.
- **Scope:** SLOs, idempotency, queue resilience, observability, performance, storage lifecycle, cost guardrails, and abuse resilience.
- **Roadmap mapping:** `6.x` stage group
- **Owner:** Platform Engineering

### `6.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Reliability baseline and SLO definition.
- **Scope:** Service-level SLOs, error budgets, and reliability reporting.
- **Roadmap mapping:** `6.1`
- **Owner:** Platform Engineering

### `6.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Idempotency and consistency hardening.
- **Scope:** Idempotent write paths and reconciliation controls.
- **Roadmap mapping:** `6.2`
- **Owner:** Platform Engineering

### `6.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Queue and worker resilience.
- **Scope:** DLQ/replay/retry controls for async workflows.
- **Roadmap mapping:** `6.3`
- **Owner:** Platform Engineering

### `6.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Observability and diagnostics maturity.
- **Scope:** Correlated logs, traces, and alerts across critical paths.
- **Roadmap mapping:** `6.4`
- **Owner:** Platform + Ops

### `6.5.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Performance optimization wave.
- **Scope:** API/search/bulk latency and throughput tuning.
- **Roadmap mapping:** `6.5`
- **Owner:** Platform + Search

### `6.6.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Storage and artifact lifecycle hardening.
- **Scope:** S3 integrity, retention, and cleanup lifecycle enforcement.
- **Roadmap mapping:** `6.6`
- **Owner:** Storage/Data Pipeline

### `6.7.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Cost reliability and budget guardrails.
- **Scope:** Cost controls and usage-based throttling.
- **Roadmap mapping:** `6.7`
- **Owner:** Platform + Finance Ops

### `6.8.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Security and abuse resilience at scale.
- **Scope:** Advanced rate limits and abuse detection.
- **Roadmap mapping:** `6.8`
- **Owner:** Platform + Security

### `6.9.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** RC hardening for deployment era release.
- **Scope:** Reliability release-candidate validation.
- **Roadmap mapping:** `6.9`
- **Owner:** Platform Engineering

### `7.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Deployment era — secure, auditable, and governable deployment.
- **Scope:** RBAC, service-level authz, admin governance, audit/compliance event model, data lifecycle, tenant isolation, security posture hardening, and enterprise observability.
- **Roadmap mapping:** `7.x` stage group
- **Owner:** Platform + Security

### `7.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** RBAC model and access control foundation.
- **Scope:** Role hierarchy and permission matrix rollout.
- **Roadmap mapping:** `7.1`
- **Owner:** Platform + Security

### `7.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Service-level authorization enforcement.
- **Scope:** Internal service authz controls standardization.
- **Roadmap mapping:** `7.2`
- **Owner:** Platform + Security

### `7.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Admin governance controls.
- **Scope:** Approval flows and audited admin actions.
- **Roadmap mapping:** `7.3`
- **Owner:** DocsAI + Platform

### `7.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Audit and compliance event model.
- **Scope:** Immutable audit event schema and reporting.
- **Roadmap mapping:** `7.4`
- **Owner:** Security + Logs Platform

### `7.5.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Data governance and lifecycle controls.
- **Scope:** Data classification, retention, and deletion enforcement.
- **Roadmap mapping:** `7.5`
- **Owner:** Platform + Data Governance

### `7.6.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Tenant and policy isolation.
- **Scope:** Cross-tenant isolation and policy boundaries validation.
- **Roadmap mapping:** `7.6`
- **Owner:** Platform + Security

### `7.7.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Security posture and secrets hardening.
- **Scope:** Secret rotation and privileged control hardening.
- **Roadmap mapping:** `7.7`
- **Owner:** Security Engineering

### `7.8.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Deployment observability and enterprise reporting.
- **Scope:** Tenant-aware operational and governance reports.
- **Roadmap mapping:** `7.8`
- **Owner:** Platform + Data

### `7.9.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** RC hardening for APIs era release.
- **Scope:** Deployment era release-candidate validation.
- **Roadmap mapping:** `7.9`
- **Owner:** Platform + Security

### `8.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Public and private APIs era — stable, versioned, observable API contracts.
- **Scope:** Analytics instrumentation, private service contracts, public GraphQL/REST APIs, API versioning, webhook delivery, partner auth, and API documentation.
- **Roadmap mapping:** `8.x` stage group
- **Owner:** Integrations + Platform Engineering

### `8.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Analytics taxonomy and event instrumentation.
- **Scope:** Canonical event/metric dictionary and end-to-end instrumentation rollout.
- **Roadmap mapping:** `8.1`
- **Owner:** Data Platform + Product Engineering

### `8.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Analytics ingestion hardening and data quality.
- **Scope:** Dedupe, schema control, DLQ for analytics pipeline, freshness and lineage checks.
- **Roadmap mapping:** `8.2`
- **Owner:** Data Platform

### `8.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Private API contracts and service-to-service surface.
- **Scope:** Internal service API baseline, versioning policy, and contract documentation.
- **Roadmap mapping:** `8.3`
- **Owner:** Platform Engineering

### `8.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Public API minimum surface.
- **Scope:** Stable external read/write GraphQL/REST APIs with error contracts.
- **Roadmap mapping:** `8.4`
- **Owner:** Integrations Engineering

### `8.5.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** API versioning and compatibility policy.
- **Scope:** Deprecation policy, breaking-change gates, and compatibility test suite.
- **Roadmap mapping:** `8.5`
- **Owner:** Integrations + Platform

### `8.6.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Webhook and event delivery platform v1.
- **Scope:** Signed events with retry, DLQ, and delivery tracking.
- **Roadmap mapping:** `8.6`
- **Owner:** Integrations + Platform

### `8.7.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Partner identity and tenant-safe access.
- **Scope:** Scoped partner auth and tenant-safe credential controls.
- **Roadmap mapping:** `8.7`
- **Owner:** Integrations + Security

### `8.8.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Analytics and reporting APIs.
- **Scope:** User-facing analytics views, admin analytics center, scheduled reporting.
- **Roadmap mapping:** `8.8`
- **Owner:** Data + Dashboard

### `8.9.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** RC hardening for ecosystem era release.
- **Scope:** API compatibility and reliability release-candidate validation.
- **Roadmap mapping:** `8.9`
- **Owner:** Integrations + Platform

### `9.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Ecosystem integrations and Platform productization era.
- **Scope:** Connector framework, integration contract governance, commercial controls, multi-tenant model, self-serve admin, plan entitlements, SLA/SLO operations, support tooling, cost/capacity governance.
- **Roadmap mapping:** `9.x` stage group
- **Owner:** Product + Platform + Integrations

### `9.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Integration contract governance.
- **Scope:** Versioned external contract policy and compatibility test gates.
- **Roadmap mapping:** `9.1`
- **Owner:** Integrations Engineering

### `9.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Connector framework baseline.
- **Scope:** Shared connector lifecycle, SDK baseline, and validation harness.
- **Roadmap mapping:** `9.2`
- **Owner:** Integrations Engineering

### `9.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Integration observability and commercial controls.
- **Scope:** Integration health views, support actions, and plan quota enforcement.
- **Roadmap mapping:** `9.3`
- **Owner:** Integrations + Product

### `9.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Tenant platform model standardization.
- **Scope:** Canonical tenant identity propagation and context boundaries.
- **Roadmap mapping:** `9.4`
- **Owner:** Platform Engineering

### `9.5.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Self-serve workspace administration.
- **Scope:** Tenant-admin controls and workspace management.
- **Roadmap mapping:** `9.5`
- **Owner:** Product + DocsAI

### `9.6.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Plan entitlements and packaging engine.
- **Scope:** Runtime plan enforcement and feature gating across channels.
- **Roadmap mapping:** `9.6`
- **Owner:** Product + Platform

### `9.7.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** SLA/SLO operations foundation.
- **Scope:** SLA monitoring, operational reporting, and incident alert mapping.
- **Roadmap mapping:** `9.7`
- **Owner:** Platform + Ops

### `9.8.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Cost governance and capacity forecasting.
- **Scope:** Cost attribution and capacity planning controls.
- **Roadmap mapping:** `9.8`
- **Owner:** Platform + Finance Ops

### `9.9.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** RC hardening for email campaign era release.
- **Scope:** Ecosystem and productization release-candidate validation.
- **Roadmap mapping:** `9.9`
- **Owner:** Product + Platform

### `10.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Email campaign era — compliant, observable, and commercially governed campaign delivery.
- **Scope:** Campaign entity model, audience segmentation, policy gates, suppression lists, template system, execution engine, deliverability/safety, observability, feature flags, send metering, PII retention, opt-out auditing, and contract freeze.
- **Roadmap mapping:** `10.x` stage group
- **Owner:** Campaign + Platform + Compliance

### `10.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Campaign foundation — entity model, policy gates, suppression, templates.
- **Scope:** Campaign and audience entities, consent/region/content/rate-limit policy, suppression lists, template system.
- **Roadmap mapping:** `10.1`
- **Owner:** Campaign Engineering

### `10.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Campaign execution engine.
- **Scope:** Campaign state machine, idempotent send, retry semantics, pause/resume.
- **Roadmap mapping:** `10.2`
- **Owner:** Campaign Engineering + Platform

### `10.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Campaign deliverability and safety.
- **Scope:** Pre-send verification (Mailvetter), bounce handling, domain warmup, safety checks.
- **Roadmap mapping:** `10.3`
- **Owner:** Campaign + Deliverability Engineering

### `10.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Campaign observability, support bundles, and release automation.
- **Scope:** Campaign metrics, structured logging, feature flags, canary rollouts.
- **Roadmap mapping:** `10.4`
- **Owner:** Campaign + Platform Ops

### `10.5.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Campaign commercial controls and compliance.
- **Scope:** Send metering, PII retention, opt-out auditing, and contract freeze.
- **Roadmap mapping:** `10.5`
- **Owner:** Campaign + Compliance + Product

### `10.9.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Final contract freeze and campaign release governance.
- **Scope:** Campaign era governance baseline and long-term release process sign-off.
- **Roadmap mapping:** `10.9`
- **Owner:** Product + Engineering leadership

---

## Deep task packs by era (planning companion)

Use this section to break each planned minor into actionable execution slices.

### `1.x` task-pack pattern (user, billing, credit)

- Contract: user/credit/billing GraphQL schema changes.
- Service: auth/session, credit deduction, billing mutation, and analytics query updates.
- Surface: dashboard auth flows, credit display, billing UX, and notification wiring.
- Data/Ops: credit ledger consistency checks, billing state observability, and fraud/abuse controls.

### `2.x` task-pack pattern (email system)

- Contract: finder/verifier API and GraphQL schema changes.
- Service: pattern generation, Go worker path, Mailvetter integration, bulk job processor updates.
- Surface: email UI components, bulk export UX, and results display updates.
- Data/Ops: credit deduction accuracy, bulk job checkpoint reliability, and provider fallback telemetry.

### `3.x` task-pack pattern (contact/company data)

- Contract: VQL filter taxonomy and search schema changes.
- Service: Connectra VQL, dual-write logic, enrichment pipeline, and dedupe algorithm updates.
- Surface: advanced filter UX, company drill-down, and saved-search feature updates.
- Data/Ops: index refresh reliability, search relevance checks, and deduplication quality metrics.

### `4.x` task-pack pattern (extension and Sales Navigator)

- Contract: extension auth token contract and sync payload schema changes.
- Service: extension session logic, SN ingestion parser, conflict resolution, and telemetry updates.
- Surface: extension UI auth flows, ingestion status indicators, and sync health display.
- Data/Ops: sync idempotency checks, telemetry coverage, and SN source variability handling.

### `5.x` task-pack pattern (AI workflows)

- Contract: AI chat/utility GraphQL schema and confidence/explanation field changes.
- Service: HF streaming client, Gemini utility paths, cost quota enforcement, and prompt version updates.
- Surface: AI response rendering, confidence display, and usage cap messaging.
- Data/Ops: AI cost per user metrics, prompt regression checks, and quota breach telemetry.

### `6.x` task-pack pattern (reliability and scaling)

- Contract: SLO definitions and idempotency key contract updates.
- Service: retry/DLQ configuration, idempotency middleware, trace ID propagation, and abuse guard updates.
- Surface: health/SLO endpoint exposure and operational dashboard updates.
- Data/Ops: SLO attainment dashboards, cost guardrail activation, and reliability RC gate.

**Execution:** minors `6.0`–`6.10` with codenamed patches `6.N.P — *.md` — each patch carries **Micro-gate** + **Service task slices** (former standalone `*-reliability-scaling-task-pack.md` files merged into patches).

### `7.x` task-pack pattern (deployment)

- Contract: RBAC role matrix, audit event schema, and data lifecycle policy updates.
- Service: permission check middleware, audit event emission, tenant isolation boundary, and secret rotation updates.
- Surface: admin governance UX, role management screens, and compliance reporting views.
- Data/Ops: audit log integrity checks, tenant boundary test coverage, and security control verification.

**Execution:** minors `7.0`–`7.10` with codenamed patches `7.N.P — *.md` — each patch carries **Micro-gate** + **Service task slices** (former standalone `*-deployment-task-pack.md` files merged into patches).

### `8.x` task-pack pattern (public and private APIs)

- Contract: API versioning policy, webhook event envelope, and analytics schema updates.
- Service: public/private API handler, webhook delivery/retry, partner auth scope, and analytics ingestion updates.
- Surface: API documentation, developer portal, and analytics dashboard updates.
- Data/Ops: delivery observability, API compatibility regression tests, and analytics quality checks.

**Execution:** minors `8.0`–`8.10` with codenamed patches `8.N.P — *.md` — each patch carries **Micro-gate** + **Service task slices** (former standalone `*-api-endpoint-task-pack.md` / `*-public-private-apis-task-pack.md` files merged into patches).

### `9.x` task-pack pattern (ecosystem integrations and productization)

- Contract: connector lifecycle, tenant/policy/entitlement model updates.
- Service: connector SDK, multi-tenant enforcement, entitlement engine, and lifecycle automation updates.
- Surface: integration setup UX, self-serve admin workspace, and support tooling updates.
- Data/Ops: SLA reporting, compliance overlays, cost/capacity controls, and integration health dashboards.

**Execution:** minors `9.0`–`9.10` with codenamed patches `9.N.P — *.md` — each patch carries **Micro-gate** + **Service task slices** (former standalone `*-ecosystem-productization-task-pack.md` files merged into patches).

### `10.x` task-pack pattern (email campaign)

- Contract: campaign entity schema, policy gate rules, and compliance contract updates.
- Service: campaign execution state machine, send metering, deliverability checks, and PII lifecycle updates.
- Surface: campaign creation UI, audience builder, deliverability dashboard, and opt-out management.
- Data/Ops: send metering accuracy, bounce rate tracking, opt-out audit completeness, and feature flag gates.

**Execution:** minors `10.0`–`10.10` with codenamed patches `10.N.P — *.md` — each patch carries **Micro-gate** + **Service task slices** (former standalone `*-email-campaign-task-pack.md` files merged into patches).

---

## Deep planning rule

Before a planned minor (`X.Y.0`) moves to `in_progress`, ensure:

- A matching roadmap stage exists and is current.
- Stage acceptance criteria and task breakdown are reflected in `docs/roadmap.md` for the target era (and optional `docs/versions/version_*.md` when used).
- Owner and KPI fields are explicit in both roadmap and versions docs.


## 10.x campaign release mapping
- 10.1.0 to 10.5.0 campaign milestones (planned)

## Per-minor file governance

All entries in this file must have a corresponding per-minor document under `docs/versions/version_*.md`.
Each per-minor document must include backend endpoint scope, database lineage scope, frontend UX scope, UI elements checklist, flow delta, and release evidence sections.

## `s3storage` execution spine (all eras)

Use this checklist whenever a planned/released minor includes storage work:

- `0.x`: baseline API contract and logical key taxonomy.
- `1.x`: user artifact policy (avatar/photo/proof/resume) and validation.
- `2.x`: durable multipart protocol and metadata freshness.
- `3.x`: ingestion/export lineage and analysis endpoint quality.
- `4.x`: extension-origin provenance and access policy.
- `5.x`: AI artifact lifecycle controls.
- `6.x`: idempotency, reconciliation, and storage SLOs.
- `7.x`: authz, retention/deletion policy enforcement, compliance evidence.
- `8.x`: versioned storage contracts and event/webhook readiness.
- `9.x`: entitlement/quota model and tenant cost controls.
- `10.x`: campaign artifact compliance and reproducibility guarantees.

Deep task decomposition reference: `docs/codebases/s3storage-codebase-analysis.md`.

Per-minor normalization policy:

- Every `docs/versions/version_*.md` must keep the three storage evidence sections explicitly populated (no placeholders):
  - `Backend API and Endpoint Scope`
  - `Database and Data Lineage Scope`
  - `Frontend UX Surface Scope`
- Wording in those sections must remain era-aware (`0.x` through `10.x`) and reference canonical storage docs/endpoints.
- If one minor in an era is updated for storage contract behavior, run the same normalization pass for sibling minors in that era.

## `s3storage` era pack index

- `0.x` -> `docs/0. Foundation and pre-product stabilization and codebase setup/0.5 — Object storage plane.md` (patches `0.5.0`–`0.5.9`; **Service task slices** per patch)
- `1.x` -> `docs/1. Contact360 user and billing and credit system/` — minors `1.0`–`1.10`, patches `1.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-user-billing-task-pack.md` scope merged into patches)
- `2.x` -> `docs/2. Contact360 email system/` — minors `2.0`–`2.10`, patches `2.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-email-system-task-pack.md` scope merged into patches)
- `3.x` -> `docs/3. Contact360 contact and company data system/` — minors `3.0`–`3.10`, patches `3.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-contact-company-task-pack.md` scope merged into patches)
- `4.x` -> `docs/4. Contact360 Extension and Sales Navigator maturity/` — minors `4.0`–`4.10`, patches `4.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-extension-sn-task-pack.md` scope merged into patches)
- `5.x` -> `docs/5. Contact360 AI workflows/` — minors `5.0`–`5.10`, patches `5.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-ai-task-pack.md` scope merged into patches)
- `6.x` -> `docs/6. Contact360 Reliability and Scaling/` — minors `6.0`–`6.10`, patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-reliability-scaling-task-pack.md` merged into patches)
- `7.x` -> `docs/7. Contact360 deployment/` — minors `7.0`–`7.10`, patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-deployment-task-pack.md` merged into patches)
- `8.x` -> `docs/8. Contact360 public and private apis and endpoints/` — minors `8.0`–`8.10`, patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-api-endpoint-task-pack.md` merged into patches)
- `9.x` -> `docs/9. Contact360 Ecosystem integrations and Platform productization/` — minors `9.0`–`9.10`, patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-ecosystem-productization-task-pack.md` merged into patches)
- `10.x` -> `docs/10. Contact360 email campaign/` — minors `10.0`–`10.10`, patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-email-campaign-task-pack.md` merged into patches)

## `logs.api` execution spine (all eras)

Status legend: `✅ Completed` · `🟡 In Progress` · `📌 Planned` · `⬜ Incomplete`

- 📌 Planned: `0.x`: health + baseline write/read contract
- 📌 Planned: `1.x`: auth/billing/credit event schema and lineage
- 📌 Planned: `2.x`: email workflow telemetry scale and batch behavior
- 📌 Planned: `3.x`: contact/company support diagnostics and query semantics
- 📌 Planned: `4.x`: extension telemetry provenance and replay evidence
- 📌 Planned: `5.x`: AI telemetry policy and cost/error monitoring
- 📌 Planned: `6.x`: SLO/error-budget evidence and query reliability
- 📌 Planned: `7.x`: deployment/audit retention compliance evidence
- 📌 Planned: `8.x`: public/private API observability and compatibility coverage
- 📌 Planned: `9.x`: tenant integration governance and SLA evidence
- 📌 Planned: `10.x`: campaign compliance and immutable audit trail evidence


## `logs.api` era pack index

- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-email-campaign-task-pack.md` merged)
- Other eras: see `logsapi-*-task-pack.md` in the corresponding `docs/0...10` era folders where published.

## `connectra` execution spine (all eras)

| Era | Connectra concern | Primary dependency |
|-----|-------------------|-------------------|
| 0.x | Service bootstrap, ES index baseline, API key contract | Dashboard and gateway bootstrap |
| 1.x | Credit-aware volume guards, billing event linkage | Billing and credit system |
| 2.x | Bulk CSV import/export pipeline, streaming contract | Email finder/verifier bulk flows |
| 3.x | VQL freeze, filter taxonomy, dual-write PG+ES, enrichment/dedup | Contact/company search core |
| 4.x | SN ingestion batch-upsert contract, provenance, sync idempotency | Extension and SN ingest |
| 5.x | AI-readable field exposure, artifact query paths | AI workflow enrichment |
| 6.x | SLO/error-budget for search+export, job DLQ/retry, idempotency | Reliability and scaling |
| 7.x | RBAC on write paths, audit events per batch-upsert, tenant isolation | Deployment governance |
| 8.x | REST API versioning, job lifecycle webhooks, partner API keys | Public/private APIs |
| 9.x | Per-tenant quota/throttle, entitlement-aware filters, connector SDK | Ecosystem productization |
| 10.x | Audience segmentation query, suppression filter, campaign export compliance | Email campaign |

Deep task decomposition reference: `docs/codebases/connectra-codebase-analysis.md`.

## `connectra` era pack index

- `0.x` -> `docs/0. Foundation and pre-product stabilization and codebase setup/0.7 — Search & dual-write substrate.md` (patches `0.7.0`–`0.7.9`)
- `1.x` -> `docs/1. Contact360 user and billing and credit system/` — minors `1.0`–`1.10`, patches `1.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-user-billing-task-pack.md` scope merged into patches)
- `2.x` -> `docs/2. Contact360 email system/` — minors `2.0`–`2.10`, patches `2.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-email-system-task-pack.md` scope merged into patches)
- `3.x` -> `docs/3. Contact360 contact and company data system/` — minors `3.0`–`3.10`, patches `3.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-contact-company-task-pack.md` scope merged into patches)
- `4.x` -> `docs/4. Contact360 Extension and Sales Navigator maturity/` — minors `4.0`–`4.10`, patches `4.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-extension-sn-task-pack.md` scope merged into patches)
- `5.x` -> `docs/5. Contact360 AI workflows/` — minors `5.0`–`5.10`, patches `5.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-ai-task-pack.md` scope merged into patches)
- `6.x` -> `docs/6. Contact360 Reliability and Scaling/` — minors `6.0`–`6.10`, patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-reliability-scaling-task-pack.md` merged into patches)
- `7.x` -> `docs/7. Contact360 deployment/` — minors `7.0`–`7.10`, patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-deployment-task-pack.md` merged into patches)
- `8.x` -> `docs/8. Contact360 public and private apis and endpoints/` — minors `8.0`–`8.10`, patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-api-endpoint-task-pack.md` merged into patches)
- `9.x` -> `docs/9. Contact360 Ecosystem integrations and Platform productization/` — minors `9.0`–`9.10`, patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-ecosystem-productization-task-pack.md` merged into patches)
- `10.x` -> `docs/10. Contact360 email campaign/` — minors `10.0`–`10.10`, patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `connectra-email-campaign-task-pack.md` merged into patches)
## `emailapis` execution spine (`0.x`-`10.x`)

- `0.x`: runtime baseline and endpoint contract freeze
- `1.x`: credit-aware finder/verifier contract alignment
- `2.x`: email core maturity (bulk correctness + provider harmonization)
- `3.x`: contact/company enrichment integration hardening
- `4.x`: extension/SN provenance and sync stability
- `5.x`: AI-assisted workflow compatibility
- `6.x`: reliability, scaling, and failure-path hardening
- `7.x`: deployment and governance controls
- `8.x`: public/private API contract readiness
- `9.x`: ecosystem integrations and tenant controls
- `10.x`: campaign deliverability and compliance evidence

## `emailapis` era task pack index

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.3 — Service mesh contracts.md` (patches `0.3.0`–`0.3.9` — emailapis / logsapi / s3storage clients + Lambdas)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `emailapis-user-billing-credit-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `emailapis-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `emailapis-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `emailapis-extension-salesnav-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `emailapis-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `emailapis-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `emailapis-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailapis-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailapis-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailapis-email-campaign-task-pack.md` merged)

## `jobs` execution spine (all eras)

- 📌 Planned: `0.x`: scheduler contract and worker baseline.
- 📌 Planned: `1.x`: billing/credit-aware creation and retry audit.
- 📌 Planned: `2.x`: email stream processors and bulk reliability.
- 📌 Planned: `3.x`: contact/company import-export and VQL validation.
- 📌 Planned: `4.x`: extension/SN provenance job flows.
- 📌 Planned: `5.x`: AI batch metadata and quota controls.
- 📌 Planned: `6.x`: idempotency, retry/DLQ, stale recovery hardening.
- 📌 Planned: `7.x`: role-aware access, retention, and audit controls.
- 📌 Planned: `8.x`: versioned API and callback/webhook lifecycle.
- 📌 Planned: `9.x`: tenant quota/isolation/entitlement scheduling.
- 📌 Planned: `10.x`: campaign send/track/verify compliance bundles.

## `jobs` era pack index

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.6 — Async job spine.md` (patches `0.6.0`–`0.6.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `jobs-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `jobs-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `jobs-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `jobs-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `jobs-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `jobs-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `jobs-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-email-campaign-task-pack.md` merged)

## `contact.ai` execution spine (all eras)

- 📌 Planned: `0.x`: FastAPI Lambda skeleton + `ai_chats` DDL baseline; health endpoints; CI probe.
- 📌 Planned: `1.x`: `user_id` FK integrity; cascade strategy for user deletion; IAM hardening.
- 📌 Planned: `2.x`: `analyzeEmailRisk` contract lock; HF JSON task; PII review.
- 📌 Planned: `3.x`: `parseContactFilters` + `generateCompanySummary` aligned with Connectra VQL taxonomy.
- 📌 Planned: `4.x`: SN contact JSONB compatibility; extension CSP review.
- 📌 Planned: `5.x`: ALL features live — chat CRUD, sync + SSE message send, all utility endpoints, `ModelSelection` shim.
- 📌 Planned: `6.x`: SLO targets, SSE reliability, TTL, optimistic lock, distributed tracing.
- 📌 Planned: `7.x`: RBAC, per-tenant API keys, GDPR erasure cascade, audit log.
- 📌 Planned: `8.x`: Rate limit headers, scoped API keys, usage tracking, API quota UI.
- 📌 Planned: `9.x`: Webhook AI delivery, ecosystem connector adapter.
- 📌 Planned: `10.x`: Campaign AI generation endpoint, `campaign_ai_log` compliance table.

## `contact.ai` era pack index

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.2 — Schema & migration bedrock.md` + `0.3 — Service mesh contracts.md` + `0.10 — Ship & ops hardening.md` (schema / contract / ops bands — see patch **Service task slices**)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `contact-ai-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `contact-ai-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `contact-ai-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `contact-ai-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `contact-ai-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `contact-ai-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `contact-ai-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-email-campaign-task-pack.md` merged)

## `email campaign` execution spine (all eras)

`backend(dev)/email campaign` — Go 1.24, Gin, Asynq/Redis, PostgreSQL, AWS S3. Campaign delivery engine owning bulk email send, template S3 storage, suppression/unsubscribe, and IMAP.

- 📌 Planned: `0.x`: Schema baseline (fix templates table + recipients.unsub_token drift); SMTP auth; auth middleware; Docker; health check.
- 📌 Planned: `1.x`: JWT validation; credit pre-check guard on /campaign; user_id/org_id attribution in campaigns table.
- 📌 Planned: `2.x`: SMTP provider hardening; bounce/complaint webhook receivers; rate-limiter per worker; DLQ policy.
- 📌 Planned: `3.x`: Connectra audience resolver; segment/VQL audience source; replace CSV filepath model; contact_ref_id lineage.
- 📌 Planned: `4.x`: SN batch audience integration; enrichment-gated recipient resolution pipeline.
- 📌 Planned: `5.x`: AI template generation endpoint (`POST /templates/generate`); personalization field extension (Company, Title, Industry).
- 📌 Planned: `6.x`: SLO definition; resume-from-checkpoint; idempotency key per campaign; circuit-breaker for SMTP; Prometheus metrics.
- 📌 Planned: `7.x`: RBAC role checks; audit log emissions to logs.api; secrets in vault; readiness probe; deployment pipeline.
- 📌 Planned: `8.x`: GraphQL module (createCampaign/getCampaign/listCampaigns); public REST v1; webhook dispatcher (campaign.created, campaign.completed, recipient.unsubscribed).
- 📌 Planned: `9.x`: Entitlement enforcement (send volume limits); suppression import endpoint; sender domain management; CRM integration suppression sync.
- 📌 Planned: `10.x`: Sequence engine; A/B test split; open/click tracking pixel; campaign analytics aggregation; campaign scheduler; CAN-SPAM/GDPR compliance.

## `email campaign` era pack index

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.2 — Schema & migration bedrock.md` (patches `0.2.0`–`0.2.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `emailcampaign-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `emailcampaign-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `emailcampaign-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `emailcampaign-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `emailcampaign-ai-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `emailcampaign-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `emailcampaign-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailcampaign-api-endpoint-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailcampaign-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailcampaign-email-campaign-task-pack.md` merged)

## `salesnavigator` era pack index

**Service:** `backend(dev)/salesnavigator` — FastAPI Lambda, no local DB, Connectra integration, deterministic UUID5, HTML extraction, deduplication.

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.9 — Extension channel scaffold.md` (patches `0.9.0`–`0.9.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `salesnavigator-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `salesnavigator-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `salesnavigator-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `salesnavigator-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `salesnavigator-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `salesnavigator-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `salesnavigator-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-email-campaign-task-pack.md` merged)

**Era execution spine summary:**

| Era | Primary SN concern |
| --- | --- |
| `0.x` | Scaffold, UUID contract, health endpoint |
| `1.x` | Actor context, billing stub |
| `2.x` | Email field validation, enrichment handoff |
| `3.x` | Full field mapping + provenance tags |
| `4.x` | **PRIMARY** — extension UX, HTML extraction, docs drift fix |
| `5.x` | AI-ready field quality gates |
| `6.x` | Rate limiting, idempotency, CORS hardening |
| `7.x` | RBAC, per-tenant keys, GDPR, audit events |
| `8.x` | Rate-limit headers, usage tracking, versioned path |
| `9.x` | Connector adapter, webhook delivery |
| `10.x` | Campaign audience provenance, suppression guard |

---

## Appointment360 (`contact360.io/api`) execution spine

**Service:** `contact360.io/api` — Appointment360 GraphQL gateway (FastAPI + Strawberry GraphQL + asyncpg + PostgreSQL)
**Role:** Sole API entry point for all dashboard and extension requests. 28 GraphQL modules, single `/graphql` endpoint. Orchestrates Connectra, tkdjob, Lambda Email, Lambda AI, Resume AI, S3 Storage, Logs API, DocsAI.

**Era task pack index:**

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.1 — Monorepo bootstrap.md` (gateway bootstrap; further Appointment360 slices also appear under other minors’ patches — grep **Appointment360 (gateway)** in `0.*.* — *.md`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `appointment360-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `appointment360-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `appointment360-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `appointment360-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `appointment360-ai-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `appointment360-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `appointment360-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-api-endpoint-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-email-campaign-task-pack.md` merged)

**Era execution spine summary:**

| Era | Primary Appointment360 concern |
| --- | --- |
| `0.x` | FastAPI app bootstrap, 8-layer middleware stack, DB session lifecycle, JWT auth, health endpoints |
| `1.x` | Auth mutations (login/register/refresh/logout), billing/usage module, credit deduction, idempotency on billing |
| `2.x` | Email module (finder/verifier), jobs module (create/list/status), remove inline debug file writes |
| `3.x` | Contacts/companies modules, ConnectraClient, VQL converter, DataLoaders, saved searches |
| `4.x` | LinkedIn/SalesNavigator modules, extension session auth, SN credit deduction |
| `5.x` | AI chats module, resume module, LambdaAIClient, ResumeAIClient, AI credit deduction |
| `6.x` | Enable rate limit + abuse guard + idempotency for production, PostgreSQL idempotency store, complexity/timeout extensions, SLO |
| `7.x` | Deployment hardening (EC2/Lambda/Docker), CI/CD pipeline, SuperAdmin RBAC, Alembic migration hygiene |
| `8.x` | **PRIMARY** — Pages/DocsAI module, profile/API keys, 2FA, X-API-Key public auth, saved searches |
| `9.x` | Notifications module, analytics/events, admin panel, tenant model, webhooks |
| `10.x` | Campaigns/sequences/templates GraphQL modules, CampaignServiceClient proxy, credit deduction per recipient |

**Codebase analysis:** `docs/codebases/appointment360-codebase-analysis.md`
**Module index:** `docs/backend/apis/APPOINTMENT360_ERA_TASK_PACKS.md`
**Endpoint matrix:** `docs/backend/endpoints/appointment360_endpoint_era_matrix.json`
**Data lineage:** `docs/backend/database/appointment360_data_lineage.md`
**Postman checklist:** `docs/backend/postman/README.md` → Appointment360 section
**Era 8.x service reference:** `docs/8. Contact360 public and private apis and endpoints/appointment360-service.md`

---

## Mailvetter (`backend(dev)/mailvetter`) execution spine

**Service:** `backend(dev)/mailvetter` — verifier microservice (Go + Gin + Redis queue + PostgreSQL)
**Role:** Deep email verification engine for single and bulk verification flows, job tracking, and result export.

**Era task pack index:**

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.2 — Schema & migration bedrock.md` (Mailvetter rows in patch **Service task slices**)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `mailvetter-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `mailvetter-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `mailvetter-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `mailvetter-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `mailvetter-ai-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `mailvetter-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `mailvetter-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-email-campaign-task-pack.md` merged)

**Era execution spine summary:**

| Era | Primary mailvetter concern |
| --- | --- |
| `0.x` | API/worker foundation, queue + DB bootstrap, canonical `/v1` contract baseline |
| `1.x` | API key ownership and plan/rate governance aligned with billing and credits |
| `2.x` | **PRIMARY** — single/bulk verification contract, async job lifecycle, scoring model freeze |
| `3.x` | Contact/company verification lineage and freshness integration |
| `4.x` | Extension/SN source provenance and anti-abuse burst handling |
| `5.x` | AI explainability reason codes for verifier outcomes |
| `6.x` | Reliability hardening: distributed limiter, idempotency, retry/DLQ, SLO observability |
| `7.x` | Deployment governance: migration discipline and deprecation controls |
| `8.x` | Public/private API maturity: OpenAPI and scoped key contracts |
| `9.x` | Ecosystem integration: webhook replay and partner connector reliability |
| `10.x` | Campaign preflight verification and recipient-level compliance traceability |

**Codebase analysis:** `docs/codebases/mailvetter-codebase-analysis.md`
**Task-pack index:** `docs/backend/apis/MAILVETTER_ERA_TASK_PACKS.md`
**Endpoint matrix:** `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`
**Data lineage:** `docs/backend/database/mailvetter_data_lineage.md`
**Postman checklist:** `docs/backend/postman/README.md` → Mailvetter section
**Era 8.x service reference:** `docs/8. Contact360 public and private apis and endpoints/mailvetter-service.md`

---

## Email app era track — `contact360.io/email`

| Era | Email app status |
| --- | --- |
| 0.x | foundation shell and route structure |
| 1.x | auth + profile/account surface live |
| 2.x | core mailbox operations live (folder/detail/imap connect) |
| 3.x | preparatory integration points for contact enrichment |
| 4.x | extension parity hooks pending |
| 5.x | AI assistant UI placeholder present |
| 6.x | reliability hardening backlog (retry/backoff/telemetry) |
| 7.x | deployment and environment hardening required |
| 8.x | endpoint contract formalization in progress |
| 9.x | ecosystem export/integration hooks pending |
| 10.x | campaign handoff pathways pending |

## 2026 Evidence Addendum

### `0.x` stabilization status notes

- 📌 Planned: `backend(dev)/email campaign`: blocked by schema/query/auth wiring defects (`EC-0.1` to `EC-0.4`).
- 📌 Planned: `lambda/s3storage`: blocked by missing auth enforcement and in-memory multipart session state (`S3S-0.1`, `S3S-0.3`).
- 📌 Planned: `backend(dev)/mailvetter`: foundation delivered, but distributed limiter and canonical contract hardening remain.

### `1.1.0` in-progress evidence notes

- 📌 Planned: Billing/admin surfaces exist in `contact360.io/admin` and gateway integrations are active.
- 📌 Planned: Remaining gap: immutable credit-change audit timeline and approval workflow hardening.

### `2.x` and `6.x` gating notes

- 📌 Planned: `2.x` email-system progression depends on campaign-service P0 fixes before promotion.
- 📌 Planned: `6.x` reliability remains blocked while core services retain non-distributed in-memory control state in scale paths.


### Master era structure sync
- Era folders `0.x` through `10.x` now follow unified packet structure: README hub, 11 minor files, and 110 patch files with Flowchart + Micro-gate + Evidence gate sections.
- Remaining work is execution evidence closeout, not structural schema alignment.
