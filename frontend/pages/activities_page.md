---
title: "Activities"
page_id: activities_page
source_json: activities_page.json
generator: json_to_markdown.py
---

# Activities

## Overview

- **page_id:** activities_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 1.x, 6.x, 11.x
- **flow_id:** activities
- **_id:** activities_page-001

## Metadata

- **route:** /activities
- **file_path:** contact360.io/app/app/(dashboard)/activities/page.tsx
- **purpose:** Activity tracking page with stats cards, filterable activity table, and details modal. Filters: service_type, action_type, status, date range. Data batched via activitiesPageApi (activities + activityStats).
- **s3_key:** data/pages/activities_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
### uses_endpoints (2)

- `graphql/GetActivities` — List user activities via activities.activities. Filters: serviceType, actionType, status, startDate, endDate, limit, offset. Batched in activitiesPageApi via useActivitiesPage.
- `graphql/GetActivityStats` — Get activity stats via activities.activityStats. Returns totalActivities, byServiceType, byActionType, byStatus. Batched in activitiesPageApi via useActivitiesPage. Optional (includeStats).

### UI components (metadata)

- **ActivitiesPage** — `app/(dashboard)/activities/page.tsx`
- **ActivitiesSidebar** — `components/activities/ActivitiesSidebar.tsx`
- **ActivitiesToolbar** — `components/activities/ActivitiesToolbar.tsx`
- **ActivityStatsCards** — `components/activities/ActivityStatsCards.tsx`
- **ActivityTable** — `components/activities/ActivityTable.tsx`
- **ActivitiesPagination** — `components/activities/ActivitiesPagination.tsx`
- **ActivityDetailsModal** — `components/activities/ActivityDetailsModal.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **EmptyState** — `components/shared/EmptyState.tsx`

- **versions:** []
- **endpoint_count:** 2
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Activities

### description

Activity tracking page with stats cards, filterable activity table, and details modal. Filters: service_type, action_type, status, date range. Data batched via activitiesPageApi (activities + activityStats).


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| stats | 2 | Statistics |
| table | 2 | Activity Table |


### subheadings



### tabs



### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| ActivitiesToolbar.onRefresh | ActivitiesToolbar | refresh-activities | Refresh | icon | 6.x |
| ActivitiesToolbar.onOpenFilters | ActivitiesToolbar | open-filters | Filters | secondary | 0.x |
| ActivityTable.onSelectActivity | ActivityTable | view-activity-detail | View Details | ghost | 0.x |
| ActivitiesSidebar.onFiltersChange (reset) | ActivitiesSidebar | clear-filters | Clear Filters | secondary | 0.x |
| ActivityDetailsModal.onCopyTraceId | ActivityDetailsModal | copy-trace-id | Copy Trace ID | ghost | 6.x |


### input_boxes

| component | id | label | placeholder | required | type | era |
| --- | --- | --- | --- | --- | --- | --- |
| ActivitiesSidebar | search-activities | Search | Search activities... | False | search | 0.x |
| ActivitiesSidebar | date-start | From date |  | False | date | 0.x |
| ActivitiesSidebar | date-end | To date |  | False | date | 0.x |
| ActivitiesSidebar | service-filter | Service | Select service... | False | select | 0.x |


### text_blocks

| component | content | id | type | era |
| --- | --- | --- | --- | --- |
| ActivityTable | No activities yet. Start by finding an email or uploading a CSV file. | empty-activities | empty-state | 0.x |
| LottiePlayer | src="/animation/activity.json" | loading-anim | lottie | 6.x |
| ActivitiesToolbar | Syncing in background... | background-sync | info | 6.x |


### components



### checkboxes



### radio_buttons



### progress_bars



### graphs

| chart_type | component | data_source | id | label | metrics |
| --- | --- | --- | --- | --- | --- |
| stat_cards | ActivityStatsCard | activitiesService.GetActivityStats | activity-stats-cards | Activity summary stat cards | ['total', 'success', 'failed', 'pending'] |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ActivitiesPage | activity-filter-flow | Filter and view activities | ['Select service_type filter (finder/verifier/export/import)', 'Select action_type filter', 'Select status (success/failed/pending)', 'Set date range', 'useActivitiesPage refetches with new filters',  |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/activitiesConstants.ts | activitiesConstants | ACTIVITY_LABELS, ACTIVITY_ICONS, ACTIVITY_COLORS by type |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities', 'GetActivityStats'] |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useActivities.ts | useActivities | Activity data fetching, stats, and pagination | 6.x |
| lib/dashboardMapper.ts | mapActivityItemToDisplay | Transform raw API items for UI display | 0.x |
| context/AuthContext.tsx | AuthContext | User ID for filtering own activities |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User ID for filtering own activities |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useActivitiesPage | QUERY | GetActivities | activitiesService |
| useActivitiesPage | QUERY | GetActivityStats | activitiesService |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| refresh-activities | Refresh | icon | refetch activities + stats | PageHeader |
| view-activity-detail | View Details | ghost | open ActivityDetailsModal | ActivitiesTable |
| clear-filters | Clear Filters | secondary | reset all filter state | ActivitiesFilters |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| search-activities | Search | search | Search activities... | ActivitiesToolbar |
| date-start | From date | date |  | ActivitiesFilters |
| date-end | To date | date |  | ActivitiesFilters |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useActivities.ts | useActivitiesPage | Batched activities + activityStats; filter state management |
| hooks/useActivities.ts | useActivities | Activity list with pagination and filter |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities', 'GetActivityStats'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/GetActivities, graphql/GetActivityStats | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: activitiesService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useActivitiesPage, useActivities -> activitiesService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, generic sidebar, theme tokens, lottie basics.
- **1.x** — User / billing / credit — user-specific activity streams.
- **6.x** — Reliability & scaling — analytics, activities, background sync logic, performance stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [H:Header] + [F:FilterBar] + [T:ActivityTable] -> {useActivities}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/activities`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions.

**Typical outbound:** Sidebar peers; [contacts_page.md](contacts_page.md) (from detail context); [email_page.md](email_page.md).

**Cross-host:** Activity audit trail shared with **email** (Mailhub) for platform-wide event logging.
**Backend:** Appointment360 GraphQL gateway; real-time activity tracking and statistics services.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [contacts_page](contacts_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [profile_page](profile_page.md)
- [register_page](register_page.md)
- [root_page](root_page.md)
- [sequences_page](sequences_page.md)
- [settings_page](settings_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetActivities` | [get_activities_graphql.md](../../backend/endpoints/get_activities_graphql.md) | QUERY | 0.x |
| `GetActivityStats` | [query_get_activity_stats_graphql.md](../../backend/endpoints/query_get_activity_stats_graphql.md) | QUERY | 6.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
