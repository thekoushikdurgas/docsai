# logs.api task pack — era `4.x` (extension / Sales Navigator)

**Service:** `lambda/logs.api`  
**Era focus:** telemetry schema, ingestion reliability, and operator visibility for extension + SN paths.

## Contract track

- [ ] Freeze `4.x` event names and required fields.
- [ ] Ensure canonical event set includes: `extension.session.token_refreshed`, `sn.ingest.started`, `sn.ingest.completed`, `sn.ingest.failed`, `sn.sync.conflict_resolved`.
- [ ] Require provenance fields: `workspace_id`, `ingestion_batch_id`, `source`, optional `extension_version`, `trace_id`.
- [ ] Update endpoint matrix on write/auth changes: [`docs/backend/endpoints/logsapi_endpoint_era_matrix.json`](../backend/endpoints/logsapi_endpoint_era_matrix.json).

## Service track

- [ ] Validate burst ingestion behavior after large SN harvests.
- [ ] Verify auth and error envelope for event writers.
- [ ] Correlate `trace_id` + `ingestion_batch_id` + lambda request id across pipeline.

## Surface track

- [ ] Document dashboard ingestion status surfaces and source filters.
- [ ] Ensure empty/error states map to logs-derived aggregates.

## Data track

- [ ] Define S3 CSV partition/prefix strategy for extension/SN event volume.
- [ ] Document retention and query-window expectations for operations.
- [ ] Confirm lineage in [`docs/backend/database/logsapi_data_lineage.md`](../backend/database/logsapi_data_lineage.md).

## Ops track

- [ ] Add dashboards and alerts for failed ingest, token-refresh failures, and conflict spikes.
- [ ] Publish replay/rollback runbook for poison payloads and schema breaks.
- [ ] Capture load-test evidence for peak extension cohort traffic.

## References

- [`extension-telemetry.md`](extension-telemetry.md)
- [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md)
- [`docs/frontend/logsapi-ui-bindings.md`](../frontend/logsapi-ui-bindings.md)
- [`docs/backend/database/logsapi_data_lineage.md`](../backend/database/logsapi_data_lineage.md)
