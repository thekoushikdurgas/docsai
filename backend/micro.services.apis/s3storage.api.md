# S3 storage API (`EC2/s3storage.server`)

HTTP API for the **Go/Gin** service at `EC2/s3storage.server` (`contact360.io/s3storage`). The Contact360 gateway uses **`S3StorageEC2Client`** (`contact360.io/api/app/clients/s3storage_ec2_client.py`) against `LAMBDA_S3STORAGE_API_URL` / `LAMBDA_S3STORAGE_API_KEY`.

**Base path:** `/api/v1`  
**Code:** `EC2/s3storage.server/internal/api/router.go` (`Register`).  
**Process entry:** `EC2/s3storage.server/cmd/api/main.go` — loads config, opens Postgres (required), registers routes; **`S3STORAGE_API_KEY` / `API_KEY` must be non-empty** or the server exits.

## Operation inventory

| Method | Path | Auth |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Public |
| `GET` | `/api/v1/health/ready` | Public |
| `GET` | `/api/v1/jobs` | API key |
| `GET` | `/api/v1/jobs/:id` | API key |
| `GET` | `/api/v1/buckets/:name/ping` | API key |
| `GET` | `/api/v1/files` | API key |
| `POST` | `/api/v1/uploads/initiate-csv` | API key |
| `GET` | `/api/v1/uploads/:id/parts/:n` | API key |
| `POST` | `/api/v1/uploads/:id/complete` | API key |
| `DELETE` | `/api/v1/uploads/:id/abort` | API key |
| `GET` | `/api/v1/analysis/schema` | API key |
| `GET` | `/api/v1/analysis/stats` | API key |
| `GET` | `/api/v1/avatars/:user` | API key |

## Configuration (environment)

Loaded in `internal/config/config.go` unless noted.

| Variable | Fallback / default | Role |
| --- | --- | --- |
| `S3STORAGE_PORT` | `PORT`, then `8087` | HTTP listen port |
| `S3STORAGE_API_KEY` | `API_KEY` | **Required** — process exits on empty (`cmd/api/main.go`) |
| `AWS_REGION` | `us-east-1` | S3 client region |
| `S3STORAGE_BUCKET` | `BUCKET`, `S3_BUCKET_NAME`, then `""` | Default bucket for list/upload/analysis/avatars |
| `REDIS_ADDR` | `localhost:6379` | Used by broader app/workers (not every HTTP handler) |
| `ASYNQ_PREFIX` | `s3storage` | Asynq queue prefix |

**AWS credentials:** Standard SDK chain (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` when set — see `internal/s3store/s3store.go` `New`).

**Postgres:** Required at startup for `multipart_sessions` and metadata job visibility (`s3storage_metadata_jobs`). DSN comes from app wiring in `cmd/api` (not in `config.Config` struct).

## Middleware and background behavior

- **`X-Request-ID`:** Every response sets this header; if the client omits it, a new UUID is generated (`router.go`).
- **Multipart session TTL:** In-memory/DB rows older than **2 hours** are not automatically validated per request; a background goroutine runs every **15 minutes** and deletes `multipart_sessions` rows with `created_at` older than 2h.
- **Table:** `multipart_sessions` is created at startup if missing (`ensureMultipartSessionTable`).

## Authentication

| Location | When |
| --- | --- |
| `X-API-Key: <key>` | Preferred for protected routes |
| `?api_key=<key>` | Alternative (middleware accepts either) |

**Public (no key):** `GET /api/v1/health`, `GET /api/v1/health/ready`.

Invalid or missing key on protected routes: **`401`** with `{"error":"unauthorized"}`.

## Error responses (common shapes)

| Situation | HTTP | Body |
| --- | --- | --- |
| Missing/invalid API key | `401` | `{"error":"unauthorized"}` |
| S3/AWS errors (many handlers use `writeS3Err`) | varies | `{"error":"<message>"}` and optionally `{"aws_error_code":"<code>"}` |
| JSON bind failure (e.g. complete upload) | `400` | `{"error":"<bind error>"}` |
| Missing required query (`analysis/*` without `key`) | `400` | `{"error":"key required"}` |
| Unknown multipart session / part | `404` | `{"error":"unknown upload"}`, `unknown upload or part`, etc. |
| Job not found | `404` | `{"error":"job not found"}` |
| Invalid job id | `400` | `{"error":"invalid job id"}` |
| DB or unexpected handler error | `500` | `{"error":"<message>"}` |
| `HeadBucket` failure on ping | `502` | S3 error shape above |

## Request ID

Responses may include header **`X-Request-ID`** (generated if the client did not send one).

---

## Health

### `GET /api/v1/health`

Liveness. **No auth.**

**Response `200`:**

```json
{
  "status": "ok"
}
```

### `GET /api/v1/health/ready`

Readiness (S3 bucket configured and `HeadBucket` succeeds). **No auth.**

**Response `200`:**

```json
{
  "ready": true
}
```

**Response `503` (examples):**

```json
{
  "ready": false,
  "error": "S3STORAGE_BUCKET not set"
}
```

```json
{
  "ready": false,
  "error": "...",
  "aws_error_code": "NoSuchBucket"
}
```

---

## Metadata jobs (Postgres queue)

### `GET /api/v1/jobs`

**Auth:** required.

| Query param | Type | Default | Description |
| --- | --- | --- | --- |
| `state` | string | (empty) | Filter by job state |
| `limit` | int | `50` | Clamped to `1..500` |

**Response `200`:**

```json
{
  "jobs": [
    {
      "id": 1,
      "bucket": "my-bucket",
      "bucket_id": "user-uuid",
      "key": "user-uuid/upload/file.csv",
      "state": "pending",
      "last_error": null,
      "attempts": 0,
      "available_at": "2026-04-05T12:00:00Z",
      "created_at": "2026-04-05T11:59:00Z",
      "updated_at": "2026-04-05T11:59:00Z"
    }
  ],
  "total": 1
}
```

### `GET /api/v1/jobs/:id`

**Auth:** required. `:id` is numeric.

**Response `200`:**

```json
{
  "job": {
    "id": 1,
    "bucket": "my-bucket",
    "bucket_id": "user-uuid",
    "key": "user-uuid/upload/file.csv",
    "state": "pending",
    "last_error": null,
    "attempts": 0,
    "available_at": "2026-04-05T12:00:00Z",
    "created_at": "2026-04-05T11:59:00Z",
    "updated_at": "2026-04-05T11:59:00Z"
  }
}
```

**Response `404`:** `{"error":"job not found"}`  
**Response `400`:** `{"error":"invalid job id"}`

---

## Buckets

### `GET /api/v1/buckets/:name/ping`

**Auth:** required. Calls S3 `HeadBucket` on `:name`.

**Response `200`:** `{"bucket":"<name>","ok":true}`  
**Response `502`:** S3 error; may include `aws_error_code`.

---

## Files

### `GET /api/v1/files`

**Auth:** required.

| Query | Description |
| --- | --- |
| `prefix` | Passed to S3 list (optional) |

Uses configured default bucket from env (`DefaultBucket`).

**Response `200`:**

```json
{
  "objects": []
}
```

Each element is an AWS SDK **`types.Object`** value from `ListObjectsV2` (`MaxKeys` **500** in code). JSON uses the SDK’s field names (pointers become `null` or are omitted). Typical fields:

| Field | Meaning |
| --- | --- |
| `Key` | Object key |
| `LastModified` | RFC3339 timestamp |
| `ETag` | Entity tag (often quoted) |
| `Size` | Size in bytes |
| `StorageClass` | e.g. `STANDARD` |
| `ChecksumCRC32`, `ChecksumCRC32C`, … | Optional checksums when present |

Empty prefix with no objects yields `"objects": []` or `null` from AWS — clients should treat missing/null as empty list.

---

## Multipart uploads (CSV)

### `POST /api/v1/uploads/initiate-csv`

**Auth:** required. **Content-Type:** `application/x-www-form-urlencoded` (or multipart form compatible with `PostForm`).

| Form field | Required | Description |
| --- | --- | --- |
| `key` | No | S3 object key; default `uploads/{uuid}.csv` |

| Header | Description |
| --- | --- |
| `X-Idempotency-Key` | Optional; if duplicate, returns existing `upload_id` with `"dedup": true` |

**Response `201`:**

```json
{
  "upload_id": "session-uuid",
  "bucket": "default-bucket",
  "key": "uploads/abc.csv"
}
```

**Response `200` (dedup):**

```json
{
  "upload_id": "session-uuid",
  "dedup": true
}
```

### `GET /api/v1/uploads/:id/parts/:n`

**Auth:** required. Presigned **PUT** URL for part number `n` (≥ 1). TTL **15 minutes**.

**Response `200`:**

```json
{
  "url": "https://...",
  "expires_in": "15m"
}
```

**Response `404`:** `{"error":"unknown upload or part"}`

### `POST /api/v1/uploads/:id/complete`

**Auth:** required.

**Body (JSON):**

```json
{
  "parts": [
    { "part_number": 1, "etag": "\"abc123\"" }
  ]
}
```

Completes multipart upload, enqueues metadata job (table `s3storage_metadata_jobs`), deletes session row.

**Response `200`:** `{"bucket":"...","key":"..."}`  
**Response `202` (queue error, upload still completed): `{"bucket":"...","key":"...","metadata_queued":false,"queue_error":"..."}` — S3 multipart completed; inserting into `s3storage_metadata_jobs` failed; session row is still deleted on this path.  
**Response `404`:** `{"error":"unknown upload"}`  
**Response `500`:** S3 complete failure uses `writeS3Err`; bind errors `400`.

### `DELETE /api/v1/uploads/:id/abort`

**Auth:** required. Aborts multipart upload and removes session.

**Response `200`:** `{"aborted":true}`  
**Response `404`:** `{"error":"unknown upload"}`

---

## CSV analysis

### `GET /api/v1/analysis/schema`

**Auth:** required.

| Query | Required |
| --- | --- |
| `key` | Yes — full S3 key in default bucket |

**Response `200`:**

```json
{
  "delimiter": ",",
  "sample_bytes": 1024
}
```

### `GET /api/v1/analysis/stats`

**Auth:** required.

| Query | Required |
| --- | --- |
| `key` | Yes — full S3 key |

**Response `200`:**

```json
{
  "rows_in_sample": 100
}
```

---

## Avatars

### `GET /api/v1/avatars/:user`

**Auth:** required.

| Query | Default |
| --- | --- |
| `ext` | `png` (sanitized, max 8 chars) |

Builds key `avatars/{user}.{ext}` and returns a presigned **GET** URL (1 hour).

**Response `200`:** `{"url":"https://..."}`

---

## Key convention (bucket id / file key)

Server-side helpers treat keys as `{bucket_id}/{file_key}` for metadata queueing: first path segment is the logical tenant id, remainder is the relative file key (see `splitKeyPrefix` in `router.go`).

---

## Related docs

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Service map |
| [s3storage_endpoint_era_matrix.md](../endpoints/s3storage_endpoint_era_matrix.md) | Era / endpoints |
| [s3storage_data_lineage.md](../database/s3storage_data_lineage.md) | Data lineage |
| [07_S3_MODULE.md](../graphql.modules/07_S3_MODULE.md) | GraphQL S3 module (gateway → this API) |
| [10_UPLOAD_MODULE.md](../graphql.modules/10_UPLOAD_MODULE.md) | GraphQL Upload module |
| [../postman/EC2_s3storage.server.postman_collection.json](../postman/EC2_s3storage.server.postman_collection.json) | Postman collection |
