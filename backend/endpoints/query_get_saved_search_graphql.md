---
title: "graphql/GetSavedSearch"
source_json: query_get_saved_search_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetSavedSearch

## Overview

Get a specific saved search by ID. Returns SavedSearch with id, name, description, type (contact, company, all), searchTerm, filters (JSON), sortField, sortDirection, pageSize, createdAt, updatedAt, lastUsedAt, and useCount. Uses SavedSearchRepository.get_by_id to retrieve saved search. User isolation enforced - users can only access their own saved searches. Raises NotFoundError if saved search doesn't exist or ForbiddenError if it doesn't belong to user.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_saved_search_graphql |
| _id | query_get_saved_search_graphql-001 |
| endpoint_path | graphql/GetSavedSearch |
| method | QUERY |
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
| service_file | contact360.io/api/app/graphql/modules/saved_searches/queries.py |
| router_file | contact360/dashboard/src/services/graphql/savedSearchesService.ts |


## Service / repository methods

### service_methods

- getSavedSearch

## Inventory

- **page_count:** 0
- **Source:** `query_get_saved_search_graphql.json`

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

- **Inbound**: `Search Page` (Saved Search Detail).
- **Outbound**: `QueryContacts`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_saved_search_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
