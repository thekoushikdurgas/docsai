---
title: "graphql/ListExports"
source_json: list_exports_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListExports

## Overview

List exports for current user with filtering. Accepts optional ExportFilterInput with status (enum: PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED), exportType (enum: contact, company), limit (Int, default 100), offset (Int, default 0). Returns ExportConnection with items (array of Export), total, limit, offset, hasNext, hasPrevious. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | list_exports_graphql |
| _id | list_exports_graphql-001 |
| endpoint_path | graphql/ListExports |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 3.x |
| introduced_in | 3.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 50 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/exports/queries.py |
| router_file | contact360/dashboard/src/services/graphql/exportsService.ts |


## GraphQL operation

```graphql
query ListExports($input: ExportFilterInput) { exports { exports(input: $input) { items { id name status progress downloadUrl createdAt } total hasNext } } }
```

## Service / repository methods

### service_methods

- exports

### repository_methods

- get_exports_by_user

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /dashboard | Dashboard Page | exportsService | useDashboardPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /export | Export Page | exportsService | useExportPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 2
- **Source:** `list_exports_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `list_exports_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
