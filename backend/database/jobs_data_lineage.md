# jobs data lineage

Data-lineage reference for `contact360.io/jobs` scheduler-owned database tables and cross-service flow.

## Stores and boundaries

- Scheduler-owned Postgres: `DATABASE_URL` (`job_node`, `edges`, `job_events`)
- Contact360 shared Postgres: `CONTACT360_DATABASE_URL` (import/export read-write paths)
- OpenSearch: `OPENSEARCH_CONNECTION` (contact/company search operations)
- S3 artifacts: input/output CSVs used by stream processors

## Table lineage

### `job_node`

Primary lifecycle table for each job execution unit.

- Identity: `uuid`, `job_title`, `job_type`
- Scheduling: `degree`, `priority`, `status`, `run_after`
- Retry: `try_count`, `retry_interval`
- Payload/result: `data` (JSONB), `job_response` (JSONB)
- Progress: `checkpoint_byte`, `processed_rows`, `total_bytes`, `checkpoint_uuid`, `checkpoint_data`
- Audit time: `created_at`, `updated_at`, `deleted_at`

Lineage notes:
- Inbound from API create/retry endpoints and DAG insertion.
- Updated by scheduler, worker pool, and processors.
- Exposed to UI via status/list/detail endpoints.

### `edges`

DAG dependency relationship table.

- `source` -> `target` (both FK to `job_node.uuid`)

Lineage notes:
- Written during complete graph insert.
- Read during dependency resolution and degree decrement.
- Governs readiness of downstream nodes.

### `job_events`

Append-style lifecycle/event audit table.

- `job_uuid`, `event_type`, `event_data`, `timestamp`

Lineage notes:
- Written during enqueue/start/progress/complete/fail/retry transitions.
- Exposed via `GET /api/v1/jobs/{uuid}/timeline`.
- Compliance evidence source for historical execution traces.

## Era lineage concerns (0.x-10.x)

- `0.x`: establish canonical schema and event naming.
- `1.x`: link creation/retry events to billing/credit accountability.
- `2.x`: email stream output lineage (`input` CSV -> `output` CSV).
- `3.x`: Contact360 import/export lineage across Postgres/OpenSearch/S3.
- `4.x`: extension/sales-nav source provenance in job metadata.
- `5.x`: AI metadata (`model`, `confidence`, `cost`) in `job_response`.
- `6.x`: reliability lineage (idempotency, retry reason, stale recovery evidence).
- `7.x`: access/audit governance, retention policy auditability.
- `8.x`: external callback/webhook lineage and API-version traces.
- `9.x`: tenant-aware partitioning, quota and entitlement lineage.
- `10.x`: campaign compliance lineage bundles from `job_events` timeline.
