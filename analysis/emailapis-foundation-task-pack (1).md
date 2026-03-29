# emailapis task pack — era `0.x`

This pack decomposes `lambda/emailapis` and `lambda/emailapigo` work into Contract, Service, Surface, Data, and Ops tracks for the **foundation** era only.

| Track | Owner (default) | Priority |
| --- | --- | --- |
| Contract | Backend / platform | P0 |
| Service | Backend | P0 |
| Surface | Frontend + docs | P1 |
| Data | Backend + data | P0 |
| Ops | Platform / DevOps | P0 |

## Contract tasks

- Define and freeze **`0.x`** email endpoint and payload compatibility notes (finder, verifier, pattern, health). (patch assignment: `0.3.0`–`0.3.2`)
- Update endpoint/reference matrix in `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`. (patch assignment: `0.3.0`–`0.3.2`)
- Align error envelope and auth header contract with `appointment360` GraphQL clients that call these Lambdas. (patch assignment: `0.3.0`–`0.3.2`)

## Service tasks

- Implement/validate runtime behavior for **`0.x`** finder, verifier, pattern, and fallback paths. (patch assignment: `0.3.0`–`0.3.2`)
- Verify auth, provider routing, error envelope, and health diagnostics behavior. (patch assignment: `0.3.0`–`0.3.2`)
- Confirm `lambda/emailapigo` parity with shared models / expectations documented for `lambda/emailapis` where both are in scope. (patch assignment: `0.3.0`–`0.3.2`)

## Surface tasks

- Document impacted dashboard pages/tabs/buttons/inputs/components for **`0.x`** (minimal: health/finder/verifier entry points only if exposed). (patch assignment: `0.3.3`–`0.3.6`)
- Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio). (patch assignment: `0.3.3`–`0.3.6`)
- Surface binding reference: `docs/frontend/emailapis-ui-bindings.md` (era `0.x` rows for health/finder/verifier UI scaffolding).

## Data tasks

- Document `email_finder_cache` and `email_patterns` lineage impact for **`0.x`**. (patch assignment: `0.3.0`–`0.3.2`)
- Record provider, status, and traceability expectations for this era. (patch assignment: `0.3.0`–`0.3.2`)

## Ops tasks

- Add observability checks and release validation evidence for **`0.x`**. (patch assignment: `0.3.7`–`0.3.9`)
- Capture rollback and incident-runbook notes for email-impacting releases. (patch assignment: `0.3.3`–`0.3.6`)

---

## Provider drift and parity (`lambda/emailapis` vs `lambda/emailapigo`)

From [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md). Primary minors: **`0.3`** (contracts), **`2.x`** readiness (capabilities).

### Python / Go parity matrix

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Maintain matrix: endpoint × field × Python vs Go behavior (finder, verifier, pattern, bulk) | P0 | Stale matrix = production drift | `0.3.0`–`0.3.2` |
| CI check or periodic diff script: shared response model keys | P1 | | `0.3.3`–`0.3.6` |
| Document **which** runtime is canonical for each route in `0.x` | P0 | | `0.3.0`–`0.3.2` |

### Status semantic vocabulary freeze

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Single table: provider raw status → **platform** status enum (per finder/verifier) | P0 | Analysis: semantic drift | `0.3.0`–`0.3.2` |
| GraphQL mapping doc for Appointment360 consumers | P0 | | `0.3.0`–`0.3.2` |
| Deprecation policy for status renames | P1 | | `0.3.3`–`0.3.6` |

### Bulk correctness test baseline

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Golden bulk fixture: N≥100 emails — compare counts, ordering guarantees, partial failure behavior | P0 | | `0.3.0`–`0.3.2` |
| Idempotency: repeat submission policy documented | P0 | | `0.3.0`–`0.3.2` |
| Load test **not** in `0.x` — correctness first | — | | N/A (out of scope for `0.x`) |

### Observability — request correlation

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Accept propagate **`X-Request-ID`** (and optional traceparent) from gateway | P0 | | `0.3.0`–`0.3.2` |
| Include id in **all** provider call logs and error envelopes | P0 | | `0.3.0`–`0.3.2` |
| Health endpoint returns build version / git sha | P1 | `0.10` matrix | `0.3.3`–`0.3.6` |

**Reference:** [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md)
