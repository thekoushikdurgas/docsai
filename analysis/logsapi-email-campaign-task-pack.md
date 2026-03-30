# LogsAPI Task Pack (10.x)

Codebase: `lambda/logs.api`

## Campaign event schema

Required fields for campaign logs:

- `campaign_id`
- `batch_id`
- `trace_id` (`X-Trace-Id`)
- `event_type`
- `org_id`
- `timestamp`

## Implementation queue

| Task | Scope | Patch |
| --- | --- | --- |
| Freeze campaign event contract | contract | `10.A.0` |
| Add strict schema validation on writes | service | `10.A.1` |
| Persist campaign CSV lifecycle to S3 with retention | data | `10.A.2` |
| Expose logs filter patterns for campaign UI | surface | `10.A.3` |
| Add error-rate and lag alerts | ops | `10.A.8` |

## Storage lifecycle

- Path prefix: `logs/campaign/{campaign_id}/...`
- CSV artifacts are append-only for compliance replay.
