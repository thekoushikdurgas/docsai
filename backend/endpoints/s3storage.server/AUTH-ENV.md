# s3storage.server — auth and environment variables

## HTTP authentication

Protected routes use **`apiKeyMiddleware`**: the caller must supply the shared secret via **`X-API-Key`** **or** query parameter **`api_key`**. There is no `Authorization: Bearer` branch in the current router.

## Go service (`EC2/s3storage.server`)

| Variable | Purpose |
|----------|---------|
| `S3STORAGE_PORT` / `PORT` | API listen port (default **8087**) |
| `S3STORAGE_API_KEY` / `API_KEY` | Shared API key for authenticated routes |
| `S3STORAGE_BUCKET` / `BUCKET` / `S3_BUCKET_NAME` | Default S3 bucket for objects |
| `AWS_REGION` | AWS region |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Credentials (or instance role) |
| `REDIS_ADDR` | Redis for multipart sessions, job hashes, Asynq broker |
| `REDIS_PASSWORD` | Optional |
| `ASYNQ_PREFIX` | Redis key prefix / Asynq namespace (default `s3storage`) |
| `S3STORAGE_WORKER_CONCURRENCY` | Worker concurrency (default **10**; see `cmd/worker`) |

See also [`EC2/s3storage.server/.env.example`](../../../../EC2/s3storage.server/.env.example).

## Gateway (`contact360.io/api`)

| Variable | Purpose |
|----------|---------|
| `S3STORAGE_SERVER_API_URL` | Base URL **without** `/api/v1` suffix (e.g. `http://3.27.164.107:8087`). Aliases: `LAMBDA_S3STORAGE_API_URL` |
| `S3STORAGE_SERVER_API_KEY` | Must match `S3STORAGE_API_KEY` on the Go service. Aliases: `LAMBDA_S3STORAGE_API_KEY` |
| `S3STORAGE_SERVER_API_TIMEOUT` | HTTP client timeout. Alias: `LAMBDA_S3STORAGE_API_TIMEOUT` |

The Python client strips a trailing `/api/v1` from the base URL if present — see [`s3storage_client.py`](../../../../contact360.io/api/app/clients/s3storage_client.py).

Last updated: 2026-04-15.
