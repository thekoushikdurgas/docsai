---
title: "graphql/SearchLogs"
source_json: query_search_logs_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/SearchLogs

## Overview

Search logs by text content with pagination. Returns paginated log entries matching the search query.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_search_logs_graphql |
| _id | query_search_logs_graphql-001 |
| endpoint_path | graphql/SearchLogs |
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
| service_file | contact360.io/api/app/graphql/modules/admin/queries.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## Service / repository methods

### service_methods

- searchLogs

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/logs | Admin Logs Page | adminService | useAdminLogs | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_search_logs_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Observability).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `logs` | READ | [logs.sql](../database/tables/logs.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Logs API Service](../database/logsapi_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API**: Search execution via `lambda/logsapi`.

## Related endpoint graph

- **Inbound**: `Admin Logs Page`.
- **Outbound**: `GetLogStatistics`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_search_logs_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
