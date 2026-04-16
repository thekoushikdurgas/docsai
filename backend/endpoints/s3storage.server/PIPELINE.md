# s3storage.server — core pipelines

## Multipart CSV / tabular upload

1. **Initiate:** `POST /api/v1/uploads/initiate-csv` — form fields `key` (optional; default `uploads/{uuid}.csv`), `content_type`. Optional header `X-Idempotency-Key` deduplicates session creation via Redis (`{prefix}:mp:idem:{key}`).
2. **Session:** Redis hash `{prefix}:mp:{upload_id}` stores S3 bucket, object key, S3 `UploadId`, TTL **2h** — see [`internal/redisqueue/multipart.go`](../../../../EC2/s3storage.server/internal/redisqueue/multipart.go).
3. **Parts:** `GET /api/v1/uploads/{id}/parts/{n}` returns a presigned PUT URL (15 minutes).
4. **Complete:** `POST /api/v1/uploads/{id}/complete` with JSON `{ "parts": [{ "part_number", "etag" }] }`. On success, enqueues a **metadata** Asynq task and deletes the multipart session.
5. **Abort:** `DELETE /api/v1/uploads/{id}/abort` — aborts S3 multipart, then deletes Redis session.

## Metadata jobs (per uploaded object)

- **Enqueue:** Triggered after successful multipart complete via `redisqueue.EnqueueMetadata` — task type **`s3storage:metadata`**.
- **State:** Job rows in Redis hash `{prefix}:job:{id}`; index sorted set `{prefix}:jobs`. Worker concurrency: **`S3STORAGE_WORKER_CONCURRENCY`** (default **10**).
- **API:** `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`, scoped `GET /api/v1/bucket/jobs?bucket_id=`.

## Sync-metadata (whole logical bucket)

- **Start:** `POST /api/v1/bucket/sync-metadata?bucket_id=` — enqueues **`s3storage:sync_metadata`**; job records under `{prefix}:syncjob:{id}` / `{prefix}:syncjobs` — see [`internal/redisqueue/syncjob.go`](../../../../EC2/s3storage.server/internal/redisqueue/syncjob.go).
- **Status:** `GET /api/v1/bucket/sync-metadata/{id}`.

## Bucket metadata file

- **Read:** `GET /api/v1/bucket/metadata?bucket_id=` loads `{bucket_id}/metadata.json` from the default bucket; implementation in [`router.go`](../../../../EC2/s3storage.server/internal/api/router.go) (S3 GetObject).

## Analysis

- **Schema:** `GET /api/v1/analysis/schema?key=` — sniffs delimiter and headers from a byte range of the object.
- **Stats:** `GET /api/v1/analysis/stats?key=` — row count in sample window.

Last updated: 2026-04-15.
