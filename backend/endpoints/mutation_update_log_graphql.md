---
title: "graphql/UpdateLog"
source_json: mutation_update_log_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateLog

## Overview

Update an existing log entry. Accepts UpdateLogInput with logId (required, must be valid log ID, 1-255 characters), message (optional, new message text), and context (optional, updated context object). At least one of message or context must be provided. Returns LogEntry with id, message, context, timestamp. Uses LambdaLogsClient.update_log to update log entry. Only provided fields are updated. Role check via UserProfileRepository (must be SuperAdmin).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_log_graphql |
| _id | mutation_update_log_graphql-001 |
| endpoint_path | graphql/UpdateLog |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
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


## Service / repository methods

### service_methods

- updateLog

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_log_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Reliability & Scaling.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_activities` | READ / WRITE | [user_activities.sql](../database/tables/user_activities.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API Lambda** (`lambda/logs.api`): Log update delegated via `LambdaLogsClient`.

## Related endpoint graph

- **Inbound**: `Activities Page` (Frontend edit action).
- **Outbound**: `QueryLogs` (verify update).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_log_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
