---
title: "Terms of Service"
page_id: terms_page
source_json: terms_page.json
generator: json_to_markdown.py
---

# Terms of Service

## Overview

- **page_id:** terms_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Legal
- **era_tags:** 0.x, 11.x
- **flow_id:** terms
- **_id:** terms_page-001

## Metadata

- **route:** /terms
- **file_path:** contact360.io/root/app/(marketing)/terms/page.tsx
- **purpose:** Terms of service page displaying terms and conditions, user agreements, and service usage policies.
- **s3_key:** data/pages/terms_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** published
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **LegalPage** — `contact360/marketing/src/components/pages/MarketingPages.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Terms of Service

### subtitle

Last updated: Dynamic date

### description

These Terms of Service govern your use of the Contact360 platform ("Service"). Please read them carefully before using our website or purchasing a subscription.

### hero

- **title:** Terms of Service
- **description:** These Terms of Service govern your use of the Contact360 platform ("Service"). By accessing or using the Service, you agree to these Terms.
- **features**
  - 1. Acceptance of Terms
  - 2. Subscriptions & Payments
  - 3. Prohibited Use



## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| title | 1 | Terms of Service |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to / | termsPage | back-home | Back to Home | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| termsPage | Static legal document content | content | legal |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components



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
| back-home | Back to Home | ghost | navigate to / | termsPage |


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

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [C] > [H:Title] + [C:LegalContent] + (btn:back-home) + [C:Footer]

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/terms`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** [landing_page.md](landing_page.md) footer, SEO.

**Typical outbound:** [landing_page.md](landing_page.md), sign in / register.

**Cross-host:** Hand-off to `app` (authentication) and `email` (Mailhub) via shared marketing navigation.
**Backend:** Public legal surface; no first-party GraphQL host in `root`.



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
