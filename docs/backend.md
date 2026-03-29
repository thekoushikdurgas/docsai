# Contact360 Backend (0.x-10.x)

Backend operating map for APIs, services, data stores, and era-aligned execution.

## Era-by-era backend surface

| Era | Theme | Modules | Tables | Service entrypoints |
|---|---|---|---|---|
| `0.x` | Foundation | auth, health | users, sessions | `api/main.py` |
| `1.x` | User/Billing/Credit | auth, users, billing, usage | users, user_profiles, addon_packages | auth/billing modules |
| `2.x` | Email system | email, jobs, mailbox REST | scheduler_jobs, user_activities | email services + mailvetter + `contact360.io/email` REST integration |
| `3.x` | Contacts/Companies | contacts, companies | saved_searches | connectra + graphql modules |
| `4.x` | Extension/SalesNav | linkedin, sales_navigator | user_scraping | Sales Navigator FastAPI Lambda + extension utilities (backend path complete through 4.2) |
| `5.x` | AI workflows | ai_chats | ai_chats, resume_documents | contact.ai + resumeai + admin AI assistant fallback chain (OpenAI -> Gemini -> Lambda AI) |
| `6.x` | Reliability | cross-cutting guards | n/a | slo/error budget systems |
| `7.x` | Deployment | admin, governance | activities | deployment and audit controls |
| `8.x` | Public/private APIs | webhooks | webhooks | webhook dispatcher |
| `9.x` | Ecosystem | integrations | integrations | connector framework |
| `10.x` | Email campaign | campaigns, sequences, templates | campaigns, sequences, templates | campaign engine workers |

## Era-to-module additions table

| Era | API modules emphasized | Data emphasis |
| --- | --- | --- |
| `1.x` | auth/users/billing/usage | users, credits, plans, invoices |
| `2.x` | email/jobs/upload | email verification/finder lifecycle |
| `3.x` | contacts/companies/s3 | contacts and companies dual-store lineage |
| `4.x` | linkedin/sales navigator | ingestion and sync integrity |
| `5.x` | ai chats/jobs | AI prompt/result lineage |
| `6.x` | analytics/activities/health | reliability telemetry and RC evidence |
| `7.x` | admin/authz | governance and audit trails |
| `8.x` | webhooks/integrations | public-private contract lineage |
| `9.x` | profile/notifications/2fa | tenant and ecosystem controls |
| `10.x` | campaigns/sequences/templates | campaign execution and compliance |

## `s3storage` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Freeze upload/list/download endpoint contracts | Stabilize S3/filesystem backend parity | Baseline health and smoke checks |
| `1.x` | Define object class policy (`avatar`, `photo`, `resume`) | Validate content type/size per path | Audit fields and abuse monitoring |
| `2.x` | Freeze multipart API contract | Durable multipart session store | Metadata freshness and retry telemetry |
| `3.x` | Define ingestion artifact contract | Robust schema/preview/stats behavior | Lineage for ingest/export artifacts |
| `4.x` | Extension-safe access and TTL policy | Channel-aware access controls | Source provenance in metadata |
| `5.x` | AI artifact and retention contract | Policy enforcement for AI artifacts | Sensitive artifact audit trails |
| `6.x` | Idempotency and SLO contract | Reconciliation and metadata write safety | Error budgets and incident runbooks |
| `7.x` | Service-to-service auth contract | Endpoint authz and retention hooks | Compliance evidence generation |
| `8.x` | Versioning/deprecation contract | Storage lifecycle event contracts | Compatibility and partner reliability gates |
| `9.x` | Entitlement and quota contract | Plan-aware throttling and limits | Tenant cost/residency reporting |
| `10.x` | Campaign artifact reproducibility contract | Immutable compliance storage paths | Compliance/audit sign-off evidence |

Deep reference: `docs/codebases/s3storage-codebase-analysis.md`.

## `logs.api` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Baseline log write/query contract | S3 CSV repository stabilization | Health and smoke checks |
| `1.x` | User/billing/credit event schema | Auth and billing event logging | Security and abuse monitoring |
| `2.x` | Job progress/result logging contract | Batch write optimization | Query latency and throughput evidence |
| `3.x` | Contact/company op logging schema | Support-focused filtering/search | Lineage and incident diagnostics |
| `4.x` | Extension/SN telemetry contract | Ingestion source tagging | Provenance and sync replay observability |
| `5.x` | AI workflow telemetry contract | AI event write policies | Cost and quality monitoring |
| `6.x` | SLO/error-budget evidence contract | Cache + stream path hardening | Reliability runbooks |
| `7.x` | Deployment audit contract | Release and environment event capture | Retention/compliance evidence |
| `8.x` | Public/private API audit contract | Key-scoped filtering and reports | Partner compatibility gates |
| `9.x` | Tenant ecosystem audit contract | Integration connector event logging | Tenant SLA evidence |
| `10.x` | Campaign audit/compliance contract | Immutable campaign event log flows | Compliance sign-off evidence |

## `connectra` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Baseline route + auth contract | Gin middleware and route bootstrap | PG/ES/index baseline checks |
| `1.x` | Credit-aware search/export contract | Query guards and over-limit handling | Billing linkage telemetry |
| `2.x` | CSV batch upsert/import contract | Job creation/list + stream pipeline behavior | Queue durability and retry metrics |
| `3.x` | VQL/query/filter contract freeze | `ListByFilters`, `CountByFilters`, `batch-upsert` hardening | ES/PG parity and facet integrity |
| `4.x` | SN provenance payload contract | Ingestion adapter to `batch-upsert` | Sync conflict + replay observability |
| `5.x` | AI-enrichment read contract | AI-oriented field and filter exposure | Enrichment lineage and confidence data |
| `6.x` | SLO/idempotency contract | Worker resilience and failure-path hardening | Error budgets, drift checks, runbooks |
| `7.x` | RBAC + privileged write policy | Authz for writes/exports/filter mutation paths | Audit and retention evidence |
| `8.x` | Versioned API contract | Partner-scoped key and endpoint maturity | Compatibility and webhook-readiness evidence |
| `9.x` | Entitlement/quota contract | Tenant-aware throttling and connector safety | SLA, quota, and capacity reporting |
| `10.x` | Campaign audience contract | Suppression-aware query and export paths | Compliance traceability and reproducibility |

## `emailapis` / `emailapigo` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Baseline endpoint and health contract | Runtime bootstrap and middleware hardening | DB connectivity and smoke checks |
| `1.x` | Credit-impact and verifier contract | Finder/verifier policy alignment | Billing/usage traceability |
| `2.x` | Email system contract freeze | Bulk finder/verifier and provider orchestration hardening | Cache/pattern lineage + latency evidence |
| `3.x` | Contact/company enrichment contract | Connectra identity and merge stability | Enrichment drift diagnostics |
| `4.x` | Extension provenance contract | Source-tagged lookups and sync resilience | Replay and sync observability |
| `5.x` | AI workflow email contract | Assistant-supporting orchestration paths | AI-assisted lineage and quality metrics |
| `6.x` | Reliability/SLO contract | Concurrency, timeout, retry hardening | Error budgets and incident runbooks |
| `7.x` | Deployment and governance contract | Environment parity and health checks | Release audit evidence |
| `8.x` | Public/private API contract | Partner-safe error and auth behavior | Compatibility and audit gates |
| `9.x` | Ecosystem entitlement contract | Tenant-aware controls and throttles | SLA and partner evidence |
| `10.x` | Campaign compliance contract | Deliverability/compliance-safe verification | Immutable audit and retention evidence |

## `jobs` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Baseline scheduler endpoint/status contract | API/scheduler/consumer/worker baseline | `job_node`/`edges`/`job_events` bootstrap |
| `1.x` | Credit-aware creation and retry contract | Billing-aware metadata and ownership checks | Billing/job traceability in timeline events |
| `2.x` | Email stream job contract freeze | Harden finder/verify/pattern processors | CSV lineage + checkpoint correctness |
| `3.x` | Contact import/export and VQL contract | `contact360_import_prepare`/`contact360_export_stream` hardening | PG/OpenSearch lineage + replay safety |
| `4.x` | Extension/SN provenance job contract | Source-tagged ingestion/sync jobs | Provenance and dedupe audit evidence |
| `5.x` | AI batch job contract extensions | AI processor stubs + quota-aware scheduling | Confidence/cost lineage in `job_response` |
| `6.x` | Idempotency/retry/DLQ contract | Recovery and resilience hardening | SLO/error-budget and incident evidence |
| `7.x` | Role-aware authz and retention contract | Access control + policy enforcement | `job_events` audit and retention compliance |
| `8.x` | Versioned API + webhook contract | Partner-safe submission and callback handling | Compatibility and callback delivery evidence |
| `9.x` | Tenant quota/entitlement contract | Tenant isolation and fairness scheduling | Tenant SLA and quota governance evidence |
| `10.x` | Campaign execution/compliance contract | Send/track/verify processor orchestration | Compliance bundles from timelines/events |

## `mailvetter` backend track by era

`backend(dev)/mailvetter` — Go 1.25, Gin, Redis queue workers, PostgreSQL (`pgx`). Deep SMTP/DNS/OSINT verifier with async bulk jobs.

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | `/v1` route and auth baseline | API+worker boot path stabilization | `jobs`/`results` migration baseline |
| `1.x` | Plan limits + key ownership | API key store hardening + usage capture | billing/usage linkage logs |
| `2.x` | Single/bulk/job/results contract freeze | scoring and queue lifecycle hardening | result/job lineage and status parity |
| `3.x` | contact/company linkage contract | verification metadata linking to Connectra IDs | relationship lineage and reconciliation |
| `4.x` | extension/SN provenance contract | source tagging and burst controls | provenance/dedupe audit evidence |
| `5.x` | AI explainability contract | reason-code summarization outputs | PII-safe AI evidence trail |
| `6.x` | idempotency + distributed limit + SLO | Redis limiter, retry/DLQ, failure states | queue lag/error budget dashboards |
| `7.x` | versioning + deprecation contract | migration pipeline split, prod gates | backup/restore and rollback runbooks |
| `8.x` | public/private API contract | OpenAPI + key scopes + rotation | API audit and quota evidence |
| `9.x` | ecosystem webhook/connector contract | webhook replay and partner adapters | delivery log and SLA evidence |
| `10.x` | campaign preflight contract | campaign-scale verification batching | campaign compliance evidence |

Deep reference: `docs/codebases/mailvetter-codebase-analysis.md`.

## `contact360.io/admin` (DocsAI Django) backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Baseline admin/auth route contracts | Django view bootstrap + template shell hardening | local DB baseline checks |
| `1.x` | billing/user admin contract | `apps/admin/views.py` payment/user controls + GraphQL bridge | payment audit traceability |
| `2.x` | email docs/control contract | documentation dashboard service wiring | dashboard query reliability metrics |
| `3.x` | contact/company relationship docs contract | relationship aggregation + graph payload generation | graph data consistency checks |
| `4.x` | extension/SN governance contract | docs/admin control views for SN-related inventories | provenance and sync diagnostics |
| `5.x` | AI tooling governance contract | ai-agent/admin surfaces and Python client call guards | AI workflow audit readiness |
| `6.x` | reliability/health contract | retries, cache strategy, health/system status views | runbooks, cache staleness checks |
| `7.x` | RBAC/deployment governance contract | `require_super_admin`, `require_admin_or_super_admin`, deploy script lifecycle | release evidence + access audits |
| `8.x` | private/public API governance contract | endpoint docs, OpenAPI exposure, contract administration | compatibility and policy evidence |
| `9.x` | ecosystem/platform governance contract | integration/admin control workflows | tenant governance evidence |
| `10.x` | campaign governance contract | campaign-aligned admin/compliance controls | immutable compliance traceability |

## `email campaign` backend track by era

`backend(dev)/email campaign` — Go 1.24, Gin, Asynq/Redis, PostgreSQL, AWS S3. Two-binary deployment: API server + async worker.

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Schema baseline, health/env contract, SMTP contract | Fix schema drift; SMTP auth; env validation; Docker | Bootstrap PG/Redis/S3; Dockerize API + worker binaries |
| `1.x` | Auth/billing/credit attribution contract | JWT middleware; credit pre-check guard on `/campaign` | Add user_id/org_id columns; credit log per campaign |
| `2.x` | SMTP provider, bounce/DLQ, retry contract | SMTP credentials; bounce webhook receiver; rate-limiter | Provider credential rotation; DLQ alert; delivery metrics |
| `3.x` | Audience source contract (segment/VQL/CSV) | Connectra REST audience resolver; replace CSV filepath | Recipient lineage from Connectra contact UUIDs |
| `4.x` | SN audience source contract | SN batch → Connectra → recipient pipeline | Enrichment-gated recipient resolution |
| `5.x` | AI template generation, personalization fields | `/templates/generate` endpoint; extend TemplateData | AI template metadata (model, prompt) in DB |
| `6.x` | SLO/DLQ/idempotency/resume contract | Graceful shutdown; resume-from-offset; circuit-breaker | HPA worker scaling; Prometheus campaign metrics |
| `7.x` | RBAC, audit log, governance contract | Role checks on routes; audit events → logs.api | Secrets in vault; deployment pipeline; readiness probe |
| `8.x` | GraphQL module, public REST v1, webhook contract | Campaign/template GraphQL resolvers; webhook dispatcher | Webhook delivery log; API usage metrics |
| `9.x` | Entitlement, suppression import, partner send contract | Entitlement middleware; suppression import endpoint | Sender domain table; integration suppression sync |
| `10.x` | Sequence engine, A/B test, analytics, compliance | Full sequences/tracking/scheduler/A/B implementation | Analytics aggregation cron; tracking pixel CDN |

Deep reference: `docs/codebases/emailcampaign-codebase-analysis.md`.

## `contact.ai` backend track by era

`backend(dev)/contact.ai` — FastAPI on AWS Lambda (Mangum), async SQLAlchemy, PostgreSQL `ai_chats` shared table, HF Inference Providers + Gemini fallback.

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Service skeleton, health endpoints, OpenAPI stub | FastAPI + Mangum scaffold; env wiring | `ai_chats` DDL + migration baseline |
| `1.x` | `X-User-ID` → `users.uuid` FK contract | `user_id` FK integrity; cascade strategy | Referential integrity validated; IAM hardened |
| `2.x` | `analyzeEmailRisk` request/response schema lock | `HFService` JSON task; email PII policy | Stateless call; no DB write; HF data retention reviewed |
| `3.x` | `parseContactFilters` + `generateCompanySummary` schema lock | NL filter parser; VQL alignment | JSONB `contacts[]` aligned with Connectra fields |
| `4.x` | SN contact object compatibility; extension CSP | SN contact JSONB round-trip test | SN provenance optionally tagged in JSONB |
| `5.x` | Full REST API contract: all chat + utility endpoints | All endpoints live; HF streaming; model fallback | `messages` validated; `model_version` in JSONB; 100-msg cap |
| `6.x` | SLO targets: sync p95 < 3s, SSE first-token p95 < 1s | SSE reliability; TTL; optimistic lock; tracing | `version` column; archival policy; atomic `updated_at` |
| `7.x` | RBAC for AI features; per-tenant API keys; retention policy | Feature gate middleware; GDPR erasure cascade | Audit log to `logs.api`; retention enforced |
| `8.x` | Rate limit headers; scoped API keys; usage tracking | Rate limit headers on all routes; usage counters | `api_usage` or `ai_usage_log` schema |
| `9.x` | Connector spec; webhook delivery contract | Webhook dispatcher; connector adapter | Webhook delivery log; integration audit trail |
| `10.x` | Campaign AI generation endpoint; compliance evidence schema | `POST /api/v1/ai/email/generate`; bulk generation | `campaign_ai_log` table; immutable audit evidence |

Deep reference: `docs/codebases/contact-ai-codebase-analysis.md`.

## `salesnavigator` backend track by era

`backend(dev)/salesnavigator` — FastAPI on AWS Lambda (Mangum), no local DB, all persistence via Connectra (`/contacts/bulk`, `/companies/bulk`). Stateless ingestion service with deterministic UUID5 strategy, HTML extraction pipeline, and deduplication.

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | UUID5 deterministic contract; health spec | FastAPI+Mangum scaffold; SAM template; env wiring | UUID generation rules documented; smoke tests |
| `1.x` | Actor context headers contract; billing event stub | `X-User-ID`/`X-Org-ID` pass-through; billing stub | `actor_id`/`org_id` in Connectra contact metadata |
| `2.x` | Email field handoff contract (SN → email finder) | Email/phone field validation; enrichment queue stub | `email`, `email_status` field presence validated |
| `3.x` | Full field mapping contract; provenance tags | `mappers.py` fully implemented; provenance fields | `source=sales_navigator`, `lead_id`, `search_id` in Connectra |
| `4.x` | API semantics locked; docs drift fixed | HTML extraction hardened; full extension UX | `data_quality_score`, `recently_hired`, `is_premium` |
| `5.x` | AI field requirements; `data_quality_score` VQL contract | `seniority`, `departments`, `about` quality gated | `data_quality_score` indexed for AI context |
| `6.x` | SLO contract; rate limit and CORS policy | Rate limiter; chunk idempotency; CORS hardened | Load tests; error budget dashboards; `X-Request-ID` |
| `7.x` | RBAC and per-tenant key contract; GDPR cascade | Per-tenant API keys; audit event per save | Immutable audit events; GDPR erasure via Connectra |
| `8.x` | Rate-limit headers; versioned path; usage tracking | `X-RateLimit-*` headers; usage counters | `api_usage` table; quota enforcement |
| `9.x` | Connector adapter contract; webhook delivery | Adapter layer; webhook retry delivery | Connector audit trail; tenant lineage |
| `10.x` | Campaign provenance; suppression non-overwrite | Suppression guard on re-ingest; `lead_id` → campaign | Campaign audience traceability to SN session |

Deep reference: `docs/codebases/salesnavigator-codebase-analysis.md`.

## `appointment360` (contact360.io/api) backend track by era

`contact360.io/api` — FastAPI 0.11x, Strawberry GraphQL (code-first), asyncpg, async SQLAlchemy, PostgreSQL, custom 8-layer middleware stack, Mangum (AWS Lambda). Primary GraphQL gateway — 28 modules, single `/graphql` endpoint.

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Schema root, health endpoint contracts, Pydantic settings model | FastAPI app bootstrap, full middleware stack registration, DB session lifecycle, Mangum handler | `users`, `token_blacklist` tables; `.env.example`; Docker |
| `1.x` | Auth mutation types (login/register/refresh/logout), billing/usage GraphQL contracts, credit model schema | JWT auth service, credit deduction, billing service, idempotency on billing mutations, abuse guard config | `credits`, `plans`, `subscriptions`, `payment_submissions`, `activities` |
| `2.x` | Email module types (finder/verifier), jobs module types (create/list/status), SchedulerJob type | `LambdaEmailClient`, `TkdjobClient`, remove debug writes from `email/queries.py` and `jobs/mutations.py` | Activity entries for email jobs; tkdjob + lambda email env vars |
| `3.x` | Contacts/companies module types, VQLQueryInput type, filter/filterData types | `ConnectraClient`, `vql_converter.py`, `connectra_mappers.py`, DataLoaders for N+1 prevention | Contacts/companies stored in Connectra; `saved_searches` in appointment360 DB; Connectra env vars |
| `4.x` | LinkedIn/SalesNavigator module types, extension session auth contract | `sales_navigator_client.py`, `upsertByLinkedinUrl`, extension token validation, SN credit deduction | `sessions` table; SN results → Connectra; abuse guard on LinkedIn mutations |
| `5.x` | AI chats module types, resume module types, model selection type | `LambdaAIClient`, `ResumeAIClient`, AI credit deduction per call | `ai_chats`, `ai_chat_messages`, `resumes`; AI API env vars |
| `6.x` | SLO/complexity/timeout/rate limit/idempotency/abuse guard contracts documented | Enable all middleware guards for production, Redis state sharing for idempotency + abuse guard | `idempotency_keys` fallback table; slow-query logging; load tests; SLO alerts |
| `7.x` | Deployment targets (EC2/Lambda), health readiness, RBAC/SuperAdmin guards | Mangum cold-start < 3s, graceful shutdown, CI/CD pipeline, `require_admin`/`require_super_admin` | Alembic migration hygiene; Dockerfile; GitHub Actions CI/CD |
| `8.x` | Pages/DocsAI module, saved searches module, profile/API keys module, public API `X-API-Key` auth contract | `DocsAIClient`, `apiKeys` CRUD, 2FA TOTP (`pyotp`), `X-API-Key` guard, `DOCSAI_ENABLED` health check | `api_keys`, `sessions`, `saved_searches` tables; DocsAI env vars; public API Postman collection |
| `9.x` | Notifications module, analytics module, admin panel module, tenant model | Notification service, analytics event tracking, plan-entitlement guard, `require_super_admin` for admin | `notifications`, `events`, `feature_flags`, `workspaces` tables |
| `10.x` | Campaigns/sequences/templates GraphQL module contracts, campaign wizard orchestration | `CampaignServiceClient` proxy to email campaign service, credit deduction per recipient, abuse guard | Campaign data in campaign service DB; activity entries in appointment360 DB; campaign env vars |

Deep reference: `docs/codebases/appointment360-codebase-analysis.md`.

> **Era-specific operational docs:** RBAC and access-control patterns → `docs/7. Contact360 deployment/rbac-authz.md`. Idempotency and SLO contracts → `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md`. Webhook delivery and replay → `docs/8. Contact360 public and private apis and endpoints/webhooks-replay.md`. Queue resilience and observability → `docs/6. Contact360 Reliability and Scaling/queue-observability.md`. Connector framework and commercial controls → `docs/9. Contact360 Ecosystem integrations and Platform productization/connectors-commercial.md`.

### DocsAI backend implementation notes

- Python GraphQL transport: `contact360.io/admin/apps/core/services/graphql_client.py` (`httpx`, retries, backoff, cache-aware wrappers).
- Appointment360 bridge: `contact360.io/admin/apps/core/clients/appointment360_client.py`.
- Admin operation bridge: `contact360.io/admin/apps/admin/services/admin_client.py`.
- Access-control decorators are first-class backend contract gates:
  - `require_super_admin`
  - `require_admin_or_super_admin`
- Data sources span local Django persistence, Appointment360 GraphQL, Redis cache, and S3 index artifacts.

---

## Extension backend track — `extension/contact360`

### Extension backend dependencies

| Backend service | Endpoint | Protocol | Called from |
| --- | --- | --- | --- |
| Appointment360 (GraphQL gateway) | `POST /graphql` → `mutation { auth { refreshToken(...) } }` | GraphQL over HTTPS | `auth/graphqlSession.js` |
| Lambda Sales Navigator API | `POST /v1/save-profiles` | REST/HTTPS | `utils/lambdaClient.js` |
| Connectra (via Lambda relay) | `POST /contacts/bulk` | REST/HTTPS (internal) | Lambda SN API → Connectra |
| Connectra (via Lambda relay) | `POST /companies/bulk` | REST/HTTPS (internal) | Lambda SN API → Connectra |

### Extension per-era backend track

| Era | Backend work driven by extension |
| --- | --- |
| `0.x` | Extension folder scaffolded; no backend calls deployed |
| `1.x` | `auth.refreshToken` mutation implemented in Appointment360; `chrome.storage.local` token lifecycle established |
| `3.x` | Lambda SN API `/v1/save-profiles` endpoint created; Connectra `/contacts/bulk` and `/companies/bulk` bulk ingestion endpoints activated |
| `4.x` | Lambda SN API hardened for production volume; retry/back-off client in `lambdaClient.js`; Connectra bulk indexing at scale |
| `6.x` | Extension client adaptive timeout and request queueing; Connectra ingestion pipeline reliability improvements |
| `8.x` | `/v1/save-profiles` documented as private internal API; `auth.refreshToken` documented as public GraphQL mutation |
| `9.x` | Extension ingestion data feeds Ecosystem integrations (SN profiles → Connectra → downstream platform) |
| `10.x` | Bulk-ingested SN contacts available as email campaign audience sources |

### Lambda SN API contract (as consumed by extension)

```
POST /v1/save-profiles
Headers:
  Authorization: Bearer <accessToken>
  Content-Type: application/json
Body:
  {
    "profiles": [
      {
        "profile_url": "https://linkedin.com/in/...",
        "name": "...",
        "title": "...",
        "company": "...",
        "email": "...",
        "phone": "...",
        "location": "...",
        "connections": "..."
      }
    ]
  }
Response:
  {
    "saved": <number>,
    "errors": [{ "profile_url": "...", "reason": "..." }]
  }
```

### Appointment360 auth mutation (as consumed by extension)

```graphql
mutation RefreshToken($refreshToken: String!) {
  auth {
    refreshToken(refreshToken: $refreshToken) {
      accessToken
      refreshToken
      expiresIn
    }
  }
}
```
---

## Email frontend backend track — `contact360.io/email`

| API contract | Endpoint | Consumer |
| --- | --- | --- |
| Login | `POST /auth/login` | `login-form.tsx` |
| Signup | `POST /auth/signup` | `signup-form.tsx` |
| User profile read | `GET /auth/user/{userId}` | sidebar and account page |
| Logout | `POST /logout` | `nav-user.tsx` |
| Folder email list | `GET /api/emails/{folder}` | `email-list.tsx` |
| Email detail | `GET /api/emails/{mailId}?folder={folder}` | `app/email/[mailId]/page.tsx` |
| IMAP accounts read | `GET /api/user/{userId}` | account page |
| Profile update | `PUT /api/user/update/{userId}` | account page |
| IMAP account connect | `POST /api/user/imap/{userId}` | account page |

### Email app data flow notes
- Frontend is stateless for persistence and consumes backend APIs via `NEXT_PUBLIC_BACKEND_URL`.
- HTML email body rendering is sanitized using DOMPurify before `dangerouslySetInnerHTML`.
- Current credential transport (`X-Email`, `X-Password`) is documented as legacy/high-risk and should migrate to tokenized mailbox sessions.

## `contact360.io/admin` cross-era execution stream

- `0.x`: Django foundation, core apps wiring, middleware baseline, admin shell and service clients.
- `1.x`: Billing/payment review and user admin surfaces live; credit-change audit timeline still incomplete.
- `2.x`: Email operations surfaces partially present; provider health and suppression governance views pending.
- `3.x`: Contact/company lineage operations are partial and mostly downstream-proxy; conflict-resolution views pending.
- `4.x`: Extension/Sales Navigator operator controls are planned and not yet complete.
- `5.x`: AI governance and cost controls are partial; prompt/version/cost observability requires expansion.
- `6.x`: Reliability controls are in progress (throttling consistency, trace IDs, SLO views).
- `7.x`: Deployment and DR controls are partial; CI production-readiness gates need tightening.
- `8.x`: Public/private API boundary for admin APIs remains incomplete and requires explicit versioning.
- `9.x`: Partner-safe access, webhook replay tooling, and tenant policy overlays are planned.
- `10.x`: Campaign ops console and compliance evidence workflows are planned.

### Era task-pack links (admin)

- `docs/0. Foundation and pre-product stabilization and codebase setup/admin-foundation-task-pack.md`
- `docs/1. Contact360 user and billing and credit system/admin-user-billing-task-pack.md`
- `docs/2. Contact360 email system/` — era `2.x` minors/patches (admin surfaces tied to email era ship in minor docs + patch **Micro-gate**)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; admin Contact360 scope folded into era patches; no standalone `admin-contact-company-task-pack.md`)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; admin Extension/SN scope folded into era patches; no standalone `admin-extension-sn-task-pack.md`)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; admin AI scope folded into era patches; no standalone `admin-ai-workflows-task-pack.md`)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; admin reliability scope folded into gateway minors — no standalone `admin-reliability-scaling-task-pack.md`)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; admin deployment folded into gateway minors — no standalone `admin-deployment-task-pack.md`)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `admin-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `admin-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `admin-email-campaign-task-pack.md` merged)

## P0 correction notes (cross-service)

- 📌 Planned: `lambda/s3storage` auth and multipart durability gap closure (`S3S-0.1`, `S3S-0.3`).
- 📌 Planned: `lambda/logs.api` storage-contract canonicalization to S3 CSV (`LOG-0.1`).
- 📌 Planned: `lambda/emailapigo` logging secret/env hardening (`EGO-0.4`).
- 📌 Planned: `backend(dev)/email campaign` unsubscribe, schema parity, and SMTP/config hardening blocker closure (`EC-0.1` to `EC-0.4`).

## s3storage routing compliance matrix

| Service | Status |
| --- | --- |
| appointment360 | ✅ uses S3StorageClient |
| contact360.io/jobs | 📌 Planned migrate direct S3 paths |
| backend(dev)/contact.ai | 📌 Planned audit/migrate |
| backend(dev)/email campaign | 📌 Planned migrate direct S3 paths |
| backend(dev)/mailvetter | 📌 Planned audit/migrate |
| backend(dev)/resumeai | 📌 Planned confirm/migrate |
| contact360.io/admin | 📌 Planned confirm/migrate |

## System & API Contracts
- [Service Mesh Contracts](backend/apis/00_SERVICE_MESH_CONTRACTS.md)
- [SalesNavigator UUID5 Contract](backend/apis/17_SALESNAVIGATOR_UUID5_CONTRACT.md)
- [Foundation Exit Gate Signoff](backend/apis/21_FOUNDATION_EXIT_GATE_SIGNOFF.md)
