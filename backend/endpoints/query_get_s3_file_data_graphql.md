---
title: "graphql/GetS3FileData"
source_json: query_get_s3_file_data_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetS3FileData

## Overview

Get paginated CSV file data from S3. Returns S3FileData with rows array (each row as JSON object with column names as keys), limit, offset, and totalRows. Pagination is required for large files (limit: 1-1000, offset: non-negative). CSV files are parsed and returned as structured JSON data. Used by S3FileBrowser component and useS3FileData hook.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_s3_file_data_graphql |
| _id | query_get_s3_file_data_graphql-001 |
| endpoint_path | graphql/GetS3FileData |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 2.x |
| introduced_in | 2.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/s3/queries.py |
| router_file | contact360/dashboard/src/services/graphql/s3Service.ts |


## Service / repository methods

### service_methods

- getS3FileData
- s3FileData

## Inventory

- **page_count:** 0
- **Source:** `query_get_s3_file_data_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (S3 Data).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `s3_files` | READ | [s3_files.sql](../database/tables/s3_files.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: File data retrieval via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `S3FileBrowser`.
- **Outbound**: `ListS3Files`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_s3_file_data_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
