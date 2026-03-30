---
title: "Documentation"
page_id: docs_page
source_json: docs_page.json
generator: json_to_markdown.py
---

# Documentation

## Overview

- **page_id:** docs_page
- **page_type:** docs
- **codebase:** root
- **surface:** Root Docs
- **era_tags:** 0.x, 8.x, 9.x, 11.x
- **flow_id:** docs
- **_id:** docs_page-001

## Metadata

- **route:** /docs
- **file_path:** contact360.io/root/app/(marketing)/docs/page.tsx
- **purpose:** Documentation list page displaying available documentation pages. Uses useDocumentation hook and DocumentationList component.
- **s3_key:** data/pages/docs_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **DocumentationPage** — `app/(marketing)/docs/page.tsx`
- **DocumentationList** — `components/documentation/DocumentationList.tsx`
- **LoadingSpinner** — `inline-tailwindcss` (animate-spin)
- **RetryButton** — `inline-tailwindcss` (bg-gray-900)
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Documentation

### description

Documentation list page displaying available documentation pages. Uses useDocumentation hook and DocumentationList component.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| docs-title | 1 | Documentation |
| docs-list | 2 | Available Guides |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| docs-getting-started | getting-started | Getting Started |
| docs-api-reference | api-reference | API Reference |
| docs-integrations | integrations | Integrations |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /docs/{pageId} | DocumentationList | view-doc | View Guide | ghost |
| filter documentation list | DocumentationList | search-docs | Search | icon |


### input_boxes

| component | id | label | placeholder | type |
| --- | --- | --- | --- | --- |
| DocumentationList | docs-search | Search documentation | Search guides... | search |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| DocumentationList | Everything you need to integrate and use Contact360. | docs-intro | body |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/documentation/DocumentationList.tsx | DocumentationList | Grid of documentation page cards with search and category tabs |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useDocumentation.ts | useDocumentation | Fetches and manages documentation page list | 0.x |
| gateway/docs services | documentation content endpoints | public documentation list rendering |


### services



### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| view-doc | View Guide | ghost | navigate to /docs/{pageId} | DocumentationList |
| search-docs | Search | icon | filter documentation list | DocumentationList |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| docs-search | Search documentation | search | Search guides... | DocumentationList |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useDocumentation | ListDocumentationPages (or equivalent) | documentationService | query |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway/docs services | documentation content endpoints | public documentation list rendering |


## Data Sources

- documentation GraphQL/services content
- fallback documentation list content


## Flow summary

root docs page -> useDocumentation -> docs service/content fetch -> list/filter UI -> per-doc route navigation


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:DocsList] > [H:Header] + [Q:ListContainer] -> {useDocumentation}

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/docs`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [landing_page.md](landing_page.md) navbar/footer, SEO.

**Typical outbound:** [api_docs_page.md](api_docs_page.md), [docs_pageid_page.md](docs_pageid_page.md).

**Cross-host:** Hand-off to `app` (authentication) and `email` (Mailhub) via shared marketing navigation.
**Backend:** Public documentation engine; uses `useDocumentation` hook for content resolution.



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
- [docs_pageid_page](docs_pageid_page.md)
- [email_finder_page](email_finder_page.md)
- [email_verifier_page](email_verifier_page.md)
- [integrations_page](integrations_page.md)
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
