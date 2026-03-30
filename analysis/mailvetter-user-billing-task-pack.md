# Mailvetter — 1.x User/Billing/Credit Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `1.x` — User, billing, and credit alignment

## Codebase evidence (backend(dev)/mailvetter)

- Stack:
  - runtime: Go (Go 1.25)
  - HTTP: Gin (`gin-gonic/gin`)
  - DB: PostgreSQL via `pgx/v5/pgxpool`
  - Queue: Redis (`go-redis/v9`) with list `tasks:verify`
  - Workers: in-process worker pool (`cmd/worker`)
- API route surface (authenticated v1 routes):
  - `GET /v1/health`
  - `POST /v1/emails/validate` (single verification)
  - `POST /v1/emails/validate-bulk` (async bulk verification)
  - `GET /v1/jobs/:job_id` (job status)
  - `GET /v1/jobs/:job_id/results` (results export)
- Job model (billing-linked):
  - `jobs` table: `status`, counters (`total_count/processed_count/valid_count/invalid_count`), ownership/routing (`owner_key`, `job_name`), webhook callback fields
  - `results` table: `job_id`, `email`, `score`, `is_valid`, `data` JSONB payload
- Contract risk:
  - dual API surface exists (v1 + legacy routes); freeze legacy behavior for 1.x to avoid drift.

## Contract track

- [ ] Define plan-tier contract (`free`, `pro`, `enterprise`) for rate, bulk, and concurrent jobs.
- [ ] Define API key ownership contract (`owner_id`, `tenant_id`, `plan`).
- [ ] Define credit-consumption events for single and bulk validation.
- [ ] Map 1.x credit semantics onto these endpoints explicitly:
  - `POST /v1/emails/validate` (single): one-credit-per-verify (gateway policy)
  - `POST /v1/emails/validate-bulk` (bulk): credits charged based on actual job results/counters

## Service track

- [ ] Replace env-only single key fallback with DB-backed key management.
- [ ] Add key scope checks (read-only vs bulk-write permissions).
- [ ] Attach `owner_id` and `tenant_id` to jobs at creation time.
- [ ] Emit usage events on each request for billing reconciliation.
- [ ] Ensure provider scoring/status classification maps to “charged vs not charged vs partial” reconciliation vocabulary.

## Surface track

- [ ] Dashboard usage widgets map verifier usage per plan and remaining limits.
- [ ] Add error messaging for `RATE_LIMIT_EXCEEDED`, `BULK_SIZE_EXCEEDED`, `CONCURRENT_JOB_LIMIT`.
- [ ] Ensure bulk UI can render job-level failures using:
  - `GET /v1/jobs/:job_id`
  - `GET /v1/jobs/:job_id/results`

## Data track

- [ ] Add `api_keys` table (hashed key, owner, plan, active, rotated_at).
- [ ] Add `usage_logs` table for hourly/daily aggregation.
- [ ] Add `credit_events` table for billable operations.

## Ops track

- [ ] Add key rotation runbook and secret separation policy.
- [ ] Add plan enforcement tests across all three tiers.
- [ ] Add billing parity checks against appointment360 usage records.
