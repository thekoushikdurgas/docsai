---
title: "graphql/DeleteDocumentationPage"
source_json: mutation_delete_documentation_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteDocumentationPage

## Overview

Delete a documentation page. Accepts DeleteDocumentationPageInput with pageId (required, String, max 255 chars). Removes page from both S3 (markdown content) and MongoDB (metadata). Returns Boolean (true if deleted). Uses Lambda Documentation service. Raises NotFoundError (404) if page not found. Raises ForbiddenError (403) if not Admin/SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_documentation_page_graphql |
| _id | mutation_delete_documentation_page_graphql-001 |
| endpoint_path | graphql/DeleteDocumentationPage |
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
mutation DeleteDocumentationPage($input: DeleteDocumentationPageInput!) { documentation { deleteDocumentationPage(input: $input) } }
```

## Service / repository methods

### service_methods

- deleteDocumentationPage

## Inventory

- **page_count:** 0
- **Source:** `mutation_delete_documentation_page_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Knowledge Base).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `documentation_pages` | DELETE | [documentation_pages.sql](../database/tables/documentation_pages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Knowledge Base Architecture](../database/documentation_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Content managed via `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Admin Docs Editor`.
- **Outbound**: `ListDocumentationPages`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_documentation_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
