# Email Campaign Service — Era 0.x Task Pack
## Foundation and pre-product stabilization

### Context
`backend(dev)/email campaign` must be initialized with a clean schema, functional health check, and Redis/Postgres/S3 connectivity before any product features can be layered on top. This era establishes the deployment baseline so the service can accept and queue campaign tasks safely.

---

## Track A — Contract

| Task | Description | Owner | Patch assignment |
| --- | --- | --- | --- |
| A-0.1 | Define service contract document: routes, payloads, status codes, env var requirements | Backend | `0.2.0`–`0.2.2` |
| A-0.2 | Confirm API key auth scheme vs JWT gateway pattern for internal calls | Backend + Arch | `0.2.0`–`0.2.2` |
| A-0.3 | Agree two-binary model (API + worker) as the permanent deployment topology | DevOps | `0.2.3`–`0.2.6` |

## Track B — Service (backend implementation)

| Task | Description | Owner | Patch assignment |
| --- | --- | --- | --- |
| B-0.1 | Fix `db/schema.sql` — add `templates` table and `recipients.unsub_token` column | Backend | `0.2.0`–`0.2.2` |
| B-0.2 | Fix `GetUnsubToken` — replace `DB.Exec` with `DB.Get` so token value is returned | Backend | `0.2.0`–`0.2.2` |
| B-0.3 | Add SMTP credentials via env vars; pass auth to `smtp.SendMail` | Backend | `0.2.3`–`0.2.6` |
| B-0.4 | Implement `/health` response to include DB ping and Redis ping (not just HTTP 200) | Backend | `0.2.3`–`0.2.6` |
| B-0.5 | Add env validation at startup (panic if required vars missing) | Backend | `0.2.3`–`0.2.6` |
| B-0.6 | Remove or gate `queue/reddis_queue.go` — confirm if legacy; add clear comment or delete | Backend | `0.2.3`–`0.2.6` |

## Track C — Surface (UI/UX frontend)

| Task | Description | Owner | Patch assignment |
| --- | --- | --- | --- |
| C-0.1 | No product UI in 0.x (only internal/admin health page). Confirm campaign composer routes do not exist in this era. | Frontend | `0.2.3`–`0.2.6` |
| C-0.2 | Ensure campaign service base URL is wired in environment config for dashboard (stubbed/unreferenced for UI in 0.x). | Frontend | `0.2.3`–`0.2.6` |

## Track D — Data

| Task | Description | Owner | Patch assignment |
| --- | --- | --- | --- |
| D-0.1 | Bootstrap migration script executing `schema.sql` idempotently | Backend | `0.2.0`–`0.2.2` |
| D-0.2 | Seed test data: 1 template, 1 campaign, 2 recipients, 1 suppressed email | Backend/QA | `0.2.0`–`0.2.2` |
| D-0.3 | Confirm S3 bucket and prefix (`templates/`) exist and IAM role has `GetObject`/`PutObject` | DevOps | `0.2.3`–`0.2.6` |
| D-0.4 | Confirm Redis instance and Asynq queue namespace don't conflict with Connectra's queue | DevOps | `0.2.3`–`0.2.6` |

## Track E — Ops

| Task | Description | Owner | Patch assignment |
| --- | --- | --- | --- |
| E-0.1 | Write `Dockerfile` for API server binary | DevOps | `0.2.3`–`0.2.6` |
| E-0.2 | Write `Dockerfile` for worker binary | DevOps | `0.2.3`–`0.2.6` |
| E-0.3 | Write `docker-compose.yml` for local dev (API + worker + Redis + Postgres) | DevOps | `0.2.3`–`0.2.6` |
| E-0.4 | Add structured logging (JSON) to all handler/worker paths | Backend | `0.2.3`–`0.2.6` |

---

## Completion gate
- [ ] `schema.sql` bootstraps cleanly on fresh Postgres; all 4 tables created. (patch assignment: `0.2.7`–`0.2.9`)
- [ ] API server starts with valid env; `/health` returns `{db: ok, redis: ok}`. (patch assignment: `0.2.7`–`0.2.9`)
- [ ] Worker process starts, connects to Redis, registers `campaign:send` handler. (patch assignment: `0.2.7`–`0.2.9`)
- [ ] SMTP test message delivered from staging credentials. (patch assignment: `0.2.7`–`0.2.9`)
