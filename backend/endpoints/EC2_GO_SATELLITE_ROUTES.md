# EC2 Go / Gin satellite routes (parity with Python / legacy)

**Purpose:** Track HTTP surfaces implemented under `EC2/*.server/` while **`contact360.io/api`** (Python GraphQL) remains the customer orchestration gateway. Update this file when EC2 routes change; optional follow-up is to extend the matching `*_endpoint_era_matrix.json` files.

| Module path | Code path | Base URL (typical) | Notes |
| --- | --- | --- | --- |
| `contact360.io/s3storage` | `EC2/s3storage.server/` | `S3STORAGE_PORT` (default `8087`) | `/api/v1/*`; pgqueue (Postgres) `s3storage_metadata_jobs`; Asynq/Redis not used in this service |
| `contact360.io/ai` | `EC2/ai.server/` | `AI_PORT` (default `8090`) | Root-mounted `/health`, `/ai/*`, `/ai-chats/*` |
| `contact360.io/logsapi` | `EC2/log.server/` | `LOGSAPI_PORT` (default `8091`) | `/logs*`; Asynq `logs:flush`, `logs:sweep` |
| `contact360.io/extension` | `EC2/extension.server/` | `EXTENSION_PORT` (default `8092`) | `/v1/save-profiles`; scrape **not** on server |

**Deep links:** [s3storage](#ec2-s3storage) · [ai](#ec2-ai) · [logsapi](#ec2-logsapi) · [extension](#ec2-extension)

> **2026-04:** `EC2/job.server` was removed from the monorepo. Async jobs are orchestrated by **`contact360.io/api`** (GraphQL) against **`EC2/email.server`** (email finder/verifier/S3 jobs) and **`EC2/sync.server`** (`/common/jobs/*` import/export). See `docs/backend/apis/16_JOBS_MODULE.md`.

<a id="ec2-s3storage"></a>

## `contact360.io/s3storage` (`EC2/s3storage.server`)

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/health` | OK |
| GET | `/api/v1/health/ready` | S3 head bucket |
| GET | `/api/v1/buckets/:name/ping` | Bucket check (auth) |
| GET | `/api/v1/files` | List objects (`prefix` query) |
| POST | `/api/v1/uploads/initiate-csv` | Multipart start (`X-Idempotency-Key`) |
| GET | `/api/v1/uploads/:id/parts/:n` | Presigned part URL |
| POST | `/api/v1/uploads/:id/complete` | Complete + enqueue metadata task |
| DELETE | `/api/v1/uploads/:id/abort` | Abort multipart |
| GET | `/api/v1/analysis/schema` | Delimiter sniff (`key` query) |
| GET | `/api/v1/analysis/stats` | Row count sample (`key` query) |
| GET | `/api/v1/avatars/:user` | Presigned avatar URL (`?ext=` default `png`; response echoes `X-Request-ID`) |

**2026-04 update:** multipart upload session state is **Postgres-only** (`multipart_sessions`); the API process refuses to start multipart routes without a queue DB handle (no in-process fallback map).

**New routes (2026-04):**
- `GET /api/v1/jobs` — list metadata jobs (query: `state`, `limit`; max 500)
- `GET /api/v1/jobs/:id` — get specific job row

**Retry logic:** `Fail()` now implements exponential back-off (attempt × 30s, cap 5 min), up to 5 attempts, then `dead` state.

**EC2 client:** `contact360.io/api` now uses `s3storage_ec2_client.py` as the canonical adapter (maps `objects` → `files`, correct HTTP methods for abort/etc).

<a id="ec2-ai"></a>

## `contact360.io/ai` (`EC2/ai.server`)

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | OK |
| GET | `/health/ready` | `HF_API_KEY` configured |
| POST | `/ai/email/analyze` | Email risk (raw model output) |
| POST | `/ai/company/summary` | Summary |
| POST | `/ai/filters/parse` | NL → filters (raw) |
| POST | `/ai/rag/match` | Chunk + embed match |
| POST,GET,PUT,DELETE | `/ai-chats/` … | In-memory store (Postgres target per plan) |
| POST | `/ai-chats/:id/message` | Chat round-trip |
| POST | `/ai-chats/:id/message/stream` | SSE proxy |

Worker: `ai:resume_parse`, `ai:ats_score` (Asynq).

<a id="ec2-logsapi"></a>

## `contact360.io/logsapi` (`EC2/log.server`)

| Method | Path | Description |
| --- | --- | --- |
| POST | `/logs` | Single log |
| POST | `/logs/batch` | Batch (max 100) |
| GET | `/logs` | List (`limit`, `level`) |
| GET | `/logs/search` | Text search (`q`, `limit`) |
| GET | `/logs/:id` | Get |
| PUT | `/logs/:id` | Update |
| DELETE | `/logs/:id` | Delete |
| POST | `/logs/delete` | Bulk by ids |

<a id="ec2-extension"></a>

## `contact360.io/extension` (`EC2/extension.server`)

| Method | Path | Description |
| --- | --- | --- |
| POST | `/v1/save-profiles` | Dedup, chunk 500, Connectra upsert |
| POST | `/v1/scrape` | **501** — scrape in extension only |

<a id="ec2-emailapigo"></a>

## `contact360.io/emailapigo` (`EC2/email.server`)

Module: `github.com/ayan/emailapigo` | **Canonical port: `3000`** (`.env.example` and `config.go` default, production `http://16.176.172.50:3000`) | Auth: `X-API-Key`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/health` | Public | Diagnostics (all providers + DB + Redis configured?) |
| GET | `/` | Public | Service info |
| GET | `/metrics` | Public | In-process cache hit/miss, response time counters |
| GET | `/health/live` | Public | Liveness (always `200` when process serves) |
| GET | `/health/ready` | Public | Redis + Postgres ping |
| GET | `/health/db` | Public | Postgres ping only |
| GET | `/jobs` | ✅ | List 50 most recent emailapi_jobs |
| GET | `/jobs/:id/status` | ✅ | Job progress from PG + Redis hash |
| POST | `/email/finder/` | ✅ | Single find (query params: `first_name`, `last_name`, **`domain` and/or `website`**) |
| POST | `/email/finder/bulk` | ✅ | Bulk find; semaphore 15 goroutines |
| POST | `/email/finder/bulk/job` | ✅ | Enqueue bulk find to Asynq; returns job_id |
| POST | `/email/single/verifier/` | ✅ | Single verify (JSON body; provider) |
| POST | `/email/bulk/verifier/` | ✅ | Parallel bulk verify (5 concurrent, 1.1s stagger) |
| POST | `/email/bulk/verifier/job` | ✅ | Enqueue bulk verify to Asynq; returns job_id |
| POST | `/email/verify/s3` | ✅ | Stream S3 CSV → verify per row (background) |
| POST | `/email/finder/s3` | ✅ | Stream S3 CSV → find per row (background) |
| POST | `/web/web-search` | ✅ | DuckDuckGo + OpenAI email discovery |
| POST | `/email-patterns/add` | ✅ | Add single email pattern |
| POST | `/email-patterns/add/bulk` | ✅ | Add batch email patterns |
| POST | `/email-patterns/predict` | ✅ | Pattern suggestions for one person+domain (JSON body) |
| POST | `/email-patterns/predict/bulk` | ✅ | Pattern suggestions for many triplets |
| POST | `/email/single/verifier/find` | ✅ | Find-then-verify first candidate (JSON body; `domain` or `website`) |

**Worker queues (Asynq/Redis):**

| Queue | Concurrency | Task types |
| --- | --- | --- |
| `mailtester` | 5 | `email:verify:mailtester`, `email:s3csv:verify:mailtester` |
| `mailvetter` | 1 | `email:verify:mailvetter`, `email:s3csv:verify:mailvetter` |
| `email_finder` | 4 | `email:find`, `email:s3csv:find` |
| `default` | 1 | (unused) |

**Era 0 hardening (done in repo):** SQL migrations under `EC2/email.server/migrations/001_emailapi_jobs.sql`, `MAILVETTER_BASE_URL` typo fixed (`mailvetter.com`), batch logger now uses `LAMBDA_LOGS_API_URL` / `LAMBDA_LOGS_API_KEY` env vars, PORT aligned to `3000`, `X-Request-ID` middleware enabled. `StatusRisky` added to email verification status constants.

**Additions (2026-04):** `POST /email-patterns/predict` and `POST /email-patterns/predict/bulk` routes wired. Worker tests added for mailtester, mailvetter, and email_finder workers.

**Era task pack:** `docs/backend/apis/EMAILAPIGO_ERA_TASK_PACKS.md`  
**Codebase analysis:** `docs/codebases/emailapis-codebase-analysis.md`

---

## Related

- `docs/docs/architecture.md` — Request paths diagram
- `docs/backend/services.apis/*.api.md` — Go target notes
- `docs/docs/backend-language-strategy.md` — Satellite migration inventory

## Local smoke findings (2026-03-30)

- `contact360.io/sync` local boot currently fails before bind (`:8080`) due env/dependency issues:
  - PostgreSQL auth failure
  - OpenSearch refused on `:9200`
  - S3 key invalid
  - `NewTicker` panic on non-positive interval
- `EC2/s3storage.server` readiness requires `S3STORAGE_BUCKET`; `/health/ready` returns `503` when missing.
- `EC2/ai.server` readiness requires `HF_API_KEY`; `/health/ready` returns `503` when missing.
- `EC2/extension.server` behavior confirmed:
  - `/v1/scrape` returns `501` (expected server-side non-support)
  - `/v1/save-profiles` parse/auth behavior should be standardized in contract docs.
- `EC2/email.server` compose runtime currently exposes a host/container port mismatch for API listener (`container logs show :8080 while compose maps 3000:3000`), causing empty reply on local probes.

## Docker smoke findings (2026-03-30)

- Docker images built successfully for:
  - `EC2/sync.server`
  - `EC2/s3storage.server`
  - `EC2/ai.server`
  - `EC2/log.server`
  - `EC2/extension.server`
  - `EC2/email campaign`
- Docker runtime probes:
  - `sync` container exits on startup (`HTTP 000`, `2.246460s`) with postgres/socket + elastic + S3 config failures and `NewTicker` panic.
  - `s3storage` responds `GET /api/v1/health => 200` (`0.033908s`), but `GET /api/v1/health/ready => 503` (`0.012579s`) when `S3STORAGE_BUCKET` is missing.
  - `ai` responds `GET /health => 200` (`0.019502s`), but `GET /health/ready => 503` (`0.014414s`) when `HF_API_KEY` is missing.
  - `logsapi` responds `GET /health => 200` (`0.020882s`) and `GET /logs?limit=5 => 200` (`0.024331s`, empty data).
  - `extension` responds `GET /health => 200` (`0.018526s`), `POST /v1/scrape => 501` (`0.010210s`), and valid JSON `POST /v1/save-profiles => 200` (`accepted: 0`).
  - `email campaign` image builds, but container exits before bind due missing required `S3_TEMPLATE_BUCKET` (`HTTP 000`, `2.229080s`).
  - `email.server` compose on host `:3000` still returns empty reply (`HTTP 000`, `~0.007s`) in docker runtime.
