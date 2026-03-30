---
title: "graphql/UpdatePreferences"
source_json: mutation_update_notification_preferences_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdatePreferences

## Overview

Update notification preferences for the current user. Accepts UpdateNotificationPreferencesInput with optional boolean fields: emailDigest, newLeads, securityAlerts, marketing, billingUpdates, pushEnabled, emailEnabled. Supports partial updates. Preferences stored as JSON in user profile. Returns updated NotificationPreferences. Used by profile page and useNotifications hook.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_notification_preferences_graphql |
| _id | mutation_update_notification_preferences_graphql-001 |
| endpoint_path | graphql/UpdatePreferences |
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

- updatePreferences
- updateNotificationPreferences

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_notification_preferences_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Ecosystem Integrations & Platform Productization.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_profiles` | READ / WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Updates notification preferences JSON field on `user_profiles` via NotificationRepository. Partial update supported.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend settings section), `Notification Center` (preferences modal).
- **Outbound**: `ListNotifications` (filter behavior changes based on preferences).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_notification_preferences_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
