# log.server — authentication and environment

## HTTP authentication

When **`LOGSAPI_API_KEY`** is non-empty, all routes except **`GET /health`** require **`X-API-Key`** (or query **`api_key`**) to match.

## Go service (`EC2/log.server`)

| Variable | Purpose |
|----------|---------|
| `LOGSAPI_PORT` | HTTP listen port (default **8091**) |
| `LOGSAPI_API_KEY` | Shared API key (optional in dev — if empty, auth middleware allows all) |
| `AWS_REGION` | AWS region |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` | S3 credentials (or instance role) |
| `S3_BUCKET_NAME` | Bucket for CSV flush + worker TTL sweep |
| `LOG_TTL_DAYS` | S3 object age for sweep delete (default **90**) |
| `LOG_FLUSH_INTERVAL_SECONDS` | API process periodic flush ticker (default **30**) |
| `REDIS_ADDR` | Required for **`cmd/worker`** (e.g. `redis:6379` in compose) |
| `WORKER_CONCURRENCY` | Asynq worker concurrency (default **2**; set **10** to match a 10-worker pool) |

See [`EC2/log.server/.env.example`](../../../../EC2/log.server/.env.example).

## Gateway (`contact360.io/api`)

| Variable | Purpose |
|----------|---------|
| `LOGS_SERVER_API_URL` | Base URL only (e.g. `http://3.91.83.154:8091`). Aliases: `LAMBDA_LOGS_API_URL` |
| `LOGS_SERVER_API_KEY` | Must match `LOGSAPI_API_KEY` on the Go service. Aliases: `LAMBDA_LOGS_API_KEY` |
| `LOGS_SERVER_API_TIMEOUT` | HTTP client timeout. Alias: `LAMBDA_LOGS_API_TIMEOUT` |

Optional logging toggles: `ENABLE_LOGS_SERVER_LOGGING`, `LOG_BATCH_SIZE`, `LOG_FLUSH_INTERVAL`, etc. — see [`app/core/config.py`](../../../../contact360.io/api/app/core/config.py).

Last updated: 2026-04-15.
