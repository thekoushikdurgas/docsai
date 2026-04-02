---
title: "Campaigns"
page_id: campaigns_page
source_json: campaigns_page.json
generator: json_to_markdown.py
---

# Campaigns

## Overview

- **page_id:** campaigns_page
- **page_type:** dashboard (planned)
- **codebase:** app
- **surface:** app
- **era_tags:** 10.x
- **flow_id:** campaigns
- **_id:** campaigns_page-001

## Metadata

- **route:** /campaigns
- **file_path:** contact360.io/app/app/(dashboard)/campaigns/page.tsx
- **purpose:** Campaign Management: Overview of all active, scheduled, and draft marketing activities.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Plan gated; Pro+ or campaign entitlement required.
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
- **uses_endpoints:** []
- **ui_components:** []
- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Campaigns

### description

Planned: campaign list and management for outbound email campaigns.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| campaigns-title | 1 | Email Campaigns |
| list | 2 | Your campaigns |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| campaigns-all | all | All |
| campaigns-draft | draft | Drafts |
| campaigns-scheduled | scheduled | Scheduled |
| campaigns-sent | sent | Sent |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /campaigns/new | CampaignsPage | new-campaign | New campaign | primary |
| campaignService.DuplicateCampaign | CampaignRow | duplicate-campaign | Duplicate | ghost |
| campaignService.PauseCampaign | CampaignRow | pause-campaign | Pause | secondary |
| navigate to /campaigns/{id}/stats | CampaignRow | view-stats | View stats | ghost |


### input_boxes

| component | id | label | placeholder | type |
| --- | --- | --- | --- | --- |
| CampaignsPage | search-campaigns | Search | Search campaigns... | search |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| CampaignsPage | No campaigns yet. Create your first campaign to reach your contacts. | empty-campaigns | empty-state |
| CampaignRow | Delivery: {delivered}/{sent} ({pct}%) | delivery-rate | stat |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| CampaignRow | send-progress | Send progress | Rows sent / total for in-flight sends | determinate |


### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/campaigns/CampaignsPage.tsx | CampaignsPage | Planned: filterable campaign table + new CTA |
| components/features/campaigns/CampaignRow.tsx | CampaignRow | Planned: status badge, progress, actions |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaigns.ts | useCampaigns | Planned: list campaigns with filters |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/campaignService.ts | campaignService | ['ListCampaigns', 'GetCampaign', 'PauseCampaign', 'DuplicateCampaign'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User-scoped campaigns |


### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| new-campaign | New campaign | primary | navigate to /campaigns/new | CampaignsPage |
| duplicate-campaign | Duplicate | ghost | campaignService.DuplicateCampaign | CampaignRow |
| pause-campaign | Pause | secondary | campaignService.PauseCampaign | CampaignRow |
| view-stats | View stats | ghost | navigate to /campaigns/{id}/stats | CampaignRow |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| search-campaigns | Search | search | Search campaigns... | CampaignsPage |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| send-progress | Send progress | Rows sent / total for in-flight sends | determinate | CampaignRow |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaigns.ts | useCampaigns | Planned: list campaigns with filters |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/campaignService.ts | campaignService | ['ListCampaigns', 'GetCampaign', 'PauseCampaign', 'DuplicateCampaign'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: campaignService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useCampaigns -> campaignService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **10.x** — Email campaign — campaigns, sequences, templates, builder (planned routes).
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

**Route (registry):** `/campaigns`

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
| — | *No `graphql/...` references in this page spec* | — | — |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
