---
title: "graphql/GetCompany"
source_json: get_company_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetCompany

## Overview

Get a single company by UUID. Accepts uuid (ID!, required, valid UUID format). Returns Company object with full details including id, name, domain, industry, employeeCount, description, website, linkedinUrl, twitterUrl, facebookUrl, foundedYear, headquarters (city, state, country), funding information (totalFunding, lastFundingRound, lastFundingDate), technologies array, and metadata. Uses Connectra service for data retrieval. Raises NotFoundError (404) if company doesn't exist.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_company_graphql |
| _id | get_company_graphql-001 |
| endpoint_path | graphql/GetCompany |
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
query GetCompany($uuid: ID!) { companies { company(uuid: $uuid) { id name domain industry employeeCount description website linkedinUrl headquarters { city country } } } }
```

## Data & infrastructure

### db_tables_read

- companies
- companies_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- company

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /companies/[id] | Companies Id Page | companiesService | useCompanyDetail | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /companies | Companies Page | companiesService | useCompanySummary | secondary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/companies_page.json
- contact360.io/app/app/(dashboard)/companies/page.tsx
- contact360.io/app/src/services/graphql/companiesService.ts

## Inventory

- **page_count:** 2
- **Source:** `get_company_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `tags` | READ | [tags.sql](../database/tables/tags.sql) |
| `company_tags` | READ | [company_tags.sql](../database/tables/company_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Real-time retrieval from `contact360.io/sync` endpoint.

## Related endpoint graph

- **Inbound**: `Companies Page` (Search Result).
- **Outbound**: `UpdateCompany`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_company_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
