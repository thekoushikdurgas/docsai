---
title: "graphql/GetExportDownloadUrl"
source_json: query_get_export_download_url_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetExportDownloadUrl

## Overview

Get download URL for completed export job. Accepts jobUuid (required, must be valid UUID format). Returns String (presigned download URL). Fetches job by UUID, validates that job status is 'completed', extracts S3 key from job_response.s3_key, and uses S3Service.generate_presigned_url to generate download URL. Raises NotFoundError if job doesn't exist, BadRequestError if job is not completed or S3 key is missing.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_export_download_url_graphql |
| _id | query_get_export_download_url_graphql-001 |
| endpoint_path | graphql/GetExportDownloadUrl |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 3.x |
| introduced_in | 3.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/jobs/queries.py |
| router_file | contact360/dashboard/src/services/graphql/jobsService.ts |


## GraphQL operation

```graphql
query GetExportDownloadUrl($jobUuid: ID!) { jobs { exportDownloadUrl(jobUuid: $jobUuid) } }
```

## Data & infrastructure

### db_tables_read

- jobs
- scheduler_jobs

### lambda_services

- contact360.io/jobs
- lambda/s3storage

## Service / repository methods

### service_methods

- getExportDownloadUrl
- exportDownloadUrl

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | jobsService | useJobs | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/jobs/page.tsx
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_get_export_download_url_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `jobs` — *no `tables/jobs.sql` snapshot in docs; see service lineage below*
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)

### Write
- *None listed in JSON metadata*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [S3 Storage](../database/s3storage_data_lineage.md)
- [TKD Jobs](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`contact360.io/jobs`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/s3storage`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_export_download_url_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
