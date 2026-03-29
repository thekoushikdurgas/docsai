---
title: "Finder"
page_id: finder_page
source_json: finder_page.json
generator: json_to_markdown.py
---

# Finder [ARCHIVED]

> [!IMPORTANT]
> This page is **ARCHIVED**. All Email Finder functionality (Single Search, Bulk Upload, Mapping) has been consolidated into the [email_page.md](email_page.md) under the **Finder** tab.

## Overview

- **page_id:** finder_page
- **page_type:** dashboard (alias)
- **codebase:** app
- **surface:** app
- **era_tags:** 2.x, 10.x
- **flow_id:** finder
- **_id:** finder_page-001

## Metadata

- **route:** /email
- **file_path:** contact360.io/app/app/(dashboard)/email/page.tsx
- **purpose:** Legacy spec for Finder. Now part of [email_page.md](email_page.md).
- **status:** archived
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2025-01-27T12:00:00.000000+00:00
### uses_endpoints (2)

- `graphql/FindSingleEmail` — Get a single email address for a contact using first name, last name, and company domain. Main API call for Email Finder functionality.
- `graphql/VerifyAndFind` — Verify and find the first valid email with verification. Alternative endpoint for enhanced email finding.

### UI components (metadata)

- **FinderSingleSearch** — `components/features/finder/FinderSingleSearch.tsx`
- **FinderBulkUpload** — `components/features/finder/FinderBulkUpload.tsx`
- **FinderMappingModal** — `components/features/finder/FinderMappingModal.tsx`

- **versions:** []
- **endpoint_count:** 2
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Finder

### description

Finder tab on Email page: find email addresses from names/domains. Superseded by email_page. Route /finder does not exist; use /email with Finder tab.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| finder-title | 1 | Email Finder |
| finder-subtitle | 2 | Find a verified email |
| result-title | 2 | Verified Contact Found |
| history-title | 2 | Recent Searches |


### subheadings

| id | level | text |
| --- | --- | --- |
| sidebar-credits | 3 | Credits Remaining |
| empty-state | 3 | No recent searches |


### tabs

| content_ref | id | label |
| --- | --- | --- |
| finder-single-search | single | Single Search |
| finder-bulk-upload | bulk | Bulk Upload |


### buttons

| action | component | icon | id | label | loading_state | type | visibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| emailService.FindSingleEmail | FinderSingleSearch |  | find-email | Find Verified Email | Searching Database... | primary |  |
| clipboard.copyToClipboard(email) | FinderSingleSearch | Copy | copy-email-result | Copy |  | icon |  |
| open file picker | FinderBulkUpload |  | bulk-upload-btn | Upload CSV |  | secondary |  |
| emailService.FindEmailsBulk | FinderBulkUpload |  | bulk-find-submit | Find Emails in Bulk |  | primary |  |
| navigate to /billing | SidebarCreditsWidget |  | upgrade-plan | Upgrade Plan |  | primary | low credits |


### input_boxes

| accept | component | icon | id | label | placeholder | required | type |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | FinderSingleSearch | User | first-name | First Name | e.g. Sarah | True | text |
|  | FinderSingleSearch | User | last-name | Last Name | e.g. Connor | True | text |
|  | FinderSingleSearch | Building2 | company-domain | Company Domain | e.g. skynet.com | True | text |
| .csv | FinderBulkUpload |  | bulk-csv | CSV file |  | True | file |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| FinderSingleSearch | Name: {firstName} {lastName} | result-name | result |
| FinderSingleSearch | Company Domain: {domain} | result-domain | result |
| FinderSingleSearch | Email Address: {email} | result-email | result |
| FinderSingleSearch | Confidence: {confidence}% | result-confidence | result |
| FinderSingleSearch | Your search results will appear here. | empty-description | empty-state |
| SidebarCreditsWidget | {credits} credits remaining | credits-remaining | stat |
| NA | This page spec is archived. See email_page.json for current implementation (Finder tab). | archived-notice | info |


### checkboxes



### radio_buttons



### progress_bars

| color_logic | component | id | label | purpose | type |
| --- | --- | --- | --- | --- | --- |
| green > 70%, amber 40-70%, red < 40% | FinderSingleSearch | confidence-bar | Email confidence score | 0–100% confidence that found email is accurate | determinate |


### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| FinderSingleSearch | single-find-flow | Single email find flow | ['Enter first name, last name, company domain', "Click 'Find Verified Email'", 'emailService.FindSingleEmail MUTATION', 'Credit deducted', 'Result card appears with email + confidence bar', 'Copy butt |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/finder/FinderSingleSearch.tsx | FinderSingleSearch | 3-field form + result card with confidence bar + copy button |
| components/features/finder/FinderBulkUpload.tsx | FinderBulkUpload | CSV file upload + column mapping for bulk email finding |
| components/features/finder/FinderMappingModal.tsx | FinderMappingModal | Map CSV columns to first name, last name, domain fields |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useEmailFinderSingle.ts | useFinder | Form state, validation, FindSingleEmail mutation |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/emailService.ts | emailService | ['FindSingleEmail', 'VerifyAndFind', 'FindEmailsBulk'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | Credit check before submit |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy found email to clipboard |
| lib/email/emailValidation.ts | emailValidation | Validate domain format, name fields |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useFinder | MUTATION | FindSingleEmail | emailService |
| useFinder | MUTATION | VerifyAndFind | emailService |


## UI elements (top-level)

### buttons

| id | label | type | action | loading_state | component |
| --- | --- | --- | --- | --- | --- |
| find-email | Find Verified Email | primary | emailService.FindSingleEmail | Searching Database... | FinderSingleSearch |
| copy-email-result | Copy | icon | clipboard.copyToClipboard(email) |  | FinderSingleSearch |
| bulk-upload-btn | Upload CSV | secondary | open file picker |  | FinderBulkUpload |
| bulk-find-submit | Find Emails in Bulk | primary | emailService.FindEmailsBulk |  | FinderBulkUpload |
| upgrade-plan | Upgrade Plan | primary | navigate to /billing |  | SidebarCreditsWidget |


### inputs

| id | label | type | placeholder | required | icon | component |
| --- | --- | --- | --- | --- | --- | --- |
| first-name | First Name | text | e.g. Sarah | True | User | FinderSingleSearch |
| last-name | Last Name | text | e.g. Connor | True | User | FinderSingleSearch |
| company-domain | Company Domain | text | e.g. skynet.com | True | Building2 | FinderSingleSearch |
| bulk-csv | CSV file | file |  | True |  | FinderBulkUpload |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | color_logic | component |
| --- | --- | --- | --- | --- | --- |
| confidence-bar | Email confidence score | 0–100% confidence that found email is accurate | determinate | green > 70%, amber 40-70%, red < 40% | FinderSingleSearch |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useEmailFinderSingle.ts | useFinder | Form state, validation, FindSingleEmail mutation |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/emailService.ts | emailService | ['FindSingleEmail', 'VerifyAndFind', 'FindEmailsBulk'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/FindSingleEmail, graphql/VerifyAndFind | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: emailService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useFinder -> emailService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–11.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **2.x** — Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.
- **11.x** — Legacy — functionality consolidated into /email surface.
- **Status** — Archived spec; prefer [email_page.md](email_page.md) for live `/email` UX.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [Redirect] -> [email_page.md](email_page.md) (Finder Tab)
SingleEmail, VerifyAndFind}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/email` (Finder tab)

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions.

**Typical outbound:** Sidebar peers; [contacts_page.md](contacts_page.md) (save result); [billing_page.md](billing_page.md) (credits).

**Cross-host:** Lead data discovered here is shared with **email** (Mailhub) for direct outreach.
**Backend:** Appointment360 GraphQL gateway; waterfall email discovery and verification services.

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
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `FindSingleEmail` | [mutation_find_single_email_graphql.md](../../backend/endpoints/mutation_find_single_email_graphql.md) | MUTATION | 2.x |
| `VerifyAndFind` | [mutation_verify_and_find_graphql.md](../../backend/endpoints/mutation_verify_and_find_graphql.md) | MUTATION | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
