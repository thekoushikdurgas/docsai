# Email Campaign Service — Era 1.x Task Pack
## Contact360 User, Billing, and Credit System

### Context
In `1.x`, Contact360 adds user identity, multi-tenancy, billing tiers, and credit accounting. The email campaign service must become tenant-aware: campaigns must be attributed to users/organizations, and the send volume must deduct credits before enqueueing.

---

## Codebase evidence (backend(dev)/email campaign)

- Runtime + queue:
  - Go + Gin HTTP server
  - Async job queue: Asynq on Redis
  - Separate Asynq worker binary consumes task type `campaign:send`
- Concurrency model:
  - 5 worker goroutines per campaign, joined via `sync.WaitGroup` before marking status `completed`
- Route surface:
  - `POST /campaign` → enqueue `campaign:send` (template_id + filepath/name context)
  - `GET /unsub` uses a JWT-signed unsubscribe token → sets suppression + updates recipient status
  - `POST /templates`, `GET /templates`, `GET /templates/:id`, `DELETE /templates/:id`, `POST /templates/:id/preview`
  - `GET /health` liveness probe
- Storage:
  - Templates stored in S3 as `templates/{id}.html`
- Data model:
  - `campaigns`: title/status/filepath/total/sent/failed
  - `recipients`: per-recipient send status + tracking
  - `suppression_list` and `templates` for opt-out + rendering

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-1.1 | Define `user_id` / `org_id` fields on `campaigns` table | Backend |
| A-1.2 | Specify credit cost model: credits-per-recipient or credits-per-campaign | Product |
| A-1.3 | Document JWT claims that campaign routes will validate (sub, org, plan tier) | Backend + Auth |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-1.1 | Add `user_id` and `org_id` columns to `campaigns` table migration | Backend |
| B-1.2 | Add authentication middleware on `/campaign`, `/templates` routes (validate JWT from gateway) | Backend |
| B-1.3 | Pre-send credit check: call billing service before enqueue; return 402 if insufficient | Backend |
| B-1.4 | Post-send credit deduction: deduct credits per sent recipient on completion | Backend |
| B-1.5 | Surface plan-tier limits: monthly send-volume cap per org | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-1.1 | Dashboard: show credit cost estimate on campaign create wizard (phase-ahead UI) | Frontend |
| C-1.2 | Billing page: add "Email Sends" as a line item in credit usage breakdown | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-1.1 | Migration: add `user_id TEXT`, `org_id TEXT` to `campaigns` | Backend |
| D-1.2 | Log per-campaign credit transaction for audit | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-1.1 | Auth middleware configuration via env (JWT public key or HMAC secret) | DevOps |
| E-1.2 | Add billing service base URL as env var; health check its reachability | DevOps |

---

## Completion gate
- [ ] Unauthenticated `POST /campaign` returns 401.
- [ ] Campaign create with insufficient credits returns 402 with descriptive error.
- [ ] Campaign row includes `user_id` and `org_id` from JWT claims.
