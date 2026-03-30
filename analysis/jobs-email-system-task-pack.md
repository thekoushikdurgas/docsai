# jobs — era `2.x` email system task pack

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks for **email finder export**, **email verify export**, and **email pattern import** streaming pipelines.

## Codebase file map (processors + lifecycle)

Grounded in [`docs/codebases/jobs-codebase-analysis.md`](../codebases/jobs-codebase-analysis.md).

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| API entrypoint | `contact360.io/jobs/app/api/main.py` | FastAPI app bootstrap |
| Job routes | `contact360.io/jobs/app/api/v1/routes/jobs.py` | Create/list/status/retry/timeline endpoints |
| Scheduler/consumers | `contact360.io/jobs/app/workers/scheduler.py`, `consumer.py` | Lifecycle transitions: open → in_queue → processing → completed/failed |
| Processor registry | `contact360.io/jobs/app/processors/` | `job_type` → processor implementation mapping |
| Email stream processors | `contact360.io/jobs/app/processors/email_finder_export_stream.py`, `email_verify_export_stream.py`, `email_pattern_import_stream.py` | Primary `2.x` email bulk processors |

## API contract reference (service surface)

From the jobs codebase analysis “API contract snapshot”:

- `POST /api/v1/jobs/email-export`
- `POST /api/v1/jobs/email-verify`
- `POST /api/v1/jobs/email-pattern-import`
- `GET /api/v1/jobs/{uuid}` + `/status` + `/timeline` + `/dag`
- `PUT /api/v1/jobs/{uuid}/retry`

## DAG schema reference (scheduler-owned DB)

Tables (minimum fields that must stay consistent with UI expectations):

- `job_node`: `uuid`, `job_type`, `status`, `checkpoint_byte`, `processed_rows`, `total_bytes`, `job_response` (JSONB)
- `edges`: `source`, `target`
- `job_events`: `job_uuid`, `event_type`, `event_data`, `timestamp` (powers timelines)

## Stream processors (canonical names)

- [ ] `email_finder_export_stream` — CSV in → finder batching → S3 output.  
- [ ] `email_verify_export_stream` — CSV in → Mailvetter/email API batching → S3 output.  
- [ ] `email_pattern_import_stream` — pattern CSV → validation → persistence hooks.

Freeze **processor name strings**, **DAG node types**, and **status** values consumed by the dashboard (`useNewExport`, job list APIs).

---

## Contract tasks

- [ ] Freeze contracts for `email_finder_export_stream`, `email_verify_export_stream`, and `email_pattern_import_stream` (inputs, outputs, terminal states).  
- [ ] Keep endpoint and **status semantics** aligned with UI progress expectations (percent, processed/total, failure counts).  
- [ ] Document **checkpoint** fields: byte offset or row cursor, idempotent resume rules.  
- [ ] Define **`job_node.data`** metadata for **`2.x` billing alignment**: `user_uuid`, `billing.correlation_id`, optional `credit_estimate`, `rows_total` — see `version_2.9`.  
- [ ] **Retry policy:** which failures are worker-retriable vs terminal; no duplicate credit charge on successful retry (coordinate with gateway).

## Service tasks

- [ ] Validate stream processor behavior for **large CSV** inputs (memory bounds, backpressure).  
- [ ] Enforce **retry and checkpoint** semantics for email flows; kill/restart worker test passes.  
- [ ] Concurrency targets per roadmap: finder stream **3**, verifier stream **5** (tune via config; document).  
- [ ] Batch calls to `emailapis` / `emailapigo` / Mailvetter with **bounded concurrency** and backoff.

## Surface tasks

- [ ] Document email **bulk** pages using job status, timeline, and retry controls.  
- [ ] Cover mapping checkboxes/radio controls and **progress bar** states (match Mailvetter/job percent contract).

### UI bindings (where this appears in the product)

- `docs/frontend/jobs-ui-bindings.md` (primary)
- `docs/frontend/pages/jobs_page.json` and `docs/frontend/pages/files_page.json` (UI inventory / controls / flows)

## Data tasks

- [ ] Document input/output **CSV lineage** and error envelopes in `job_response` / job store.  
- [ ] Record **checkpoint-byte** and **processed-row** meaning for email workflows.  
- [ ] Link **output S3 key** to `job_id` for support (see `logsapi` pack).

## Ops tasks

- [ ] Add **throughput** and **failure-rate** observability for email jobs.  
- [ ] Add runbook steps for external provider failures and retries.  
- [ ] **Billing-impact alerts:** job failure rate spike after bulk start; stuck checkpoint; output missing.

## Completion gate

- [ ] E2E: upload → process → download **success**.  
- [ ] E2E: mid-run worker failure → **resume** completes without duplicate charges.  
- [ ] Dashboard progress matches processor **processed/total** within one refresh interval.
