---
title: "graphql/CompleteUpload"
source_json: mutation_complete_upload_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CompleteUpload

## Overview

Complete multipart upload by combining all uploaded parts. Accepts CompleteUploadInput with uploadId (required, String). Validates at least one part has been registered. Uses S3Service.complete_multipart_upload to finalize in S3. Parts sorted by partNumber before completion. Returns CompleteUploadResponse with status (String: 'completed'), fileKey (String), s3Url (String, presigned URL), location (String, S3 object URL). Session deleted after success. Raises BadRequestError (400) if no parts registered. Raises NotFoundError (404) if upload session not found.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_complete_upload_graphql |
| _id | mutation_complete_upload_graphql-001 |
| endpoint_path | graphql/CompleteUpload |
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
mutation CompleteUpload($input: CompleteUploadInput!) { upload { completeUpload(input: $input) { status fileKey s3Url location } } }
```

## Service / repository methods

### service_methods

- completeUpload

## Inventory

- **page_count:** 0
- **Source:** `mutation_complete_upload_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Upload Complete).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `upload_sessions` | DELETE | [upload_sessions.sql](../database/tables/upload_sessions.sql) |
| `s3_files` | WRITE | [s3_files.sql](../database/tables/s3_files.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Multipart upload finalization via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `RegisterUploadPart`.
- **Outbound**: `ListS3Files`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_complete_upload_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
