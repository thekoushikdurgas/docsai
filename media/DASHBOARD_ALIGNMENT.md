# Dashboard Page – Media Alignment

This document describes how the **dashboard page** (`/dashboard`) is aligned across `media/pages`, `media/endpoints`, `media/postman`, and `media/relationship` per the JSON model specs.

## Dashboard's Four Operations

The dashboard page uses four GraphQL operations (see `media/pages/dashboard_page.json` → `metadata.uses_endpoints`):

| Operation | Endpoint path | Via service   | Usage type  | Usage context   |
|-----------|---------------|---------------|-------------|-----------------|
| UserStats | graphql/GetUserStats | adminService   | conditional | analytics        |
| Activities | graphql/GetActivities | activitiesService | primary   | data_fetching    |
| ListExports | graphql/ListExports | exportsService | primary   | data_fetching    |
| Usage     | graphql/GetUsage | usageService   | secondary  | data_fetching    |

## Canonical Endpoint Documents

Each operation has one canonical endpoint document under `media/endpoints/`:

| Endpoint ID                 | File                               | used_by_pages includes /dashboard |
|----------------------------|------------------------------------|-----------------------------------|
| get_user_stats_graphql     | get_user_stats_graphql.json        | Yes                               |
| get_activities_graphql     | get_activities_graphql.json        | Yes                               |
| list_exports_graphql       | list_exports_graphql.json          | Yes                               |
| query_get_usage_graphql    | query_get_usage_graphql.json       | Yes                               |

All four conform to **endpoints_json_models.md** (EndpointDocumentation, EndpointPageUsage). `page_count` equals `used_by_pages.length`.

## Relationship (by-page)

- **File:** `media/relationship/by-page/dashboard.json`
- **Source:** Generated from pages by `scripts/sync_pages_to_relationships.py` (page → endpoints).
- Each of the four entries has:
  - **endpoint_path** aligned with endpoint docs (e.g. `graphql/GetUserStats`, `graphql/GetActivities`, `graphql/ListExports`, `graphql/GetUsage`).
  - **endpoint_reference:** `{ endpoint_id, endpoint_path, method, api_version }` pointing to the canonical endpoint document.
  - **postman_reference:** `{ mapping_id, config_id: "contact360" }` pointing to the Postman configuration's endpoint mapping.

## Postman Configuration

- **File:** `media/postman/contact360.json`
- **endpoint_mappings:** Four entries link documentation endpoints to Postman requests:

| mapping_id                    | endpoint_id                 | postman_request_id (UUID)     | postman_folder_path              |
|------------------------------|-----------------------------|-------------------------------|----------------------------------|
| map-get_user_stats_graphql   | get_user_stats_graphql      | 550e8400-e29b-41d4-a716-446655440001 | ["GraphQL Dashboard", "Admin"]   |
| map-get_activities_graphql   | get_activities_graphql      | 550e8400-e29b-41d4-a716-446655440002 | ["GraphQL Dashboard", "Activities"] |
| map-list_exports_graphql     | list_exports_graphql        | 550e8400-e29b-41d4-a716-446655440003 | ["GraphQL Dashboard", "Exports"] |
| map-query_get_usage_graphql  | query_get_usage_graphql     | 550e8400-e29b-41d4-a716-446655440004 | ["GraphQL Dashboard", "Usage"]   |

- **sync_status:** `synced`. The Postman collection in `contact360.json` includes a **GraphQL Dashboard** folder with four requests (User Stats (Admin), List Activities, List Exports, Get Usage) using the above UUIDs as item `id`. Each request is POST `{{baseUrl}}/graphql` with the corresponding GraphQL query in the body.

## Indexes

- **media/endpoints/index.json** – Lightweight index (endpoint_id, path, file_name). No regeneration needed for the dashboard-four changes; only `used_by_pages` was updated in one file.
- **media/postman/index.json** – Lists configurations (contact360); no structural change.
- To fully regenerate indexes: use Django management command `normalize_media_indexes` (with `--write`) or the IndexGeneratorService from the DocsAI app.

## Specs

- Endpoints: `media/json_models/endpoints_json_models.md`
- Postman: `media/json_models/postman_json_models.md`
- Relationships: `media/json_models/relationship_json_models.md`
