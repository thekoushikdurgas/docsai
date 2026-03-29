---
title: "contact360.io/sync — era matrix"
source_json: connectra_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# contact360.io/sync

## Service metadata

| Field | Value |
| --- | --- |
| service | contact360.io/sync |
| base_path | / |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| POST | /contacts/ | 3.x, 4.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| POST | /contacts/count | 3.x, 6.x, 8.x, 9.x, 10.x |
| POST | /contacts/batch-upsert | 3.x, 4.x, 6.x, 7.x, 8.x, 9.x |
| POST | /companies/ | 3.x, 4.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| POST | /companies/count | 3.x, 6.x, 8.x, 9.x, 10.x |
| POST | /companies/batch-upsert | 3.x, 4.x, 6.x, 7.x, 8.x, 9.x |
| POST | /common/batch-upsert | 2.x, 3.x, 4.x, 6.x, 8.x, 9.x |
| GET | /common/upload-url | 2.x, 3.x, 6.x, 8.x, 10.x |
| POST | /common/jobs | 2.x, 3.x, 6.x, 8.x, 10.x |
| POST | /common/jobs/create | 2.x, 3.x, 6.x, 8.x, 10.x |
| GET\\|POST | /common/:service/filters | 3.x, 4.x, 5.x, 8.x, 9.x, 10.x |
| GET\\|POST | /common/:service/filters/data | 3.x, 4.x, 5.x, 8.x, 9.x, 10.x |
| GET | /health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |


## era_focus

| Era | Focus |
| --- | --- |
| 0.x | service bootstrap, middleware, and health baseline |
| 1.x | credit-aware query/export interaction contracts |
| 2.x | bulk import/export and job orchestration contracts |
| 3.x | core VQL search, filter taxonomy, dual-store write/read |
| 4.x | extension and sales navigator ingestion parity |
| 5.x | AI-readable filter/query surfaces |
| 6.x | query/export SLO, retry model, and reliability hardening |
| 7.x | deployment governance, RBAC on write paths, and auditability |
| 8.x | public/private API versioning and partner-safe endpoint behavior |
| 9.x | tenant-aware quota/throttle and connector safety |
| 10.x | campaign audience/suppression and compliance-ready exports |


## references

- docs/codebases/connectra-codebase-analysis.md
- docs/3. Contact360 contact and company data system/connectra-service.md
- docs/backend/apis/03_CONTACTS_MODULE.md
- docs/backend/apis/04_COMPANIES_MODULE.md

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `contact360.io/sync`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `connectra_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
