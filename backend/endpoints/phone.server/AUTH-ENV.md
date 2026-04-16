# phone.server — authentication and environment

## Satellite (`EC2/phone.server`)

| Variable | Purpose |
|----------|---------|
| `API_KEY` | Required. Must match callers’ `X-API-Key`. |
| `PORT` | Default **3000**. |
| `DATABASE_URL` | Postgres DSN. |
| `REDIS_ADDR` | Redis for Asynq + job hashes. |
| `CONNECTRA_BASE_URL` / `CONNECTRA_API_KEY` | Optional; used by finder flow when calling sync.server. |

## Gateway (`contact360.io/api`)

| Variable | Maps to satellite |
|----------|-------------------|
| `PHONE_SERVER_API_URL` | Base URL (e.g. `http://18.176.172.50:3000`). |
| `PHONE_SERVER_API_KEY` | Must equal **`API_KEY`**. |
| `PHONE_SERVER_API_TIMEOUT` | HTTP client timeout (seconds). |

Legacy aliases: `LAMBDA_PHONE_API_URL`, `LAMBDA_PHONE_API_KEY`, `LAMBDA_PHONE_API_TIMEOUT`.
