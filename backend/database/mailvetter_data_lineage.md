# Mailvetter Data Lineage (`backend(dev)/mailvetter`)

## Service identity

- Runtime: Go (Gin API + worker pool)
- Database: PostgreSQL
- Queue: Redis (`tasks:verify`)
- Core tables: `jobs`, `results`

## Table lineage

### `jobs`

| Column | Source | Purpose |
| --- | --- | --- |
| `id` | generated UUID | bulk job identity |
| `status` | service lifecycle update | pending/processing/completed/failed tracking |
| `total_count` | bulk request normalized email count | total workload |
| `processed_count` | worker updates | progress tracking |
| `valid_count` | worker updates | validity summary |
| `invalid_count` | worker updates | invalid summary |
| `owner_key` | API key / client identity | ownership and plan enforcement |
| `job_name` | generated name | human-readable job reference |
| `callback_url` | bulk request input | webhook destination |
| `callback_events` | bulk request input | webhook trigger filters |
| `webhook_sent` | dispatcher update | callback delivery state |
| `created_at` | insert time | lifecycle audit |
| `started_at` | first worker update | processing start |
| `updated_at` | each worker update | latest mutation timestamp |
| `completed_at` | final worker update | completion timestamp |

### `results`

| Column | Source | Purpose |
| --- | --- | --- |
| `id` | serial PK | row identity |
| `job_id` | queue task/job linkage | parent job relationship |
| `email` | normalized request item | verified address |
| `score` | scoring engine | numeric confidence/risk |
| `is_valid` | status mapping | boolean validity rollup |
| `processed_at` | worker write time | per-email processing timestamp |
| `data` | JSON marshal of full validation result | explainability payload (`status`, `reachability`, `score_details`, `analysis`) |

## Queue lineage

Redis task payload:

```json
{
  "job_id": "<uuid>",
  "email": "user@example.com",
  "verify_smtp": true,
  "check_disposable": true
}
```

Flow: bulk request -> Redis enqueue -> worker consume -> DB `results` write -> DB `jobs` counter update.

## Webhook lineage

On terminal job state, dispatcher sends:

- `event` (`completed` / `failed`)
- `job_id`
- summary (`total_emails`, `valid`, `invalid`, `valid_percentage`)
- signed with `X-Webhook-Signature` (HMAC-SHA256)

## Era alignment summary

| Era | Lineage emphasis |
| --- | --- |
| `0.x` | `jobs`/`results` baseline and queue flow |
| `1.x` | owner/plan attribution and usage lineage |
| `2.x` | verification payload completeness and score traceability |
| `3.x` | linkage to contact/company identifiers |
| `4.x` | source provenance (`extension`/`sales_navigator`) |
| `5.x` | AI explainability factor lineage |
| `6.x` | retry/DLQ/job event lineage |
| `7.x` | migration and deployment audit lineage |
| `8.x` | scoped key and API audit lineage |
| `9.x` | webhook delivery and partner connector lineage |
| `10.x` | campaign recipient verification snapshot lineage |
