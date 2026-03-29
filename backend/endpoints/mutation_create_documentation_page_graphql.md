---
title: "graphql/CreateDocumentationPage"
source_json: mutation_create_documentation_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateDocumentationPage

## Overview

Create a new documentation page. Accepts CreateDocumentationPageInput with pageId (required, String, max 255 chars), title (required, String, max 500 chars), description (optional, String, max 1000 chars), category (optional, String, max 100 chars), content (required, String, markdown, max 100000 chars). Returns DocumentationPage with pageId, title, description, category, contentUrl (presigned S3 URL), lastUpdated, version, id. Uses Lambda Documentation service - uploads markdown to S3, saves metadata to MongoDB. Raises ConflictError (409) if pageId exists. Raises ForbiddenError (403) if not Admin/SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_documentation_page_graphql |
| _id | mutation_create_documentation_page_graphql-001 |
| endpoint_path | graphql/CreateDocumentationPage |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/documentation/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/documentationService.ts |


## GraphQL operation

```graphql
mutation CreateDocumentationPage($input: CreateDocumentationPageInput!) { documentation { createDocumentationPage(input: $input) { pageId title description category contentUrl version } } }
```

## Service / repository methods

### service_methods

- createDocumentationPage

## Inventory

- **page_count:** 0
- **Source:** `mutation_create_documentation_page_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Knowledge Base).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `documentation_pages` | WRITE | [documentation_pages.sql](../database/tables/documentation_pages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Knowledge Base Architecture](../database/documentation_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Content managed via `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Admin Docs Editor`.
- **Outbound**: `GetDocumentationPage`, `UpdateDocumentationPage`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_documentation_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
