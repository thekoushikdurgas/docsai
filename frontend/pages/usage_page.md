---
title: "Usage"
page_id: usage_page
source_json: usage_page.json
generator: json_to_markdown.py
---

# Usage

## Overview

- **page_id:** usage_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 1.x, 6.x, 11.x
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **flow_id:** usage
- **_id:** usage_page-001

## Metadata

- **route:** /usage
- `graphql/GetUsage` — Get credit balance and feature limits. Returns used, limit, remaining. Via useUsage hook.
- `graphql/GetFeatureUsage` — Get granular breakdown for a selected feature. Via useFeatureOverview hook.
- `graphql/ListActivities` — Get audit trail of platform actions (exports, verifies, etc). Via useActivities hook.

### UI components (metadata)

- **UsagePage** — `app/(dashboard)/usage/page.tsx`
- **UsageSummaryCards** — `components/usage/UsageSummaryCards.tsx`
- **UsageViewSwitch** — `components/usage/UsageViewSwitch.tsx`
- **UsageFeatureCards** — `components/usage/UsageFeatureCards.tsx`
- **UsageFeatureTable** — `components/usage/UsageFeatureTable.tsx`
- **UsageBanner** — `components/usage/UsageBanner.tsx`
- **FeatureSelect** — `components/usage/FeatureSelect.tsx`
- **FeatureOverviewPanel** — `components/usage/FeatureOverviewPanel.tsx`
- **Tabs** — `components/ui/tabs/Tabs.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **EmptyState** — `components/shared/EmptyState.tsx`
- **BarChart3** — `lucide-react` (icon)

- **versions:** []
- **endpoint_count:** 12
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Usage

### description

Usage and limits page displaying feature usage statistics and remaining limits across all features in cards or table view.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| usage-title | 1 | Usage & Limits |
| overview | 2 | Credit Overview |
| feature-breakdown | 2 | Feature Breakdown |


### subheadings

| id | level | text |
| --- | --- | --- |
| resets-at | 3 | Resets on {resetDate} |


### tabs

| content_ref | id | label | era |
| --- | --- | --- | --- |
| usage-overview | overview | Overview | 1.x |
| usage-by-feature | by-feature | By Feature | 1.x |
| usage-activity | activity | Activity | 3.x |


### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| setViewMode | UsageViewSwitch | view-mode-btn | Cards / Table | toggle | 0.x |
| setActiveTab | Tabs | nav-tab | [Tab Name] | ghost | 0.x |
| setSelectedFeature | FeatureSelect | feature-sel | [Feature] | select | 1.x |
| refetch | UsagePage | refresh-btn | Refresh | icon | 0.x |
| router.push('/billing') | UsageBanner | upgrade-btn | Upgrade Plan | primary | 1.x |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| UsageOverview | {remaining} / {limit} credits remaining | credit-balance-text | stat |
| UsageOverview | Credits reset on {resetDate} | reset-notice | caption |
| UsageLimitsTable | You've reached your {feature} limit. Upgrade or purchase add-ons. | limit-reached | warning |


### checkboxes



### radio_buttons



### progress_bars

| color_logic | component | id | label | purpose | type |
| --- | --- | --- | --- | --- | --- |
| green > 50% remaining, amber 20-50%, red < 20% | UsageOverview | total-credits-bar | Total credits used | Overall credit consumption vs plan limit | determinate |
|  | FeatureOverviewPanel | email-finder-bar | Email Finder usage | Finder credits used / limit | determinate |
|  | FeatureOverviewPanel | email-verifier-bar | Email Verifier usage | Verifier credits used / limit | determinate |
|  | FeatureOverviewPanel | ai-chat-bar | AI Chat usage | AI message credits used / limit | determinate |
|  | FeatureOverviewPanel | contact-export-bar | Contact Export usage | Export credits used / limit | determinate |


### graphs

- **[0]**
  - **id:** feature-usage-bar-chart
  - **label:** Feature usage breakdown
  - **chart_type:** bar
  - **orientation:** vertical
  - **data_source:** usageService.GetFeatureUsage
  - **x_axis:** Feature name
  - **y_axis:** Credits used
  - **component:** FeatureOverviewPanel

- **[1]**
  - **id:** usage-overview-cards
  - **label:** Usage Overview Cards
  - **chart_type:** stat_cards
  - **data_source:** usageService.GetUsage
  - **component:** UsageSummaryCards
  - **view:** overview tab



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| UsagePage | usage-page-flow | Usage page load and display | ['useUsagePage fetches GetUsage for all features', 'UsageOverview renders credit balance + total progress bar', 'FeatureOverviewPanel renders per-feature progress bars', 'View toggle: Cards (Card3D) v |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/usage/UsageOverview.tsx | UsageOverview | Credit balance, total bar, reset date, upgrade CTA |
| components/usage/FeatureOverviewPanel.tsx | FeatureOverviewPanel | Per-feature usage bars (finder, verifier, AI, exports) |
| components/features/usage/UsageLimitsTable.tsx | UsageLimitsTable | Tabular view of all features with used/limit/remaining |
| components/ui/Card3D.tsx | Card3D | 3D usage card per feature (cards view) |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useUsage.ts | useUsage | Aggregate credit and feature limit tracking | 1.x |
| hooks/useFeatureOverview.ts | useFeatureOverview | Detailed metrics for a single selected capability | 1.x |
| hooks/useActivities.ts | useActivities | Retrieval of granular consumption logs | 0.x |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/usageService.ts | usageService | ['GetUsage', 'GetFeatureUsage'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | Plan tier determines limits per feature |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/usageFormatters.ts | usageFormatters | formatCredits(), formatPercent(), creditBalanceColor() |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useUsagePage | QUERY | GetUsage | usageService |
| useFeatureOverview | QUERY | GetFeatureUsage | usageService |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| upgrade-plan | Upgrade Plan | primary | navigate to /billing | UsageOverview |
| buy-credits | Buy More Credits | secondary | navigate to /billing#addons | UsageOverview |
| refresh-usage | Refresh | icon | refetch usage data | PageHeader |


### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | color_logic | component |
| --- | --- | --- | --- | --- | --- |
| total-credits-bar | Total credits used | Overall credit consumption vs plan limit | determinate | green > 50% remaining, amber 20-50%, red < 20% | UsageOverview |
| email-finder-bar | Email Finder usage | Finder credits used / limit | determinate |  | FeatureOverviewPanel |
| email-verifier-bar | Email Verifier usage | Verifier credits used / limit | determinate |  | FeatureOverviewPanel |
| ai-chat-bar | AI Chat usage | AI message credits used / limit | determinate |  | FeatureOverviewPanel |
| contact-export-bar | Contact Export usage | Export credits used / limit | determinate |  | FeatureOverviewPanel |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useUsage.ts | useUsagePage | Fetch and manage usage data |
| hooks/useFeatureOverview.ts | useFeatureOverview | Feature-level usage summary |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/usageService.ts | usageService | ['GetUsage', 'GetFeatureUsage'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/GetUsage | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: usageService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useUsagePage, useFeatureOverview -> usageService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/usage`

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
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetUsage` | [query_get_usage_graphql.md](../../backend/endpoints/query_get_usage_graphql.md) | QUERY | 1.x |
| `GetFeatureUsage` | *unresolved — add to endpoint index* | — | — |
| `ListActivities` | *unresolved — add to endpoint index* | — | — |

**Unresolved operations** (not found in `index.md` / `endpoints_index.md`): 
`graphql/GetFeatureUsage`, `graphql/ListActivities`

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
