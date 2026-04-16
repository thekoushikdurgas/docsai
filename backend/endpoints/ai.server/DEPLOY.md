# ai.server — deploy (Era 7)

## Listen

- Default **`AI_PORT=3000`** (e.g. `http://16.176.172.50:3000`).
- Binary: `go run ./cmd/api` or Docker image `Dockerfile` exposing **3000**.

## Git

Remote: **`https://github.com/thekoushikdurgas/ai.server.git`** (satellite repo root).

## Compose

[`docker-compose.yml`](../../../../EC2/ai.server/docker-compose.yml) includes **redis**, **api** (`3000:3000`), **worker** (`REDIS_ADDR`, `WORKER_CONCURRENCY=10`).

## CI

[`.github/workflows/deploy.yml`](../../../../EC2/ai.server/.github/workflows/deploy.yml) health-checks `http://127.0.0.1:3000/health`.

Last updated: 2026-04-15.
