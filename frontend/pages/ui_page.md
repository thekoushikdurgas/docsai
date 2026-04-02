---
title: "UI Showcase"
page_id: ui_page
source_json: ui_page.json
generator: json_to_markdown.py
---

# UI Showcase

## Overview

- **page_id:** ui_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Marketing
- **era_tags:** 0.x, 9.x, 11.x
- **flow_id:** ui
- **_id:** ui_page-001

## Metadata

- **route:** /ui
- **file_path:** contact360.io/root/app/(marketing)/ui/page.tsx
- **purpose:** UI component showcase displaying component library, interactive demos, and code examples for all reusable components (Foundation, Layout, Composite, Advanced phases).
- **s3_key:** data/pages/ui_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **ShowcaseLayout** — `contact360/marketing/src/components/showcase/ShowcaseLayout.tsx`
- **FoundationDemos** — `contact360/marketing/src/components/showcase/demos/FoundationDemos.tsx`
- **LayoutDemos** — `contact360/marketing/src/components/showcase/demos/LayoutDemos.tsx`
- **CompositeDemos** — `contact360/marketing/src/components/showcase/demos/CompositeDemos.tsx`
- **AdvancedDemos** — `contact360/marketing/src/components/showcase/demos/AdvancedDemos.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

UI Showcase

### description

UI component showcase displaying component library, interactive demos, and code examples for all reusable components (Foundation, Layout, Composite, Advanced phases).


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| showcase-title | 1 | UI Component Showcase |
| foundation | 2 | Foundation Components |
| layout | 2 | Layout Components |
| composite | 2 | Composite Components |
| advanced | 2 | Advanced Components |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| showcase-foundation | foundation | Foundation |
| showcase-layout | layout | Layout |
| showcase-composite | composite | Composite |
| showcase-advanced | advanced | Advanced |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| demo interaction | FoundationDemos | demo-primary | Primary Button | primary |
| demo interaction | FoundationDemos | demo-secondary | Secondary Button | secondary |
| demo interaction | FoundationDemos | demo-danger | Danger Button | danger |
| demo interaction | FoundationDemos | demo-ghost | Ghost Button | ghost |
| clipboard.copyToClipboard(code) | ShowcaseLayout | copy-code | Copy Code | icon |


### input_boxes

| component | id | label | placeholder | rows | type |
| --- | --- | --- | --- | --- | --- |
| FoundationDemos | demo-text | Text Input demo | Type something... |  | text |
| FoundationDemos | demo-search | Search Input demo | Search... |  | search |
| FoundationDemos | demo-email | Email Input demo | email@example.com |  | email |
| FoundationDemos | demo-textarea | Textarea demo |  | 3 | textarea |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ShowcaseLayout | Interactive showcase of all reusable UI components. Phase 1: Foundation. Phase 2: Layout. Phase 3: Composite. Phase 4: Advanced. | showcase-description | body |


### checkboxes

| component | id | label | purpose |
| --- | --- | --- | --- |
| FoundationDemos | demo-checkbox | Demo checkbox | Interactive checkbox demo |


### radio_buttons

| component | id | label | options | purpose |
| --- | --- | --- | --- | --- |
| FoundationDemos | demo-radio | Demo radio group | ['Option A', 'Option B', 'Option C'] | Interactive radio button demo |


### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| FoundationDemos | demo-progress-determinate | Determinate progress bar demo | Shows configurable fill levels | determinate |
| FoundationDemos | demo-progress-indeterminate | Indeterminate progress bar demo | Shows animated loading bar | indeterminate |
| AdvancedDemos | demo-progress-stacked | Stacked progress bar demo | Multi-segment stacked bar | stacked |


### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| line | AdvancedDemos | static demo data | demo-line-chart | Line chart demo |
| bar | AdvancedDemos | static demo data | demo-bar-chart | Bar chart demo |
| stat_cards | CompositeDemos | static demo data | demo-stat-cards | Stat card grid demo |


### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/showcase/ShowcaseLayout.tsx | ShowcaseLayout | 4-tab showcase shell with sidebar navigation and code copy |
| contact360.io/root/src/components/showcase/demos/FoundationDemos.tsx | FoundationDemos | Button/input/checkbox/radio/badge/typography demos |
| contact360.io/root/src/components/showcase/demos/LayoutDemos.tsx | LayoutDemos | Grid/flex/card/modal layout demos |
| contact360.io/root/src/components/showcase/demos/CompositeDemos.tsx | CompositeDemos | DataTable/form/stat card composite component demos |
| contact360.io/root/src/components/showcase/demos/AdvancedDemos.tsx | AdvancedDemos | Chart/graph/progress/animation advanced component demos |


### hooks



### services



### contexts



### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy code snippets from showcase |


### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| demo-primary | Primary Button | primary | demo interaction | FoundationDemos |
| demo-secondary | Secondary Button | secondary | demo interaction | FoundationDemos |
| demo-danger | Danger Button | danger | demo interaction | FoundationDemos |
| demo-ghost | Ghost Button | ghost | demo interaction | FoundationDemos |
| copy-code | Copy Code | icon | clipboard.copyToClipboard(code) | ShowcaseLayout |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| demo-text | Text Input demo | text | Type something... | FoundationDemos |
| demo-search | Search Input demo | search | Search... | FoundationDemos |
| demo-email | Email Input demo | email | email@example.com | FoundationDemos |
| demo-textarea | Textarea demo | textarea |  | FoundationDemos |


### checkboxes

| id | label | purpose | component |
| --- | --- | --- | --- |
| demo-checkbox | Demo checkbox | Interactive checkbox demo | FoundationDemos |


### radio_buttons

| id | label | options | purpose | component |
| --- | --- | --- | --- | --- |
| demo-radio | Demo radio group | ['Option A', 'Option B', 'Option C'] | Interactive radio button demo | FoundationDemos |


### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| demo-progress-determinate | Determinate progress bar demo | Shows configurable fill levels | determinate | FoundationDemos |
| demo-progress-indeterminate | Indeterminate progress bar demo | Shows animated loading bar | indeterminate | FoundationDemos |
| demo-progress-stacked | Stacked progress bar demo | Multi-segment stacked bar | stacked | AdvancedDemos |


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

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [P] public layout > [H] hero/title > [C] sections — `(btn)` CTAs, optional `(in)` newsletter; light `{REST}` or static content.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/ui`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [landing_page.md](landing_page.md) nav/footer, SEO, `/docs` tree.

**Typical outbound:** Sign in / Get started → **app** [login_page.md](login_page.md) / [register_page.md](register_page.md); product CTAs → same.

**Cross-host:** No shared session with Mailhub unless integrated; dashboard uses separate GraphQL auth.
**Backend:** Public/marketing shell — no first-party GraphQL host here; `AUTO:endpoint-links` tables apply only where this spec references `graphql/...` for cross-docs.



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
- [prospect_finder_page](prospect_finder_page.md)
- [refund_page](refund_page.md)
- [terms_page](terms_page.md)

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
