# log.server — health and tracing

## `GET /health`

- **Auth:** None.
- **Response:** `{"status":"ok","service":"logsapi"}` — liveness.

## `X-Request-ID`

- Every response includes **`X-Request-ID`**: taken from the incoming header or generated (see [`RequestIDMiddleware`](../../../../EC2/log.server/internal/api/router.go) in [`cmd/api/main.go`](../../../../EC2/log.server/cmd/api/main.go)).

## Dependency notes

- **S3** misconfiguration surfaces as skipped flush logs or worker sweep no-ops.
- **Redis** is required for **`cmd/worker`**; the API process can start without Redis for basic HTTP ingest (not recommended for production without the worker).

Last updated: 2026-04-15.
