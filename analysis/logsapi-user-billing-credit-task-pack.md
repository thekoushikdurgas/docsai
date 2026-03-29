# logs.api task pack — era 1.x

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks.

## Codebase evidence (lambda/logs.api)

- Entrypoint: `lambda/logs.api/app/main.py`
- Routing:
  - `app/api/v1/endpoints/logs.py`
  - `app/api/v1/endpoints/health.py`
- Service layer: `app/services/log_service.py`
- Data repository: `app/models/log_repository.py`
- Storage client: `app/clients/s3.py`
- Deployment contract: `lambda/logs.api/template.yaml`
- Canonical ingestion/query endpoints snapshot:
  - `POST /logs`, `POST /logs/batch`
  - `GET /logs`, `GET /logs/search`, `GET /logs/{log_id}`
  - `PUT /logs/{log_id}`, `DELETE /logs/{log_id}`
  - `POST /logs/delete`, `DELETE /logs`
  - health: `GET /health`, `GET /health/info`

## Contract tasks
- Define and freeze era `1.x` logging schema additions and compatibility notes.
- Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.

## Service tasks
- Implement/validate service behavior for era `1.x` event sources and query expectations.
- Verify auth, error envelope, and health behavior for consuming services.

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era `1.x`.
- Document relevant hooks/services/contexts and UX states (loading/error/progress/check/radio).

## Data tasks
- Document S3 CSV storage and lineage impact for era `1.x`.
- Record retention, trace IDs, and query-window expectations.

## Ops tasks
- Add observability checks and release validation evidence for era `1.x`.
- Capture rollback and incident-runbook notes for logging-impacting releases.

---

## 1.x — Auth, billing, and credit event schema

Canonical store remains **S3 CSV** (not MongoDB). Cross-link [`docs/backend/database/logsapi_data_lineage.md`](../backend/database/logsapi_data_lineage.md) and `lambda/logs.api/docs/api.md`.

### Recommended event categories (extend `1.x` schema doc)

| Event type | Required fields | Notes |
| --- | --- | --- |
| `auth.login_success` | `user_uuid`, `request_id`, `timestamp`, `ip_hash` | No passwords |
| `auth.login_failure` | `email_hash`, `request_id`, `reason` | Rate-limit friendly |
| `credit.deduct` | `user_uuid`, `feature`, `amount`, `balance_after`, `correlation_id` | Tie to gateway ledger (`credits`) and idempotency grouping |
| `billing.payment_submitted` | `user_uuid`, `submission_id`, `request_id`, `proof_url` (or S3 key only) | After proof upload; avoid PII duplication |
| `billing.payment_approved` | `actor_admin_uuid`, `submission_id`, `credits_granted`, `request_id` | Audit; must align with `payment_submissions.status=approved` |
| `billing.payment_declined` | `actor_admin_uuid`, `submission_id`, `reason`, `request_id` | Must align with `payment_submissions.status=declined` |
| `job.bulk_started` / `job.bulk_completed` | `job_uuid`, `user_uuid`, `rows`, `credits_reserved` | Pair with jobs pack |

### Query scope for admin billing views

- [ ] Time-windowed queries with **hard cap**; index or partition strategy documented for `1.x` CSV prefixes.
- [ ] Role-gated filters: staff-only queries for payment + credit adjust events.
- [ ] PII classification: proof artifacts **not** duplicated in logs — reference S3 key only.

### Retention

- [ ] Default retention for `1.x` billing/auth events (e.g. 90d / 1y) documented in pack + `audit-compliance.md` alignment.
- [ ] Legal hold bypass procedure stub for finance.

**Reference:** [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md)
