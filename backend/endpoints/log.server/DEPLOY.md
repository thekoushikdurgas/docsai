# log.server — deploy (EC2 / Docker)

## Reference URL

Example production base URL: **`http://3.91.83.154:8091`**. Gateway **`LOGS_SERVER_API_URL`** should be set to that origin (no path suffix).

## Processes

| Binary | Role |
|--------|------|
| `logsapi` (`cmd/api`) | Gin HTTP API — default port **8091** |
| `logsapi-worker` (`cmd/worker`) | Asynq + scheduled tasks (`logs:flush`, `logs:sweep`) |

## Dependencies

- **Redis** — required for worker (`REDIS_ADDR`, e.g. `redis:6379` in Docker Compose).
- **S3** — bucket + IAM for PutObject, List, Delete.
- **AWS credentials** — env or instance profile.

## Git

```bash
git remote add origin https://github.com/thekoushikdurgas/contactlogs.git
git branch -M main
```

## CI

See [`EC2/log.server/.github/workflows/deploy.yml`](../../../../EC2/log.server/.github/workflows/deploy.yml) — deploys to EC2 and curls **`http://127.0.0.1:8091/health`**.

Last updated: 2026-04-15.
