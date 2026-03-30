# jobs — era `3.x` contact and company data

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks for **Contact360 import/export** and **VQL validation** aligned with the contact/company data era.

## Processors and endpoints (canonical)

| Job type | Processor | Creation endpoint (typical) |
| --- | --- | --- |
| `contact360_import_prepare` | `contact360_import_prepare` | `POST /api/v1/jobs/contact360-import` |
| `contact360_export_stream` | `contact360_export_stream` | `POST /api/v1/jobs/contact360-export` |

**VQL validation:** `POST /api/v1/jobs/validate/vql` — must stay aligned with dashboard export and [`vql-filter-taxonomy.md`](vql-filter-taxonomy.md).

## Contract tasks

- [ ] Freeze **`contact360_import_prepare`** request/response: CSV/schema hints, target entity, column mapping version, optional user/tenant scope fields.  
- [ ] Freeze **`contact360_export_stream`** request/response: serialized VQL or equivalent, export format, row limits, notification hooks.  
- [ ] Keep **`validate/vql`** behavior aligned with export workflows — errors must match GraphQL converter semantics (unknown fields, invalid ranges).  
- [ ] Document **retry contract:** downstream nodes use explicit `retry` semantics; do not model retry directly from `failed` without scheduler involvement ([`docs/codebases/jobs-codebase-analysis.md`](../codebases/jobs-codebase-analysis.md)).  

## Service tasks

- [ ] Validate import/export stream processors for **PG + OpenSearch** data paths; bounded memory streaming where applicable.  
- [ ] Enforce **dependency-safe DAG** behavior and **degree updates** — known risk: *DAG degree-decrement failure can block downstream nodes*; add diagnostics and manual unblock runbook.  
- [ ] Stale **`processing`** recovery depends on scheduler recovery loop — document timeout + operator action.  

## Surface tasks

- [ ] Document contact/company **import/export** pages and execution graph panels.  
- [ ] Define error and **partial-progress** UX for long-running data jobs (row-level errors vs fatal failure).  

## Data tasks

- [ ] Document lineage across **`job_node`**, target **Postgres** tables, and **OpenSearch** indexes — include `job_id` → artifact keys.  
- [ ] Document **VQL/query payload traceability** in `job_node.data` and `job_response` (hash or normalized JSON pointer).  
- [ ] For exports initiated from UI, store **saved_search_id** or **query fingerprint** for audit (`version_3.4`).  

## Ops tasks

- [ ] Incident runbook for **import/export drift** (counts wrong, index missing rows) and **replay** procedure.  
- [ ] SLI checks: completion latency, failure ratio, *stuck-processing* age.  
- [ ] Alert on **VQL validate** error spike after deploy (signals converter drift).  

## Known gaps (cross-reference)

- Single shared **`X-API-Key`** model in jobs service — no per-user authz in service itself; rely on gateway or future `3.9`/`7.x` hardening.  
- Legacy multi-node Contact360 DAG patterns may exist in docs but not in active registry — reconcile docs vs code when touching this pack.  

## Completion gate

- [ ] E2E: **validate/vql** → export job → artifact download matches count from Connectra `CountByFilters` for same VQL.  
- [ ] Import replay after simulated worker failure yields **idempotent** row counts (no duplicate keys).  
- [ ] Runbook reviewed for **blocked DAG** scenario.
