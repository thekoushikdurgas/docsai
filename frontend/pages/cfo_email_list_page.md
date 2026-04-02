---
title: "CFO Email List"
page_id: cfo_email_list_page
source_json: cfo_email_list_page.json
generator: json_to_markdown.py
---

# CFO Email List

## Overview

- **page_id:** cfo_email_list_page
- **page_type:** title
- **codebase:** root
- **surface:** title
- **era_tags:** 2.x, 9.x
- **flow_id:** cfo_email_list
- **_id:** cfo_email_list_page-001

## Metadata

- **route:** /products/cfo-email-list
- **file_path:** contact360.io/root/app/(marketing)/products/cfo-email-list/page.tsx
- **purpose:** CFO Email List: Targeted marketing landing page for finance leader contact data.
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
- **CFOHeroSection** — `contact360/marketing/src/components/marketing/CFOHeroSection.tsx`
- **CFOConversionStrip** — `contact360/marketing/src/components/marketing/CFOConversionStrip.tsx`
- **CFOSegmentation** — `contact360/marketing/src/components/landing/sections/CFOEmailListSections.tsx`
- **CFOBenefits** — `contact360/marketing/src/components/landing/sections/CFOEmailListSections.tsx`
- **CFODataQuality** — `contact360/marketing/src/components/landing/sections/CFOEmailListSections.tsx`
- **CFOTestimonials** — `contact360/marketing/src/components/landing/sections/CFOEmailListSections.tsx`
- **CFOFAQ** — `contact360/marketing/src/components/landing/sections/CFOEmailListSections.tsx`

- **versions:** []
- **endpoint_count:** 1
### api_versions

- graphql

- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

CFO Email List

### subtitle

Target Finance Leaders

### description

The CFO Mailing List is a highly targeted business contact database that contains the names and emails of top level executives in companies.

### hero

- **title:** CFO Email List
- **subtitle:** Target Finance Leaders
- **description:** The CFO Mailing List is a highly targeted business contact database that contains the names and emails of top level executives in companies. This list can be used for telemarketing, direct mail, email campaigns, or any other marketing campaign.
- **features**
  - CFO-focused segments
  - Verified emails and phones
  - Fortune 500 coverage
  - Bulk export

- **cta_text:** ACCESS NOW


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| cfo-title | 1 | CFO Email List |
| cfo-subtitle | 2 | Target Finance Leaders |
| hero-stats | 2 | Database Coverage |
| segmentation | 2 | CFO Segmentation |
| data-quality | 2 | Data Quality |
| testimonials | 2 | Trusted by marketers |
| faq | 2 | FAQ |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register or contact sales | CFOHeroSection | access-cfo-list | ACCESS NOW | primary |
| navigate to /register | CFOConversionStrip | conversion-strip-cta | Get CFO Contacts | primary |
| expand/collapse FAQ item | CFOFAQ | faq-expand | FAQ accordion | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| CFOHeroSection | The CFO Mailing List is a highly targeted business contact database containing the names and emails of top-level executives. Use for telemarketing, direct mail, or email campaigns. | hero-description | body |
| CFOHeroSection | 160+ Countries Covered | stat-countries | stat |
| CFOHeroSection | 100% Verified Database | stat-verified | stat |
| CFOHeroSection | 17+ Years Industry Expertise | stat-years | stat |
| CFOHeroSection | 95% Delivery Guaranteed | stat-delivery | stat |
| CFOHeroSection | National: 223,919 contacts / 199,039 emails | national-count | stat |
| CFOHeroSection | International: 92,164 contacts / 51,842 emails | international-count | stat |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| CFODataQuality | delivery-rate | Email delivery guarantee | 95% delivery rate bar visualization | determinate |


### graphs

| chart_type | component | data_source | id | label | metrics |
| --- | --- | --- | --- | --- | --- |
| stat_cards | CFOHeroSection | static content_sections.hero_stats | hero-stats-cards | CFO database coverage stats | ['160+ countries', '100% verified', '17+ years', '95% delivery'] |
| comparison_table | CFOHeroSection | static content_sections.hero_table | national-intl-table | National vs international contacts table |  |


### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/marketing/CFOHeroSection.tsx | CFOHeroSection | Hero with title, description, stat cards, hero table, CTA |
| contact360.io/root/src/components/marketing/CFOConversionStrip.tsx | CFOConversionStrip | CTA conversion strip with email CTA |
| contact360.io/root/src/components/landing/sections/CFOEmailListSections.tsx | CFOSegmentation | CFO audience segmentation breakdown section |
| contact360.io/root/src/components/landing/sections/CFOEmailListSections.tsx | CFOBenefits | Benefits of CFO email list section |
| contact360.io/root/src/components/landing/sections/CFOEmailListSections.tsx | CFODataQuality | Data quality and accuracy stats section |
| contact360.io/root/src/components/landing/sections/CFOEmailListSections.tsx | CFOTestimonials | Customer testimonials carousel |
| contact360.io/root/src/components/landing/sections/CFOEmailListSections.tsx | CFOFAQ | FAQ accordion section |


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
| access-cfo-list | ACCESS NOW | primary | navigate to /register or contact sales | CFOHeroSection |
| conversion-strip-cta | Get CFO Contacts | primary | navigate to /register | CFOConversionStrip |
| faq-expand | FAQ accordion | ghost | expand/collapse FAQ item | CFOFAQ |


### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| delivery-rate | Email delivery guarantee | 95% delivery rate bar visualization | determinate | CFODataQuality |


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

**Composite layout:** [H] + [C] — focused landing / list title surface; `(btn)` to product or auth.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/products/cfo-email-list`

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
| `GetMarketingPage` | [query_get_marketing_page_graphql.md](../../backend/endpoints/query_get_marketing_page_graphql.md) | QUERY | 9.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
