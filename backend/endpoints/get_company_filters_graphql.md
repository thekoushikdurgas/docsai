---
title: "graphql/GetCompanyFilters"
source_json: get_company_filters_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetCompanyFilters

## Overview

Get available filter definitions for companies. No input required. Returns array of FilterDefinition with key (filter field name), type (data type: string, number, boolean, date, enum), label (display label), displayName (human-readable name), operators (supported filter operators), options (for enum types, array of valid values), isDerived (whether filter is computed from other fields), isActive (whether filter is enabled). Used by frontend filter builder UI for companies.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_company_filters_graphql |
| _id | get_company_filters_graphql-001 |
| endpoint_path | graphql/GetCompanyFilters |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 3.x |
| introduced_in | 3.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/companies/queries.py |
| router_file | contact360/dashboard/src/services/graphql/companiesService.ts |


## GraphQL operation

```graphql
query GetCompanyFilters { companies { companyFilters { key type label displayName operators options isDerived isActive } } }
```

## Data & infrastructure

### db_tables_read

- filters
- filters_data

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- companyFilters

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /companies | Companies Page | companiesService | useCompaniesPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/companies_page.json
- contact360.io/app/app/(dashboard)/companies/page.tsx
- contact360.io/app/src/hooks/companies/useCompaniesFilters.ts

## Inventory

- **page_count:** 1
- **Source:** `get_company_filters_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — Company Data (Filters).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `filters` | READ | [filters.sql](../database/tables/filters.sql) |
| `filters_data` | READ | [filters_data.sql](../database/tables/filters_data.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Linked to `contact360.io/sync` for schema synchronization.

## Related endpoint graph

- **Inbound**: `Companies Page` (Filter Sidebar).
- **Outbound**: `QueryCompanies`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_company_filters_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
