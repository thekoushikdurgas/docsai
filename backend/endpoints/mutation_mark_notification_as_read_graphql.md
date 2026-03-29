---
title: "graphql/MarkNotificationAsRead"
source_json: mutation_mark_notification_as_read_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/MarkNotificationAsRead

## Overview

Mark a notification as read. Accepts MarkAsReadInput with notificationId (required, ID/UUID). Updates isRead to true and sets readAt timestamp. Returns updated Notification with id, title, message, type, priority, isRead (true), readAt (DateTime). User isolation enforced - users can only mark their own notifications. Raises NotFoundError (404) if notification not found. Raises ForbiddenError (403) if user doesn't own notification.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_mark_notification_as_read_graphql |
| _id | mutation_mark_notification_as_read_graphql-001 |
| endpoint_path | graphql/MarkNotificationAsRead |
| method | MUTATION |
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
| service_file | appointment360/app/graphql/modules/notifications/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/notificationsService.ts |


## GraphQL operation

```graphql
mutation MarkNotificationAsRead($input: MarkAsReadInput!) { notifications { markAsRead(input: $input) { id title isRead readAt } } }
```

## Service / repository methods

### service_methods

- markAsRead

### repository_methods

- update_notification

## Inventory

- **page_count:** 0
- **Source:** `mutation_mark_notification_as_read_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Ecosystem Integrations & Platform Productization.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `notifications` | READ / WRITE | [notifications.sql](../database/tables/notifications.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Updates `is_read` and `read_at` on `notifications` via NotificationRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Notification Center` (Frontend), `ListNotifications` (notification panel click).
- **Outbound**: `GetUnreadCount` (badge refresh), `ListNotifications` (UI refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_mark_notification_as_read_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
