# Email Campaign Service Reference (`backend(dev)/email campaign`)

## Runtime and surface

- Runtime: Go + Gin API, Asynq workers, Redis queue, PostgreSQL, S3 templates.
- Key routes: `/campaign`, `/unsub`, `/templates*`, `/health`.
- Canonical status vocabulary: `pending`, `sending`, `completed`, `completed_with_errors`, `failed`, `paused`.

## Required schema drift fixes

Apply in `db/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  subject TEXT NOT NULL,
  s3_key TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE recipients
ADD COLUMN IF NOT EXISTS unsub_token TEXT;
```

## Required code fixes

- `db/queries.go`: replace unsubscribe token read path from `DB.Exec` to `DB.Get`.
- `worker/email_worker.go`: replace nil SMTP auth with env-driven `smtp.PlainAuth`.
- `cmd/main.go`: enforce JWT middleware on all non-health routes.
- `queue/reddis_queue.go`: remove or hard-disable legacy raw Redis queue path to avoid dual-queue drift with Asynq.

## SMTP/auth config contract

Required env vars:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`

JWT requirements:

- Tenant-aware claims (`user_id`, `org_id`, `role`).
- Route guards on campaign creation, template CRUD, mailbox/inbox routes.

## Asynq baseline

- Task type: `campaign:send`
- Queue: `default`
- Retries: `3`
- Timeout: `30m`
- Worker fan-out: 5 goroutines + `sync.WaitGroup` join
- Reliability baseline: idempotency key per `(campaign_id, recipient_email)`

## logsapi integration contract

Emit immutable events for:

- `campaign.created`
- `campaign.sending.started`
- `campaign.recipient.sent`
- `campaign.recipient.failed`
- `campaign.unsubscribed`
- `campaign.completed`

Required fields: `campaign_id`, `recipient_id` (optional per event), `batch_id`, `org_id`, `trace_id` (`X-Trace-Id`), `timestamp`.

## Integration notes (10.x delivery)

- Audience sources must evolve from CSV-only to `segment`, `vql`, and `sn_batch`.
- Mailvetter preflight (`validate-bulk`) is mandatory before send fan-out.
- S3 template path contract: `templates/{template_id}.html`.
- This file is the core service truth used by all `10.x` version and task-pack docs.
