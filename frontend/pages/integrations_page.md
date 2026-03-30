---
title: "Integrations"
page_id: integrations_page
source_json: integrations_page.json
generator: json_to_markdown.py
---

# Integrations

## Overview

- **page_id:** integrations_page
- **page_type:** marketing
- **codebase:** root
- **surface:** marketing
- **era_tags:** 9.x
- **flow_id:** integrations
- **_id:** integrations_page-001

### UI components (metadata)

- **IntegrationsPage** — `app/(marketing)/integrations/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **IntegrationsPageRenderer** — `components/pages/MarketingPages.tsx` (IntegrationsPage)
- **Card3D** — `components/ui/Card3D.tsx`

## Metadata

- **route:** /integrations
- **file_path:** contact360.io/root/app/(marketing)/integrations/page.tsx
- **purpose:** Integrations page displaying partner integrations and API connections. Connect Contact360 with your favorite tools.
- **s3_key:** data/pages/integrations_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-02-03T00:00:00.000000+00:00
- **uses_endpoints:** []

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Integrations

### subtitle

Connect Contact360 with your favorite tools.

### description

Connect Contact360 with your favorite tools.

### hero

- **title:** Integrations
- **description:** Connect Contact360 with your favorite tools.
- **features**
  - Salesforce
  - HubSpot
  - Pipedrive
  - Zapier
  - Slack
  - Gmail
  - Outlook
  - Outreach

- **cta_text:** View Integrations


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| integrations-title | 1 | Integrations |
| crm | 2 | CRM Integrations |
| automation | 2 | Automation & Workflow |
| email-tools | 2 | Email & Communication |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| integrations-all | all | All |
| integrations-crm | crm | CRM |
| integrations-automation | automation | Automation |
| integrations-email | email | Email |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| open integration OAuth/setup flow | IntegrationCard | connect-integration | Connect | primary |
| show all integration cards | IntegrationsPage | view-integrations-cta | View All Integrations | primary |


### input_boxes

| component | id | label | placeholder | type |
| --- | --- | --- | --- | --- |
| IntegrationsPage | search-integrations | Search integrations | Search by name (Salesforce, HubSpot...) | search |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| IntegrationsPage | Connect Contact360 with your favorite tools. Push verified contacts directly to your CRM. | integrations-intro | body |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| IntegrationCard | crm-connect-flow | Connect CRM integration | ['Select integration (Salesforce, HubSpot, etc.)', "Click 'Connect' → OAuth redirect", 'Authorize Contact360 in CRM', 'Callback → integration active', 'Push contacts/companies directly from Contact360 |


### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/pages/MarketingPages.tsx | IntegrationsPage | Integration catalog with search and category tabs |
| contact360.io/root/src/components/pages/MarketingPages.tsx | IntegrationCard | Individual integration card (logo, name, description, connect button) |


### hooks



### services



### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| connect-integration | Connect | primary | open integration OAuth/setup flow | IntegrationCard |
| view-integrations-cta | View All Integrations | primary | show all integration cards | IntegrationsPage |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| search-integrations | Search integrations | search | Search by name (Salesforce, HubSpot...) | IntegrationsPage |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway/content | marketing/docs content operations (page-specific) | public content rendering and CTA routing |


## Data Sources

- Marketing/docs content sources
- GraphQL read paths and fallback content where configured


## Flow summary

root page UI -> page hooks -> page services -> content/API reads -> rendered marketing/docs surface


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [C] > [H:Partners] + [T:Categories] + [V:Cards] + [C:Footer]

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/integrations`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [landing_page.md](landing_page.md) navbar/footer, SEO.

**Typical outbound:** [api_docs_page.md](api_docs_page.md), sign in / register.

**Cross-host:** Hand-off to `app` (authentication) for OAuth flow initiation.
**Backend:** Public marketing surface; no first-party GraphQL host in `root`.



## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [about_page](about_page.md)
- [ai_email_writer_page](ai_email_writer_page.md)
- [api_docs_page](api_docs_page.md)
- [careers_page](careers_page.md)
- [cfo_email_list_page](cfo_email_list_page.md)
- [chrome_extension_page](chrome_extension_page.md)
- [docs_page](docs_page.md)
- [docs_pageid_page](docs_pageid_page.md)
- [email_finder_page](email_finder_page.md)
- [email_verifier_page](email_verifier_page.md)
- [landing_page](landing_page.md)
- [privacy_page](privacy_page.md)
- [prospect_finder_page](prospect_finder_page.md)
- [refund_page](refund_page.md)
- [terms_page](terms_page.md)
- [ui_page](ui_page.md)

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
