---
title: "graphql/GetUsage"
source_json: query_get_usage_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUsage

## Overview

Get feature usage for current user. Accepts optional featureKey (String) to get specific feature usage. Returns UsageInfo with features (array of FeatureUsage with featureKey, used, limit, remaining, percentage, resetAt, isUnlimited). Limits are role-based: FreeUser (limited), ProUser (higher limits), Admin/SuperAdmin (unlimited). Usage resets monthly. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_usage_graphql |
| _id | query_get_usage_graphql-001 |
| endpoint_path | graphql/GetUsage |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/usage/queries.py |
| router_file | contact360/dashboard/src/services/graphql/usageService.ts |


## GraphQL operation

```graphql
query GetUsage($featureKey: String) { usage { usage(featureKey: $featureKey) { features { featureKey used limit remaining percentage resetAt isUnlimited } } } }
```

## Service / repository methods

### service_methods

- usage

### repository_methods

- get_usage_by_user

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /usage | Usage Page | usageService | useUsageTracking | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /dashboard | Dashboard Page | usageService | useUsageTracking | secondary | data_fetching | 2026-02-03T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 2
- **Source:** `query_get_usage_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Usage Tracking).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_usage` | READ | [user_usage.sql](../database/tables/user_usage.sql) |
| `users` | READ | [users.sql](../database/tables/users.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gatekeeping**: Direct dependency for all credit-consuming features.

## Related endpoint graph

- **Inbound**: `Dashboard`, `Usage Page`.
- **Outbound**: `ResetUsage` (Admin-only).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_usage_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
