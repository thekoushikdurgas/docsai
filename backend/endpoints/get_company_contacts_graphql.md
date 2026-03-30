---
title: "graphql/GetCompanyContacts"
source_json: get_company_contacts_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetCompanyContacts

## Overview

Get contacts belonging to a specific company. Accepts companyId (ID!, required, valid UUID format) and optional VQLQueryInput with filters, sort, pagination, fields. Returns ContactConnection with items (array of Contact), total count, limit, offset, hasNext, hasPrevious. Automatically filters contacts by company_id. Uses Connectra service for data retrieval. Raises NotFoundError (404) if company doesn't exist.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_company_contacts_graphql |
| _id | get_company_contacts_graphql-001 |
| endpoint_path | graphql/GetCompanyContacts |
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
query GetCompanyContacts($companyId: ID!, $input: VQLQueryInput) { companies { companyContacts(companyId: $companyId, input: $input) { items { id firstName lastName email jobTitle } total hasNext } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies
- contacts_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- companyContacts

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /companies/[id] | Companies Id Page | companiesService | useCompanyContacts | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/companies_page.json
- contact360.io/app/app/(dashboard)/companies/page.tsx
- contact360.io/app/src/services/graphql/companiesService.ts

## Inventory

- **page_count:** 1
- **Source:** `get_company_contacts_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — Company Data (Contact Linking).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | READ | [contacts.sql](../database/tables/contacts.sql) |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `contacts_index` | READ | [contacts_index.sql](../database/tables/contacts_index.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Real-time retrieval via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Company Detail` (Contacts Tab).
- **Outbound**: `GetContact` (drill-down).

<!-- AUTO:db-graph:end -->
---

*Generated from `get_company_contacts_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
