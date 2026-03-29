---
title: "graphql/CancelExport"
source_json: mutation_cancel_export_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CancelExport

## Overview

Cancel a pending or processing export. Accepts CancelExportInput with exportId (required, ID/UUID). Sets export status to 'cancelled'. Returns Boolean indicating success (true if cancelled, false if already completed/failed/cancelled). Raises NotFoundError (404) if export not found. Raises ForbiddenError (403) if user doesn't own the export. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_cancel_export_graphql |
| _id | mutation_cancel_export_graphql-001 |
| endpoint_path | graphql/CancelExport |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/jobs/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/exportsService.ts |


## GraphQL operation

```graphql
mutation CancelExport($input: CancelExportInput!) { exports { cancelExport(input: $input) } }
```

## Service / repository methods

### service_methods

- cancelExport

### repository_methods

- update_export_status

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /export | Export Page | exportsService | useExportManager | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_cancel_export_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Bulk Operations & Automation (Cancellation).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `scheduler_jobs` | WRITE | [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [TKD Jobs Service](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- **Jobs**: Task cancellation via `contact360.io/jobs`.

## Related endpoint graph

- **Inbound**: `Export Page`.
- **Outbound**: `CreateExportJob`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_cancel_export_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
