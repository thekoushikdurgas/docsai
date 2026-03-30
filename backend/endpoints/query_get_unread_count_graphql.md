---
title: "graphql/GetUnreadCount"
source_json: query_get_unread_count_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUnreadCount

## Overview

Get count of unread notifications for the current user. Returns UnreadCountResponse with count field. User isolation enforced - counts only user's own notifications. Used by NotificationCenter component and useNotifications hook for displaying unread badge.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_unread_count_graphql |
| _id | query_get_unread_count_graphql-001 |
| endpoint_path | graphql/GetUnreadCount |
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
| service_file | appointment360/app/graphql/modules/notifications/queries.py |
| router_file | contact360/dashboard/src/services/graphql/notificationsService.ts |


## Service / repository methods

### service_methods

- getUnreadCount
- unreadCount

## Inventory

- **page_count:** 0
- **Source:** `query_get_unread_count_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `notifications` | READ | [notifications.sql](../database/tables/notifications.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: COUNT query on `notifications` where `is_read = false` via NotificationRepository. User-scoped.

## Related endpoint graph

- **Inbound**: `NotificationCenter` (Frontend badge), `Dashboard Layout` (header badge), all pages with notification bell icon.
- **Outbound**: `ListNotifications` (open panel on click).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_unread_count_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
