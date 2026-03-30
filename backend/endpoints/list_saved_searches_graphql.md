---
title: "graphql/ListSavedSearches"
source_json: list_saved_searches_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListSavedSearches

## Overview

List all saved searches for current user. Accepts optional SavedSearchFilterInput with searchType (enum: contacts, companies), limit (Int, default 100), offset (Int, default 0). Returns SavedSearchConnection with items, total, limit, offset, hasNext, hasPrevious. User isolation enforced at repository level.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | list_saved_searches_graphql |
| _id | list_saved_searches_graphql-001 |
| endpoint_path | graphql/ListSavedSearches |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 9.x |
| introduced_in | 9.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 50 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/saved_searches/queries.py |
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
- **Source:** `list_saved_searches_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Feature Maturity (Saved Search).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `saved_searches` | READ | [saved_searches.sql](../database/tables/saved_searches.sql) |
| `vql_queries` | READ | [vql_queries.sql](../database/tables/vql_queries.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Search Module Lineage](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Contextual search results via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Search Page` (Saved Search Sidebar).
- **Outbound**: `GetSavedSearch`, `QueryContacts`.

<!-- AUTO:db-graph:end -->
---

*Generated from `list_saved_searches_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
