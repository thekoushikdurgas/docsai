---
title: "graphql/GetVQLHealth"
source_json: query_get_vql_health_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetVQLHealth

## Overview

Get VQL (Vivek Query Language)/Connectra health status including connectraEnabled, connectraStatus, connectraBaseUrl, connectraDetails, connectraError, and monitoringAvailable.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_vql_health_graphql |
| _id | query_get_vql_health_graphql-001 |
| endpoint_path | graphql/GetVQLHealth |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
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
| service_file | contact360.io/api/app/graphql/modules/health/queries.py |
| router_file | contact360/dashboard/src/services/graphql/healthService.ts |


## GraphQL operation

```graphql
query GetVQLHealth { health { vqlHealth { connectraEnabled connectraStatus connectraBaseUrl connectraDetails connectraError monitoringAvailable } } }
```

## Data & infrastructure

### db_tables_read

- contacts_index
- companies_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- getVQLHealth
- vqlHealth

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/system-status | Admin System Status Page | healthService | useSystemStatus | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/admin/page.tsx
- contact360.io/app/src/services/graphql/healthService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_get_vql_health_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Observability (VQL Health).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts_index` | READ | [contacts_index.sql](../database/tables/contacts_index.sql) |
| `companies_index` | READ | [companies_index.sql](../database/tables/companies_index.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Search Module Lineage](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Real-time health check via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Admin System Status Page`.
- **Outbound**: `GetVQLStats`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_vql_health_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
