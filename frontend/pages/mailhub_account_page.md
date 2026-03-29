---
title: "Account"
page_id: mailhub_account_page
source_json: mailhub_account_page.json
generator: json_to_markdown.py
---

# Account

## Overview

- **page_id:** mailhub_account_page
- **page_type:** dashboard
- **codebase:** email
- **surface:** Mailhub
- **era_tags:** 1.x, 11.x
- **flow_id:** mailhub-account
- **_id:** mailhub_account_page-001

### UI components (metadata)

- **UserAccount** — `src/app/account/[userId]/page.tsx`
- **Avatar** — `components/ui/avatar.tsx`
- **Button** — `components/ui/button.tsx`
- **Input** — `components/ui/input.tsx`
- **Label** — `components/ui/label.tsx`
- **Badge** — `components/ui/badge.tsx`
- **Alert** — `components/ui/alert.tsx`
- **SidebarInset** — `components/ui/sidebar.tsx`
- **Icons** — `lucide-react` (Camera, Trash2, Mail, Save, etc.)

## Metadata

- **route:** /account/[userId]
- **file_path:** contact360.io/email/src/app/account/[userId]/page.tsx
- **purpose:** Per-user account/settings surface in Mailhub.
- **s3_key:** data/pages/mailhub_account_page.json
- **status:** published
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **codebase:** email
- **canonical_repo:** contact360.io/email

## Content sections (summary)

### title

Account

### description

User-scoped account route in Mailhub.


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

- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:AccountSettings] > [Q:ProfileSection] + [Q:ConnectionSection] -> {useImap}

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/account`

**Codebase:** `contact360.io/email` (Mailhub client).

**Typical inbound:** Click profile/avatar in sidebar.

**Typical outbound:** [mailhub_home_page.md](mailhub_home_page.md) back to inbox.

**Cross-host:** Hand-off to `app` (Dashboard) for subscription and billing central.
**Backend:** IMAP-proxy REST API; see [emailapp_data_lineage.md](../../backend/database/emailapp_data_lineage.md).



## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [mailhub_auth_login_page](mailhub_auth_login_page.md)
- [mailhub_auth_signup_page](mailhub_auth_signup_page.md)
- [mailhub_draft_page](mailhub_draft_page.md)
- [mailhub_email_detail_page](mailhub_email_detail_page.md)
- [mailhub_home_page](mailhub_home_page.md)
- [mailhub_inbox_page](mailhub_inbox_page.md)
- [mailhub_sent_page](mailhub_sent_page.md)
- [mailhub_spam_page](mailhub_spam_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| context/imap-context.tsx | useImap | Manages global IMAP state and active account selection | 1.x |
| React | use (params) | Unwraps async route parameters | 0.x |
[ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
