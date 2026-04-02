---
title: "System Status"
page_id: status_page
source_json: status_page.json
generator: json_to_markdown.py
---

# System Status

## Overview

- **page_id:** status_page
- **page_type:** marketing (planned)
- **codebase:** root (marketing shell)
- **surface:** public
- **era_tags:** 6.x, 9.x
- **flow_id:** status
- **_id:** status_page-001

## Metadata

- **route:** /status
- **file_path:** contact360.io/root/app/(marketing)/status/page.tsx
- **purpose:** Public system status page for Contact360. Planned: incident history, component health (API, GraphQL, email pipeline), uptime percentages, and subscribe-to-updates. Cross-cutting reliability patterns (skeletons, error boundaries, offline banner) apply to all dashboard surfaces.
- **s3_key:** data/pages/status_page.json
- **status:** planned
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** planned
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

System Status

### description

Planned public status page: component health, incidents, maintenance windows.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| status-title | 1 | Contact360 System Status |
| components | 2 | Component health |
| incidents | 2 | Recent incidents |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| status-all | all | All systems |
| status-api | api | API |
| status-email | email | Email pipeline |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| email subscribe or RSS | StatusPage | subscribe-updates | Subscribe to updates | secondary |
| refetch health status | StatusPage | refresh-status | Refresh | icon |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| StatusPage | All systems operational \| Degraded \| Partial outage | overall-status | stat |
| StatusPage | Uptime calculated over trailing 90 days | uptime-note | caption |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| StatusPage | uptime-bar | Component uptime % | Per-component uptime visualization | determinate |


### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| timeline | StatusPage | statusService or static CMS | incident-timeline | Incident timeline |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| AppRoot | app-health-check | Client health check (cross-cutting 6.x) | ['healthService on app mount', 'If degraded → inline Alert or banner', 'Retry button on failed data fetches', 'Skeleton loaders replace spinners on list pages'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/status/StatusPage.tsx | StatusPage | Planned: status overview, component rows, incident list |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useSystemStatus.ts | useSystemStatus | Planned: poll health endpoints |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/healthService.ts | healthService | ['GetHealth', 'ListIncidents'] |


### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| subscribe-updates | Subscribe to updates | secondary | email subscribe or RSS | StatusPage |
| refresh-status | Refresh | icon | refetch health status | StatusPage |


### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| uptime-bar | Component uptime % | Per-component uptime visualization | determinate | StatusPage |


### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useStatusPage (planned) | GetSystemHealth, ListIncidents | statusService (planned) | query |


## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useSystemStatus.ts | useSystemStatus | Planned: poll health endpoints |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/healthService.ts | healthService | ['GetHealth', 'ListIncidents'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| health/observability | status and incident endpoints (planned) | public reliability visibility |


## Data Sources

- health/status backend services (planned)
- incident telemetry and logs integrations (planned)


## Flow summary

public status page -> planned status hooks/services -> health/incident data -> tabs/progress/timeline UI


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **6.x** — Reliability & scaling — analytics, activities, jobs, status, error/retry/skeleton patterns.
- **7.x** — Deployment — governance, deployments surface, RBAC-sensitive admin views.
- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/status`

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
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| — | *No `graphql/...` references in this page spec* | — | — |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
