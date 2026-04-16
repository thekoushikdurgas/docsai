# Connectra (sync.server) vs s3storage.server — boundary

## sync.server (Connectra)

- **Owns:** Contact and company CRUD/VQL, OpenSearch indexing, Connectra-scoped **CSV import/export jobs** (Postgres job rows), and **generic** S3 presign helpers for workflows that need a one-off upload/download URL.
- **Typical patterns:** [`GET /common/upload-url`](../../../../EC2/sync.server/modules/common/controller/uploadController.go), [`GET /common/download-url`](../../../../EC2/sync.server/modules/common/controller/uploadController.go) — returns `s3_key` + presigned URL using Connectra’s S3 configuration.

## s3storage.server

- **Owns:** **Logical tenant namespaces** as S3 key prefixes (`bucket_id/…`), **multipart** CSV/tabular uploads with Redis-backed sessions, **metadata** processing jobs (Redis + Asynq task `s3storage:metadata`), **bucket-wide** `metadata.json` sync (`s3storage:sync_metadata`), CSV **analysis** (schema/stats), presigned GET for CRM file UX, and small **photo/JSON** uploads used by the product gateway.

## How they relate

- **Data plane:** Both may talk to **S3**, but with different responsibilities: Connectra keys are oriented around **import/export and integration** jobs; s3storage keys are oriented around **CRM upload buckets**, multipart state, and derived metadata.
- **CRM database:** **Postgres** for CRM entities and (where applicable) `scheduler_jobs` lives in the **gateway** ecosystem — **not** in s3storage’s Redis job store.
- **When to call which:** Use **sync.server** for Connectra entity operations and Connectra job APIs. Use **s3storage.server** when the gateway GraphQL layer needs listing, multipart upload, analysis, or metadata jobs as implemented in [`s3storage_client.py`](../../../../contact360.io/api/app/clients/s3storage_client.py).

Last updated: 2026-04-15.
