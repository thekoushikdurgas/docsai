# Task breakdown: Storage GraphQL API Postman collection

## Purpose

Create a **focused** Postman collection for the **storage-related GraphQL API** of Appointment360. It covers only Auth (to obtain a token), S3 (file list/info/data/download/schema, CSV multipart initiate/complete, delete), and Upload (status, presigned URL, register part, abort). This allows developers to test storage and file flows via GraphQL without using the full Contact360 GraphQL API collection.

**Audience:** Developers working on storage, Files page, or s3storage integration.

**Relationship to existing collections:**
- **Contact360_GraphQL_API.postman_collection.json** — Full GraphQL API (all roots). Use when testing non-storage modules.
- **Storage_Backend_s3storage.postman_collection.json** — REST API for the s3storage service (direct HTTP). Use when testing or debugging the storage Lambda itself.
- **Storage_GraphQL_API.postman_collection.json** (this deliverable) — GraphQL subset: Auth + S3 + Upload only. Same endpoint as Contact360 GraphQL (`POST {{baseUrl}}/graphql`), but only storage-related operations.

---

## Analysis

### Endpoint and auth

- **URL:** `POST {{baseUrl}}/graphql` (same as full GraphQL API).
- **Body:** JSON `{ "query": "...", "variables": { ... } }`.
- **Auth:** All S3 and Upload operations require `Authorization: Bearer {{accessToken}}`. Run **Auth > Login** first; optionally use a test script to save `accessToken` (and `refreshToken`, `userId`) from the response into collection/environment variables.

### GraphQL roots in scope

| Root    | Purpose |
|---------|--------|
| `auth`  | Login (and optionally me, session) to obtain tokens. |
| `s3`    | File listing, metadata, data, download URL, schema; CSV multipart initiate/complete; delete file. |
| `upload`| Multipart session status, presigned URL per part, register part, abort. |

**CSV multipart flow:** `s3.initiateCsvUpload` → `upload.presignedUrl(uploadId, partNumber)` (per part) → upload part to URL → `upload.registerPart(input)` → `s3.completeCsvUpload(input)` with `upload_id`. See `07_S3_MODULE.md` and `10_UPLOAD_MODULE.md`.

### Variable naming (schema)

- Backend S3/Upload inputs use **snake_case** in the schema for many fields: `file_size`, `upload_id`, `part_number`, `file_key`, etc.
- Some query arguments may appear as camelCase in the schema (e.g. `uploadId`, `partNumber` for `presignedUrl`). Use the same names as in the API docs and dashboard `s3Service` / `useCsvUpload` to avoid 422/validation errors.
- **Collection variables:** `baseUrl`, `accessToken`, `email`, `password`, `prefix`, `fileKey`, `upload_id`, `part_number`, `expires_in` (optional, for download URL TTL).

### Source of truth

- **S3 operations:** `lambda/appointment360/sql/apis/07_S3_MODULE.md`
- **Upload operations:** `lambda/appointment360/sql/apis/10_UPLOAD_MODULE.md`
- **Schema composition:** `lambda/appointment360/app/graphql/schema.py`
- **Dashboard usage (reference):** `contact360/dashboard/src/services/graphql/s3Service.ts`

---

## Tasks (small)

### 1. Create collection file and metadata

- **File:** `lambda/appointment360/sql/postman/Storage_GraphQL_API.postman_collection.json`
- **Content:** Postman v2.1.0 collection with:
  - Unique `_postman_id` (e.g. UUID).
  - `info.name`: "Storage (GraphQL API)" or "Storage GraphQL API".
  - `info.description`: Short setup (baseUrl, email, password, run Auth > Login, set accessToken); note that this is the GraphQL API for storage only; link to README and 07_S3 / 10_UPLOAD.
  - Collection variables: `baseUrl` (e.g. `http://localhost:8000`), `accessToken`, `email`, `password`, `prefix`, `fileKey`, `upload_id`, `part_number`, `expires_in` (optional).

### 2. Auth folder

- **Folder name:** Auth
- **Requests:**
  - **Login** — Mutation `auth.login(input: { email, password })`. Body: `query` + `variables` with `{{email}}`, `{{password}}`. Optional test script to parse response and set `accessToken`, `refreshToken`, `userId` in environment.
  - **Get me** (optional) — Query `auth.me { uuid, email, name, ... }`. Header: `Authorization: Bearer {{accessToken}}`. Useful to verify token.

### 3. S3 folder

- **Folder name:** S3
- **Requests (order suggested for flow):**
  1. **List S3 Files** — Query `s3.s3Files(prefix: $prefix)`. Variables: `prefix` (optional, e.g. `upload/` or `exports/`).
  2. **Get S3 File Info** — Query `s3.s3FileInfo(fileKey: $fileKey)`. Variables: `fileKey`.
  3. **Get S3 File Data** — Query `s3.s3FileData(fileKey, limit, offset)`. Variables: `fileKey`, `limit`, `offset`.
  4. **Get S3 File Download URL** — Query `s3.s3FileDownloadUrl(fileKey, expiresIn?)`. Variables: `fileKey`, optionally `expiresIn`.
  5. **Get S3 File Schema** — Query `s3.s3FileSchema(fileKey)` (if present in schema). Variables: `fileKey`.
  6. **Initiate Csv Upload** — Mutation `s3.initiateCsvUpload(input: { filename, file_size })`. Variables: `filename` (must end with .csv), `file_size` (bytes). Returns `uploadId`, `fileKey`, `chunkSize`, `numParts`.
  7. **Complete Csv Upload** — Mutation `s3.completeCsvUpload(input: { upload_id })`. Variables: `upload_id` (from initiate step).
  8. **Delete File** — Mutation `s3.deleteFile(fileKey: $fileKey)`. Variables: `fileKey`.
- **Descriptions:** One-line description per request; reference 07_S3_MODULE.md where helpful.

### 4. Upload folder

- **Folder name:** Upload
- **Requests:**
  1. **Get Upload Status** — Query `upload.uploadStatus(upload_id: $upload_id)`. Variables: `upload_id`. (Schema uses `upload_id`; see dashboard getUploadStatus.)
  2. **Get Presigned URL** — Query `upload.presignedUrl(uploadId, partNumber)`. Variables: `uploadId` (or `upload_id` if schema uses snake_case), `partNumber`. Returns presigned URL and optionally `etag` for registerPart.
  3. **Register Part** — Mutation `upload.registerPart(input: { upload_id, part_number, etag })` (or camelCase per schema). Variables: from presigned URL step + etag from PUT response.
  4. **Abort Upload** — Mutation `upload.abortUpload(input: { upload_id })`. Variables: `upload_id`.
- **Descriptions:** Reference 10_UPLOAD_MODULE.md; note that CSV flow uses `s3.initiateCsvUpload` and `s3.completeCsvUpload`, with Upload only for presignedUrl and registerPart.

### 5. Align request bodies with schema

- Ensure each request body uses the correct variable names and types (String!, Int!, input objects) as in 07_S3_MODULE and 10_UPLOAD_MODULE. Match dashboard `s3Service` and upload hooks for variable names (e.g. `upload_id` vs `uploadId` per operation).
- Response field names: use snake_case where the schema returns snake_case (e.g. `upload_id`, `file_key` in uploadStatus).

### 6. Update README

- In `lambda/appointment360/sql/postman/README.md`:
  - Add **Storage_GraphQL_API.postman_collection.json** to the Files list.
  - Add a subsection **Storage (GraphQL API) – Storage_GraphQL_API.postman_collection.json** that explains: focused collection for Auth + S3 + Upload; same endpoint `POST {{baseUrl}}/graphql`; setup (baseUrl, email, password, Login → accessToken); variables (prefix, fileKey, upload_id, part_number, etc.); link to 07_S3_MODULE and 10_UPLOAD_MODULE.
  - Optionally add a row in the "Folder → GraphQL root mapping" table or a short note that the Storage GraphQL collection only includes Auth, S3, and Upload.

### 7. Optional: keep in sync

- When new storage-related operations are added (e.g. s3FileStats, bucketMetadata), add corresponding requests to this collection and refresh descriptions from the API docs.

---

## File layout after implementation

- `lambda/appointment360/sql/postman/Storage_GraphQL_API.postman_collection.json` — new.
- `lambda/appointment360/sql/postman/README.md` — updated with Storage GraphQL section.
- `lambda/appointment360/sql/postman/TASK_BREAKDOWN_STORAGE_GRAPHQL_POSTMAN.md` — this file.

---

## Checklist

- 📌 Planned: Collection file created with unique ID and description.
- 📌 Planned: Collection variables: baseUrl, accessToken, email, password, prefix, fileKey, upload_id, part_number, (expires_in).
- 📌 Planned: Auth: Login (with optional test script), Get me.
- 📌 Planned: S3: List, File Info, File Data, Download URL, File Schema (if any), Initiate Csv Upload, Complete Csv Upload, Delete File.
- 📌 Planned: Upload: Upload Status, Presigned URL, Register Part, Abort Upload.
- 📌 Planned: All requests POST to `{{baseUrl}}/graphql` with Content-Type application/json and Authorization Bearer {{accessToken}} (except Login if desired).
- 📌 Planned: README updated with Storage GraphQL collection and setup.
