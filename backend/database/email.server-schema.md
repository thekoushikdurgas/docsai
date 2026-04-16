# email.server — Postgres (and Redis) reference

## Migrated SQL

| Artifact | File |
|----------|------|
| Async job metadata | [`EC2/email.server/migrations/001_emailapi_jobs.sql`](../../EC2/email.server/migrations/001_emailapi_jobs.sql) |

### `emailapi_jobs`

Columns: `id` (text PK), `provider`, `status`, `total_emails`, `completed`, `unknown_count`, `avg_duration_ms`, `done`, `output_s3_key`, timestamps. Used by **`GET /jobs`**, **`GET /jobs/:id/status`**, and S3 streaming handlers.

## GORM-managed tables

The service uses GORM models; ensure these exist in Postgres (migrations may live in a separate process or auto-migrate in dev):

| Model | Table | Notes |
|-------|-------|--------|
| [`EmailPattern`](../../EC2/email.server/internal/models/email_pattern.go) | `email_patterns` | Pattern learning / prediction |
| [`EmailFinderCache`](../../EC2/email.server/internal/models/email_finder_cache.go) | `email_finder_cache` | Finder short-circuit cache; **`citext`** extension recommended |

## Redis keys (operational)

Not SQL — documented for DBA/runbook completeness:

- Asynq task queues: `mailtester`, `mailvetter`, `email_finder`, `email_pattern`, `default`
- Job progress: `job:{job_id}:rows`, `job:{job_id}:total`, `job:{job_id}:s3meta` (TTL ~24h in handlers)

See also [MIGRATION-RUNBOOK](../endpoints/email.server/MIGRATION-RUNBOOK.md).
