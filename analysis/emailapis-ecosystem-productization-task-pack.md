# Email APIs / EmailAPIGo — 9.x Ecosystem Productization Task Pack

**Services:** `lambda/emailapis`, `lambda/emailapigo`  
**Era:** `9.x` — Contact360 ecosystem integrations and platform productization

This pack decomposes email execution capabilities into Contract, Service, Surface, Data, and Ops tracks for partner-safe, tenant-safe operation.

## Contract track

- [ ] Freeze 9.x finder/verifier/pattern endpoint contracts in:
  - `lambda/emailapis/app/api/v1/router.py`
  - `lambda/emailapigo/internal/api/router.go`
- [ ] Normalize error envelope for both runtimes (`status`, `message`, `provider`, `request_id`, `retryable`) and map to gateway GraphQL errors in `contact360.io/api`.
- [ ] Define partner connector compatibility contract for email workflows (input mapping and expected response cardinality).
- [ ] Update endpoint matrix in `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`.

## Service track

- [ ] Implement entitlement-aware execution guard for finder/verifier paths (per-tenant caps before provider fanout).
- [ ] Align provider orchestration behavior between runtimes (mailvetter/icypeas/truelist fallback order and timeout windows).
- [ ] Validate auth behavior (`X-API-Key` and gateway-issued context headers) across both runtimes.
- [ ] Add deterministic idempotency key support for bulk finder/verifier requests to avoid duplicate partner billing.

## Surface track

- [ ] Bind integrations UX to runtime diagnostics:
  - `docs/frontend/emailapis-ui-bindings.md`
  - `docs/frontend/components.md`
  - `docs/frontend/hooks-services-contexts.md`
- [ ] Define user-facing status vocabulary for email connector outcomes (`success`, `partial_success`, `quota_blocked`, `provider_degraded`).
- [ ] Add connector health and fallback explanation copy for settings and integrations pages.
- [ ] Document loading/error/progress patterns for bulk operations and webhook-triggered runs.

## Data track

- [ ] Document 9.x lineage changes for `email_finder_cache` and `email_patterns` in `docs/backend/database`.
- [ ] Record per-request provider decision lineage (`provider`, `fallback_provider`, `status`, `latency_ms`, `tenant_id`, `trace_id`).
- [ ] Add tenant-safe usage attribution fields required for commercial metering reconciliation.

## Ops track

- [ ] Add 9.x observability checks for provider health, fallback rate, and partner webhook error rate.
- [ ] Update rollback and incident runbook for email-impacting releases with connector-specific playbooks.
- [ ] Define release evidence bundle for each minor (`9.x.y`): contract diff, load test summary, and parity proof between Python and Go runtimes.

## References

- `docs/codebases/emailapis-codebase-analysis.md`
- `docs/backend/postman/README.md`
- `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`
