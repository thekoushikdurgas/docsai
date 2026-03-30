# logs.api — 9.x Ecosystem Productization Task Pack

**Service:** `lambda/logs.api`  
**Era:** `9.x` — Contact360 ecosystem integrations and platform productization

This pack decomposes logging and audit evidence capabilities into Contract, Service, Surface, Data, and Ops tracks.

## Contract track

- [ ] Freeze 9.x logging schema additions and compatibility notes for partner and tenant observability.
- [ ] Define 9.x audit export contract for support and compliance bundles.
- [ ] Align endpoint references in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.
- [ ] Define traceability field contract (`tenant_id`, `request_id`, `trace_id`, `connector_id`, `event_type`).

## Service track

- [ ] Implement/validate event ingestion and query behavior in `app/services/log_service.py`.
- [ ] Add tenant-safe filtering defaults for query/search/stat endpoints.
- [ ] Verify auth and error envelope behavior for gateway and service consumers.
- [ ] Add audit-bundle export path with bounded query window and deterministic CSV formatting.

## Surface track

- [ ] Document impacted pages/tabs/components for audit and integrations evidence views.
- [ ] Document hooks/services/contexts for logs and diagnostics flows in frontend bindings.
- [ ] Define UX states for long-running evidence exports (queued, ready, failed, expired).
- [ ] Add operator-facing wording for trace correlation and redaction-safe support workflows.

## Data track

- [ ] Document tenant-prefixed S3 CSV object convention and lineage.
- [ ] Define retention policy and archive expectations per tenant tier.
- [ ] Record SLA evidence table expectations for incident and monthly reliability reports.
- [ ] Update lineage reference in `docs/backend/database/logsapi_data_lineage.md`.

## Ops track

- [ ] Add observability checks for query latency, ingestion lag, and export failures.
- [ ] Add release validation evidence for 9.x logging schema and audit export compatibility.
- [ ] Capture rollback and incident runbook notes for logging-impacting releases.
- [ ] Define alerting thresholds for abnormal error rates by tenant/connector cohort.

## References

- `docs/codebases/logsapi-codebase-analysis.md`
- `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`
- `docs/backend/database/logsapi_data_lineage.md`
