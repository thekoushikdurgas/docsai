---
title: "Settings"
page_id: settings_page
source_json: settings_page.json
generator: json_to_markdown.py
---

# Settings

## Overview

- **page_id:** settings_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 1.x, 11.x
- **flow_id:** settings
- **_id:** settings_page-001

### UI components (metadata)

- **SettingsPage** — `app/(dashboard)/settings/page.tsx` (Redirects to `/profile`)
- **ProfilePage** — `app/(dashboard)/profile/page.tsx` (Target destination)

## Metadata

- **route:** /settings
- **file_path:** contact360.io/app/app/(dashboard)/settings/page.tsx
- **purpose:** Settings redirect: Unified entry point that routes to /profile for account management.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard in layout)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
- **uses_endpoints:** []
- **ui_components:** []
- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Settings

### description

Redirect-only page. Immediately redirects /settings to /profile. No UI or API calls. User settings are managed on the profile page.

## Sections (UI structure)

### headings

### subheadings

### tabs

### buttons

### input_boxes

### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| SettingsPage | Redirecting to /profile... | redirect-notice | info |

### checkboxes

### radio_buttons

### progress_bars

### graphs

### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| SettingsPage | settings-redirect | Settings redirect flow | ['User navigates to /settings', 'Next.js redirect immediately sends to /profile', 'No UI rendered'] |

### components

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| next/navigation | useRouter | Client-side redirection logic | 0.x |

### services

### contexts

### utilities

### ui_components

### endpoints

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

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |

## Data Sources

- Appointment360 GraphQL gateway
- Backend-owned data stores (via GraphQL modules)

## Flow summary

app page UI -> page hooks -> page services -> GraphQL gateway -> backend modules -> rendered states

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/settings`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), `router.push` / `<Link>` from **### buttons** table above.

**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / [register_page.md](register_page.md); product pages on **root** deep-link to app auth.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [contacts_page](contacts_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [profile_page](profile_page.md)
- [register_page](register_page.md)
- [root_page](root_page.md)
- [sequences_page](sequences_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

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
