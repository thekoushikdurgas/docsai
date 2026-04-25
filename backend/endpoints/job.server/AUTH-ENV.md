# job.server — auth and environment

## Auth

- **`/api/v1/*`:** When **`API_KEY` is non-empty**, **`X-API-Key`** must match it. When **`API_KEY` is empty**, the middleware does **not** require a key (any `APP_ENV`); this is for local development only. **Always set a strong `API_KEY` in production.** (See [`EC2/job.server/internal/middleware/auth.go`](../../../../EC2/job.server/internal/middleware/auth.go).)
- **`GET /health`:** On the **root** router, **not** under the API key group — used for liveness/compose healthchecks without a key.

## Key variables

See also [`EC2/job.server/.env.example`](../../../../EC2/job.server/.env.example).

| Variable | Role |
| -------- | ---- |
| `PORT` | HTTP listen (default e.g. **9900**) |
| `APP_ENV` | e.g. `development` / `production` |
| `API_KEY` | Shared secret for **`X-API-Key`** |
| `MONGO_URI`, `MONGO_DATABASE` | Job and run storage |
| `REDIS_ADDR` | Asynq + scrape locks |
| `APIFY_API_TOKEN`, `APIFY_ACTOR_ID` | Apify actor |
| `SCRAPE_DEFAULT_*` | Default URLs / counts for scrapes |
| `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY` | **sync.server** (Connectra) base and key. Required for **batch upserts** during ingest and for **read-through** API routes (job → company/contacts) — they return **503** if unset. |
| `CONNECTRA_TIMEOUT`, `CONNECTRA_RETRY_*` | Outbound client timeout (seconds) and resty retries |
| `GIN_MODE` | Set to **`release`** to suppress Gin debug output (or rely on `APP_ENV=production`; see `main.go`). `docker-compose` for `job-api` may set this. |
| `EMBEDDED_ASYNQ_WORKER` | `true` runs the Asynq worker **inside the API process**; production usually uses a separate `cmd/worker` / `job-worker` container. |
| `SCRAPE_CRON_*` | `robfig/cron` daily enqueue (`Asia/Kolkata` default) |
| `ASYNQ_MAX_RETRY` | Task retries |

## Gateway (contact360.io/api)

| Variable | Use |
| -------- | --- |
| `JOB_SERVER_API_URL` | Base URL (no trailing path; client calls `/health`, `/api/v1/...`) |
| `JOB_SERVER_API_KEY` | Sent as **`X-API-Key`** to job.server |
| `JOB_SERVER_API_TIMEOUT` | Per-request seconds |

`health_check` in `JobServerClient` uses the same key when configured.

Last reviewed: 2026-04-25.
