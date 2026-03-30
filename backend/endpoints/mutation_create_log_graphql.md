---
title: "graphql/CreateLog"
source_json: mutation_create_log_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateLog

## Overview

Create a new log entry. Accepts CreateLogInput with level (required, enum: DEBUG, INFO, WARNING, ERROR, CRITICAL), logger (required, String), message (required, String), context (optional, JSON), performance (optional, JSON with duration, memory, etc.), error (optional, JSON with message, stack, code), userId (optional, UUID), requestId (optional, String), timestamp (optional, DateTime, defaults to now). Returns Log with id, level, logger, message, timestamp. Uses Lambda Logs API for centralized logging to MongoDB. Raises ForbiddenError (403) if not Admin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_log_graphql |
| _id | mutation_create_log_graphql-001 |
| endpoint_path | graphql/CreateLog |
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
mutation CreateLog($input: CreateLogInput!) { admin { createLog(input: $input) { id level logger message timestamp } } }
```

## Service / repository methods

### service_methods

- createLog

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/logs | Admin Logs Page | adminService | useAdminLogs | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_create_log_graphql.json`

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

- **Logs API Lambda** (`lambda/logs.api`): Log creation delegated via `LambdaLogsClient`.

## Related endpoint graph

- **Inbound**: `Activities Page` (Frontend), system-wide activity logging.
- **Outbound**: `QueryLogs` (verify log), `GetLogStatistics` (aggregate updates).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_log_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
