# Mailvetter Service (8.x API Hardening)

## Legacy Route Deprecation

| Legacy route | Replacement | Removal era |
| --- | --- | --- |
| `/verify` | `/v1/verify` | 9.0 |
| `/upload` | `/v1/upload` | 9.0 |
| `/status` | `/v1/status` | 9.0 |
| `/results` | `/v1/results` | 9.0 |

## Required Controls

- Distributed rate limiter is mandatory (Redis-backed), no in-memory fallback.
- `WEBHOOK_SECRET_KEY` must be isolated and must not fallback to `API_SECRET_KEY`.
- OpenAPI export is required for all `/v1/*` endpoints.
- Bulk job creation requires `Idempotency-Key`.
- Status vocabulary lock: `pending` -> `processing` -> `completed | failed`.
