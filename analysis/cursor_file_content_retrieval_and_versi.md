# File content retrieval and version analysis
_Exported on 3/25/2026 at 14:31:44 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Please read and return the content of these files:

1. List ALL files in: d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\ (if folder exists, else confirm missing)
2. If files exist, read 4.0 — Harbor.md (first 80 lines), 4.1 — Auth & Session.md (first 80 lines), README.md (full), any task-pack files (full)

Also read these sections:
3. d:\code\ayan\contact\docs\roadmap.md - find VERSION 4.x section, stage names, status, KPIs, code pointers
4. d:\code\ayan\contact\docs\versions.md - find 4.x entries (4.0.0 through 4.4.0 or similar)

Return all raw content found.

---

**Cursor**


Gathering directory listings and reading the requested files and sections.




Reading `4.0 — Harbor.md` and `4.1 — Auth & Session.md` (first 80 lines), full `README.md`, full task-pack files, and expanded `versions.md` 4.x sections.




Here is everything requested. The folder **exists**.

---

## 1. All files in `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\`

(26 files, absolute paths)

- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\README.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.9 — Extension Reliability.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.8 — Lens.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.7 — Campaign Audience.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.6 — Dashboard Integration.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.5 — Popup UX.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.4 — Extension Telemetry.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.3 — Sync Integrity.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.2 — Harvest.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.10 — Exit Gate.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.1 — Auth & Session.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.0 — Harbor.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\mailvetter-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\appointment360-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\salesnavigator-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\emailcampaign-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\contact-ai-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\jobs-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\connectra-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\emailapis-extension-salesnav-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\logsapi-extension-salesnav-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\s3storage-extension-sn-task-pack.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\extension-telemetry.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\extension-sync-integrity.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\sales-navigator-ingestion.md`
- `d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\extension-auth.md`

---

## 2a. `4.0 — Harbor.md` — first 80 lines (raw)

```1:80:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.0 — Harbor.md
# Version 4.0

- **Status:** planned
- **Target window:** TBD
- **Summary:** AI-assisted workflow maturity. Cross-service execution pack for this minor across contract, service, surface, data, and ops.
- **Scope:** `contact.ai` integration, confidence controls, fallback logic, and prompt governance.
- **Roadmap mapping:** `4.1` to `4.4`
- **Owner:** AI Platform Team

## Scope

- Target minor: `4.0.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["4.0.0 — contact.ai workflows and governance"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v4.0 AI candidate ranking"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["explanation payload path feedback loop"]
    persist --> stabilize["confidence guardrails stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v4.0 contract outcomes for AI candidate ranking; harden request/response schema boundaries in `contact360.io/api` while advancing explanation payload path.
- 🔴 Incompleted: **app**: define v4.0 contract outcomes for AI candidate ranking; align UI payload contracts with backend enums in `contact360.io/app` while advancing explanation payload path.
- 🔴 Incompleted: **jobs**: define v4.0 contract outcomes for AI candidate ranking; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing confidence guardrails.
- 🔴 Incompleted: **sync**: define v4.0 contract outcomes for AI candidate ranking; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing explanation payload path.
- 🔴 Incompleted: **admin**: define v4.0 contract outcomes for AI candidate ranking; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing AI candidate ranking.
- 🔴 Incompleted: **mailvetter**: define v4.0 contract outcomes for AI candidate ranking; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing AI candidate ranking.
- 🔴 Incompleted: **emailapis**: define v4.0 contract outcomes for AI candidate ranking; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing confidence guardrails.
- 🔴 Incompleted: **emailapigo**: define v4.0 contract outcomes for AI candidate ranking; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing AI candidate ranking.

### Service
- 🔴 Incompleted: **api**: deliver v4.0 service outcomes for AI candidate ranking; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing explanation payload path.
- 🔴 Incompleted: **app**: deliver v4.0 service outcomes for AI candidate ranking; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing explanation payload path.
```

---

## 2b. `4.1 — Auth & Session.md` — first 80 lines (raw)

```1:80:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\4.1 — Auth & Session.md
# Version 4.1

- **Status:** planned
- **Era:** 4.x (AI workflows)
- **Summary:** Sub-minor within the 4.x era. Scope is defined when a planned stage is approved and the entry is added to `docs/versions.md`. Cross-service execution pack for this minor across contract, service, surface, data, and ops.

## Scope

- Target minor: `4.1.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["4.1.x placeholder — AI chats REST and streaming slice"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v4.1 explanation payload path"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["confidence guardrails feedback loop"]
    persist --> stabilize["prompt lineage capture stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v4.1 contract outcomes for explanation payload path; harden request/response schema boundaries in `contact360.io/api` while advancing confidence guardrails.
- 🔴 Incompleted: **app**: define v4.1 contract outcomes for explanation payload path; align UI payload contracts with backend enums in `contact360.io/app` while advancing confidence guardrails.
- 🔴 Incompleted: **jobs**: define v4.1 contract outcomes for explanation payload path; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing prompt lineage capture.
- 🔴 Incompleted: **sync**: define v4.1 contract outcomes for explanation payload path; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing confidence guardrails.
- 🔴 Incompleted: **admin**: define v4.1 contract outcomes for explanation payload path; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing explanation payload path.
- 🔴 Incompleted: **mailvetter**: define v4.1 contract outcomes for explanation payload path; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing explanation payload path.
- 🔴 Incompleted: **emailapis**: define v4.1 contract outcomes for explanation payload path; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing prompt lineage capture.
- 🔴 Incompleted: **emailapigo**: define v4.1 contract outcomes for explanation payload path; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing explanation payload path.

### Service
- 🔴 Incompleted: **api**: deliver v4.1 service outcomes for explanation payload path; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing confidence guardrails.
- 🔴 Incompleted: **app**: deliver v4.1 service outcomes for explanation payload path; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing confidence guardrails.
- 🔴 Incompleted: **jobs**: deliver v4.1 service outcomes for explanation payload path; tune queue worker orchestration and idempotent retries in `contact360.io/jobs` while advancing prompt lineage capture.
- 🔴 Incompleted: **sync**: deliver v4.1 service outcomes for explanation payload path; tighten replication loops and conflict-resolution behavior in `contact360.io/sync` while advancing confidence guardrails.
- 🔴 Incompleted: **admin**: deliver v4.1 service outcomes for explanation payload path; harden operator workflows and privilege-aware actions in `contact360.io/admin` while advancing explanation payload path.
```

---

## 2c. `README.md` — full (raw)

```1:26:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\README.md
# 4. Contact360 Extension and Sales Navigator maturity

## Era theme
- See `docs/version-policy.md` and `docs/versions.md` for canonical theme and release mapping for `4.x`.

## Service task-pack files
- `appointment360-extension-sn-task-pack.md`
- `connectra-extension-sn-task-pack.md`
- `contact-ai-extension-sn-task-pack.md`
- `emailapis-extension-salesnav-task-pack.md`
- `emailcampaign-extension-sn-task-pack.md`
- `jobs-extension-sn-task-pack.md`
- `logsapi-extension-salesnav-task-pack.md`
- `mailvetter-extension-sn-task-pack.md`
- `s3storage-extension-sn-task-pack.md`
- `salesnavigator-extension-sn-task-pack.md`

## Operational and supporting docs
- `extension-auth.md`
- `extension-sync-integrity.md`
- `extension-telemetry.md`
- `sales-navigator-ingestion.md`

## Version notes
- Version detail files are stored as `version_<major>.<minor>.md` in this folder and indexed from `docs/versions.md`.
```

---

## 2d. Task-pack files — full (raw)

### `mailvetter-extension-sn-task-pack.md`

```1:31:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\mailvetter-extension-sn-task-pack.md
# Mailvetter — 4.x Extension & Sales Navigator Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `4.x` — Extension and SN maturity integration

## Contract track

- 🔴 Incompleted: Define provenance contract: `source=extension|sales_navigator|dashboard`.
- 🔴 Incompleted: Define idempotency contract for repeated extension verification submits.

## Service track

- 🔴 Incompleted: Add source-tag support in verification payloads and persisted results.
- 🔴 Incompleted: Add anti-abuse safeguards for extension burst traffic.
- 🔴 Incompleted: Add priority queueing policy for interactive extension calls.

## Surface track

- 🔴 Incompleted: Extension: show verification progress and final state badges.
- 🔴 Incompleted: SN import flow: pre-verify selected leads before save/export.

## Data track

- 🔴 Incompleted: Add `source` and `source_session_id` in `results` metadata.
- 🔴 Incompleted: Add dedupe key for repeated verification within short windows.

## Ops track

- 🔴 Incompleted: Add extension-specific rate and error dashboards.
- 🔴 Incompleted: Add source-based abuse detection and alerting.
```

### `appointment360-extension-sn-task-pack.md`

```1:74:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\appointment360-extension-sn-task-pack.md
# Appointment360 (contact360.io/api) — Era 4.x Extension & Sales Navigator Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `LinkedInMutation { upsertByLinkedinUrl, searchLinkedin, exportLinkedinResults }` | P0 |
| Define `SalesNavigatorQuery { salesNavigatorSearch(query) }` | P0 |
| Define `SalesNavigatorMutation { saveSalesNavigatorProfiles, syncSalesNavigator }` | P0 |
| Define `LinkedInProfileType`, `SalesNavigatorResultType` GraphQL output types | P0 |
| Define `LinkedInUpsertInput`, `SalesNavigatorSearchInput` GraphQL input types | P0 |
| Document LinkedIn module in `docs/backend/apis/20_LINKEDIN_MODULE.md` | P1 |
| Document Sales Navigator module in `docs/backend/apis/21_SALES_NAVIGATOR_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `upsertByLinkedinUrl` mutation: call `ConnectraClient.search_by_linkedin_url(url)` then upsert | P0 |
| Implement `searchLinkedin` mutation: call Sales Navigator external service, return profile list | P0 |
| Implement `saveSalesNavigatorProfiles` mutation: bulk upsert to Connectra via `batch_upsert_contacts` | P0 |
| Implement `syncSalesNavigator` mutation: trigger tkdjob sync task | P1 |
| Implement `exportLinkedinResults` mutation: create contact360 export job via tkdjob | P1 |
| Add `sales_navigator_client.py` in `app/clients/` wrapping SN external API | P0 |
| Add credit deduction for Sales Navigator search queries | P0 |
| Add extension session token validation for browser extension requests | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Extension popup → `mutation upsertByLinkedinUrl(url)` to save LinkedIn contact | P0 |
| Extension search results panel → `mutation saveSalesNavigatorProfiles([...])` bulk save | P0 |
| `/contacts` page, LinkedIn import tab → `mutation searchLinkedin` | P0 |
| SN export button in contacts table → `mutation exportLinkedinResults` | P1 |
| `useSalesNavigatorSearch` hook: manage search state, batch save | P0 |
| `useLinkedInSync` hook: extension-to-dashboard sync trigger | P0 |
| Extension badge count (unsaved profiles) synced via `mutation syncSalesNavigator` | P1 |
| Extension auth state: JWT-based auth token validated per extension request | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Contact/company records from LinkedIn upserts stored in Connectra (not appointment360 DB) | P0 |
| Track SN searches in `activities` table: `type=sales_navigator_search`, `metadata.query` | P0 |
| Store extension session tokens in `sessions` table (appointment360 DB) | P1 |
| Deduct credits for each SN search or export operation | P0 |
| Log `source=linkedin` / `source=sales_navigator` on Connectra records | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure Sales Navigator API key in `.env.example` | P0 |
| Ensure `upsertByLinkedinUrl` is rate-limited (abuse guard middleware) | P0 |
| Add SN + extension mutation tests in Postman collection | P1 |
| Write E2E test: extension captures LinkedIn profile → appears in `/contacts` table | P1 |
| Add `X-Extension-Token` header validation middleware or GraphQL guard | P1 |

---

## Email app surface contributions (era sync)

- Email app prepared for extension-parity mailbox ingestion signals and source attribution UX.
- No direct extension runtime in this surface; integration remains API-mediated.
```

### `salesnavigator-extension-sn-task-pack.md` (full file is long; user asked full — I'll include remainder)

Lines 87-110 continuation:

```87:110:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\salesnavigator-extension-sn-task-pack.md
---

## Extension surface contributions (era sync)

### Era 4.x — Extension & Sales Navigator Maturity

**`extension/contact360` full reliability and UX hardening:**
- `utils/lambdaClient.js` — retry with exponential back-off + jitter; adaptive timeout per retry; request queueing
- `auth/graphqlSession.js` — proactive 5-min token refresh buffer for uninterrupted scrape sessions
- `utils/profileMerger.js` — HTML vs deep-scrape variant support; per-field merge with completeness-based tie-breaking

**Extension popup UI contract (to be implemented in popup layer):**
- Progress bar: idle → extracting (20%) → dedup (40%) → saving (60–90%) → done (100%)
- Profile count badge (deduplicated vs raw)
- Error toast for failed batches with retry CTA
- Token status indicator (active / expired)
- Sync status panel (saved / errored counts)

**Tasks:**
- 🔴 Incompleted: Wire `lambdaClient.saveProfiles()` to popup progress bar update events
- 🔴 Incompleted: Implement `SNRetryButton` backed by retry logic in `lambdaClient`
- 🔴 Incompleted: Confirm adaptive timeout values under Lambda cold-start conditions
- 🔴 Incompleted: Test proactive token refresh in long scrape sessions (30+ min)
```

(Full `salesnavigator-extension-sn-task-pack.md` lines 1–86 were already shown in the tool output above — contract through References.)

### `emailcampaign-extension-sn-task-pack.md`

```1:51:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\emailcampaign-extension-sn-task-pack.md
# Email Campaign Service — Era 4.x Task Pack
## Contact360 Extension and Sales Navigator Maturity

### Context
Era `4.x` adds the browser extension and LinkedIn Sales Navigator scraping surface. Contacts sourced from SN or directly enriched via the extension become first-class campaign audience candidates. The campaign service must accept SN-sourced batches, resolve them against suppression lists, and feed them into the wizard.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-4.1 | Define `sn_audience` audience source type: list of LinkedIn URLs → Connectra upsert → segment | Backend |
| A-4.2 | Document enrichment-to-campaign pipeline latency expectations | Backend + Product |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-4.1 | Add `audience_source: "sn_batch"` to `CampaignPayload`; resolve via SN profile→Connectra path | Backend |
| B-4.2 | Pre-campaign enrichment check: verify emails resolved before scheduling (emit warning for missing emails) | Backend |
| B-4.3 | Bulk-upsert SN contacts to Connectra, then use resulting contact IDs as recipient list | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-4.1 | Extension popup: "Add to Campaign" button on a SN profile page; opens campaign selector modal | Frontend (Extension) |
| C-4.2 | Campaign wizard: "From Sales Navigator" audience source option with LinkedIn URL list input | Frontend |
| C-4.3 | Audience step: email-available indicator per SN contact (enrichment status badge) | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-4.1 | Migration: add `sn_profile_batch_id TEXT` to `campaigns` | Backend |
| D-4.2 | Lineage: record SN LinkedIn URL → Connectra contact_id → recipient_id chain | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-4.1 | Rate-limit SN profile upsert calls to Connectra to respect scraper budget | DevOps |

---

## Completion gate
- 🔴 Incompleted: Campaign can be created from a SN LinkedIn URL list.
- 🔴 Incompleted: Contacts without resolved emails are excluded from recipient list with a warning.
- 🔴 Incompleted: "Add to Campaign" CTA visible in extension when viewing SN profile.
```

### `contact-ai-extension-sn-task-pack.md`

```1:45:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\contact-ai-extension-sn-task-pack.md
# Contact AI — 4.x Extension / Sales Navigator Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `4.x` — Extension and Sales Navigator maturity  
**Status:** No new contact.ai endpoints; SN contact objects tested in `messages.contacts` JSONB

---

## Contract track

- 🔴 Incompleted: Confirm no new Contact AI endpoints are introduced in `4.x`.
- 🔴 Incompleted: Validate `messages.contacts[]` JSONB `ContactInMessage` schema is compatible with SN profile objects.
- 🔴 Incompleted: Document SN contact provenance: if needed, add `source` field to `ContactInMessage` (e.g. `"source": "sales_navigator"`).
- 🔴 Incompleted: Confirm extension CSP (Content Security Policy) allows requests to `LAMBDA_AI_API_URL` domain.

## Service track

- 🔴 Incompleted: Test SN contact object fields against `ContactInMessage` schema:
  - `uuid`, `firstName`, `lastName`, `title`, `company`, `email`, `city`, `state`, `country`
- 🔴 Incompleted: Confirm SN contacts stored via `ai_chats.messages` JSONB round-trip without field loss.
- 🔴 Incompleted: Optional: surface AI context panel in extension popup if SN contact is selected and `ENABLE_AI_CHAT=true`.

## Surface track

- 🔴 Incompleted: Optional: add AI context action in extension SN contact flyout: "Open in AI Chat".
- 🔴 Incompleted: If implemented: extension popup sends SN contact data as initial message context to new chat.
- 🔴 Incompleted: Define UX: extension AI panel is optional; main AI chat page (`/app/ai-chat`) remains canonical.

## Data track

- 🔴 Incompleted: Confirm SN contact fields are not PII-leaked to HF/Gemini unless explicitly included in chat message prompt.
- 🔴 Incompleted: Review prompt construction: only include SN contact fields that are explicitly referenced in user query.
- 🔴 Incompleted: Document in `contact_ai_data_lineage.md`: SN contact provenance in `messages.contacts[]` JSONB.

## Ops track

- 🔴 Incompleted: CSP review for extension: add `LAMBDA_AI_API_URL` to allowed `connect-src` origins.
- 🔴 Incompleted: Test extension flow (optional): SN contact → extension popup → AI chat context → message sent → response received.
- 🔴 Incompleted: No new Lambda timeout or memory changes expected in `4.x`.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/frontend/contact-ai-ui-bindings.md`
```

### `jobs-extension-sn-task-pack.md`

```1:24:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\jobs-extension-sn-task-pack.md
# jobs task pack — era 4.x

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define extension-origin/SN provenance fields for jobs metadata.
- Define sync batch contract for extension-driven ingestion flows.

## Service tasks
- Add source tagging and provenance-safe scheduling for extension jobs.
- Harden retry semantics for ingestion batches from extension/SN flows.

## Surface tasks
- Document sync status cards, retry controls, and execution history.
- Map extension-origin job states to user-facing labels.

## Data tasks
- Document provenance lineage (`source`, `workspace`, `channel`) in job payloads.
- Define dedupe/idempotency evidence fields for extension ingests.

## Ops tasks
- Add observability checks for sync lag and retry churn.
- Add rollback/replay playbook for extension ingestion regressions.
```

### `connectra-extension-sn-task-pack.md`

```1:14:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\connectra-extension-sn-task-pack.md
# Connectra extension-SN task pack (`4.x`)

## Scope

Integrate Sales Navigator ingestion into Connectra with idempotent and provenance-safe writes.

## Small tasks

- **Contract:** Define SN-to-Connectra payload contract including provenance/source tags.
- **Service:** Validate SN ingestion adapters call `batch-upsert` idempotently under retries.
- **Database:** Preserve source metadata and conflict-resolution outcomes in PG and ES documents.
- **Flow:** Confirm extension sync flow reaches Connectra with replay-safe dedup keys.
- **Release gate evidence:** Replay tests, provenance filter checks, and conflict resolution diagnostics.
```

### `emailapis-extension-salesnav-task-pack.md`

```1:24:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\emailapis-extension-salesnav-task-pack.md
# emailapis task pack — era 4.x

This pack decomposes lambda/emailapis and lambda/emailapigo work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define and freeze era $(System.Collections.Hashtable.era) email endpoint and payload compatibility notes.
- Update endpoint/reference matrix in docs/backend/endpoints/emailapis_endpoint_era_matrix.json.

## Service tasks
- Implement/validate runtime behavior for era $(System.Collections.Hashtable.era) finder, verifier, pattern, and fallback paths.
- Verify auth, provider routing, error envelope, and health diagnostics behavior.

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era $(System.Collections.Hashtable.era).
- Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio).

## Data tasks
- Document email_finder_cache and email_patterns lineage impact for era $(System.Collections.Hashtable.era).
- Record provider, status, and traceability expectations for this era.

## Ops tasks
- Add observability checks and release validation evidence for era $(System.Collections.Hashtable.era).
- Capture rollback and incident-runbook notes for email-impacting releases.
```

### `logsapi-extension-salesnav-task-pack.md`

```1:24:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\logsapi-extension-salesnav-task-pack.md
# logs.api task pack — era 4.x

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define and freeze era `4.x` logging schema additions and compatibility notes.
- Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.

## Service tasks
- Implement/validate service behavior for era `4.x` event sources and query expectations.
- Verify auth, error envelope, and health behavior for consuming services.

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era `4.x`.
- Document relevant hooks/services/contexts and UX states (loading/error/progress/check/radio).

## Data tasks
- Document S3 CSV storage and lineage impact for era `4.x`.
- Record retention, trace IDs, and query-window expectations.

## Ops tasks
- Add observability checks and release validation evidence for era `4.x`.
- Capture rollback and incident-runbook notes for logging-impacting releases.
```

### `s3storage-extension-sn-task-pack.md`

```1:21:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\s3storage-extension-sn-task-pack.md
# `s3storage` Task Pack - Era `4.x.x`

## Scope
- Extension and Sales Navigator artifact handling
- Channel-safe access and provenance

## Small tasks
- Contract:
  - define extension-origin upload policy and URL TTL boundaries
  - define channel provenance metadata fields
- Service:
  - enforce channel-aware access restrictions on storage endpoints
  - support extension-specific object prefix controls
- Database/Data lineage:
  - persist provenance tags for extension and SN ingestion artifacts
- Flow/Graph:
  - extension sync flow: capture -> upload -> process -> telemetry correlation
- Release gate evidence:
  - extension channel reliability metrics
  - provenance field validation across sampled records
```

**Full middle of `salesnavigator-extension-sn-task-pack.md` (lines 1–86)** — included in the Read output above; omitted here only where redundant with the read tool output you already have in full in this message’s earlier block (lines 1–86 match the tool result exactly).

To be complete, here is **lines 1–86** of `salesnavigator-extension-sn-task-pack.md`:

```1:86:d:\code\ayan\contact\docs\4. Contact360 Extension and Sales Navigator maturity\salesnavigator-extension-sn-task-pack.md
# Sales Navigator — 4.x Extension & Sales Navigator Maturity Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `4.x` — Contact360 Extension and Sales Navigator Maturity  
**Status:** PRIMARY DELIVERY ERA — full feature complete

---

## Contract track

- 🔴 Incompleted: Lock final API contract for `POST /v1/save-profiles` and `POST /v1/scrape`
- 🔴 Incompleted: Fix documentation drift: remove `POST /v1/scrape-html-with-fetch` from `docs/api.md` (not implemented) OR implement it
- 🔴 Incompleted: Clarify `POST /v1/scrape` active status in `README.md` (README incorrectly states scraping is removed)
- 🔴 Incompleted: Define error response structure: `{success: false, errors: [{profile_url, message}]}`
- 🔴 Incompleted: Define partial-success semantics: `saved_count > 0` with non-empty `errors[]` is valid
- 🔴 Incompleted: Lock `ScrapeHtmlRequest` max HTML size (10 MB) as tested and documented
- 🔴 Incompleted: Freeze `SaveProfilesRequest` max profiles (1000) with rejection behavior documented

## Service track

- 🔴 Incompleted: Harden HTML extraction across multiple SN DOM variants:
  - 🔴 Incompleted: Standard search results page
  - 🔴 Incompleted: Account map view
  - 🔴 Incompleted: People tab on company page
- 🔴 Incompleted: Optimize extraction for 25-profile search result pages (primary extension use case)
- 🔴 Incompleted: Validate deduplication correctness: same `profile_url` → single record, best-completeness kept
- 🔴 Incompleted: Fix `convert_sales_nav_url_to_linkedin()` coverage — document when PLACEHOLDER is returned
- 🔴 Incompleted: Implement extraction fallback for missing fields (graceful null, not error)
- 🔴 Incompleted: Add `X-Request-ID` correlation header to all responses
- 🔴 Incompleted: Test chunk boundary behavior: exactly 500, 501, 1000 profiles

## Surface track

### Extension popup UI (primary deliverable)

- 🔴 Incompleted: `SNSaveButton` — "Save to Contact360" button with loading state
- 🔴 Incompleted: `SNSyncCTA` — "Sync Page" button (scrape + save)
- 🔴 Incompleted: `SNProfileCountBadge` — "25 profiles found"
- 🔴 Incompleted: `SNSaveProgress` — progress bar: idle → extracting (20%) → dedup (40%) → saving (60–90%) → done (100%)
- 🔴 Incompleted: `SNSaveSummaryCard` — shows saved count, created/updated split
- 🔴 Incompleted: `SNErrorToast` — quick error notification
- 🔴 Incompleted: `SNErrorDrawer` — detailed failed profiles list with reason
- 🔴 Incompleted: `SNRetryButton` — retry after partial failure
- 🔴 Incompleted: `DataQualityBadge` — per-profile quality indicator (green/yellow/red)
- 🔴 Incompleted: `AlreadySavedBadge` — show if profile UUID already in Contact360
- 🔴 Incompleted: `ProfileCheckbox` + `ProfileSelectAll` — selective save
- 🔴 Incompleted: `ConnectionDegreeBadge` — 1st/2nd/3rd degree indicator

### Dashboard SN panel

- 🔴 Incompleted: `SNIngestionPanel` — `/contacts/import` tab with SN section
- 🔴 Incompleted: `SNSyncHistoryTable` — past SN sync sessions with stats
- 🔴 Incompleted: `SNIngestionStatsCard` — saved count, quality average, error rate
- 🔴 Incompleted: `SNSourceFilterChip` — filter contacts by `source=sales_navigator`

## Data track

- 🔴 Incompleted: Confirm provenance fields written per profile: `lead_id`, `search_id`, `data_quality_score`, `connection_degree`, `recently_hired`, `is_premium`
- 🔴 Incompleted: Add `source="sales_navigator"` tag on all contacts from this service
- 🔴 Incompleted: Validate `data_quality_score` computation accuracy (70% required + 30% optional weighted)
- 🔴 Incompleted: Dedup evidence: log `duplicate_count` per save session

## Ops track

- 🔴 Incompleted: P95 latency target: `save-profiles` for 25 profiles < 3s; for 100 profiles < 5s
- 🔴 Incompleted: CloudWatch alarm: `save-profiles` Lambda timeout rate > 1%
- 🔴 Incompleted: Lambda timeout tuning: current 60s sufficient for 1000 profiles; confirm under load
- 🔴 Incompleted: Test: 1000-profile batch end-to-end in staging
- 🔴 Incompleted: Deploy via SAM to staging + production
- 🔴 Incompleted: Extension CSP check: confirm Lambda API domain is allowed in extension manifest

---

**P0 action items (must complete before release):**

1. Fix doc drift: `scrape-html-with-fetch` in `docs/api.md`
2. Fix README scraping ambiguity
3. Add `X-Request-ID` correlation header

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- `docs/frontend/salesnavigator-ui-bindings.md`
- `docs/backend/database/salesnavigator_data_lineage.md`

---

```

(Plus lines 87–110 as cited earlier.)

---

## 3. `roadmap.md` — VERSION 4.x section (raw)

**Primary heading (stages 4.1–4.4)** — from `d:\code\ayan\contact\docs\roadmap.md`:

```257:300:d:\code\ayan\contact\docs\roadmap.md
## VERSION 4.x — Extension and Sales Navigator Maturity

### Stage 4.1 - Extension auth/session hardening

**Status:** Planned  
**Depends on:** Appointment360 auth contracts  
**Risk:** Session expiry and token refresh failures in browser context  
**Definition of done:** Stable authenticated extension session lifecycle  
**KPI:** Extension auth failure rate  
**Ships in:** `4.0.0`

---

### Stage 4.2 - Sales Navigator ingestion optimization

**Status:** Planned  
**Depends on:** Stage 4.1 and `salesnavigator` backend updates  
**Risk:** Source-side data variability  
**Definition of done:** Ingestion accuracy and throughput targets are met  
**KPI:** Records ingested per run, ingestion error rate  
**Ships in:** `4.0.0`

---

### Stage 4.3 - Sync integrity and conflict handling

**Status:** Planned  
**Depends on:** Stages 4.1, 4.2  
**Risk:** Duplicate writes and state divergence  
**Definition of done:** Deterministic sync conflict handling is in place  
**KPI:** Sync conflict auto-resolution success rate  
**Ships in:** `4.0.0`

---

### Stage 4.4 - Extension telemetry and reliability

**Status:** Planned  
**Depends on:** Stage 4.3 and `logs.api` integration  
**Risk:** Limited visibility into extension production failures  
**Definition of done:** Extension telemetry and error observability are production-ready  
**KPI:** Error triage time and telemetry coverage  
**Ships in:** `4.0.0`

---
```

**Code / product pointers implied in that block**

- **Depends on:** `Appointment360 auth contracts`; **`salesnavigator`** backend; **`logs.api`** integration.

**Related roadmap bullets (migration `3.x` → `4.x`)** at `d:\code\ayan\contact\docs\roadmap.md`:

```879:896:d:\code\ayan\contact\docs\roadmap.md
### `3.x` → `4.x` (Contact/company data → Extension)

- **3.1 VQL/filters**
  - Freeze filter taxonomy and validate VQL-to-ES query translation.
  - Add performance regression tests for complex filter queries.
- **3.2 Enrichment/dedupe**
  - Tune merge-on-conflict rules and deterministic UUID assignment.
  - Add deduplication quality metrics to observability.
- **3.3 Search quality**
  - Tune index refresh cycle and relevance scoring.
  - Validate P95 latency targets against SLO.
- **3.4 Search UX**
  - Build advanced filter UI with saved-search capability.
  - Add company drill-down and search-to-export conversion tracking.
- **4.1–4.4 Extension**
  - Harden token refresh and session expiry handling in extension context.
  - Validate SN ingestion pipeline with dedup and conflict resolution.
  - Add telemetry error shipping to logs.api and ingestion status UX.
```

**`4.x` extension maturity under `s3storage` cross-era** (same file):

```1013:1016:d:\code\ayan\contact\docs\roadmap.md
### `4.x` extension maturity
- Contract: extension-safe storage policies and URL lifetimes.
- Service: channel-aware access and provenance markers.
- Data/Ops: extension upload reliability telemetry.
```

**`logs.api` cross-era** line for `4.x`:

```1067:1067:d:\code\ayan\contact\docs\roadmap.md
- `4.x`: extension and SN ingestion telemetry provenance.
```

**`jobs` cross-era** line for `4.x`:

```1083:1083:d:\code\ayan\contact\docs\roadmap.md
- `4.x`: extension/SN provenance and sync jobs.
```

**`contact.ai` cross-era** line for `4.x`:

```1111:1111:d:\code\ayan\contact\docs\roadmap.md
- `4.x`: SN contact object compatibility in `messages.contacts[]` JSONB; extension CSP.
```

---

## 4. `versions.md` — 4.x entries (raw)

**Release index row:**

```31:31:d:\code\ayan\contact\docs\versions.md
| `4.0.0` | planned | TBD | Extension and Sales Navigator maturity era |
```

**Release entries `4.0.0`–`4.4.0`:**

```194:237:d:\code\ayan\contact\docs\versions.md
### `4.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension and Sales Navigator maturity era.
- **Scope:** Extension auth/session hardening, ingestion stability, sync integrity, and telemetry.
- **Roadmap mapping:** `4.1` to `4.4`
- **Owner:** Extension + Integrations Engineering

### `4.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension auth and session hardening.
- **Scope:** Token refresh, session lifecycle, and stable authenticated extension state.
- **Roadmap mapping:** `4.1`
- **Owner:** Extension Engineering

### `4.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Sales Navigator ingestion optimization.
- **Scope:** Ingestion accuracy and throughput against Sales Navigator source data.
- **Roadmap mapping:** `4.2`
- **Owner:** Sales Navigator Engineering

### `4.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Sync integrity and conflict handling.
- **Scope:** Deterministic conflict resolution and idempotent sync.
- **Roadmap mapping:** `4.3`
- **Owner:** Extension + Data Engineering

### `4.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Extension telemetry and reliability.
- **Scope:** Error shipping to logs.api and ingestion status UX.
- **Roadmap mapping:** `4.4`
- **Owner:** Extension Engineering + Platform
```

---

**Note:** `4.0 — Harbor.md` and `4.1 — Auth & Session.md` in the Extension/SN folder currently describe **AI / `contact.ai`** themes and “AI workflows,” which conflicts with `docs/versions.md` and `README.md` for era **4.x** (extension + SN). `emailapis-extension-salesnav-task-pack.md` contains the literal placeholder `$(System.Collections.Hashtable.era)` instead of `4.x`.

