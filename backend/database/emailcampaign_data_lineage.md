# Email Campaign Service — Data Lineage (`backend(dev)/email campaign`)

## Primary data stores

| Store | Technology | Owner | Purpose |
| --- | --- | --- | --- |
| Campaign DB | PostgreSQL (sqlx) | Campaign service | Campaigns, recipients, suppression, templates |
| Template storage | AWS S3 (`templates/{id}.html`) | Campaign service | Template HTML bodies |
| Task queue | Redis (Asynq) | Campaign service | Async campaign:send task queue |

---

## Table lineage by era

### `campaigns` table

| Column | Type | Era introduced | Source | Notes |
| --- | --- | --- | --- | --- |
| `id` | TEXT (UUID) | `0.x` | API handler | Generated on campaign create |
| `title` | TEXT | `0.x` | POST /campaign body | Campaign name |
| `status` | TEXT | `0.x` | Worker updates | `pending → sending → completed/failed` |
| `filepath` | TEXT | `0.x` | POST /campaign body | CSV recipient file path (deprecated `3.x`+) |
| `total` | INT | `0.x` | Worker (recipient count) | Total recipients loaded |
| `sent` | INT | `0.x` | Worker (`IncrementSent`) | Successfully sent count |
| `failed` | INT | `0.x` | Worker (`IncrementFailed`) | Failed send count |
| `created_at` | TIMESTAMP | `0.x` | DB default | Row creation time |
| `user_id` | TEXT | `1.x` | JWT claims | User who created campaign |
| `org_id` | TEXT | `1.x` | JWT claims | Organization context |
| `audience_source` | TEXT | `3.x` | POST /campaign body | `csv`, `segment`, `vql`, `sn_batch` |
| `segment_id` | TEXT | `3.x` | POST /campaign body | Connectra saved segment ID |
| `vql_query` | TEXT | `3.x` | POST /campaign body | VQL filter query |
| `scheduled_at` | TIMESTAMP | `10.x` | POST /campaign body | Scheduled send time |
| `subject` | TEXT | `10.x` | Template reference | Denormalized subject for quick display |
| `ab_test_enabled` | BOOLEAN | `10.x` | POST /campaign body | A/B test flag |

### `recipients` table

| Column | Type | Era introduced | Source | Notes |
| --- | --- | --- | --- | --- |
| `id` | TEXT (UUID) | `0.x` | Worker (generated) | Per-recipient UUID |
| `campaign_id` | TEXT | `0.x` | FK to campaigns | FK reference |
| `email` | TEXT | `0.x` | CSV / audience resolver | Recipient email address |
| `name` | TEXT | `0.x` | CSV / audience resolver | Recipient display name |
| `status` | TEXT | `0.x` | Worker | `pending → sent/failed/skipped/unsubscribed` |
| `error` | TEXT | `0.x` | Worker on failure | SMTP error message |
| `sent_at` | TIMESTAMP | `0.x` | Worker on success | Send completion time |
| `unsub_token` | TEXT | `0.x` | Worker (JWT) | JWT token for unsubscribe link (⚠ missing from schema.sql) |
| `retry_count` | INT | `6.x` | Worker retry logic | Number of send attempts |
| `contact_ref_id` | TEXT | `3.x` | Connectra audience resolver | Connectra contact UUID for lineage |

### `suppression_list` table

| Column | Type | Era introduced | Source | Notes |
| --- | --- | --- | --- | --- |
| `email` | TEXT (PK) | `0.x` | Unsubscribe endpoint, bounce webhook | Global suppression: cannot be re-sent |
| `reason` | TEXT | `0.x` | Unsubscribe endpoint | `unsubscribe`, `bounce`, `complaint`, `manual` |
| `created_at` | TIMESTAMP | `0.x` | DB default | When suppressed |

### `templates` table

| Column | Type | Era introduced | Source | Notes |
| --- | --- | --- | --- | --- |
| `id` | TEXT (UUID) | `0.x` | Template create handler | Generated on create |
| `name` | TEXT | `0.x` | POST /templates body | Display name |
| `subject` | TEXT | `0.x` | POST /templates body | Email subject line (Go template) |
| `s3_key` | TEXT | `0.x` | Template service | S3 key `templates/{id}.html` |
| `created_at` | TIMESTAMP | `0.x` | DB default | Row creation time |
| `updated_at` | TIMESTAMP | `0.x` | Update handler | Last update time |
| `is_ai_generated` | BOOLEAN | `5.x` | AI generate endpoint | AI flag for badge display |
| `ai_prompt` | TEXT | `5.x` | AI generate endpoint | Prompt used for generation |
| `ai_model` | TEXT | `5.x` | AI generate endpoint | AI model identifier |

---

## Future tables (planned by era)

### `sequences` (era `10.x`)

| Column | Type | Source |
| --- | --- | --- |
| `id` | TEXT | Generated |
| `org_id` | TEXT | JWT claims |
| `name` | TEXT | API body |
| `status` | TEXT | State machine |
| `created_at` | TIMESTAMP | DB default |

### `sequence_steps` (era `10.x`)

| Column | Type | Source |
| --- | --- | --- |
| `id` | TEXT | Generated |
| `sequence_id` | TEXT | FK to sequences |
| `step_type` | TEXT | `send_email`, `wait_days`, `branch_on_open`, `branch_on_click` |
| `delay_days` | INT | API body |
| `template_id` | TEXT | FK to templates |
| `condition` | TEXT | Branch condition |
| `position` | INT | Step ordering |

### `campaign_events` (era `10.x`)

| Column | Type | Source |
| --- | --- | --- |
| `id` | TEXT | Generated |
| `campaign_id` | TEXT | FK |
| `recipient_id` | TEXT | FK |
| `event_type` | TEXT | `open`, `click`, `unsubscribe`, `bounce` |
| `occurred_at` | TIMESTAMP | Tracking endpoint |

### `campaign_analytics` (era `10.x`)

| Column | Type | Source |
| --- | --- | --- |
| `campaign_id` | TEXT | FK |
| `computed_at` | TIMESTAMP | Aggregation cron |
| `open_rate` | FLOAT | Computed from campaign_events |
| `click_rate` | FLOAT | Computed from campaign_events |
| `unsub_rate` | FLOAT | Computed from campaign_events |
| `bounce_rate` | FLOAT | Computed from campaign_events |

### `ab_test_variants` (era `10.x`)

| Column | Type | Source |
| --- | --- | --- |
| `campaign_id` | TEXT | FK |
| `variant` | TEXT | `A` or `B` |
| `template_id` | TEXT | FK |
| `recipient_pct` | INT | Split ratio |

---

## S3 data lineage

| S3 key pattern | Producer | Consumer | TTL/Retention |
| --- | --- | --- | --- |
| `templates/{id}.html` | `template/service.go:UploadTemplate` | `worker/email_worker.go:fetchTemplate` (via cache) | Permanent until `DeleteTemplate` |

---

## Redis lineage

| Key pattern | Producer | Consumer | TTL |
| --- | --- | --- | --- |
| Asynq task `campaign:send` | `api/handlers.go:CreateCampaign` | `worker/campaign_worker.go:HandleCampaignTask` | Until processed or DLQ |

---

## Cross-service data dependencies

| External service | Data consumed | Integration point |
| --- | --- | --- |
| Connectra (`contact360.io/sync`) | Contact list for audience resolution | `3.x`+ via `POST /contacts/search` or saved segment |
| `logs.api` | Campaign lifecycle events | `7.x`+ audit log emission |
| Billing service | Credit balance check | `1.x`+ pre-send credit guard |
| AI service | Generated template HTML | `5.x`+ `POST /templates/generate` |

---

## Known schema drift (must fix)

| Issue | Affected table | Fix |
| --- | --- | --- |
| `templates` table missing from `db/schema.sql` | `templates` | Add CREATE TABLE DDL to schema.sql |
| `recipients.unsub_token` missing from `db/schema.sql` | `recipients` | Add column DDL to schema.sql |
| `GetUnsubToken` uses `DB.Exec` not `DB.Get` | `recipients` | Fix query in `db/queries.go` |

## 2026 lineage addendum

- `templates` and `recipients.unsub_token` are required schema elements for campaign/unsubscribe traceability.
- Unsubscribe correctness depends on query-path fix (`DB.Get`) to ensure suppression lineage evidence is reliable.
