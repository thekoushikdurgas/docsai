---
title: "graphql/DeleteLogsBulk"
source_json: mutation_delete_logs_bulk_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteLogsBulk

## Overview

Delete multiple log entries by filters. Accepts DeleteLogsBulkInput with optional filters: level (enum: DEBUG, INFO, WARNING, ERROR, CRITICAL), logger (String, max 200 chars), userId (UUID), requestId (String, max 100 chars), startTime (DateTime), endTime (DateTime). Returns DeleteLogsBulkResponse with deletedCount (Int). Uses Lambda Logs API for bulk deletion in MongoDB. Raises ForbiddenError (403) if not SuperAdmin. Use with caution - deletions are permanent.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_logs_bulk_graphql |
| _id | mutation_delete_logs_bulk_graphql-001 |
| endpoint_path | graphql/DeleteLogsBulk |
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
mutation DeleteLogsBulk($input: DeleteLogsBulkInput!) { admin { deleteLogsBulk(input: $input) { deletedCount } } }
```

## Service / repository methods

### service_methods

- deleteLogsBulk

## Inventory

- **page_count:** 0
- **Source:** `mutation_delete_logs_bulk_graphql.json`

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

- **Logs API Lambda** (`lambda/logs.api`): Bulk log deletion delegated via `LambdaLogsClient`.

## Related endpoint graph

- **Inbound**: `Activities Page` (Frontend bulk delete action).
- **Outbound**: `QueryLogs` (refresh list), `GetLogStatistics` (aggregate updates).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_logs_bulk_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
