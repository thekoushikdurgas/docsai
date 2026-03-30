---
title: "graphql/AbortUpload"
source_json: mutation_abort_upload_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/AbortUpload

## Overview

Abort an incomplete multipart upload and clean up resources. Accepts AbortUploadInput with uploadId (required, String). Uses S3Service.abort_multipart_upload to cancel in S3. Session deleted after abort. Returns AbortUploadResponse with status (String: 'aborted'), uploadId (String). Idempotent: returns success even if session not found. Prevents orphaned multipart uploads and associated S3 storage costs. Raises ServiceUnavailableError (503) if S3 unavailable.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_abort_upload_graphql |
| _id | mutation_abort_upload_graphql-001 |
| endpoint_path | graphql/AbortUpload |
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
mutation AbortUpload($input: AbortUploadInput!) { upload { abortUpload(input: $input) { status uploadId } } }
```

## Service / repository methods

### service_methods

- abortUpload

## Inventory

- **page_count:** 0
- **Source:** `mutation_abort_upload_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Upload Abort).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `upload_sessions` | DELETE | [upload_sessions.sql](../database/tables/upload_sessions.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Multipart upload abortion via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `Import Page`, `Upload Dialog`.
- **Outbound**: `InitiateUpload`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_abort_upload_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
