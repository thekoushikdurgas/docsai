# phone.server — database migration runbook

## Required table

Apply [`EC2/phone.server/migrations/001_phoneapi_jobs.sql`](../../../../EC2/phone.server/migrations/001_phoneapi_jobs.sql) once per Postgres database.

```bash
psql "$DATABASE_URL" -f EC2/phone.server/migrations/001_phoneapi_jobs.sql
```

## Redis

Same **`REDIS_ADDR`** for the Gin API and **`cmd/worker`** (Asynq queues + job row hashes).

## Go module

**Module:** `github.com/thekoushikdurgas/phone.server` ([`go.mod`](../../../../EC2/phone.server/go.mod)).
