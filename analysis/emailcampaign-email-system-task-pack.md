# Email Campaign Service — Era 2.x Task Pack
## Contact360 Email System

Grounded in [`docs/codebases/emailcampaign-codebase-analysis.md`](../codebases/emailcampaign-codebase-analysis.md).

## Codebase file map (high-value)

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| API server | `backend(dev)/email campaign/cmd/main.go` | Gin routes, template + campaign endpoints |
| Worker | `backend(dev)/email campaign/cmd/worker/main.go` | Asynq consumer + send pipeline |
| DB schema | `backend(dev)/email campaign/db/schema.sql` | **Known gap:** missing `templates` table and `recipients.unsub_token` column |
| SMTP send | `smtp.SendMail(...)` call site | **Known gap:** uses `nil` auth; must use env-driven auth |

### Context
Era `2.x` hardens the core email delivery infrastructure. The campaign service evolves from a basic SMTP relay to a production-grade send engine with authentication, bounce handling, retry logic, DKIM signing awareness, and suppression-list accuracy.

## Known critical gaps (must be reflected in 2.x gates)

From the codebase analysis “Gaps and risks”:

- [ ] **SMTP auth is currently `nil`** (`smtp.SendMail(..., nil, ...)`) → will fail for authenticated providers.
- [ ] `db/schema.sql` is incomplete: missing `templates` table and `recipients.unsub_token`.
- [ ] `GetUnsubToken` uses `DB.Exec` instead of `DB.Get` (does not return token value as intended).
- [ ] No authentication on routes (must be protected before exposure).

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-2.1 | Document supported SMTP providers (SendGrid, AWS SES, Mailgun) and auth configuration | Backend |
| A-2.2 | Define bounce/complaint handling webhook contract (provider → campaign service) | Backend |
| A-2.3 | Document retry policy: max attempts, backoff intervals, DLQ behaviour | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-2.1 | SMTP auth: read username/password/host/port from env; pass `smtp.PlainAuth` to `smtp.SendMail` | Backend |
| B-2.2 | Per-message retry with exponential backoff and Asynq max-retry policy | Backend |
| B-2.3 | Implement bounce webhook receiver endpoint; auto-add bounced email to `suppression_list` | Backend |
| B-2.4 | Implement complaint webhook receiver (Spam/Abuse feedback); add to suppression | Backend |
| B-2.5 | Add DKIM header passthrough note or SES-managed signing recommendation | Backend |
| B-2.6 | Add configurable send-rate throttle (N emails/sec) to `EmailWorker` goroutines | Backend |
| B-2.7 | Campaign status: add `completed_with_errors` when `failed > 0 && sent > 0` | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-2.1 | Email settings page: input boxes for SMTP host, port, username; masked password field | Frontend |
| C-2.2 | Campaign list: colour-coded status badge (`pending`, `sending`, `completed`, `completed_with_errors`, `failed`) | Frontend |
| C-2.3 | Campaign detail: sent/failed/unsubscribed counts with mini progress bar | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-2.1 | Migration: add `bounced_at TIMESTAMP` and `complaint_at TIMESTAMP` to `recipients` | Backend |
| D-2.2 | Migration: add `provider TEXT` and `send_rate_limit INT` to `campaigns` | Backend |
| D-2.3 | Ensure suppression_list has index on `email` for fast pre-send lookup | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-2.1 | SMTP credential rotation: mount as Kubernetes secret or SSM parameter | DevOps |
| E-2.2 | Dead-letter queue monitoring: alert on tasks exceeding max-retry in Asynq dashboard | DevOps |

---

## Completion gate
- [ ] Email delivered from real SMTP credentials without nil auth.
- [ ] Bounce/complaint webhook adds email to suppression list and suppresses future sends.
- [ ] Campaign with partial failures shows `completed_with_errors` status.
- [ ] Per-second rate limit prevents exceeding SES/SendGrid quota.
