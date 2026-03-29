---
title: "graphql/GetDocumentationPage"
source_json: query_get_documentation_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetDocumentationPage

## Overview

Get a documentation page by page_id. Accepts pageId (String!, required, non-empty string, max 255 characters). Returns DocumentationPage with pageId, title, description, category, contentUrl (presigned S3 URL), lastUpdated, version, and id. Uses LambdaDocumentationClient.get_page to retrieve page metadata. Response structure is validated before conversion to GraphQL type. Raises NotFoundError if page doesn't exist. Public endpoint (no authentication required). Response is cached.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_documentation_page_graphql |
| _id | query_get_documentation_page_graphql-001 |
| endpoint_path | graphql/GetDocumentationPage |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.8.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/documentation/queries.py |
| router_file | contact360/dashboard/src/services/graphql/documentationService.ts |


## Service / repository methods

### service_methods

- getDocumentationPage

## Inventory

- **page_count:** 0
- **Source:** `query_get_documentation_page_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Knowledge Base).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `documentation_pages` | READ | [documentation_pages.sql](../database/tables/documentation_pages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Knowledge Base Architecture](../database/documentation_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Content managed via `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Docs Sidebar`, `Help Center`.
- **Outbound**: `ListDocumentationPages`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_documentation_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
