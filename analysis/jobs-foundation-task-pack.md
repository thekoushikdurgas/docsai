# jobs task pack — era `0.x` (`contact360.io/jobs`)

This pack decomposes **`contact360.io/jobs`** (TKD Job / scheduler stack) into Contract, Service, Surface, Data, and Ops tracks for foundation readiness before heavy `2.x`+ email and import workloads.

| Track | Owner (default) | Priority |
| --- | --- | --- |
| Contract | Platform backend | P0 |
| Service | Platform backend | P0 |
| Surface | Frontend + docs | P1 |
| Data | Platform backend | P0 |
| Ops | Platform / DevOps | P0 |

## Contract tasks

- Freeze baseline **scheduler HTTP API**: job `create`, `status`, `timeline` (or equivalent), `retry` — request/response shapes and error codes. (patch assignment: `0.6.0`–`0.6.2`)
- Freeze **health contract**: `/health`, `/health/live`, `/health/ready` semantics and what “ready” means (Kafka, DB, Redis if applicable). (patch assignment: `0.6.0`–`0.6.2`)
- Document **Kafka topic** name(s) (e.g. `JOBS_TOPIC`) and producer/consumer ownership for `0.x`. (patch assignment: `0.6.0`–`0.6.2`)
- Capture **idempotency** expectations for `create` and retry (even if minimal in `0.x`). (patch assignment: `0.6.0`–`0.6.2`)

## Service tasks

- Stabilize **API**, **scheduler**, **consumer**, and **worker** processes: ordered startup, config validation, graceful shutdown. (patch assignment: `0.6.0`–`0.6.2`)
- Validate **processor registry** bootstrap: known processor types register without panic; unknown types fail fast with clear errors. (patch assignment: `0.6.0`–`0.6.2`)
- Validate **DAG insertion** baseline: `job_node` + `edges` accepted; cycle detection or validation errors are explicit. (patch assignment: `0.6.0`–`0.6.2`)
- Wire **stale recovery** hooks for `PROCESSING_TIMEOUT` / `JOB_EXECUTION_TIMEOUT` (or document “not yet implemented” with ticket). (patch assignment: `0.6.0`–`0.6.2`)

## Surface tasks

- Document baseline **jobs** UI in `contact360.io/app`:
  - `components/jobs/JobsCard.tsx` stub renders job list/card + status badge
  - `components/jobs/JobsPipelineStats.tsx` stub renders processed/failed/pending segments
  - status badge mapping uses design-token colors from `docs/frontend/design-system.md` (patch assignment: `0.6.3`–`0.6.6`)
- Stub `hooks/useJobs.ts` (poll every ~15s as documented) and return empty state when no jobs. (patch assignment: `0.6.3`–`0.6.6`)
- Document **progress** indicators and expected refresh intervals for foundation-era flows. (patch assignment: `0.6.3`–`0.6.6`)

## Data tasks

- Establish Alembic (or equivalent) **migration baseline** for `job_node`, `edges`, `job_events` (and any scheduler metadata tables). (patch assignment: `0.6.0`–`0.6.2`)
- Document **status vocabulary** and allowed transitions (state machine diagram or table in `docs/backend` or codebase README). (patch assignment: `0.6.0`–`0.6.2`)
- Note **retention**: how long `job_events` live in `0.x` (even if “unbounded — TBD”). (patch assignment: `0.6.0`–`0.6.2`)

## Ops tasks

- Add **local and staging smoke**: create → worker picks up → terminal state → timeline readable. (patch assignment: `0.6.0`–`0.6.2`)
- Add **scheduler liveness** check playbook (what to restart, in what order). (patch assignment: `0.6.0`–`0.6.2`)
- Capture **stale-processing recovery** runbook one-pager: symptom → metric → mitigation. (patch assignment: `0.6.0`–`0.6.2`)

## Release gate evidence (`0.x`)

- [ ] Health endpoints pass in CI or manual smoke checklist (patch assignment: `0.6.7`–`0.6.9`)
- [ ] One end-to-end job completes with persisted `job_events` (patch assignment: `0.6.7`–`0.6.9`)
- [ ] Migration applied cleanly on empty DB (patch assignment: `0.6.7`–`0.6.9`)
- [ ] README or runbook link from `docs/codebase.md` / service README (patch assignment: `0.6.7`–`0.6.9`)
