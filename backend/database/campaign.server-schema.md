# campaign.server — Postgres schema

Canonical SQL: [`EC2/campaign.server/db/migrations/001_init.sql`](../../../EC2/campaign.server/db/migrations/001_init.sql), [`003_campaign_overhaul.sql`](../../../EC2/campaign.server/db/migrations/003_campaign_overhaul.sql).

## Tables

| Table | Purpose |
|-------|---------|
| `campaigns` | Campaign run metadata (`channel`, `sequence_id`, `target_filter`, `paused_at`, `updated_at`, …) |
| `recipients` | Per-recipient send status + `unsub_token` |
| `templates` | Template metadata + S3 key; multi-channel (`channel`, `body_type`, `variables`, …) |
| `sequences` | Named sequence + JSON filters |
| `sequence_steps` | Ordered steps referencing `templates` |
| `suppression_list` | Global email suppression |

## Redis / Asynq

Job payloads only; no CRM entity store in Redis.
