# Extension telemetry (roadmap stage 4.4)

## Target platform

- **`lambda/logs.api`** — centralized logs and audit (**S3 CSV** object storage + query cache). Canonical architecture: [`docs/architecture.md`](../architecture.md), [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md).
- Data lineage: [`docs/backend/database/logsapi_data_lineage.md`](../backend/database/logsapi_data_lineage.md).

## Event schema (4.x freeze)

| Event | Required fields | Notes |
| --- | --- | --- |
| `extension.session.token_refreshed` | `workspace_id`, `trace_id`, `outcome`, `latency_ms` | Auth lifecycle from `graphqlSession` |
| `sn.ingest.started` | `workspace_id`, `ingestion_batch_id`, `profile_count`, `trace_id` | Save initiated |
| `sn.ingest.completed` | `workspace_id`, `ingestion_batch_id`, `saved_count`, `duration_ms` | Includes partial success cases |
| `sn.ingest.failed` | `workspace_id`, `ingestion_batch_id`, `error_code`, `stage`, `message` | `stage`: extract/dedup/save/connectra |
| `sn.sync.conflict_resolved` | `workspace_id`, `ingestion_batch_id`, `entity_id`, `resolution`, `trace_id` | Sync integrity signals |

Common provenance fields for all events:
- `source` (`sales_navigator` or `extension`)
- `extension_version` (if available)
- `request_id` (gateway or lambda request identifier)

## CloudWatch and correlation mapping

| Field | Origin | Use |
| --- | --- | --- |
| `trace_id` | Client/gateway | Correlate extension popup with backend writes |
| `ingestion_batch_id` | Extension save flow | Join retry paths and dedup outcomes |
| `request_id` | Lambda/API | Map app errors to infrastructure logs |

Correlation rule: extension and dashboard operators should be able to answer **"one save action to one outcome"** using `workspace_id + ingestion_batch_id + trace_id`.

## Extension-side implementation expectations

- Emit structured events from content/background scripts for scrape, dedup, save, retry, and auth refresh actions.
- Include duration and profile counts; never include raw HTML or full PII payloads.
- Use buffered/batched shipping with backoff to avoid noisy retries during outages.
- Align auth event emission with [`extension-auth.md`](extension-auth.md).

## Dashboard UX surfaces

- **`contact360.io/app`** import/jobs surfaces should show ingest status and error reasons sourced from logs aggregates.
- Required UX states: `queued`, `in_progress`, `partial_success`, `success`, `failed`.
- Link status detail drawers to `ingestion_batch_id` for support and replay operations.

## Ops gates and runbooks

- Alert thresholds:
  - `sn.ingest.failed` error rate spike
  - sustained `extension.session.token_refreshed` failures
  - anomaly in `sn.sync.conflict_resolved` volume
- Replay policy for poison payloads: isolate by `ingestion_batch_id`, patch payload contract, replay once with new idempotency token.
- Rollback policy for schema break: keep previous parser active for one release window; reject unknown critical fields with explicit error code.

## References

- **Service task slices** in `4.4.P` / `4.9.P` patches (ex-`logsapi-extension-salesnav-task-pack.md`)
- [`docs/backend/endpoints/logsapi_endpoint_era_matrix.json`](../backend/endpoints/logsapi_endpoint_era_matrix.json)
- [`docs/frontend/logsapi-ui-bindings.md`](../frontend/logsapi-ui-bindings.md)
- [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md)
