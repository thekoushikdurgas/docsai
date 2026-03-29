---
title: "Live Voice"
page_id: live_voice_page
source_json: live_voice_page.json
generator: json_to_markdown.py
---

# Live Voice

## Overview

- **page_id:** live_voice_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 5.x, 11.x
- **flow_id:** live_voice
- **_id:** live_voice_page-001

## Metadata

- **route:** /live-voice
- **file_path:** contact360.io/app/app/(dashboard)/live-voice/page.tsx
- **purpose:** Voice Link Alpha: Low-latency, multimodal AI interaction for real-time lead sentiment analysis and neural transcription.
- **status:** experimental
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None (Alpha access)
- **page_state:** alpha
- **last_updated:** 2026-03-29T00:00:00Z
- **uses_endpoints:** []
### UI components (metadata)

- **LiveVoicePage** — `app/(dashboard)/live-voice/page.tsx`
- **Button** — `components/ui/Button.tsx`
- **Badge** — `components/ui/Badge.tsx`
- **Mic Visualizer** — (Internal animated bars)
- **Transcription Feed** — (Internal list of role-based messages)

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Live Voice

### description

Prototype interface for live voice interactions (Voice Link Alpha) demonstrating microphone control, status, and a mock transcription timeline.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| voice-title | 1 | Voice Link Alpha |
| transcription | 2 | Neural Transcription |


### subheadings

| id | level | text |
| --- | --- | --- |
| alpha-notice | 3 | Experimental Feature — Alpha |


### tabs



### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| request microphone access → start audio stream | LiveVoicePage | start-voice | Start Recording | primary |
| stop audio stream + submit transcript | LiveVoicePage | stop-voice | Stop Recording | danger |
| clear transcription timeline | LiveVoicePage | clear-transcript | Clear | ghost |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| LiveVoicePage | Alpha — Experimental feature | alpha-badge | badge |
| LiveVoicePage | Ready — Click 'Start Recording' to begin | status-idle | status |
| LiveVoicePage | Recording... {elapsedTime} | status-recording | status |
| LiveVoicePage | Neural transcription output stream | transcription-output | result |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- |
| LiveVoicePage | audio-level | Microphone audio level | Real-time audio input level indicator (waveform / volume bar) | indeterminate |


### graphs

| chart_type | component | data_source | id | label |
| --- | --- | --- | --- | --- |
| waveform | LiveVoicePage | Web Audio API (MediaStream) | audio-waveform | Live audio waveform |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| LiveVoicePage | voice-record-flow | Voice recording flow | ["Click 'Start Recording'", 'Browser requests microphone permission', 'Audio stream starts → waveform animation', 'Neural transcription (mock/real) shows text in real-time', "Click 'Stop' → transcript |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/ui/Button.tsx | Button | Start/Stop recording controls |
| components/ui/Badge.tsx | Badge | Alpha label badge |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| (internal) | useState | Manages session active state and transcription history | 5.x |


### services



### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | Session required |


### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| start-voice | Start Recording | primary | request microphone access → start audio stream | LiveVoicePage |
| stop-voice | Stop Recording | danger | stop audio stream + submit transcript | LiveVoicePage |
| clear-transcript | Clear | ghost | clear transcription timeline | LiveVoicePage |


### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| audio-level | Microphone audio level | Real-time audio input level indicator (waveform / volume bar) | indeterminate | LiveVoicePage |


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

## Era coverage (Contact360 0.x–11.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **5.x** — AI workflows — AI chat, live voice, AI email writer product, assistant panels.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H:Header] + [G:VoiceVisualizer] + [B:ActionButton] + [Q:Transcripts] -> {useState}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/live-voice`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [ai_chat_page.md](ai_chat_page.md) (Voice toggle).

**Typical outbound:** Sidebar peers; [ai_chat_page.md](ai_chat_page.md) (Summary handoff); [activities_page.md](activities_page.md) (Recording audit).

**Cross-host:** Voice streams are processed by **email** (Mailhub) for AI-driven response generation based on live sentiment.
**Backend:** Appointment360 GraphQL gateway; low-latency neural transcription and sentiment analysis services.

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
| — | *No `graphql/...` references in this page spec* | — | — |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
