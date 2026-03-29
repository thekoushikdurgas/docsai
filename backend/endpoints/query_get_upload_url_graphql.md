---
title: "graphql/GetUploadUrl"
source_json: query_get_upload_url_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUploadUrl

## Overview

Get presigned S3 upload URL for CSV import. Accepts filename (required, non-empty string, max 255 characters). Returns UploadUrlResponse with uploadUrl (presigned S3 URL), s3Key (S3 key for uploaded file), and expiresIn (expiration time, e.g., '24h0m0s'). Uses ConnectraClient.get_upload_url. Presigned URL is used for direct S3 upload (bypasses server). Used in import workflow: get upload URL, upload CSV to S3, then create import job with the s3Key.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_upload_url_graphql |
| _id | query_get_upload_url_graphql-001 |
| endpoint_path | graphql/GetUploadUrl |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 2.x |
| introduced_in | 2.0.0 |


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
query GetUploadUrl($filename: String!) { jobs { getUploadUrl(filename: $filename) { uploadUrl s3Key expiresIn } } }
```

## Data & infrastructure

### db_tables_read

- jobs

### lambda_services

- contact360.io/sync
- lambda/s3storage

## Service / repository methods

### service_methods

- getUploadUrl
- uploadUrl

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /files | Files Page | jobsService | useCsvUpload | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/files/page.tsx
- contact360.io/app/src/hooks/useCsvUpload.ts
- contact360.io/app/src/services/graphql/jobsService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_get_upload_url_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Presigned Upload).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `s3_files` | WRITE | [s3_files.sql](../database/tables/s3_files.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Presigned URL generation via `lambda/s3storage`.
- **Sync**: Integration for import ingestion.

## Related endpoint graph

- **Inbound**: `Files Page`.
- **Outbound**: `CreateImportJob`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_upload_url_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
