# log.server — data ownership (memory + S3 + Redis)

This service does **not** use **PostgreSQL**. CRM Postgres remains in the **gateway** database.

## In-memory (`internal/store/memory.go`)

- **Entries:** `id`, `bucket`, `level`, `logger`, `message`, `meta` (string, often JSON for `user_id`, `request_id`, etc.), `created_at`.
- **Lost on restart** — treat as a **hot buffer**; S3 CSV holds historical snapshots.

## S3 (`S3_BUCKET_NAME`)

- **Flush path:** `logs/flush/YYYY/MM/DD/HH.csv` (hourly CSV from `csvlog`).
- **Worker sweep:** deletes objects under `logs/` older than **`LOG_TTL_DAYS`** by parsing date segments in keys.

## Redis (worker only)

- **Asynq** broker/backend for scheduled tasks (`logs:flush`, `logs:sweep`). Not used for the primary HTTP log row store.

## Gateway

- **`LogStatsRepository`** / MongoDB may hold aggregates for **`logStatistics`** — separate from this Go service.

Last updated: 2026-04-15.
