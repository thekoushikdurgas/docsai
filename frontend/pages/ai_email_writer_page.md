---
title: "Turn cold leads into warm conversations."
page_id: ai_email_writer_page
source_json: ai_email_writer_page.json
generator: json_to_markdown.py
---

# Turn cold leads into warm conversations

## Overview

- **page_id:** ai_email_writer_page
- **page_type:** product
- **codebase:** root
- **surface:** product
- **era_tags:** 5.x, 9.x
- **flow_id:** ai_email_writer
- **_id:** ai_email_writer_page-001

## Metadata

- **route:** /products/ai-email-writer
- **file_path:** contact360.io/root/app/(marketing)/products/ai-email-writer/page.tsx
- **purpose:** AI Email Writer product page displaying features, benefits, workflow, integrations, and social proof.
- **s3_key:** data/pages/ai_email_writer_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-02-03T00:00:00.000000+00:00

### uses_endpoints (1)

- `graphql/GetMarketingPage` — Get marketing page content dynamically. Falls back to static content if API fails.

### UI components (metadata)

- **ProductPageLayout** — `contact360/marketing/src/components/landing/shared/ProductPageLayout.tsx`
- **MarketingPageContainer** — `contact360/marketing/src/components/marketing/MarketingPageContainer.tsx`
- **PersonalizationEngineAnimation** — `components/landing/animations/PersonalizationEngineAnimation.tsx`
- **FunnelImpact** — `components/landing/sections/ai-writer/FunnelImpact.tsx`
- **WriterWorkflow** — `components/landing/sections/ai-writer/WriterWorkflow.tsx`
- **BeforeAfterComparison** — `components/landing/sections/ai-writer/BeforeAfterComparison.tsx`
- **WriterIntegrations** — `components/landing/sections/ai-writer/WriterIntegrations.tsx`
- **WriterSocialProof** — `components/landing/sections/ai-writer/WriterSocialProof.tsx`
- **AiBenefits** — `components/landing/sections/ai-writer/AiBenefits.tsx`
- **WriterFAQ** — `components/landing/sections/ai-writer/WriterFAQ.tsx`
- **AIWriterCTASection** — `components/marketing/AIWriterCTASection.tsx`

- **versions:** []
- **endpoint_count:** 1

### api_versions

- graphql

- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Turn cold leads into warm conversations.

### subtitle

AI Email Writer

### description

Stop sending generic templates that get ignored. Our AI analyzes your prospect's LinkedIn profile, company news, and tech stack to craft hyper-relevant emails that actually get replies.

### hero

- **title:** Turn cold leads into warm conversations.
- **subtitle:** AI Email Writer
- **description:** Stop sending generic templates that get ignored. Our AI analyzes your prospect's LinkedIn profile, company news, and tech stack to craft hyper-relevant emails that actually get replies.
- **features**
  - Instant personalization based on company news
  - Tone adjustment for different buyer personas
  - Subject line optimization
  - A/B testing suggestions

- **cta_text:** Write Better Emails

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| hero-title | 1 | Turn cold leads into warm conversations. |
| writer-workflow | 2 | How it works |
| before-after | 2 | Before vs After |
| benefits | 2 | AI Email Benefits |
| integrations | 2 | Integrations |
| social-proof | 2 | Trusted by sales teams |
| faq | 2 | FAQ |

### subheadings

### tabs

### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register or /ai-chat | ProductPageLayout | primary-cta | Write Better Emails | primary |
| navigate to /register | AIWriterCTASection | secondary-cta | Start Personalizing Now | primary |
| expand/collapse FAQ accordion item | WriterFAQ | faq-expand | FAQ Item | ghost |

### input_boxes

### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ProductPageLayout | Stop sending generic templates that get ignored. Our AI analyzes your prospect's LinkedIn profile, company news, and tech stack to craft hyper-relevant emails that actually get replies. | hero-description | body |
| AIWriterCTASection | No credit card required | cta-no-credit-card | caption |
| AiBenefits | Instant personalization based on company news | feature-personalization | feature |
| AiBenefits | Tone adjustment for different buyer personas | feature-tone | feature |
| AiBenefits | Subject line optimization | feature-subject | feature |

### checkboxes

### radio_buttons

### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| PersonalizationEngineAnimation | personalization-engine-animation | Personalization engine animation | Animated illustration of AI processing pipeline | indeterminate |

### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| funnel | FunnelImpact | static marketing data | funnel-impact | Sales funnel impact chart |

### flows

### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/landing/shared/ProductPageLayout.tsx | ProductPageLayout | Full-width product marketing page shell |
| contact360.io/root/src/components/landing/animations/PersonalizationEngineAnimation.tsx | PersonalizationEngineAnimation | Animated diagram of AI email personalization pipeline |
| contact360.io/root/src/components/landing/sections/ai-writer/FunnelImpact.tsx | FunnelImpact | Funnel chart showing reply rate improvement |
| contact360.io/root/src/components/landing/sections/ai-writer/WriterWorkflow.tsx | WriterWorkflow | Step-by-step workflow illustration |
| contact360.io/root/src/components/landing/sections/ai-writer/BeforeAfterComparison.tsx | BeforeAfterComparison | Before/after email quality comparison |
| contact360.io/root/src/components/landing/sections/ai-writer/AiBenefits.tsx | AiBenefits | Feature bullets list: personalization, tone, subject |
| contact360.io/root/src/components/landing/sections/ai-writer/WriterIntegrations.tsx | WriterIntegrations | Integration partner logos (Gmail, Outreach, etc.) |
| contact360.io/root/src/components/landing/sections/ai-writer/WriterSocialProof.tsx | WriterSocialProof | Customer testimonials and trust badges |
| contact360.io/root/src/components/landing/sections/ai-writer/WriterFAQ.tsx | WriterFAQ | Accordion FAQ section |
| contact360.io/root/src/components/marketing/AIWriterCTASection.tsx | AIWriterCTASection | Final CTA section with sign up button |

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
| primary-cta | Write Better Emails | primary | navigate to /register or /ai-chat | ProductPageLayout |
| secondary-cta | Start Personalizing Now | primary | navigate to /register | AIWriterCTASection |
| faq-expand | FAQ Item | ghost | expand/collapse FAQ accordion item | WriterFAQ |

### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| personalization-engine-animation | Personalization engine animation | Animated illustration of AI processing pipeline | indeterminate | PersonalizationEngineAnimation |

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

- **5.x** — AI workflows — AI chat, live voice, AI email writer product, assistant panels.
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

**Route (registry):** `/products/ai-email-writer`

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
| `GetMarketingPage` | [query_get_marketing_page_graphql.md](../../backend/endpoints/query_get_marketing_page_graphql.md) | QUERY | 9.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
