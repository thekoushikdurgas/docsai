---
title: "graphql/UpdateDashboardPage"
source_json: mutation_update_dashboard_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateDashboardPage

## Overview

Update a custom dashboard page by pageId. Returns updated page data with sections and access control.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_dashboard_page_graphql |
| _id | mutation_update_dashboard_page_graphql-001 |
| endpoint_path | graphql/UpdateDashboardPage |
| method | MUTATION |
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

- updateDashboardPage
- page

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/dashboard-pages | Admin Dashboard Pages Page | dashboardPagesService | useAdminDashboardPages | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |
| /admin/dashboard-pages/[pageId] | Admin Dashboard Pages Pageid Page | dashboardPagesService | useDashboardPageEditor | primary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 2
- **Source:** `mutation_update_dashboard_page_graphql.json`

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

*Generated from `mutation_update_dashboard_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
