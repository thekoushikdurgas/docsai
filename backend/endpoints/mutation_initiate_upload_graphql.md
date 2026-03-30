---
title: "graphql/InitiateUpload"
source_json: mutation_initiate_upload_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/InitiateUpload

## Overview

Initialize multipart upload session for large files. Accepts InitiateUploadInput with filename (required, String), fileSize (required, Int, max 10GB), contentType (optional, String). Returns InitiateUploadResponse with uploadId (String), fileKey (format: {prefix}{user_uuid}/{timestamp}_{filename}), s3UploadId (String), chunkSize (Int, default 100MB), numParts (Int). Creates upload session in UploadSessionManager for tracking. S3 multipart upload is initiated. Raises BadRequestError (400) if file size exceeds limit. Raises ServiceUnavailableError (503) if S3 is unavailable.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_initiate_upload_graphql |
| _id | mutation_initiate_upload_graphql-001 |
| endpoint_path | graphql/InitiateUpload |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/upload/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/uploadService.ts |


## GraphQL operation

```graphql
mutation InitiateUpload($input: InitiateUploadInput!) { upload { initiateUpload(input: $input) { uploadId fileKey s3UploadId chunkSize numParts } } }
```

## Service / repository methods

### service_methods

- initiateUpload

## Inventory

- **page_count:** 0
- **Source:** `mutation_initiate_upload_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Upload Init).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `upload_sessions` | WRITE | [upload_sessions.sql](../database/tables/upload_sessions.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Multipart upload initialization via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `Import Page`, `Upload Dialog`.
- **Outbound**: `RegisterUploadPart`, `CompleteUpload`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_initiate_upload_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
