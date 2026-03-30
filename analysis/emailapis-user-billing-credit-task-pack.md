# emailapis task pack — era `1.x`

This pack decomposes `lambda/emailapis` and `lambda/emailapigo` work into Contract, Service, Surface, Data, and Ops tracks for the **1.x** user, billing, and credit era.

| Track | Owner (default) | Priority |
| --- | --- | --- |
| Contract | Backend / platform | P0 |
| Service | Backend | P0 |
| Surface | Frontend + docs | P1 |
| Data | Backend + data | P0 |
| Ops | Platform / DevOps | P0 |

## Codebase evidence (lambda/emailapis + lambda/emailapigo)

- Python runtime:
  - entrypoint: `lambda/emailapis/app/main.py`
  - router: `lambda/emailapis/app/api/v1/router.py`
  - finder: `lambda/emailapis/app/services/email_finder_service.py`
  - verifier: `lambda/emailapis/app/services/email_verification_service.py`
  - pattern: `lambda/emailapis/app/services/email_pattern_service.py`
- Go runtime:
  - entrypoint: `lambda/emailapigo/main.go`
  - router: `lambda/emailapigo/internal/api/router.go`
- Billing correlation:
  - Appointment360 passes `X-Request-ID` to correlate email provider calls with gateway `deduct_credit`/usage rows and `logs.api` events.

## Endpoint mapping (finder/verifier/pattern)

- Finder:
  - GraphQL `findEmails` → Lambda POST `/email/finder/`
  - GraphQL `findEmailsBulk` → Lambda POST `/email/finder/bulk`
- Verifier:
  - GraphQL `verifySingleEmail` → Lambda POST `/email/single/verifier/`
  - GraphQL `verifyEmailsBulk` → Lambda POST `/email/bulk/verifier/`
- Patterns:
  - GraphQL `addEmailPattern` → Lambda POST `/email-patterns/add`
  - GraphQL `addEmailPatternBulk` → Lambda POST `/email-patterns/add/bulk`

## Contract tasks

- Define and freeze era **`1.x`** email endpoint and payload compatibility notes (finder, verifier, pattern, bulk, health).
- Update endpoint/reference matrix in `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`.
- Align error envelope and auth header contract with `appointment360` GraphQL clients that call these Lambdas.
- **Credit correlation (1.x):** document how each operation type maps to **gateway `deduct_credit` / usage** (finder vs verifier vs bulk row); ensure **no double charge** when gateway and Lambda both reason about cost.

## Service tasks

- Implement/validate runtime behavior for era **`1.x`** finder, verifier, pattern, bulk, and fallback paths.
- Verify auth, provider routing, error envelope, and health diagnostics behavior.
- Confirm `lambda/emailapigo` parity with shared models / expectations documented for `lambda/emailapis` where both are in scope.
- **Request-ID + billing trace:** accept `X-Request-ID` from Appointment360; include in logs and error payloads to correlate with **usage/billing** rows and `logs.api` events.

## Surface tasks

- Document impacted pages/tabs/buttons/inputs/components for era **`1.x`** (finder, verifier, bulk progress, credit warning).
- Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio).

## Data tasks

- Document `email_finder_cache` and `email_patterns` lineage impact for era **`1.x`**.
- Record provider, status, and traceability expectations for this era.
- **Status vocabulary (1.x):** maintain a single table mapping **provider raw status → platform status → billing impact** (charged vs not charged vs partial); used for ledger reconciliation.

### `email_finder_cache` (identity + result cache)

- Identity keys:
  - `first_name`, `last_name`, `domain` (domain case-insensitive)
- Result fields:
  - `email_found`, `email_source`
- Billing relevance:
  - cache hit must not double-charge (gateway holds charge decision; provider only returns results).

### `email_patterns` (learned pattern persistence)

- Keys:
  - `uuid`, `company_uuid`, `domain`
- Fields:
  - `pattern_format`, `pattern_string`
- Metrics to persist:
  - `contact_count`, `success_rate`, `error_rate`

## Ops tasks

- Add observability checks and release validation evidence for era **`1.x`**.
- Capture rollback and incident-runbook notes for email-impacting releases.
- **Billing regression:** alert when bulk job completion count diverges from expected credit consumption (pair with `jobs-user-billing-task-pack.md`).

---

## 1.x — Credit-aware execution (from gateway perspective)

| Task | Priority | Notes |
| --- | --- | --- |
| Document **per-row** vs **per-job** credit semantics for bulk verify/finder | P0 | Must match `contact360.io/jobs` metadata |
| Failed provider call: **refund or no-charge** policy explicit | P0 | |
| Idempotent bulk chunk: same chunk replay must not **double-bill** | P0 | |
| Parity matrix row: Python vs Go for **billing-relevant** response fields | P0 | See `docs/codebases/emailapis-codebase-analysis.md` |

**References:** [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md) · [`1.x-master-checklist.md`](1.x-master-checklist.md) · [`appointment360-user-billing-task-pack.md`](appointment360-user-billing-task-pack.md)
