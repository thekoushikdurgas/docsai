# s3storage.server — data ownership (Redis + S3)

This service does **not** use a **PostgreSQL** table for async jobs. CRM Postgres (including `scheduler_jobs` when used) remains in the **gateway** database.

## Redis (prefix = `ASYNQ_PREFIX`, default `s3storage`)

| Pattern | Purpose |
|---------|---------|
| `{prefix}:jobs:seq` | Monotonic ID sequence for metadata jobs |
| `{prefix}:job:{id}` | Hash — metadata job fields (`id`, `bucket`, `bucket_id`, `object_key`, `state`, …) |
| `{prefix}:jobs` | Sorted set — metadata job IDs (score = created time) |
| `{prefix}:mp:{upload_id}` | Hash — multipart session (`bucket`, `object_key`, `s3_upload_id`, …), TTL **2h** |
| `{prefix}:mp:idem:{key}` | Idempotency mapping for initiate-csv |
| `{prefix}:syncjobs:seq` | Sequence for sync-metadata jobs |
| `{prefix}:syncjob:{id}` | Hash — sync job state |
| `{prefix}:syncjobs` | Sorted set — sync job index |

Asynq uses the same Redis for task queues; task types include **`s3storage:metadata`** and **`s3storage:sync_metadata`**.

## S3 (default bucket `S3STORAGE_BUCKET`)

- **Tenant prefix:** Keys typically start with `{bucket_id}/` where `bucket_id` is a logical namespace (not necessarily the S3 bucket name).
- **Metadata sidecar:** `{bucket_id}/metadata.json` — read via `GET /api/v1/bucket/metadata`.
- **Uploads:** Multipart keys from initiate-csv; photo uploads under `{bucket_id}/photo/…`; JSON under `{bucket_id}/json/…`.
- **Avatars:** `avatars/{user}.{ext}` (presigned GET).

## Gateway cross-link

GraphQL and REST in `contact360.io/api` orchestrate calls to s3storage; they do **not** mirror Redis job rows into CRM tables unless a separate product feature writes to `scheduler_jobs`.

Last updated: 2026-04-15.
