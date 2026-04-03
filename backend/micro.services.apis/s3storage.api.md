# S3 storage (`s3storage` Lambda / storage layer)

Presigned multipart uploads, CSV and export artifacts, and object metadata used by imports/exports and file surfaces in the app.

**Go / EC2 target:** `EC2/s3storage.server/` — module `contact360.io/s3storage` (Gin API + Asynq `storage:metadata` worker). Parity with Python `lambda/s3storage` is tracked in era tasks.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Storage in the delegation map |
| [s3storage_endpoint_era_matrix.md](../endpoints/s3storage_endpoint_era_matrix.md) | Era maturity and endpoints |
| [s3storage_data_lineage.md](../database/s3storage_data_lineage.md) | Buckets, keys, lifecycle |
| [../database/tables/README.md](../database/tables/README.md) | Gateway-side table snapshots where metadata is mirrored |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — endpoint metadata conventions.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — lists [s3storage_endpoint_era_matrix.md](../endpoints/s3storage_endpoint_era_matrix.md); use [index.md](../endpoints/index.md) for GraphQL upload/list ops (`graphql/*Upload*`, `graphql/ListS3Files`, etc.) that delegate to storage.

## Role

- Called from GraphQL upload/export flows and from workers (jobs, email campaign templates, etc.).
- Prefer documenting **new** object workflows here and in lineage; avoid ad hoc bucket usage without updating the matrix.

## GraphQL bridge

Operations such as multipart upload and file listing are exposed under appointment360 **s3** / **upload** modules—see [index.md](../endpoints/index.md) (`graphql/StartMultipartUpload`, `graphql/ListS3Files`, etc.).

## Peer services

- **Jobs** — durable processing after upload ([jobs.api.md](jobs.api.md)).
- **Email campaign** — template bodies and assets may live in S3 ([emailcampaign.api.md](emailcampaign.api.md)).
