# campaign.server — auth and environment (Era 1)

| Variable | Purpose |
|----------|---------|
| `CAMPAIGN_API_KEY` | Primary API key (`X-API-Key`) |
| `ADMIN_API_KEY` | Legacy alias |
| `CAMPAIGN_PORT` | HTTP listen port (default **9800**; legacy `PORT` supported via `config.Config`) |
| `WORKER_CONCURRENCY` | Asynq worker concurrency (default **10**) |
| `DATABASE_URL` | Postgres DSN (or `DB_HOST`/`DB_PORT`/`DB_USER`/`DB_PASSWORD`/`DB_NAME`) |
| `REDIS_ADDR` | Redis for Asynq |
| `S3_TEMPLATE_BUCKET` | AWS bucket for template bodies |
| `JWT_SECRET` | Unsubscribe tokens ([`utils/token`](../../../../EC2/campaign.server/utils/token.go)) |
| `SMTP_*` | Outbound email |
| `APP_URL` | Base URL for unsubscribe links |
| `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY` | Sequence trigger (contact fetch) |
| `EMAIL_SERVER_API_URL`, `EMAIL_SERVER_API_KEY` | Optional finder |
| `PHONE_SERVER_API_URL`, `PHONE_SERVER_API_KEY` | Optional finder |
| `S3STORAGE_SERVER_API_URL`, `S3STORAGE_SERVER_API_KEY` | Optional presign |

Gateway: `CAMPAIGN_API_URL`, `CAMPAIGN_API_KEY`.
