---
title: "Build your perfect lead list."
page_id: prospect_finder_page
source_json: prospect_finder_page.json
generator: json_to_markdown.py
---

# Build your perfect lead list.

## Overview

- **page_id:** prospect_finder_page
- **page_type:** product
- **codebase:** root
- **surface:** product
- **era_tags:** 3.x, 4.x, 9.x
- **flow_id:** prospect_finder
- **_id:** prospect_finder_page-001

## Metadata

- **route:** /products/prospect-finder
- **file_path:** contact360.io/root/app/(marketing)/products/prospect-finder/page.tsx
- **purpose:** Prospect Finder: Marketing landing page for wide-scale B2B contact search.
- **status:** shipped
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
### uses_endpoints (1)

- `graphql/GetMarketingPage` — Get marketing page content dynamically. Falls back to static content if API fails.

### UI components (metadata)

- **ProductPageLayout** — `contact360/marketing/src/components/landing/shared/ProductPageLayout.tsx`
- **MarketingPageContainer** — `contact360/marketing/src/components/marketing/MarketingPageContainer.tsx`
- **ProspectFinderAnimation** — `components/landing/animations/ProspectFinderAnimation.tsx`

- **versions:** []
- **endpoint_count:** 1
### api_versions

- graphql

- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Build your perfect lead list.

### subtitle

Prospect Finder

### description

Filter through 200 million verified B2B contacts by Industry, Location, and Job Title.

### hero

- **title:** Build your perfect lead list.
- **subtitle:** Prospect Finder
- **description:** Stop wasting time on LinkedIn. Use our advanced search engine to filter through 200 million verified B2B contacts. Filter by Industry, Location, and Job Title to find your perfect match.
- **features**
  - 50+ advanced search filters
  - Save searches and get alerted
  - Export clean, verified data directly
  - Filter by Tech Stack and Revenue

- **cta_text:** Build Your List


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| prospect-title | 1 | Build your perfect lead list. |
| how-it-works | 2 | How Prospect Finder works |
| features | 2 | Advanced Search Filters |


### subheadings

| id | level | text |
| --- | --- | --- |
| filter-capabilities | 3 | 50+ advanced search filters |


### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register (prospect intent) | ProductPageLayout | build-list-cta | Build Your List | primary |
| scroll to filter section | ProductPageLayout | see-filters | See All Filters | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ProductPageLayout | Filter through 200 million verified B2B contacts by Industry, Location, and Job Title. | hero-description | body |
| ProspectFinderAnimation | 50+ advanced search filters | feature-filters | feature |
| ProspectFinderAnimation | Save searches and get alerted on new matches | feature-alerts | feature |
| ProspectFinderAnimation | Export clean, verified data directly | feature-export | feature |
| ProspectFinderAnimation | Filter by Tech Stack and Revenue | feature-techstack | feature |


### checkboxes



### radio_buttons



### progress_bars



### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| animated_filter_demo | ProspectFinderAnimation | static demo data | prospect-animation | Prospect search animation |


### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/landing/shared/ProductPageLayout.tsx | ProductPageLayout | Product marketing page shell with hero, features, CTA |
| contact360.io/root/src/components/landing/animations/ProspectFinderAnimation.tsx | ProspectFinderAnimation | Interactive animation showing live filter and search |
| contact360.io/root/src/components/marketing/MarketingPageContainer.tsx | MarketingPageContainer | Shared marketing layout wrapper |


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
| build-list-cta | Build Your List | primary | navigate to /register (prospect intent) | ProductPageLayout |
| see-filters | See All Filters | ghost | scroll to filter section | ProductPageLayout |


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

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway/content | graphql/GetMarketingPage | public content rendering and CTA routing |


## Data Sources

- Marketing/docs content sources
- GraphQL read paths and fallback content where configured


## Flow summary

root page UI -> page hooks -> page services -> content/API reads -> rendered marketing/docs surface


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **3.x** — Contact & company data — VQL tables, export modals, files, prospect finder narrative.
- **4.x** — Extension & Sales Navigator — LinkedIn dashboard page, Chrome extension marketing, SN workflows.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:MarketingPage] > [H:HeroSection] + [S:FeatureSection] + [Q:WorkflowSection] + [C:CtaSection]

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/products/prospect-finder`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [landing_page.md](landing_page.md) navbar/footer, SEO.

**Typical outbound:** [api_docs_page.md](api_docs_page.md), sign in / register.

**Cross-host:** Hand-off to `app` (authentication) and `email` (Mailhub) via shared marketing navigation.
**Backend:** Public product surface; uses `GetMarketingPage` for dynamic content.



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
- [integrations_page](integrations_page.md)
- [landing_page](landing_page.md)
- [privacy_page](privacy_page.md)
- [refund_page](refund_page.md)
- [terms_page](terms_page.md)
- [ui_page](ui_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetMarketingPage` | [query_get_marketing_page_graphql.md](../../backend/endpoints/query_get_marketing_page_graphql.md) | QUERY | 9.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
