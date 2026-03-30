---
title: "graphql/ListS3Files"
source_json: query_list_s3_files_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListS3Files

## Overview

List CSV files in S3 bucket. Accepts optional prefix (String) for directory-like filtering (e.g., 'exports/', 'imports/'). Returns S3FileList with files (array of S3File with key, name, size, lastModified, contentType) and total count. Only CSV files are returned (filtered by .csv extension). Uses S3Service for file listing. Raises ServiceUnavailableError (503) if S3 service is unavailable.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_s3_files_graphql |
| _id | query_list_s3_files_graphql-001 |
| endpoint_path | graphql/ListS3Files |
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


## GraphQL operation

```graphql
query ListS3Files($prefix: String) { s3 { s3Files(prefix: $prefix) { files { key name size lastModified } total } } }
```

## Service / repository methods

### service_methods

- s3Files

## Inventory

- **page_count:** 0
- **Source:** `query_list_s3_files_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Email & Storage Foundation (S3).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `s3_files` | READ | [s3_files.sql](../database/tables/s3_files.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [S3 Storage Service](../database/s3storage_data_lineage.md)

## Downstream services (cross-endpoint)

- **S3Storage**: File listing via `lambda/s3storage`.

## Related endpoint graph

- **Inbound**: `Dashboard`, `Settings`.
- **Outbound**: `GetS3FileData`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_s3_files_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
