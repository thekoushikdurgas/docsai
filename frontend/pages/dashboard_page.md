---

title: "Dashboard"
page_id: dashboard_page
source_json: dashboard_page.json
generator: json_to_markdown.py
---

# Dashboard

## Overview

- **page_id:** finder_page
- **page_type:** dashboard (alias)
- **codebase:** app
- **surface:** app
- **era_tags:** 2.x, 10.x, 11.x
- **flow_id:** dashboard
- **_id:** dashboard_page-001

## Metadata

- **route:** /dashboard
- **file_path:** contact360.io/app/app/(dashboard)/dashboard/page.tsx
- **purpose:** Main dashboard page with stats (admin/superAdmin only), performance chart, activity feed, pending exports, usage overview, quick actions, and upgrade banner for free users.
- **s3_key:** data/pages/dashboard_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Stats grid (userStats) visible only to admin/superAdmin. Performance chart and activity feed gated via DashboardComponentGuard.
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00

### uses_endpoints (4)

- `graphql/UserStats` — Admin user statistics (total users, active users, users by role/plan). Only batched when includeStats is true (admin/superAdmin). Via dashboardPageApi.
- `graphql/Activities` — Recent user activities with limit (default 5). Batched with userStats and exports in dashboardPageApi via useDashboardPage hook.
- `graphql/ListExports` — List pending and processing exports. Filtered by status. Batched in dashboardPageApi via useDashboardPage hook. Auto-refresh every 60s.
- `graphql/Usage` — Feature usage via UsageOverview. Fetched by useUsageTracking within UsageOverview component.

### UI components (metadata)

- **DashboardPage** — `app/(dashboard)/dashboard/page.tsx`
- **WelcomeBar** — `components/dashboard/WelcomeBar.tsx`
- **DashboardOverview** — `components/dashboard/DashboardOverview.tsx`
- **DashboardActivityTab** — `components/dashboard/DashboardActivityTab.tsx`
- **DashboardUsageTab** — `components/dashboard/DashboardUsageTab.tsx`
- **Tabs** — `components/ui/tabs/Tabs.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **DashboardLineChart** — `components/dashboard/DashboardLineChart.tsx`
- **TopSourcesCard** — `components/dashboard/TopSourcesCard.tsx`
- **ActivityFeedCard** — `components/dashboard/ActivityFeedCard.tsx`
- **SegmentationCard** — `components/dashboard/SegmentationCard.tsx`
- **SatisfactionCard** — `components/dashboard/SatisfactionCard.tsx`
- **AddComponentCard** — `components/dashboard/AddComponentCard.tsx`
- **ResourceAllocationCard** — `components/dashboard/ResourceAllocationCard.tsx`
- **QuickActionsGrid** — `components/dashboard/QuickActionsGrid.tsx`
- **PendingJobsBlock** — `components/dashboard/PendingJobsBlock.tsx`

- **versions:** []
- **endpoint_count:** 4

### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Dashboard

### description

Main dashboard page with stats (admin/superAdmin only), performance chart, activity feed, pending exports, usage overview, quick actions, and upgrade banner for free users.

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| stats | 2 | Statistics |
| performance_chart | 2 | Performance |
| activity_feed | 2 | Recent Activity |
| usage | 2 | Usage Overview |
| exports | 2 | Pending Exports |

### subheadings

### tabs

| id | label | era |
| --- | --- | --- |
| overview | Overview | 1.x |
| activity | Activity | 6.x |
| usage | Usage & Jobs | 1.x, 6.x |

### buttons

| action | component | id | label | type | visibility | era |
| --- | --- | --- | --- | --- | --- | --- |
| navigate to /email | DashboardQuickActions | quick-find-email | Find Email | primary |  | 1.x |
| navigate to /email (verifier tab) | DashboardQuickActions | quick-verify-email | Verify Email | secondary |  | 2.x |
| navigate to /files | DashboardQuickActions | quick-upload-csv | Upload CSV | secondary |  | 3.x |
| navigate to /contacts | DashboardQuickActions | quick-view-contacts | View Contacts | ghost |  | 3.x |
| navigate to /billing | DashboardUpgradeBanner | upgrade-cta | Upgrade Plan | primary | free users only | 1.x |
| navigate to /activities | DashboardActivityFeed | view-all-activity | View All Activity | link |  | 6.x |
| navigate to /jobs | DashboardPendingExports | view-all-exports | View All Jobs | link |  | 6.x |
| retry query | ErrorState | retry-btn | Retry | secondary | error state only | 6.x |

### input_boxes

### text_blocks

| component | content | id | type | visibility |
| --- | --- | --- | --- | --- |
| DashboardHeader | Welcome back, {userName} | welcome-message | heading |  |
| DashboardUpgradeBanner | You're on the Free plan. Upgrade to Pro for bulk operations, AI chat, and priority support. | upgrade-banner-text | info | free users only |
| DashboardActivityFeed | No recent activity. Start by finding an email or uploading a CSV file. | empty-activity | empty-state |  |
| DashboardPendingExports | No pending jobs. Create a new export to get started. | empty-exports | empty-state |  |

### checkboxes

### radio_buttons

### progress_bars

| color_logic | component | id | label | polling_interval | purpose | type |
| --- | --- | --- | --- | --- | --- | --- |
| green > 50%, amber 20-50%, red < 20% | UsageOverview | credit-balance-bar | Credit balance |  | Shows remaining credits vs. plan limit | determinate |
|  | DashboardPendingExports | export-progress | Export job progress | 60s | Shows processing progress for active exports | determinate |

### graphs

- **[0]**
  - **id:** performance-line-chart
  - **label:** Activity performance over time
  - **chart_type:** line
  - **data_source:** useDashboardPage → adminService/activitiesService
  - **x_axis:** Date (daily)
  - **y_axis:** Count (lookups, verifications, exports)
  - **component:** DashboardLineChart

- **[1]**
  - **id:** stats-cards
  - **label:** User statistics summary cards
  - **chart_type:** stat_cards
  - **data_source:** adminService.UserStats (admin/superAdmin only)
  - **metrics**
    - total users
    - active users
    - users by role
    - users by plan

  - **component:** StatsGrid
  - **visibility:** admin/superAdmin only

### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| DashboardPage | dashboard-load-flow | Dashboard page load flow | ['useSessionGuard checks JWT', 'DashboardAccessGate checks role', 'useDashboardPage batches: UserStats + Activities + Exports + Usage', 'DashboardComponentGuard gates chart/feed per role', 'Auto-refre |

### components

| file_path | name | purpose | visibility | era |
| --- | --- | --- | --- | --- |
| components/dashboard/WelcomeBar.tsx | WelcomeBar | Header greeting with user name, plan label, and date |  | 0.x, 1.x |
| components/dashboard/DashboardOverview.tsx | DashboardOverview | Statistics grid, activity feed, and job summary |  | 1.x |
| components/dashboard/DashboardActivityTab.tsx | DashboardActivityTab | Full timeline of user/system events |  | 6.x |
| components/dashboard/DashboardUsageTab.tsx | DashboardUsageTab | Credit usage charts and job history |  | 1.x, 6.x |
| components/ui/tabs/Tabs.tsx | Tabs | Generic tab switching component |  | 0.x |
| components/shared/ErrorState.tsx | ErrorState | Error display with retry logic |  | 6.x |
| components/shared/LottiePlayer.tsx | LottiePlayer | Dashboard animation for loading states |  | 0.x |

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| context/AuthContext.ts | useAuth | User session and profile data | 0.x |
| hooks/useDashboardData.ts | useDashboardData | Fetches overview stats and recent activities | 0.x, 6.x |
| hooks/useJobs.ts | useJobs | Monitors background task status | 1.x, 7.x |
| next/navigation | useRouter, useSearchParams | Routing and tab state persistence | 0.x |

### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/adminService.ts | adminService | ['UserStats'] |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities'] |
| services/graphql/usageService.ts | usageService | ['Usage'] |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User identity and token |
| context/RoleContext.tsx | RoleContext | Role-based plan labeling (PREMIUM, ADMIN) |

### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/dashboardMapper.ts | dashboardMapper | Map API responses to chart/stats UI models |
| lib/dashboardConstants.ts | dashboardConstants | REFRESH_INTERVAL_MS, STATS_CONFIG |

### ui_components

### endpoints

| condition | hook | method | operation | service |
| --- | --- | --- | --- | --- |
| admin/superAdmin only | useDashboardPage | QUERY | UserStats | adminService |
|  | useDashboardPage | QUERY | GetActivities | activitiesService |
|  | useDashboardPage | QUERY | ListExports | exportsService |
|  | useUsageTracking | QUERY | Usage | usageService |

## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| quick-find-email | Find Email | primary | navigate to /email | DashboardQuickActions |
| quick-verify-email | Verify Email | secondary | navigate to /email (verifier tab) | DashboardQuickActions |
| quick-upload-csv | Upload CSV | secondary | navigate to /files | DashboardQuickActions |
| quick-view-contacts | View Contacts | ghost | navigate to /contacts | DashboardQuickActions |
| upgrade-cta | Upgrade Plan | primary | navigate to /billing | DashboardUpgradeBanner |
| view-all-activity | View All Activity | link | navigate to /activities | DashboardActivityFeed |
| view-all-exports | View All Jobs | link | navigate to /jobs | DashboardPendingExports |

### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | color_logic | component |
| --- | --- | --- | --- | --- | --- |
| credit-balance-bar | Credit balance | Shows remaining credits vs. plan limit | determinate | green > 50%, amber 20-50%, red < 20% | UsageOverview |
| export-progress | Export job progress | Shows processing progress for active exports | determinate |  | DashboardPendingExports |

### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useDashboardPage | UserStats | adminService | query |
| useDashboardPage | GetActivities | activitiesService | query |
| useDashboardPage | ListExports | exportsService | query |

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useDashboardPage.ts | useDashboardPage | Batched: UserStats + Activities + Exports; 60s export polling |
| hooks/dashboard/useDashboardPageAccess.ts | useDashboardPageAccess | Role-based section visibility (showStats, showChart) |
| hooks/useUsage.ts | useUsageTracking | Feature credit usage for UsageOverview |
| hooks/useSessionGuard.ts | useSessionGuard | Enforces authenticated session |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/adminService.ts | adminService | ['UserStats'] |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities'] |
| services/graphql/usageService.ts | usageService | ['Usage'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/UserStats, graphql/GetActivities, graphql/ListExports, graphql/Usage | dashboard analytics and status |

## Data Sources

- Appointment360 GraphQL gateway
- service-owned application databases via backend modules

## Flow summary

app dashboard page -> hooks/page APIs -> GraphQL gateway queries -> aggregated dashboard cards/charts/feeds with role gating

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.
- **6.x** — Reliability & scaling — analytics, activities, jobs, status, error/retry/skeleton patterns.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [W:WelcomeBar] + [S:Tabs] + [U:TabContent] > [Q:StatCards] + [A:ActivityLog] + [J:PendingJobs] -> {useDashboardData}

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/dashboard`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [login_page.md](login_page.md) redirect.

**Typical outbound:** [email_page.md](email_page.md) (Quick Actions), [contacts_page.md](contacts_page.md), [billing_page.md](billing_page.md), [jobs_page.md](jobs_page.md), [activities_page.md](activities_page.md).

**Cross-host:** Marketing [landing_page.md](landing_page.md) login links. Product pages on **root** deep-link to app auth.
**Backend:** Appointment360 GraphQL gateway; aggregates multiple service-owned application databases.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [contacts_page](contacts_page.md)
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
| `UserStats` | [get_user_stats_graphql.md](../../backend/endpoints/get_user_stats_graphql.md) | QUERY | 1.x |
| `Activities` | [get_activities_graphql.md](../../backend/endpoints/get_activities_graphql.md) | QUERY | 0.x |
| `ListExports` | [list_exports_graphql.md](../../backend/endpoints/list_exports_graphql.md) | QUERY | 3.x |
| `Usage` | [query_get_usage_graphql.md](../../backend/endpoints/query_get_usage_graphql.md) | QUERY | 1.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
