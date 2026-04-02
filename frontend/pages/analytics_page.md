---
title: "Analytics"
page_id: analytics_page
source_json: analytics_page.json
generator: json_to_markdown.py
---

# Analytics

## Overview

- **page_id:** analytics_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 6.x, 11.x
- **flow_id:** analytics
- **_id:** analytics_page-001

## Metadata

- **route:** /analytics
- **file_path:** contact360.io/app/app/(dashboard)/analytics/page.tsx
- **purpose:** Analytics Studio: Performance monitoring and diagnostic dashboard for LCP, FID, CLS, TTFB, and API latency trends.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z

### uses_endpoints (1)

- `graphql/PerformanceMetrics` — Get performance metrics with optional date range and metric name filters. Batched via analyticsPageApi.

### UI components (metadata)

- **AnalyticsPage** — `app/(dashboard)/analytics/page.tsx`
- **StatCard** — `components/shared/StatCard.tsx`
- **Button** — `components/ui/Button.tsx`
- **Input** — `components/ui/Input.tsx`
- **Badge** — `components/ui/Badge.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **SVG Chart** — (Internal SVG implementation)

- **versions:** []
- **endpoint_count:** 1

### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Analytics

### description

Analytics dashboard for performance metrics (LCP, FID, CLS, TTFB, FCP, TTI, API latency, filter latency, page load time). Includes date range filtering and metric summary cards.

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| analytics-title | 1 | Analytics |
| performance-overview | 2 | Performance Overview |
| metrics-detail | 2 | Metrics |

### subheadings

| id | level | text |
| --- | --- | --- |
| web-vitals | 3 | Web Vitals (LCP, FID, CLS, FCP, TTFB) |
| api-perf | 3 | API Performance |
| filter-perf | 3 | Filter Latency |

### tabs

| content_ref | id | label |
| --- | --- | --- |
| analytics-web-vitals | web-vitals | Web Vitals |
| analytics-api | api | API Latency |
| analytics-page-load | page-load | Page Load |

### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| handleExport | Button | export-analytics | Export | primary | 6.x |
| handleSync | Button | sync-analytics | Sync | outline | 6.x |
| refetch (error state) | ErrorState | retry-analytics | Retry | primary | 6.x |

### input_boxes

| component | id | label | placeholder | required | type | era |
| --- | --- | --- | --- | --- | --- | --- |
| AnalyticsHeader | date-start | Start date |  | False | date | 0.x |
| AnalyticsHeader | date-end | End date |  | False | date | 0.x |
| AnalyticsHeader | metric-selector | Select metric |  | False | select | 0.x |

### text_blocks

| component | content | id | type | era |
| --- | --- | --- | --- | --- |
| LoadingSpinner | Synchronizing with neural cluster... | sync-loading | info | 6.x |
| Badge | 24 Hour Window | time-window | badge | 6.x |
| Badge | Recorded Traces | trace-count | badge | 6.x |

### checkboxes

### radio_buttons

### progress_bars

### graphs

- **[0]**
  - **id:** telemetry-svg-chart
  - **label:** Performance metrics over time
  - **chart_type:** svg-path
  - **data_source:** generateChartPath()
  - **x_axis:** Date/time
  - **y_axis:** Metric value (ms or score)
  - **multi_series:** False (single metric focus)
  - **component:** Custom SVG in AnalyticsPage
  - **era:** 6.x

- **[1]**
  - **id:** metrics-overview-cards
  - **label:** Metric summary stat cards
  - **chart_type:** stat_cards
  - **data_source:** analyticsService.PerformanceMetrics
  - **metrics:** ['Total Events', 'Avg Value', 'Peak Value', 'Reliability Score']
  - **component:** StatCard
  - **era:** 6.x

### flows

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/shared/StatCard.tsx | StatCard | Generic statistics visualization card |
| components/shared/LoadingSpinner.tsx | LoadingSpinner | Application-wide loading state |
| components/shared/ErrorState.tsx | ErrorState | Generic error handling view |
| components/ui/Button.tsx | Button | Action trigger |
| components/ui/Input.tsx | Input | Form field |
| components/ui/Badge.tsx | Badge | Status/label indicator |

### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useAnalytics.ts | useAnalytics | Data fetching for performance metrics |

### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/analyticsService.ts | analyticsService | ['PerformanceMetrics'] |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User-scoped analytics |

### utilities

### ui_components

### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useAnalyticsPage | QUERY | PerformanceMetrics | analyticsService |

## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| apply-date-range | Apply | primary | refetch with new date range | AnalyticsHeader |
| export-metrics | Export CSV | secondary | download metrics CSV | MetricsTable |
| refresh-analytics | Refresh | icon | useAnalyticsPage.refetch() | AnalyticsHeader |

### inputs

| id | label | type | component |
| --- | --- | --- | --- |
| date-from | From | date | AnalyticsHeader |
| date-to | To | date | AnalyticsHeader |
| metric-filter | Metric | select | AnalyticsHeader |

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
| hooks/useAnalytics.ts | useAnalyticsPage | Fetch performance metrics with date range filter |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/analyticsService.ts | analyticsService | ['PerformanceMetrics'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/PerformanceMetrics | dashboard data and mutations via services/hooks |

## Data Sources

- Appointment360 GraphQL gateway
- Service modules: analyticsService
- Backend-owned data stores (via GraphQL modules)

## Flow summary

app page UI -> useAnalyticsPage -> analyticsService -> GraphQL gateway -> backend modules -> rendered states

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.
- **6.x** — Reliability & scaling — analytics, activities, jobs, status, error/retry/skeleton patterns.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/analytics`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), `router.push` / `<Link>` from **### buttons** table above.

**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / [register_page.md](register_page.md); product pages on **root** deep-link to app auth.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
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
| `PerformanceMetrics` | [query_get_performance_metrics_graphql.md](../../backend/endpoints/query_get_performance_metrics_graphql.md) | QUERY | 6.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
