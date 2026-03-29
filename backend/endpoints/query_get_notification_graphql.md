---
title: "graphql/GetNotification"
source_json: query_get_notification_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetNotification

## Overview

Get a single notification by ID. Accepts notification_id (ID!, required, positive integer). Returns Notification with id, title, message, type, priority, isRead, createdAt. Requires authentication. User can only view their own notifications. Raises NotFoundError (404) if notification not found or not owned by current user.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_notification_graphql |
| _id | query_get_notification_graphql-001 |
| endpoint_path | graphql/GetNotification |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-02-03T00:00:00.000000+00:00 |
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
query GetNotification($notification_id: ID!) { notifications { notification(notification_id: $notification_id) { id title message type priority isRead createdAt } } }
```

## Service / repository methods

### service_methods

- notification

## Inventory

- **page_count:** 0
- **Source:** `query_get_notification_graphql.json`

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

- **Gateway DB**: Reads single notification by ID from `notifications` via NotificationRepository. User isolation enforced.

## Related endpoint graph

- **Inbound**: `Notification Center` (Frontend detail view).
- **Outbound**: `MarkNotificationAsRead` (auto-mark on view).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_notification_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
