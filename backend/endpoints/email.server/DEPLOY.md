# email.server — deployment

## Ports

- **API:** listens on **`PORT`** (default **3000**). Example production URL: `http://16.176.172.50:3000`.
- **Health:** `GET /health` returns **200** when Postgres and Redis ping OK; **503** with `dependencies` if either fails.

## Processes

Two binaries are required in production:

| Binary | Role |
|--------|------|
| `go run .` or built `main` | Gin HTTP API ([`main.go`](../../../../EC2/email.server/main.go)) |
| `go run ./cmd/worker` | Asynq workers for queues `mailtester`, `mailvetter`, `email_finder`, `email_pattern`, `default` ([`cmd/worker/main.go`](../../../../EC2/email.server/cmd/worker/main.go)) |

Without **cmd/worker**, S3 and async tasks enqueue but **do not process**.

## Dependencies

- **Postgres** — run [`migrations/001_emailapi_jobs.sql`](../../../../EC2/email.server/migrations/001_emailapi_jobs.sql) (see [MIGRATION-RUNBOOK](MIGRATION-RUNBOOK.md)).
- **Redis** — same `REDIS_ADDR` for API and worker.
- **Connectra** — `CONNECTRA_BASE_URL` + `CONNECTRA_API_KEY` for finder.
- **S3 / verification providers** — optional per feature set.

## Git

```bash
git remote add origin https://github.com/thekoushikdurgas/emailapis.git
git branch -M main
```

Use the same repo layout as `EC2/email.server` or adjust CI paths.

## Gateway

Set **`EMAIL_SERVER_API_URL`** to the public API base (e.g. `http://16.176.172.50:3000`) and **`EMAIL_SERVER_API_KEY`** equal to **`API_KEY`** on the satellite.
