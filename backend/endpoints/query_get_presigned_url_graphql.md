---
title: "graphql/GetPresignedUrl"
source_json: query_get_presigned_url_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetPresignedUrl

## Overview

Get presigned URL for uploading a specific part in multipart upload. Returns PresignedUrlResponse with presignedUrl (null if part already uploaded), partNumber, alreadyUploaded flag, and etag (if part already uploaded). If part already uploaded, returns existing ETag instead of new URL. Used for direct S3 uploads bypassing server.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_presigned_url_graphql |
| _id | query_get_presigned_url_graphql-001 |
| endpoint_path | graphql/GetPresignedUrl |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/upload/queries.py |
| router_file | contact360/dashboard/src/services/graphql/uploadService.ts |


## Service / repository methods

### service_methods

- getPresignedUrl
- presignedUrl

## Inventory

- **page_count:** 0
- **Source:** `query_get_presigned_url_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_presigned_url_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
