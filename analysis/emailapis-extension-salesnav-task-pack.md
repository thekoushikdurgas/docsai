# emailapis task pack — era `4.x` (extension / Sales Navigator)

**Service:** `lambda/emailapis` + `lambda/emailapigo`  
**Era focus:** extension-origin and SN-attributed find/verify traffic with provenance-safe behavior.

## Contract track

- [ ] Freeze `4.x` finder/verify payload compatibility for extension-originated flows.
- [ ] Require provenance fields: `source`, `workspace_id`, `ingestion_batch_id` (or equivalent), `trace_id`.
- [ ] Update endpoint matrix when fields/routes change: [`docs/backend/endpoints/emailapis_endpoint_era_matrix.json`](../backend/endpoints/emailapis_endpoint_era_matrix.json).

## Service track

- [ ] Validate burst behavior for SN imports; avoid unbounded parallel verify/finder storms.
- [ ] Ensure auth, provider routing, and error envelopes for `audience_source=sn_batch` traffic.
- [ ] Keep `email_finder_cache` key policy stable across SN vs manual ingest paths.

## Surface track

- [ ] Document dashboard surfaces that chain to emailapis after SN ingest (`contacts/import`, campaign audience).
- [ ] Document hooks/services attaching provenance from extension to API requests.

## Data track

- [ ] Confirm lineage expectations for `email_finder_cache` and `email_patterns`.
- [ ] Preserve traceability from verify/finder responses to logs (`trace_id`, `ingestion_batch_id`).
- [ ] Prevent SN-sourced rows from clobbering curated patterns without policy checks.

## Ops track

- [ ] Add release evidence for burst latency, cache hit rate, and provider error share by source.
- [ ] Record rollback and incident runbook notes for post-harvest degradation.
- [ ] Verify no duplicate paid verification on replayed extension batches.

## References

- [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md)
- [`docs/backend/database/emailapis_data_lineage.md`](../backend/database/emailapis_data_lineage.md)
- [`docs/frontend/emailapis-ui-bindings.md`](../frontend/emailapis-ui-bindings.md)
- [`jobs-extension-sn-task-pack.md`](jobs-extension-sn-task-pack.md)
