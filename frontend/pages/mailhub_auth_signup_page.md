---
title: "Mailhub signup"
page_id: mailhub_auth_signup_page
source_json: mailhub_auth_signup_page.json
generator: json_to_markdown.py
---

# Mailhub signup

## Overview

- **page_id:** mailhub_auth_signup_page
- **page_type:** dashboard
- **codebase:** email
- **surface:** Mailhub
- **era_tags:** 0.x, 1.x, 11.x
- **flow_id:** mailhub-auth-signup
- **_id:** mailhub_auth_signup_page-001

### UI components (metadata)

- **SignupPage** — `src/app/auth/signup/page.tsx`
- **SignupForm** — `components/signup-form.tsx`
- **Card** — `components/ui/card.tsx`
- **Button** — `components/ui/button.tsx`
- **Input** — `components/ui/input.tsx`
- **Field** — `components/ui/field.tsx`
- **codebase:** email
- **canonical_repo:** contact360.io/email

## Metadata

- **route:** /auth/signup
- **file_path:** contact360.io/email/src/app/auth/signup/page.tsx
- **purpose:** Mailhub signup / registration.
- **s3_key:** data/pages/mailhub_auth_signup_page.json
- **status:** published
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **codebase:** email
- **canonical_repo:** contact360.io/email

## Content sections (summary)

### title

Mailhub signup

### description

Account creation for Mailhub.


## UI elements (top-level)

### buttons

[]

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


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] Mailhub layout > [H] or folder chrome > `[Q]` message list / `[F]` account — `{REST}` IMAP-backed APIs; `(btn)` `(in)` `(cb)` per sections above; `(pb)` sync optional.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/auth/signup`

**Codebase:** `contact360.io/email` (Mailhub, REST backend).

**Typical inbound:** folder nav from [mailhub_home_page.md](mailhub_home_page.md), auth from [mailhub_auth_login_page.md](mailhub_auth_login_page.md).

**Typical outbound:** [mailhub_email_detail_page.md](mailhub_email_detail_page.md) from lists; account [mailhub_account_page.md](mailhub_account_page.md).

**Cross-host:** Deployed separately from dashboard; optional product links to **app** (integration TBD).
**REST / data lineage (Mailhub):** [../../backend/database/emailapp_data_lineage.md](../../backend/database/emailapp_data_lineage.md) (not the dashboard GraphQL gateway).



## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [mailhub_account_page](mailhub_account_page.md)
- [mailhub_auth_login_page](mailhub_auth_login_page.md)
- [mailhub_draft_page](mailhub_draft_page.md)
- [mailhub_email_detail_page](mailhub_email_detail_page.md)
- [mailhub_home_page](mailhub_home_page.md)
- [mailhub_inbox_page](mailhub_inbox_page.md)
- [mailhub_sent_page](mailhub_sent_page.md)
- [mailhub_spam_page](mailhub_spam_page.md)

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
