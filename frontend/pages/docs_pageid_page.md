---
title: "Documentation Page"
page_id: docs_pageid_page
source_json: docs_pageid_page.json
generator: json_to_markdown.py
---

# Documentation Page

## Overview

- **page_id:** docs_pageid_page
- **page_type:** docs
- **codebase:** root
- **surface:** Root Docs
- **era_tags:** 0.x, 8.x, 9.x, 11.x
- **flow_id:** docsid
- **_id:** docs_pageid_page-001

## Metadata

- **route:** /docs/[pageId]
- **file_path:** contact360.io/root/app/(marketing)/docs/[pageId]/page.tsx
- **purpose:** Individual documentation page displaying markdown content with DocumentationViewer. Uses useDocumentationPage hook to load content.
- **s3_key:** data/pages/docs_pageid_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **DocumentationDetailPage** — `app/(marketing)/docs/[pageId]/page.tsx`
- **DocumentationViewer** — `components/documentation/DocumentationViewer.tsx`
- **LoadingSpinner** — `inline-tailwindcss` (animate-spin)
- **ErrorBlock** — `inline-tailwindcss` (text-2xl font-bold)
- **RetryButton** — `inline-tailwindcss` (bg-gray-900)
- **BreadcrumbLink** — `next/link`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Documentation Page

### description

Individual documentation page displaying markdown content with DocumentationViewer. Uses useDocumentationPage hook to load content.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| doc-title | 1 | {documentTitle} (from CMS) |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /docs | DocumentationViewer | back-to-docs | Back to Docs | ghost |
| clipboard.copyToClipboard(codeBlock) | DocumentationViewer | copy-code | Copy | icon |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| DocumentationViewer | Rendered markdown documentation loaded by useDocumentationPage | markdown-content | markdown |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/documentation/DocumentationViewer.tsx | DocumentationViewer | Renders markdown documentation with syntax highlighting, TOC, and code copy |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useDocumentation.ts | useDocumentationPage | Manages metadata and content loading for specific doc | 0.x |
| gateway/content | marketing/docs content operations (page-specific) | public content rendering and CTA routing |


### services



### contexts



### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy code blocks |


### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| back-to-docs | Back to Docs | ghost | navigate to /docs | DocumentationViewer |
| copy-code | Copy | icon | clipboard.copyToClipboard(codeBlock) | DocumentationViewer |


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

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useDocumentation.ts | useDocumentationPage | Manages metadata and content loading for specific doc | 0.x |
| gateway/content | marketing/docs content operations (page-specific) | public content rendering and CTA routing |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway/content | marketing/docs content operations (page-specific) | public content rendering and CTA routing |


## Data Sources

- Marketing/docs content sources
- GraphQL read paths and fallback content where configured


## Flow summary

root page UI -> useDocumentationPage -> page services -> content/API reads -> rendered marketing/docs surface


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:DocDetail] > [Q:ContentPane] -> {useDocumentationPage}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/docs/[pageId]`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [docs_page.md](docs_page.md) list, SEO.

**Typical outbound:** Cross-links to other docs, [api_docs_page.md](api_docs_page.md).

**Cross-host:** Hand-off to `app` (authentication) for private docs access if required.
**Backend:** Public documentation surface; uses `useDocumentationPage` for MD loading.



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
