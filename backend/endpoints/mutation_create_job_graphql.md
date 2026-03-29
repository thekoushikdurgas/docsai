---
title: "graphql/CreateJob"
source_json: mutation_create_job_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateJob

## Overview

Create scheduler jobs through the GraphQL jobs module as a gateway-facing contract to TKD Job. Supports job-type specific mutations (email export/verify/pattern import, contact360 import/export) and generic job creation paths where enabled. Response shape maps to scheduler job records plus live status payloads from the TKD Job service.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_job_graphql |
| _id | mutation_create_job_graphql-001 |
| endpoint_path | graphql/CreateJob |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/jobs/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/jobsService.ts |


## GraphQL operation

```graphql
mutation CreateJob($input: CreateJobInput!) { jobs { createJob(input: $input) { uuid jobType status data createdAt } } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs
- job_node

### db_tables_write

- scheduler_jobs
- job_node
- job_events

### lambda_services

- contact360.io/sync
- contact360.io/jobs

## Service / repository methods

### service_methods

- createJob

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | jobsService | useJobs | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/jobs/page.tsx
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_create_job_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Job Creation).

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

- **Jobs**: Execution via `contact360.io/jobs`.
- **Sync**: Direct data ingestion via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Jobs Page`, `Import/Export Flow`.
- **Outbound**: `GetJobStatus`, `ListJobs`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_job_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
