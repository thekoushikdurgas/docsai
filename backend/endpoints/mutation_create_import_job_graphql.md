---
title: "graphql/CreateImportJob"
source_json: mutation_create_import_job_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateImportJob

## Overview

Create Contact360 import jobs through GraphQL gateway (`createContact360Import`) mapping to TKD Job processor `contact360_import_prepare`. Accepts S3 source metadata and retry controls; returns scheduler job metadata used by files/import UX and status polling.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_import_job_graphql |
| _id | mutation_create_import_job_graphql-001 |
| endpoint_path | graphql/CreateImportJob |
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
| service_file | contact360.io/api/app/graphql/modules/imports/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/importsService.ts |


## GraphQL operation

```graphql
mutation CreateImportJob($input: CreateImportJobInput!) { imports { createImportJob(input: $input) { uuid jobType status data createdAt } } }
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
- lambda/s3storage

## Service / repository methods

### service_methods

- createImportJob

### repository_methods

- create_user_import

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /files | Files Page | importsService | useImportJobs | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/files/page.tsx
- contact360.io/app/src/services/graphql/importsService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_create_import_job_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Import).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | WRITE | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |
| `job_nodes` | WRITE | [job_nodes.sql](../database/tables/job_nodes.sql) |
| `contacts` | WRITE | [contacts.sql](../database/tables/contacts.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)
- [Sync Service](../database/sync_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Ingestion orchestration via `contact360.io/sync`.
- **Jobs**: Job state handling via `contact360.io/jobs`.

## Related endpoint graph

- **Inbound**: `Files Page`, `Import Dialog`.
- **Outbound**: `GetImportJob`, `ListImportJobs`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_import_job_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
