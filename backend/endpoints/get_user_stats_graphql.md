---
title: "graphql/GetUserStats"
source_json: get_user_stats_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUserStats

## Overview

Get user statistics for admin dashboard. No input required. Returns UserStats with totalUsers (Int), activeUsers (Int), inactiveUsers (Int), usersByRole (array of {role, count}), usersByPlan (array of {plan, count}), newUsersThisMonth (Int), newUsersThisWeek (Int). Raises ForbiddenError (403) if not Admin/SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_user_stats_graphql |
| _id | get_user_stats_graphql-001 |
| endpoint_path | graphql/GetUserStats |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 20 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/admin/queries.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## GraphQL operation

```graphql
query GetUserStats { admin { userStats { totalUsers activeUsers usersByRole { role count } usersByPlan { plan count } newUsersThisMonth } } }
```

## Service / repository methods

### service_methods

- userStats

### repository_methods

- get_user_stats

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/statistics | Admin Statistics Page | adminService | useAdminStatistics | primary | analytics | 2026-01-20T00:00:00.000000+00:00 |
| /admin/users | Admin Users Page | adminService | useAdminUsers | secondary | analytics | 2026-01-20T00:00:00.000000+00:00 |
| /dashboard | Dashboard Page | adminService | useDashboardPage | conditional | analytics | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 3
- **Source:** `get_user_stats_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — User & Billing (Statistics).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | READ | [users.sql](../database/tables/users.sql) |
| `user_usage` | READ | [user_usage.sql](../database/tables/user_usage.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API**: Aggregate usage stats via `lambda/logs.api`.

## Related endpoint graph

- **Inbound**: `Admin Statistics Page`.
- **Outbound**: `ListUsers`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_user_stats_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
