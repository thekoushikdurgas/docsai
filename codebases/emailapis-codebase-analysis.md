# emailapigo / EC2/email.server — Codebase Deep Analysis (Contact360 eras 0.x–10.x)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

---

## Service summary

`EC2/email.server` (`github.com/ayan/emailapigo`) is the **canonical Go runtime** for Contact360's email operations: email finding, verification, pattern management, and web-search fallback. It is a **Gin HTTP API + Asynq/Redis worker pool** backed by PostgreSQL (GORM) and AWS S3 for large CSV batch flows.

It is the Go counterpart to the retired `lambda/emailapis` Python FastAPI service and feeds the `contact360.io/api` (Python Strawberry GraphQL gateway) via `LambdaEmailClient` → `LAMBDA_EMAIL_API_URL`.

---

## Runtime architecture

```
contact360.io/api (Python FastAPI + Strawberry GraphQL)
        │  HTTP + X-API-Key (LambdaEmailClient)
        ▼
EC2/email.server  (Go, Gin, port 3000/8080 per .env)
  ├── internal/api/router.go         (HTTP routes)
  ├── internal/services/             (finder, verifier, pattern, S3CSV, web-search)
  ├── internal/clients/              (Mailtester, Mailvetter, Connectra, Truelist, IcyPeas, OpenAI, DuckDuckGo)
  ├── internal/repositories/         (email_patterns, email_finder_cache — PostgreSQL/GORM)
  ├── internal/models/               (Job, EmailPattern, EmailFinderCache)
  ├── internal/tasks/ + worker/      (Asynq queues: mailtester, mailvetter, email_finder, default)
  └── internal/logging/              (batch logger → logs API Gateway)

cmd/worker/main.go  →  4 asynq.Server instances (Redis)
        ├── queue:mailtester    concurrency=5
        ├── queue:mailvetter    concurrency=1
        ├── queue:email_finder  concurrency=4
        └── queue:default       concurrency=1
```

---

## All source files (45 files total)

### Top-level
| File | Role |
|------|------|
| `main.go` | Boot: godotenv → InitDB → SetupRouter → Lambda or http.Server on PORT |
| `go.mod` | Module `github.com/ayan/emailapigo`, Go 1.24 |
| `Dockerfile` | Builds `./main.go` → `/app/email-api`, exposes 3000 |
| `Dockerfile.worker` | Builds `./cmd/worker/main.go` → `/app/email-worker` |
| `docker-compose.yml` | Redis + api + worker |
| `docker-compose.email.yml` | API port 8080:8080, worker Dockerfile.worker |
| `Makefile` | Build/run helpers |
| `template.yaml` | AWS SAM (Lambda+API Gateway fallback path) |
| `.env.example` | All env vars documented |

### `cmd/worker/`
| File | Role |
|------|------|
| `cmd/worker/main.go` | Starts 4 asynq.Server instances; shared ServeMux |

### `internal/api/`
| File | Role |
|------|------|
| `internal/api/router.go` | All 16 HTTP routes; service/client wiring |

### `internal/clients/`
| File | Role |
|------|------|
| `internal/clients/connectra_client.go` | POST to Connectra `/contacts` |
| `internal/clients/database.go` | GORM Postgres init + AutoMigrate gate |
| `internal/clients/duckduckgo_client.go` | HTML scrape `https://html.duckduckgo.com/html/` |
| `internal/clients/icypeas_client.go` | POST `/email-search`, `/bulk-single-searchs/read` |
| `internal/clients/mailtester.go` | GET `{MAILTESTER_BASE_URL}/ninja?email&key` |
| `internal/clients/mailvetter_client.go` | GET `{MAILVETTER_BASE_URL}/verify?email` + Bearer |
| `internal/clients/openai_client.go` | POST `https://api.openai.com/v1/chat/completions` |
| `internal/clients/truelist_client.go` | POST `{TRUELIST_BASE_URL}/api/v1/verify_inline?email` |

### `internal/config/`
| File | Role |
|------|------|
| `internal/config/config.go` | Singleton Config; caarlos0/env; 30 env vars |

### `internal/email_patterns/`
| File | Role |
|------|------|
| `internal/email_patterns/detector.go` | Pattern type detection |
| `internal/email_patterns/patterns.go` | Pattern name pieces |
| `internal/email_patterns/renderer.go` | Pattern string renderer |
| `internal/email_patterns/tokens.go` | Tokenizer for names/patterns |

### `internal/errors/`
| File | Role |
|------|------|
| `internal/errors/errors.go` | Domain errors + HTTPStatus mapper |

### `internal/logging/`
| File | Role |
|------|------|
| `internal/logging/batch_logger.go` | BatchLogHandler; forwards to logs API Gateway |
| `internal/logging/logger.go` | ServiceLogger wrapper |

### `internal/middleware/`
| File | Role |
|------|------|
| `internal/middleware/auth.go` | APIKeyMiddleware: header X-API-Key |
| `internal/middleware/monitoring.go` | MonitoringMiddleware: duration metrics |

### `internal/models/`
| File | Role |
|------|------|
| `internal/models/email_finder_cache.go` | GORM model → table `email_finder_cache` |
| `internal/models/email_pattern.go` | GORM model → table `email_patterns` |
| `internal/models/job.go` | Plain struct → table `emailapi_jobs` (raw SQL) |

### `internal/repositories/`
| File | Role |
|------|------|
| `internal/repositories/email_finder_cache_repository.go` | Upsert/lookup cache; ON CONFLICT composite |
| `internal/repositories/email_pattern_repository.go` | CRUD + search for patterns |

### `internal/schemas/`
| File | Role |
|------|------|
| `internal/schemas/requests.go` | 15 request structs (finder, verifier, pattern, S3CSV, web-search) |
| `internal/schemas/responses.go` | 14 response structs + EmailVerificationStatus enum |

### `internal/services/`
| File | Role |
|------|------|
| `internal/services/email_finder_service.go` | Finder orchestration: cache → Connectra → pattern → generate → race-verify |
| `internal/services/email_generation_service.go` | Thin wrapper: generate email candidates |
| `internal/services/email_pattern_service.go` | Pattern add/bulk/predict logic |
| `internal/services/email_verification_service.go` | VerifySingle + VerifyParallel (5 concurrent, ~1.1s stagger) |
| `internal/services/s3csv_service.go` | Stream S3 CSV → enqueue rows; merge results → S3 |
| `internal/services/web_search_service.go` | DuckDuckGo scrape + OpenAI extraction |

### `internal/tasks/`
| File | Role |
|------|------|
| `internal/tasks/queues.go` | Queue name constants |
| `internal/tasks/types.go` | Task payload structs (EmailVerify, S3CSVVerify, EmailFind, S3CSVFind) |

### `internal/utils/`
| File | Role |
|------|------|
| `internal/utils/cache_metrics.go` | In-process CacheMetrics (response time, hits, misses) |
| `internal/utils/domain.go` | Domain normalisation helpers |
| `internal/utils/email_generator.go` | Email candidate generator (prefix patterns) |
| `internal/utils/logger.go` | slog helper |
| `internal/utils/unmask_email.go` | Unmask obfuscated email strings |

### `internal/worker/`
| File | Role |
|------|------|
| `internal/worker/email_finder_worker.go` | Asynq task: email:find → finderSvc + store result in Redis hash |
| `internal/worker/generic_worker.go` | Generic verify worker (mailvetter path) |
| `internal/worker/mailtester_worker.go` | Asynq task: email:verify:mailtester → Mailtester + DB update |
| `internal/worker/s3csv_finder_worker.go` | Asynq task: email:s3csv:find → per-row finder |
| `internal/worker/s3csv_worker.go` | Asynq task: email:s3csv:verify:mailtester → per-row verify |
| `internal/worker/server.go` | Queue constants + RegisterVerifyHandlers + RegisterFinderHandlers |

---

## HTTP routes (complete)

All auth-protected routes require **`X-API-Key`** header matching `API_KEY`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | Public | Diagnostics (all integrations configured?) |
| GET | `/` | Public | Service info |
| GET | `/metrics` | Public | Cache hit/miss, response time |
| GET | `/jobs` | ✅ | List 50 most recent emailapi_jobs |
| POST | `/email/finder/` | ✅ | Single email find (query params: first_name, last_name, domain) |
| POST | `/email/finder/bulk` | ✅ | Bulk email find (JSON body); semaphore 15 goroutines |
| POST | `/email/finder/bulk/job` | ✅ | Enqueue bulk find to Asynq; returns job_id |
| POST | `/email/single/verifier/` | ✅ | Single email verify (JSON body; provider field) |
| POST | `/email/bulk/verifier/` | ✅ | Parallel bulk verify (5 concurrent, 1.1s stagger) |
| POST | `/email/bulk/verifier/job` | ✅ | Enqueue bulk verify to Asynq; returns job_id |
| POST | `/email/verify/s3` | ✅ | Stream S3 CSV → verify per row (background goroutine) |
| POST | `/email/finder/s3` | ✅ | Stream S3 CSV → find per row (background goroutine) |
| POST | `/web/web-search` | ✅ | DuckDuckGo + OpenAI email discovery |
| GET | `/jobs/:id/status` | ✅ | Job progress: PG + Redis hash polling |
| POST | `/email-patterns/add` | ✅ | Add single email pattern (email or pattern_format) |
| POST | `/email-patterns/add/bulk` | ✅ | Add batch email patterns |

**Missing vs docs contract (gaps):**
- `POST /email-patterns/predict` — in requests.go but no route registered → ⬜ TODO
- `POST /email-patterns/predict/bulk` — in requests.go but no route registered → ⬜ TODO
- `POST /email/single/verifier/find` (SingleEmailVerifierFindResponse) — response type exists, no route → ⬜ TODO
- `/health/db`, `/health/ready`, `/health/live` — not present; only `/health` → 🟡 partial

---

## Asynq worker pool

| Queue | Concurrency | Task type | Handler |
|-------|-------------|-----------|---------|
| `mailtester` | 5 | `email:verify:mailtester` | MailtesterWorker |
| `mailtester` | 5 | `email:s3csv:verify:mailtester` | S3CSVWorker |
| `mailvetter` | 1 | `email:verify:mailvetter` | GenericVerifyWorker |
| `email_finder` | 4 | `email:find` | EmailFinderWorker |
| `email_finder` | 4 | `email:s3csv:find` | S3CSVFinderWorker |
| `default` | 1 | (unused) | — |

---

## Database tables

| Table | Engine | Notes |
|-------|--------|-------|
| `email_finder_cache` | GORM model | Composite key `(first_name, last_name, domain)`; ON CONFLICT upsert |
| `email_patterns` | GORM model | AutoMigrate in `development` ENV only |
| `emailapi_jobs` | Raw SQL (GORM Exec/Raw) | NOT a GORM model; no AutoMigrate; must be created by migration |

**Critical gap:** `emailapi_jobs` table has **no migration file** in this repo. Rows are inserted/updated with raw SQL but the table DDL is absent — must exist in `contact360.io/api` or a shared migrations folder.

---

## Redis key schema

| Key pattern | Type | TTL | Usage |
|-------------|------|-----|-------|
| `job:{id}:total` | string (int) | 1h (verify), 24h (S3) | Expected row count for completion check |
| `job:{id}` | hash | indefinite | email → JSON result (bulk verifier / finder) |
| `job:{id}:rows` | hash | indefinite | row_index → JSON result (S3 CSV verify / find) |

---

## External service dependencies

| Service | Env var | Endpoint | Notes |
|---------|---------|----------|-------|
| **Mailtester.ninja** | `MAILTESTER_BASE_URL`, `MAILTESTER_API_KEY` | `GET /ninja?email&key` | Primary verifier; fallback to Mailvetter on "Limited" |
| **Mailvetter** | `MAILVETTER_API_KEY`, `MAILVETTER_BASE_URL` | `GET /verify?email` + Bearer | Fallback verifier; bulk concurrency=1 |
| **Truelist** | `TRUELIST_API_KEY`, `TRUELIST_BASE_URL` | `POST /api/v1/verify_inline?email` | Secondary verifier |
| **IcyPeas** | `ICYPEAS_API_KEY`, `ICYPEAS_BASE_URL` | `POST /email-search` | Email finder provider |
| **Connectra (sync.server)** | `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY` | `POST /contacts` | Candidate lookup in finder |
| **OpenAI** | `OPENAI_API_KEY`, `OPENAI_MODEL` | `POST /v1/chat/completions` | Email extraction from web search |
| **DuckDuckGo** | `PROXY_ADDR` | `POST https://html.duckduckgo.com/html/` | Web search HTML scrape |
| **AWS S3** | `S3_BUCKET_NAME`, AWS SDK v2 | S3 get/put | CSV stream input/output |
| **Logs API** | Hardcoded URL in `batch_logger.go` | `POST .../logs/batch` | Batch log forwarding |
| **Redis** | `REDIS_ADDR` | `localhost:6379` default | Asynq queues + job result store |
| **PostgreSQL** | `DATABASE_URL` | GORM Postgres driver | email_patterns, email_finder_cache, emailapi_jobs |

---

## Known bugs and issues

1. **Port mismatch:** `config.go` defaults to `PORT=3000`, but `docker-compose.email.yml` maps `8080:8080`. The container listens on `:3000` while Docker exposes `:8080` → HTTP 000 on probes. → **Fix: align `PORT=8080` in `.env`/compose**.
2. **`emailapi_jobs` DDL missing:** No CREATE TABLE in repo; service panics or silently corrupts if table absent.
3. **`MAILVETTER_BASE_URL` default typo:** `mailvaiter.com` (not `mailvetter`); must be overridden in production.
4. **`/email/bulk/verifier/job` queue selection bug:** only `mailtester` or `mailvetter`; `mailvetter` task type registered in `server.go` but `TypeEmailVerify+":mailvetter"` uses `GenericVerifyWorker` — confirm behavior parity with mailtester worker.
5. **No test files:** zero `*_test.go` files — no unit, integration, or regression coverage.
6. **`GET /jobs/:id/status` registered inside `webGroup` block but on `authGroup`** — code style inconsistency (works at runtime but confusing).
7. **Batch logger URL hardcoded:** `https://c2cox8ij6c.execute-api.us-east-1.amazonaws.com/logs/batch` — should come from `LAMBDA_LOGS_API_URL` env var like other services use.
8. **`WorkerConcurrency` config field missing:** `router.go` uses `cfg.WorkerConcurrency` but it is NOT in `config.go` → compile error if referenced elsewhere. (Currently only used in extension.server; confirm email.server compile is clean.)

---

## Integration with contact360.io/api

The Python gateway calls email.server through `app/clients/lambda_email_client.py` using env var `LAMBDA_EMAIL_API_URL`. Relevant gateway GraphQL operations that delegate to email.server:

| Gateway mutation/query | Delegated path |
|------------------------|----------------|
| `FindEmail` | `POST /email/finder/` |
| `BulkFindEmails` | `POST /email/finder/bulk` |
| `VerifyEmail` | `POST /email/single/verifier/` |
| `BulkVerifyEmails` | `POST /email/bulk/verifier/` |
| `AddEmailPattern` | `POST /email-patterns/add` |
| `AddEmailPatternBulk` | `POST /email-patterns/add/bulk` |
| Job status polling | `GET /jobs/:id/status` |
| S3 CSV verify | `POST /email/verify/s3` |
| S3 CSV find | `POST /email/finder/s3` |

---

## Completion status from runtime

- [x] ✅ Go API server boots, CORS, gzip, API key middleware working.
- [x] ✅ Email finder (single + bulk + job) routes implemented.
- [x] ✅ Email verifier (single + bulk + job) routes implemented.
- [x] ✅ Email pattern add (single + bulk) routes implemented.
- [x] ✅ S3 CSV finder and verifier routes implemented (background streaming).
- [x] ✅ Asynq worker pool for all 4 queues is working.
- [x] ✅ Redis job result store with hash per job_id.
- [x] ✅ Finder flow: cache → Connectra → pattern → generate → race-verify.
- [x] ✅ Web search route (DuckDuckGo + OpenAI) implemented.
- [x] ✅ Batch logging forwarding to logs API.
- [ ] 🟡 In Progress: port mismatch (3000 vs 8080) causing Docker probe failures.
- [ ] ⬜ Incomplete: `emailapi_jobs` table DDL not in repo.
- [ ] ⬜ Incomplete: `/email-patterns/predict` and `/email-patterns/predict/bulk` routes not wired.
- [ ] ⬜ Incomplete: liveness/readiness health probes (`/health/live`, `/health/ready`, `/health/db`) absent.
- [ ] ⬜ Incomplete: zero test coverage.
- [ ] ⬜ Incomplete: batch logger URL hardcoded.
- [ ] ⬜ Incomplete: status vocabulary (`valid|invalid|catchall|unknown|risky`) not frozen.

---

## Active risks

| Risk | Severity | Status |
|------|----------|--------|
| Port 3000 vs 8080 mismatch → Docker broken | P0 | ⬜ |
| `emailapi_jobs` DDL missing → runtime SQL failure | P0 | ⬜ |
| Mailvetter base URL typo `mailvaiter.com` | P0 | ⬜ |
| No tests — regressions invisible | P1 | ⬜ |
| Batch logger URL hardcoded vs env | P1 | ⬜ |
| Provider contract (`mailvetter` vs `truelist`) not frozen | P1 | 🟡 |
| Status vocab not canonical across gateway/emailapigo | P1 | ⬜ |
| Predict endpoints (schema exists, route missing) | P2 | ⬜ |
| CORS wildcard possible if `CORS_ALLOWED_ORIGINS` unset | P2 | 🟡 |

---

## Era-by-era completion map (0.x–10.x)

### `0.x.x — Foundation`
- [x] ✅ Go Gin scaffold, config, CORS, API key, health, logging bootstrap.
- [x] ✅ GORM DB init, email_patterns + email_finder_cache AutoMigrate.
- [ ] ⬜ Fix port mismatch (`PORT=3000` default → should be `8080`).
- [ ] ⬜ Add `emailapi_jobs` migration SQL file to repo.
- [ ] ⬜ Move batch logger URL to env var.
- [ ] ⬜ Add `/health/live`, `/health/ready`, `/health/db` endpoints.
- [ ] ⬜ Add `WorkerConcurrency` to config struct.
- [ ] ⬜ Fix Mailvetter base URL default typo.

### `1.x.x — User / billing / credit`
- [ ] 🟡 Credit-impact fields (`user_id`, `tenant_id`) on all email operation responses.
- [ ] ⬜ Propagate `X-User-ID` header from gateway to email.server; log per-user operations.
- [ ] ⬜ Enforce per-user credit deduction lineage on finder/verifier paths.

### `2.x.x — Email system`
- [x] ✅ Core finder/verifier/pattern endpoints live.
- [x] ✅ Bulk endpoints with semaphore concurrency.
- [x] ✅ Job-based async bulk (Asynq + Redis hash).
- [x] ✅ S3 CSV stream verify + find.
- [ ] ⬜ Wire `/email-patterns/predict` and `/email-patterns/predict/bulk` routes.
- [ ] ⬜ Freeze status vocabulary (`valid|invalid|catchall|unknown|risky`) in `responses.go`.
- [ ] ⬜ Align provider contract: `truelist` vs `mailvetter` → define priority order.
- [ ] ⬜ Add idempotency keys to bulk verify/find (prevent double-enqueue).
- [ ] ⬜ Add replay-safe bulk handler (dedup by job_id + index).
- [ ] ⬜ Ensure `email:s3csv:verify:mailvetter` task type registered (only mailtester currently).

### `3.x.x — Contact / company data`
- [ ] 🟡 Connectra integration in finder tested end-to-end.
- [ ] ⬜ Candidate merge strategy documented for when Connectra returns multiple contacts.
- [ ] ⬜ Add lineage fields (`source`, `request_id`) to `email_finder_cache` rows.

### `4.x.x — Extension / Sales Navigator`
- [ ] 📌 Extension-origin email requests should carry `source: extension` metadata.
- [ ] ⬜ Define extension-safe retry contract for `/email/finder/` calls from background.js.

### `5.x.x — AI workflows`
- [ ] 🟡 OpenAI client wired for web-search email extraction.
- [ ] ⬜ Add structured confidence/scoring to AI-assisted email discovery results.
- [ ] ⬜ Add safe logging redaction for AI context fields (PII minimisation).
- [ ] 📌 Define AI fallback policy when OpenAI is unavailable.

### `6.x.x — Reliability / scaling`
- [ ] ⬜ Add circuit breaker for each external provider (Mailtester, Mailvetter, Truelist, IcyPeas).
- [ ] ⬜ Unified provider degradation strategy (fallback chain, backoff, dead-letter).
- [ ] ⬜ Add SLO metrics: bulk success rate, per-provider latency p50/p95.
- [ ] ⬜ Add `/metrics` Prometheus exporter (replace in-process CacheMetrics only approach).
- [ ] ⬜ Redis connection pool sizing and backpressure controls.
- [ ] ⬜ Add `MaxRetry` per-provider config (currently hardcoded `3`).

### `7.x.x — Deployment`
- [ ] ⬜ Fix Docker port mismatch — `PORT=8080` in `.env.example` + compose.
- [ ] ⬜ `go build ./...` CI gate in Makefile / GitHub Actions.
- [ ] ⬜ Add `CORS_ALLOWED_ORIGINS` required-in-production validation.
- [ ] ⬜ Add readiness probe path (`/health/ready`) checking Redis + DB + S3 connectivity.
- [ ] ⬜ Add `emailapi_jobs` DDL to `db/` migrations folder.
- [ ] ⬜ Remove stale `template.yaml` / SAM references or clearly document Lambda-fallback intent.

### `8.x.x — Public/private APIs`
- [ ] ⬜ Version prefix `/v1/` on all routes (currently flat paths).
- [ ] ⬜ Freeze external contract; publish breaking-change policy.
- [ ] ⬜ Partner-safe error envelope (no stack traces; standard `{ "error": { "code", "message" } }`).
- [ ] 📌 Publish Postman collection `EC2_email.server.postman_collection.json` aligned with Go routes.

### `9.x.x — Ecosystem integrations`
- [ ] 📌 Tenant-aware throttling (`X-Tenant-ID` on queues).
- [ ] ⬜ Cross-service trace correlation (`X-Request-ID`, `X-Trace-ID` propagation).
- [ ] 📌 Partner usage quotas for bulk finder/verifier.

### `10.x.x — Email campaign`
- [ ] 📌 Campaign-triggered bulk verify path with immutable result storage.
- [ ] ⬜ Campaign compliance lineage: retain verification evidence per campaign_id.
- [ ] 📌 Campaign release gate: block send if bulk verify success rate < threshold.

---

## Immediate execution queue (P0 → P2)

### P0 — must fix before production readiness

- [ ] **FIX-1**: Set `PORT` default to `8080` in `config.go`; align `docker-compose.email.yml` and `.env.example`.
- [ ] **FIX-2**: Create `db/migrations/001_emailapi_jobs.sql` with `emailapi_jobs` DDL matching `router.go` raw SQL columns.
- [ ] **FIX-3**: Fix `MAILVETTER_BASE_URL` default from `mailvaiter.com` to correct host.
- [ ] **FIX-4**: Move `batch_logger.go` hardcoded logs API URL to `LAMBDA_LOGS_API_URL` env var.

### P1 — before Era 2.x sign-off

- [ ] **FIX-5**: Wire `/email-patterns/predict` route using existing `EmailPatternPredictRequest` and `EmailPatternPredictResponse`.
- [ ] **FIX-6**: Wire `/email-patterns/predict/bulk` route using existing `BulkEmailPatternPredictRequest`.
- [ ] **FIX-7**: Add `WorkerConcurrency int` to `config.Config` (avoids potential compile error in shared usage).
- [ ] **FIX-8**: Register `email:s3csv:verify:mailvetter` task type + handler for Mailvetter S3 CSV path parity.
- [ ] **FIX-9**: Freeze `EmailVerificationStatus` values as const block; add `risky` and `unknown` handling policy.
- [ ] **FIX-10**: Add `/health/db` (GORM ping) and `/health/ready` (Redis ping + DB ping) endpoints.

### P2 — before Era 6.x sign-off

- [ ] **FIX-11**: Add at least one `*_test.go` per service package (finder, verifier, pattern).
- [ ] **FIX-12**: Provider priority config: `PROVIDER_PRIMARY` / `PROVIDER_FALLBACK` env vars instead of hardcoded logic.
- [ ] **FIX-13**: Add `X-Request-ID` middleware; propagate to all provider HTTP calls and Redis writes.
- [ ] **FIX-14**: Add Prometheus `/metrics` with `email_find_duration_ms_bucket`, `email_verify_duration_ms_bucket`.
- [ ] **FIX-15**: Validate `CORS_ALLOWED_ORIGINS` non-empty when `APP_ENV=production`.

---

## 2026 Gap Register

### P0
- [ ] `EMAILGO-0.1` Port + Docker compose fix (3000→8080).
- [ ] `EMAILGO-0.2` `emailapi_jobs` DDL migration.
- [ ] `EMAILGO-0.3` Mailvetter URL typo fix.
- [ ] `EMAILGO-0.4` Batch logger URL env var.

### P1/P2
- [ ] `EMAILGO-2.1` Predict endpoint routes.
- [ ] `EMAILGO-2.2` Bulk idempotency keys.
- [ ] `EMAILGO-2.3` Status vocabulary freeze.
- [ ] `EMAILGO-2.4` Provider fallback chain config.
- [ ] `EMAILGO-6.1` Circuit breaker per provider.
- [ ] `EMAILGO-6.2` SLO metrics (Prometheus).
- [ ] `EMAILGO-7.1` Readiness/liveness probes.
- [ ] `EMAILGO-7.2` CI build gate.

### P3+
- [ ] `EMAILGO-8.1` API versioning `/v1/`.
- [ ] `EMAILGO-9.1` Trace correlation headers.
- [ ] `EMAILGO-10.1` Campaign verification evidence lineage.
