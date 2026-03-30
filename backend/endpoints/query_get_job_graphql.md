---
title: "graphql/GetJob"
source_json: query_get_job_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetJob

## Overview

Get a scheduler job by ID from GraphQL jobs module and enrich with live TKD Job payloads (`statusPayload`, `timelinePayload`, `dagPayload`) when requested. Used by job detail views and status polling surfaces.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_job_graphql |
| _id | query_get_job_graphql-001 |
| endpoint_path | graphql/GetJob |
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
query GetJob($uuid: ID!) { jobs { job(uuid: $uuid) { uuid jobType status data jobResponse createdAt updatedAt } } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs
- job_node
- job_events
- edges

### lambda_services

- contact360.io/sync
- contact360.io/jobs

## Service / repository methods

### service_methods

- getJob
- job

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | jobsService | useExpandedJobDetails | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/jobs/page.tsx
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_get_job_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Job Retrieval).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | READ | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |
| `job_nodes` | READ | [job_nodes.sql](../database/tables/job_nodes.sql) |
| `job_events` | READ | [job_events.sql](../database/tables/job_events.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- **Jobs**: Status fetching via `contact360.io/jobs`.

## Related endpoint graph

- **Inbound**: `Jobs Page`, `Polling Hook`.
- **Outbound**: `ListJobs`, `RetryJob`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_job_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
