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

Single endpoint `/graphql` (plus health probes). No REST feature routes. The schema (`schema.py`) is composed as a flat `Query` + `Mutation` root with nested module namespaces (23 query roots including top-level `featureOverview`; mutations omit that field). Campaign modules under `app/graphql/modules/campaigns/` are scaffold-only and not mounted on the root schema yet.

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
| email | `EmailQuery` | `findEmails`, `createEmailFinderExportJob`, `createEmailVerifyExportJob`, `createEmailPatternImportJob`, `findEmailsBulk`, `verifySingleEmail`, `verifyEmailsBulk`, `exportEmails`, `verifyexportEmail` |
| jobs | `JobQuery` | `job(jobId)`, `jobs(limit,offset,status,jobType)` |
| usage | `UsageQuery` | `usage(feature)` |
| featureOverview | `FeatureOverviewQuery` | `featureOverview()` |
| billing | `BillingQuery` | `billing`, `plans`, `addons`, `invoices`, `paymentInstructions`, `paymentSubmissions` |
| activities | `ActivityQuery` | `activities(...)`, `activityStats(...)` |
| analytics | `AnalyticsQuery` | `performanceMetrics`, `aggregateMetrics` |
| health | `HealthQuery` | `apiMetadata`, `apiHealth`, `vqlHealth`, `vqlStats`, `performanceStats` |
| pages | `PagesQuery` | `page`, `pages`, `pageContent`, `pagesByType`, `pageTypes`, `pageStatistics`, `pagesByState`, `pagesByStateCount`, `pagesByUserType`, `pagesByDocsaiUserType`, `myPages`, `pageAccessControl`, `pageSections`, `pageComponents`, `pageEndpoints`, `pageVersions`, `dashboardPages`, `marketingPages` |
| s3 | `S3Query` | `s3Files`, `s3FileData`, `s3FileInfo`, `s3FileDownloadUrl`, `s3FileSchema`, `s3FileStats`, `s3BucketMetadata` |
| upload | `UploadQuery` | `uploadStatus`, `presignedUrl` |
| aiChats | `AIChatQuery` | `aiChat(uuid)`, `aiChats()` |
| notifications | `NotificationQuery` | `notifications`, `notification`, `unreadCount`, `notificationPreferences` |
| salesNavigator | `SalesNavigatorQuery` | `salesNavigatorRecords(...)` |
| admin | `AdminQuery` | `users`, `usersWithBuckets`, `userStats`, `userHistory`, `logStatistics`, `logs`, `searchLogs` |
| savedSearches | `SavedSearchQuery` | `listSavedSearches(...)`, `getSavedSearch(...)` |
| twoFactor | `TwoFactorQuery` | `get2FAStatus()` |
| profile | `ProfileQuery` | `listAPIKeys()`, `listSessions()`, `listTeamMembers()` |
| resume | `ResumeQuery` | `resumes()`, `resume(id)` |

### Mutation modules

| Module | Class | Key operations |
| --- | --- | --- |
| auth | `AuthMutation` | `login`, `register`, `logout`, `refresh_token` |
| users | `UserMutation` | `update_profile`, `upload_avatar`, `update_user`, `promote_to_admin`, `promote_to_super_admin` |
| contacts | `ContactMutation` | `createContact`, `batchCreateContacts`, `importContacts`, `updateContact`, `deleteContact`, `exportContacts` |
| companies | `CompanyMutation` | `createCompany`, `exportCompanies`, `importCompanies`, `updateCompany`, `deleteCompany` |
| billing | `BillingMutation` | `subscribe`, `purchaseAddon`, `submitPaymentProof`, `approvePayment`, `declinePayment` |
| linkedin | `LinkedInMutation` | `search`, `upsertByLinkedInUrl` |
| jobs | `JobMutation` | `createEmailFinderExport`, `createEmailVerifyExport`, `createEmailPatternImport`, `createContact360Export`, `createContact360Import`, `createAppointmentImport`, `retryJob` |
| email | `EmailMutation` | `addEmailPattern`, `addEmailPatternBulk` |
| usage | `UsageMutation` | `trackUsage`, `resetUsage` |
| upload | `UploadMutation` | `initiateUpload`, `registerPart`, `completeUpload`, `abortUpload` |
| s3 | `S3Mutation` | `initiateCsvUpload`, `completeCsvUpload`, `deleteFile` |
| analytics | `AnalyticsMutation` | `submitPerformanceMetric` |
| aiChats | `AIChatMutation` | `createAIChat`, `updateAIChat`, `deleteAIChat`, `sendMessage`, `analyzeEmailRisk`, `generateCompanySummary`, `parseContactFilters` |
| notifications | `NotificationMutation` | `markNotificationAsRead`, `markNotificationsAsRead`, `deleteNotifications`, `updateNotificationPreferences` |
| salesNavigator | `SalesNavigatorMutation` | `saveSalesNavigatorProfiles` |
| admin | `AdminMutation` | `updateUserRole`, `updateUserCredits`, `deleteUser`, `promoteToAdmin`, `promoteToSuperAdmin`, `createLog`, `createLogsBatch`, `updateLog`, `deleteLog`, `deleteLogsBulk` |
| savedSearches | `SavedSearchMutation` | `createSavedSearch`, `updateSavedSearch`, `deleteSavedSearch`, `updateSavedSearchUsage` |
| twoFactor | `TwoFactorMutation` | `setup2FA`, `verify2FA`, `disable2FA`, `regenerateBackupCodes` |
| profile | `ProfileMutation` | `createAPIKey`, `deleteAPIKey`, `revokeSession`, `revokeAllOtherSessions`, `inviteTeamMember`, `updateTeamMemberRole`, `removeTeamMember` |
| resume | `ResumeMutation` | `saveResume`, `deleteResume` |

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

- [x] ✅ Completed: runtime service URL defaults are now removed from settings, and production enforces URL/API-key pairing for downstream dependencies.
- [x] ✅ Completed: deployment env templates now sanitize real-looking API URLs/keys and replace token-like commented examples with redacted placeholders.
- [ ] ⬜ Incomplete: production security depends on environment discipline; default values remain risky for misconfigured deploys.
- [ ] 🟡 In Progress: idempotency guard exists, but strict enforcement (`IDEMPOTENCY_ENFORCE_GRAPHQL_MUTATIONS`) is optional and not always enabled.

### Contract and module completeness

- [ ] ⬜ Incomplete: campaign GraphQL modules (`campaigns/sequences/templates`) are still missing for full `10.x` scope.
- [ ] 🟡 In Progress: docs/runtime parity across all module contracts is partial.
- [ ] ⬜ Incomplete: status/behavior contract consistency for downstream email/storage/log clients requires stronger automated coverage.

### Reliability and scale gaps

- [ ] 🟡 In Progress: production now enforces PostgreSQL backends for idempotency and upload sessions; abuse-guard/token shared-store state remains incomplete across replicas.
- [ ] 🟡 In Progress: token blacklist checks are expiry-aware with eager stale-entry cleanup plus startup/shutdown and periodic lifecycle cleanup hooks (configurable cadence, production-enforced interval > 0), and health evidence is exposed via both REST (`/health/token-blacklist`) and GraphQL (`health.performanceStats.token_blacklist_cleanup`) with contract test coverage (`tests/graphql/test_health_performance_stats.py`); broader token-control scale hardening remains pending.
- [x] ✅ Completed: resolver/client debug artifact patterns are removed and protected with regression guard tests (`tests/test_no_debug_artifacts.py`).

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
- [x] ✅ Completed: add regression guard to block debug artifact patterns in historically risky resolver/client files.
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
- [ ] 🟡 In Progress: shared-store strategy is implemented for abuse/idempotency; token-blacklist reliability improved via expiry-aware checks and stale-entry cleanup.
- [ ] 📌 Planned: campaign evidence and compliance lineage model.

### Ops pack

- [x] ✅ Health checks, RED metrics, and SLO endpoints exist in runtime.
- [ ] 🟡 In Progress: startup now hard-fails in production for permissive wildcard CORS/trusted-host config (`ALLOWED_ORIGINS='*'` or `TRUSTED_HOSTS='*'`); remaining secret-default cleanup is pending.
- [ ] ⬜ Incomplete: add stronger contract parity tests tied to docs and release gates.
- [ ] 🟡 In Progress: rate-limit and abuse guard tuning per environment.
- [ ] 📌 Planned: reliability promotion gates based on error budgets and multi-service dependency health.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: gateway bootstrap, middleware baseline, context/session lifecycle, and schema composition are implemented.
- [x] ✅ Completed: foundational docs/runtime drift for Appointment360 — `appointment360_endpoint_era_matrix.md` aligned with resolvers, parity tests (`test_endpoint_docs_*.py`, `tests/doc_paths.py`), and CI (`docs/.github/workflows/ci.yml`).
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
- [ ] 🟡 In Progress: PostgreSQL-backed distributed state is enforced for idempotency and abuse guard in production; token controls still need final scale hardening.
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

- [x] ✅ Completed: `AP-0.1` Resolver/client debug artifact regression guard added (`tests/test_no_debug_artifacts.py`) and risky paths are clean.
- [x] ✅ Completed: `AP-0.2` Production now fails closed on wildcard CORS/trusted-host settings and enforces downstream URL/API-key contracts (including DocsAI and Sales Navigator enablement checks).
- [ ] ⬜ Incomplete: `AP-0.3` Campaign/sequences/templates GraphQL module completion for `10.x`.
- [x] ✅ Completed: `AP-0.4` Production now enforces strict GraphQL idempotency guard policy (`IDEMPOTENCY_ENFORCE_GRAPHQL_MUTATIONS=true`) plus postgres-backed idempotency/abuse/session backends.

### P1/P2

- [x] ✅ Completed: `AP-1.2` Abuse guard now supports PostgreSQL-backed shared window state (`graphql_abuse_guard_events`) and production enforces `IDEMPOTENCY_BACKEND=postgres`, `UPLOAD_SESSION_BACKEND=postgres`, and `ABUSE_GUARD_BACKEND=postgres`.
- [x] ✅ Completed: `AP-1.3` Guarded mutation SLI exports are now emitted via `/health/slo` (`guarded_mutation_sli`) with per-mutation request/success/error/rate-limited and latency metrics.
- [ ] 🟡 In Progress: `AP-2.1` Immutable audit events — append-only `graphql_audit_events` (`app/models/graphql_audit_event.py`, `append_graphql_audit_event` in `app/services/graphql_audit_service.py`, migration `20260402_0004_graphql_audit_events.py`); wired for `updateUserCredits`, `approvePayment`, `declinePayment`. **Extend** to other admin/billing mutations and add read/query path or export as needed.
- [x] ✅ Completed: `AP-2.2` Docs/runtime parity — health REST list vs `appointment360_endpoint_era_matrix.md`; `module_index` rows vs resolver sources (`test_endpoint_docs_parity.py`, `tests/doc_paths.py`, meta-test for full matrix coverage); high-risk and privileged mutation doc presence + metadata (`test_endpoint_docs_operation_parity.py`, `test_endpoint_docs_metadata_parity.py`, including users promote mutations); CI gate in `docs/.github/workflows/ci.yml` (**Run Appointment360 docs/runtime parity tests**). Follow-up: broader per-operation Markdown outside the matrix is optional.

### P3+

- [ ] 📌 Planned: `AP-3.1` Public/private API governance package and compatibility suite.
- [ ] 📌 Planned: `AP-3.2` Ecosystem SLA evidence and partner incident tooling.
