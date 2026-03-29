---
title: "Email detail"
page_id: mailhub_email_detail_page
source_json: mailhub_email_detail_page.json
generator: json_to_markdown.py
---

# Email detail

## Overview

- **page_id:** mailhub_email_detail_page
- **page_type:** dashboard
- **codebase:** email
- **surface:** Mailhub
- **era_tags:** 2.x, 11.x
- **flow_id:** mailhub-email-detail
- **_id:** mailhub_email_detail_page-001

## Metadata

- **route:** /email/[mailId]
- **file_path:** contact360.io/email/src/app/email/[mailId]/page.tsx

### UI components (metadata)

- **EmailPage** — `src/app/email/[mailId]/page.tsx`
- **Spinner** — `components/ui/spinner.tsx`
- **DOMPurify** — `isomorphic-dompurify`
- **MailDetailWrapper** — `inline-tailwindcss` (prose max-w-none)
- **purpose:** Single message view: dynamic route by mailId.
- **s3_key:** data/pages/mailhub_email_detail_page.json
- **status:** published
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **codebase:** email
- **canonical_repo:** contact360.io/email

## Content sections (summary)

### title

Email detail

### description

Read single email in Mailhub.


## UI elements (top-level)

### buttons

[]

### inputs

[]

### checkboxes

[]

### radio_buttons

### radio_buttons

[]

### progress_bars

[]

### toasts

[]


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **2.x** — Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:MailDetail] > [H:Subject] + [Q:MailBody] -> {useImap}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/email/[emailId]`

**Codebase:** `contact360.io/email` (Mailhub client).

**Typical inbound:** Folder list item in [mailhub_inbox_page.md](mailhub_inbox_page.md).

**Typical outbound:** Back to inbox; reply/forward via [mailhub_draft_page.md](mailhub_draft_page.md).

**Cross-host:** Hand-off to `app` (Dashboard) via marketing header.
**Backend:** IMAP-proxy REST API; see [emailapp_data_lineage.md](../../backend/database/emailapp_data_lineage.md).



## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [mailhub_account_page](mailhub_account_page.md)
- [mailhub_auth_login_page](mailhub_auth_login_page.md)
- [mailhub_auth_signup_page](mailhub_auth_signup_page.md)
- [mailhub_draft_page](mailhub_draft_page.md)
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
| context/imap-context.tsx | useImap | Provides active IMAP account credentials for secure fetching | 1.x |
[ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
