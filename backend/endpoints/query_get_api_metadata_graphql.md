---
title: "graphql/GetAPIMetadata"
source_json: query_get_api_metadata_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetAPIMetadata

## Overview

Get API metadata information. No input required. Returns APIMetadata with version (String), environment (String: development, staging, production), buildDate (DateTime), commitHash (String), modules (array of ModuleInfo with name, version, description). Also includes endpoints count and supported features. Public endpoint - no authentication required.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_api_metadata_graphql |
| _id | query_get_api_metadata_graphql-001 |
| endpoint_path | graphql/GetAPIMetadata |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
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
| service_file | contact360.io/api/app/graphql/modules/health/queries.py |
| router_file | contact360/dashboard/src/services/graphql/healthService.ts |


## GraphQL operation

```graphql
query GetAPIMetadata { health { apiMetadata { version environment buildDate commitHash modules { name version } } } }
```

## Service / repository methods

### service_methods

- apiMetadata

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/system-status | Admin System Status Page | healthService | useSystemStatus | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_api_metadata_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Metadata).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `api_metadata` | READ | [api_metadata.sql](../database/tables/api_metadata.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Module status via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Admin System Status Page`.
- **Outbound**: `GetHealth`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_api_metadata_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
