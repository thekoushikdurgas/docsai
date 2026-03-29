---
title: "contact360.io/jobs — era matrix"
source_json: jobs_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# contact360.io/jobs

## Service metadata

| Field | Value |
| --- | --- |
| service | contact360.io/jobs |
| base_path | /api/v1 |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| POST | /api/v1/jobs/bulk-insert/complete-graph | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/email-export | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/email-verify | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/email-pattern-import | 2.x, 3.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/contact360-import | 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/contact360-export | 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/jobs/ | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/jobs/{uuid} | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/jobs/{uuid}/status | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/jobs/{uuid}/timeline | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/jobs/{uuid}/dag | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| PUT | /api/v1/jobs/{uuid}/retry | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/jobs/validate/vql | 3.x, 4.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| GET | /api/v1/metrics | 0.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/metrics/stats | 0.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /health/live | 0.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /health/ready | 0.x, 6.x, 7.x, 8.x, 9.x, 10.x |


## era_focus

| Era | Focus |
| --- | --- |
| 0.x | scheduler bootstrap, health and baseline contract |
| 1.x | billing/credit-aware job governance and ownership |
| 2.x | email stream processor execution and bulk status UX |
| 3.x | contact/company import-export and VQL validation |
| 4.x | extension and sales navigator provenance jobs |
| 5.x | AI workflow batch orchestration and metadata |
| 6.x | idempotency, retry hardening, stale recovery, SLOs |
| 7.x | role-aware access controls, audit and retention |
| 8.x | public/private API versioning and callback readiness |
| 9.x | tenant-aware quotas, isolation and entitlement scheduling |
| 10.x | campaign compliance evidence and strict idempotency |


## references

- docs/codebases/jobs-codebase-analysis.md
- docs/backend/apis/16_JOBS_MODULE.md
- docs/backend/apis/JOBS_ERA_TASK_PACKS.md
- docs/backend/database/jobs_data_lineage.md
- contact360.io/jobs/app/api/v1/routes/jobs.py

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `contact360.io/jobs`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `jobs_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
