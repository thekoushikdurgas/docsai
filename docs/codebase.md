# Contact360 Codebase Deep Map

**Frontend surfaces (dashboard, marketing, DocsAI, extension):** see **`docs/frontend.md`**. **Backend services:** **`docs/backend.md`**.
**Deep per-service analyses:** see **`docs/codebases/README.md`**.

**Stack direction:** **`docs/docs/backend-language-strategy.md`** (Python GraphQL gateway + Go/Gin satellites).

## Monorepo structure

This table lists the **canonical service and app folders** for this workspace. Legacy paths are tracked separately below.

| Path | Role | Primary tech | Primary API entry |
| --- | --- | --- | --- |
| `contact360.io/app/` | Authenticated product (dashboard) | Next.js 16, React 19, TypeScript | GraphQL via `contact360.io/api` |
| `contact360.io/root/` | Public marketing site | Next.js 16, React 19, TypeScript | Mixed (static + GraphQL for forms where used) |
| `contact360.io/admin/` | DocsAI — internal roadmap/architecture mirrors and control plane | Django | Internal / admin (GraphQL → `contact360.io/api`) |
| `contact360.io/email/` | Mailbox/email web surface | Next.js 16, React 19, TypeScript | Mixed (GraphQL auth + REST mailbox backend) |
| `contact360.io/api/` | Appointment360 GraphQL gateway | FastAPI (Python), Strawberry GraphQL | GraphQL (`/graphql`) |
| `contact360.io/sync/` | Connectra search / VQL data plane | Go (Gin), Elasticsearch | REST / internal |
| `contact360.io/jobs/` | TKD Job scheduler and DAG workers | Python (gateway client) + Go (EC2 job server) | REST / internal |
| `contact360.io/joblevel/` | Joblevel recruiting UI | Next.js App Router | GraphQL via `contact360.io/api` |
| `EC2/ai.server/` | AI + resume AI service (`contact360.io/ai`) | Go (Gin) | REST / internal |
| `EC2/email.server/` | Email APIs (finder/verifier) service (`contact360.io/emailapi`) | Go (Gin) | REST / internal |
| `EC2/email campaign/` | Email campaign engine (`contact360.io/emailcampaign`) | Go (Gin), Asynq (Redis) | REST / internal |
| `EC2/extension.server/` | Sales Navigator / extension façade (`contact360.io/extension`) | Go (Gin) | REST / internal |
| `EC2/log.server/` | Logs API service (`contact360.io/logsapi`) | Go (Gin) | REST / internal |
| `EC2/s3storage.server/` | S3 storage control plane (`contact360.io/s3storage`) | Go (Gin) | REST / internal |
| `contact360.extension/` | Chrome extension codebase (MV3) | JavaScript / TypeScript | GraphQL via `contact360.io/api` + REST to satellites |

## Legacy and alternate paths

Older docs and some historical monorepos use different folder layouts. Treat these as **aliases only**; new work should reference the canonical paths above.

| Older / logical path | Typical role | Canonical in this workspace |
| --- | --- | --- |
| `contact360/dashboard/` | Dashboard app | `contact360.io/app/` |
| `contact360/marketing/` | Marketing site | `contact360.io/root/` |
| `contact360/docsai/` | Django DocsAI | `contact360.io/admin/` |
| `lambda/appointment360/` | GraphQL gateway | `contact360.io/api/` |
| `lambda/connectra/` | Connectra | `contact360.io/sync/` |
| `EC2/email.server`, `EC2/sync.server` | Async jobs (finder/verify/import/export) | Satellites behind gateway `jobs` module (`scheduler_jobs`) |
| `lambda/emailapis/` | Email APIs (Python orchestration) | `EC2/email.server/` (Go target) |
| `lambda/emailapigo/` | Email APIs (Go workers) | `EC2/email.server/` |
| `lambda/logs.api/` | Logs API (Python) | `EC2/log.server/` |
| `lambda/s3storage/` | S3 storage (Python) | `EC2/s3storage.server/` |
| `lambda/mailvetter/` | Mailvetter verifier | `backend(dev)/mailvetter/` (service tree) |
| `backend(dev)/mailvetter/` | Verification engine | `backend(dev)/mailvetter/` (service tree) |
| `backend(dev)/contact.ai/` | Contact AI service | `EC2/ai.server/` (Go target) |
| `backend(dev)/resumeai/` | Resume AI service | `EC2/ai.server/` (Go target) |
| `backend(dev)/salesnavigator/` | Sales Navigator backend | `EC2/extension.server/` (Go target) |
| `extension/contact360/` | Extension logic/transport layer | `contact360.extension/` repo (extension codebase) |

See **`docs/docs/architecture.md`** → *Service register (canonical)* for the full service inventory and status.

**Service status:** see `docs/architecture.md` → *Service register (canonical)*.

## Core runtime contracts

- Client surfaces (`contact360.io/app`, extension) call **Appointment360** (`contact360.io/api`) as the primary contract gateway.
- Appointment360 orchestrates service calls to finder, verifier, search, scheduling, and storage services.
- Async flows run through **`contact360.io/jobs`**, with telemetry routed to `lambda/logs.api` and artifacts to `lambda/s3storage`.
- Search and enrichment behavior rely on **Connectra** (`contact360.io/sync`) (query/filter/index contract).
- `contact360.io/email` consumes backend REST contracts via `NEXT_PUBLIC_BACKEND_URL` and is not GraphQL-only.

## Deep decomposition framework (how to break work)

Use five task tracks for every roadmap stage:

1. **Contract track**: GraphQL/API/event contract definitions and compatibility.
2. **Service track**: Backend implementation per owning service.
3. **Surface track**: Dashboard/extension/docsai UX and action wiring.
4. **Data track**: Storage, lineage, quality, and reconciliation.
5. **Ops track**: Observability, rollback safety, and release validation.

## `s3storage` focused implementation map

- Primary service: `lambda/s3storage/`
- API entrypoints: `app/api/v1/endpoints/uploads.py`, `files.py`, `schema.py`, `avatars.py`, `buckets.py`
- Core backend abstraction: `app/services/storage_service.py` and `app/services/storage_backends.py`
- Metadata worker path: `app/utils/worker.py`, `metadata_job.py`, `update_bucket_metadata.py`
- Deploy contract: `lambda/s3storage/template.yaml`

Immediate engineering queue:

1. Replace in-memory multipart session state with durable shared storage.
2. Remove hardcoded metadata worker function name from endpoint logic.
3. Add concurrency-safe metadata update strategy for `metadata.json`.
4. Add contract parity tests between `docs/API.md` and implemented routes.
5. Add E2E failure-path test coverage (duplicate complete, missing parts, worker failure).

See full era-by-era decomposition: `docs/codebases/s3storage-codebase-analysis.md`.

## `contact360.io/jobs` focused implementation map

- Primary service: `contact360.io/jobs/`
- API entrypoints: `app/api/main.py`, `app/api/v1/routes/jobs.py`
- Workers: `app/workers/scheduler.py`, `consumer.py`, `worker_pool.py`
- Processors: `app/processors/registry.py`, stream processors under `app/processors/`
- Models: `app/models/job_node.py`, `edge.py`, `job_event.py`
- Services/repositories: `app/services/job_service.py`, `app/repositories/`
- Middleware/config: `app/middleware/auth.py`, `rate_limit.py`, `app/core/config.py`

Immediate engineering queue:

1. Add stronger authz model beyond shared `X-API-Key`.
2. Add detection/remediation for DAG degree-decrement deadlocks.
3. Add idempotency keys for create/retry submission paths.
4. Improve stale `processing` recovery guarantees and evidence.
5. Add contract parity tests for endpoints vs docs/module mapping.

Era task-pack index: `docs/backend/apis/JOBS_ERA_TASK_PACKS.md`.

## `backend(dev)/contact.ai` focused implementation map

- Primary service: `backend(dev)/contact.ai/`
- App entrypoint: `app/main.py` (FastAPI + Mangum Lambda adapter)
- API entrypoints: `app/api/v1/endpoints/ai_chats.py` (chat CRUD + send/stream), `app/api/v1/endpoints/ai.py` (email risk, company summary, parse filters)
- Services: `app/services/hf_service.py` (HF inference routing, fallback, streaming), `app/services/ai_chat_service.py` (chat orchestration)
- Repositories: `app/repositories/ai_chat.py` (PostgreSQL `ai_chats` CRUD)
- Models / schemas: `app/models/ai_chat.py`, `app/schemas/ai_chat.py` (Pydantic + `ModelSelection` enum)
- Config / dependencies: `app/core/config.py`, `app/api/dependencies.py` (`api_key_dep`, `db_session_dep`)

Immediate engineering queue:

1. Fix `ModelSelection` enum mapping shim: GraphQL enum values must map to HF model IDs in `LambdaAIClient`.
2. Align `LambdaAIClient` paths to `/api/v1/ai/…` — remove any legacy `/gemini/…` references.
3. Implement strict JSONB `messages` validation in `AIChatService` (max text length, valid sender, max contacts).
4. Add SSE stream error handling + client reconnect for Lambda timeout edge cases.
5. Add optimistic lock (`version` column on `ai_chats`) to prevent concurrent message append races.

Era task-pack index: `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`.

## Small-task template (per stage)

- Task A: Define/adjust contract and acceptance boundaries.
- Task B: Implement service logic and edge-case guards.
- Task C: Wire UI surface behavior and permission checks.
- Task D: Validate data integrity and background processing behavior.
- Task E: Add telemetry, alerts, and release/rollback notes.

## Deep breakdown examples by era

### `1.x` (user, billing, credit)

- Contract: User/credit/billing GraphQL mutations and entitlement checks.
- Service: Auth/session, credit deduction, billing state machine, analytics queries.
- Surface: Dashboard auth flows, credit display, billing UX, notification components.
- Data: Credit ledger consistency, billing payment state, usage logs.
- Ops: Credit balance observability, fraud/abuse controls, payment audit.

### `2.x` (email system)

- Contract: Finder/verifier GraphQL API shape and credit deduction contract.
- Service: Pattern generation (`emailapis`), Go worker path (`emailapigo`), Mailvetter integration, bulk job processors.
- Surface: Email UI components, bulk export flow, results display.
- Data: Finder/verifier result storage, bulk job checkpoint and S3 output.
- Ops: Provider fallback telemetry, bulk job health, credit deduction accuracy.

### `3.x` (contact and company data)

- Contract: VQL filter taxonomy freeze and search schema.
- Service: Connectra VQL translation, dual-write PG+ES, enrichment pipeline, dedup algorithm.
- Surface: Advanced filter UI, company drill-down, saved-search feature.
- Data: Elasticsearch index refresh, enrichment completeness, dedup quality metrics.
- Ops: Search relevance checks, index drift alerts, P95 latency targets.

### `4.x` (extension and Sales Navigator)

- Contract: Extension auth token contract and SN sync payload schema.
- Service: Extension session logic, SN ingestion parser, conflict resolution, telemetry shipping.
- Surface: Extension UI auth flows, ingestion status indicators, sync health display.
- Data: Sync dedup, SN record lineage, error telemetry in `logs.api`.
- Ops: Sync idempotency checks, extension error triage coverage.

### `5.x` (AI workflows)

- Contract: AI chat/utility GraphQL schema; confidence/explanation fields; cost quota policy.
- Service: HF streaming client, Gemini utility paths, quota enforcement, prompt version management.
- Surface: AI response rendering, confidence display, usage cap messaging.
- Data: AI conversation state in PostgreSQL, model usage cost tracking.
- Ops: AI cost per user metrics, prompt regression checks, quota breach telemetry.

### `6.x` (reliability and scaling)

- Contract: SLO definition document; idempotency key contract for billing/bulk/sync writes.
- Service: Retry/DLQ configuration, idempotency middleware, trace ID propagation, abuse guard.
- Surface: Health/SLO endpoint exposure, operational dashboard updates.
- Data: Error budget ledger, SLO attainment time-series, artifact lifecycle logs.
- Ops: SLO attainment dashboards, cost guardrail activation, reliability RC gate.

### `7.x` (deployment)

- Contract: RBAC role matrix, audit event schema, data lifecycle policy definitions.
- Service: Permission-check middleware, audit event emission, tenant isolation, secret rotation.
- Surface: Admin governance UX, role management screens, compliance reporting views.
- Data: Immutable audit log, tenant boundary test evidence, security control attestation.
- Ops: Audit log integrity checks, tenant isolation test coverage, deployment RC gate.

### `8.x` (public and private APIs)

- Contract: API versioning policy; webhook event envelope; analytics event schema.
- Service: Public/private API handlers, webhook delivery/retry, partner auth scopes, analytics ingestion.
- Surface: API documentation, developer portal, analytics dashboard.
- Data: API usage telemetry, delivery observability, analytics quality metrics.
- Ops: API compatibility regression tests, analytics quality checks, partner incident runbooks.

### `9.x` (ecosystem integrations and platform productization)

- Contract: Connector lifecycle schema; tenant/policy/entitlement model.
- Service: Connector SDK, multi-tenant enforcement, entitlement engine, lifecycle automation.
- Surface: Integration setup UX, self-serve admin workspace, support diagnostics.
- Data: SLA reporting, compliance evidence, cost/capacity forecasting metrics.
- Ops: SLA attainment dashboards, compliance overlays, integration health dashboards.

### `10.x` (email campaign)

- Contract: Campaign entity schema; policy gate rules; compliance contract.
- Service: Campaign execution state machine, send metering, deliverability verification, PII lifecycle.
- Surface: Campaign creation UI, audience builder, deliverability dashboard, opt-out management.
- Data: Send metering ledger, bounce/complaint logs, opt-out audit trail.
- Ops: Bounce rate tracking, opt-out audit completeness, feature flag gates, canary rollout.

---

## Mailvetter repository layout (onboarding)

The Mailvetter service root in this workspace is **`backend(dev)/mailvetter/`** (often also published as `lambda/mailvetter/` in other checkouts). Production-oriented Go sources for the verifier often live under **`app/mailvetter-bak/`** (historical folder name: **`-bak`** does *not* mean “unused backup” in all environments — treat it as the packaged app subtree unless a deployment doc says otherwise).

---

## Per-service implementation summaries

High-level entry points for engineers mapping features to code. For API shapes, prefer `contact360.io/api/sql/apis/*.md` and GraphQL module docs under `contact360.io/api/app/graphql/modules/`.

### Dashboard (`contact360.io/app/`)

- **GraphQL:** `src/services/graphql/` — feature modules (`jobsService.ts`, `billingService.ts`, `contactsService.ts`, …) call the shared GraphQL client.
- **Feature gating:** `src/lib/featureAccess.ts` (or adjacent config) coordinates plan/feature flags with UI.
- **Bulk export UX:** `src/hooks/useNewExport.ts` — multipart upload orchestration for CSV → job pipeline; pairs with `src/services/graphql/jobsService.ts` and S3 helpers.
- **Styling:** Modular CSS under `app/css/*` (see app `README.md`).

### DocsAI (`contact360.io/admin/`)

- Django apps under `contact360.io/admin/apps/` — **roadmap** and **architecture** UIs read from `apps/roadmap/constants.py` and `apps/architecture/constants.py` (mirrors of `docs/roadmap.md`, `docs/architecture.md` per `docs/docsai-sync.md`).

### Marketing (`contact360.io/root/`)

- **Env:** `GRAPHQL_URL` for read-only API calls where enabled; `DASHBOARD_URL` (or equivalent) for auth redirects — see marketing `.env.example` and `README.md`.
- **Resilience:** `API_FALLBACKS.md` (if present) documents static fallbacks when API is down.
- **Styling:** Custom CSS, BEM-like naming (not Tailwind).

### Appointment360 (`contact360.io/api/`)

- **GraphQL:** `app/graphql/modules/*` — resolvers and schema composition per domain (jobs, billing, auth, …).
- **HTTP clients:** `app/clients/*` — downstream service wrappers (email, Connectra, jobs, …).
- **Contracts:** `sql/apis/*.md` and module-specific `*_MODULE.md` files document expected payloads and DB boundaries.

### Connectra (`contact360.io/sync/`)

- **Routes:** HTTP handlers grouped for `/contacts`, `/companies`, `/common` (filters, shared utilities).
- **VQL:** Vivek Query Language parsing and translation to Elasticsearch queries — see service README and `common` route group for filter metadata endpoints.
- **Auth:** API-key / internal auth for gateway-to-Connectra calls (align with Appointment360 client config).
- **Two-phase read path:** `VQL -> Elasticsearch IDs -> PostgreSQL hydrate -> in-memory hash join` for full response assembly.
- **Write concurrency model:** Batch upsert fans out in parallel to five stores (PG contacts, ES contacts, PG companies, ES companies, `filters_data`) using goroutines + `WaitGroup`.
- **Search type mapping:** `exact`, `shuffle`, `substring` map to distinct ES query modes and are governed by the VQL taxonomy contract.
- **Job engine:** `OPEN -> IN_QUEUE -> PROCESSING -> COMPLETED/FAILED -> RETRY_IN_QUEUED` with separate first-time and retry runners.
- **Idempotency:** UUID5 derivation on normalized entity keys keeps bulk ingest replay-safe for contacts/companies/filter facets.

### emailapis (`lambda/emailapis/`)

- Python orchestration for finder/verifier pipelines. Shares conceptual contract with **`LambdaEmailClient`** (or equivalent) in the gateway.
- **`emailapis/README.md`** endpoint lists may lag code — verify against OpenAPI/route definitions before integration testing.

### emailapigo (`lambda/emailapigo/`)

- Go workers for high-throughput finder paths. **Swap-the-URL model:** gateway may route heavy finder workloads to Go instead of Python depending on config/environment.

### contact.ai (`backend(dev)/contact.ai/`)

- FastAPI REST + optional Lambda packaging. Gateway forwards **`X-User-ID`** (or equivalent) for tenancy.
- **Data:** Shared PostgreSQL patterns for `ai_chats` / conversation state — see module docs under the service.

### logs.api (`lambda/logs.api/`)

- Ingests structured logs; optional-disable pattern in gateway (**`LambdaLogsClient`**) so dev/test can silence shipping logs.
- **Boundary:** analytics aggregates vs raw log storage — align field names (`user_id`, `request_id`) with usage/analytics roadmap stages.

### Mailvetter (`backend(dev)/mailvetter/`)

- **`app/mailvetter-bak/`** — primary packaged verifier sources (see onboarding note above).
- **API:** `/v1/emails/validate` and bulk validation routes; routing may fan out to Truelist/IcyPeas or other providers per configuration.

### s3storage (`lambda/s3storage/`)

- **`StorageBackend`** protocol / implementation split for S3 operations.
- **Model:** Logical `bucket_id` / tenant-facing bucket abstraction — see service README.
- **Multipart:** `multipart_upload_guide.md` (or equivalent) documents initiate → presign → part → complete.

### salesnavigator (`backend(dev)/salesnavigator/`)

- **Runtime:** FastAPI on AWS Lambda via Mangum; SAM deployment (`template.yaml`; 60s timeout, 1024 MB).
- **REST:** `GET /`, `GET /v1/health`, `POST /v1/scrape` (HTML parse + optional save), `POST /v1/save-profiles` (profile array → Connectra bulk upsert).
- **GraphQL:** `salesNavigator` operations proxied via Appointment360 for dashboard flows.
- **No local DB:** All persistence via Connectra (`/contacts/bulk`, `/companies/bulk`). Deterministic UUID5 strategy for idempotent upserts.
- **Core services:** `SaveService` (dedup by `profile_url`, completeness scoring, chunking 500/chunk, parallel async save), `mappers.py` (SN → Connectra field mapping), `extraction.py` (BeautifulSoup HTML parsing).
- **Auth:** `X-API-Key` (global service-to-service key; per-tenant scoping planned for `7.x`).
- **Known gaps:** `scrape-html-with-fetch` documented but not implemented; no rate limiting; wide-open CORS; no `X-Request-ID` correlation header.
- **Deep reference:** `docs/codebases/salesnavigator-codebase-analysis.md`.
- **Era task packs:** `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`.

### Async jobs (email.server + sync.server)

- **Gateway:** `contact360.io/api` GraphQL **jobs** module + `scheduler_jobs` table; clients `EmailServerJobsClient`, `ConnectraClient`.
- **Satellites:** `EC2/email.server` (S3 bulk finder/verifier, pause/resume), `EC2/sync.server` (CSV import/export queue).
- **Legacy:** Standalone Python `contact360.io/jobs` / `EC2/job.server` removed from monorepo — see `docs/codebases/jobs-codebase-analysis.md` archive note.

### resumeai (`backend(dev)/resumeai/`)

- Resume-focused AI features when this checkout is present; align gateway routes and env with service README.

### Extension (canonical path)

- Code lives under **`extension/contact360/`** when checked out; not all clones include this tree. Chrome Web Store / build pipelines may use a separate repo mirror — align with `docs/architecture.md` service register. Do not use the historical typo `extention/` or the shorthand `extension/contact360/` for new work.

---

## Admin surface split (Dashboard vs DocsAI)

- **Dashboard `/admin`:** In-product admin/statistics route (`contact360.io/app/app/(dashboard)/admin/page.tsx`). Use for authenticated operators who already use the product shell.
- **DocsAI:** Django mirror of roadmap/architecture constants and internal docs workflows (`contact360.io/admin/`). Use for documentation governance and internal control-plane UX — not a substitute for gateway authorization on privileged mutations.
- **Future wiring:** Admin credit adjustments and audit views should go through **Appointment360** resolvers and **`lambda/logs.api`** for structured audit trails; avoid duplicating privileged actions across surfaces without an explicit security review. Track Stage 1.13 in **`docs/roadmap.md`** and **`docs/versions.md`**.


### 8.x-10.x backend pointers
- webhooks module
- integrations module
- campaigns/sequences/templates modules

## Five-track execution pack (documentation standard)

For each era and minor release, docs must explicitly include:

- Contract track updates (API and schema)
- Service track updates (backend runtime changes)
- Surface track updates (UI routes, tabs, components)
- Data track updates (DB/index/storage lineage)
- Ops track updates (runbooks, release gates, evidence)

## `logs.api` focused implementation map

- Primary service: `lambda/logs.api/`
- API entrypoints: `app/api/v1/endpoints/logs.py`, `health.py`
- Service/repository path: `app/services/log_service.py`, `app/models/log_repository.py`
- Storage client: `app/clients/s3.py`
- Cache/monitoring utilities: `app/utils/query_cache.py`, `query_monitor.py`, `cache_metrics.py`
- Deploy contract: `lambda/logs.api/template.yaml`

Immediate engineering queue:

1. Correct MongoDB references in logs.api docs and contracts to S3 CSV reality.
2. Replace static shared API key pattern with rotated secret strategy and per-service identities.
3. Add scalability guardrails for wide time-range queries and costly scans.
4. Strengthen retention/audit evidence generation for compliance flows.
5. Add contract parity tests between documented endpoints and runtime routes.

## `emailapis` / `emailapigo` focused implementation map

- Primary services: `lambda/emailapis/`, `lambda/emailapigo/`
- API routes: `app/api/v1/router.py`, `internal/api/router.go`
- Finder core: `app/services/email_finder_service.py`, `internal/services/email_finder_service.go`
- Verifier core: `app/services/email_verification_service.py`, `internal/services/email_verification_service.go`
- Pattern services/repositories: `app/services/email_pattern_service.py`, `internal/services/email_pattern_service.go`, corresponding repositories
- Data models: `app/models/email_finder_cache.py`, `app/models/email_patterns.py`, Go equivalents under `internal/models/`

Immediate engineering queue:

1. Unify provider naming and contract (`truelist` vs `mailvetter`) across frontend, GraphQL, and both runtimes.
2. Freeze status semantics and mapping tables across all layers.
3. Add contract parity tests for endpoint payloads and error envelopes.
4. Harden bulk failure-path mapping and retry/idempotency behavior.
5. Add end-to-end observability contract (trace/request IDs across app -> api -> jobs -> lambda).

See full era-by-era decomposition: `docs/codebases/emailapis-codebase-analysis.md`.

## `backend(dev)/email campaign` focused implementation map

`email campaign` is the Go campaign delivery service introduced in `10.x`. It runs as two separate binaries: API server (`cmd/main.go`) and Asynq worker (`cmd/worker/main.go`).

- **API server entrypoints:** `cmd/main.go` → registers Gin router, DB/Redis/S3 init, mounts all API routes.
- **Handlers:** `api/handlers.go` — campaign create, unsubscribe, IMAP endpoints; `template/handlers.go` — template CRUD + preview.
- **Worker entrypoint:** `cmd/worker/main.go` → registers `HandleCampaignTask` with Asynq server (5 workers).
- **Campaign worker:** `worker/campaign_worker.go` — loads CSV/audience, creates recipients, dispatches to `EmailWorker` goroutines.
- **Email worker:** `worker/email_worker.go` — fetches template from S3, renders with Go `html/template`, checks suppression, sends via `net/smtp`.
- **Template service:** `template/service.go` — S3 `PutObject`/`GetObject` with in-memory `sync.RWMutex` cache.
- **Database layer:** `db/db.go` (sqlx init), `db/queries.go` (campaign/recipient/suppression queries), `db/template_queries.go` (template CRUD).
- **Tasks:** `tasks/campaign.go` — Asynq task type `TypeCampaign`, `CampaignPayload` struct.
- **JWT utils:** `utils/token.go` — `GenerateUnsubToken`, `ParseUnsubToken` using HS256.
- **Schema:** `db/schema.sql` — defines `campaigns`, `recipients`, `suppression_list` tables (⚠ missing `templates` table and `recipients.unsub_token`).

Immediate engineering queue:

1. Fix `db/schema.sql` — add `templates` table DDL and `recipients.unsub_token TEXT` column.
2. Fix `GetUnsubToken` in `db/queries.go` — replace `DB.Exec` with `DB.Get` to return token value.
3. Add SMTP auth: read `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` env vars; pass `smtp.PlainAuth` to `smtp.SendMail`.
4. Add authentication middleware on `/campaign`, `/templates`, and `/unsub` (admin) routes.
5. Replace CSV filepath audience with Connectra REST query for recipient resolution (`3.x` integration).
6. Add `completed_with_errors` campaign status for partial failures.

See full era-by-era decomposition: `docs/codebases/emailcampaign-codebase-analysis.md`.

Era task-pack index: era folders `0–10` each contain `emailcampaign-*-task-pack.md`.

## `contact360.io/api` (Appointment360) focused implementation map

Appointment360 is the GraphQL-only gateway. Single `/graphql` endpoint. 28 module namespaces. No REST feature routes.

- **App entrypoint:** `app/main.py` — FastAPI app factory, middleware registration (8 layers), exception handlers, health routes, Mangum Lambda handler, GraphQL router mount.
- **Settings:** `app/core/config.py` — Pydantic `BaseSettings` with 50+ env vars across categories: GraphQL guards, DB pool, security, downstream clients, idempotency, abuse guard, SLO.
- **Middleware:** `app/core/middleware.py` — all 8 custom Starlette middleware classes: `REDMetricsMiddleware`, `GraphQLBodySizeMiddleware`, `GraphQLIdempotencyMiddleware`, `GraphQLMutationAbuseGuardMiddleware`, `GraphQLRateLimitMiddleware`, `RequestIdMiddleware`, `TraceIdMiddleware`, `TimingMiddleware`.
- **Schema:** `app/graphql/schema.py` — flat composition: `Query` + `Mutation` assembled from 28 module class imports.
- **Context:** `app/graphql/context.py` — per-request `Context` with `db` (AsyncSession), `user` (JWT decode), `user_uuid`, `dataloaders`.
- **Extensions:** `app/graphql/extensions.py` — `QueryComplexityExtension` (limit 100) + `QueryTimeoutExtension` (30s).
- **Downstream clients:** `app/clients/connectra_client.py`, `email_server_client.py`, `lambda_email_client.py`, `lambda_ai_client.py`, `resume_ai_client.py`, `lambda_s3storage_client.py`, `lambda_logs_client.py`, `docsai_client.py`.
- **Module resolvers:** `app/graphql/modules/*/queries.py` and `app/graphql/modules/*/mutations.py` — one folder per GraphQL module (auth, users, contacts, companies, email, jobs, billing, usage, aiChats, resume, salesNavigator, admin, savedSearches, profile, twoFactor, notifications, analytics, pages, s3, upload, featureOverview, etc.).
- **Services:** `app/services/` — billing, credit, activity, notification, analytics, pages business logic.
- **Repositories:** `app/repositories/` — user, profile, saved_search, scheduler_job, token_blacklist data access.
- **DB session:** `app/db/session.py` — async engine, pool monitoring event listeners, `get_db()` FastAPI dependency.
- **Utilities:** `app/utils/vql_converter.py` (VQLQueryInput → Connectra REST), `app/utils/connectra_mappers.py` (response type mapping).

Immediate engineering queue:

1. Remove all inline debug file writes (`_debug_log`, `debug.log` writes) from `email/queries.py` and `jobs/mutations.py`.
2. Add `campaigns`, `sequences`, `campaignTemplates` GraphQL modules (10.x).
3. Enable `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` in production environment configuration.
4. Restore or link SQL schema source (`sql/tables/` files referenced by README but missing locally).
5. ~~Move idempotency to Redis~~ — **done:** PostgreSQL (`graphql_idempotency_replays`); extend abuse guard with Postgres-backed counters when multi-replica enforcement is required.
6. Add `DOCSAI_ENABLED` health check — pages module health should surface DocsAI dependency status.
7. Write contract parity tests for each GraphQL module against `docs/backend/apis/*.md`.

See full era-by-era decomposition: `docs/codebases/appointment360-codebase-analysis.md`.

Era task-pack index: era folders `0–10` each contain `appointment360-*-task-pack.md`.

## `contact360.io/root` implementation notes (marketing app)

- Stack/shape: Next.js App Router + React + TypeScript, custom BEM-like CSS and 3D UI component system.
- Core UX pattern: `app/(marketing)/layout.tsx` applies `useForceLightTheme` and wraps all marketing pages with common navbar/footer.
- API contract path: GraphQL requests through `src/lib/graphqlClient.ts` with auth-aware error handling/retry behavior.
- Component highlights: 3D primitives (`Button3D`, `Input3D`, `Checkbox3D`, `Modal3D`, `Tabs3D`, `Table3D`) plus selector/tooltip/card families.

## `contact360.io/admin` implementation notes (DocsAI app)

- Stack/shape: Django templates + static CSS/JS component system.
- Navigation and shell: `apps/core/navigation.py` (`SIDEBAR_MENU`) + `templates/base.html`.
- Backend integration path: Python GraphQL client (`apps/core/services/graphql_client.py`) with retries/backoff and domain clients in `apps/core/clients/` and `apps/admin/services/`.
- Graph and flow UI: D3 (`relationship-graph-viewer.js`) and Cytoscape (`graph.js`) based relationship visualizations.
- Data coupling: local Django persistence plus Appointment360 GraphQL, optional Redis cache (only if `USE_REDIS_CACHE=True`), and S3 index artifacts.

---

## Extension implementation notes — `extension/contact360`

### Tech

- **Language:** JavaScript ES6+ (no transpile step)
- **Chrome API:** MV3 — `chrome.storage.local` for token persistence
- **Auth backend:** Appointment360 GraphQL (`POST /graphql` — `auth.refreshToken` mutation)
- **Data backend:** Lambda SN API (`POST /v1/save-profiles`) → Connectra bulk endpoints

### Key implementation patterns

#### `auth/graphqlSession.js` — JWT lifecycle
- Pure base64url decode for JWT payload (no library dependency)
- Proactive refresh with 300-second buffer; avoids mid-scrape token expiry
- All storage calls Promise-wrapped for async/await compatibility in MV3 service workers

#### `utils/lambdaClient.js` — REST transport
- Chunked batching: profiles split into arrays of `BATCH_SIZE` (default 10) before each fetch call
- Retry strategy: exponential back-off with jitter (`attempt => baseDelay * 2^attempt + Math.random() * jitter`)
- Adaptive timeout: increases per retry to handle Lambda cold-start latency
- Payload pruning: removes `null`/`undefined` fields to reduce payload size

#### `utils/profileMerger.js` — dedup and merge
- Dedup key: `profile_url` (LinkedIn/SN canonical URL)
- Completeness score: `filledFields / totalFields` — checked fields: name, title, company, email, phone, location, connections
- Merge strategy: per-field winner is the value from the higher-scoring record; ties resolved by preferring the `deepScrape` variant over `HTML`

### Era tagging

| Module | Primary era |
| --- | --- |
| `auth/graphqlSession.js` | 1.x (token lifecycle), 4.x (proactive refresh) |
| `utils/lambdaClient.js` | 3.x (save flow), 4.x (reliability), 6.x (retry/back-off) |
| `utils/profileMerger.js` | 3.x (contact data quality), 4.x (SN maturity) |
---

## Email app implementation notes — `contact360.io/email`

- **Framework:** Next.js 16 App Router + React 19.
- **UI primitives:** `src/components/ui/*` (Button, Input, Tabs, Checkbox, Table, Alert, Badge, Tooltip, Drawer, Select).
- **Table architecture:** `@tanstack/react-table` with row selection, pagination, and tab filtering.
- **Contexts/hooks:** `ImapProvider` (`activeAccount`, `isLoading`) + `useIsMobile`.
- **Routing:** mailbox routes (`/inbox`, `/sent`, `/spam`, `/draft`), detail route (`/email/[mailId]`), auth routes, account settings route.
- **Security helper:** DOMPurify sanitization in email detail rendering.
- **Known hardening gap:** IMAP credentials currently moved through custom headers and localStorage account blob.

## `backend(dev)/mailvetter` focused implementation map

- Primary service: `backend(dev)/mailvetter/app/mailvetter-bak/`
- API bootstrap: `cmd/api/main.go`, `internal/api/router.go`
- Worker bootstrap: `cmd/worker/main.go`, `internal/worker/runner.go`
- Handlers: `internal/handlers/validate.go`, `jobs.go`, `health.go`
- Validation core: `internal/validator/logic.go`, `internal/validator/scoring.go`
- Protocol lookups: `internal/lookup/dns.go`, `smtp.go`, `security.go`
- Data layer: `internal/store/db.go` (`jobs`, `results`, indexes)
- Queue layer: `internal/queue/client.go` (`tasks:verify`)
- Webhook lifecycle: `internal/webhook/dispatcher.go`
- Legacy operator UI: `static/index.html`

Immediate engineering queue:

1. Canonicalize `/v1` routes and deprecate legacy `/verify|/upload|/status|/results`.
2. Replace in-memory limiter with Redis-backed distributed limiter.
3. Add idempotency key support for bulk job creation.
4. Add explicit `processing` and `failed` job statuses plus retry/DLQ flow.
5. Split DB migration execution from runtime startup.
6. Separate `WEBHOOK_SECRET_KEY` from `API_SECRET_KEY` with strict policy.
7. Add endpoint contract parity tests for all `/v1` routes.

See full era-by-era decomposition: `docs/codebases/mailvetter-codebase-analysis.md`.

Era task-pack index: era folders `0–10` each contain `mailvetter-*-task-pack.md`.

## 2026 Documentation Overhaul Addendum

### Added explicit service ownership notes

- `contact360.io/admin`: Django operator/control plane with RBAC middleware, billing ops, logs/jobs/storage consoles, and cross-service admin clients.
- `lambda/s3storage`: object lifecycle + CSV analysis + multipart upload orchestration. Current reliability/auth gaps are roadmap blockers.
- `lambda/logs.api`: S3 CSV log persistence and query/statistics API. MongoDB references are legacy and removed from canonical interpretation.

### Dependency and risk matrix updates

- `backend(dev)/email campaign` depends on Redis + PostgreSQL + SMTP + S3 templates; schema parity and unsubscribe query path remain P0 blockers.
- `lambda/emailapigo` and `lambda/emailapis` share provider-network responsibilities and must keep status vocabulary + cache contracts aligned.
- `contact360.io/admin` integrates with `appointment360` (GraphQL), `logs.api`, and `s3storage` (job visibility via gateway); missing API-key forwarding in some client calls is tracked.


## Attached Analysis & Task Packs
- [Appointment360 Foundation Task Pack](../../contact360.io/root/docs/imported/analysis/appointment360-foundation-task-pack.md)
- [Appointment360 User Billing Task Pack](../../contact360.io/root/docs/imported/analysis/appointment360-user-billing-task-pack.md)
- [Connectra Foundation Task Pack](../../contact360.io/root/docs/imported/analysis/connectra-foundation-task-pack.md)
- [Contact AI Foundation Task Pack](../../contact360.io/root/docs/imported/analysis/contact-ai-foundation-task-pack.md)
- [Contact360 E2E Architecture Flow](../../contact360.io/root/docs/imported/analysis/Contact360 End-to-End Architecture and Flow.md)
- [Email APIs Foundation Task Pack](../../contact360.io/root/docs/imported/analysis/emailapis-foundation-task-pack.md)
- [Sync Codebase Analysis](../codebases/sync-codebase-analysis.md)
