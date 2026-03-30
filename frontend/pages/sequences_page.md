---
title: "Sequences"
page_id: sequences_page
source_json: sequences_page.json
generator: json_to_markdown.py
---

# Sequences

## Overview

- **page_id:** sequences_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 10.x, 11.x
- **flow_id:** sequences
- **_id:** sequences_page-001

## Metadata

- **route:** /campaigns/sequences
- **file_path:** contact360.io/app/app/(dashboard)/campaigns/sequences/page.tsx
- **purpose:** Planned multi-step email sequences (drip campaigns): define steps, delays, exit conditions, and link to templates. 10.x email campaign product.
- **s3_key:** data/pages/sequences_page.json
- **status:** planned
- **authentication:** Required
- **authorization:** Plan gated when shipped
- **page_state:** planned
- **last_updated:** 2026-03-29T10:30:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Sequences

### description

Planned: visual sequence builder for drip / nurture flows.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| seq-title | 1 | Sequences |
| builder | 2 | Sequence builder |


### subheadings



### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| navigate to /campaigns/sequences/new | SequencesPage | new-sequence | New sequence | primary |
| append email step + delay | SequenceBuilder | add-step | Add step | secondary |
| sequenceService.UpsertSequence | SequenceBuilder | save-sequence | Save | primary |


### input_boxes

| component | id | label | placeholder | type |
| --- | --- | --- | --- | --- |
| SequenceStep | step-delay | Days after previous step | e.g. 3 | number |
| SequenceBuilder | sequence-name | Sequence name | e.g. Welcome series | text |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| SequenceCard | {n} steps | step-count | caption |


### checkboxes

| component | id | label | purpose |
| --- | --- | --- | --- |
| SequenceBuilder | exit-on-reply | Exit sequence on reply | Stop sequence when recipient replies |


### radio_buttons

| component | id | label | options |
| --- | --- | --- | --- |
| SequenceBuilder | trigger-type | Enrollment trigger | ['Manual list', 'Segment', 'Form submit'] |


### progress_bars



### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| funnel | SequenceStats | campaignAnalyticsService | sequence-funnel | Step funnel (opens / clicks) |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| SequencesPage | sequence-enrollment-flow | Enrollment flow | ['Select contacts or segment', 'Enroll → sequenceService.EnrollContacts', 'Step 1 sends at T+0', 'Subsequent steps send after delay days', 'Exit on reply if enabled'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/campaigns/SequencesPage.tsx | SequencesPage | Planned: list of sequences + builder entry |
| components/features/campaigns/SequenceBuilder.tsx | SequenceBuilder | Planned: ordered steps with delays and template refs |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useSequences.ts | useSequences | Planned: CRUD sequences |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/sequenceService.ts | sequenceService | ['ListSequences', 'UpsertSequence', 'EnrollContacts'] |


### contexts



### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| new-sequence | New sequence | primary | navigate to /campaigns/sequences/new | SequencesPage |
| add-step | Add step | secondary | append email step + delay | SequenceBuilder |
| save-sequence | Save | primary | sequenceService.UpsertSequence | SequenceBuilder |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| step-delay | Days after previous step | number | e.g. 3 | SequenceStep |
| sequence-name | Sequence name | text | e.g. Welcome series | SequenceBuilder |


### checkboxes

| id | label | purpose | component |
| --- | --- | --- | --- |
| exit-on-reply | Exit sequence on reply | Stop sequence when recipient replies | SequenceBuilder |


### radio_buttons

| id | label | options | component |
| --- | --- | --- | --- |
| trigger-type | Enrollment trigger | ['Manual list', 'Segment', 'Form submit'] | SequenceBuilder |


### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useSequences.ts | useSequences | Planned: CRUD sequences |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/sequenceService.ts | sequenceService | ['ListSequences', 'UpsertSequence', 'EnrollContacts'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: sequenceService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useSequences -> sequenceService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–11.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **10.x** — Email campaign — campaigns, sequences, templates, builder (planned routes).
- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > [G:Stats] + [Q:Queue] | [E:Visualizer] — {GQL ListSequences, GetSequence, UpsertSequence}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/campaigns/sequences`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [contacts_page.md](contacts_page.md) (Enroll in sequence).

**Typical outbound:** Sidebar peers; [campaigns_page.md](campaigns_page.md) (campaign association); [campaign_templates_page.md](campaign_templates_page.md).

**Cross-host:** Sequence delivery is handled by **email** (Mailhub) via shared campaign execution workers.
**Backend:** Appointment360 GraphQL gateway; automation engine for drip scheduling and reply tracking.

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
- [settings_page](settings_page.md)
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
