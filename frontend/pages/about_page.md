---
title: "About Contact360"
page_id: about_page
source_json: about_page.json
generator: json_to_markdown.py
---

# About Contact360

## Overview

- **page_id:** about_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Marketing
- **era_tags:** 0.x, 9.x, 11.x
- **flow_id:** about
- **_id:** about_page-001

## Metadata

- **route:** /about
- **file_path:** contact360.io/root/app/(marketing)/about/page.tsx
- **purpose:** About Contact360 page showing mission hero, value cards, and company story. Used for marketing site and internal documentation.
- **s3_key:** data/pages/about_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **AboutPage** — `app/(marketing)/about/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **AboutPageRenderer** — `components/pages/MarketingPages.tsx` (AboutPage)
- **Card3D** — `components/ui/Card3D.tsx`
- **Button3D** — `components/ui/Button3D.tsx`
- **Shield** — `lucide-react`
- **Zap** — `lucide-react`
- **Users** — `lucide-react`

### title

About Contact360

### subtitle

We're on a mission to democratize B2B data accuracy.

### hero

- **title:** About Contact360
- **subtitle:** We're on a mission to democratize B2B data accuracy.
- **description:** Founded in 2024, Contact360 started with a simple observation: B2B data was too expensive and too inaccurate. We built a proprietary engine that verifies data in real-time, ensuring you only pay for contacts that actually exist.
- **features**
  - Data Integrity
  - Real-time Verification
  - Customer First

- **cta_text:** Join Our Journey


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| about-title | 1 | About Contact360 |
| mission | 2 | Our Mission |
| values | 2 | Our Values |
| story | 2 | Our Story |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register | AboutPage | about-cta | Get Started Free | primary |
| mailto:hello@contact360.io | AboutPage | contact-us | Contact Us | secondary |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| AboutPage | We're on a mission to democratize B2B data accuracy. | mission-statement | body |
| AboutPage | Precision first — 98%+ deliverability or we refund your credits. | value-accuracy | feature |
| AboutPage | No hidden fees. No bulk minimums. No locked-in contracts. | value-transparency | feature |
| AboutPage | Real-time Verification — SMTP handshake with 99% accuracy. | value-speed | feature |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/pages/MarketingPages.tsx | AboutPage | Static about page with company story, values, team section |


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
| about-cta | Get Started Free | primary | navigate to /register | AboutPage |
| contact-us | Contact Us | secondary | mailto:hello@contact360.io | AboutPage |


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

**Route (registry):** `/about`

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
