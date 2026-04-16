# phone.server — deployment

## Target example

- **URL:** `http://18.176.172.50:3000` (set **`PORT=3000`**).
- **Git:** `git remote add origin https://github.com/thekoushikdurgas/phone.server.git` then `git branch -M main`.

## Processes

| Process | Role |
|---------|------|
| `go run .` or binary from repo root | Gin HTTP API |
| `go run ./cmd/worker` | Asynq workers (required for S3/async jobs) |

## Dependencies

- Postgres + migration [`001_phoneapi_jobs.sql`](../../../../EC2/phone.server/migrations/001_phoneapi_jobs.sql)
- Redis (same address for API and worker)

## Gateway

Set **`PHONE_SERVER_API_URL`** and **`PHONE_SERVER_API_KEY`** in `contact360.io/api`.
