# Codebase analysis content retrieval
_Exported on 3/26/2026 at 17:08:02 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their FULL content. Report each file's path header then content.

1. d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md
2. d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md
3. d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md

Focus especially on the era 8.x section and "Known gaps and risks" / "Immediate engineering queue" sections of each file.

---

**Cursor**


Reading all three files in full.




Below is the **full text** of each file (path as header). A short **8.x / gaps / queue** digest is at the end.

---

## `d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md`

```markdown
# Appointment360 Codebase Analysis (`contact360.io/api`)

## Purpose and role

`contact360.io/api` (Appointment360) is Contact360's **primary GraphQL gateway and orchestrator**. It is the only entry point through which the dashboard (`contact360.io/app`) and extension reach all backend capability. It translates GraphQL operations into downstream REST calls to Connectra, tkdjob, lambda email, S3 storage, DocsAI, contact.ai, and logs.api. All user authentication, credit deduction, activity logging, usage tracking, and entitlement enforcement pass through this service.

---

## Technology stack

| Concern | Technology |
| --- | --- |
| HTTP server | FastAPI (Python 3.11+) with Mangum for AWS Lambda adaptation |
| GraphQL runtime | Strawberry (code-first, type-safe, async) |
| Database ORM | Async SQLAlchemy (`create_async_engine`, `AsyncSession`) |
| DB driver | asyncpg (PostgreSQL) |
| Auth | HS256 JWT — access + refresh tokens, token blacklist in DB |
| Background tasks | FastAPI `BackgroundTasks` |
| Caching | Optional Redis (`REDIS_URL`), TTLCache for user objects |
| Config | Pydantic `BaseSettings` with `.env` + env vars |
| Middleware | Custom Starlette middleware stack (8 layers) |
| Deploy targets | EC2 (uvicorn), AWS Lambda (Mangum), Docker |
| Query routing | `app/clients/` — ConnectraClient, TkdjobClient, LambdaEmailClient, LambdaAIClient, etc. |

---

## Architecture patterns

### GraphQL-only design

Single endpoint `/graphql` (plus health probes). No REST feature routes. The schema (`schema.py`) is composed as a flat `Query` + `Mutation` root with 28 nested module namespaces:

```
query { auth | users | contacts | companies | email | jobs | usage | billing | analytics | activities | health | pages | s3 | upload | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume | featureOverview }
mutation { auth | users | contacts | companies | billing | linkedin | jobs | email | usage | upload | s3 | analytics | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume }
```

### Request lifecycle

```
Request → CORS → TrustedHost → ExceptionGroupMiddleware → DatabaseCommitMiddleware → 
  GraphQLIdempotencyMiddleware → GraphQLMutationAbuseGuardMiddleware → 
  GraphQLRateLimitMiddleware → RequestIdMiddleware → TraceIdMiddleware → 
  TimingMiddleware → REDMetricsMiddleware → GZip → GraphQLBodySizeMiddleware → 
  GraphQLRouter → get_context(JWT decode → User fetch) → Resolver execution
```

### Context (`app/graphql/context.py`)

Per-request `Context` carries:
- `db`: `AsyncSession` (from async generator, committed by `DatabaseCommitMiddleware`)
- `user`: `User | None` extracted from Bearer JWT
- `user_uuid`: `str | None`
- `dataloaders`: `DataLoaders` (per-request N+1 prevention)

### External service clients (`app/clients/`)

| Client | Calls | Auth |
| --- | --- | --- |
| `ConnectraClient` | Connectra REST (VQL queries, batch upsert, jobs, filters) | `X-API-Key` header |
| `TkdjobClient` | TKD Job scheduler REST (create/list/status/retry jobs) | `X-API-Key` header |
| `LambdaEmailClient` | Lambda Email API (finder, verifier, bulk, patterns) | API key |
| `LambdaAIClient` | Contact AI REST (chats, Gemini) | API key |
| `LambdaS3StorageClient` | S3 Storage API (list, preview, download) | API key |
| `LambdaLogsClient` | Logs API (write, query, stats) | API key |
| `DocsAIClient` | DocsAI Django (page management, docs content) | API key |
| `ResumeAIClient` | Resume AI microservice | API key |

---

## Module catalog

### Query modules

| Module | Class | Key operations |
| --- | --- | --- |
| auth | `AuthQuery` | `me` |
| users | `UserQuery` | `user(uuid)`, `users()`, `userStats()` |
| contacts | `ContactQuery` | `contact(uuid)`, `contacts(query)`, `contactCount(query)`, `contactQuery(query)`, `filters()`, `filterData(input)` |
| companies | `CompanyQuery` | `company(uuid)`, `companies(query)`, `companyCount(query)`, `companyQuery(query)`, `companyContacts(company_uuid)`, `filters()`, `filterData(input)` |
| email | `EmailQuery` | `findEmails`, `findEmailsBulk`, `verifySingleEmail`, `verifyEmailsBulk`, `createEmailFinderExportJob`, `createEmailVerifyExportJob`, `createEmailPatternImportJob` |
| jobs | `JobQuery` | `job(jobId)`, `jobs(limit,offset,status,jobType)` |
| usage | `UsageQuery` | `usage(feature)` |
| featureOverview | `FeatureOverviewQuery` | `featureOverview()` |
| billing | `BillingQuery` | `billingInfo`, `plans`, `invoices` |
| activities | `ActivityQuery` | `activities(limit,offset,type)` |
| analytics | `AnalyticsQuery` | `analytics(...)` |
| health | `HealthQuery` | `health()` |
| pages | `PagesQuery` | `page(id)`, `pages(type)` |
| s3 | `S3Query` | `files(bucket,prefix)`, `fileContent(key)` |
| upload | `UploadQuery` | `uploadStatus(sessionId)` |
| aiChats | `AIChatQuery` | `aiChat(uuid)`, `aiChats()` |
| notifications | `NotificationQuery` | `notifications()` |
| salesNavigator | `SalesNavigatorQuery` | `salesNavigatorSearch()` |
| admin | `AdminQuery` | `adminStats()`, `paymentSubmissions()`, `users()` |
| savedSearches | `SavedSearchQuery` | `savedSearch(id)`, `savedSearches(type)` |
| twoFactor | `TwoFactorQuery` | `twoFactorStatus()` |
| profile | `ProfileQuery` | `apiKeys()`, `sessions()` |
| resume | `ResumeQuery` | `resumes()`, `resume(id)` |

### Mutation modules

| Module | Class | Key operations |
| --- | --- | --- |
| auth | `AuthMutation` | `login`, `register`, `logout`, `refresh_token` |
| users | `UserMutation` | `updateUser`, `deleteUser`, `promoteUser` |
| contacts | `ContactMutation` | `createContact`, `batchCreateContacts`, `updateContact`, `deleteContact`, `exportContacts`, `batchUpsertContacts`, `upsertByLinkedinUrl`, `searchLinkedin`, `syncIntegration`, `saveLinkedinSearchResults` |
| companies | `CompanyMutation` | `createCompany`, `batchCreateCompanies`, `updateCompany`, `deleteCompany`, `exportCompanies` |
| billing | `BillingMutation` | `subscribe`, `purchaseAddon`, `submitPaymentProof`, `approvePayment`, `declinePayment` |
| linkedin | `LinkedInMutation` | `upsertByLinkedinUrl`, `searchLinkedin`, `exportLinkedinResults` |
| jobs | `JobMutation` | `createEmailFinderExport`, `createEmailVerifyExport`, `createEmailPatternImport`, `createContact360Export`, `createContact360Import`, `createAppointmentImport`, `retryJob` |
| email | `EmailMutation` | `addEmailPattern`, `addEmailPatternBulk` |
| usage | `UsageMutation` | `trackUsage`, `resetUsage` |
| upload | `UploadMutation` | `startMultipartUpload`, `uploadPart`, `completeMultipartUpload`, `abortMultipartUpload` |
| s3 | `S3Mutation` | `startCsvMultipartUpload`, `uploadCsvPart`, `completeCsvUpload` |
| analytics | `AnalyticsMutation` | `trackEvent` |
| aiChats | `AIChatMutation` | `createAiChat`, `sendAiMessage`, `deleteAiChat`, `generateCompanySummary`, `analyzeEmailRisk`, `parseContactFilters` |
| notifications | `NotificationMutation` | `markNotificationRead`, `markAllRead` |
| salesNavigator | `SalesNavigatorMutation` | `saveSalesNavigatorProfiles`, `syncSalesNavigator` |
| admin | `AdminMutation` | `creditUser`, `adjustCredits`, `approvePayment`, `declinePayment` |
| savedSearches | `SavedSearchMutation` | `createSavedSearch`, `updateSavedSearch`, `deleteSavedSearch` |
| twoFactor | `TwoFactorMutation` | `enableTwoFactor`, `verifyTwoFactor`, `disableTwoFactor` |
| profile | `ProfileMutation` | `createApiKey`, `deleteApiKey`, `updateProfile` |
| resume | `ResumeMutation` | `createResume`, `updateResume`, `deleteResume` |

---

## Middleware stack (all 8 layers)

| Layer | Class | Purpose |
| --- | --- | --- |
| 1 | `GZipMiddleware` | Response compression (optional, `ENABLE_RESPONSE_COMPRESSION`) |
| 2 | `REDMetricsMiddleware` | Rate/error/duration aggregate metrics → `/health/slo` |
| 3 | `TimingMiddleware` | `X-Process-Time` and `X-Response-Time` response headers |
| 4 | `RequestIdMiddleware` | Echo `X-Request-Id` header from request to response |
| 5 | `TraceIdMiddleware` | Attach/propagate `X-Trace-Id` for cross-service correlation |
| 6 | `GraphQLBodySizeMiddleware` | Reject POST bodies > `GRAPHQL_MAX_BODY_BYTES` (default 2MB) |
| 7 | `GraphQLIdempotencyMiddleware` | Cache and replay `X-Idempotency-Key` mutations (billing/payment guards) |
| 8 | `GraphQLMutationAbuseGuardMiddleware` | Sliding-window per-actor rate guard on high-risk mutations |
| 9 | `GraphQLRateLimitMiddleware` | Per-IP rate limit on `/graphql` (disabled by default in dev) |
| 10 | `DatabaseCommitMiddleware` | Ensure DB generator completes and commits after each GraphQL request |

---

## GraphQL extensions

| Extension | Class | Purpose |
| --- | --- | --- |
| Complexity | `QueryComplexityExtension` | Reject queries exceeding `GRAPHQL_COMPLEXITY_LIMIT` (default 100) |
| Timeout | `QueryTimeoutExtension` | Kill queries exceeding `GRAPHQL_QUERY_TIMEOUT` (default 30s) |

---

## Configuration (`app/core/config.py`)

Critical environment variables by category:

| Category | Key variables |
| --- | --- |
| Gateway identity | `PROJECT_NAME`, `VERSION`, `ENVIRONMENT`, `DEBUG` |
| GraphQL | `GRAPHQL_COMPLEXITY_LIMIT`, `GRAPHQL_QUERY_TIMEOUT`, `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE`, `GRAPHQL_MAX_BODY_BYTES` |
| DB | `POSTGRES_USER/PASS/HOST/PORT/DB`, `DATABASE_POOL_SIZE` (25), `DATABASE_MAX_OVERFLOW` (50) |
| Connectra | `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY`, `CONNECTRA_TIMEOUT` |
| tkdjob | `TKDJOB_API_URL`, `TKDJOB_API_KEY`, `TKDJOB_API_TIMEOUT` |
| Lambda email | `LAMBDA_EMAIL_API_URL`, `LAMBDA_EMAIL_API_KEY` |
| Lambda AI | `LAMBDA_AI_API_URL`, `LAMBDA_AI_API_KEY` |
| S3 storage | `LAMBDA_S3STORAGE_API_URL`, `LAMBDA_S3STORAGE_API_KEY` |
| Logs | `LAMBDA_LOGS_API_URL`, `LAMBDA_LOGS_API_KEY` |
| DocsAI | `DOCSAI_API_URL`, `DOCSAI_API_KEY`, `DOCSAI_ENABLED` |
| Resume AI | `RESUME_AI_BASE_URL`, `RESUME_AI_API_KEY` |
| Security | `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` (30), `REFRESH_TOKEN_EXPIRE_DAYS` (7) |
| Idempotency | `IDEMPOTENCY_REQUIRED_MUTATIONS`, `IDEMPOTENCY_TTL_SECONDS` (86400) |
| Abuse guard | `ABUSE_GUARDED_MUTATIONS`, `MUTATION_ABUSE_GUARD_RPM` (30) |
| SLO | `SLO_ERROR_BUDGET_PERCENT` (1.0%) |
| Caching | `REDIS_URL`, `ENABLE_REDIS_CACHE`, `ENABLE_USER_CACHE`, `USER_CACHE_TTL` |

---

## Strengths

- Production-grade middleware stack (idempotency, abuse guard, RED metrics, trace propagation).
- Fully async end-to-end (FastAPI + asyncpg + httpx clients).
- Per-request DB session lifecycle with commit/rollback discipline.
- DataLoaders for N+1 prevention across related entity queries.
- JWT context with TTL user cache option for high-traffic deployments.
- Query complexity + timeout extensions as gatekeeping for GraphQL abuse.
- Lambda-compatible via Mangum with graceful lifecycle handling.
- Multi-environment (EC2, Lambda, Docker) with single codebase.

---

## Gaps and risks

| Risk | Severity | Notes |
| --- | --- | --- |
| Ad-hoc debug file writes in prod code | High | `email/queries.py` and `jobs/mutations.py` write to local files; must be removed before release |
| `DOCSAI_ENABLED=False` by default | Medium | Pages functionality depends on external DocsAI service; missing health check |
| Rate limiting disabled by default | Medium | `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE=0` means rate limiting is off in dev/prod unless explicitly configured |
| SQL schema not in this checkout | Medium | `sql/tables/` path referenced by README and docs but missing from workspace |
| No campaigns GraphQL module yet | Medium | `10.x` campaign surface requires new `campaigns/sequences/templates` GraphQL modules |
| Abuse guard relies on in-memory state | Low | Does not share state across replicas; use Redis for distributed environments |
| Token blacklist is DB-only | Low | Redis-backed blacklist needed for horizontal scale scenarios |
| Inline debug log files from agent | Medium | `d:\code\ayan\contact\.cursor\debug.log` writes — remove from production branch |

---

## Era mapping (`0.x`–`10.x`)

| Era | Appointment360 concern |
| --- | --- |
| `0.x` | Service bootstrap, middleware baseline, context/session lifecycle, schema layout |
| `1.x` | Auth mutations (login/register/refresh/logout), credit deduction, billing module, usage tracking |
| `2.x` | Email module (finder/verifier), jobs orchestration module, activity logging |
| `3.x` | Contacts/companies modules, VQL conversion, Connectra integration |
| `4.x` | LinkedIn/SalesNavigator modules, extension session and sync mutations |
| `5.x` | AI chats module, resume module, Gemini AI integration |
| `6.x` | Complexity/timeout extensions, idempotency, abuse guard, rate limiting, RED/SLO |
| `7.x` | RBAC (admin/SuperAdmin guards), audit log emissions, deployment security |
| `8.x` | Pages module, saved searches, profile/API keys, public API surface |
| `9.x` | Tenant model, entitlement enforcement, connector governance, notifications |
| `10.x` | Campaigns/sequences/templates modules, campaign wizard orchestration |

---

## Immediate execution queue

1. Remove all inline debug file writes (`_debug_log`, `debug.log` writes) from production modules.
2. Add `campaigns`, `sequences`, `campaignTemplates` GraphQL modules in schema.
3. Enable `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` in production environment.
4. Restore SQL schema docs or link to shared schema source.
5. Add Redis-backed distributed state for idempotency/abuse guard in multi-replica deployments.
6. Wire `DOCSAI_ENABLED` health check — pages `/health` should surface DocsAI dependency.
7. Write contract parity tests for each module against `docs/backend/apis/*.md`.

---

## File map

| Path | Role |
| --- | --- |
| `app/main.py` | FastAPI app, middleware registration, health endpoints, Mangum Lambda handler |
| `app/core/config.py` | `Settings` Pydantic model, all env var definitions |
| `app/core/middleware.py` | All 10 custom middleware classes |
| `app/core/security.py` | JWT encode/decode, `require_auth()` |
| `app/graphql/schema.py` | Root `Query` + `Mutation` composition |
| `app/graphql/context.py` | Per-request `Context` with JWT extraction |
| `app/graphql/dataloaders.py` | `DataLoaders` for N+1 batching |
| `app/graphql/extensions.py` | `QueryComplexityExtension`, `QueryTimeoutExtension` |
| `app/graphql/errors.py` | Error classes and `handle_graphql_error` |
| `app/graphql/modules/*/queries.py` | Per-module query resolvers |
| `app/graphql/modules/*/mutations.py` | Per-module mutation resolvers |
| `app/clients/connectra_client.py` | Connectra REST client |
| `app/clients/tkdjob_client.py` | tkdjob scheduler client |
| `app/db/session.py` | Engine, session factory, pool monitoring |
| `app/services/` | Business logic: billing, usage, credit, activity, pages, notification |
| `app/repositories/` | Data access: user, profile, scheduler_job, token_blacklist, saved_search |
| `app/utils/vql_converter.py` | GraphQL VQLQueryInput → Connectra VQL format |
| `app/utils/connectra_mappers.py` | Response mapping: Connectra → GraphQL types |
```

---

## `d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md`

```markdown
# Connectra Codebase Analysis (`contact360.io/sync`)

## Purpose and role

Connectra is Contact360's search and data-intelligence core for `3.x` contact/company workflows and downstream eras (`4.x`-`10.x`). It provides VQL-powered read APIs, deterministic idempotent upserts, filter metadata hydration, and batch job processing for CSV-based import/export.

## Current architecture snapshot

- **Runtime:** Go 1.24+, Gin HTTP server, Cobra CLI entrypoint.
- **Data plane:** PostgreSQL (`contacts`, `companies`, `jobs`, `filters`, `filters_data`) + Elasticsearch (`contacts_index`, `companies_index`).
- **Read model:** Two-phase query (`VQL -> ES IDs -> PG hydrate -> in-memory join`).
- **Write model:** Parallel fan-out writes (PG+ES for contacts and companies + `filters_data`).
- **Middleware:** CORS -> gzip -> token-bucket rate limiter -> API key auth.
- **API groups:** `/contacts`, `/companies`, `/common`, plus `/health`.
- **Job engine:** Buffered queue with worker pools (`first_time` and `retry`) and state transitions.

## Route surface

- `POST /contacts/`, `POST /contacts/count`, `POST /contacts/batch-upsert`
- `POST /companies/`, `POST /companies/count`, `POST /companies/batch-upsert`
- `POST /common/batch-upsert`, `GET /common/upload-url`
- `POST /common/jobs`, `POST /common/jobs/create`
- `GET|POST /common/:service/filters`, `GET|POST /common/:service/filters/data`
- `GET /health`

## Core mechanics

### VQL and query execution

- `exact` -> `match_phrase` (+ optional `slop`)
- `shuffle` -> `match` (+ fuzzy/operator tuning)
- `substring` -> ngram-backed matching field path
- `keyword_match` and `range_query` support exact and numeric/date boundaries

### Parallel write flow

`BulkUpsertToDb` executes five concurrent stores and joins on `WaitGroup` completion:

1. PG contacts
2. ES contacts
3. PG companies
4. ES companies
5. `filters_data` facet rows

### Job engine

State progression: `OPEN -> IN_QUEUE -> PROCESSING -> COMPLETED|FAILED -> RETRY_IN_QUEUED`.

- Primary runner: `first_time` worker pool
- Retry runner: single worker
- Queue capacity: 1000 buffered channel

### Idempotency and dedup

- Contacts UUID5 key: `firstName + lastName + linkedinURL`
- Companies UUID5 key: `name + linkedinURL`
- Filter facet UUID5 key: `filterKey + service + value`

## Strengths

- Strong throughput profile via goroutines/channel-based concurrency.
- Deterministic IDs enable repeatable batch upserts and conflict-safe retries.
- Two-phase read keeps search relevance in ES and authoritative records in PG.
- `io.Pipe()` streaming model supports large CSV workloads with bounded memory.

## Gaps and risks

- Single in-memory queue can lose pending work on abrupt process crash.
- API key and rate-limit policy need stricter rotation and tenant partitioning.
- `AllowAllOrigins` CORS posture is too broad for hardened environments.
- ES/PG drift detection and reconciliation automation are not first-class.

## Era mapping (`0.x`-`10.x`)

| Era | Connectra concern | Small-task decomposition |
| --- | --- | --- |
| `0.x` | Service bootstrap | API key baseline, index bootstrap scripts, health checks |
| `1.x` | Credit-aware usage | Search/export volume guards and billing event alignment |
| `2.x` | Bulk email pipeline | CSV contract stability, column mapping, stream import/export |
| `3.x` | Core data system | VQL freeze, filter taxonomy, dual-write and dedup integrity |
| `4.x` | Extension/SN ingest | Provenance fields and idempotent sync from SN sources |
| `5.x` | AI workflows | AI-readable attributes and enrichment artifact lookup paths |
| `6.x` | Reliability/scaling | Query P95 SLO, job success SLI, retry/DLQ hardening |
| `7.x` | Deployment governance | RBAC on write/export, audit evidence, tenant isolation |
| `8.x` | Public/private APIs | Versioned REST contracts, partner keys, webhook-ready job events |
| `9.x` | Productization | Quota-aware throttling and connector-safe filter contracts |
| `10.x` | Campaign runtime | Audience query stability, suppression filter compliance, export controls |

## Immediate execution queue

1. Add persistent queue backing for job durability.
2. Add ES-PG reconciliation job and drift diagnostics.
3. Add per-tenant rate limiting and API key scope model.
4. Add contract-parity tests for VQL operators and filter metadata.
5. Add release gates for batch-upsert idempotency evidence.

## Suggested owner map

- **Connectra service owner:** Search/Data Engineering
- **Gateway contract owner:** Appointment360/API team
- **UI contract owner:** Dashboard data-experience team
- **Ops owner:** Platform reliability team

## Release gate checklist

- 🔴 Incompleted: VQL taxonomy changes mirrored in `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`.
- 🔴 Incompleted: Endpoint/table bindings updated in `docs/backend/apis/` and `docs/backend/endpoints/*.json`.
- 🔴 Incompleted: ES mapping changes include integration tests for list/count/filter paths.
- 🔴 Incompleted: Batch-upsert contract changes include rollback and replay/idempotency evidence.
- 🔴 Incompleted: `docs/versions.md` and era task-pack docs updated for impacted eras.
```

---

## `d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md`

```markdown
# jobs codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`contact360.io/jobs` is the TKD Job scheduler service for long-running flows (email export/verify/pattern import, Contact360 import/export) with DAG-aware orchestration, retry support, and timeline observability.

## Runtime stack and architecture

- Runtime: FastAPI + SQLAlchemy + PostgreSQL + Kafka + ThreadPoolExecutor/ProcessPoolExecutor
- API entrypoint: `contact360.io/jobs/app/api/main.py`
- Router: `contact360.io/jobs/app/api/v1/routes/jobs.py`
- Scheduler: `contact360.io/jobs/app/workers/scheduler.py`
- Consumer: `contact360.io/jobs/app/workers/consumer.py`
- Worker pool: `contact360.io/jobs/app/workers/worker_pool.py`
- Processors: `contact360.io/jobs/app/processors/`
- Service/repo layer: `app/services/job_service.py`, `app/repositories/`
- Auth and rate limit: `app/middleware/auth.py`, `app/middleware/rate_limit.py`

## Data model (scheduler-owned database)

### `job_node`

- `uuid`, `job_title`, `job_type`, `degree`, `priority`, `status`
- `data` (JSONB), `job_response` (JSONB)
- `try_count`, `retry_interval`, `run_after`
- `checkpoint_byte`, `processed_rows`, `total_bytes`
- `checkpoint_uuid`, `checkpoint_data` (JSONB)
- `created_at`, `updated_at`, `deleted_at`

### `edges`

- `source` (FK -> `job_node.uuid`)
- `target` (FK -> `job_node.uuid`)

### `job_events`

- `id`, `job_uuid` (FK -> `job_node.uuid`)
- `event_type`, `event_data` (JSONB)
- `timestamp`

## Job lifecycle

`open -> in_queue -> processing -> completed | failed -> retry -> in_queue`

- Scheduler enqueues `open` and `retry` jobs when eligible.
- Worker updates progress via checkpoint fields and writes result/error envelopes in `job_response`.
- Timeline endpoint is backed by `job_events`.

## Processor registry (current)

| Job type | Processor | Main creation endpoint |
| --- | --- | --- |
| `email_finder_export_stream` | `email_finder_export_stream` | `POST /api/v1/jobs/email-export` |
| `email_verify_export_stream` | `email_verify_export_stream` | `POST /api/v1/jobs/email-verify` |
| `email_pattern_import_stream` | `email_pattern_import_stream` | `POST /api/v1/jobs/email-pattern-import` |
| `contact360_import_prepare` | `contact360_import_prepare` | `POST /api/v1/jobs/contact360-import` |
| `contact360_export_stream` | `contact360_export_stream` | `POST /api/v1/jobs/contact360-export` |
| `export_csv_file` | validation stub | DAG/manual only |
| `insert_csv_file` | validation stub | DAG/manual only |

## API contract snapshot

- `POST /api/v1/jobs/bulk-insert/complete-graph`
- `POST /api/v1/jobs/email-export`
- `POST /api/v1/jobs/email-verify`
- `POST /api/v1/jobs/email-pattern-import`
- `POST /api/v1/jobs/contact360-import`
- `POST /api/v1/jobs/contact360-export`
- `GET /api/v1/jobs/`, `GET /api/v1/jobs/{uuid}`, `GET /api/v1/jobs/{uuid}/status`
- `GET /api/v1/jobs/{uuid}/timeline`, `GET /api/v1/jobs/{uuid}/dag`
- `PUT /api/v1/jobs/{uuid}/retry`
- `POST /api/v1/jobs/validate/vql`
- `GET /api/v1/metrics`, `GET /api/v1/metrics/stats`
- `GET /health`, `/health/live`, `/health/ready`

## Key environment contracts

- Scheduler DB: `DATABASE_URL`
- Contact360 data-plane DB: `CONTACT360_DATABASE_URL`
- Search bridge: `OPENSEARCH_CONNECTION`
- Job transport: `KAFKA_BROKERS`
- Storage integration: `S3_BUCKET`
- Downstream email runtime: `EMAIL_API_BASE_URL`

## Known gaps and risks

1. Stale `processing` recovery depends on active scheduler recovery loop.
2. DAG degree-decrement failure can block downstream nodes.
3. Single shared `X-API-Key` model (no per-user/role authz in service itself).
4. Retry trigger is explicit `retry` status semantics; docs must not model retry directly from `failed`.
5. Some legacy multi-node Contact360 DAG patterns are no longer active in registry.

## Era-by-era small task breakdown (Contract / Service / Surface / Data / Ops)

### 0.x Foundation
- Contract: baseline health and scheduler API envelope.
- Service: queue/scheduler/consumer/worker baseline.
- Surface: initial jobs status cards + polling hooks.
- Data: `job_node`/`edges`/`job_events` migration baseline.
- Ops: boot checks, worker liveness, crash recovery runbook.

### 1.x User/Billing/Credit
- Contract: credit-aware creation and usage audit payload.
- Service: attach billing context to job metadata.
- Surface: user-facing credit warnings/retry affordances.
- Data: job-to-credit trace fields in audit events.
- Ops: billing-impact monitoring and fallback controls.

### 2.x Email system
- Contract: finder/verify/pattern stream job contracts.
- Service: harden email stream processors and CSV contracts.
- Surface: progress bars, mapping controls, retry radios.
- Data: result CSV lineage and checkpoint visibility.
- Ops: throughput/error dashboards for email jobs.

### 3.x Contact/company data
- Contract: import/export + VQL validation contracts.
- Service: `contact360_import_prepare` and `contact360_export_stream`.
- Surface: import/export table states and detail dialogs.
- Data: PG+OpenSearch lineage and replay safety.
- Ops: partial-failure handling and replay runbooks.

### 4.x Extension/Sales Navigator
- Contract: extension-origin provenance fields.
- Service: sync/ingestion jobs with source tagging.
- Surface: extension sync status and retry controls.
- Data: provenance lineage and dedupe markers.
- Ops: extension sync drift alerting.

### 5.x AI workflows
- Contract: AI batch job envelope (`confidence`, `cost`).
- Service: AI processor stubs and quota-aware scheduling.
- Surface: AI job explanation/progress UI surfaces.
- Data: model/run metadata in `job_response`.
- Ops: model cost and failure guardrails.

### 6.x Reliability/scaling
- Contract: idempotency and retry semantics as hard contract.
- Service: DLQ/retry hardening and stale job recovery tuning.
- Surface: reliability dashboards and incident drilldowns.
- Data: idempotency keys and duplicate suppression evidence.
- Ops: SLO/error-budget monitoring + chaos tests.

### 7.x Deployment
- Contract: deployment and access-control contract upgrades.
- Service: role-aware API keys / token auth path.
- Surface: admin-only controls and audit review panels.
- Data: retention and deletion policy evidence.
- Ops: deployment gating with jobs health checklist.

### 8.x Public/private APIs
- Contract: versioned job API and callback/webhook contracts.
- Service: partner-safe submission and scoped credentials.
- Surface: API integration pages and key selectors.
- Data: external callback event lineage.
- Ops: backward-compatibility and deprecation playbooks.

### 9.x Ecosystem/productization
- Contract: tenant quotas and entitlement scheduling contract.
- Service: tenant isolation and fairness scheduling.
- Surface: tenant quota dashboards and controls.
- Data: per-tenant partitioning and audit boundaries.
- Ops: SLA monitoring across tenant cohorts.

### 10.x Email campaign
- Contract: campaign send/track/verify processor contract.
- Service: strict idempotency and compliance bundles.
- Surface: campaign execution/timeline compliance views.
- Data: immutable audit timelines via `job_events`.
- Ops: compliance readiness checks before campaign runs.
```

---

### Focus: **8.x**, **gaps/risks**, and **execution queue**

| File | **8.x** | **Gaps / risks** | **Queue** |
| --- | --- | --- | --- |
| **Appointment360** | Pages, saved searches, profile/API keys, **public API surface**. | Debug file writes; DocsAI off by default / no health; rate limit off by default; missing SQL schema in checkout; no campaigns module yet; in-memory abuse guard; DB-only token blacklist; `.cursor/debug.log` writes. | Titled **“Immediate execution queue”**: strip debug I/O; add campaign GraphQL modules; enable GraphQL rate limit in prod; schema docs; Redis for idempotency/abuse; DocsAI health; contract parity tests. |
| **Connectra** | **Public/private APIs**: versioned REST, partner keys, **webhook-ready job events**. | In-memory job queue durability; API key / rate-limit needs rotation + tenant partitioning; permissive CORS; no first-class ES/PG drift reconciliation. | Titled **“Immediate execution queue”**: persistent queue; ES–PG reconciliation/diagnostics; per-tenant limits + key scopes; VQL/filter contract tests; idempotency release gates. |
| **jobs** | **Public/private APIs**: versioned job API, **callback/webhook** contracts; partner-safe submission; scoped creds; integration UX; callback lineage; compat playbooks. | Stale `processing` tied to scheduler recovery; DAG degree blocking; single `X-API-Key`; retry semantics doc trap (`failed` vs explicit `retry`); legacy DAG patterns inactive. | **No** separate “Immediate engineering queue”; closest is the era breakdown (8.x bullets above). |

Naming note: only the **jobs** doc uses the heading **“Known gaps and risks”**; Appointment360 and Connectra use **“Gaps and risks”**. None use the exact phrase **“Immediate engineering queue”**—Appointment360 and Connectra use **“Immediate execution queue”**.

