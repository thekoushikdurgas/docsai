---
title: "graphql/CreateExportJob"
source_json: mutation_create_export_job_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateExportJob

## Overview

Create Contact360 export jobs through GraphQL gateway (`createContact360Export`) mapping to TKD Job processor `contact360_export_stream`. Accepts VQL query contract and output/storage controls; returns scheduler job metadata for exports pages and job timeline polling.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_export_job_graphql |
| _id | mutation_create_export_job_graphql-001 |
| endpoint_path | graphql/CreateExportJob |
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
mutation CreateExportJob($input: CreateExportJobInput!) { jobs { createExportJob(input: $input) { uuid jobType status data createdAt } } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs
- job_node
- contacts
- companies

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

- createExportJob

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | jobsService | useNewExport | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/src/services/graphql/jobsService.ts
- contact360.io/app/src/hooks/useNewExport.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_create_export_job_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Export).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | WRITE | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |
| `job_nodes` | WRITE | [job_nodes.sql](../database/tables/job_nodes.sql) |
| `contacts` | READ | [contacts.sql](../database/tables/contacts.sql) |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **Jobs**: Stream processing via `contact360.io/jobs`.
- **S3Storage**: File persistence via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `Contacts Page`, `Export Dialog`.
- **Outbound**: `GetJobStatus`, `GetExportDownloadUrl`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_export_job_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
