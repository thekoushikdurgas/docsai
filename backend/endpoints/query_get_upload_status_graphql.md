---
title: "graphql/GetUploadStatus"
source_json: query_get_upload_status_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUploadStatus

## Overview

Get upload session status for resuming interrupted uploads. Returns UploadStatusResponse with uploadId, fileKey, fileSize, chunkSize, uploadedParts array, totalParts, uploadedBytes, and status (in_progress, completed, aborted). Uses UploadSessionManager to retrieve session data. User isolation enforced - users can only access their own upload sessions.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_upload_status_graphql |
| _id | query_get_upload_status_graphql-001 |
| endpoint_path | graphql/GetUploadStatus |
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
| service_file | contact360.io/api/app/graphql/modules/upload/queries.py |
| router_file | contact360/dashboard/src/services/graphql/uploadService.ts |


## GraphQL operation

```graphql
query GetUploadStatus($uploadId: String!) { upload { uploadStatus(uploadId: $uploadId) { uploadId fileKey fileSize chunkSize uploadedParts totalParts uploadedBytes status } } }
```

## Data & infrastructure

### db_tables_read

- jobs

### lambda_services

- lambda/s3storage

## Service / repository methods

### service_methods

- getUploadStatus
- uploadStatus

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /files | Files Page | uploadService | useCsvUpload | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/files/page.tsx
- contact360.io/app/src/services/graphql/uploadService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_get_upload_status_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Upload Status).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `upload_sessions` | READ | [upload_sessions.sql](../database/tables/upload_sessions.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Status retrieval via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `RegisterUploadPart`.
- **Outbound**: `CompleteUpload`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_upload_status_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
