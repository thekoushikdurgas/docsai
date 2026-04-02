# EC2 Go / Gin satellite routes (parity with Python / legacy)

**Purpose:** Track HTTP surfaces implemented under `EC2/*.server/` while **`contact360.io/api`** (Python GraphQL) remains the customer orchestration gateway. Update this file when EC2 routes change; optional follow-up is to extend the matching `*_endpoint_era_matrix.json` files.

| Module path | Code path | Base URL (typical) | Notes |
| --- | --- | --- | --- |
| `contact360.io/jobs` | `EC2/job.server/` | `:8000` | Legacy group `/jobs/*`; v1 group `/api/v1/jobs/*` |
| `contact360.io/s3storage` | `EC2/s3storage.server/` | `S3STORAGE_PORT` (default `8087`) | `/api/v1/*`; pgqueue (Postgres) `s3storage_metadata_jobs`; Asynq/Redis not used in this service |
| `contact360.io/ai` | `EC2/ai.server/` | `AI_PORT` (default `8090`) | Root-mounted `/health`, `/ai/*`, `/ai-chats/*` |
| `contact360.io/logsapi` | `EC2/log.server/` | `LOGSAPI_PORT` (default `8091`) | `/logs*`; Asynq `logs:flush`, `logs:sweep` |
| `contact360.io/extension` | `EC2/extension.server/` | `EXTENSION_PORT` (default `8092`) | `/v1/save-profiles`; scrape **not** on server |

**Deep links:** [jobs](#ec2-jobs) · [s3storage](#ec2-s3storage) · [ai](#ec2-ai) · [logsapi](#ec2-logsapi) · [extension](#ec2-extension)

<a id="ec2-jobs"></a>

## `contact360.io/jobs` (`EC2/job.server`)

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Liveness-style OK |
| GET | `/health/live` | Alive |
| GET | `/health/ready` | PostgreSQL ping |
| GET | `/metrics` | Prometheus (**not** under `/api/v1` in current Go image) |
| GET | `/api/v1/jobs/:uuid` | Single job |
| POST | `/api/v1/jobs/email-export` | DAG insert |
| POST | `/api/v1/jobs/contact360-import` | DAG insert |
| POST | `/api/v1/jobs/contact360-export` | DAG insert |
| POST | `/jobs/bulk-insert/complete-graph` | Bulk DAG |
| PUT | `/jobs/:uuid/retry` | Retry |
| GET | `/jobs/` | List / filter |

**Parity gaps vs `jobs_endpoint_era_matrix` (Python):** timeline, DAG detail, `email-verify`, `email-pattern-import`, `validate/vql`, `/api/v1/metrics` paths — track in era tasks before marking matrix green for Go-only cutover.

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

Module: `github.com/ayan/emailapigo` | Port: `8080` (production) / `3000` (config default — see FIX-1 in era task pack) | Auth: `X-API-Key`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/health` | Public | Diagnostics (all providers + DB + Redis configured?) |
| GET | `/` | Public | Service info |
| GET | `/metrics` | Public | In-process cache hit/miss, response time counters |
| GET | `/health/live` | Public | **TODO** Era 0 — not yet implemented |
| GET | `/health/ready` | Public | **TODO** Era 0 — not yet implemented |
| GET | `/health/db` | Public | **TODO** Era 0 — not yet implemented |
| GET | `/jobs` | ✅ | List 50 most recent emailapi_jobs |
| GET | `/jobs/:id/status` | ✅ | Job progress from PG + Redis hash |
| POST | `/email/finder/` | ✅ | Single find (query params: first_name, last_name, domain) |
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
| POST | `/email-patterns/predict` | **TODO** | Era 2 — schema exists, route not wired |
| POST | `/email-patterns/predict/bulk` | **TODO** | Era 2 — schema exists, route not wired |
| POST | `/email/single/verifier/find` | **TODO** | Era 2 — response type exists, route not wired |

**Worker queues (Asynq/Redis):**

| Queue | Concurrency | Task types |
| --- | --- | --- |
| `mailtester` | 5 | `email:verify:mailtester`, `email:s3csv:verify:mailtester` |
| `mailvetter` | 1 | `email:verify:mailvetter` |
| `email_finder` | 4 | `email:find`, `email:s3csv:find` |
| `default` | 1 | (unused) |

**Known issues (fix in Era 0):**
- Port mismatch: container binds `:3000` but compose maps `8080:8080` → empty reply on probes.
- `emailapi_jobs` DDL missing from repo (no migration file).
- `MAILVETTER_BASE_URL` default has typo `mailvaiter.com`.
- Batch logger URL hardcoded in `internal/logging/batch_logger.go`.

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
- `EC2/job.server` requires `.env` in service root; boot fails without it.
- `EC2/s3storage.server` readiness requires `S3STORAGE_BUCKET`; `/health/ready` returns `503` when missing.
- `EC2/ai.server` readiness requires `HF_API_KEY`; `/health/ready` returns `503` when missing.
- `EC2/extension.server` behavior confirmed:
  - `/v1/scrape` returns `501` (expected server-side non-support)
  - `/v1/save-profiles` parse/auth behavior should be standardized in contract docs.
- `EC2/email.server` compose runtime currently exposes a host/container port mismatch for API listener (`container logs show :8080 while compose maps 3000:3000`), causing empty reply on local probes.

## Docker smoke findings (2026-03-30)

- Docker images built successfully for:
  - `EC2/sync.server`
  - `EC2/job.server`
  - `EC2/s3storage.server`
  - `EC2/ai.server`
  - `EC2/log.server`
  - `EC2/extension.server`
  - `EC2/email campaign`
- Docker runtime probes:
  - `sync` container exits on startup (`HTTP 000`, `2.246460s`) with postgres/socket + elastic + S3 config failures and `NewTicker` panic.
  - `job.server` container exits on startup (`HTTP 000`, `2.240538s`) because `.env` is not found in `/app`.
  - `s3storage` responds `GET /api/v1/health => 200` (`0.033908s`), but `GET /api/v1/health/ready => 503` (`0.012579s`) when `S3STORAGE_BUCKET` is missing.
  - `ai` responds `GET /health => 200` (`0.019502s`), but `GET /health/ready => 503` (`0.014414s`) when `HF_API_KEY` is missing.
  - `logsapi` responds `GET /health => 200` (`0.020882s`) and `GET /logs?limit=5 => 200` (`0.024331s`, empty data).
  - `extension` responds `GET /health => 200` (`0.018526s`), `POST /v1/scrape => 501` (`0.010210s`), and valid JSON `POST /v1/save-profiles => 200` (`accepted: 0`).
  - `email campaign` image builds, but container exits before bind due missing required `S3_TEMPLATE_BUCKET` (`HTTP 000`, `2.229080s`).
  - `email.server` compose on host `:3000` still returns empty reply (`HTTP 000`, `~0.007s`) in docker runtime.
