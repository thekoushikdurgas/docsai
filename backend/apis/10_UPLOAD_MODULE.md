# Upload Module

The Upload module provides GraphQL operations for **multipart uploads** via the dedicated `s3storage` service. Appointment360 never talks to S3 directly; instead it delegates to `s3storage`, which stores files in a single physical S3 bucket using per-user logical buckets and key prefixes.
**Location:** `app/graphql/modules/upload/`

## Overview
- Supports large file uploads via multipart sessions
- Typically used for user-provided CSVs and other large assets (e.g. CSVs for jobs/exports)
- Orchestrates uploads using:
  - `UploadSessionManager` (in-memory/Redis-compatible session tracking)
  - `S3StorageClient` → `s3storage` service for initiating, completing, and aborting multipart uploads and generating presigned URLs

### Key semantics

- Each authenticated user has a logical bucket id stored in `users.bucket` (falling back to `users.uuid` when empty).
- When `upload.initiateUpload` is called, the client passes a simple filename (e.g. `contacts_2026.csv`); `s3storage` prepends an `upload/` prefix and a timestamp to create a logical key such as `upload/20260210_120000_contacts_2026.csv`.
- The `fileKey` returned by `initiateUpload` is always **relative to the logical bucket root** and is later passed to Jobs or the S3 module without modification.
- `s3storage` maps the logical key into a physical S3 key by prefixing it with the bucket id, for example: `{bucket_id}/upload/20260210_120000_contacts_2026.csv`.

## Primary entrypoints
- `upload.*` queries for upload session inspection (if enabled)
- `upload.*` mutations to create/complete/abort multipart upload sessions (if enabled)

## Implementation details (s3storage)

- **completeUpload**: The s3storage REST API requires `bucket_id` as a query parameter when completing a multipart upload (for the metadata worker and consistency). The resolver passes the authenticated user's bucket id (`users.bucket` or `users.uuid`) to `S3StorageClient.complete_upload(upload_id, bucket_id)`.
- **Single-shot CSV upload**: The s3storage service also exposes `POST /api/v1/uploads/csv` (multipart form) for smaller files; `S3StorageClient.upload_csv` is available but this flow is not exposed in GraphQL—use the multipart flow for uploads from the app.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `uploadStatus` | `uploadId` | String! | upload status type |
| `presignedUrl` | `uploadId`, `partNumber`, (contentType?) | String!, Int!, String? | presigned URL type |
| **Mutations** | | | |
| `initiateUpload` | `input` | InitiateUploadInput! | init result (includes `uploadId`, `fileKey`) |
| `registerPart` | `input` | RegisterPartInput! | result (part registered) |
| `completeUpload` | `input` | CompleteUploadInput! | result (includes `fileKey`) |
| `abortUpload` | `input` | AbortUploadInput! | result |

Use camelCase in variables (e.g. `uploadId`, `partNumber`, `fileKey`). The `fileKey` from `completeUpload` is passed to Jobs (e.g. `inputCsvKey`, `s3Key`).

## Error handling
- Storage/S3 errors surfaced by `s3storage` (and underlying S3) are mapped via shared external error helpers
- Validation uses shared validation utilities in `app/utils/validation.py`

## References
- **s3storage REST API:** `lambda/s3storage/docs/API.md`
- **Storage Backend Postman:** `sql/postman/Storage_Backend_s3storage.postman_collection.json` (set `storage_base_url` to s3storage API URL)

## Task breakdown (for maintainers)

1. **Trace initiateUpload:** Input (filename, contentLength?, contentType?); resolver gets user bucket from context; call S3StorageClient to create multipart session; return uploadId and fileKey (logical key).
2. **presignedUrl:** uploadId + partNumber (and optionally contentType); s3storage returns presigned URL for PUT; client uploads part and gets ETag for registerPart.
3. **registerPart:** Register each part (uploadId, partNumber, etag) so s3storage can complete multipart; validate part numbers and ETags.
4. **completeUpload:** uploadId + list of parts (partNumber, etag); pass bucket_id to s3storage; return fileKey for use in Jobs/S3.
5. **abortUpload:** uploadId; cleanup session and abort multipart on s3storage; confirm cleanup is non-blocking or logged on failure.

## Related Modules
- **S3 Module**: file listing/metadata/reading; S3 CSV upload mutations delegate to Upload and reuse this flow.
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): uploads here are for CSV/assets via s3storage; Contact AI chat content is not uploaded through this module.

## Documentation metadata

- Era: `3.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

