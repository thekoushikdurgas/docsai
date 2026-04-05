# Upload Module

The Upload module provides GraphQL operations for **multipart uploads** via the dedicated `s3storage` service. The Contact360 gateway never talks to S3 directly; it delegates to `s3storage`, which stores files in a single physical S3 bucket using per-user logical buckets and key prefixes.
**Location:** `app/graphql/modules/upload/`

GraphQL paths: `query { upload { uploadStatus(uploadId: ...) { ... } presignedUrl(uploadId: ..., partNumber: ...) { ... } } }`, `mutation { upload { initiateUpload(...) { ... } } }`.

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

- **completeUpload**: The gateway passes the authenticated user's logical bucket id (`users.bucket` or `users.uuid`) to the storage client so completed keys enqueue metadata jobs on the **EC2** service where applicable.
- **EC2 Go routes** (`EC2/s3storage.server/internal/api/router.go`): **`POST /api/v1/uploads/initiate-csv`** (form `key`, optional `X-Idempotency-Key`), **`GET /api/v1/uploads/:id/parts/:n`**, **`POST /api/v1/uploads/:id/complete`** with `{ "parts": [ { "part_number", "etag" } ] }`, **`DELETE /api/v1/uploads/:id/abort`**. See [s3storage.api.md](../micro.services.apis/s3storage.api.md) and [EC2_s3storage.server.postman_collection.json](../postman/EC2_s3storage.server.postman_collection.json).
- **Client mapping:** `app/clients/s3storage_ec2_client.py` documents Lambda vs Go path differences.
- **Single-shot CSV upload** (`POST` form to `/api/v1/uploads/csv` or similar) is not part of the GraphQL surface; use multipart from the app unless you call the REST API directly.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `uploadStatus` | `uploadId` | String! | upload status type |
| `presignedUrl` | `uploadId`, `partNumber` | `String!`, `Int!` | `PresignedUrlResponse` |
| **Mutations** | | | |
| `initiateUpload` | `input` | InitiateUploadInput! | init result (includes `uploadId`, `fileKey`) |
| `registerPart` | `input` | RegisterPartInput! | result (part registered) |
| `completeUpload` | `input` | CompleteUploadInput! | result (includes `fileKey`) |
| `abortUpload` | `input` | AbortUploadInput! | result |

Use camelCase in variables (e.g. `uploadId`, `partNumber`, `fileKey`). The `fileKey` from `completeUpload` is passed to Jobs (e.g. `inputCsvKey`, `s3Key`).

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type UploadQuery {
  uploadStatus(uploadId: String!): UploadStatusResponse!
  presignedUrl(uploadId: String!, partNumber: Int!): PresignedUrlResponse!
}

type UploadMutation {
  initiateUpload(input: InitiateUploadInput!): InitiateUploadResponse!
  registerPart(input: RegisterPartInput!): RegisterPartResponse!
  completeUpload(input: CompleteUploadInput!): CompleteUploadResponse!
  abortUpload(input: AbortUploadInput!): AbortUploadResponse!
}

input InitiateUploadInput {
  filename: String!
  fileSize: BigInt!
  contentType: String! = "text/csv"
  prefix: String = null
}

input RegisterPartInput {
  uploadId: String!
  partNumber: Int!
  etag: String!
}

input CompleteUploadInput {
  uploadId: String!
}

input AbortUploadInput {
  uploadId: String!
}
```

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `upload.initiateUpload` (mutation)

```json
{
  "query": "mutation ($input: InitiateUploadInput!) { upload { initiateUpload(input: $input) { uploadId fileKey s3UploadId chunkSize numParts } } }",
  "variables": {
    "input": {
      "filename": "contacts.csv",
      "fileSize": 1048576,
      "contentType": "text/csv",
      "prefix": null
    }
  }
}
```

### `upload.presignedUrl` (query)

```json
{
  "query": "query ($uploadId: String!, $partNumber: Int!) { upload { presignedUrl(uploadId: $uploadId, partNumber: $partNumber) { presignedUrl partNumber alreadyUploaded etag } } }",
  "variables": { "uploadId": "<session-id>", "partNumber": 1 }
}
```

## Error handling

- Storage/S3 errors surfaced by `s3storage` (and underlying S3) are mapped via shared external error helpers
- Validation uses shared validation utilities in `app/utils/validation.py`

## References

- **s3storage REST API (EC2):** [s3storage.api.md](../micro.services.apis/s3storage.api.md) — full routes, parameters, and bodies for `EC2/s3storage.server`.
- **Postman:** [EC2_s3storage.server.postman_collection.json](../postman/EC2_s3storage.server.postman_collection.json) — set collection variables `s3storage_base_url`, `s3storage_api_key`, and upload/session variables as needed.

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
