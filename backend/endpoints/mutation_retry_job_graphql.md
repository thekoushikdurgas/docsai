---
title: "graphql/RetryJob"
source_json: mutation_retry_job_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/RetryJob

## Overview

Retry an existing scheduler job through GraphQL jobs module. Maps to TKD Job endpoint `PUT /api/v1/jobs/{uuid}/retry` with optional retry controls and data/priority overrides.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_retry_job_graphql |
| _id | mutation_retry_job_graphql-001 |
| endpoint_path | graphql/RetryJob |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user, admin, superadmin |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/jobs/mutations.py |
| router_file | contact360.io/app/src/services/graphql/jobsService.ts |


## GraphQL operation

```graphql
mutation RetryJob($input: RetryJobInput!) { jobs { retryJob(input: $input) } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs
- job_node

### db_tables_write

- job_node
- job_events

### lambda_services

- contact360.io/jobs

## Service / repository methods

### service_methods

- retryJob

### repository_methods

- get_scheduler_job_by_id

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | jobsService | useJobs | primary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/jobs/page.tsx
- contact360.io/app/src/components/jobs/JobsRetryModal.tsx
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_retry_job_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Job Retry).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | WRITE | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |
| `job_nodes` | WRITE | [job_nodes.sql](../database/tables/job_nodes.sql) |
| `job_events` | WRITE | [job_events.sql](../database/tables/job_events.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- **Jobs**: Retry execution via `contact360.io/jobs`.

## Related endpoint graph

- **Inbound**: `Jobs Page`, `Retry Modal`.
- **Outbound**: `GetJobStatus`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_retry_job_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
