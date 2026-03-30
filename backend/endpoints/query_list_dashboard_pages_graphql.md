---
title: "graphql/ListDashboardPages"
source_json: query_list_dashboard_pages_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListDashboardPages

## Overview

List all custom dashboard pages. Returns page metadata including pageId, title, status, and access control.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_dashboard_pages_graphql |
| _id | query_list_dashboard_pages_graphql-001 |
| endpoint_path | graphql/ListDashboardPages |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 9.x |
| introduced_in | 9.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/pages/queries.py |
| router_file | contact360/dashboard/src/services/graphql/dashboardPagesService.ts |


## Service / repository methods

### service_methods

- listDashboardPages
- dashboardPages

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/dashboard-pages | Admin Dashboard Pages Page | dashboardPagesService | useAdminDashboardPages | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_dashboard_pages_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

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

*Generated from `query_list_dashboard_pages_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
