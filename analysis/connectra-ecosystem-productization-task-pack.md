# Connectra — 9.x Ecosystem Productization Task Pack

**Service:** `contact360.io/sync`  
**Era:** `9.x` — Contact360 ecosystem integrations and platform productization

## Contract track

- [ ] Define entitlement-aware VQL policy contract for tenant plans in `app/services/query/*`.
- [ ] Freeze connector-facing request/response compatibility for:
  - `POST /contacts/batch-upsert`
  - `POST /companies/batch-upsert`
  - `POST /common/jobs/create`
- [ ] Document tenant isolation guarantees for read (`/contacts`, `/companies`) and write paths.
- [ ] Align endpoint era mapping in `docs/backend/endpoints/connectra_endpoint_era_matrix.json`.

## Service track

- [ ] Add per-tenant quota/throttle middleware for heavy query/export workloads.
- [ ] Enforce tenant filter injection before VQL execution in route handlers under `app/api/routes/`.
- [ ] Validate UUID5 dedup behavior and ensure connector ingestion is replay-safe under retries.
- [ ] Add fairness controls for mixed-tenant high-volume batch upsert traffic.

## Surface track

- [ ] Expose tenant quota and connector health signals to integrations/admin surfaces in:
  - `docs/frontend/README.md`
  - `docs/frontend/components.md`
  - `docs/frontend/hooks-services-contexts.md`
- [ ] Define user-facing messaging for quota blocked / degraded connector outcomes.
- [ ] Add support-facing reconciliation view requirements for created-vs-updated entity counts.

## Data track

- [ ] Store tenant usage aggregates for billing, quota, and SLA reporting.
- [ ] Persist connector lineage fields: `tenant_id`, `connector_id`, `source`, `session_id`, `trace_id`.
- [ ] Define audit table expectations for UUID collisions, dedup merges, and replay attempts.

## Ops track

- [ ] Add per-tenant SLO/error-budget dashboards for Connectra read/write paths.
- [ ] Add runbook for noisy-neighbor mitigation and quota override approvals.
- [ ] Define release gate evidence: tenant isolation report, quota enforcement tests, VQL policy conformance tests.

## References

- `docs/codebases/connectra-codebase-analysis.md`
- `docs/backend/endpoints/connectra_endpoint_era_matrix.json`
