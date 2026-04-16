# s3storage.server — events (polling vs webhooks)

## Outbound events

The s3storage service does **not** emit Kafka topics or outbound webhooks for job completion. Integrations should **poll** HTTP:

- **Metadata jobs:** `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`, or tenant-scoped `GET /api/v1/bucket/jobs?bucket_id=`.
- **Sync-metadata jobs:** `GET /api/v1/bucket/sync-metadata/{id}`.

## Gateway

The CRM gateway uses [`S3StorageEC2Client`](../../../../contact360.io/api/app/clients/s3storage_client.py) for GraphQL-driven flows. Long-running UX that needs job status should follow the same **polling** pattern unless a future design adds webhooks explicitly.

## Inbound

Work is triggered by **synchronous HTTP** (uploads, enqueue endpoints) and **Asynq** workers consuming Redis-backed tasks — not by external event buses.

Last updated: 2026-04-15.
