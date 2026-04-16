# log.server — ingest and storage pipeline

## Ingest (API process)

1. **`POST /logs`** / **`POST /logs/batch`** — JSON mapped to [`store.Entry`](../../../../EC2/log.server/internal/store/memory.go); append rows to a CSV [`AppendBuffer`](../../../../EC2/log.server/internal/csvlog/csvlog.go).
2. **In-memory** — `Memory` holds recent entries for **`GET /logs`**, **`GET /logs/search`**, CRUD by id.

## Periodic S3 flush (`cmd/api`)

- Ticker every **`LOG_FLUSH_INTERVAL_SECONDS`** (default **30**).
- On **Asia/Kolkata** hour boundary, may reset buffer; uploads CSV to **`logs/flush/YYYY/MM/DD/HH.csv`** when buffer is dirty and large enough (see [`cmd/api/main.go`](../../../../EC2/log.server/cmd/api/main.go)).

## Worker (`cmd/worker`)

- **Redis** required (`REDIS_ADDR`); **Asynq** scheduler:
  - `logs:flush` — periodic tick (currently lightweight; CSV flush is primarily in API).
  - `logs:sweep` — lists `logs/` in S3 and deletes objects older than **`LOG_TTL_DAYS`**.
- **`WORKER_CONCURRENCY`** (default **2**; set **10** for a 10-worker pool).

Last updated: 2026-04-15.
