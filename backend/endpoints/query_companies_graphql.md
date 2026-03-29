---
title: "graphql/QueryCompanies"
source_json: query_companies_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/QueryCompanies

## Overview

Query companies using VQL (Vivek Query Language). Accepts VQLQueryInput with filters (optional, nested AND/OR filter logic), sort (optional, array of SortInput with field and direction), pagination (optional, PaginationInput with limit 1-1000, offset, search_after for cursor-based), fields (optional, array of field names to return), include_count (optional, Boolean). Returns CompanyConnection with items (array of Company), total count, limit, offset, hasNext, hasPrevious. Uses Connectra service for data retrieval. Supports complex filter expressions with operators: eq, neq, gt, gte, lt, lte, contains, starts_with, ends_with, in, not_in, is_null, is_not_null.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_companies_graphql |
| _id | query_companies_graphql-001 |
| endpoint_path | graphql/QueryCompanies |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 3.x.x |
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
query QueryCompanies($input: VQLQueryInput) { companies { companies(input: $input) { items { id name domain industry } total limit offset hasNext } } }
```

## Data & infrastructure

### db_tables_read

- companies
- contacts
- filters
- filters_data
- companies_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- companies

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /companies | Companies Page | companiesService | useCompaniesPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/companies_page.json
- contact360.io/app/app/(dashboard)/companies/page.tsx
- contact360.io/app/src/hooks/companies/useCompaniesPage.ts

## Inventory

- **page_count:** 1
- **Source:** `query_companies_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `contacts` | READ | [contacts.sql](../database/tables/contacts.sql) |
| `tags` | READ | [tags.sql](../database/tables/tags.sql) |
| `company_tags` | READ | [company_tags.sql](../database/tables/company_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Linked to `contact360.io/sync` for real-time indexing.

## Related endpoint graph

- **Inbound**: `Companies Page`.
- **Outbound**: `GetCompany`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_companies_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
