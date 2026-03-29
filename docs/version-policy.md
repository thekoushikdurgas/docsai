# Contact360 Version Policy

## SemVer policy

- **Major (`X.0.0`)**: New product era, major channel expansion, or foundational architecture shift.
- **Minor (`X.Y.0`)**: New feature sets within an existing product era.
- **Patch (`X.Y.Z`)**: Bug fixes and reliability/performance improvements without scope expansion.
- **Ownership**: Product + engineering leads approve version bumps per shipped scope.

## Decision rubric (Contact360 specific)

- Use a **major** bump when introducing a new platform capability family (for example, moving from core user/billing to the email system era, or from email to contact/company data).
- Use a **minor** bump when adding a customer-visible capability in an existing major (for example, new billing flows, analytics panels, extension telemetry).
- Use a **patch** bump for hotfixes, edge-case fixes, retry logic hardening, and non-breaking operational updates.
- Critical credential/secret exposure fixes (for example plaintext credentials or leaked default secrets) must ship as patch releases immediately, even when the related major/minor era scope is unchanged.

## Release entry schema

Every release entry in `docs/versions.md` should include:

- `version`
- `status` (`released`, `in_progress`, `planned`)
- `released_on` (or `target_window` if planned)
- `summary`
- `scope`
- `Roadmap mapping` (roadmap stage IDs; canonical display label in `docs/versions.md`, equivalent to `ships_stages`)
- `owner`

## Version hygiene rules

- **Repo paths:** Canonical product and gateway paths are under **`contact360.io/`** (see `docs/architecture.md`). Older stubs may reference `contact360/dashboard` or `lambda/appointment360/` — align to `contact360.io/app/` and `contact360.io/api/` when editing links or code pointers.
- Do not pre-generate placeholder versions.
- Create version entries only when scope is approved (`planned`) or shipped (`released`).
- Keep `docs/versions.md` and `docs/roadmap.md` cross-referenced on every release update.
- Use `Roadmap mapping` as the release-entry field label consistently in `docs/versions.md`.

---

## Major themes (`0.x` to `10.0.0`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- Initial repository setup, service skeletons, CI pipelines, base authentication primitives, DocsAI bootstrap, and internal experiments.
- Core concern: repo hygiene, service wiring, and pre-product foundation readiness.

### `1.x.x` - Contact360 user and billing and credit system

- User authentication and session management, credit lifecycle (deduction, top-up, lapse), billing/payment flows, user-facing analytics, notifications, admin control panel, and basic security baseline.
- Core concern: the end-to-end user account lifecycle and credit economy.

### `2.x.x` - Contact360 email system

- Email finder engine (multi-pattern generation, high-throughput Go path, provider fallback), email verification engine (Mailvetter, DNS/SMTP/SPF), results surface, and bulk CSV processing.
- Core concern: the complete email discovery and verification product experience.

### `3.x.x` - Contact360 contact and company data system

- Connectra VQL filtering, dual-write PostgreSQL + Elasticsearch, enrichment quality, deduplication, deterministic UUID assignment, and advanced dashboard search UX.
- Core concern: contacts and companies intelligence, search depth, and data quality.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- Browser extension auth/session hardening, Sales Navigator ingestion reliability, sync integrity and conflict resolution, and extension telemetry.
- Core concern: Sales Navigator channel quality and extension reliability.

### `5.x.x` - Contact360 AI workflows

- Contact AI integration into user journeys, HF streaming and Gemini utilities, confidence and explainability controls, AI cost governance, and prompt versioning.
- Core concern: AI-assisted user workflows and responsible AI operations.

### `6.x.x` - Contact360 Reliability and Scaling

- SLO baselines and error budgets, idempotency hardening, queue/worker resilience, correlated observability, performance optimization, storage lifecycle, cost guardrails, and abuse resilience.
- Core concern: platform reliability, throughput capacity, and operational hardening.

### `7.x.x` - Contact360 deployment

- RBAC model and access control, service-level authorization, admin governance, audit/compliance event model, data governance and lifecycle, tenant/policy isolation, security posture hardening, and enterprise observability.
- Core concern: secure, auditable, and governable deployment across environments.

### `8.x.x` - Contact360 public and private APIs and endpoints

- Analytics taxonomy and event instrumentation, analytics ingestion hardening, private service-to-service API contracts, public GraphQL/REST API surface, API versioning and compatibility policy, webhook/event delivery platform, partner identity and access controls, and API documentation.
- Core concern: stable, versioned, and observable API contracts for all consumers (internal, partner, and public).

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- Integration contract governance, connector framework, integration observability, commercial entitlements, multi-tenant model standardization, self-serve workspace administration, plan packaging engine, SLA/SLO operations, support and incident tooling, cost/capacity governance.
- Core concern: third-party ecosystem connectivity and multi-tenant platform maturity.

### `10.x.x` - Contact360 email campaign

- Campaign entity model, audience segmentation, policy gates (consent, content, rate limits), suppression lists, template system, campaign execution engine, deliverability and safety (Mailvetter pre-send), campaign observability and structured logging, feature flags and canary rollouts, send metering, PII retention, opt-out auditing, and contract freeze for reproducibility.
- Core concern: compliant, observable, and commercially controlled email campaign delivery.

---

## Planning granularity standard (mandatory)

For all planned minors (`X.Y.0`), break implementation into these minimum task groups:

- **Contract tasks**: schema/policy/event contract changes and compatibility notes.
- **Service tasks**: API/service implementation tasks per owning backend.
- **Surface tasks**: dashboard/extension/docsai UI integration tasks.
- **Data tasks**: storage/index/lineage changes and validation tasks.
- **Ops tasks**: rollout guardrails, observability, and incident readiness tasks.

Each `docs/versions.md` minor entry should map to at least one roadmap stage and one owner group.

Reference strategic-era breakdown: `docs/roadmap.md` (stages `7.x`–`10.x`) and `docs/versions.md` / optional `docs/versions/version_*.md`.

---

## Era-to-system mapping summary

| Era | Major theme | Primary services | Key contract boundary |
| --- | --- | --- | --- |
| `0.x` | Foundation | All (setup) | Repo + CI baseline |
| `1.x` | User, billing, credit | `appointment360`, `logs.api` | User/credit/billing GraphQL contracts |
| `2.x` | Email system | `emailapis`, `emailapigo`, `mailvetter`, `appointment360`, `tkdjob` | Finder/verifier API contract |
| `3.x` | Contact/company data | `connectra`, `appointment360`, `tkdjob` | VQL filter and search contracts |
| `4.x` | Extension and Sales Navigator | `salesnavigator`, `appointment360`, `extension`, `tkdjob` | Extension auth and sync contracts |
| `5.x` | AI workflows | `contact.ai`, `appointment360`, `tkdjob` | AI chat/utility API and cost contracts |
| `6.x` | Reliability and Scaling | All core services, `tkdjob` | SLO, idempotency, and observability contracts |
| `7.x` | Deployment | `appointment360`, `docsai`, all services, `tkdjob` | RBAC, audit, and governance contracts |
| `8.x` | Public and private APIs | `appointment360`, `tkdjob`, `logs.api` | External API/webhook/analytics contracts |
| `9.x` | Ecosystem + Productization | All services + integrations | Tenant, entitlement, and connector contracts |
| `10.x` | Email campaign | `appointment360`, `tkdjob`, `emailapis`, `logs.api` | Campaign execution and compliance contracts |

---

## Related documentation

- `docs/versions.md` — release entries and index (this policy governs their shape).
- `docs/roadmap.md` — stages and `ships in` metadata.
- `docs/architecture.md` — planning horizon and service ownership.
- `docs/docsai-sync.md` — when roadmap or architecture changes require Django constant mirrors.

## Documentation schema requirements for per-minor files

Every `docs/versions/version_*.md` file must include the following explicit sections:

- `## Backend API and Endpoint Scope`
- `## Database and Data Lineage Scope`
- `## Frontend UX Surface Scope`
- `## UI Elements Checklist`
- `## Flow/Graph Delta for This Minor`
- `## Release Gate and Evidence`

These sections are mandatory for new and existing minors and should contain concrete file/module references, not generic placeholders.

## Era-to-surface and era-to-api module matrix

| Era | Primary frontend surfaces | Primary backend API modules |
| --- | --- | --- |
| `0.x` | setup/status/docs placeholders | health/bootstrap metadata |
| `1.x` | auth, billing, usage, settings | auth, users, billing, usage |
| `2.x` | email finder, verifier, results | email, jobs, upload/export |
| `3.x` | contacts, companies, files, export | contacts, companies, s3, upload |
| `4.x` | extension and sales navigator views | linkedin, sales navigator |
| `5.x` | AI chat and AI utilities | ai chats, jobs |
| `6.x` | analytics and activity operations | analytics, activities, health |
| `7.x` | admin governance and deployment views | admin, authz, audit |
| `8.x` | integrations and API docs | webhooks, integrations, api keys |
| `9.x` | profile, docs, 2FA, ecosystem pages | profile, notifications, saved searches, 2FA |
| `10.x` | campaigns, sequences, templates | campaigns, sequences, campaign templates |

## Era-to-storage maturity matrix (`s3storage`)

| Era | Storage maturity theme | Key storage concern |
| --- | --- | --- |
| `0.x` | Bootstrap | Service wiring, endpoint baseline, key taxonomy |
| `1.x` | User artifacts | Avatar/photo/payment-proof handling and validation |
| `2.x` | Bulk file engine | Multipart upload durability and metadata readiness |
| `3.x` | Data intelligence feed | Ingestion/export lineage and analysis quality |
| `4.x` | Channel maturity | Extension/SN provenance and access policy |
| `5.x` | AI artifact governance | Sensitive artifact lifecycle and policy enforcement |
| `6.x` | Reliability hardening | Idempotency, reconciliation, SLO/error budget coverage |
| `7.x` | Governance controls | Authz, retention/deletion, compliance evidence |
| `8.x` | API externalization | Versioned storage contracts and delivery/replay semantics |
| `9.x` | Productization | Entitlements, quotas, tenant economics |
| `10.x` | Campaign compliance | Reproducible campaign artifacts and audit trail guarantees |

## Era-to-logging maturity matrix (`logs.api`)

| Era | Logging maturity goal |
| --- | --- |
| `0.x` | Basic service health and event persistence baseline |
| `1.x` | User/billing/credit auditable event trail |
| `2.x` | High-volume email workflow telemetry reliability |
| `3.x` | Data pipeline support diagnostics and lineage |
| `4.x` | Extension/SN provenance and sync diagnostics |
| `5.x` | AI workflow and cost telemetry governance |
| `6.x` | SLO/error-budget observability and runbook evidence |
| `7.x` | Deployment/audit governance and retention evidence |
| `8.x` | API ecosystem observability and compatibility signals |
| `9.x` | Tenant/platform integration governance trail |
| `10.x` | Campaign compliance-grade immutable audit events |

## Jobs maturity matrix (`contact360.io/jobs`)

| Era | Jobs maturity theme | Key dependency |
| --- | --- | --- |
| `0.x` | Scheduler baseline and DAG primitives | API + Kafka + scheduler DB bootstrap |
| `1.x` | Billing-aware job governance | Billing/usage traceability contracts |
| `2.x` | Email stream processing maturity | `emailapis`/`emailapigo` + `s3storage` |
| `3.x` | Contact/company import-export stream maturity | Connectra/VQL + Contact360 PG/OpenSearch |
| `4.x` | Extension/SN provenance jobs | extension + salesnavigator ingest flows |
| `5.x` | AI batch orchestration | AI workflow contracts and quota services |
| `6.x` | Reliability and idempotency hardening | SLO/observability + retry/DLQ controls |
| `7.x` | Governance and access controls | RBAC/authz + retention policy |
| `8.x` | Versioned partner-safe jobs API | webhook/callback and API versioning |
| `9.x` | Tenant-aware scheduling productization | entitlement engine and tenant quotas |
| `10.x` | Campaign compliance execution | campaign orchestration + immutable audit evidence |

## Contact AI maturity matrix (`backend(dev)/contact.ai`)

Service: FastAPI Lambda — HF Inference + Gemini fallback — `ai_chats` PostgreSQL table shared with appointment360.

| Era | Contact AI maturity theme | Key service dependency |
| --- | --- | --- |
| `0.x` | Lambda skeleton + DDL baseline | FastAPI + Mangum + `ai_chats` DDL + health endpoints |
| `1.x` | User FK integrity + IAM | `users.uuid` FK constraint; cascade strategy; secrets management |
| `2.x` | Email risk analysis contract | `analyzeEmailRisk` endpoint; HF JSON task; PII policy |
| `3.x` | Filter parsing + company summary | `parseContactFilters` aligned to Connectra VQL; `generateCompanySummary` |
| `4.x` | SN contact JSONB compatibility | SN contact fields in `messages.contacts[]`; extension CSP |
| `5.x` | Full AI workflows live | All chat CRUD + SSE streaming + all utility endpoints; `ModelSelection` shim |
| `6.x` | Reliability and SLO | SSE error handling; TTL archival; optimistic lock; distributed tracing |
| `7.x` | RBAC + audit + retention | Feature gating by plan; GDPR erasure cascade; audit log to `logs.api` |
| `8.x` | Public API surface | Rate limit headers; scoped API keys; usage tracking; quota UI |
| `9.x` | Ecosystem connectors | Webhook AI delivery; connector adapter; integration panel |
| `10.x` | Campaign AI generation | `POST /api/v1/ai/email/generate`; `campaign_ai_log` compliance table |

## Era-to-system mapping summary (all services)

| Era | Services active |
| --- | --- |
| `0.x` | appointment360, connectra, emailapis, logs.api, s3storage, tkdjob (skeleton), contact.ai (skeleton) |
| `1.x` | + billing module, contact.ai (FK validation) |
| `2.x` | + emailapigo, mailvetter, tkdjob (email processors), contact.ai (analyzeEmailRisk) |
| `3.x` | + connectra (VQL), tkdjob (import/export), contact.ai (parseFilters + companySummary) |
| `4.x` | + salesnavigator (full extension UX, HTML extraction, Connectra ingest), extension, contact.ai (SN JSONB compat) |
| `5.x` | + contact.ai (full), resumeai, tkdjob (AI batch) |
| `6.x` | All core services + SLO, contact.ai (reliability), tkdjob (idempotency) |
| `7.x` | All + RBAC/audit across all services including contact.ai |
| `8.x` | All + public API surface including contact.ai scoped keys |
| `9.x` | All + ecosystem connectors including contact.ai webhook delivery |
| `10.x` | All + campaign engine including contact.ai campaign AI generation |

## `salesnavigator` service maturity matrix

| Era | Maturity level | Key deliverable |
| --- | --- | --- |
| `0.x` | Scaffold | Health endpoint, UUID contract |
| `1.x` | Auth/actor stub | Actor context headers |
| `2.x` | Field validation | Email/phone handling |
| `3.x` | Field mapping | Full provenance tagging |
| `4.x` | **GA / Primary** | Extension UX, HTML extraction, docs fix |
| `5.x` | AI integration | Quality gates for AI context |
| `6.x` | Hardened | Rate limiting, idempotency, CORS |
| `7.x` | Governed | RBAC, per-tenant keys, GDPR |
| `8.x` | API product | Rate-limit headers, usage tracking |
| `9.x` | Platform | Connector adapter, webhook delivery |
| `10.x` | Compliant | Campaign provenance, suppression guard |

## `mailvetter` service maturity matrix

| Era | Maturity level | Key deliverable |
| --- | --- | --- |
| `0.x` | Scaffold | API/worker split, `/v1` baseline, DB/queue bootstrap |
| `1.x` | Guarded | API key ownership and plan limits |
| `2.x` | **GA / Primary** | Single/bulk verifier and async jobs contract |
| `3.x` | Linked | Contact/company verification lineage |
| `4.x` | Provenance-aware | Extension/SN source-tagged verification |
| `5.x` | AI-ready | Explainability reason codes for AI surfaces |
| `6.x` | Hardened | Distributed limiter, idempotency, retry/DLQ |
| `7.x` | Governed | Migration discipline and release gates |
| `8.x` | API product | OpenAPI, scoped keys, audit-ready public/private surface |
| `9.x` | Platform | Partner webhook replay and connector reliability |
| `10.x` | Compliant | Campaign preflight verification and traceability |

**Pre-4.x planning note:** The `salesnavigator` service has documented gaps that must be resolved before the `4.x` era GA gate: missing `POST /v1/scrape-html-with-fetch` implementation, stale README, no rate limiting, no `X-Request-ID` header, wide-open CORS, and a single global `API_KEY` (per-tenant scoping is a `7.x` deliverable). Full details and remediation tasks: **`docs/codebases/salesnavigator-codebase-analysis.md`**.

---

> **Email app era track** (`contact360.io/email`) is maintained in **`docs/backend.md`** under the `Email frontend backend track` section, and in **`docs/architecture.md`** under the `Email app surface register` section. Do not duplicate it here.

## 2026 Policy Addendum

- A service with unresolved P0 defects (correctness, auth bypass, or non-durable distributed state) cannot be promoted to the next era stage.
- `contact360.io/admin` releases require migration/static asset/system process validation in deployment evidence.
- Services relying on runtime auto-migration must add explicit migration pipeline controls before `6.x` reliability promotion.
