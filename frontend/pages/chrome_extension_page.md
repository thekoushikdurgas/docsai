---
title: "Chrome Extension"
page_id: chrome_extension_page
source_json: chrome_extension_page.json
generator: json_to_markdown.py
---

# Chrome Extension

## Overview

- **page_id:** chrome_extension_page
- **page_type:** product
- **codebase:** root
- **surface:** Root Marketing
- **era_tags:** 4.x, 9.x, 11.x
- **flow_id:** chrome_extension
- **_id:** chrome_extension_page-001

## Metadata

- **route:** /products/chrome-extension
- **file_path:** contact360.io/root/app/(marketing)/products/chrome-extension/page.tsx
- **purpose:** Chrome extension information page displaying features, installation instructions, and benefits. Find emails on LinkedIn and company websites with one click.
- **s3_key:** data/pages/chrome_extension_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **ChromeExtensionPage** — `app/(marketing)/chrome-extension/page.tsx`
- **MarketingPageContainer** — `components/marketing/MarketingPageContainer.tsx`
- **ChromeExtensionPageRenderer** — `components/pages/MarketingPages.tsx` (ChromeExtensionPage)
- **Button3D** — `components/ui/Button3D.tsx`
- **Globe** — `lucide-react`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Chrome Extension

### subtitle

Find emails on LinkedIn and company websites with one click.

### description

Our extension layers verified data on top of the sites you visit.

### hero

- **title:** Chrome Extension
- **subtitle:** Marketing Page
- **description:** Our extension layers verified data on top of the sites you visit.
- **features**
  - Prospect Everywhere

- **cta_text:** Add to Chrome - It's Free

### features

- **title:** Prospect Everywhere
- **description:** Our extension layers verified data on top of the sites you visit.
- **cta:** Add to Chrome - It's Free


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| ext-title | 1 | Find emails on LinkedIn in one click |
| installation | 2 | Installation |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| open Chrome Web Store link | ChromeExtensionPage | install-chrome | Add to Chrome — Free | primary |
| navigate to /register | ChromeExtensionPage | ext-cta-register | Create Free Account | secondary |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ChromeExtensionPage | The Contact360 Chrome Extension lets you find and verify emails directly on LinkedIn and company websites. | ext-description | body |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ChromeExtensionPage | extension-install-flow | Extension installation flow | ["Click 'Add to Chrome'", "Chrome Web Store → 'Add Extension'", 'Extension appears in toolbar', 'Navigate to LinkedIn profile', 'Click extension icon → email found'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/pages/MarketingPages.tsx | ChromeExtensionPage | Marketing page for Chrome extension with install flow |


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
| install-chrome | Add to Chrome — Free | primary | open Chrome Web Store link | ChromeExtensionPage |
| ext-cta-register | Create Free Account | secondary | navigate to /register | ChromeExtensionPage |


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

- **4.x** — Extension & Sales Navigator — LinkedIn dashboard page, Chrome extension marketing, SN workflows.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [P] product layout > [H] > [C] value props + `[F]` demos — `(btn)` try/sign-in; links to app auth.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/products/chrome-extension`

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
