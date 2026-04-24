# job.server — auth and environment

## Auth

- **`/api/v1/*`:** **`X-API-Key`** must match **`API_KEY`** when the server is configured with a non-empty `API_KEY`.
- **Development:** If **`API_KEY`** is **empty** and **`APP_ENV=development`**, requests may skip the key (see [`EC2/job.server/internal/middleware/auth.go`](../../../../EC2/job.server/internal/middleware/auth.go)). Production must set a strong `API_KEY`.

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
| `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY` | Optional company/contact sync |
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
