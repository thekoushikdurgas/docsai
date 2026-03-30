---
title: "graphql/UploadAvatar"
source_json: mutation_upload_avatar_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UploadAvatar

## Overview

Upload avatar image for current user. Accepts UploadAvatarInput with fileData (optional, base64-encoded file data OR HTTP/HTTPS URL OR file:// URL) or filePath (optional, local server path). Exactly one of fileData or filePath must be provided. Supported formats: JPEG, PNG, GIF, WebP (detected from file content using magic bytes). Max file size: 5MB. Filename is auto-generated as {user_id}.jpg. S3 key format: avatars/{user_id}/{user_id}.jpg. Returns UserProfile with updated avatarUrl (presigned URL if S3_USE_PRESIGNED_URLS enabled). Database rollback on S3 upload failure. Raises BadRequestError (400) if file type or size is invalid. Raises ServiceUnavailableError (503) if S3 service is unavailable.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_upload_avatar_graphql |
| _id | mutation_upload_avatar_graphql-001 |
| endpoint_path | graphql/UploadAvatar |
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
| service_file | contact360.io/api/app/graphql/modules/users/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/usersService.ts |


## GraphQL operation

```graphql
mutation UploadAvatar($input: UploadAvatarInput!) { users { uploadAvatar(input: $input) { userId avatarUrl jobTitle bio role credits } } }
```

## Service / repository methods

### service_methods

- uploadAvatar

### repository_methods

- update_avatar_url

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | usersService | useUserProfile | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_upload_avatar_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (Avatars).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_profiles` | WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `s3_files` | WRITE | [s3_files.sql](../database/tables/s3_files.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Image upload via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `Profile Page`.
- **Outbound**: `UpdateProfile`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_upload_avatar_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
