# s3storage.server — public vs private routes

All paths are under **`/api/v1`**.

## Public (no API key)

| Method | Path |
|--------|------|
| GET | `/api/v1/health` |
| GET | `/api/v1/health/ready` |

## Private (`api_key` / `X-API-Key`)

All other documented routes in [`ROUTE-CLIENT-MATRIX.md`](./ROUTE-CLIENT-MATRIX.md), including jobs, uploads, analysis, objects, avatars, and bucket helpers.

Last updated: 2026-04-15.
