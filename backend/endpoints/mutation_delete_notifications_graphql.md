---
title: "graphql/DeleteNotifications"
source_json: mutation_delete_notifications_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteNotifications

## Overview

Delete multiple notifications. Accepts DeleteNotificationsInput with notificationIds array (max 1000 notifications). User isolation enforced - users can only delete their own notifications. Returns DeleteNotificationsResponse with count of deleted notifications. Used by NotificationCenter and useNotifications hook for bulk deletion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_notifications_graphql |
| _id | mutation_delete_notifications_graphql-001 |
| endpoint_path | graphql/DeleteNotifications |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
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


## Service / repository methods

### service_methods

- deleteMultipleNotifications
- deleteNotifications

## Inventory

- **page_count:** 0
- **Source:** `mutation_delete_notifications_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Ecosystem Integrations & Platform Productization.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `notifications` | DELETE | [notifications.sql](../database/tables/notifications.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Bulk delete from `notifications` via NotificationRepository. User isolation enforced — cannot delete other users' notifications.

## Related endpoint graph

- **Inbound**: `Notification Center` (Frontend bulk delete), `ListNotifications` (clear all action).
- **Outbound**: `GetUnreadCount` (badge refresh), `ListNotifications` (UI refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_notifications_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
