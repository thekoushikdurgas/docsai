---
title: "Dynamic Dashboard Page"
page_id: dashboard_pageid_page
source_json: dashboard_pageid_page.json
generator: json_to_markdown.py
---

# Dynamic Dashboard Page

## Overview

- **page_id:** dashboard_pageid_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 9.x, 11.x
- **flow_id:** dashboardid
- **_id:** dashboard_pageid_page-001

## Metadata

- **route:** /dashboard/[pageId]
- **file_path:** contact360.io/app/app/(dashboard)/dashboard/[pageId]/page.tsx
- **purpose:** Dynamic Dashboard: Specialized view for targeted analytics or specific entity deep-dives.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None (access controlled by DashboardPageGuard based on pageId)
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
### uses_endpoints (1)

- `graphql/GetPage` — Get dashboard page content by pageId from pages API.

### UI components (metadata)

- **DynamicDashboardPage** — `app/(dashboard)/dashboard/[pageId]/page.tsx`
- **DynamicDashboard** — `components/dashboard/DynamicDashboard.tsx`
- **StatCard** — `components/shared/StatCard.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **Bot** — `lucide-react`
- **Lock** — `lucide-react`
- **ArrowRight** — `lucide-react`

- **versions:** []
- **endpoint_count:** 1
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Dynamic Dashboard Page

### description

Dynamic CMS-based dashboard pages. Renders content from API by pageId. Supports access control, sections, and nested components via DashboardPageGuard and DynamicPageRenderer.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| dynamic-page-title | 1 | {pageTitle} (from CMS) |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /dashboard | DashboardPageGuard | back-to-dashboard | Back to Dashboard | ghost |


### input_boxes



### text_blocks

| component | content | id | type | visibility |
| --- | --- | --- | --- | --- |
| DynamicPageRenderer | Dynamic content loaded from API by pageId. Rendered by DynamicPageRenderer. | cms-content | body |  |
| DashboardPageGuard | You don't have access to this page. | access-denied | error | unauthorized users |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| DashboardPageGuard | cms-page-load | CMS page load flow | ['URL: /dashboard/{pageId}', 'DashboardPageGuard checks access_control field', 'dashboardPagesService.GetPage(pageId)', 'DynamicPageRenderer renders sections', 'Unauthorized → access denied message'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/layouts/DashboardPageGuard.tsx | DashboardPageGuard | Fetches page by ID, checks access control, renders or redirects |
| components/features/dashboard/DynamicPageRenderer.tsx | DynamicPageRenderer | Renders CMS page sections and components from API response |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useDashboardPage.ts | useDashboardPage | Fetches dynamic report schema and data | 5.x |
| context/AuthContext.ts | useAuth | Validates Pro/Admin role for custom reports | 1.x |
| context/RoleContext.tsx | RoleContext | Role-based access gating per CMS page |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/dashboardPagesService.ts | dashboardPagesService | ['GetPage'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User identity for access control check |
| context/RoleContext.tsx | RoleContext | Role-based access gating per CMS page |


### utilities



### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useDashboardPage | QUERY | GetPage | dashboardPagesService |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| back-to-dashboard | Back to Dashboard | ghost | navigate to /dashboard | DashboardPageGuard |


### inputs

[]

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
| hooks/useDashboardPage.ts | useDashboardPage | Fetches page content by pageId via dashboardPagesService.GetPage |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/dashboardPagesService.ts | dashboardPagesService | ['GetPage'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/GetPage | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: dashboardPagesService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useDashboardPage -> dashboardPagesService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/dashboard/[pageId]`

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
| `GetPage` | [query_get_dashboard_page_graphql.md](../../backend/endpoints/query_get_dashboard_page_graphql.md) | QUERY | 9.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
