# logs.api — era `2.x` email system task pack

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks for **email workflow** and **bulk processing** telemetry.

Grounded in [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md) (canonical store is **S3 CSV**, not MongoDB).

## Codebase file map (high-value for `2.x`)

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| Entrypoint | `lambda/logs.api/app/main.py` | FastAPI app bootstrap |
| Route handlers | `lambda/logs.api/app/api/v1/endpoints/logs.py` | Write/query/search endpoints |
| Service layer | `lambda/logs.api/app/services/log_service.py` | Validation + storage orchestration |
| Repository | `lambda/logs.api/app/models/log_repository.py` | S3 CSV storage mechanics |
| S3 client | `lambda/logs.api/app/clients/s3.py` | Object read/write helpers |

## Recommended event categories (`2.x`)

Use consistent `event_type` (or equivalent) strings; extend only with version suffixes.

| Category | Example `event_type` | Payload highlights | retention_days | query_window_days |
| --- | --- | --- | --- | --- |
| Finder | `email.finder.request` / `email.finder.response` | `user_uuid`, `request_id`, provider, latency_ms, result_count (no raw PII in aggregates) | TBD | TBD |
| Verifier | `email.verifier.request` / `email.verifier.response` | status enum, confidence_band, mailvetter_job_id | TBD | TBD |
| Bulk job | `email.bulk.job_created` / `email.bulk.progress` / `email.bulk.completed` / `email.bulk.failed` | `job_id`, `processor`, `processed`, `total`, `checkpoint`, `output_s3_key` | TBD | TBD |
| Storage | `email.s3.multipart.completed` | `upload_id`, `bucket`, `key_prefix` | TBD | TBD |
| Credit | `email.credit.deduct` | `feature`, `amount`, `correlation_id` (align gateway) | TBD | TBD |

**PII rule:** prefer **hashed email** or **row index** in high-volume logs; full addresses only in restricted, short-retention debug streams if absolutely required.

---

## Contract tasks

- [ ] Define and freeze era **`2.x`** logging schema additions and compatibility notes.  
- [ ] Update endpoint/reference matrix: `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.  
- [ ] Document **query filters** for support/admin: by `user_uuid`, `job_id`, `request_id`, time window.

## Service tasks

- [ ] Implement/validate service behavior for era **`2.x`** event sources (jobs processors, gateway, Lambdas) and query expectations.  
- [ ] Verify auth, error envelope, and health behavior for consuming services (**internal** consumers only unless explicitly exposed).

## Surface tasks

- [ ] Document impacted admin/support pages (if any) for era **`2.x`**.  
- [ ] Document relevant hooks/services/contexts and UX states (loading/error/progress).

## Data tasks

- [ ] Document **S3 CSV** storage and lineage impact for era **`2.x`** (canonical store pattern).  
- [ ] Record **retention**, **trace IDs**, and **query-window** expectations.  
- [ ] **Bulk scale:** partitioning, file rollover size, and max events/sec assumptions; cardinality limits on labels for metrics export.

### Docs parity gate (avoid drift)

- [ ] Any docs that still describe logs.api as MongoDB-backed must be updated: implementation is S3 CSV (see `docs/codebases/logsapi-codebase-analysis.md`).

## Ops tasks

- [ ] Add observability checks and release validation evidence for era **`2.x`**.  
- [ ] Capture rollback and incident-runbook notes for logging-impacting releases.  
- [ ] Dashboards: **queue lag**, **processor throughput**, **error rate by processor** (tie to `version_2.8`).

## Completion gate

- [ ] Synthetic **bulk job** produces a queryable trail in logs.api within SLA.  
- [ ] Retention policy documented and enforced for email-related CSV partitions.
