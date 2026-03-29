# Jobs Service (`contact360.io/jobs`) — Era `6.x` Reliability & Scaling Task Pack

### Context

The scheduler and worker plane for **tkdjob** must guarantee **idempotent create/retry**, **DLQ + authorized replay**, recovery from **stale `processing`**, and an auditable **`job_events`** trail. This pack mirrors the five-track structure of [`emailcampaign-reliability-scaling-task-pack.md`](emailcampaign-reliability-scaling-task-pack.md) and ties to roadmap **Stages 6.2–6.4** (idempotency), **6.3** (queues), and **6.9** (RC evidence).

**Codebase reference:** [`docs/codebases/jobs-codebase-analysis.md`](../codebases/jobs-codebase-analysis.md).

---

## Track A — Contract

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| A-6.1 | **Idempotent create** | `POST` job create with same natural key (or `Idempotency-Key` header) returns **200 + same job_id**; no duplicate DAG side effects. | Backend |
| A-6.2 | **Retry state machine** | Document `queued` → `processing` → `retry` / `failed` / `succeeded`; max attempts; terminal reasons. | Backend |
| A-6.3 | **DLQ envelope** | Poison messages include: `job_id`, `failure_class` (`transient` vs `permanent`), `trace_id`, payload hash, `last_error`. | Backend |
| A-6.4 | **Replay authorization** | Only roles/scripts with `replay:dlq` (or equivalent) may trigger replay; audit event to `job_events`. | Security + Backend |
| A-6.5 | **Trace in payload** | Queued work carries `X-Trace-Id` / W3C context for 6.4 correlation. | Backend |

---

## Track B — Service

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| B-6.1 | **Idempotent create implementation** | DB unique constraint or idempotency store; conflict returns existing row. | Backend |
| B-6.2 | **DLQ path** | Non-retryable errors route to DLQ topic/table; metric `jobs_dlq_total{reason}`. | Backend |
| B-6.3 | **Replay endpoints** | Admin/API: list DLQ, replay by id, bulk replay with limit; **dry-run** mode. | Backend |
| B-6.4 | **Stale-processing recovery** | Sweeper marks jobs stuck in `processing` > **T** minutes as `failed` or `retry` based on heartbeats. | Backend |
| B-6.5 | **Downstream degree / DAG** | Blocked nodes clearly reported; dependency failures do not wedge scheduler. | Backend |
| B-6.6 | **Graceful shutdown** | Drain in-flight work; finish or requeue with lease. | Backend |

---

## Track C — Surface

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| C-6.1 | **Operator UI / CLI** | Expose DLQ depth, last errors, replay action (protected). | Platform |
| C-6.2 | **Dashboards** | Panels: queue depth, processing age histogram, DLQ rate, replay success. | SRE |
| C-6.3 | **Customer-visible status** | If product surfaces job status: loading/error/retry consistent with [`docs/frontend/components.md`](../frontend/components.md) Era 6. | Frontend |

---

## Track D — Data

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| D-6.1 | **`job_events` audit** | Append-only: `created`, `started`, `retry`, `dlq`, `replay`, `completed`; include actor for replay. | Backend |
| D-6.2 | **Idempotency keys** | Table or column for create key; TTL policy if separate store. | Backend |
| D-6.3 | **Lineage** | Document scheduler DB tables in [`docs/backend/database/`](../backend/database/) when schema changes. | Docs |

---

## Track E — Ops

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| E-6.1 | **SLOs & alerts** | SLI: job completion latency P95; schedule success rate; alert on DLQ growth > threshold. | SRE |
| E-6.2 | **Chaos drills** | Kill worker mid-job → job becomes retryable or visible in DLQ; no silent loss. | SRE |
| E-6.3 | **Runbook** | Link from [`queue-observability.md`](queue-observability.md) — failure classes & replay procedure. | SRE |
| E-6.4 | **RC evidence** | Export last drill date + dashboard snapshot for [`reliability-rc-hardening.md`](reliability-rc-hardening.md). | Release Eng |

---

## DLQ / replay quick reference

| Step | Action |
| --- | --- |
| 1 | Confirm `trace_id` in logs for failing job |
| 2 | Classify: transient (replay) vs permanent (fix code/config) |
| 3 | Authorize replay operator |
| 4 | Replay single job; verify `job_events` entry |
| 5 | Watch error budget / DLQ depth |

---

## Completion gate

- [ ] Idempotent create proven by duplicate POST test (staging).
- [ ] At least one DLQ message successfully replayed with audit trail.
- [ ] Stale-processing sweeper verified in soak test.
- [ ] SLO panels + alert routes live; chaos drill documented.
