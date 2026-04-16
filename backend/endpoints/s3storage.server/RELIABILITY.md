# s3storage.server — health, readiness, and tracing

## Middleware

Every response includes **`X-Request-ID`**: taken from the incoming `X-Request-ID` header if present, otherwise a new UUID — see [`router.go`](../../../../EC2/s3storage.server/internal/api/router.go).

## `GET /api/v1/health`

- **Auth:** None.
- **Behavior:** Returns `{"status":"ok"}` — **liveness only** (no Redis or S3 checks).

## `GET /api/v1/health/ready`

- **Auth:** None.
- **Behavior:** Returns **503** if `S3STORAGE_BUCKET` is unset, **Redis PING** fails, or **S3 HeadBucket** fails; otherwise `{"ready":true}`.

## Optional symmetry note

`/api/v1/health` intentionally stays minimal so load balancers can mark the process up even when dependencies are briefly unhealthy. Use **`/health/ready`** for dependency-aware routing.

Last updated: 2026-04-15.
