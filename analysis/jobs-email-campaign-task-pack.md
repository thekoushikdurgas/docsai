# Jobs Task Pack (10.x)

Codebase: `contact360.io/jobs`

## Processor additions

- `campaign_send`
- `campaign_track`
- `campaign_verify`

## Required implementation

| Task | Scope | Patch |
| --- | --- | --- |
| Add processor contract + status vocabulary | contract | `10.A.0` |
| Implement idempotent processor execution | service | `10.A.6` |
| Persist timeline in `job_events` for audit replay | data | `10.A.7` |
| Expose execution progress in campaign UI panels | surface | `10.A.3` |

## Audit timeline requirements

- Every stage write must include `campaign_id`, `job_id`, `trace_id`, `status`, `timestamp`.
- Compliance bundle is generated from `job_events` as immutable history.
