---
title: "New campaign"
page_id: campaign_builder_page
source_json: campaign_builder_page.json
generator: json_to_markdown.py
---

# New campaign

## Overview

- **page_id:** campaign_builder_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 10.x, 11.x
- **flow_id:** campaign_builder
- **_id:** campaign_builder_page-001

## Metadata

- **route:** /campaigns/new
- **file_path:** contact360.io/app/app/(dashboard)/campaigns/new/page.tsx
- **purpose:** Marketing Studio: Visual layout engine for constructing email and multichannel campaigns.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Plan gated; Pro+ or campaign entitlement required.
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
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

New campaign

### description

Planned: step wizard for creating a campaign.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| wizard-title | 1 | Create campaign |


### subheadings



### tabs



### buttons

| action | component | id | label | step | type |
| --- | --- | --- | --- | --- | --- |
| wizard previous step | CampaignWizard | back-step | Back |  | ghost |
| wizard next step | CampaignWizard | next-step | Next |  | primary |
| campaignService.ScheduleCampaign(sendAt=now) | CampaignWizard | send-now | Send now | review | primary |
| open datetime picker then schedule | CampaignWizard | schedule-send | Schedule | review | primary |


### input_boxes

| id | label | required | step | type |
| --- | --- | --- | --- | --- |
| campaign-name | Campaign name | True | details | text |
| from-name | From name |  | details | text |
| reply-to | Reply-to email |  | details | email |
| schedule-datetime | Send at |  | review | datetime-local |


### text_blocks

| content | id | step | type |
| --- | --- | --- | --- |
| {n} recipients selected | audience-count | audience | stat |
| Summary card before send | review-summary | review | summary |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| CampaignWizard | wizard-progress | Wizard progress | Step 1 of 4 style determinate bar | determinate |


### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| CampaignWizard | campaign-wizard-flow | New campaign wizard | ['Step 1 Details: name, from, reply-to', 'Step 2 Audience: segment or saved search, count preview', 'Step 3 Template: pick or create', 'Step 4 Review: schedule or send now, confirm modal', 'campaignSe |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/campaigns/CampaignWizard.tsx | CampaignWizard | Planned: step container + progress indicator |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaignWizard.ts | useCampaignWizard | Planned: step state + validation |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/campaignService.ts | campaignService | ['CreateCampaign', 'ScheduleCampaign'] |


### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| back-step | Back | ghost | wizard previous step | CampaignWizard |
| next-step | Next | primary | wizard next step | CampaignWizard |
| send-now | Send now | primary | campaignService.ScheduleCampaign(sendAt=now) | CampaignWizard |
| schedule-send | Schedule | primary | open datetime picker then schedule | CampaignWizard |


### inputs

| id | label | type | required | step |
| --- | --- | --- | --- | --- |
| campaign-name | Campaign name | text | True | details |
| from-name | From name | text |  | details |
| reply-to | Reply-to email | email |  | details |
| schedule-datetime | Send at | datetime-local |  | review |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| wizard-progress | Wizard progress | Step 1 of 4 style determinate bar | determinate | CampaignWizard |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaignWizard.ts | useCampaignWizard | Planned: step state + validation |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/campaignService.ts | campaignService | ['CreateCampaign', 'ScheduleCampaign'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: campaignService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useCampaignWizard -> campaignService -> GraphQL gateway -> backend modules -> rendered states


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

**Route (registry):** `/campaigns/new`

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
| — | *No `graphql/...` references in this page spec* | — | — |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
