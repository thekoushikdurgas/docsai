---
title: "Verifier"
page_id: verifier_page
source_json: verifier_page.json
generator: json_to_markdown.py
---

# Verifier [ARCHIVED]

> [!IMPORTANT]
> This page is **ARCHIVED**. All Email Verification functionality (Single, Bulk, Risk Analysis) has been consolidated into the [email_page.md](email_page.md) under the **Verifier** tab.

## Overview

- **page_id:** verifier_page
- **page_type:** dashboard (alias)
- **codebase:** app
- **surface:** app
- **era_tags:** 2.x, 10.x
- **flow_id:** verifier
- **_id:** verifier_page-001

## Metadata

- **route:** /email
- **file_path:** contact360.io/app/app/(dashboard)/email/page.tsx
- **purpose:** [ARCHIVED] Legacy Verifier view. Consolidated into 'Marketing Studio > Verifier'.
- **status:** archived
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
### uses_endpoints (3)

- `graphql/VerifySingleEmail` — Verify a single email address for validity and risk
- `graphql/VerifyBulkEmails` — Verify multiple email addresses in bulk
- `graphql/GetActivities` — Get verification activity history

### UI components (metadata)

- **VerifierHeader** — `components/features/verifier/VerifierHeader.tsx`
- **VerifierTabNavigation** — `components/features/verifier/VerifierTabNavigation.tsx`
- **VerifierBulkTab** — `components/features/verifier/VerifierBulkTab.tsx`
- **VerifierEmailTab** — `components/features/verifier/VerifierEmailTab.tsx`
- **VerifierManagementTab** — `components/features/verifier/VerifierManagementTab.tsx`
- **VerifierHistoryTab** — `components/features/verifier/VerifierHistoryTab.tsx`

- **versions:** []
- **endpoint_count:** 3
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Verifier

### description

Verifier tab on Email page: bulk and single email verification, management, history. Superseded by email_page. Route /verifier does not exist; use /email with Verifier tab.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| verifier-title | 1 | Email Verifier |
| bulk-title | 2 | Bulk Verification |
| single-title | 2 | Single Email Verification |
| history-title | 2 | Verification History |
| manage-title | 2 | Manage Verification Lists |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| verifier-single-tab | single | Single Email |
| verifier-bulk-tab | bulk | Bulk Verify |
| verifier-management-tab | management | Management |
| verifier-history-tab | history | History |


### buttons

| action | component | id | label | loading_state | tab | type |
| --- | --- | --- | --- | --- | --- | --- |
| emailService.VerifySingleEmail | VerifierEmailTab | verify-single | Verify Email | Verifying... | single | primary |
| file input → VerifierBulkTab | VerifierBulkTab | bulk-upload | Upload CSV |  | bulk | secondary |
| emailService.VerifyBulkEmails | VerifierBulkTab | bulk-submit | Verify All |  | bulk | primary |
| download CSV of results | VerifierBulkTab | download-bulk-results | Download Results |  | bulk | secondary |


### input_boxes

- **[0]**
  - **id:** single-email
  - **label:** Email address
  - **type:** email
  - **placeholder:** email@company.com
  - **required:** True
  - **validation:** RFC 5322 format
  - **component:** VerifierEmailTab
  - **tab:** single

- **[1]**
  - **id:** bulk-csv
  - **label:** CSV file
  - **type:** file
  - **accept:** .csv
  - **required:** True
  - **component:** VerifierBulkTab
  - **tab:** bulk



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| VerifierEmailTab | Valid — deliverable email address | status-valid | success |
| VerifierEmailTab | Invalid — email does not exist | status-invalid | error |
| VerifierEmailTab | Catchall — domain accepts all mail, cannot verify | status-catchall | warning |
| VerifierEmailTab | Risky — may bounce or be a spam trap | status-risky | warning |
| NA | Archived. This spec predates email_page.json — see email_page Verifier tab for current implementation. | archived-notice | info |


### checkboxes



### radio_buttons



### progress_bars

| color_logic | component | id | label | purpose | type |
| --- | --- | --- | --- | --- | --- |
| green valid, amber catchall/risky, red invalid | VerifierEmailTab | deliverability-bar | Deliverability confidence | 0–100% confidence in email deliverability | determinate |
|  | VerifierBulkTab | bulk-progress-bar | Bulk verification progress | Rows verified / total rows | determinate |


### graphs

| chart_type | component | data_source | id | label | segments |
| --- | --- | --- | --- | --- | --- |
| stacked_bar | VerifierBulkTab | emailService.VerifyBulkEmails | bulk-result-breakdown | Verification results breakdown | ['valid', 'invalid', 'catchall', 'risky', 'unknown'] |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| VerifierEmailTab | single-verify-flow | Single email verification flow | ['Enter email address', "Click 'Verify Email'", 'emailService.VerifySingleEmail MUTATION', 'Credit deducted', 'Status badge: valid / invalid / catchall / risky', 'Deliverability confidence bar'] |
| VerifierBulkTab | bulk-verify-flow | Bulk verification flow | ['Upload CSV', 'Map email column', 'Submit → emailService.VerifyBulkEmails', 'Progress bar updates', 'Results breakdown chart: valid/invalid/catchall', 'Download CSV with status column'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/verifier/VerifierHeader.tsx | VerifierHeader | Page title + usage counter |
| components/features/verifier/VerifierTabNavigation.tsx | VerifierTabNavigation | Single / Bulk / Management / History tabs |
| components/features/verifier/VerifierEmailTab.tsx | VerifierEmailTab | Single email input + status badge + deliverability bar |
| components/features/verifier/VerifierBulkTab.tsx | VerifierBulkTab | CSV upload + progress bar + results stacked bar |
| components/features/verifier/VerifierManagementTab.tsx | VerifierManagementTab | Manage saved verification lists |
| components/features/verifier/VerifierHistoryTab.tsx | VerifierHistoryTab | History of past verifications with filter |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useEmailVerifierSingle.ts | useVerifier | Single verify form state + VerifySingleEmail mutation |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/emailService.ts | emailService | ['VerifySingleEmail', 'VerifyBulkEmails'] |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | Credit deduction gating |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/email/emailValidation.ts | emailValidation | validateEmailInput for single verify |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useVerifier | MUTATION | VerifySingleEmail | emailService |
| useVerifier | MUTATION | VerifyBulkEmails | emailService |
| useVerifier | QUERY | GetActivities | activitiesService |


## UI elements (top-level)

### buttons

| id | label | type | action | loading_state | component | tab |
| --- | --- | --- | --- | --- | --- | --- |
| verify-single | Verify Email | primary | emailService.VerifySingleEmail | Verifying... | VerifierEmailTab | single |
| bulk-upload | Upload CSV | secondary | file input → VerifierBulkTab |  | VerifierBulkTab | bulk |
| bulk-submit | Verify All | primary | emailService.VerifyBulkEmails |  | VerifierBulkTab | bulk |
| download-bulk-results | Download Results | secondary | download CSV of results |  | VerifierBulkTab | bulk |


### inputs

| id | label | type | placeholder | required | validation | component | tab |
| --- | --- | --- | --- | --- | --- | --- | --- |
| single-email | Email address | email | email@company.com | True | RFC 5322 format | VerifierEmailTab | single |
| bulk-csv | CSV file | file |  | True |  | VerifierBulkTab | bulk |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | color_logic | component |
| --- | --- | --- | --- | --- | --- |
| deliverability-bar | Deliverability confidence | 0–100% confidence in email deliverability | determinate | green valid, amber catchall/risky, red invalid | VerifierEmailTab |
| bulk-progress-bar | Bulk verification progress | Rows verified / total rows | determinate |  | VerifierBulkTab |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useEmailVerifierSingle.ts | useVerifier | Single verify form state + VerifySingleEmail mutation |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/emailService.ts | emailService | ['VerifySingleEmail', 'VerifyBulkEmails'] |
| services/graphql/activitiesService.ts | activitiesService | ['GetActivities'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/VerifySingleEmail, graphql/VerifyBulkEmails, graphql/GetActivities | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: emailService, activitiesService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useVerifier -> emailService, activitiesService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **2.x** — Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.
- **Status** — Archived spec; prefer [email_page.md](email_page.md) for live `/email` UX.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/email`

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
- [settings_page](settings_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `VerifySingleEmail` | [mutation_verify_single_email_graphql.md](../../backend/endpoints/mutation_verify_single_email_graphql.md) | MUTATION | 2.x |
| `VerifyBulkEmails` | [mutation_verify_bulk_emails_graphql.md](../../backend/endpoints/mutation_verify_bulk_emails_graphql.md) | MUTATION | 2.x |
| `GetActivities` | [get_activities_graphql.md](../../backend/endpoints/get_activities_graphql.md) | QUERY | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
