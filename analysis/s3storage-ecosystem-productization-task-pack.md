# s3storage — 9.x Ecosystem Productization Task Pack

**Service:** `lambda/s3storage`  
**Era:** `9.x` — Contact360 ecosystem integrations and platform productization

## Contract track

- [ ] Define entitlement matrix for storage capabilities by plan and tenant.
- [ ] Define quota policy contract (`rate`, `count`, `size`, `burst`) for upload/download/list operations.
- [ ] Freeze connector-safe storage API behavior for multipart and metadata paths.
- [ ] Align endpoint references in `docs/backend/endpoints/s3storage_endpoint_era_matrix.json`.

## Service track

- [ ] Enforce plan-aware limits and throttling in `app/services/storage_service.py`.
- [ ] Add tenant context validation for object key namespace and bucket prefix routing.
- [ ] Validate multipart upload controls for quota-aware part counts and finalization.
- [ ] Add integration-safe diagnostics around metadata worker handoff and failures.

## Surface track

- [ ] Define UX contract for storage entitlement failures (`quota_exhausted`, `size_limit_exceeded`, `plan_restricted`).
- [ ] Document impacted pages/components/hooks in:
  - `docs/frontend/s3storage-ui-bindings.md`
  - `docs/frontend/components.md`
  - `docs/frontend/hooks-services-contexts.md`
- [ ] Add operator workflow expectations for override and support triage paths.

## Data track

- [ ] Add tenant cost attribution fields to storage lineage and usage exports.
- [ ] Add residency metadata requirements for regulated tenant storage domains.
- [ ] Define metadata.json lineage fields for entitlement decision traceability.
- [ ] Update data lineage references in `docs/backend/database` for 9.x storage changes.

## Ops track

- [ ] Add entitlement correctness tests for upload/download/list under multiple plan tiers.
- [ ] Add quota and cost attribution accuracy checks to release evidence.
- [ ] Define alerts for quota rejection spikes and metadata worker lag.
- [ ] Add rollback procedures for storage policy misconfiguration incidents.

## References

- `docs/codebases/s3storage-codebase-analysis.md`
- `docs/backend/endpoints/s3storage_endpoint_era_matrix.json`
