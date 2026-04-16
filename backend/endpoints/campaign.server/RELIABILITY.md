# campaign.server — reliability (Era 6)

- **Liveness:** `GET /health`
- **Readiness:** `GET /health/ready` (Postgres ping)
- **Workers:** Asynq retries per library defaults; SMTP failures increment `failed` on `recipients`
- **Suppression:** `suppression_list` checked before SMTP send
