---
title: "graphql/ListScrapingRecords"
source_json: query_list_scraping_records_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListScrapingRecords

## Overview

List Sales Navigator scraping metadata records for the current user with pagination. Accepts optional SalesNavigatorFilterInput with limit and offset. Returns UserScrapingConnection with items array (UserScrapingRecord with id, userId, timestamp, version, source, searchContext, pagination, userInfo, applicationInfo, createdAt, updatedAt) and pageInfo. User isolation enforced - users can only view their own scraping records.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_scraping_records_graphql |
| _id | query_list_scraping_records_graphql-001 |
| endpoint_path | graphql/ListScrapingRecords |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/jobs/queries.py |
| router_file | contact360/dashboard/src/services/graphql/salesNavigatorService.ts |


## GraphQL operation

```graphql
query ListScrapingRecords($input: SalesNavigatorFilterInput) { salesNavigator { listScrapingRecords(input: $input) { items { id timestamp source searchContext pagination } pageInfo { total limit offset } } } }
```

## Data & infrastructure

### db_tables_read

- user_scraping
- contacts
- companies

### lambda_services

- backend(dev)/salesnavigator
- contact360.io/sync

## Service / repository methods

### service_methods

- listSalesNavigatorRecords
- jobs

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /linkedin | LinkedIn Page | salesNavigatorService | useLinkedIn | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/linkedin/page.tsx
- contact360.io/app/src/services/graphql/salesNavigatorService.ts

## Inventory

- **page_count:** 1
- **Source:** `query_list_scraping_records_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `user_scraping` → [user_scraping.sql](../database/tables/user_scraping.sql)
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*

### Write
- *None listed in JSON metadata*

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

*Generated from `query_list_scraping_records_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
