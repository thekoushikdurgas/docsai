---
title: "Campaign templates"
page_id: campaign_templates_page
source_json: campaign_templates_page.json
generator: json_to_markdown.py
---

# Campaign templates

## Overview

- **page_id:** campaign_templates_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 10.x, 11.x
- **flow_id:** campaign_templates
- **_id:** campaign_templates_page-001

## Metadata

- **route:** /campaigns/templates
- **file_path:** contact360.io/app/app/(dashboard)/campaigns/templates/page.tsx
- **purpose:** Template Library: Gallery of reusable campaign layouts with categorisation and search.
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

Campaign templates

### description

Planned: reusable template editor with merge fields and preview.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| tpl-title | 1 | Templates |
| editor | 2 | Template editor |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| templates-library | library | Library |
| templates-editor | editor | Editor |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /campaigns/templates/new | CampaignTemplatesPage | new-template | New template | primary |
| templateService.SaveTemplate | TemplateEditor | save-template | Save | primary |
| toggle preview pane with sample data | TemplateEditor | preview | Preview | secondary |
| insert {{firstName}} etc. at cursor | TemplateEditor | insert-variable | Insert variable | ghost |
| templateService.DuplicateTemplate | TemplateCard | duplicate-template | Duplicate | ghost |


### input_boxes

| component | id | label | placeholder | required | type |
| --- | --- | --- | --- | --- | --- |
| TemplateEditor | subject | Subject line | Hi {{firstName}}, ... |  | text |
| TemplateEditor | body-html | Body | Rich text / HTML |  | textarea |
| TemplateEditor | template-name | Template name |  | True | text |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| TemplateEditor | Use {{firstName}}, {{company}}, {{unsubscribeUrl}} for merge fields. | variable-hint | hint |


### checkboxes

| component | default | id | label |
| --- | --- | --- | --- |
| TemplateEditor | True | track-opens | Track opens |
| TemplateEditor | True | track-clicks | Track clicks |


### radio_buttons

| component | id | label | options |
| --- | --- | --- | --- |
| TemplateEditor | editor-mode | Editor mode | ['Rich text', 'HTML'] |


### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| CampaignWizard | template-to-campaign | Template used in campaign | ['Create or pick template', 'campaignService.CreateCampaign references templateId', 'Send uses rendered HTML with merge data per recipient'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/campaigns/CampaignTemplatesPage.tsx | CampaignTemplatesPage | Planned: template grid + search |
| components/features/campaigns/TemplateEditor.tsx | TemplateEditor | Planned: subject + body + variables + preview |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaignTemplates.ts | useCampaignTemplates | Planned: list/save templates |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/templateService.ts | templateService | ['ListTemplates', 'SaveTemplate', 'DuplicateTemplate', 'RenderPreview'] |


### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| new-template | New template | primary | navigate to /campaigns/templates/new | CampaignTemplatesPage |
| save-template | Save | primary | templateService.SaveTemplate | TemplateEditor |
| preview | Preview | secondary | toggle preview pane with sample data | TemplateEditor |
| insert-variable | Insert variable | ghost | insert {{firstName}} etc. at cursor | TemplateEditor |
| duplicate-template | Duplicate | ghost | templateService.DuplicateTemplate | TemplateCard |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| subject | Subject line | text | Hi {{firstName}}, ... | TemplateEditor |
| body-html | Body | textarea | Rich text / HTML | TemplateEditor |
| template-name | Template name | text |  | TemplateEditor |


### checkboxes

| id | label | default | component |
| --- | --- | --- | --- |
| track-opens | Track opens | True | TemplateEditor |
| track-clicks | Track clicks | True | TemplateEditor |


### radio_buttons

| id | label | options | component |
| --- | --- | --- | --- |
| editor-mode | Editor mode | ['Rich text', 'HTML'] | TemplateEditor |


### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useCampaignTemplates.ts | useCampaignTemplates | Planned: list/save templates |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/templateService.ts | templateService | ['ListTemplates', 'SaveTemplate', 'DuplicateTemplate', 'RenderPreview'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: templateService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useCampaignTemplates -> templateService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **10.x** — Email campaign — campaigns, sequences, templates, builder (planned routes).
- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > [K:Library] + [E:Editor] — {GQL ListTemplates, SaveTemplate, RenderPreview}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/campaigns/templates`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [campaign_builder_page.md](campaign_builder_page.md) (Step 3: Template).

**Typical outbound:** Sidebar peers; [campaign_builder_page.md](campaign_builder_page.md) (Use in campaign).

**Cross-host:** Templates are synchronized with **email** (Mailhub) for server-side rendering during campaign execution.
**Backend:** Appointment360 GraphQL gateway; template versioning and liquid tag parsing services.

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
