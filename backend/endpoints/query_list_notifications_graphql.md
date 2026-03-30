---
title: "graphql/ListNotifications"
source_json: query_list_notifications_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListNotifications

## Overview

List notifications for current user. Accepts optional NotificationFilterInput with unreadOnly (Boolean), type (enum: SYSTEM, SECURITY, ACTIVITY, MARKETING, BILLING), priority (enum: LOW, MEDIUM, HIGH, URGENT), limit (Int, default 100), offset (Int, default 0). Returns NotificationConnection with items (array of Notification with id, title, message, type, priority, isRead, createdAt), total, limit, offset, hasNext, hasPrevious. User isolation enforced at repository level - users can only view their own notifications.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_notifications_graphql |
| _id | query_list_notifications_graphql-001 |
| endpoint_path | graphql/ListNotifications |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 9.x |
| introduced_in | 9.0.0 |


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


## GraphQL operation

```graphql
query ListNotifications($input: NotificationFilterInput) { notifications { notifications(input: $input) { items { id title message type priority isRead createdAt } total hasNext } } }
```

## Service / repository methods

### service_methods

- notifications

### repository_methods

- get_notifications_by_user

## Inventory

- **page_count:** 0
- **Source:** `query_list_notifications_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Ecosystem Integrations & Platform Productization.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `notifications` | READ | [notifications.sql](../database/tables/notifications.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Paginated read from `notifications` via NotificationRepository with filter support (type, priority, unread-only).

## Related endpoint graph

- **Inbound**: `Notification Center` (Frontend panel listing), `Dashboard` (notification widget).
- **Outbound**: `GetNotification` (detail view), `MarkNotificationAsRead` (mark on open), `DeleteNotifications` (bulk actions).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_notifications_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
