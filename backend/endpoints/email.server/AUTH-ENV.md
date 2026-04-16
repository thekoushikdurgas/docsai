# email.server — authentication and environment mapping

## Satellite (`EC2/email.server`)

| Variable | Purpose |
|----------|---------|
| `API_KEY` | Required. Must match callers’ `X-API-Key` header. |
| `PORT` | HTTP listen port (default **3000**). |
| `DATABASE_URL` | Postgres DSN for `emailapi_jobs` and pattern tables. |
| `REDIS_ADDR` | Redis for Asynq + job row hashes (default `localhost:6379`). |
| `CONNECTRA_BASE_URL` | **sync.server** root URL (no trailing path). |
| `CONNECTRA_API_KEY` | **sync.server** `X-API-Key` (same auth model as gateway → Connectra). |

## Gateway (`contact360.io/api`)

| Variable | Maps to satellite |
|----------|-------------------|
| `EMAIL_SERVER_API_URL` | Base URL only (e.g. `http://16.176.172.50:3000`). `EmailServerClient` strips trailing `/`. |
| `EMAIL_SERVER_API_KEY` | Must equal **`API_KEY`** on email.server. |
| `EMAIL_SERVER_API_TIMEOUT` | HTTP client timeout (seconds). |

Legacy names `LAMBDA_EMAIL_API_URL` / `LAMBDA_EMAIL_API_KEY` may still be read in config — prefer the `EMAIL_SERVER_*` names in new deployments.

## Header contract

- **Inbound to email.server:** `X-API-Key: <shared secret>`
- **Outbound to Connectra:** `X-API-Key: <CONNECTRA_API_KEY>` ([`ConnectraClient`](../../../../EC2/email.server/internal/clients/connectra_client.go))

Optional: **`X-Request-ID`** is echoed or generated on every response ([`middleware.RequestID`](../../../../EC2/email.server/internal/middleware/requestid.go)).
