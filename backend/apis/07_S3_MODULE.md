# S3 Module

## Overview

The S3 module provides file operations for listing, reading, and getting metadata about CSV files stored via the `s3storage` microservice, plus **mutations for multipart CSV upload** that return a logical **file_key**. It is used for accessing export files, uploading CSVs for jobs, and downloading via presigned URLs.
**Location:** `app/graphql/modules/s3/`

**Mutations:** `s3.initiateCsvUpload`, `s3.completeCsvUpload` (multipart CSV upload; both return `file_key`), and `s3.deleteFile(fileKey)` (delete a file). Use `upload.presignedUrl` and `upload.registerPart` for each part between initiate and complete.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `s3Files` | `prefix`, `limit`, `offset` | String, Int, Int | `S3FileList` |
| `s3FileData` | `fileKey`, `limit`, `offset` | String!, Int, Int | `S3FileData` |
| `s3FileInfo` | `fileKey` | String! | `S3FileInfo` |
| `s3FileDownloadUrl` | `fileKey` | String! | `S3DownloadUrlResponse` |
| `s3FileSchema` | `fileKey` | String! | schema type |
| `s3FileStats` | `fileKey` | String! | stats type |
| `s3BucketMetadata` | — | — | bucket metadata type |
| **Mutations** | | | |
| `initiateCsvUpload` | `input` | InitiateCsvUploadInput! | init result (includes `fileKey`) |
| `completeCsvUpload` | `input` | CompleteUploadInput! | result (includes `fileKey`) |
| `deleteFile` | `fileKey` | String! | result |

Use camelCase in variables (e.g. `fileKey`). All operations are scoped to the authenticated user's logical bucket via s3storage.

## Types

### S3FileInfo

S3 file information.

```graphql
type S3FileInfo {
  key: String!
  filename: String!
  size: Int
  lastModified: DateTime
  contentType: String
}
```

**Fields:**

- `key` (String!): Object key relative to the user's logical bucket root (e.g. `upload/exp_123456.csv`)
- `filename` (String!): File name
- `size` (Int): File size in bytes
- `lastModified` (DateTime): Last modification timestamp
- `contentType` (String): MIME content type

### S3FileList

List of S3 files along with a display name for the logical bucket.

```graphql
type S3FileList {
  files: [S3FileInfo!]!
  total: Int!
  bucketDisplayName: String
}
```

### S3FileData

Paginated CSV file data.

```graphql
type S3FileData {
  fileKey: String!
  rows: [S3FileDataRow!]!
  limit: Int!
  offset: Int!
  totalRows: Int
}
```

### S3DownloadUrlResponse

Response containing presigned download URL for S3 file.

```graphql
type S3DownloadUrlResponse {
  downloadUrl: String!
  expiresIn: Int!
}
```

**Fields:**

- `downloadUrl` (String!): Presigned URL for downloading the file
- `expiresIn` (Int!): Expiration time in seconds

### S3FileDataRow

A single CSV row.

```graphql
type S3FileDataRow {
  data: JSON!
}
```

**Fields:**

- `data` (JSON!): Row data as key-value pairs (column name → value)

## Queries

### s3Files

List all CSV files in the user's logical bucket.

**Parameters:**

| Name    | Type   | Required | Description |
|---------|--------|----------|-------------|
| `prefix` | String | No       | Optional prefix to filter files (e.g. `upload/`). Max 500 characters. Default: "". |

```graphql
query ListS3Files($prefix: String) {
  s3 {
    s3Files(prefix: $prefix) {
      files {
        key
        filename
        size
        lastModified
        contentType
      }
      total
      bucketDisplayName
    }
  }
}
```

**Variables:**

```json
{
  "prefix": "upload/"
}
```

**Arguments:**

- `prefix` (String): Optional prefix to filter files (default: "")

**Returns:** `S3FileList`

**Authentication:** Required

**Validation:**

- `prefix`: Optional, max 500 characters if provided

**Implementation Details:**

- Uses `S3StorageClient.list_csv_files` to list CSV files from the `s3storage` service.
- The logical bucket id is taken from the authenticated user (`users.bucket` when present, otherwise `users.uuid`); `s3storage` maps this to a single physical S3 bucket and prefixes keys with `{bucket_id}/`.
- Prefix filtering supports directory-like organization inside the logical bucket (e.g., `"upload/"`).
- Only CSV files are returned (filtered by file extension).

**Example Response:**

```json
{
  "data": {
    "s3": {
      "s3Files": {
        "files": [
          {
            "key": "exports/exp_123456.csv",
            "filename": "exp_123456.csv",
            "size": 524288,
            "lastModified": "2024-01-15T10:30:00Z",
            "contentType": "text/csv"
          }
        ],
        "total": 1
      }
    }
  }
}
```

### s3FileData

Get paginated CSV file data from S3.

**Parameters:**

| Name     | Type  | Required | Description |
|----------|-------|----------|-------------|
| `fileKey` | String! | Yes   | S3 object key (logical path within user bucket). |
| `limit`   | Int   | No       | Max rows to return (default 100, max 1000). |
| `offset`  | Int   | No       | Number of rows to skip (default 0). |

```graphql
query GetS3FileData($fileKey: String!, $limit: Int!, $offset: Int) {
  s3 {
    s3FileData(fileKey: $fileKey, limit: $limit, offset: $offset) {
      fileKey
      rows {
        data
      }
      limit
      offset
      totalRows
    }
  }
}
```

**Variables:**

```json
{
  "fileKey": "upload/exp_123456.csv",
  "limit": 100,
  "offset": 0
}

**Arguments:**
- `fileKey` (String!): Object key relative to the logical bucket root (file path inside the user's bucket)
- `limit` (Int!): Maximum number of rows to return (required, 1-1000)
- `offset` (Int): Number of rows to skip (default: 0)

**Returns:** `S3FileData`

**Authentication:** Required

**Validation:**
- `fileKey`: Required, non-empty string, max 500 characters
- `limit`: Required, validated via `validate_pagination` utility (1-1000)
- `offset`: Optional, validated via `validate_pagination` utility (non-negative, default: 0)

**Implementation Details:**
- Uses `S3StorageClient.get_preview` to fetch paginated CSV data via the `s3storage` service.
- `fileKey` is treated as a logical key, and `s3storage` internally reads from the physical S3 key `{bucket_id}/{fileKey}`.
- Pagination is required for large files (limit is mandatory).
- Each row is returned as a JSON object with column names as keys.
- `totalRows` may be `null` if the total count cannot be determined.

**Example Response:**

```json
{
  "data": {
    "s3": {
      "s3FileData": {
        "fileKey": "exports/exp_123456.csv",
        "rows": [
          {
            "data": {
              "uuid": "123e4567-e89b-12d3-a456-426614174000",
              "firstName": "John",
              "lastName": "Doe",
              "email": "john.doe@example.com"
            }
          }
        ],
        "limit": 100,
        "offset": 0,
        "totalRows": 150
      }
    }
  }
}
```

### s3FileInfo

Get metadata/information about a CSV file in S3.

**Parameters:**

| Name     | Type    | Required | Description |
|----------|---------|----------|-------------|
| `fileKey` | String! | Yes      | S3 object key (logical path within user bucket). Max 500 characters. |

### s3FileDownloadUrl

Get presigned download URL for an S3 file. Returns a presigned URL that allows direct download from S3. The URL expires after the specified time (default: 1 hour).

**Parameters:**

| Name       | Type   | Required | Description |
|------------|--------|----------|-------------|
| `fileKey`   | String! | Yes     | S3 object key (logical path within user bucket). |
| `expiresIn` | Int    | No       | URL expiration in seconds (default: from settings, max 604800 = 7 days). |

```graphql
query GetS3FileDownloadUrl($fileKey: String!, $expiresIn: Int) {
  s3 {
    s3FileDownloadUrl(fileKey: $fileKey, expiresIn: $expiresIn) {
      downloadUrl
      expiresIn
    }
  }
}
```

**Variables:**
```json
{
  "fileKey": "exports/exp_123456.csv",
  "expiresIn": 3600
}
```

**Arguments:**

- `fileKey` (String!): S3 object key (file path)
- `expiresIn` (Int, optional): URL expiration time in seconds (default: 1 hour, max: 7 days)

**Returns:** `S3DownloadUrlResponse`

**Authentication:** Required

**Validation:**

- `fileKey`: Required, non-empty string, max 500 characters
- `expiresIn`: Optional, must be a positive integer, max 604800 seconds (7 days)

**Implementation Details:**

- Validates that file exists before generating URL
- Uses `S3StorageClient.get_download_url` to obtain a presigned URL from the `s3storage` service
- URL expiration defaults to the s3storage service setting if not provided (max 7 days)
- Raises NotFoundError if file doesn't exist

**Example Response:**
```json
{
  "data": {
    "s3": {
      "s3FileDownloadUrl": {
        "downloadUrl": "https://s3.amazonaws.com/bucket/exports/exp_123456.csv?X-Amz-Algorithm=...",
        "expiresIn": 3600
      }
    }
  }
}
```

```graphql
query GetS3FileInfo($fileKey: String!) {
  s3 {
    s3FileInfo(fileKey: $fileKey) {
      key
      filename
      size
      lastModified
      contentType
    }
  }
}
```

**Arguments:**

- `fileKey` (String!): S3 object key (file path)

**Returns:** `S3FileInfo`

**Authentication:** Required

**Validation:**

- `fileKey`: Required, non-empty string, max 500 characters

**Implementation Details:**

- Uses `S3StorageClient.get_csv_file_info` to get file metadata from the `s3storage` service
- Returns file information: key, filename, size, lastModified, contentType (logical bucket is derived from the authenticated user)
- Raises NotFoundError if the file does not exist in the user's logical bucket

**Example Response:**

```json
{
  "data": {
    "s3": {
      "s3FileInfo": {
        "key": "exports/exp_123456.csv",
        "filename": "exp_123456.csv",
        "size": 524288,
        "lastModified": "2024-01-15T10:30:00Z",
        "contentType": "text/csv"
      }
    }
  }
}
```

## Mutations

The S3 module provides mutations for **multipart CSV upload** to the S3 bucket. Both mutations return **`file_key`** (the S3 object key) for use in jobs or `s3.s3FileDownloadUrl`. The flow reuses the Upload module's session and presigned URL logic.

**Flow:** `s3.initiateCsvUpload` → get `upload_id` and `file_key` → for each part: `upload.presignedUrl(upload_id, part_number)` → upload part to URL → `upload.registerPart(upload_id, part_number, etag)` → `s3.completeCsvUpload(upload_id)` → get final `file_key`.

### initiateCsvUpload

Initiate multipart upload of a CSV file to S3. Returns `upload_id` and **`file_key`** (S3 object key).

**Parameters:**

| Name    | Type                      | Required | Description |
|---------|---------------------------|----------|-------------|
| `input` | InitiateCsvUploadInput!   | Yes      | `filename` (String!, must end with .csv), `fileSize` (BigInt!, bytes, max 10GB). |

```graphql
mutation InitiateCsvUpload($input: InitiateCsvUploadInput!) {
  s3 {
    initiateCsvUpload(input: $input) {
      uploadId
      fileKey
      chunkSize
      numParts
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "filename": "contacts.csv",
    "file_size": 1048576
  }
}
```

**Arguments:**

- `input` (InitiateCsvUploadInput!): `filename` (must end with `.csv`), `file_size` (bytes, max 10GB)

**Returns:** Same shape as Upload's `InitiateUploadResponse`: `uploadId`, **`fileKey`**, `chunkSize`, `numParts`

**Authentication:** Required

**Validation:**

- `filename`: Required, must end with `.csv` (case-insensitive), max 500 characters
- `file_size`: Positive integer, max 10GB

**Next steps:** Use `upload.presignedUrl(uploadId, partNumber)` for each part, then `upload.registerPart`, then `s3.completeCsvUpload`.

### completeCsvUpload

Complete the multipart CSV upload and return the final **`file_key`** (S3 object key).

**Parameters:**

| Name   | Type                   | Required | Description                                      |
|--------|------------------------|----------|--------------------------------------------------|
| input  | CompleteUploadInput!   | Yes      | Object containing `upload_id` from initiateCsvUpload |

```graphql
mutation CompleteCsvUpload($input: CompleteUploadInput!) {
  s3 {
    completeCsvUpload(input: $input) {
      status
      fileKey
      s3Url
      location
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "upload_id": "uuid-from-initiateCsvUpload"
  }
}
```

**Arguments:**

- `input` (CompleteUploadInput!): `upload_id` from `s3.initiateCsvUpload`

**Returns:** Same shape as Upload's `CompleteUploadResponse`: `status`, **`fileKey`**, `s3Url`, `location`

**Authentication:** Required

**Use of file_key:** Pass the returned `fileKey` to `jobs.createContact360Import` (as `s3Key`), `jobs.createEmailFinderExport` (as `input_csv_key`), or `s3.s3FileDownloadUrl(fileKey)` for download.

### deleteFile

Delete a CSV file from the user's bucket by object key. Uses the same logical bucket as uploads (user's bucket or user UUID).

**Parameters:**

| Name     | Type   | Required | Description                    |
|----------|--------|----------|--------------------------------|
| `fileKey`| String!| Yes      | S3 object key (e.g. from list or upload). |

```graphql
mutation DeleteS3File($fileKey: String!) {
  s3 {
    deleteFile(fileKey: $fileKey)
  }
}
```

**Returns:** `Boolean` — `true` on success.

**Authentication:** Required

**Implementation:** Calls s3storage `DELETE /api/v1/buckets/{bucket_id}/objects?file_key=...`. Bucket is resolved from the authenticated user (`user.bucket` or `user.uuid`).

## Error Handling

The S3 module implements comprehensive error handling with input validation, S3 service error handling, and response validation.

### Error Types

The S3 module may raise the following errors:

- **NotFoundError** (404): File not found in S3
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "S3File"`, `identifier: <file_key>`
  - Occurs when: Requested file key does not exist in S3 bucket
- **ServiceUnavailableError** (503): S3 service not configured or unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "s3"`
  - Occurs when: S3 service is not configured, connection fails, or bucket is inaccessible
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid file key format, limit out of range (must be 1-1000), invalid offset (must be non-negative), or invalid prefix format
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid or required parameters are missing

### Error Response Examples

**Example: File Not Found**

```json
{
  "errors": [
    {
      "message": "File not found: exports/exp_123456.csv",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "S3File",
        "identifier": "exports/exp_123456.csv"
      }
    }
  ]
}
```

**Example: Validation Error**

```json
{
  "errors": [
    {
      "message": "Invalid limit value",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "limit": ["Limit must be between 1 and 1000"],
          "offset": ["Offset must be a non-negative integer"]
        }
      }
    }
  ]
}
```

**Example: Service Unavailable**

```json
{
  "errors": [
    {
      "message": "S3 service temporarily unavailable. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "s3"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: File keys, limits, offsets, and prefixes are validated before processing
- **S3 Service Errors**: S3 API errors are caught and converted to appropriate GraphQL errors
- **CSV Parsing Errors**: CSV parsing errors are handled gracefully with clear error messages
- **Response Validation**: File metadata and CSV data are validated before returning
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete S3 File Operations

```graphql
# 1. List all CSV files
query ListFiles {
  s3 {
    s3Files(prefix: "exports/") {
      files {
        key
        filename
        size
        lastModified
      }
      total
    }
  }
}

# 2. Get file metadata
query GetFileInfo {
  s3 {
    s3FileInfo(fileKey: "exports/exp_123456.csv") {
      key
      filename
      size
      lastModified
      contentType
    }
  }
}

# 3. Read first 100 rows
query ReadFileData {
  s3 {
    s3FileData(
      fileKey: "exports/exp_123456.csv"
      limit: 100
      offset: 0
    ) {
      fileKey
      rows {
        data
      }
      limit
      offset
      totalRows
    }
  }
}

# 4. Read next page
query ReadNextPage {
  s3 {
    s3FileData(
      fileKey: "exports/exp_123456.csv"
      limit: 100
      offset: 100
    ) {
      rows {
        data
      }
      totalRows
    }
  }
}
```

## Implementation Details

### s3storage Integration

- **S3StorageClient**: All file operations are handled by the `S3StorageClient`, which talks to the `s3storage` Lambda over HTTP.
  - **File operations:** `list_csv_files`, `get_csv_file_info`, `get_download_url`, `delete_file` (bucket + file key).
  - **Analysis:** `get_schema`, `get_preview`, `get_stats`, `get_bucket_metadata` (bucket-level metadata).
  - **Multipart upload:** `initiate_csv_upload`, `get_presigned_part_url`, `register_part`, `complete_upload(upload_id, bucket_id)` (s3storage API requires `bucket_id` on complete), `abort_upload`.
  - **Single-shot upload:** `upload_csv(bucket_id, data, filename)` for smaller CSV files (not exposed in GraphQL; use multipart flow for large files).
  - **Avatars:** `upload_avatar`, `get_avatar_download_url` (used by Users module). Avatar key pattern: `avatar/{user_id}.jpg`.
  - **Health:** `health()`, `health_info()`, `root()` for monitoring.
- **Logical Buckets**: The logical bucket id for a user is stored in `users.bucket` (defaulting to their UUID). GraphQL resolvers pass this as `bucket_id` on all s3storage calls; `complete_upload` receives it so the storage API can run the metadata worker.
- **Physical Bucket Configuration**: The underlying S3 bucket and prefix layout are configured in the `s3storage` service (see its `template.yaml` and API.md), not in Appointment360.
- **REST API reference:** `lambda/s3storage/docs/API.md`. A Postman collection for the storage backend is in `sql/postman/Storage_Backend_s3storage.postman_collection.json`.

### CSV File Operations

- **CSV Parsing**: CSV files are parsed and returned as structured JSON data
  - Each row is converted to a JSON object with column names as keys
  - Rows are returned as `S3FileDataRow` with `data` field containing the JSON object
- **Pagination**: File data supports pagination for large files
  - `limit` is required for `s3FileData` query (1-1000)
  - `offset` is optional (default: 0, must be non-negative)
  - Pagination is validated via `validate_pagination` utility
  - `totalRows` may be `null` if the total count cannot be determined
- **Prefix Filtering**: File listing supports prefix filtering for directory-like organization
  - Prefix is optional, max 500 characters
  - Useful for filtering files by directory (e.g., "exports/", "imports/")
  - Only CSV files are returned (filtered by file extension)

### Validation

- **Input Validation**: All inputs are validated before processing
  - `prefix`: Optional, max 500 characters
  - `fileKey`: Required, non-empty string, max 500 characters
  - `limit`: Required, validated via `validate_pagination` utility (1-1000)
  - `offset`: Optional, validated via `validate_pagination` utility (non-negative, default: 0)
- **String Length Validation**: Uses `validate_string_length` utility for prefix and fileKey
- **Pagination Validation**: Uses `validate_pagination` utility for limit and offset

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - String length validation (prefix, fileKey)
  - Pagination validation (limit, offset)
- **S3 Service Error Handling**: S3 API errors are handled centrally via `handle_s3_error`
  - Connection errors are converted to ServiceUnavailableError
  - FileNotFoundError is converted to NotFoundError
  - Other S3 errors are logged and converted to appropriate GraphQL errors
- **Response Validation**: File metadata and CSV data are validated before returning
  - File list structure validation
  - CSV row data validation
  - File info structure validation
- **Error Logging**: Comprehensive error logging with context for debugging
  - User UUID, file key, operation type, and error details are logged

## Task breakdown (for maintainers)

1. **Trace s3Files:** S3Query.s3Files → S3StorageClient with user bucket; prefix/limit/offset passed to s3storage API; validate_pagination and prefix length.
2. **s3FileData/s3FileSchema/s3FileStats:** Each takes fileKey; confirm s3storage endpoints and that fileKey is relative to user's logical bucket (no leading bucket id in key).
3. **initiateCsvUpload/completeCsvUpload:** Map to s3storage multipart CSV flow; ensure returned fileKey is what Jobs module expects (inputCsvKey/s3Key); CompleteUploadInput includes part ETags and uploadId.
4. **deleteFile:** Single fileKey; verify user isolation (s3storage uses bucket from context).
5. **Error mapping:** handle_s3_error and NotFoundError for missing file; ServiceUnavailableError for s3storage down.

## Related Modules

- **Upload Module**: Multipart upload flow; S3 CSV mutations (`initiateCsvUpload`, `completeCsvUpload`) delegate to Upload. Use `upload.presignedUrl` and `upload.registerPart` for each part between initiate and complete. Upload also handles generic multipart upload (any content type).
- **Jobs Module**: Use the `file_key` returned from S3 CSV upload in `jobs.createContact360Import` (s3Key), `jobs.createEmailFinderExport` (input_csv_key), etc.
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): AI chat message bodies are stored in PostgreSQL (`ai_chats.messages`), not as objects in the user’s logical bucket; do not confuse with **Resume AI** JSON in s3storage (`resume/`).

## Documentation metadata

- Era: `3.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

