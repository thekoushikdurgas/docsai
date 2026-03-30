---
title: "graphql/SaveSalesNavigatorProfiles"
source_json: mutation_save_sales_navigator_profiles_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/SaveSalesNavigatorProfiles

## Overview

Save Sales Navigator profiles to database via bulk upsert. Accepts SaveProfilesInput with profiles (required, array of JSON objects, max 1000 per request). Each profile should contain firstName, lastName, company, headline, location, profileUrl. Creates or updates contacts and companies via ConnectraClient.bulk_upsert. Returns SaveProfilesResponse with success (Boolean), totalProfiles (Int), savedCount (Int, contacts created + updated), errors (array of String). Errors collected and returned without raising exceptions. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_save_sales_navigator_profiles_graphql |
| _id | mutation_save_sales_navigator_profiles_graphql-001 |
| endpoint_path | graphql/SaveSalesNavigatorProfiles |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
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
| service_file | appointment360/app/graphql/modules/sales_navigator/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/salesNavigatorService.ts |


## GraphQL operation

```graphql
mutation SaveSalesNavigatorProfiles($input: SaveProfilesInput!) { salesNavigator { saveProfiles(input: $input) { success totalProfiles savedCount errors } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies

### db_tables_write

- contacts
- companies
- contacts_index
- companies_index
- filters_data

### lambda_services

- backend(dev)/salesnavigator
- contact360.io/sync

## Service / repository methods

### service_methods

- saveProfiles

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /linkedin | LinkedIn Page | salesNavigatorService | useLinkedIn | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/src/services/graphql/salesNavigatorService.ts
- contact360.io/app/src/hooks/useLinkedIn.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_save_sales_navigator_profiles_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*

### Write
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*
- `contacts_index` — *no `tables/contacts_index.sql` snapshot in docs; see service lineage below*
- `companies_index` — *no `tables/companies_index.sql` snapshot in docs; see service lineage below*
- `filters_data` — *no `tables/filters_data.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Connectra (search / VQL)](../database/connectra_data_lineage.md)
- [Sales Navigator](../database/salesnavigator_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`backend(dev)/salesnavigator`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`contact360.io/sync`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_save_sales_navigator_profiles_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
