---
title: "graphql/UpdateDocumentationPage"
source_json: mutation_update_documentation_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateDocumentationPage

## Overview

Update an existing documentation page. Accepts pageId (String!, required, non-empty string, max 255 characters) and UpdateDocumentationPageInput with optional fields: title (String, max 500 characters), description (String, max 1000 characters), category (String, max 100 characters), and content (String, max 100000 characters). At least one field must be provided. Returns DocumentationPage with pageId, title, description, category, contentUrl, lastUpdated, version, and id. Role check via UserProfileRepository (must be Admin or SuperAdmin). Uses LambdaDocumentationClient.update_page to update page. Only provided fields are updated (partial update). Raises NotFoundError if page doesn't exist. Response structure is validated before conversion to GraphQL type.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_documentation_page_graphql |
| _id | mutation_update_documentation_page_graphql-001 |
| endpoint_path | graphql/UpdateDocumentationPage |
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


## Service / repository methods

### service_methods

- updateDocumentationPage
- page

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_documentation_page_graphql.json`

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
- **Outbound**: `GetDocumentationPage`, `DeleteDocumentationPage`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_documentation_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
