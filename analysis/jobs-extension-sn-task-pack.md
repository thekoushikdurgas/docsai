# jobs task pack — era `4.x` (extension / Sales Navigator)

**Service:** `contact360.io/jobs`  
**Era focus:** extension-driven ingestion DAGs with provenance-safe retry/idempotency.

## Contract track

- [ ] Define required metadata: `source`, `workspace_id`, `channel`, `ingestion_batch_id`, `idempotency_token`, `trace_id`.
- [ ] Define sync batch contract for extension submissions: payload limits, chunk boundaries, retry headers, completion callbacks.

## Service track

- [ ] Enforce source tagging and dedupe-safe scheduling for replayed batches.
- [ ] Harden retries with exponential backoff + jitter and capped attempts.
- [ ] Expose sync lag metrics from `save-profiles` success to job completion.

## Surface track

- [ ] Document sync status cards, retry controls, and execution history for extension-origin jobs.
- [ ] Map backend states (`queued`, `processing`, `failed`, `completed`, `stuck`) to user labels/actions.

## Data track

- [ ] Persist idempotency evidence fields (`idempotency_token`, content hash, ingestion batch id).
- [ ] Link API traces to job records and logs.api events.
- [ ] Document retention for audit and replay investigations.

## Ops track

- [ ] Add dashboards for sync lag p95/max, retry churn, and stuck processing age.
- [ ] Publish stuck-job runbook with replay/cancel steps by `ingestion_batch_id`.
- [ ] Add rollback playbook for extension ingestion regressions.

## References

- [`docs/codebases/jobs-codebase-analysis.md`](../codebases/jobs-codebase-analysis.md)
- [`docs/backend/endpoints/jobs_endpoint_era_matrix.json`](../backend/endpoints/jobs_endpoint_era_matrix.json)
- [`docs/frontend/jobs-ui-bindings.md`](../frontend/jobs-ui-bindings.md)
- [`extension-sync-integrity.md`](extension-sync-integrity.md)
