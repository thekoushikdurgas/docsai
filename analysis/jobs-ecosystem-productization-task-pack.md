# jobs — 9.x Ecosystem Productization Task Pack

**Service:** `contact360.io/jobs`  
**Era:** `9.x` — Contact360 ecosystem integrations and platform productization

This pack decomposes scheduler work into Contract, Service, Surface, Data, and Ops tracks.

## Contract track

- [ ] Define tenant-aware quota and entitlement scheduling contract for create/retry DAG operations.
- [ ] Freeze visibility contract for:
  - `GET /api/v1/jobs/`
  - `GET /api/v1/jobs/{uuid}`
  - `GET /api/v1/jobs/{uuid}/timeline`
  - `GET /api/v1/jobs/{uuid}/dag`
- [ ] Define connector callback payload contract for partner-facing async job completion events.
- [ ] Align endpoint references in `docs/backend/endpoints/jobs_endpoint_era_matrix.json`.

## Service track

- [ ] Implement entitlement checks at create/retry boundaries in:
  - `app/services/job_service.py`
  - `app/workers/scheduler.py`
- [ ] Add fairness-aware tenant partitioning policy in scheduler queue dispatch.
- [ ] Add processor-level quota guard hooks in `app/processors/` registry.
- [ ] Ensure tenant context propagation across scheduler -> worker -> processor -> event timeline.

## Surface track

- [ ] Document tenant quota cards, entitlement warnings, and escalation controls in jobs UI bindings.
- [ ] Define tenant-filtered jobs tables and timeline views for admin/operator users.
- [ ] Add workflow messaging for `quota_exhausted`, `tenant_blocked`, and `retry_deferred` states.

## Data track

- [ ] Record `tenant_id` and entitlement snapshot in `job_node` lifecycle lineage.
- [ ] Define isolation boundary expectations for `job_events`, DAG edges, and metrics.
- [ ] Add reconciliation evidence model for quota decisions vs observed scheduler behavior.

## Ops track

- [ ] Add per-tenant SLA/error-budget dashboards and alert thresholds.
- [ ] Add runbook for quota exhaustion and noisy-neighbor mitigation incidents.
- [ ] Add release gate checks: timeline tenant isolation test, retry policy conformance test, processor quota test.

## References

- `docs/codebases/jobs-codebase-analysis.md`
- `docs/backend/endpoints/jobs_endpoint_era_matrix.json`
