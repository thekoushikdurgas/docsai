# Media Conventions (DocsAI)

Conventions and mapping used to align `media/endpoints`, `media/postman`, and `media/relationship` with the appointment360 backend and JSON model specs.

## 1. Endpoint ID and path

- **endpoint_path**: Canonical form `graphql/{OperationName}` (e.g. `graphql/GetUserStats`, `graphql/Login`). OperationName matches the backend GraphQL field/resolver name in PascalCase as used in docs.
- **endpoint_id**: May use `query_*_graphql` or `mutation_*_graphql` (e.g. `query_get_user_stats_graphql`, `mutation_login_graphql`), or the existing mixed convention (e.g. `get_user_stats_graphql`) for backward compatibility. All references (postman `endpoint_mappings`, relationship `endpoint_reference`) must use the same `endpoint_id` as in the endpoint document.
- **File name**: `{endpoint_id}.json` under `media/endpoints/`.
- **_id**: `{endpoint_id}-001` (or same pattern) in each endpoint JSON.

## 2. Relationship directory

- **Storage**: `media/relationship/` (by-page, by-endpoint, index.json, relationships_index.json). The spec mentions `media/retations/` for backward compatibility; this repo uses `media/relationship`.

## 3. Backend source of truth

- **Operations**: All GraphQL queries and mutations are defined in `lambda/appointment360/app/graphql/modules/<module>/queries.py` and `mutations.py`.
- **service_file**: Path from repo root, e.g. `appointment360/app/graphql/modules/billing/queries.py` or `appointment360/app/graphql/modules/billing/mutations.py`.
- **service_methods**: Resolver method name(s) on the GraphQL type (e.g. `billing`, `subscribe`, `userStats`).

## 4. usage_type and usage_context (endpoints and relationships)

- **usage_type**: One of `primary`, `secondary`, `conditional`, `lazy`, `prefetch`.
- **usage_context**: One of `data_fetching`, `data_mutation`, `authentication`, `analytics`, `realtime`, `background`.

## 5. Relationship ID format

- **relationship_id**: `{page_slug}_graphql_{CanonicalOperation}_{METHOD}` (e.g. `dashboard_graphql_GetUserStats_QUERY`). CanonicalOperation matches `endpoint_path` after `graphql/` (e.g. `GetUserStats`).
