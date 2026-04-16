# s3storage.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/s3storage_client.py`](../../../../contact360.io/api/app/clients/s3storage_client.py) (`S3StorageEC2Client`, `get_s3storage_client`)
- **Server:** [`EC2/s3storage.server/internal/api/router.go`](../../../../EC2/s3storage.server/internal/api/router.go) — all functional routes under **`/api/v1`**

**Job storage:** Metadata and sync-metadata jobs live in **Redis** (hashes + sorted sets) and are processed by **Asynq** workers (`cmd/worker`). There is **no PostgreSQL queue** in this service; CRM Postgres remains in the gateway only.

Auth for protected routes: header **`X-API-Key`** or query **`api_key`** must equal the configured key (`S3STORAGE_API_KEY` or `API_KEY` on the Go side). The Python client sends **`X-API-Key`** via [`BaseHTTPClient`](../../../../contact360.io/api/app/clients/base.py).

| `S3StorageEC2Client` method | HTTP | Notes |
|-----------------------------|------|--------|
| `health` | `GET /api/v1/health` | Liveness |
| `health_info` | `GET /api/v1/health/ready` | Readiness (Redis PING + S3 HeadBucket) |
| `create_bucket` | — | **No-op** (logical namespace = S3 key prefix) |
| `list_csv_files` | `GET /api/v1/files?prefix=` | Response uses `objects` |
| `get_csv_file_info` | — | **Stub** (not implemented on Go) |
| `get_download_url` / `get_download_url_for_object_key` | `GET /api/v1/objects/presign-download` | Full S3 key in `key` |
| `delete_file` | `DELETE /api/v1/objects?key=` | |
| `get_schema` | `GET /api/v1/analysis/schema?key=` | |
| `get_stats` | `GET /api/v1/analysis/stats?key=` | |
| `get_preview` | — | **Not implemented** (returns empty) |
| `get_bucket_metadata` | `GET /api/v1/bucket/metadata?bucket_id=` | Reads `{bucket_id}/metadata.json` |
| `init_bucket_metadata` | — | **No-op** |
| `initiate_csv_upload` | `POST /api/v1/uploads/initiate-csv` | Form `key`, `content_type`; optional `X-Idempotency-Key` |
| `upload_photo` | `POST /api/v1/uploads/photo?bucket_id=` | Multipart `file` |
| `get_presigned_part_url` | `GET /api/v1/uploads/{id}/parts/{n}` | |
| `register_part` | — | **No-op** (ETags sent at complete) |
| `complete_upload` | `POST /api/v1/uploads/{id}/complete` | JSON `{ "parts": [{ "part_number", "etag" }] }` |
| `abort_upload` | `DELETE /api/v1/uploads/{id}/abort` | |
| `upload_csv` | — | **Raises** (use multipart flow) |
| `get_avatar_presign_url` / `get_avatar_download_url` | `GET /api/v1/avatars/{user}?ext=` | Presigned GET only |
| `upload_avatar` | — | **Raises** (not supported) |
| `list_jobs` | `GET /api/v1/jobs` or `GET /api/v1/bucket/jobs?bucket_id=` | |
| `get_job` | `GET /api/v1/jobs/{id}` | |

**Routes present on the server but not wrapped by the Python client** (direct HTTP / Postman / future client):

| HTTP | Purpose |
|------|---------|
| `POST /api/v1/bucket/sync-metadata?bucket_id=` | Enqueue **sync-metadata** job (Asynq `s3storage:sync_metadata`) |
| `GET /api/v1/bucket/sync-metadata/{id}` | Sync job status |
| `GET /api/v1/buckets/{name}/ping` | S3 HeadBucket for arbitrary bucket name |
| `POST /api/v1/uploads/json?bucket_id=` | Multipart JSON document upload |
| `GET /api/v1/objects/get?key=` | Raw object body (JSON) |

**Public (no API key):** `GET /api/v1/health`, `GET /api/v1/health/ready`.

Last reviewed: 2026-04-15.
