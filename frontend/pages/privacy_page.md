---
title: "Privacy Policy"
page_id: privacy_page
source_json: privacy_page.json
generator: json_to_markdown.py
---

# Privacy Policy

## Overview

- **page_id:** privacy_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Legal
- **era_tags:** 0.x, 11.x
- **flow_id:** privacy
- **_id:** privacy_page-001

## Metadata

- **route:** /privacy
- **file_path:** contact360.io/root/app/(marketing)/privacy/page.tsx
- **purpose:** Privacy policy page displaying data protection and privacy information, GDPR compliance, and user rights.
- **s3_key:** data/pages/privacy_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** published
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []

### UI components (metadata)

- **PrivacyPage** — `app/(marketing)/privacy/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **LegalPageRenderer** — `components/pages/MarketingPages.tsx` (LegalPage)

## Content sections (summary)

### title

Privacy Policy

### subtitle

Last updated: Dynamic date

### description

This Privacy Policy explains how Contact360 collects, uses, and protects your data when you use our website and services.

### hero

- **title:** Privacy Policy
- **description:** This Privacy Policy explains how Contact360 collects, uses, and protects your data when you use our website and services.
- **features**
  - 1. Data We Collect
  - 2. How We Use Data
  - 3. Payment Processing



## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| title | 1 | Privacy Policy |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to / | privacyPage | back-home | Back to Home | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| privacyPage | Static legal document content | content | legal |


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
| back-home | Back to Home | ghost | navigate to / | privacyPage |


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

**Composite layout:** [P] public layout > [H] hero/title > [C] sections — `(btn)` CTAs, optional `(in)` newsletter; light `{REST}` or static content.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/privacy`

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
