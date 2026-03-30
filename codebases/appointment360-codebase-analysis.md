# Appointment360 Codebase Analysis (`contact360.io/api`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

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

```text
query { auth | users | contacts | companies | email | jobs | usage | billing | analytics | activities | health | pages | s3 | upload | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume | featureOverview }
mutation { auth | users | contacts | companies | billing | linkedin | jobs | email | usage | upload | s3 | analytics | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume }
```

### Request lifecycle

```text
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

## Verified completion status from runtime

- [x] ✅ GraphQL gateway architecture is fully established with modular query/mutation namespaces.
- [x] ✅ Security middleware exists for idempotency, mutation abuse guard, tracing, and body-size limits.
- [x] ✅ Multi-service client integration exists (`email`, `s3storage`, `logs.api`, `tkdjob`, `connectra`, `docsai`, `ai`).
- [x] ✅ Health endpoints include DB/logging/SLO visibility.
- [x] ✅ Upload/session Redis options and operational config toggles are already present.

## Active risks and gap map

### Security and configuration drift

- [ ] ⬜ Incomplete: several service API keys/URLs have real-looking defaults in config and need secret-only policy.
- [ ] ⬜ Incomplete: production security depends on environment discipline; default values remain risky for misconfigured deploys.
- [ ] 🟡 In Progress: idempotency guard exists, but strict enforcement (`IDEMPOTENCY_ENFORCE_GRAPHQL_MUTATIONS`) is optional and not always enabled.

### Contract and module completeness

- [ ] ⬜ Incomplete: campaign GraphQL modules (`campaigns/sequences/templates`) are still missing for full `10.x` scope.
- [ ] 🟡 In Progress: docs/runtime parity across all module contracts is partial.
- [ ] ⬜ Incomplete: status/behavior contract consistency for downstream email/storage/log clients requires stronger automated coverage.

### Reliability and scale gaps

- [ ] 🟡 In Progress: middleware-level controls are strong, but distributed state for abuse/idempotency remains incomplete across replicas.
- [ ] ⬜ Incomplete: token blacklist and some anti-abuse controls need shared-store hardening for horizontal scale.
- [ ] ⬜ Incomplete: residual debug/log artifact patterns must be removed from production paths.

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ GraphQL-first contract and module namespace structure are in place.
- [ ] 🟡 In Progress: keep resolver payload contracts aligned with downstream service APIs.
- [ ] ⬜ Incomplete: enforce stricter idempotency contract for all high-risk mutations in production.
- [ ] ⬜ Incomplete: finalize campaign API contract surface for `10.x`.
- [ ] 📌 Planned: publish explicit public/private GraphQL boundary and deprecation policy.

### Service pack

- [x] ✅ Core orchestration clients and service bridges are implemented.
- [ ] 🟡 In Progress: harden distributed anti-abuse/idempotency behavior for multi-instance deployments.
- [ ] ⬜ Incomplete: remove any remaining debug-file write and ad-hoc logging artifacts.
- [ ] ⬜ Incomplete: complete campaign service orchestration modules.
- [ ] 📌 Planned: add policy-driven connector governance controls for ecosystem scale.

### Surface pack

- [x] ✅ Dashboard and extension can access all major capability modules through gateway.
- [ ] 🟡 In Progress: improve deterministic error envelopes and retry hints for clients.
- [ ] ⬜ Incomplete: close UX/API contract gaps for campaign and advanced admin flows.
- [ ] 📌 Planned: partner-facing integration guides and compatibility guarantees.

### Data pack

- [x] ✅ Async DB/session lifecycle and repository patterns are implemented.
- [ ] 🟡 In Progress: strengthen trace/request lineage consistency across all module calls.
- [ ] ⬜ Incomplete: shared-store strategy for blacklist/guard state at scale.
- [ ] 📌 Planned: campaign evidence and compliance lineage model.

### Ops pack

- [x] ✅ Health checks, RED metrics, and SLO endpoints exist in runtime.
- [ ] ⬜ Incomplete: remove insecure config defaults and enforce startup hard-fail for missing secrets in production.
- [ ] ⬜ Incomplete: add stronger contract parity tests tied to docs and release gates.
- [ ] 🟡 In Progress: rate-limit and abuse guard tuning per environment.
- [ ] 📌 Planned: reliability promotion gates based on error budgets and multi-service dependency health.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: gateway bootstrap, middleware baseline, context/session lifecycle, and schema composition are implemented.
- [ ] 🟡 In Progress: close foundational docs/runtime drift.
- [ ] ⬜ Incomplete: remove insecure default config values from baseline templates/settings.

### `1.x.x - Contact360 user and billing and credit system`

- [x] ✅ Completed: auth, billing, usage, and credit mutation/query pathways are present.
- [ ] 🟡 In Progress: strengthen immutable audit evidence for billing/admin high-risk actions.
- [ ] ⬜ Incomplete: strict idempotency enforcement for all billing mutations in production.

### `2.x.x - Contact360 email system`

- [x] ✅ Completed: email finder/verifier and job orchestration modules are integrated.
- [ ] 🟡 In Progress: normalize downstream email provider semantics and retry behavior contracts.
- [ ] ⬜ Incomplete: add full replay/failure-path tests for email-job orchestration.

### `3.x.x - Contact360 contact and company data system`

- [x] ✅ Completed: contact/company modules, VQL conversion, and Connectra integration are operational.
- [ ] 🟡 In Progress: improve enrichment lineage and trace consistency.
- [ ] ⬜ Incomplete: tighten contract parity between GraphQL filters and Connectra query semantics.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [x] ✅ Completed: LinkedIn/SalesNavigator mutation surfaces exist and are wired.
- [ ] 🟡 In Progress: improve extension-session and sync mutation reliability guarantees.
- [ ] ⬜ Incomplete: full support diagnostics and retry contracts for extension-origin ingest.

### `5.x.x - Contact360 AI workflows`

- [x] ✅ Completed: AI chats and resume module integration exist.
- [ ] 🟡 In Progress: tighten AI safety, error handling, and observability conventions.
- [ ] ⬜ Incomplete: complete cross-service AI lineage and policy guard evidence.

### `6.x.x - Contact360 Reliability and Scaling`

- [x] ✅ Completed: complexity/timeout, idempotency, abuse-guard, and RED/SLO middleware foundations.
- [ ] 🟡 In Progress: tune per-environment limits and error budget policies.
- [ ] ⬜ Incomplete: distributed shared-state enforcement for anti-abuse/idempotency/token controls.

### `7.x.x - Contact360 deployment`

- [x] ✅ Completed: multi-target deployment support (EC2/Lambda/Docker) and production guard warnings exist.
- [ ] 🟡 In Progress: deployment governance checklists and runbook alignment.
- [ ] ⬜ Incomplete: strict secret and secure-default enforcement before release promotion.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 🟡 In Progress: broad GraphQL capability exposure exists for internal/private use.
- [ ] ⬜ Incomplete: explicit versioning and public/private API governance model.
- [ ] 📌 Planned: partner-safe API contracts and compatibility suite.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 🟡 In Progress: notifications, saved searches, and connector module foundations exist.
- [ ] ⬜ Incomplete: tenant-safe entitlement controls and ecosystem governance completeness.
- [ ] 📌 Planned: SLA evidence and support tooling for partner channels.

### `10.x.x - Contact360 email campaign`

- [ ] ⬜ Incomplete: campaign/sequences/templates GraphQL modules are not complete.
- [ ] 📌 Planned: campaign wizard orchestration and compliance evidence contracts.
- [ ] 📌 Planned: campaign release gates tied to deliverability/compliance SLO signals.

---

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove insecure service key defaults and enforce secret-only startup policy.
- [ ] ⬜ Incomplete: complete campaign GraphQL modules (`campaigns`, `sequences`, `campaignTemplates`).
- [ ] 🟡 In Progress: tune and enforce GraphQL rate limit and abuse guard settings per environment.
- [ ] ⬜ Incomplete: add Redis-backed distributed state for idempotency/abuse/token controls.
- [ ] ⬜ Incomplete: add docs/runtime contract parity tests against backend API docs.
- [ ] 🟡 In Progress: wire dependency-specific health visibility (including DocsAI readiness).
- [ ] ⬜ Incomplete: remove residual debug file-write paths from resolver/client code.

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

## 2026 Gap Register (actionable)

### P0

- [ ] ⬜ Incomplete: `AP-0.1` Remove resolver/client debug file writes from production paths.
- [ ] ⬜ Incomplete: `AP-0.2` Remove insecure API key defaults from runtime settings.
- [ ] ⬜ Incomplete: `AP-0.3` Campaign/sequences/templates GraphQL module completion for `10.x`.
- [ ] 🟡 In Progress: `AP-0.4` Enforce environment-specific rate-limit/idempotency guard policy.

### P1/P2

- [ ] ⬜ Incomplete: `AP-1.2` Move idempotency/abuse-guard state to shared store for multi-instance safety.
- [ ] 🟡 In Progress: `AP-1.3` Add mutation-level SLI exports for top heavy operations.
- [ ] ⬜ Incomplete: `AP-2.1` Immutable audit events for billing/admin/high-risk mutations.
- [ ] ⬜ Incomplete: `AP-2.2` Resolver-to-doc contract parity automation.

### P3+

- [ ] 📌 Planned: `AP-3.1` Public/private API governance package and compatibility suite.
- [ ] 📌 Planned: `AP-3.2` Ecosystem SLA evidence and partner incident tooling.
