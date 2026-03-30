---
title: "graphql/CreateSavedSearch"
source_json: mutation_create_saved_search_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateSavedSearch

## Overview

Create a new saved search. Accepts CreateSavedSearchInput with name (required, String, max 255 chars), description (optional, String), searchType (required, enum: contacts, companies), filters (optional, JSON, VQL filter structure), searchTerm (optional, String), sort (optional, JSON, array of sort objects). Returns SavedSearch with uuid, name, description, searchType, filters, searchTerm, sort, useCount, lastUsedAt, createdAt, updatedAt. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_saved_search_graphql |
| _id | mutation_create_saved_search_graphql-001 |
| endpoint_path | graphql/CreateSavedSearch |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
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
| service_file | contact360.io/api/app/graphql/modules/saved_searches/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/savedSearchesService.ts |


## GraphQL operation

```graphql
mutation CreateSavedSearch($input: CreateSavedSearchInput!) { savedSearches { createSavedSearch(input: $input) { uuid name description searchType filters createdAt } } }
```

## Service / repository methods

### service_methods

- createSavedSearch

### repository_methods

- create_saved_search

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | savedSearchesService | useSavedSearches | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_create_saved_search_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Feature Maturity (Saved Search).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `saved_searches` | WRITE | [saved_searches.sql](../database/tables/saved_searches.sql) |
| `vql_queries` | WRITE | [vql_queries.sql](../database/tables/vql_queries.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Search Module Lineage](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Contextual search results via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Search Page` (Save Search Modal).
- **Outbound**: `ListSavedSearches`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_saved_search_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
