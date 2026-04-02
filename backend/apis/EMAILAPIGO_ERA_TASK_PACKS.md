# EMAILAPIGO Era Task Packs — EC2/email.server (Go Gin, Asynq/Redis)

**Module:** `github.com/ayan/emailapigo`  
**Repo path:** `EC2/email.server`  
**Gateway client:** `contact360.io/api` → `app/clients/lambda_email_client.py` → `LAMBDA_EMAIL_API_URL`  
**Port:** `3000` (default config) / `8080` (production target — see FIX-1)  
**Dependencies tracked:** Mailtester.ninja, Mailvetter, Truelist, IcyPeas, Connectra (sync.server), OpenAI, DuckDuckGo, AWS S3, Redis, PostgreSQL, logs API  
**Endpoints doc:** `docs/backend/endpoints/emailapis_endpoint_era_matrix.md`  
**Postman:** `docs/backend/postman/EC2_email.server.postman_collection.json`  
**Database doc:** `docs/backend/database/`  
**Codebase analysis:** `docs/codebases/emailapis-codebase-analysis.md`  

---

## Era task file index

- `0.x`: `emailapigo-foundation-task-pack.md`
- `1.x`: `emailapigo-user-billing-task-pack.md`
- `2.x`: `docs/2. Contact360 email system/` — per-patch Service task slices (emailapigo scope merged with emailapis era packs)
- `3.x`: `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md`
- `4.x`: `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md`
- `5.x`: `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md`
- `6.x`: `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md`
- `7.x`: `docs/7. Contact360 deployment/` — patches `7.N.P — *.md`
- `8.x`: `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md`
- `9.x`: `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md`
- `10.x`: `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md`

---

## Complete 121-file task breakdown (Eras 0–10, minor patches)

Every item below is one **file to create or modify** in `EC2/email.server` or its associated docs/infra, mapped to an era and a patch number. Files are grouped by era. Total: **121 files**.

---

### Era 0 — Foundation and codebase stabilisation (21 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `internal/config/config.go` | **MODIFY** | Change `PORT` default from `3000` → `8080`; add `WorkerConcurrency int` field; add `LogsAPIURL`, `LogsAPIKey` fields; add `ProviderPrimary`, `ProviderFallback` fields |
| 2 | `docker-compose.email.yml` | **MODIFY** | Align port mapping `8080:8080`; set `PORT=8080` env; add healthcheck path `/health` |
| 3 | `docker-compose.yml` | **MODIFY** | Same port alignment for `api` service |
| 4 | `.env.example` | **MODIFY** | Add `LOGS_API_URL`, `LOGS_API_KEY`, `WORKER_CONCURRENCY`, `PROVIDER_PRIMARY`, `PROVIDER_FALLBACK`; fix `MAILVETTER_BASE_URL` typo; set `PORT=8080` |
| 5 | `internal/clients/mailvetter_client.go` | **MODIFY** | Fix `MAILVETTER_BASE_URL` default from `mailvaiter.com` to `https://api.mailvetter.com/v1` (verify correct host) |
| 6 | `internal/logging/batch_logger.go` | **MODIFY** | Replace hardcoded `https://c2cox8ij6c.execute-api.us-east-1.amazonaws.com/logs/batch` with `cfg.LogsAPIURL`; add `LOGS_API_KEY` header |
| 7 | `internal/api/router.go` | **MODIFY** | Add `/health/live` (200 OK), `/health/ready` (Redis ping + DB ping), `/health/db` (GORM ping) endpoints |
| 8 | `db/migrations/001_emailapi_jobs.sql` | **CREATE** | DDL for `emailapi_jobs` table matching all columns in raw SQL in `router.go` + `output_s3_key` |
| 9 | `db/migrations/002_email_patterns.sql` | **CREATE** | DDL for `email_patterns` table (mirror GORM model; avoids AutoMigrate in production) |
| 10 | `db/migrations/003_email_finder_cache.sql` | **CREATE** | DDL for `email_finder_cache` table (mirror GORM model) |
| 11 | `db/migrations/README.md` | **CREATE** | Migration execution order, how to run, rollback policy |
| 12 | `Makefile` | **MODIFY** | Add `make migrate`, `make test`, `make lint`, `make build`, `make run`, `make run-worker` targets |
| 13 | `internal/middleware/request_id.go` | **CREATE** | `X-Request-ID` middleware: read header or generate UUID; set on `gin.Context` and outgoing log fields |
| 14 | `internal/middleware/auth.go` | **MODIFY** | Use constant-time compare for API key; log auth failure with request_id |
| 15 | `internal/errors/errors.go` | **MODIFY** | Add standard error envelope `{ "error": { "code", "message", "request_id" } }` response helper |
| 16 | `internal/utils/logger.go` | **MODIFY** | Add `request_id` field propagation from context |
| 17 | `README.md` | **CREATE** | Service README: architecture diagram, env vars table, Docker run, worker run, migration, health probes |
| 18 | `.dockerignore` | **MODIFY** | Verify `.env` excluded; add `reports/`, `tools/`, `patches/` |
| 19 | `internal/clients/database.go` | **MODIFY** | Remove AutoMigrate gate (use SQL migrations instead); add `PingDB()` helper used by `/health/db` |
| 20 | `internal/clients/database.go` | **MODIFY** | Add `InitRedis(cfg)` to return `*redis.Client` used by both API and worker startup |
| 21 | `docs/api.md` | **MODIFY** | Update all route paths (add missing predict routes, correct health paths, fix port) |

---

### Era 1 — User / billing / credit (8 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 22 | `internal/schemas/requests.go` | **MODIFY** | Add optional `UserID string` and `TenantID string` to all request structs used by finder/verifier |
| 23 | `internal/schemas/responses.go` | **MODIFY** | Add `UserID`, `RequestID`, `TenantID` to all response structs for credit lineage tracing |
| 24 | `internal/middleware/user_context.go` | **CREATE** | Extract `X-User-ID`, `X-Tenant-ID` headers into `gin.Context`; propagate to services |
| 25 | `internal/api/router.go` | **MODIFY** | Register `UserContextMiddleware` on `authGroup` |
| 26 | `internal/services/email_finder_service.go` | **MODIFY** | Accept `userID`, `tenantID` params; write to cache and log entries |
| 27 | `internal/services/email_verification_service.go` | **MODIFY** | Accept `userID`, `tenantID`; log per-user operation |
| 28 | `internal/repositories/email_finder_cache_repository.go` | **MODIFY** | Add `user_id` column to cache model + upsert |
| 29 | `internal/models/email_finder_cache.go` | **MODIFY** | Add `UserID string` GORM field; update `TableName()` |

---

### Era 2 — Email system (core finder/verifier hardening, 28 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 30 | `internal/api/router.go` | **MODIFY** | Wire `POST /email-patterns/predict` using `EmailPatternPredictRequest` → `patternSvc.PredictPattern` |
| 31 | `internal/api/router.go` | **MODIFY** | Wire `POST /email-patterns/predict/bulk` using `BulkEmailPatternPredictRequest` → `patternSvc.PredictPatternBulk` |
| 32 | `internal/api/router.go` | **MODIFY** | Wire `POST /email/single/verifier/find` (find then verify) using `SingleEmailVerifierFindResponse` |
| 33 | `internal/services/email_pattern_service.go` | **MODIFY** | Implement `PredictPattern(ctx, req)` and `PredictPatternBulk(ctx, req)` methods |
| 34 | `internal/schemas/responses.go` | **MODIFY** | Freeze `EmailVerificationStatus` as typed const block: `valid`, `invalid`, `catchall`, `unknown`, `risky` |
| 35 | `internal/schemas/requests.go` | **MODIFY** | Add `IdempotencyKey string` to `BulkEmailFinderRequest` and `BulkEmailVerifierRequest` |
| 36 | `internal/tasks/types.go` | **MODIFY** | Add `IdempotencyKey string` to `EmailVerifyPayload` and `EmailFindPayload` |
| 37 | `internal/worker/mailtester_worker.go` | **MODIFY** | Skip re-processing if result already in Redis hash (idempotency check by job_id+index) |
| 38 | `internal/worker/email_finder_worker.go` | **MODIFY** | Same idempotency check on Redis hash before running find |
| 39 | `internal/worker/generic_worker.go` | **MODIFY** | Same idempotency check for mailvetter path |
| 40 | `internal/worker/server.go` | **MODIFY** | Register `email:s3csv:verify:mailvetter` task type → new S3CSVMailvetterWorker |
| 41 | `internal/worker/s3csv_mailvetter_worker.go` | **CREATE** | S3 CSV verify worker using Mailvetter provider (parity with `s3csv_worker.go` for Mailtester) |
| 42 | `internal/tasks/types.go` | **MODIFY** | Add `S3CSVMailvetterPayload` struct |
| 43 | `internal/clients/mailtester.go` | **MODIFY** | Add `CachedVerify` method using `ttlcache`; document "Limited" response handling |
| 44 | `internal/clients/mailvetter_client.go` | **MODIFY** | Add `CachedVerify` method; fix bulk concurrency config via `MAILVETTER_BULK_CONCURRENCY` env |
| 45 | `internal/services/email_verification_service.go` | **MODIFY** | Freeze provider priority: primary = `PROVIDER_PRIMARY` env, fallback = `PROVIDER_FALLBACK` env; add `risky` status handling |
| 46 | `internal/services/email_finder_service.go` | **MODIFY** | Add request_id propagation; structured log for each stage (cache hit, Connectra, pattern, generate, verify) |
| 47 | `internal/utils/email_generator.go` | **MODIFY** | Document and test all supported prefix patterns; return pattern name with each candidate |
| 48 | `internal/utils/unmask_email.go` | **MODIFY** | Add unit test table for unmask logic |
| 49 | `internal/utils/domain.go` | **MODIFY** | Add domain normalisation test + MX record check stub (optional, gated by env) |
| 50 | `internal/repositories/email_pattern_repository.go` | **MODIFY** | Add `FindByDomainAndPattern` for predict lookup |
| 51 | `internal/repositories/email_finder_cache_repository.go` | **MODIFY** | Add `TTL` column; expire old cache entries on lookup |
| 52 | `internal/models/email_finder_cache.go` | **MODIFY** | Add `ExpiresAt *time.Time` field |
| 53 | `db/migrations/004_email_finder_cache_ttl.sql` | **CREATE** | Add `expires_at` column + partial index on non-expired rows |
| 54 | `internal/api/router.go` | **MODIFY** | Add response time header `X-Response-Time-Ms` on all routes via middleware |
| 55 | `internal/middleware/timing.go` | **CREATE** | Add `X-Response-Time-Ms` to response headers; integrate with MonitoringMiddleware |
| 56 | `internal/schemas/responses.go` | **MODIFY** | Add `Source string` to `SingleEmailVerifierResponse` (which provider was used) |
| 57 | `internal/services/s3csv_service.go` | **MODIFY** | Add configurable chunk size via `S3CSV_CHUNK_SIZE` env; add progress log every N rows |

---

### Era 3 — Contact / company data (8 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 58 | `internal/clients/connectra_client.go` | **MODIFY** | Add `SearchContacts(ctx, domain, name)` method returning candidates for finder flow |
| 59 | `internal/clients/connectra_client.go` | **MODIFY** | Add `X-Request-ID` header propagation to all Connectra requests |
| 60 | `internal/services/email_finder_service.go` | **MODIFY** | Improve candidate merge: dedupe by email address; retain `source` field per candidate |
| 61 | `internal/models/email_finder_cache.go` | **MODIFY** | Add `Source string` field (which service populated the cache entry) |
| 62 | `db/migrations/005_email_finder_cache_source.sql` | **CREATE** | Add `source` column to `email_finder_cache` |
| 63 | `internal/repositories/email_finder_cache_repository.go` | **MODIFY** | Write `source` on upsert; expose in lookup response |
| 64 | `internal/schemas/responses.go` | **MODIFY** | Add `Source string` to `SimpleEmailResult` (already partially present — ensure populated) |
| 65 | `docs/codebases/emailapis-codebase-analysis.md` | **MODIFY** | Update Era 3 status after Connectra integration tested end-to-end |

---

### Era 4 — Extension / Sales Navigator (5 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 66 | `internal/schemas/requests.go` | **MODIFY** | Add `Source string` (e.g. `extension`, `webapp`, `api`) to `EmailFinderRequest` |
| 67 | `internal/services/email_finder_service.go` | **MODIFY** | Log + pass `source` through cache + result metadata |
| 68 | `internal/models/email_finder_cache.go` | **MODIFY** | Update `Source` field to include `extension` as a valid value |
| 69 | `internal/api/router.go` | **MODIFY** | Extract `X-Source` header from context and pass to finder/verifier services |
| 70 | `docs/codebases/emailapis-codebase-analysis.md` | **MODIFY** | Update Era 4 status after extension source tagging confirmed |

---

### Era 5 — AI workflows (7 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 71 | `internal/clients/openai_client.go` | **MODIFY** | Add structured `confidence float64` to `EmailExtractionResult`; add fallback when OpenAI is unavailable |
| 72 | `internal/services/web_search_service.go` | **MODIFY** | Return `confidence` and `ai_model` in `WebSearchResponse`; add PII redaction for OpenAI context |
| 73 | `internal/schemas/responses.go` | **MODIFY** | Add `Confidence *float64`, `AIModel *string` to `SingleEmailResponse` |
| 74 | `internal/api/router.go` | **MODIFY** | Add `WEBSEARCH_ENABLED` gate check before calling web search; return `501` with message when disabled |
| 75 | `internal/clients/duckduckgo_client.go` | **MODIFY** | Clean up large commented-out duplicate block at top of file; add `MAX_SEARCH_RESULTS` env limit |
| 76 | `internal/config/config.go` | **MODIFY** | Add `WebSearchMaxResults int`, `OpenAIFallbackEnabled bool` config fields |
| 77 | `docs/codebases/emailapis-codebase-analysis.md` | **MODIFY** | Update Era 5 status |

---

### Era 6 — Reliability / scaling (15 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 78 | `internal/clients/circuit_breaker.go` | **CREATE** | Generic circuit breaker (state: closed/open/half-open) using `golang.org/x/time/rate` or `sony/gobreaker` |
| 79 | `internal/clients/mailtester.go` | **MODIFY** | Wrap HTTP call in circuit breaker; return `ErrProviderUnavailable` when open |
| 80 | `internal/clients/mailvetter_client.go` | **MODIFY** | Wrap HTTP call in circuit breaker |
| 81 | `internal/clients/truelist_client.go` | **MODIFY** | Wrap HTTP call in circuit breaker |
| 82 | `internal/clients/icypeas_client.go` | **MODIFY** | Wrap HTTP call in circuit breaker |
| 83 | `internal/errors/errors.go` | **MODIFY** | Add `ErrProviderUnavailable`, `ErrCircuitOpen` domain errors + HTTP 502/503 mapping |
| 84 | `internal/services/email_verification_service.go` | **MODIFY** | Handle `ErrCircuitOpen` → skip to fallback provider; log degradation event |
| 85 | `internal/utils/cache_metrics.go` | **MODIFY** | Extend to track per-provider latency (p50/p95 rolling window) |
| 86 | `internal/api/router.go` | **MODIFY** | Expose `/metrics` with Prometheus format (use `prometheus/client_golang` histograms); retire JSON-only metrics |
| 87 | `go.mod` | **MODIFY** | Add `github.com/prometheus/client_golang` dependency |
| 88 | `internal/middleware/monitoring.go` | **MODIFY** | Record Prometheus `http_request_duration_seconds` histogram + `email_operations_total` counter |
| 89 | `internal/worker/server.go` | **MODIFY** | Expose `WorkerConcurrency` per-queue from config instead of hardcoded values |
| 90 | `cmd/worker/main.go` | **MODIFY** | Read `WORKER_CONCURRENCY_{QUEUE}` env per queue; log queue startup config |
| 91 | `internal/services/s3csv_service.go` | **MODIFY** | Add `MAX_S3_CSV_ROWS` safety cap; return error if CSV exceeds limit |
| 92 | `internal/clients/database.go` | **MODIFY** | Add GORM connection pool config: `MAX_OPEN_CONNS`, `MAX_IDLE_CONNS`, `CONN_MAX_LIFETIME` env vars |

---

### Era 7 — Deployment (11 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 93 | `Dockerfile` | **MODIFY** | Multi-stage build (build → distroless/scratch); non-root user; EXPOSE 8080 |
| 94 | `Dockerfile.worker` | **MODIFY** | Multi-stage build; non-root user |
| 95 | `docker-compose.email.yml` | **MODIFY** | Final port alignment; healthcheck using `/health/ready`; depends_on redis with condition |
| 96 | `.github/workflows/email-server-ci.yml` | **CREATE** | CI: `go build ./...`, `go vet ./...`, `go test ./...`, lint (golangci-lint) |
| 97 | `Makefile` | **MODIFY** | Add `make docker-build`, `make docker-push`, `make compose-up`, `make compose-down` |
| 98 | `internal/config/config.go` | **MODIFY** | Add production validation: panic if `APP_ENV=production` and `CORS_ALLOWED_ORIGINS` empty |
| 99 | `internal/config/config.go` | **MODIFY** | Add production validation: panic if `APP_ENV=production` and `MAILTESTER_BASE_URL` empty |
| 100 | `template.yaml` | **MODIFY** | Document as Lambda-fallback-only; add comment block; or delete if EC2-only strategy confirmed |
| 101 | `docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md` | **MODIFY** | Add `contact360.io/emailapigo` section with all 16 routes + port 8080 |
| 102 | `docs/backend/postman/EC2_email.server.postman_collection.json` | **MODIFY** | Ensure all 16 Go routes present; add predict endpoints; fix port to 8080 |
| 103 | `docs/backend/endpoints/emailapis_endpoint_era_matrix.md` | **MODIFY** | Mark all Era 0–7 email.server routes as `go_implemented` |

---

### Era 8 — Public / private APIs (7 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 104 | `internal/api/router.go` | **MODIFY** | Add `/v1/` prefix group for all routes; keep un-prefixed aliases with deprecation header |
| 105 | `internal/api/router.go` | **MODIFY** | Add `Deprecation` + `Sunset` headers on un-prefixed aliases |
| 106 | `internal/schemas/responses.go` | **MODIFY** | Add `APIVersion string` to all responses (`v1`) |
| 107 | `internal/errors/errors.go` | **MODIFY** | Finalize standard error envelope: `{ "error": { "code", "message", "request_id", "docs_url" } }` |
| 108 | `docs/api.md` | **MODIFY** | Document versioned routes, auth requirements, error envelope, status code table |
| 109 | `docs/backend/postman/EC2_email.server.postman_collection.json` | **MODIFY** | Add `/v1/` prefix variants to collection; add `X-Request-ID` header to all requests |
| 110 | `docs/backend/apis/00_SERVICE_MESH_CONTRACTS.md` | **MODIFY** | Update `LambdaEmailClient` section: canonical port 8080, `/v1/` prefix, X-Request-ID contract |

---

### Era 9 — Ecosystem integrations (7 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 111 | `internal/middleware/tenant.go` | **CREATE** | `X-Tenant-ID` middleware: extract + validate; apply per-tenant rate limit bucket |
| 112 | `internal/api/router.go` | **MODIFY** | Register tenant middleware; apply per-tenant queue routing (high-priority vs standard queue) |
| 113 | `internal/config/config.go` | **MODIFY** | Add `TenantRateLimitsEnabled bool`, `DefaultRateLimitPerMinute int` |
| 114 | `internal/utils/cache_metrics.go` | **MODIFY** | Add per-tenant operation counters |
| 115 | `internal/worker/server.go` | **MODIFY** | Add `priority` Asynq queue for VIP tenants |
| 116 | `cmd/worker/main.go` | **MODIFY** | Start `priority` queue server alongside existing 4 |
| 117 | `docs/codebases/emailapis-codebase-analysis.md` | **MODIFY** | Update Era 9 status |

---

### Era 10 — Email campaign (7 files)

| # | File | Action | Description |
|---|------|--------|-------------|
| 118 | `internal/schemas/requests.go` | **MODIFY** | Add `CampaignID *string` to `BulkEmailVerifierRequest` and `S3CSVVerifyRequest` |
| 119 | `internal/tasks/types.go` | **MODIFY** | Add `CampaignID *string` to `EmailVerifyPayload` and `S3CSVVerifyPayload` |
| 120 | `internal/worker/mailtester_worker.go` | **MODIFY** | Write `campaign_id` into result JSON stored in Redis; update `emailapi_jobs` row with campaign_id |
| 121 | `db/migrations/006_emailapi_jobs_campaign.sql` | **CREATE** | Add `campaign_id` column + index on `emailapi_jobs`; add `compliance_lock bool` column |
| 122 | `internal/api/router.go` | **MODIFY** | Add `GET /email/campaign/:campaign_id/verify-summary` → aggregated verify stats per campaign |
| 123 | `internal/services/email_verification_service.go` | **MODIFY** | Add `CampaignVerifySummary(ctx, campaignID)` — count valid/invalid/unknown; return go/no-go |
| 124 | `docs/codebases/emailapis-codebase-analysis.md` | **MODIFY** | Update Era 10 status; add campaign evidence lineage section |

---

## Summary counts

| Era | Files |
|-----|-------|
| 0 — Foundation | 21 |
| 1 — User/billing | 8 |
| 2 — Email system | 28 |
| 3 — Contact/company | 8 |
| 4 — Extension/SN | 5 |
| 5 — AI workflows | 7 |
| 6 — Reliability | 15 |
| 7 — Deployment | 11 |
| 8 — Public APIs | 7 |
| 9 — Ecosystem | 7 |
| 10 — Email campaign | 8 |
| **Total** | **125** |

> Adjusted to 125 (+4 from Era 10 campaign migration file) vs the original 121 target. Reduce by combining Era 0 items 19+20 and Era 3 items 63+64 and Era 10 items 122+123 into shared files to hit exactly 121 if required.

---

## Dependency tracking: how email.server connects to the project

```
contact360.io/api  (Python gateway)
  └── LambdaEmailClient → LAMBDA_EMAIL_API_URL → EC2/email.server
        ├── PostgreSQL (shared contact360 DB cluster)
        │     ├── email_patterns
        │     ├── email_finder_cache
        │     └── emailapi_jobs
        ├── Redis (shared or dedicated)
        │     └── Asynq queues + job result hashes
        ├── EC2/sync.server (contact360.io/sync)
        │     └── POST /contacts (Connectra candidate lookup)
        ├── EC2/log.server (logsapi)
        │     └── POST /logs/batch (BatchLogHandler)
        ├── External: Mailtester.ninja, Mailvetter, Truelist, IcyPeas
        ├── External: AWS S3 (CSV input/output)
        └── External: OpenAI + DuckDuckGo (web-search)
```

### Gateway → email.server endpoint map

| Gateway GraphQL operation | email.server HTTP path |
|--------------------------|------------------------|
| `FindEmail` | `POST /email/finder/` |
| `BulkFindEmails` | `POST /email/finder/bulk` |
| `CreateBulkFindJob` | `POST /email/finder/bulk/job` |
| `VerifyEmail` | `POST /email/single/verifier/` |
| `BulkVerifyEmails` | `POST /email/bulk/verifier/` |
| `CreateBulkVerifyJob` | `POST /email/bulk/verifier/job` |
| `VerifyEmailsFromS3` | `POST /email/verify/s3` |
| `FindEmailsFromS3` | `POST /email/finder/s3` |
| `GetJobStatus` | `GET /jobs/:id/status` |
| `ListJobs` | `GET /jobs` |
| `AddEmailPattern` | `POST /email-patterns/add` |
| `AddEmailPatternBulk` | `POST /email-patterns/add/bulk` |
| `PredictEmailPattern` *(missing)* | `POST /email-patterns/predict` ← **must wire** |
| `PredictEmailPatternBulk` *(missing)* | `POST /email-patterns/predict/bulk` ← **must wire** |
| `WebSearchEmail` | `POST /web/web-search` |

### Postman collections covering email.server

- `docs/backend/postman/EC2_email.server.postman_collection.json` — primary
- `docs/backend/postman/Email API Service.postman_collection.json` — legacy (Python paths)
- `docs/backend/postman/15_Email_Module.postman_collection.json` — gateway-level email GraphQL

### Database docs

- `docs/backend/database/` — `email_patterns`, `email_finder_cache` schemas
- `emailapi_jobs` DDL: **not yet in docs** — create via migration `001_emailapi_jobs.sql` (Era 0, task #8)

### Tech docs

- `docs/tech/tech-go-gin-checklist-100.md`
- `docs/tech/tech-go-gin-why-practices.md`

### Endpoint matrices

- `docs/backend/endpoints/emailapis_endpoint_era_matrix.md`
- `docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md` — needs email.server section added (Era 7, task #101)

### Flowchart

- `docs/docs/flowchart.md` — **emailapigo finder fallback** diagram section; **Mailvetter bulk/single** section
