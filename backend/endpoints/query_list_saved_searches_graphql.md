---
title: "graphql/ListSavedSearches"
source_json: query_list_saved_searches_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListSavedSearches

## Overview

List all saved searches for current user. Accepts optional SavedSearchFilterInput with searchType (enum: contacts, companies), limit (Int, default 100), offset (Int, default 0). Returns SavedSearchConnection with items (array of SavedSearch with uuid, name, description, searchType, filters, searchTerm, sort, useCount, lastUsedAt, createdAt, updatedAt), total, limit, offset, hasNext, hasPrevious. User isolation enforced at repository level.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_saved_searches_graphql |
| _id | query_list_saved_searches_graphql-001 |
| endpoint_path | graphql/ListSavedSearches |
| method | QUERY |
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
| service_file | appointment360/app/graphql/modules/saved_searches/queries.py |
| router_file | contact360/dashboard/src/services/graphql/savedSearchesService.ts |


## GraphQL operation

```graphql
query ListSavedSearches($input: SavedSearchFilterInput) { savedSearches { savedSearches(input: $input) { items { uuid name searchType useCount lastUsedAt } total hasNext } } }
```

## Service / repository methods

### service_methods

- savedSearches

### repository_methods

- get_saved_searches_by_user

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | savedSearchesService | useContactsPage | secondary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_saved_searches_graphql.json`

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

*Generated from `query_list_saved_searches_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
