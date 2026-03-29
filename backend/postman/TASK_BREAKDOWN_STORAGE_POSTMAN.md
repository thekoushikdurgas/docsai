# Task breakdown: Storage Backend Postman collection

## Purpose

Provide a Postman collection in the Appointment360 repo to test the **s3storage** (storage backend) REST API directly. Appointment360 uses this service via `S3StorageClient` for buckets, files, multipart uploads, analysis, and avatars. The collection allows developers to call the storage API without going through GraphQL.

## Source of truth

- **API spec**: `lambda/s3storage/docs/API.md`
- **Existing collection**: `lambda/s3storage/postman/s3storage Service.postman_collection.json`
- **Appointment360 client**: `lambda/appointment360/app/clients/s3storage_client.py` (all endpoints mirrored)

## Tasks (small)

1. **Create collection file**  
   Add `Storage_Backend_s3storage.postman_collection.json` under `lambda/appointment360/sql/postman/` with:
   - Same folder/request structure as s3storage’s collection (Health, Buckets, Files, Multipart Upload, Analysis).
   - Variable `storage_base_url` (or `base_url`) for the s3storage API base URL so it isn’t confused with GraphQL `baseUrl`.
   - Default variable values aligned with API.md (e.g. `bucket_id`, `file_key`, `prefix`, `upload_id`, `part_number`, `limit`, `offset`, `expires_in`).
   - Unique `_postman_id` and clear `info.name` / `info.description`.

2. **Align with API.md and s3storage collection**  
   - Health: GET `/`, GET `/api/v1/health`, GET `/api/v1/health/info`.
   - Buckets: POST `/api/v1/buckets` (body `bucket_id`).
   - Files: GET list/info/download-url, DELETE object (path/query as in API.md).
   - Multipart: initiate-csv, get presigned part URL, register part, complete (with `bucket_id` query), abort, and POST `/api/v1/uploads/csv` (form-data `file`).
   - Analysis: GET schema, preview, stats, metadata (no `file_key` for metadata).

3. **Update README**  
   In `lambda/appointment360/sql/postman/README.md`:
   - Add “Storage Backend (s3storage)” to the list of files.
   - Document setup: set `storage_base_url` (or `base_url`) to the s3storage API URL (e.g. `LAMBDA_S3STORAGE_API_URL` or SAM `S3StorageApiUrl`).
   - Note that this is the REST API for the storage backend; GraphQL S3/Upload operations go through Appointment360 with `baseUrl` + `/graphql`.

4. **Optional: keep in sync**  
   When s3storage adds or changes endpoints, update this collection (and API.md) and optionally add a note in README that the source of truth is `lambda/s3storage/`.

## Naming and variables

- **Collection name**: “Storage Backend (s3storage)” so it’s clear it’s the storage REST API, not GraphQL.
- **Base URL variable**: Use `storage_base_url` in the collection so Postman envs can have both `baseUrl` (Appointment360 GraphQL) and `storage_base_url` (s3storage REST) without conflict.

## File layout after implementation

- `lambda/appointment360/sql/postman/Storage_Backend_s3storage.postman_collection.json` – new.
- `lambda/appointment360/sql/postman/README.md` – updated with Storage Backend section.
