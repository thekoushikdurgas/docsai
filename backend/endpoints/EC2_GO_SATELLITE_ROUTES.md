# EC2 Go / Gin satellite routes (parity with Python / legacy)

**Purpose:** Track HTTP surfaces implemented under `EC2/*.server/` while **`contact360.io/api`** (Python GraphQL) remains the customer orchestration gateway. Update this file when EC2 routes change; optional follow-up is to extend the matching `*_endpoint_era_matrix.json` files.

| Module path | Code path | Base URL (typical) | Notes |
| --- | --- | --- | --- |
| `contact360.io/jobs` | `EC2/job.server/` | `:8000` | Legacy group `/jobs/*`; v1 group `/api/v1/jobs/*` |
| `contact360.io/s3storage` | `EC2/s3storage.server/` | `S3STORAGE_PORT` (default `8087`) | `/api/v1/*`; Asynq `storage:metadata` |
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
| GET | `/api/v1/avatars/:user` | Presigned avatar URL |

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

## Related

- `docs/docs/architecture.md` — Request paths diagram
- `docs/backend/services.apis/*.api.md` — Go target notes
- `docs/docs/backend-language-strategy.md` — Satellite migration inventory
