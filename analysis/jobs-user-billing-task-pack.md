# jobs task pack — era 1.x

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks.

## Codebase evidence (contact360.io/jobs)

- Entrypoint/API:
  - `contact360.io/jobs/app/api/main.py`
  - router: `contact360.io/jobs/app/api/v1/routes/jobs.py`
- Scheduler / execution:
  - scheduler: `contact360.io/jobs/app/workers/scheduler.py`
  - consumer: `contact360.io/jobs/app/workers/consumer.py`
  - worker pool: `contact360.io/jobs/app/workers/worker_pool.py`
  - processor registry: `contact360.io/jobs/app/processors/`
- Billing correlation mechanism:
  - gateway passes billing metadata into `job_node.data` (must include `user_uuid`, `billing.correlation_id`, and `billing.credit_estimate` when applicable).

## Scheduler-owned data model (billing-aware fields)

### `job_node`

Expected core columns (jobs DB):
- `uuid` (PK)
- `job_title`, `job_type`, `degree`, `priority`, `status`
- `data` (JSONB) → owner + billing metadata
- `job_response` (JSONB) → result envelope + reconciliation inputs
- `try_count`, `retry_interval`, `run_after`
- checkpoint/progress:
  - `checkpoint_byte`, `processed_rows`, `total_bytes`
  - `checkpoint_uuid`, `checkpoint_data`
- timestamps: `created_at`, `updated_at`, `deleted_at`

### `job_events`

- `id` (PK)
- `job_uuid` (FK → `job_node.uuid`)
- `event_type` (e.g., `open`, `in_queue`, `processing`, `completed`, `failed`, plus billing checkpoints)
- `event_data` (JSONB) → row counts, error envelopes, credit checkpoint metadata
- `timestamp`

### `edges`

- `source` (FK → `job_node.uuid`)
- `target` (FK → `job_node.uuid`)

## Contract tasks
- Define credit-aware job creation payload expectations.
- Define billing/audit semantics for retry and cancellation events.

## Service tasks
- Attach billing context to job metadata when applicable.
- Validate access checks between owner/admin and retry controls.

## Surface tasks
- Add billing-aware retry UX states and credit warning patterns.
- Document job ownership and role-gated action visibility.

## Data tasks
- Ensure `job_events` carries credit/billing trace context.
- Document correlation between job IDs and usage/billing records.

## Ops tasks
- Add billing-impact alerts for job failure spikes.
- Add release checklist for billing-flow regression checks.

---

## Credit-aware job creation (1.x contract)

| Field | Location | Purpose |
| --- | --- | --- |
| `user_uuid` | `job_node.data` | Owner for RBAC + usage |
| `billing.correlation_id` | `job_node.data` | Idempotency with gateway credit hold |
| `billing.credit_estimate` | `job_node.data` | Pre-flight UI display |
| `billing.charged_rows` | `job_response` or events | Actuals for reconciliation |
| `org_id` or `tenant_id` | optional JSONB | Future multi-tenant billing |

### Validation rules

- [ ] Reject create if **pre-check credits** fails at gateway (preferred) or at jobs with explicit error code.
- [ ] Retry: **no duplicate charge** — same `correlation_id` replays must not increment usage twice.
- [ ] Cancel: document whether reserved credits **release** immediately or after TTL.

### `job_events` billing trace

- [ ] Emit `credit_checkpoint` events with row counts + running charge totals where applicable.
- [ ] Admin retry: include `actor` in event payload for audit.

### Billing-impact alerts

- [ ] Threshold: spike in `failed` bulk jobs for **paid** users (tagged via metadata).
- [ ] Divergence: `charged_rows` sum vs gateway usage over sliding window — page on-call playbook.

### Cross-service correlation evidence

- Every reconciliation attempt must be traceable using:
  - `job_uuid` (jobs timeline),
  - `billing.correlation_id` (ledger/idempotency grouping),
  - gateway request/trace IDs (propagated from Appointment360 middleware).

**Reference:** [`docs/codebases/jobs-codebase-analysis.md`](../codebases/jobs-codebase-analysis.md)
