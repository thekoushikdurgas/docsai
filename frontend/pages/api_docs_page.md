---
title: "Contact360 API"
page_id: api_docs_page
source_json: api_docs_page.json
generator: json_to_markdown.py
---

# Contact360 API

## Overview

- **page_id:** api_docs_page
- **page_type:** marketing
- **codebase:** root
- **surface:** marketing
- **era_tags:** 8.x, 9.x
- **flow_id:** api_docs
- **_id:** api_docs_page-001

## Metadata

- **route:** /api-docs
- **file_path:** contact360.io/root/app/(marketing)/api-docs/page.tsx
- **purpose:** Contact360 API documentation page displaying API endpoints, authentication, usage examples, and integration guides. Integrate our verified data directly into your application.
- **s3_key:** data/pages/api_docs_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-02-03T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **ApiDocsPage** — `app/(marketing)/api-docs/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **ApiPageRenderer** — `components/pages/MarketingPages.tsx` (ApiPage)
- **Card3D** — `components/ui/Card3D.tsx`
- **Button3D** — `components/ui/Button3D.tsx`
- **Zap** — `lucide-react`
- **Database** — `lucide-react`

Contact360 API

### subtitle

Integrate our verified data directly into your application.

### hero

- **title:** Contact360 API
- **subtitle:** API Reference
- **description:** Integrate our verified data directly into your application.
- **features**
  - Blazing Fast
  - Bulk Endpoints

- **cta_text:** Read Documentation

### features

- **[0]**
  - **title:** Blazing Fast
  - **description:** Sub-200ms response times for real-time enrichment.
  - **icon:** Zap

- **[1]**
  - **title:** Bulk Endpoints
  - **description:** Process up to 100k records in a single batch request.
  - **icon:** Database



## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| api-title | 1 | Contact360 API |
| auth | 2 | Authentication |
| endpoints | 2 | Endpoints |
| code-example | 2 | Code Example |


### subheadings

| id | level | text |
| --- | --- | --- |
| rest-api | 3 | REST API |
| graphql-api | 3 | GraphQL API |
| webhooks | 3 | Webhooks |


### tabs

| content_ref | id | label |
| --- | --- | --- |
| api-rest | rest | REST API |
| api-graphql | graphql | GraphQL |
| api-sdks | sdks | SDKs |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| clipboard.copyToClipboard(curlExample) | ApiDocsPage | copy-curl | Copy | icon |
| navigate to /profile#api-keys (or /register if not logged in) | ApiDocsPage | get-api-key | Get API Key | primary |
| navigate to full docs | ApiDocsPage | read-docs-cta | Read Documentation | secondary |


### input_boxes



### text_blocks

| component | content | id | language | type |
| --- | --- | --- | --- | --- |
| ApiDocsPage | Integrate Contact360's verified B2B data directly into your application. | api-intro |  | body |
| ApiDocsPage | curl -X POST https://api.contact360.com/v1/enrich ... | curl-example | bash | code |
| ApiDocsPage | Include your API key in the Authorization: Bearer {key} header. | auth-note |  | info |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/pages/MarketingPages.tsx | ApiPage | Marketing API docs page layout with features, examples, CTA |


### hooks



### services



### contexts



### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy curl example code snippets |


### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| copy-curl | Copy | icon | clipboard.copyToClipboard(curlExample) | ApiDocsPage |
| get-api-key | Get API Key | primary | navigate to /profile#api-keys (or /register if not logged in) | ApiDocsPage |
| read-docs-cta | Read Documentation | secondary | navigate to full docs | ApiDocsPage |


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

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useMarketingPage (conditional content path) | GetMarketingPage | marketingService | query |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway/docs references | public/private API documentation surfaces | documentation and developer onboarding |


## Data Sources

- Marketing content services
- API documentation content sources


## Flow summary

root API docs page -> marketing/docs content retrieval -> developer CTA to auth/app API key management


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.
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

**Route (registry):** `/api-docs`

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
