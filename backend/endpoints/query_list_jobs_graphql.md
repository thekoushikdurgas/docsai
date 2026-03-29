---
title: "graphql/ListJobs"
source_json: query_list_jobs_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListJobs

## Overview

List scheduler jobs with pagination and optional filters (`status`, `jobType`) through GraphQL jobs module. Backed by scheduler ownership records and TKD Job list/status APIs for dashboard jobs tables and operational panels.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_jobs_graphql |
| _id | query_list_jobs_graphql-001 |
| endpoint_path | graphql/ListJobs |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/jobs/queries.py |
| router_file | contact360/dashboard/src/services/graphql/jobsService.ts |


## GraphQL operation

```graphql
query ListJobs($input: JobFilterInput) { jobs { jobs(input: $input) { items { uuid jobType status data createdAt } total } } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs
- job_node

### lambda_services

- contact360.io/sync
- contact360.io/jobs

## Service / repository methods

### service_methods

- jobs

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | jobsService | useJobs | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/jobs/page.tsx
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_list_jobs_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Job Listing).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | READ | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |
| `job_nodes` | READ | [job_nodes.sql](../database/tables/job_nodes.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- **Jobs**: Bulk listing via `contact360.io/jobs`.

## Related endpoint graph

- **Inbound**: `Jobs Page`.
- **Outbound**: `GetJob`, `RetryJob`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_jobs_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
