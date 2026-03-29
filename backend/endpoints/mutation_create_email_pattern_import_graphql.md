---
title: "graphql/CreateEmailPatternImport"
source_json: mutation_create_email_pattern_import_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateEmailPatternImport

## Overview

Create email pattern import scheduler job via GraphQL jobs module. Maps to TKD Job endpoint `POST /api/v1/jobs/email-pattern-import` and processor `email_pattern_import_stream`. Typically restricted to elevated roles.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_email_pattern_import_graphql |
| _id | mutation_create_email_pattern_import_graphql-001 |
| endpoint_path | graphql/CreateEmailPatternImport |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era | 2.x-10.x |
| introduced_in | 2.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | superadmin |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/jobs/mutations.py |
| router_file | contact360.io/app/src/services/graphql/jobsService.ts |


## GraphQL operation

```graphql
mutation CreateEmailPatternImport($input: CreateEmailPatternImportInput!) { jobs { createEmailPatternImport(input: $input) { jobId status createdAt } } }
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

- contact360.io/jobs
- lambda/s3storage
- lambda/emailapis

## Service / repository methods

### service_methods

- createEmailPatternImport

### repository_methods

- create_scheduler_job

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /email | Email Page | jobsService | useNewExport | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_create_email_pattern_import_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x-10.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)
- `job_node` — *no `tables/job_node.sql` snapshot in docs; see service lineage below*

### Write
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)
- `job_node` — *no `tables/job_node.sql` snapshot in docs; see service lineage below*
- `job_events` — *no `tables/job_events.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Email APIs](../database/emailapis_data_lineage.md)
- [S3 Storage](../database/s3storage_data_lineage.md)
- [TKD Jobs](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`contact360.io/jobs`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/s3storage`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/emailapis`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_email_pattern_import_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
