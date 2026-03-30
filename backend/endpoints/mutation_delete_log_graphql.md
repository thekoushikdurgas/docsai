---
title: "graphql/DeleteLog"
source_json: mutation_delete_log_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteLog

## Overview

Delete a log entry by ID. Accepts DeleteLogInput with logId (required, String, MongoDB ObjectId). Removes log entry from MongoDB via Lambda Logs API. Returns Boolean indicating success (true if deleted). Raises NotFoundError (404) if log not found. Raises ForbiddenError (403) if not Admin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_log_graphql |
| _id | mutation_delete_log_graphql-001 |
| endpoint_path | graphql/DeleteLog |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 6.x |
| introduced_in | 6.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/admin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## GraphQL operation

```graphql
mutation DeleteLog($input: DeleteLogInput!) { admin { deleteLog(input: $input) } }
```

## Service / repository methods

### service_methods

- deleteLog

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/logs | Admin Logs Page | adminService | useAdminLogs | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_log_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Reliability & Scaling.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_activities` | DELETE | [user_activities.sql](../database/tables/user_activities.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API Lambda** (`lambda/logs.api`): Log deletion delegated via `LambdaLogsClient`.

## Related endpoint graph

- **Inbound**: `Activities Page` (Frontend delete action).
- **Outbound**: `QueryLogs` (refresh list).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_log_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
