---
title: "graphql/CreateLogsBatch"
source_json: mutation_create_logs_batch_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateLogsBatch

## Overview

Create multiple log entries in a single batch. Accepts CreateLogsBatchInput with logs (required, array of CreateLogInput, min 1, max 100). Each log follows CreateLogInput validation. Returns array of Log with generated IDs. Uses Lambda Logs API for efficiency - all logs created in single call to MongoDB. Raises ValidationError (422) if logs array is empty or exceeds max. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_logs_batch_graphql |
| _id | mutation_create_logs_batch_graphql-001 |
| endpoint_path | graphql/CreateLogsBatch |
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
mutation CreateLogsBatch($input: CreateLogsBatchInput!) { admin { createLogsBatch(input: $input) { id level logger message timestamp } } }
```

## Service / repository methods

### service_methods

- createLogsBatch

## Inventory

- **page_count:** 0
- **Source:** `mutation_create_logs_batch_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Reliability & Scaling.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_activities` | WRITE | [user_activities.sql](../database/tables/user_activities.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API Lambda** (`lambda/logs.api`): Batch log creation delegated via `LambdaLogsClient`. Processes up to 1000 log entries per batch.

## Related endpoint graph

- **Inbound**: Extension, Sales Navigator bulk operations, import/export completion callbacks.
- **Outbound**: `QueryLogs` (verify), `GetLogStatistics` (aggregate updates).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_logs_batch_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
