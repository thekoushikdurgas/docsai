# logs.api — era `3.x` contact and company data

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks for **search**, **import/export**, **dedup**, and **data-quality diagnostics**.

## Recommended event schema (`3.x`)

Use stable `event_type` strings; version with suffix only when breaking.

| Domain | Example `event_type` | Payload highlights |
| --- | --- | --- |
| Search | `contact.search.query` / `company.search.query` | `user_uuid`, `request_id`, `vql_hash`, `result_count`, `duration_ms` (avoid raw VQL text in high-volume logs unless policy allows) |
| Search result | `contact.search.result` | optional aggregate only — prefer counts, not row payloads |
| Import | `contact360.import.started` / `contact360.import.completed` / `contact360.import.failed` | `job_id`, `rows_total`, `rows_written`, `error_count`, `s3_input_key` |
| Export | `contact360.export.started` / `contact360.export.completed` / `contact360.export.failed` | `job_id`, `vql_hash`, `rows_exported`, `artifact_key` |
| Dedup | `contact.dedup.merged` / `contact.dedup.created` | `uuid`, `source`, `prior_uuid` (if applicable), **no full PII blob** |
| Drift | `connectra.drift.detected` | `entity`, `drift_count`, `severity`, `reconcile_job_id` |
| VQL validate | `jobs.vql.validate_failed` | `reason_code`, `field`, `job_id` |

**PII rule:** log **hashes**, **counts**, and **ids**; full email/phone only in restricted, short-retention debug streams if required.  

**Data-enrichment / search diagnostics (roadmap `3.x` cross-cutting):** emit structured events when enrichment stages alter completeness scores or when search paths degrade (timeouts, partial ES results).

---

## Contract tasks

- [ ] Define and freeze era **`3.x`** logging schema additions and compatibility notes.  
- [ ] Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.  
- [ ] Document **query window** defaults for support (e.g. last 7d search, last 30d jobs).  

## Service tasks

- [ ] Implement/validate service behavior for era **`3.x`** event sources (Connectra, jobs, gateway) and query expectations.  
- [ ] Verify auth, error envelope, and health behavior for consuming services (**internal-first**).  

## Surface tasks

- [ ] Document impacted admin/support pages for era **`3.x`**.  
- [ ] Document relevant hooks/services/contexts and UX states (loading/error/progress).  

## Data tasks

- [ ] Document **S3 CSV** storage and lineage impact for era **`3.x`**.  
- [ ] Record **retention**, **trace IDs**, and cardinality limits on labels for exported metrics.  
- [ ] **Bulk scale:** rollover size for CSV files when import/export volume grows; partition keys (`date`, `tenant_id`).  

## Ops tasks

- [ ] Add observability checks and release validation evidence for era **`3.x`**.  
- [ ] Capture rollback and incident-runbook notes for logging-impacting releases.  
- [ ] Dashboards: search P95, import/export failure ratio, dedup merge rate, drift detection count.  

## Completion gate

- [ ] Synthetic **export job** emits `contact360.export.completed` queryable within SLA.  
- [ ] Support runbook links **request_id** across app → api → Connectra → logs.api for one ticket.
