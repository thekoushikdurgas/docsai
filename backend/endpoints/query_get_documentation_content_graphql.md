---
title: "graphql/GetDocumentationContent"
source_json: query_get_documentation_content_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetDocumentationContent

## Overview

Get documentation page markdown content directly. Accepts pageId (String!, required, non-empty string, max 255 characters). Returns DocumentationPageContent with pageId and content (plain text markdown content, not presigned URL). Uses LambdaDocumentationClient.get_page_content to retrieve markdown content. Returns plain text markdown content (not presigned URL). Raises NotFoundError if page doesn't exist. Content must be a string (validated before returning). Public endpoint (no authentication required). Response is cached.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_documentation_content_graphql |
| _id | query_get_documentation_content_graphql-001 |
| endpoint_path | graphql/GetDocumentationContent |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/pages/queries.py |
| router_file | contact360/dashboard/src/services/graphql/documentationService.ts |


## Service / repository methods

### service_methods

- fetchDocumentationContent
- pageContent

## Inventory

- **page_count:** 0
- **Source:** `query_get_documentation_content_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

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

*Generated from `query_get_documentation_content_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
