---
title: "Never bounce again with 99% deliverability."
page_id: email_verifier_page
source_json: email_verifier_page.json
generator: json_to_markdown.py
---

# Never bounce again with 99% deliverability.

## Overview

- **page_id:** email_verifier_page
- **page_type:** product
- **codebase:** root
- **surface:** product
- **era_tags:** 2.x, 9.x
- **flow_id:** email_verifier
- **_id:** email_verifier_page-001

## Metadata

- **route:** /products/email-verifier
- **file_path:** contact360.io/root/app/(marketing)/products/email-verifier/page.tsx
- **purpose:** Email Verifier: Marketing landing page for deliverability and SMTP verification tools.
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
- **VerifierAnimation** — `components/landing/animations/VerifierAnimation.tsx`

- **versions:** []
- **endpoint_count:** 1
### api_versions

- graphql

- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Never bounce again with 99% deliverability.

### subtitle

Email Verifier

### description

Our 7-step verification process pings SMTP servers in real-time. Pay only for Safe to Send results.

### hero

- **title:** Never bounce again with 99% deliverability.
- **subtitle:** Email Verifier
- **description:** Protect your sender reputation. Our 7-step verification process pings SMTP servers in real-time to confirm inbox existence without sending a test email. Pay only for 'Safe to Send' results.
- **features**
  - Bulk verify lists of up to 100,000 emails
  - Detect disposable & spam-trap emails
  - Automatic replacement of invalid contacts
  - API access for real-time verification

- **cta_text:** Verify Your List


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| verifier-hero | 1 | Verify any email address instantly |
| how-it-works | 2 | How Email Verifier works |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register | EmailVerifierProductPage | verifier-try-cta | Try Email Verifier Free | primary |
| scroll to demo section | EmailVerifierProductPage | verifier-see-demo | See How It Works | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| EmailVerifierProductPage | Verify emails in real-time with SMTP handshake. Clean your lists and reduce bounce rates. | verifier-description | body |
| EmailVerifierProductPage | 99% deliverability when using Contact360 | deliverability-stat | stat |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/landing/shared/ProductPageLayout.tsx | ProductPageLayout | Product marketing page shell |


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
| verifier-try-cta | Try Email Verifier Free | primary | navigate to /register | EmailVerifierProductPage |
| verifier-see-demo | See How It Works | ghost | scroll to demo section | EmailVerifierProductPage |


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

- **2.x** — Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.
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

**Route (registry):** `/products/email-verifier`

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
| `GetMarketingPage` | [query_get_marketing_page_graphql.md](../../backend/endpoints/query_get_marketing_page_graphql.md) | QUERY | 9.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
