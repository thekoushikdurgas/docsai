---
title: "graphql/ListImportJobs"
source_json: query_list_import_jobs_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListImportJobs

## Overview

List import jobs (CSV import jobs only). Accepts optional ImportJobFilterInput with status (array of status strings) and limit (pagination). Automatically filters for job_type='insert_csv_file' jobs only. Returns JobConnection with items array (Job objects) and total count. Uses ConnectraClient.list_jobs with job_type='insert_csv_file'. Supports filtering by status.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_import_jobs_graphql |
| _id | query_list_import_jobs_graphql-001 |
| endpoint_path | graphql/ListImportJobs |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 5.x |
| introduced_in | 5.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/imports/queries.py |
| router_file | contact360/dashboard/src/services/graphql/importsService.ts |


## GraphQL operation

```graphql
query ListImportJobs($input: ImportJobFilterInput) { imports { importJobs(input: $input) { items { uuid jobType status data createdAt } total } } }
```

## Data & infrastructure

### db_tables_read

- jobs
- scheduler_jobs

### lambda_services

- contact360.io/sync
- contact360.io/jobs

## Service / repository methods

### service_methods

- listImportJobs
- importJobs

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /files | Files Page | importsService | useImportJobs | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/files/page.tsx
- contact360.io/app/src/services/graphql/importsService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_list_import_jobs_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `jobs` — *no `tables/jobs.sql` snapshot in docs; see service lineage below*
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)

### Write
- *None listed in JSON metadata*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Connectra (search / VQL)](../database/connectra_data_lineage.md)
- [TKD Jobs](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`contact360.io/sync`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`contact360.io/jobs`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_import_jobs_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
