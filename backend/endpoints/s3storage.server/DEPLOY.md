# s3storage.server — deploy (EC2 / Docker)

## Reference host

Example API base URL used in docs and client defaults: **`http://3.27.164.107:8087`**. Gateway **`S3STORAGE_SERVER_API_URL`** should be set to that origin **without** a trailing `/api/v1` path.

## Processes

1. **API:** Gin HTTP server — default port **`8087`** (`S3STORAGE_PORT` / `PORT`).
2. **Worker:** [`cmd/worker`](../../../../EC2/s3storage.server/cmd/worker/main.go) — Asynq consumer for `s3storage:metadata` and `s3storage:sync_metadata`. Set **`S3STORAGE_WORKER_CONCURRENCY`** (default **10**).

## Dependencies

- **Redis** — multipart sessions, job hashes, Asynq broker/backend.
- **S3** — object store; bucket must exist and credentials/role must allow HeadBucket, multipart, Get/Put/Delete as used by routes.
- **AWS credentials** — env vars or instance profile.

## Git

Upstream repository is often tracked as: **`https://github.com/thekoushikdurgas/storage.server.git`**. The Go module path remains `contact360.io/s3storage` — see [`MODULE-OPTIONAL.md`](./MODULE-OPTIONAL.md).

## CI deploy sketch

[`EC2/s3storage.server/.github/workflows/deploy.yml`](../../../../EC2/s3storage.server/.github/workflows/deploy.yml) copies the tree to `/home/$USER/s3storage` on the EC2 host, writes `.env` from secrets, runs **`docker compose up --build -d`**, then curls **`http://127.0.0.1:8087/api/v1/health/ready`**.

Last updated: 2026-04-15.
