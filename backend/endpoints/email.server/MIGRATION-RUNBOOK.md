# email.server — database migration runbook

## Required table

The API and workers expect Postgres table **`emailapi_jobs`** (and GORM models for email patterns — see [`EC2/email.server/migrations/001_emailapi_jobs.sql`](../../../../EC2/email.server/migrations/001_emailapi_jobs.sql)).

### Apply once

```bash
psql "$DATABASE_URL" -f EC2/email.server/migrations/001_emailapi_jobs.sql
```

Or paste the SQL from that file into your migration runner.

### Verify

```sql
\d emailapi_jobs
SELECT COUNT(*) FROM emailapi_jobs;
```

## Redis

Asynq uses the same **`REDIS_ADDR`** for:

- Task queues (`mailtester`, `mailvetter`, `email_finder`, `email_pattern`, `default`)
- Per-job row hashes (`job:{id}:rows`, `job:{id}:total`, `job:{id}:s3meta`)

No separate migration; ensure Redis is reachable before starting **`cmd/worker`**.

## Optional: Go module path

The Go module is currently **`github.com/ayan/emailapigo`**. If you need imports to match **`github.com/thekoushikdurgas/emailapis`**, rename `go.mod` and replace import paths across `EC2/email.server` in a dedicated PR (large diff; not required for runtime if you build from this tree).
