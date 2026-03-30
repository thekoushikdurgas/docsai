---
title: "graphql/DeleteCompany"
source_json: mutation_delete_company_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteCompany

## Overview

Delete a company by UUID. Accepts DeleteCompanyInput with companyId (required, UUID). Uses ConnectraClient to delete company from Connectra service. Returns Boolean indicating success (true if deleted). Note: This is a soft delete in Connectra. Raises NotFoundError (404) if company not found. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_company_graphql |
| _id | mutation_delete_company_graphql-001 |
| endpoint_path | graphql/DeleteCompany |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/companies/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/companiesService.ts |


## GraphQL operation

```graphql
mutation DeleteCompany($input: DeleteCompanyInput!) { companies { deleteCompany(input: $input) } }
```

## Data & infrastructure

### db_tables_read

- companies
- companies_index

### db_tables_write

- companies
- companies_index
- filters_data

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- deleteCompany

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /companies | Companies Page | companiesService | useCompaniesModals | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/companies_page.json
- contact360.io/app/app/(dashboard)/companies/page.tsx
- contact360.io/app/src/services/graphql/companiesService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_company_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `companies` | WRITE | [companies.sql](../database/tables/companies.sql) |
| `company_tags` | WRITE | [company_tags.sql](../database/tables/company_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Triggers record removal in Connectra search index via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Company Detail` (Delete Action).
- **Outbound**: `QueryCompanies`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_company_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
