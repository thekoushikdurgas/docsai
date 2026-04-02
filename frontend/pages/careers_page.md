---
title: "Join the Team"
page_id: careers_page
source_json: careers_page.json
generator: json_to_markdown.py
---

# Join the Team

## Overview

- **page_id:** careers_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Marketing
- **era_tags:** 0.x, 9.x, 11.x
- **flow_id:** careers
- **_id:** careers_page-001

## Metadata

- **route:** /careers
- **file_path:** contact360.io/root/app/(marketing)/careers/page.tsx
- **purpose:** Careers page displaying job openings and company culture information. Help us build the future of B2B intelligence.
- **s3_key:** data/pages/careers_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **CareersPage** — `app/(marketing)/careers/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **CareersPageRenderer** — `components/pages/MarketingPages.tsx` (CareersPage)
- **Badge3D** — `components/ui/Badge3D.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Join the Team

### subtitle

Help us build the future of B2B intelligence.

### description

Help us build the future of B2B intelligence.

### hero

- **title:** Join the Team
- **subtitle:** Help us build the future of B2B intelligence.
- **description:** Help us build the future of B2B intelligence.
- **features**
  - Senior Frontend Engineer
  - Product Designer
  - Growth Marketer
  - Data Scientist

- **cta_text:** View Open Roles


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| careers-title | 1 | Join the Team |
| open-roles | 2 | Open Roles |
| culture | 2 | Life at Contact360 |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| careers-engineering | engineering | Engineering |
| careers-sales | sales | Sales |
| careers-all | all | All Roles |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| open job application (external or form) | JobCard | apply-role | Apply Now | primary |
| scroll to culture section | CareersPage | learn-culture | Learn About Our Culture | secondary |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| CareersPage | Help us build the future of B2B intelligence. | careers-subtitle | body |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/pages/MarketingPages.tsx | CareersPage | Job listings with culture section and apply CTAs |


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
| apply-role | Apply Now | primary | open job application (external or form) | JobCard |
| learn-culture | Learn About Our Culture | secondary | scroll to culture section | CareersPage |


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

**Route (registry):** `/careers`

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
