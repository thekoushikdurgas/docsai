# Codebase analysis content retrieval
_Exported on 3/25/2026 at 01:54:47 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their content (first 60 lines of each):
1. d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md
2. d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md
3. d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md
4. d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md
5. d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md
6. d:\code\ayan\contact\docs\codebases\emailcampaign-codebase-analysis.md
7. d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md

Return the raw content focusing on: gaps/risks sections, era mapping sections, immediate execution queues.

---

**Cursor**


Reading the first 60 lines of each file in parallel.




Searching for "gap", "risk", "era", and "queue" section headers — the first 60 lines often omit dedicated gaps/risks blocks.




Noting the first 60 lines omit most dedicated "Gaps and risks", "Era mapping", and "Immediate execution queue" sections (they appear later). Reading those sections for each file.




Fetching the remainder of s3storage's era mapping (sections 3.x–10.x).




Here is a concise report. **Important:** In most of these docs, the titled **Gaps and risks**, **Era mapping**, and **Immediate execution queue** blocks start **after line 60**. What appears in lines 1–60 is mostly purpose, stack, and architecture; only a few queue/era/gap hints show up early (called out below). Below are **lines 1–60 verbatim** (from the files), then the **dedicated focus sections** copied from later in each file.

---

### Where the “focus” sections live (line anchors)

| File | Gaps / risks | Era mapping | Immediate execution queue |
|------|----------------|-------------|---------------------------|
| `d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md` | § ~192 | § ~207 | § ~225 |
| `d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md` | § ~66 | § ~73 | § ~89 |
| `d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md` | § ~83 | § ~125–360 | § ~361 |
| `d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md` | § ~85 | § ~93–170 | **No section with this title** |
| `d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md` | § ~133 | § ~147 | § ~165 |
| `d:\code\ayan\contact\docs\codebases\emailcampaign-codebase-analysis.md` | § ~77 (queue notes § ~55–58) | § ~93 | § ~109 |
| `d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md` | § ~237 | § ~273–351 | **§ ~354 “Engineering queue (prioritized)”** (same role) |

**In lines 1–60 only:** Connectra mentions downstream eras (`4.x`–`10.x`) and describes the **job engine** (`first_time` / `retry`, 1000-buffer channel). Mailvetter: **Redis list `tasks:verify`**. Email campaign: **`10.x` runtime** and **§ Queue architecture** (Asynq `campaign:send`, legacy Redis list). Sales Navigator: **Era relevance `4.x`**, **Era task-pack index**, and **rate limiting none** / **CORS `*`** as gaps. S3 doc line 3 mentions **0.x.x–10.x.x** execution breakdown.

---

### 1) `appointment360-codebase-analysis.md` — lines 1–60

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
```

**Gaps and risks / Era mapping / Immediate execution queue** (from later in the same file): see the blocks I quoted in the unified section at the end of this message for Appointment360 (table + 7 numbered queue items).

---

### 2) `connectra-codebase-analysis.md` — lines 1–60

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
```

---

### 3) `s3storage-codebase-analysis.md` — lines 1–60

```markdown
# Contact360 `lambda/s3storage` Codebase Analysis and Task Decomposition

This document is a deep analysis of the `lambda/s3storage` service in Contact360 and a version-aligned execution breakdown across `0.x.x` to `10.x.x`.

## Purpose and role in Contact360

`s3storage` is the storage control plane for Contact360 file artifacts. It provides:

- bucket namespace initialization
- file upload/download/list/delete APIs
- multipart upload orchestration for large CSV files
- CSV schema/preview/stats analysis
- asynchronous metadata extraction and `metadata.json` maintenance
- avatar/photo/resume storage paths

This service directly supports product flows in dashboard, API gateway, jobs, extension, and future campaign/integration systems.

## Current architecture snapshot

## Service and API layer

- Entrypoint: `lambda/s3storage/app/main.py`
- Framework: FastAPI + Mangum (Lambda adapter)
- Router: `lambda/s3storage/app/api/v1/router.py`
- Endpoint groups:
  - `health`
  - `buckets`
  - `files`
  - `uploads`
  - `analysis` (schema/preview/stats/metadata)
  - `avatars`

## Backend abstraction

- Service facade: `lambda/s3storage/app/services/storage_service.py`
- Concrete backends: `lambda/s3storage/app/services/storage_backends.py`
  - `S3Backend`
  - `FilesystemBackend`
- Config selector:
  - `S3STORAGE_STORAGE_BACKEND=s3|filesystem`
  - loaded through `lambda/s3storage/app/core/config.py`

## Data and key model

Logical bucket model is prefix-based in a single S3 bucket:

- `{bucket_id}/avatar/`
- `{bucket_id}/upload/`
- `{bucket_id}/photo/`
- `{bucket_id}/export/`
- `{bucket_id}/metadata.json`

This model is aligned with Contact360 multi-surface file usage and downstream ingestion.

## Async metadata pipeline

- Upload complete triggers worker lambda invocation:
  - `s3storage-metadata-worker`
- Worker handler:
  - `lambda/s3storage/app/utils/worker.py`
```

---

### 4) `jobs-codebase-analysis.md` — lines 1–60

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
```

---

### 5) `mailvetter-codebase-analysis.md` — lines 1–60

```markdown
# Mailvetter Codebase Analysis (`backend(dev)/mailvetter`)

## Purpose and role

`backend(dev)/mailvetter` is Contact360's deep email-verification engine. It provides:

- single verification (`POST /v1/emails/validate`)
- async bulk verification (`POST /v1/emails/validate-bulk`)
- job tracking (`GET /v1/jobs/:job_id`)
- results export (`GET /v1/jobs/:job_id/results`)

It combines SMTP protocol probing, DNS/MX checks, catch-all disambiguation, Office365 false-positive correction, and OSINT proof signals (GitHub, Adobe, Gravatar, Google Calendar, optional HIBP).

---

## Technology stack

| Concern | Implementation |
| --- | --- |
| Language/runtime | Go 1.25 |
| HTTP API | Gin (`gin-gonic/gin`) |
| Data store | PostgreSQL via `pgx/v5/pgxpool` |
| Queue | Redis (`go-redis/v9`) |
| Workers | In-process worker pool binary (`cmd/worker`) |
| Proxy layer | Optional proxy rotation and SMTP proxying |
| Webhooks | HMAC-SHA256 signed callbacks on job completion/failure |
| Deployment | Docker (API + worker + Redis + Postgres + Caddy) |

---

## Architecture

### Runtime shape

- **API binary**: `cmd/api/main.go` + Gin router
- **Worker binary**: `cmd/worker/main.go` + queue consumer pool
- **Shared DB**: `jobs` and `results` tables in Postgres
- **Shared queue**: Redis list `tasks:verify`

### API route surface

V1 authenticated routes:

- `GET /v1/health`
- `POST /v1/emails/validate`
- `POST /v1/emails/validate-bulk`
- `GET /v1/jobs/:job_id`
- `GET /v1/jobs/:job_id/results`

Legacy routes (still enabled, auth-protected except `/info`):

- `GET /verify`
- `POST /upload`
- `GET /status`
- `GET /results`
- `GET /info`

### Validation pipeline

For each email, validator executes parallel signal probes:
```

---

### 6) `emailcampaign-codebase-analysis.md` — lines 1–60

```markdown
# Email Campaign Codebase Analysis (`backend(dev)/email campaign`)

## Purpose and role

`backend(dev)/email campaign` is Contact360's campaign delivery engine. It owns template management, asynchronous bulk email dispatch, SMTP-level send, per-recipient tracking, and unsubscribe/suppression enforcement. It is the `10.x` execution runtime that the planned campaign UI, wizard, and sequence engine will drive through the gateway.

## Current architecture snapshot

- **Runtime:** Go 1.24, Gin HTTP server, Asynq job queue, Redis.
- **Data:** PostgreSQL (`campaigns`, `recipients`, `suppression_list`, `templates`).
- **Storage:** AWS S3 (template HTML files; key `templates/{id}.html`).
- **Two binaries:** API server (`cmd/main.go`) + Asynq worker (`cmd/worker/main.go`).
- **Concurrency model:** 5 goroutines per campaign consume from a buffered channel; `sync.WaitGroup` joins all workers before marking status `completed`.

## Route surface

| Route | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Liveness probe |
| `/campaign` | POST | Enqueue campaign send job (template_id + name + filepath) |
| `/unsub` | GET | JWT-signed unsubscribe (sets suppression + updates recipient status) |
| `/list/mailbox` | GET | IMAP mailbox listing |
| `/list/inbox` | GET | IMAP inbox fetch (latest 10 messages) |
| `/body/:uid` | GET | IMAP fetch email body by UID |
| `/templates` | POST | Create template (upload HTML to S3, insert metadata to DB) |
| `/templates` | GET | List all templates |
| `/templates/:id` | GET | Get single template |
| `/templates/:id` | DELETE | Delete template (S3 + DB + cache invalidation) |
| `/templates/:id/preview` | POST | Render template with sample recipient data |

## Core mechanics

### Campaign send flow

1. `POST /campaign` → saves `campaigns` row, enqueues `campaign:send` task on Asynq/Redis.
2. Asynq worker picks up task → marks status `sending` → fetches template from S3.
3. CSV file loaded from path → goroutine filters suppressed emails → inserts `recipients` rows.
4. 5 concurrent `EmailWorker` goroutines consume recipient channel → render HTML from S3-backed template → SMTP send.
5. Per-recipient: success → `sent` status + `IncrementSent`; failure → `failed` status + `IncrementFailed`.
6. After all workers: campaign status → `completed`.

### Template system

- HTML template stored in S3 under `templates/{id}.html`.
- In-memory cache layer (`Service.cache`) with `sync.RWMutex`; cache miss fetches from S3.
- `RenderString` method supports Go template syntax in subject line (`{{.FirstName}}` etc.).
- `TemplateData` struct: `FirstName`, `LastName`, `Email`, `UnsubscribeURL`.

### Unsubscribe token

- JWT (HS256) signed with `JWT_SECRET`, 30-day expiry.
- Claims: `email`, `campaign_id`.
- `GET /unsub?token=...` validates → inserts `suppression_list` → updates `recipients.status = 'unsubscribed'`.

### Queue architecture

- Primary path: Asynq (built on Redis); task type `campaign:send`.
- Secondary path: Raw Redis list helper (`queue/reddis_queue.go`) — appears to be legacy/experimental parallel path.

## Data model
```

---

### 7) `salesnavigator-codebase-analysis.md` — lines 1–60

```markdown
# Sales Navigator Codebase Deep Analysis

**Service path:** `backend(dev)/salesnavigator/`  
**Runtime:** FastAPI on AWS Lambda (via Mangum adapter)  
**Language:** Python 3.11  
**Era relevance:** `4.x` (primary) — with influence from `0.x` setup through `10.x` campaign audience  
**Era task-pack index:** `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## 1. Stack and dependencies

| Component | Implementation |
| --- | --- |
| HTTP framework | FastAPI (async) |
| Lambda adapter | Mangum |
| HTTP client | `httpx` (async, connection pooling) |
| Retry logic | `tenacity` (exponential backoff, max 3 retries) |
| HTML parsing | BeautifulSoup4 (`html.parser`) |
| Data validation | Pydantic v2 (`pydantic-settings`) |
| Auth | `X-API-Key` header only (global service-to-service key) |
| Rate limiting | **None currently implemented** (noted as gap) |
| CORS | Wide-open (`*`) — service-to-service intent |
| Deployment | AWS SAM (`template.yaml`), 60s timeout, 1024 MB RAM |

---

## 2. Repository structure

```
backend(dev)/salesnavigator/
├── app/
│   ├── main.py                     # FastAPI app, Mangum handler, exception handlers
│   ├── api/
│   │   ├── dependencies.py         # verify_api_key (X-API-Key header)
│   │   ├── router.py               # mounts /v1 sub-router
│   │   └── v1/
│   │       ├── router.py           # mounts scrape + health routers
│   │       └── endpoints/
│   │       ├── scrape.py       # POST /v1/scrape, POST /v1/save-profiles
│   │       └── health.py       # GET /v1/health
│   ├── core/
│   │   ├── config.py               # Settings (API_KEY, CONNECTRA_API_URL, etc.)
│   │   └── exceptions.py           # ConnectraClientError hierarchy, ValidationError
│   ├── services/
│   │   ├── save_service.py         # SaveService + dedup + chunk/parallel logic
│   │   ├── mappers.py              # Profile → Contact/Company field mapping
│   │   └── sales_navigator/
│   │       ├── extraction.py       # HTML DOM extraction (lead cards, metadata)
│   │       ├── parsing.py          # URL/URN parsing (lead ID, company URL)
│   │       ├── utils.py            # UUID gen, name/location/seniority parsing
│   │       └── normalization.py    # Text normalization, PLACEHOLDER_VALUE sentinel
│   ├── clients/
│   │   └── connectra_client.py     # ConnectraClient + ConnectraClientPool (singleton)
│   └── schemas/
│       ├── requests.py             # SaveProfilesRequest, ScrapeHtmlRequest
│       └── responses.py            # SaveProfilesResponse, ScrapeHtmlResponse
├── tests/
│   ├── test_api.py
│   ├── test_save_service.py
```

---

## Focus sections (full text from the docs)

### Appointment360 — Gaps and risks; Era mapping; Immediate execution queue

**Gaps and risks** (table): ad-hoc debug file writes; `DOCSAI_ENABLED=False`; rate limit off by default; missing `sql/tables/`; no campaigns GraphQL yet; abuse guard in-memory; token blacklist DB-only; inline debug log path.

**Era mapping:** table `0.x`–`10.x` mapping gateway concerns (bootstrap through campaigns/sequences/templates for `10.x`).

**Immediate execution queue:** (1) remove debug writes (2) add `campaigns`/`sequences`/`campaignTemplates` GraphQL modules (3) enable rate limit in prod (4) restore/link SQL schema docs (5) Redis for idempotency/abuse guard (6) DocsAI health (7) contract parity tests vs `docs/backend/apis/*.md`.

### Connectra — Gaps and risks; Era mapping; Immediate execution queue

**Gaps:** in-memory queue durability; API key / rate-limit policy; `AllowAllOrigins`; ES/PG drift automation missing.

**Era mapping:** table `0.x`–`10.x` with “Connectra concern” + “Small-task decomposition” columns.

**Immediate execution queue:** persistent queue; ES–PG reconciliation; per-tenant rate limits + key scopes; VQL/filter contract tests; batch-upsert idempotency release gates.

### S3storage — Gaps; Era mapping; Immediate execution queue

**Gaps:** (1) multipart sessions in-memory (2) hardcoded worker function name (3) metadata RMW race (4) doc/contract drift (5) permissive CORS / auth upstream assumption.

**Era mapping:** `## Contact360 era mapping (`0.x.x` to `10.x.x`)` with per-era goals and Contract/Service/Surface/Data/Ops bullets from `0.x.x` through `10.x.x` (foundation through email campaign compliance artifacts).

**Immediate execution queue (high impact):** durable multipart store; env-driven worker name; concurrency-safe `metadata.json`; contract parity vs `docs/API.md`; E2E multipart + worker tests; failure-path tests; upload security checklist; SLO/dashboards.

### Jobs — Known gaps and risks; Era-by-era breakdown

**Gaps:** stale `processing` recovery; DAG degree-decrement failure blocking; single shared `X-API-Key`; retry semantics vs `failed`; legacy DAG patterns inactive.

**Era breakdown:** `0.x` foundation through `10.x` email campaign — each era lists Contract / Service / Surface / Data / Ops bullets.

**Immediate execution queue:** **not defined** as a titled list in this file.

### Mailvetter — Gaps and risks; Era mapping; Immediate execution queue

**Gaps** (table): V1+legacy dual surface; in-memory rate limiter; runtime migrations; webhook secret fallback; docs naming; legacy UI; no multi-tenant keys model.

**Era mapping:** table `0.x`–`10.x` (verifier as primary in `2.x`, campaign preflight in `10.x`).

**Immediate execution queue:** deprecate legacy / Redis limiter / migration pipeline / separate webhook secret / idempotency keys / status vocabulary / v1 parity tests.

### Email campaign — Queue (partial); Gaps; Era; Immediate queue

**Queue (from doc):** Asynq `campaign:send`; legacy Redis list in `queue/reddis_queue.go`.

**Gaps** (table): schema drift (`templates`, `unsub_token`); no auth; nil SMTP auth; `GetUnsubToken` bug; partial-failure status; dual queues; CSV-only audience; no open/click tracking; no warmup/rate-limit; CORS.

**Era mapping:** table `0.x`–`10.x` with small-task decomposition.

**Immediate execution queue:** fix `schema.sql`; fix `GetUnsubToken`; SMTP auth env; protect routes; `completed_with_errors`/`paused`; Connectra audience; log to `logs.api`.

### Sales Navigator — Known gaps and risks; Era breakdown; Engineering queue

**Gaps** (table): doc vs implementation drift (`scrape-html-with-fetch`); README vs `POST /v1/scrape`; global API key; no rate limit; CORS `*`; no request-ID; LinkedIn URL placeholder; null `employees_count`/`industries`; dead `extraction.py`; Connectra-only availability; no chunk idempotency.

**Era breakdown:** `0.x`–`10.x` sections with Contract/Service/Surface/Data/Ops (primary `4.x`).

**Engineering queue (prioritized):** P0 doc/README fixes; P1 request-ID, rate limit, CORS tighten, chunk idempotency; P2 scoped keys, audit events; P3 optional `scrape-html-with-fetch`, enrichment pass.

---

If you need **every** line of the long `s3storage` era section (roughly lines 125–360) pasted verbatim in one message, say so and we can split it by era (`0.x.x` … `10.x.x`).

