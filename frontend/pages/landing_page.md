---
title: "Landing"
page_id: landing_page
source_json: landing_page.json
generator: json_to_markdown.py
---

# Landing

## Overview

- **page_id:** landing_page
- **page_type:** marketing
- **codebase:** root
- **surface:** Root Marketing
- **era_tags:** 0.x, 9.x, 11.x
- **flow_id:** landing
- **_id:** landing_page-001

## Metadata

- **route:** /
- **file_path:** contact360.io/root/app/page.tsx
- **purpose:** Landing page with hero section, features showcase, product demonstrations, pricing tiers, and footer. The world's most accurate B2B data platform with 200M+ verified contacts.
- **s3_key:** data/pages/landing_page.json
- **status:** published
- **authentication:** Not required (public page)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
### UI components (metadata)

- **LandingPage** — `app/page.tsx`
- **Navbar** — `components/landing/Navbar.tsx`
- **Hero** — `components/landing/Hero.tsx`
- **DataStatsSection** — `components/landing/DataStatsSection.tsx`
- **PlatformTabs** — `components/landing/PlatformTabs.tsx`
- **EmailFinderSection** — `components/landing/EmailFinderSection.tsx`
- **ChromeExtensionSection** — `components/landing/ChromeExtensionSection.tsx`
- **ProspectFinderSection** — `components/landing/ProspectFinderSection.tsx`
- **EmailVerifierSection** — `components/landing/EmailVerifierSection.tsx`
- **AIWriterSection** — `components/landing/AIWriterSection.tsx` (Dynamic)
- **Features** — `components/landing/Features.tsx` (Dynamic)
- **Pricing** — `components/landing/Pricing.tsx` (Dynamic)
- **SalesCTA** — `components/landing/SalesCTA.tsx`
- **Footer** — `components/landing/Footer.tsx`
- **EmailFinderSection** — `contact360/marketing/src/components/landing/sections/EmailFinderSection.tsx`
- **ChromeExtensionSection** — `contact360/marketing/src/components/landing/sections/ChromeExtensionSection.tsx`
- **ProspectFinderSection** — `contact360/marketing/src/components/landing/sections/ProspectFinderSection.tsx`
- **EmailVerifierSection** — `contact360/marketing/src/components/landing/sections/EmailVerifierSection.tsx`
- **AIWriterSection** — `contact360/marketing/src/components/landing/sections/AIWriterSection.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** root
- **canonical_repo:** contact360.io/root

## Content sections (summary)

### title

Landing

### description

Landing page with hero section, features showcase, product demonstrations, pricing tiers, and footer. The world's most accurate B2B data platform with 200M+ verified contacts.

### navbar

- **title:** Contact360
- **navigation_items**
  - **[0]**
    - **label:** Data
    - **href:** #features
    - **page:** landing

  - **[1]**
    - **label:** Pricing
    - **href:** #pricing
    - **page:** landing

  - **[2]**
    - **label:** Integrations
    - **page:** integrations

  - **[3]**
    - **label:** API
    - **page:** api-docs


- **cta_buttons**
  - **[0]**
    - **label:** Sign In
    - **action:** navigate
    - **page:** login

  - **[1]**
    - **label:** Get Started
    - **action:** navigate
    - **page:** register



### hero

- **badge_text:** Now with 200M+ Verified Contacts
- **headline:** The World's Most Accurate Data
- **subheading:** The only B2B data platform where you pay strictly for verified emails.
- **cta_primary**
  - **text:** Start Prospecting for Free
  - **action:** navigate
  - **page:** register

- **cta_secondary**
  - **text:** View Live Demo
  - **action:** navigate
  - **page:** about

- **trust_section**
  - **label:** Trusted by growth teams at
  - **companies**
    - Acme Corp
    - GlobalTech
    - Nebula
    - FoxRun
    - Circle



### features

- **title:** Try our tools now, it's free
- **description:** Start prospecting with the most accurate data in the industry.
- **items**
  - **[0]**
    - **title:** Email Finder
    - **description:** Find any email address from a first name, last name and company name.
    - **icon:** Search

  - **[1]**
    - **title:** Email Verifier
    - **description:** Pay only for verified emails. Upload your list and verify deliverability instantly.
    - **icon:** ShieldCheck

  - **[2]**
    - **title:** Prospect Finder
    - **description:** Find high-quality B2B leads from our database of 200M+ verified contacts.
    - **icon:** Users




## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| hero-title | 1 | The world's most accurate B2B data platform |
| features-title | 2 | Everything you need to fill your pipeline |
| pricing-title | 2 | Simple, transparent pricing |
| testimonials-title | 2 | Trusted by high-growth sales teams |
| cta-title | 2 | Start finding verified contacts today |


### subheadings

| id | level | text |
| --- | --- | --- |
| hero-subtitle | 3 | 200M+ verified contacts. Real-time enrichment. No bad data. |


### tabs

| content_ref | id | label |
| --- | --- | --- |
| platform-tab-finder | email-finder | Email Finder |
| platform-tab-verifier | email-verifier | Email Verifier |
| platform-tab-enrichment | data-enrichment | Data Enrichment |
| platform-tab-ai | ai-tools | AI Tools |


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /register | Hero | hero-get-started | Get Started Free | primary |
| open demo video modal | Hero | hero-see-demo | Watch Demo | ghost |
| navigate to /register | PricingSection | pricing-free-cta | Start for Free | primary |
| navigate to /register (pro intent) | PricingSection | pricing-pro-cta | Get Pro | primary |
| navigate to /register | FooterCTASection | footer-cta | Start Prospecting Now | primary |
| navigate to /login | Navbar | navbar-login | Sign In | ghost |
| navigate to /register | Navbar | navbar-signup | Get Started | primary |
| expand/collapse FAQ item | FAQSection | faq-expand | FAQ accordion | ghost |
| open Chrome Web Store link | ChromeExtensionSection | chrome-extension-cta | Add to Chrome — Free | primary |


### input_boxes

| component | id | label | note | placeholder | type |
| --- | --- | --- | --- | --- | --- |
| Hero | hero-email | Work email | Quick signup inline input in hero section | you@company.com | email |
| FooterCTASection | newsletter-email | Email for updates |  | you@company.com | email |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| Hero | Find, verify, and enrich B2B contacts with 200M+ verified emails. Powered by AI. | hero-description | body |
| DataStatsSection | 200M+ verified contacts | data-stats-200m | stat |
| DataStatsSection | 98% deliverability rate | data-stats-98pct | stat |
| DataStatsSection | 50M+ companies | data-stats-50m | stat |


### checkboxes



### radio_buttons



### progress_bars



### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| animated_counter | DataStatsSection | static (200M+, 98%) | accuracy-animation | Email accuracy visualization |


### flows



### components

| file_path | name | purpose |
| --- | --- | --- |
| contact360.io/root/src/components/landing/Navbar.tsx | Navbar | Top navigation: logo, product links, login/signup CTAs |
| contact360.io/root/src/components/landing/Hero.tsx | Hero | Full-width hero with animated headline, inline email CTA, demo button |
| contact360.io/root/src/components/landing/sections/DataStatsSection.tsx | DataStatsSection | 3 animated stat counters (contacts, accuracy, companies) |
| contact360.io/root/src/components/landing/PlatformTabs.tsx | PlatformTabs | Product feature tabs: Finder/Verifier/Enrichment/AI |
| contact360.io/root/src/components/landing/sections/EmailFinderSection.tsx | EmailFinderSection | Email Finder product demo section |
| contact360.io/root/src/components/landing/sections/ChromeExtensionSection.tsx | ChromeExtensionSection | Chrome extension promotion section |
| contact360.io/root/src/components/landing/sections/PricingSection.tsx | PricingSection | Pricing tiers (Free, Pro, Enterprise) with feature lists |
| contact360.io/root/src/components/landing/sections/TestimonialsSection.tsx | TestimonialsSection | Customer testimonial carousel |
| contact360.io/root/src/components/landing/sections/FAQSection.tsx | FAQSection | Accordion FAQ |
| contact360.io/root/src/components/landing/sections/FooterCTASection.tsx | FooterCTASection | Final CTA banner with email signup |
| contact360.io/root/src/components/landing/Footer.tsx | Footer | Full site footer with links and social icons |


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
| hero-get-started | Get Started Free | primary | navigate to /register | Hero |
| hero-see-demo | Watch Demo | ghost | open demo video modal | Hero |
| pricing-free-cta | Start for Free | primary | navigate to /register | PricingSection |
| pricing-pro-cta | Get Pro | primary | navigate to /register (pro intent) | PricingSection |
| footer-cta | Start Prospecting Now | primary | navigate to /register | FooterCTASection |
| navbar-login | Sign In | ghost | navigate to /login | Navbar |
| navbar-signup | Get Started | primary | navigate to /register | Navbar |
| faq-expand | FAQ accordion | ghost | expand/collapse FAQ item | FAQSection |
| chrome-extension-cta | Add to Chrome — Free | primary | open Chrome Web Store link | ChromeExtensionSection |


### inputs

| id | label | type | placeholder | component | note |
| --- | --- | --- | --- | --- | --- |
| hero-email | Work email | email | you@company.com | Hero | Quick signup inline input in hero section |
| newsletter-email | Email for updates | email | you@company.com | FooterCTASection |  |


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
| useLandingContent | GetMarketingPage (conditional/fallback) | marketingService | query |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/GetMarketingPage | read-only marketing content |


## Data Sources

- Appointment360 GraphQL gateway
- fallback marketing page constants/content


## Flow summary

root landing UI -> marketing hooks/services -> GraphQL read (optional) -> fallback content -> CTA handoff to app auth routes

## Fallback data

*(4 entries; abbreviated)*

```json
[
  {
    "source": "fallbackMarketingPages",
    "page_key": "landing-product-showcase",
    "section_key": "product_showcase",
    "hero": {
      "title": "Find anyone's professional email.",
      "subtitle": "Unified Discovery",
      "description": "Connect with decision-makers directly. Enter identifiers and let our waterfall enrichment engine cross-reference 15+ real-time data sources.",
      "features": [
        "Enrich data from LinkedIn profiles",
        "Get professional email & direct dials",
        "Real-time confidence scores"
      ],
      "cta_text": "Try Search Engine"
    },
    "sections": {
      "product_showcase": {
        "email_finder": {
          "badge": "Unified Discovery",
          "badge_icon": "Search",
          "title": "Find anyone's professional email.",
          "description": "Connect with decision-makers directly. Enter identifiers and let our waterfall enrichment engine cross-reference 15+ real-time data sources.",
          "cta_text": "Try Search Engine"
        },
        "chrome_extension": {
          "badge": "Real-time Overlay",
          "badge_icon": "Chrome",
          "title": "Prospect directly on LinkedIn.",
          "description": "Reveal verified emails and phone numbers right where you prospect. Sync contacts directly to your CRM with a single click, without ever leaving Sales Navigator.",
          "cta_text": "Add to Chrome — It's Free"
        },
        "prospect_finder": {
          "badge": "List Building",
          "badge_icon": "Users",
          "title": "Build the perfect lead list.",
          "description": "Stop wasting time manually searching. Access 250M+ verified contacts with advanced filters for industry, revenue, and recent funding events.",
          "cta_text": "Build My List"
        },
        "email_verifier": {
          "badge": "Data Integrity",
          "badge_icon": "ShieldCheck",
          "title": "Never bounce again. 99% accuracy.",
          "description": "Protect your sender reputation. Our 7-step verification process pings SMTP servers in real-time without sending test emails.",
          "cta_text": "Verify Your List"
        },
        "ai_writer": {
          "badge": "AI Co-Pilot",
          "badge_icon": "Sparkles",
          "title": "Turn cold leads into warm conversations.",
          "description": "Don't just find the right person—say the right thing. Our AI scans the global web for recent company milestones, then crafts outreach so personal it's impossible to ignore.",
          "cta_text": "Start Writing With AI"
        }
      }
    }
  },
  {
    "source": "fallbackMarketingPages",
    "page_key": "landing-platform-tabs",
    "section_key": "platform_tabs",
    "metadata": {
      "title": "The Unified Prospecting Workflow",
      "description": "One platform for the entire sales cycle, powered by verified data and AI."
    },
    "sections": {
      "platform_tabs": {
        "title": "The Unified Prospecting Workflow",
        "description": "One platform for the entire sales cycle, powered by verified data and AI.",
        "tabs": [
          {
            "id": "search",
            "label": "Identify",
            "icon": "Search",
            "title": "Precision Targeting",
            "description": "Filter through 250M+ prospects with granular firmographic and technographic data.",
            "color": "bg-blue-600",
            "details": [
              "50+ Search Filters",
              "Technographic Data",
              "Funding Alerts"
            ]
          },
          {
            "id": "verify",
            "label": "Verify",
            "icon": "ShieldCheck",
            "title": "Zero-Bounce Guarantee",
            "description": "Our 7-step verification engine pings SMTP servers in real-time.",
            "color": "bg-green-600",
            "details": [
              "SMTP Handshake",
              "Spam Trap Detection",
              "99% Deliverability"
            ]
          },
          {
            "id": "engage",
            "label": "Personalize",
            "icon": "Zap",
            "title": "AI Personalization",
            "description": "Generate hyper-personalized cold emails using real-time web news and LinkedIn data.",
            "color": "bg-brand-600",
            "details": [
              "Web News Scanning",
              "Dynamic Variable Injection",
              "Persona Modeling"
            ]
          },
          {
            "id": "scale",
            "label": "Scale",
            "icon": "BarChart3",
            "title": "Revenue Acceleration",
            "description": "Sync your verified pipeline directly to your CRM and start closing.",
            "color": "bg-slate-900",
            "details": [
              "One-click CRM Sync",
              "Team Collaboration",
              "ROI Analytics"
            ]
          }
        ]
      }
    }
  },
  {
    "source": "fallbackMarketingPages",
    "page_key": "landing-data-stats",
    "section_key": "data_stats",
    "metadata": {
      "title": "250M+ Verified B2B Profiles",
      "description": "Real-time synced global B2B contact data."
    },
    "sections": {
      "data_stats": {
        "main_stat": {
          "value": "250M+",
          "label": "Verified B2B Profiles",
          "badge": "Real-Time Sync"
        },
        "breakdown": [
          {
            "value": "120M+",
            "label": "Mobiles",
            "icon": "Phone"
          },
          {
            "value": "60M+",
            "label": "Companies",
            "icon": "Building2"
          },
          {
            "value": "140+",
            "label": "Verticals",
            "icon": "TrendingUp"
          },
          {
            "value": "195",
            "label": "Countries",
            "icon": "Globe"
          }
        ]
      }
    }
  },
  {
    "source": "fallbackMarketingPages",
    "page_key": "landing-sales-cta",
    "section_key": "sales_cta",
    "metadata": {
      "title": "Get in Touch with Our Sales Team",
      "description": "See Contact360 in action and review pricing."
    },
    "sections": {
      "sales_cta": {
        "badge": "SEE CONTACT360 IN ACTION",
        "title": "Get in Touch with Our Sales Team",
        "button_text": "View Pricing List",
        "mockup_data": {
          "total_count": 478,
          "contacts": [
            {
              "name": "John Carter",
              "company": "Salesforce",
              "role": "Business Develop...",
              "color": "bg-blue-600"
            },
            {
              "name": "Mike Warren",
              "company": "Intercom",
              "role": "Director of Recru...",
              "color": "bg-blue-400"
            },
            {
              "name": "Matt Cannon",
              "company": "LinkedIn",
              "role": "VP of Customer S...",
              "color": "bg-[#0077b5]"
            },
            {
              "name": "Sophie Moore",
              "company": "SendGrid",
              "role": "Senior Project Ma...",
              "color": "bg-blue-500"
            },
            {
              "name": "Jeremy Matthews",
              "company": "Slack",
              "role": "Director of Produ...",
              "color": "bg-[#4a154b]"
            },
            {
              "name": "Katie Corl",
              "company": "Zendesk",
              "role": "VP of Marketing",
              "color": "bg-[#03363d]"
            },
            {
              "name": "Sam Owen",
              "company": "SendGrid",
              "role": "Financial Data An...",
              "color": "bg-blue-500"
            }
          ]
        }
      }
    }
  }
]
```


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Landing] > [H:Navbar] + [Q:Hero] + [S:Features] + [P:Pricing] + [F:Footer]

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/`

**Codebase:** `contact360.io/root` (marketing / public docs shell).

**Typical inbound:** SEO / External entry, [index.md](index.md) root navigation.

**Typical outbound:** Sign in / Get started → **app** [login_page.md](login_page.md) / [register_page.md](register_page.md); product CTAs → same; Footer → `/about`, `/careers`, `/docs`.

**Cross-host:** Hand-off to `app` (authentication) and `email` (Mailhub) via landing site CTAs.
**Backend:** Public marketing surface; no first-party GraphQL host in `root`.



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
