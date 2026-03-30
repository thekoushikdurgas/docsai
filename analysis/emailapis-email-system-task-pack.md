# emailapis / emailapigo — era `2.x` email system task pack

This pack decomposes `lambda/emailapis` and `lambda/emailapigo` work into Contract, Service, Surface, Data, and Ops tracks for the **Contact360 email system** era.

## Runtime split file map (Python vs Go)

Grounded in [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md).

| Runtime | Entrypoint | Router | Core services (start here) |
| --- | --- | --- | --- |
| Python (`lambda/emailapis`) | `lambda/emailapis/app/main.py` | `lambda/emailapis/app/api/v1/router.py` | `app/services/email_finder_service.py`, `email_verification_service.py`, `email_pattern_service.py` |
| Go (`lambda/emailapigo`) | `lambda/emailapigo/main.go` | `lambda/emailapigo/internal/api/router.go` | `internal/services/email_finder_service.go`, `email_verification_service.go`, `email_pattern_service.go` |

## Endpoint contract reference (docs → runtime parity)

- Primary matrix: `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`
- Required CI gate: “docs matrix → runtime routes/payloads” parity for all `2.x` touched endpoints

## Cross-service risks (from codebase analysis)

1. **Provider drift:** Python/docs may reference `truelist`; Go runtime may prioritize `mailvetter` — registry must be single source of truth.  
2. **Status semantic drift:** `valid` / `invalid` / `catchall` / `unknown` (and roadmap-specific labels) must map identically across app, gateway, and Lambdas.  
3. **Observability gap:** Correlate **app → api → jobs → lambda** with one **request id** (and optional trace parent).  
4. **Contract drift:** Docs/backend matrices may lag runtime — CI parity required.  
5. **Bulk correctness:** Partial-batch errors and retries must not double-charge or drop rows silently.

---

## Contract tasks

- [ ] Define and freeze era **`2.x`** email endpoint and payload compatibility notes (finder, verifier, pattern, bulk batch).  
- [ ] Update endpoint/reference matrix: `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`.  
- [ ] Publish **provider parity matrix**: same input → normalized output for **Python vs Go** adapters (golden fixtures).  
- [ ] Freeze **status vocabulary** table consumed by Appointment360 GraphQL mappers.  
- [ ] Document **bulk partial-batch** semantics: which rows retry, which are terminal, how errors surface in `job_response`.

### Provider drift — make it actionable

The codebase analysis explicitly flags this risk:

- Python/docs often mention **`truelist`**.
- Go runtime health/runtime design often prefers **`mailvetter`** (behind a “mailvetter_configured” readiness check).

Gate for `2.6.x` (Provider Harmonization):

- [ ] Provider registry exists as a single source of truth (no undocumented names).
- [ ] Golden fixtures verify: same inputs → same normalized outputs across Python and Go.

## Service tasks

- [ ] Implement/validate runtime behavior for era **`2.x`** finder, verifier, pattern, and fallback paths.  
- [ ] Verify auth, provider routing, **error envelope**, and health diagnostics behavior.  
- [ ] Propagate **`X-Request-ID`** (or equivalent) from gateway into Lambda logs.  
- [ ] Align **credit correlation**: accept gateway context headers or payload fields for billing traces (see `2.9` minor).

## Surface tasks

- [ ] Document impacted pages/tabs/buttons/inputs/components for era **`2.x`** (Email Studio, bulk flows).  
- [ ] Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio).

## Data tasks

- [ ] Document **`email_finder_cache`** and **`email_patterns`** lineage impact for era **`2.x`**.  
- [ ] Record provider, status, and traceability expectations for this era (cache key includes provider/version if needed).

## Ops tasks

- [ ] Add observability checks and release validation evidence for era **`2.x`** (latency, error rate by adapter).  
- [ ] Capture rollback and incident-runbook notes for email-impacting releases.  
- [ ] Add **contract tests** in CI: docs ↔ runtime for critical routes.

## Completion gate

- [ ] Parity tests green for shared golden cases (Python/Go).  
- [ ] No undocumented provider name in production config.  
- [ ] Request id visible in a sample distributed trace across at least **api + lambda**.
