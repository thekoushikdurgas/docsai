# Documentation folder exploration
_Exported on 3/26/2026 at 19:28:28 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Explore the docs folder at d:\code\ayan\contact\docs and provide:
1. The complete folder/file tree (all subdirectories and files)
2. Read the first 50 lines of each of these files:
   - d:\code\ayan\contact\docs\architecture.md
   - d:\code\ayan\contact\docs\versions.md
   - d:\code\ayan\contact\docs\roadmap.md
   - d:\code\ayan\contact\docs\governance.md
   - d:\code\ayan\contact\docs\frontend.md
   - d:\code\ayan\contact\docs\codebase.md
   - d:\code\ayan\contact\docs\backend.md
   - d:\code\ayan\contact\docs\flowchart.md
   - d:\code\ayan\contact\docs\version-policy.md
   - d:\code\ayan\contact\docs\docsai-sync.md
   - d:\code\ayan\contact\docs\audit-compliance.md
3. List all files in docs/analysis/, docs/plans/, docs/ideas/, docs/codebases/, docs/frontend/, docs/backend/
Return all findings clearly.

---

**Cursor**


Gathering the docs tree, reading the first 50 lines of the listed files, and listing files in the requested subfolders.




Tree output was empty. Collecting a full file list via glob and rechecking the tree.




Gathering top-level structure and subtree summaries because `tree` produced no output and the full glob exceeds 6,400 files.




Building the tree by listing each top-level subtree:




Here is a concise report of what’s under `d:\code\ayan\contact\docs`.

---

## 1. Folder / file tree (overview)

A recursive glob over `d:\code\ayan\contact\docs` reports **6,439 files** total (this includes **`d:\code\ayan\contact\docs\.git`** and large nested trees such as **`docs\ideas\`** and **`docs\backend\postman\`**). Running `tree /F` in this environment returned no visible output, so the layout below is summarized from targeted globs and reads.

**High-level layout**

```
d:\code\ayan\contact\docs\
├── .git\                          (nested Git metadata for the docs tree)
│
├── Canonical top-level Markdown (examples; not exhaustive)
│   architecture.md, roadmap.md, versions.md, governance.md, frontend.md,
│   codebase.md, backend.md, flowchart.md, version-policy.md, docsai-sync.md,
│   audit-compliance.md, …
│
├── analysis\                      (41 × *.md — Cursor analysis exports)
├── plans\                         (28 × *.plan.md)
├── codebases\                     (16 × *.md + README)
├── frontend\
│   ├── docs\                      (*.md — components, design system, bindings, …)
│   ├── excel\                     (*.csv — page exports)
│   └── pages\                     (*.json — page specs, index)
├── backend\
│   ├── apis\                      (38 files — module + era task-pack docs)
│   ├── database\                  (55 files — lineage, migrations, tables\, table_data\)
│   ├── endpoints\                 (197 × *.json — endpoint specs + era matrices)
│   └── postman\                   (3,138 files — collections incl. third-party API mirrors)
├── ideas\                         (2,529 files — README + nested experiments/clones:
│                                  admin\, api\, app\, job\, jobs\, mailvetter\, resume\,
│                                  root\, s3storage\, sync\, …; includes .git, .ssh, .docker, source)
│
└── Era numbered folders (0.x–10.x) — version docs + task packs + checklists
    ├── 0. Foundation and pre-product stabilization and codebase setup\     (23 files)
    ├── 1. Contact360 user and billing and credit system\                    (23 files)
    ├── 2. Contact360 email system\                                          (24 files)
    ├── 3. Contact360 contact and company data system\                       (27 files)
    ├── 4. Contact360 Extension and Sales Navigator maturity\                (27 files)
    ├── 5. Contact360 AI workflows\                                          (24 files)
    ├── 6. Contact360 Reliability and Scaling\                               (26 files)
    ├── 7. Contact360 deployment\                                          (26 files)
    ├── 8. Contact360 public and private apis and endpoints\                 (27 files)
    ├── 9. Contact360 Ecosystem integrations and Platform productization\    (26 files)
    └── 10. Contact360 email campaign\                                       (28 files)
```

**Counts (from workspace globs)**

| Area | Approx. files |
|------|----------------|
| Entire `docs\` | **6,439** |
| `docs\backend\postman\` | **3,138** |
| `docs\ideas\` | **2,529** |
| `docs\backend\endpoints\` | **197** |
| `docs\*.md` (recursive) | **877** |
| `docs\*.json` (recursive) | **3,314** (mostly backend + frontend pages) |

A **literal line-by-line tree of all 6,439 paths** is not inlined here; the two largest branches are **`docs\backend\postman\`** and **`docs\ideas\`**.

---

## 2. First 50 lines of each requested file

```1:50:d:\code\ayan\contact\docs\architecture.md
# Contact360 Architecture

## Overview

**Contact360** is a B2B SaaS platform focused on email discovery and verification. The system uses a Next.js dashboard, a Django DocsAI admin/docs surface, a FastAPI GraphQL gateway (`appointment360`), and multiple backend services for search, verification, AI, scheduling, logging, and file storage.

---

## Repository layout (this monorepo)

Product UI, the GraphQL gateway, Connectra, and the job scheduler live under **`contact360.io/`**. Shared email/log/storage microservices often live under **`lambda/`**. Additional backend checkouts in this workspace use **`backend(dev)/`** (AI, Mailvetter, Sales Navigator, Resume AI). **`docs/`** holds markdown source of truth; **DocsAI** Django constants are under **`contact360.io/admin/`** (not a separate `contact360/docsai/` tree in this layout).

| Path | Purpose |
| --- | --- |
| `contact360.io/app/` | Authenticated dashboard (Next.js; package name `contact360-dashboard`). |
| `contact360.io/root/` | Marketing / public site (Next.js; package name `contact360-marketing`). |
| `contact360.io/admin/` | Django DocsAI — roadmap & architecture mirrors, internal control surfaces. |
| `contact360.io/api/` | **Appointment360** — FastAPI GraphQL gateway (`/graphql`), `sql/apis/*.md`, `app/graphql/modules/*`. |
| `contact360.io/sync/` | **Connectra** — Go search / VQL / Elasticsearch (see service `README.md`). |
| `contact360.io/jobs/` | **TKD Job** — Python scheduler, Kafka consumers, DAG processors (`README.md`). |
| `lambda/` | Deployable email/log/storage services (subset in minimal clones: `emailapis/`, `emailapigo/`, `logs.api/`, `s3storage/`). |
| `backend(dev)/` | Extra service trees when present: `contact.ai/`, `mailvetter/`, `salesnavigator/`, `resumeai/`. |
| `extension/` | Browser extension packages (optional checkout). |
| `docs/` | Product documentation (architecture, roadmap, versioning). |

**Legacy / alternate names (full monorepo or older docs):**

| Older / logical path | Typical role | This workspace |
| --- | --- | --- |
| `contact360/dashboard/` | Dashboard app | `contact360.io/app/` |
| `contact360/marketing/` | Marketing site | `contact360.io/root/` |
| `contact360/docsai/` | Django DocsAI | `contact360.io/admin/` |
| `lambda/appointment360/` | GraphQL gateway | `contact360.io/api/` |
| `lambda/connectra/` | Connectra | `contact360.io/sync/` |
| `lambda/tkdjob/` | Job scheduler | `contact360.io/jobs/` |
| `lambda/mailvetter/` | Verifier | Often `backend(dev)/mailvetter/` here, or `lambda/mailvetter/` in other checkouts |

**Naming note:** historical docs used `extention/contact360` and `extension/contact360`. Current canonical extension package folder is **`extension/contact360/`**.

### `extension/` detail

- `contact360/` — Chrome extension for Sales Navigator workflows.

**Checkout note:** Some clones omit the `extension/` tree (e.g. backend-only worktrees). The **canonical** package path remains `extension/contact360/`; do not introduce new paths under the historical `extention/` spelling.

---

## Dashboard routes (product)

The authenticated dashboard uses the Next.js App Router under `contact360.io/app/app/(dashboard)/`.
```

```1:50:d:\code\ayan\contact\docs\versions.md
# Contact360 Release History

This file tracks meaningful releases only. It does not enumerate empty placeholder versions.

**Planning alignment:** Near-term cuts (`1.x`–`6.x`) are the default execution horizon. Strategic eras (`7.x`–`10.x`) are defined in `docs/roadmap.md` and `docs/architecture.md` (*Planning horizon*). Foundation (`0.x`) minors use `docs/0. Foundation and pre-product stabilization and codebase setup/version_0.*.md`. Other optional per-minor stubs may live under `docs/versions/version_*.md` when that folder is used. A major moving to `in_progress` here should still have matching roadmap stages and owners.

**Documentation index:** `docs/architecture.md` (system boundaries), `docs/codebase.md` (repo map), `docs/backend.md` (gateway + services), `docs/frontend.md` (dashboard, marketing, DocsAI, extension), `docs/flowchart.md` (diagrams), `docs/version-policy.md` (version policy). **Foundation era (`0.x`) minors:** `docs/0. Foundation and pre-product stabilization and codebase setup/version_0.*.md` and `0.x-master-checklist.md` in that folder. Optional generic stubs may also appear as `docs/versions/version_*.md` when present.

**Path convention:** Product code lives under **`contact360.io/`** (e.g. `app/` = dashboard, `api/` = Appointment360, `admin/` = DocsAI). Per-minor stubs may still mention legacy names such as `contact360/dashboard` — treat them as **`contact360.io/app/`** unless a release note says otherwise.

## Unreleased (next cut)

- **Target:** `1.1.0`
- **Status:** in_progress
- **Summary:** Complete bulk validation hardening and billing flow operationalization.
- **Planned stage mapping:** `1.3` (billing), `2.4` (bulk processing)
- **Owner:** Product + Platform Engineering

---

## Release index

| Version | Status | Released/Target | Summary |
| --- | --- | --- | --- |
| `0.1.0` | released | historical | **Monorepo bootstrap** — internal foundation baseline |
| `1.0.0` | released | historical | Contact360 MVP baseline — auth, credits, email core |
| `1.1.0` | in_progress | next cut | Bulk + billing maturity |
| `1.2.0` | planned | upcoming | Analytics, notifications, admin controls, security baseline |
| `2.0.0` | planned | TBD | Email system era — finder, verifier, results, bulk |
| `3.0.0` | planned | TBD | Contact and company data system era |
| `4.0.0` | planned | TBD | Extension and Sales Navigator maturity era |
| `5.0.0` | planned | TBD | AI workflows era |
| `6.0.0` | planned | TBD | Reliability and Scaling era |
| `7.0.0` | planned | TBD | Deployment era |
| `8.0.0` | planned | TBD | Public and private APIs era |
| `9.0.0` | planned | TBD | Ecosystem integrations and Platform productization era |
| `10.0.0` | planned | TBD | Email campaign era |

---

## Release entries

### `0.1.0`

- **Status:** released
- **Released on:** historical
- **Codename:** Monorepo bootstrap
- **Summary:** Initial monorepo, service skeletons, and product foundation setup.
- **Scope:** Base app/service directories, early integration scaffolding, CI pipelines, DocsAI bootstrap, and bootstrapping flows.
- **Roadmap mapping:** pre-v1 foundation work
```

```1:50:d:\code\ayan\contact\docs\roadmap.md
# Contact360 Roadmap

This roadmap defines staged delivery across major versions.  
Stage metadata standard for every stage:

- **Status**
- **Depends on**
- **Risk**
- **Definition of done**
- **KPI**
- **Ships in**

---

## Current focus

Delivery is currently centered on **billing and payments (Stage 1.3)** and **bulk validation hardening (Stage 2.4)**. Core **finder → verifier → results** flows remain the product backbone.

**Planning horizon:** near-term execution is **`1.x`–`6.x`** (this file + `docs/versions.md`). Strategic runway **`7.x`–`10.x`** is detailed in roadmap era sections below and in **`docs/architecture.md`** (*Planning horizon*). Optional per-minor notes: `docs/versions/version_*.md`. Strategic stages do not block current releases.

**Product surfaces:** Dashboard, marketing, DocsAI, and extension entry points are summarized in **`docs/frontend.md`**. Backend service index: **`docs/backend.md`**.

---

## VERSION 1.x — User, Billing and Credit System

### Stage 1.1 - User and Authentication System

**Status:** Completed
**Depends on:** Foundation platform setup  
**Risk:** Session handling regressions across dashboard and extension  
**Definition of done:** User can register, sign in, and begin usage with starter credits  
**KPI:** Successful signup-to-first-action conversion, auth failure rate  
**Ships in:** `1.0.0`

- Email signup and login
- Basic user profile
- Auto credit assignment (50 credits)
- Session management
- **Code pointers:** `contact360.io/app/src/context/RoleContext.tsx`, `contact360.io/api/app/main.py`

---

### Stage 1.2 - Credit Management System (CORE)

**Status:** Completed
**Depends on:** Stage 1.1  
**Risk:** Incorrect deduction and lapse behavior can block valid user actions  
**Definition of done:** Finder deductions and entitlement checks behave correctly under standard flows  
**KPI:** Credit ledger consistency, blocked-request correctness at zero balance  
```

```1:50:d:\code\ayan\contact\docs\governance.md
# Contact360 Docs and Service Governance

This file defines baseline governance for the monorepo and service skeletons.

## Monorepo baseline

- Product surfaces and APIs live under `contact360.io/`.
- Lambda-style services live under `lambda/`.
- Optional backend workspaces live under `backend(dev)/`.
- Browser extension code is canonical in `extension/contact360/`.
- **Frontend page inventory (supplementary):** `docs/frontend/` — JSON page specs under `docs/frontend/pages/`, CSV exportsUnder `docs/frontend/excel/`, overview in `docs/frontend/README.md`. The **canonical live UI map** remains **`docs/frontend.md`** (dashboard `contact360.io/app/`, marketing `root/`, DocsAI `admin/`, extension).

## Mandatory docs synchronization

When editing architecture or roadmap docs, mirror updates in DocsAI constants:

- `docs/architecture.md` -> `contact360.io/admin/apps/architecture/constants.py`
- `docs/roadmap.md` -> `contact360.io/admin/apps/roadmap/constants.py`

Follow the full runbook in `docs/docsai-sync.md`.

## CI baseline

Repo-level checks run via `.github/workflows/ci.yml` to ensure:

- required top-level directories exist,
- DocsAI constants files exist,
- and core docs files are present.

## Release hygiene

- No major/minor stage status transitions without doc + constants sync.
- No new service path aliases unless reflected in architecture docs.

## Version era summary (canonical)

| Version | Theme |
| ------- | ----- |
| `0.x.x` | Foundation and pre-product stabilization and codebase setup |
| `1.x.x` | Contact360 user and billing and credit system |
| `2.x.x` | Contact360 email system |
| `3.x.x` | Contact360 contact and company data system |
| `4.x.x` | Contact360 Extension and Sales Navigator maturity |
| `5.x.x` | Contact360 AI workflows |
| `6.x.x` | Contact360 Reliability and Scaling |
| `7.x.x` | Contact360 deployment |
| `8.x.x` | Contact360 public and private APIs and endpoints |
| `9.x.x` | Contact360 Ecosystem integrations and Platform productization |
| `10.x.x` | Contact360 email campaign |
```

Note: In the source file, line 11 uses “CSV exports” followed by “under” on the same line; I accidentally merged a typo (“exportsUnder”) in the block above. Correct wording from disk:

```11:11:d:\code\ayan\contact\docs\governance.md
- **Frontend page inventory (supplementary):** `docs/frontend/` — JSON page specs under `docs/frontend/pages/`, CSV exports under `docs/frontend/excel/`, overview in `docs/frontend/README.md`. The **canonical live UI map** remains **`docs/frontend.md`** (dashboard `contact360.io/app/`, marketing `root/`, DocsAI `admin/`, extension).
```

```1:50:d:\code\ayan\contact\docs\frontend.md
# Contact360 frontend map

> **Note:** This file is named `frontend.md` in the repository. It is the **frontend** (product UI) index — dashboard, marketing, DocsAI, and extension.

For **backend** services, see **`docs/backend.md`**. For the full monorepo and per-service code pointers, see **`docs/codebase.md`**. For system boundaries, see **`docs/architecture.md`**.

**Page inventory, component catalog, design system, and hooks/services docs** live under **`docs/frontend/`** (see **`docs/frontend/README.md`**). Canonical app code remains under **`contact360.io/`** below.

---

## Version era → primary UI surfaces (`0.x`–`10.x`)

Themes are defined in **`docs/version-policy.md`**. UI surface coverage at a glance:

| Era | Theme | Primary UI surfaces | Key UI elements introduced |
| --- | --- | --- | --- |
| `0.x` | Foundation | App shell, routing, design tokens | Layout, sidebar, auth shell, global CSS |
| `1.x` | User, billing, credit | Auth, profile, settings, billing, usage, admin | Login/register forms, billing modals, credit display, UPI payment, usage charts |
| `2.x` | Email system | Finder, verifier, results, export, jobs, files | Email input forms, result cards, progress bars, bulk upload, job status indicators |
| `3.x` | Contact & company data | Contacts, companies, search/filter UX | VQL query builder, data tables, filter sidebar, saved searches, company drill-down |
| `4.x` | Extension & Sales Navigator | `extension/contact360/` (Chrome), LinkedIn flows | Extension popup, SN ingestion panels, sync status indicators |
| `5.x` | AI workflows | AI chat, AI-assisted email writer, live voice | Chat message streams, AI confidence badges, streaming progress, AI tool panels |
| `6.x` | Reliability & scaling | Client resilience patterns | Error boundaries, retry UI, loading skeletons, offline banners |
| `7.x` | Deployment | RBAC-sensitive admin surfaces, DocsAI governance | Role-gated UI, feature flags, admin governance screens |
| `8.x` | Public & private APIs | API docs, integrations, analytics/reporting | API key manager, analytics charts, integration cards, reporting tables |
| `9.x` | Ecosystem & productization | Integrations hub, workspace/tenant admin | Integration setup wizards, entitlement indicators, plan upgrade flows |
| `10.x` | Email campaign | Campaign builder, audience, templates, send review | Campaign form, audience picker, email template editor, send progress tracker |

---

## Product applications (`contact360.io/`)

| Path | Role | Stack | Key docs |
| --- | --- | --- | --- |
| `contact360.io/app/` | Authenticated product (GraphQL-only client) | Next.js 16, React 19, modular CSS under `app/css/*` | `contact360.io/app/README.md`, `docs/DESIGN_UX.md`, `docs/API_DASHBOARD_MAPPING.md` |
| `contact360.io/root/` | Public marketing and growth pages | Next.js 16, custom CSS (BEM-like) | `contact360.io/root/README.md`; env: `GRAPHQL_URL`, dashboard URL for auth CTAs |
| `contact360.io/admin/` | Internal docs/admin mirror (roadmap & architecture constants) | Django | `docs/docsai-sync.md`, `contact360.io/admin/deploy/README.md` |

**Gateway contract:** All dashboard API traffic goes through **`contact360.io/api/`** GraphQL (`NEXT_PUBLIC_API_URL` / GraphQL URL in dashboard config).

---

## Browser extension

| Path | Role | Notes |
| --- | --- | --- |
| `extension/contact360/` | Chrome extension (Sales Navigator workflows) | **Canonical** path. Some clones omit `extension/`; see `docs/architecture.md` → *Service register*. Do not use `extention/` spelling for new work. |

Phase **4.x** Extension and Sales Navigator maturity (auth, telemetry, SN ingestion, sync) is tracked in **`docs/roadmap.md`** and **`docs/versions.md`**.
```

```1:50:d:\code\ayan\contact\docs\codebase.md
# Contact360 Codebase Deep Map

**Frontend surfaces (dashboard, marketing, DocsAI, extension):** see **`docs/frontend.md`**. **Backend services:** **`docs/backend.md`**.
**Deep per-service analyses:** see **`docs/codebases/README.md`**.

## Monorepo structure

| Path | Role | Primary tech |
| --- | --- | --- |
| `contact360.io/app/` | Authenticated product (dashboard) | Next.js 16, React 19, TypeScript |
| `contact360.io/root/` | Public marketing site | Next.js |
| `contact360.io/admin/` | DocsAI — internal roadmap/architecture mirrors | Django |
| `contact360.io/api/` | Appointment360 GraphQL gateway | FastAPI, Python |
| `contact360.io/sync/` | Connectra search / VQL | Go, Elasticsearch |
| `contact360.io/jobs/` | TKD Job scheduler and DAG workers | Python, Kafka |
| `lambda/emailapis/` | Finder/verifier orchestration | Python |
| `lambda/emailapigo/` | High-throughput finder (Go workers) | Go |
| `lambda/logs.api/` | Logging/telemetry ingestion | Python, S3 CSV + in-memory cache |
| `lambda/s3storage/` | File lifecycle and object storage | Python, S3 |
| `backend(dev)/mailvetter/` | Verification engine | Go |
| `backend(dev)/contact.ai/` | AI-driven workflows | Python |
| `backend(dev)/salesnavigator/` | Sales Navigator integration backend | Python |
| `backend(dev)/resumeai/` | Resume AI workflows | Python |
| `extension/contact360/` | Browser extension runtime | JS/TS extension stack |

**Legacy aliases:** older docs and full monorepos often use `contact360/dashboard`, `lambda/appointment360`, `lambda/connectra`, `lambda/tkdjob`, and `lambda/mailvetter/` — see **`docs/architecture.md`** → *Legacy / alternate names*.

**Service status:** see `docs/architecture.md` → *Service register (canonical)*.

## Core runtime contracts

- Client surfaces (`contact360.io/app`, extension) call **Appointment360** (`contact360.io/api`) as the primary contract gateway.
- Appointment360 orchestrates service calls to finder, verifier, search, scheduling, and storage services.
- Async flows run through **`contact360.io/jobs`**, with telemetry routed to `lambda/logs.api` and artifacts to `lambda/s3storage`.
- Search and enrichment behavior rely on **Connectra** (`contact360.io/sync`) (query/filter/index contract).

## Deep decomposition framework (how to break work)

Use five task tracks for every roadmap stage:

1. **Contract track**: GraphQL/API/event contract definitions and compatibility.
2. **Service track**: Backend implementation per owning service.
3. **Surface track**: Dashboard/extension/docsai UX and action wiring.
4. **Data track**: Storage, lineage, quality, and reconciliation.
5. **Ops track**: Observability, rollback safety, and release validation.

## `s3storage` focused implementation map

- Primary service: `lambda/s3storage/`
- API entrypoints: `app/api/v1/endpoints/uploads.py`, `files.py`, `schema.py`, `avatars.py`, `buckets.py`
```

```1:50:d:\code\ayan\contact\docs\backend.md
# Contact360 Backend (0.x-10.x)

Backend operating map for APIs, services, data stores, and era-aligned execution.

## Era-by-era backend surface

| Era | Theme | Modules | Tables | Service entrypoints |
|---|---|---|---|---|
| `0.x` | Foundation | auth, health | users, sessions | `api/main.py` |
| `1.x` | User/Billing/Credit | auth, users, billing, usage | users, user_profiles, addon_packages | auth/billing modules |
| `2.x` | Email system | email, jobs | scheduler_jobs, user_activities | email services mailvetter |
| `3.x` | Contacts/Companies | contacts, companies | saved_searches | connectra graphql modules |
| `4.x` | Extension/SalesNav | linkedin, sales_navigator | user_scraping | sales navigator service |
| `5.x` | AI workflows | ai_chats | ai_chats, resume_documents | contact.ai resumeai |
| `6.x` | Reliability | cross-cutting guards | n/a | slo/error budget systems |
| `7.x` | Deployment | admin, governance | activities | deployment and audit controls |
| `8.x` | Public/private APIs | webhooks | webhooks | webhook dispatcher |
| `9.x` | Ecosystem | integrations | integrations | connector framework |
| `10.x` | Email campaign | campaigns, sequences, templates | campaigns, sequences, templates | campaign engine workers |

## Era-to-module additions table

| Era | API modules emphasized | Data emphasis |
| --- | --- | --- |
| `1.x` | auth/users/billing/usage | users, credits, plans, invoices |
| `2.x` | email/jobs/upload | email verification/finder lifecycle |
| `3.x` | contacts/companies/s3 | contacts and companies dual-store lineage |
| `4.x` | linkedin/sales navigator | ingestion and sync integrity |
| `5.x` | ai chats/jobs | AI prompt/result lineage |
| `6.x` | analytics/activities/health | reliability telemetry and RC evidence |
| `7.x` | admin/authz | governance and audit trails |
| `8.x` | webhooks/integrations | public-private contract lineage |
| `9.x` | profile/notifications/2fa | tenant and ecosystem controls |
| `10.x` | campaigns/sequences/templates | campaign execution and compliance |

## `s3storage` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Freeze upload/list/download endpoint contracts | Stabilize S3/filesystem backend parity | Baseline health and smoke checks |
| `1.x` | Define object class policy (`avatar`, `photo`, `resume`) | Validate content type/size per path | Audit fields and abuse monitoring |
| `2.x` | Freeze multipart API contract | Durable multipart session store | Metadata freshness and retry telemetry |
| `3.x` | Define ingestion artifact contract | Robust schema/preview/stats behavior | Lineage for ingest/export artifacts |
| `4.x` | Extension-safe access and TTL policy | Channel-aware access controls | Source provenance in metadata |
| `5.x` | Define AI artifact and retention contract | Policy enforcement for AI artifacts | Sensitive artifact audit trails |
| `6.x` | Define idempotency and SLO contract | Reconciliation and metadata write safety | Error budgets and incident runbooks |
| `7.x` | Define service-to-service auth contract | Endpoint authz and retention hooks | Compliance evidence generation |
| `8.x` | Define versioning/deprecation contract | Storage lifecycle event contracts | Compatibility and partner reliability gates |
| `9.x` | Define entitlement and quota contract | Plan-aware throttling and limits | Tenant cost/residency reporting |
| `10.x` | Define campaign artifact reproducibility contract | Immutable compliance storage paths | Compliance/audit sign-off evidence |
```

Note: Row 11 in the table on disk uses `email services + mailvetter` (with `+`); the paste shortened `+` to a space in one cell—see file for exact punctuation.

```1:50:d:\code\ayan\contact\docs\flowchart.md
# Contact360 Flowcharts

## Core request flow

```mermaid
flowchart LR
    user["User / Workspace"]
    dash["Dashboard / Extension"]
    mkt["Marketing"]
    gateway["appointment360 GraphQL"]
    finder["emailapis / emailapigo"]
    verify["mailvetter"]
    search["connectra"]
    jobs["tkdjob"]
    files["s3storage"]
    logs["logs.api"]
    ai["contact.ai"]

    user --> dash --> gateway
    user --> mkt
    mkt -->|"reads (GraphQL)"| gateway
    mkt -->|"auth CTAs"| dash
    gateway --> finder
    gateway --> verify
    gateway --> search
    gateway --> jobs
    gateway --> ai
    jobs --> files
    gateway --> logs
    jobs --> logs
```

Marketing is unauthenticated: it may call GraphQL for **read-only** product data where configured, and routes **sign-in / sign-up** flows to the dashboard for authenticated actions.

**Code paths (this monorepo):** GraphQL gateway → `contact360.io/api/`; Connectra → `contact360.io/sync/`; TKD Job → `contact360.io/jobs/`; dashboard → `contact360.io/app/`; marketing → `contact360.io/root/`. Shared email/log/storage services remain under `lambda/*`; Mailvetter and several integrations may live under `backend(dev)/` depending on checkout.

## Stage execution decomposition flow (per minor)

```mermaid
flowchart TD
    stage["Roadmap stage X.Y"]
    contract["Contract tasks"]
    service["Service tasks"]
    surface["Surface tasks"]
    data["Data tasks"]
    ops["Ops tasks"]
    release["Version entry + release gate"]

    stage --> contract
    stage --> service
```

```1:50:d:\code\ayan\contact\docs\version-policy.md
# Contact360 Version Policy

## SemVer policy

- **Major (`X.0.0`)**: New product era, major channel expansion, or foundational architecture shift.
- **Minor (`X.Y.0`)**: New feature sets within an existing product era.
- **Patch (`X.Y.Z`)**: Bug fixes and reliability/performance improvements without scope expansion.
- **Ownership**: Product + engineering leads approve version bumps per shipped scope.

## Decision rubric (Contact360 specific)

- Use a **major** bump when introducing a new platform capability family (for example, moving from core user/billing to the email system era, or from email to contact/company data).
- Use a **minor** bump when adding a customer-visible capability in an existing major (for example, new billing flows, analytics panels, extension telemetry).
- Use a **patch** bump for hotfixes, edge-case fixes, retry logic hardening, and non-breaking operational updates.

## Release entry schema

Every release entry in `docs/versions.md` should include:

- `version`
- `status` (`released`, `in_progress`, `planned`)
- `released_on` (or `target_window` if planned)
- `summary`
- `scope`
- `Roadmap mapping` (roadmap stage IDs; canonical display label in `docs/versions.md`, equivalent to `ships_stages`)
- `owner`

## Version hygiene rules

- **Repo paths:** Canonical product and gateway paths are under **`contact360.io/`** (see `docs/architecture.md`). Older stubs may reference `contact360/dashboard` or `lambda/appointment360/` — align to `contact360.io/app/` and `contact360.io/api/` when editing links or code pointers.
- Do not pre-generate placeholder versions.
- Create version entries only when scope is approved (`planned`) or shipped (`released`).
- Keep `docs/versions.md` and `docs/roadmap.md` cross-referenced on every release update.
- Use `Roadmap mapping` as the release-entry field label consistently in `docs/versions.md`.

---

## Major themes (`0.x` to `10.0.0`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- Initial repository setup, service skeletons, CI pipelines, base authentication primitives, DocsAI bootstrap, and internal experiments.
- Core concern: repo hygiene, service wiring, and pre-product foundation readiness.

### `1.x.x` - Contact360 user and billing and credit system

- User authentication and session management, credit lifecycle (deduction, top-up, lapse), billing/payment flows, user-facing analytics, notifications, admin control panel, and basic security baseline.
- Core concern: the end-to-end user account lifecycle and credit economy.

### `2.x.x` - Contact360 email system
```

```1:50:d:\code\ayan\contact\docs\docsai-sync.md
# DocsAI Sync Runbook

## Purpose

DocsAI uses hardcoded constants for architecture and roadmap views. This runbook defines mandatory sync rules between markdown docs and DocsAI constants.

## Sync rules

1. If `docs/architecture.md` changes, update `contact360.io/admin/apps/architecture/constants.py` in the same change set.
2. If `docs/roadmap.md` changes, update `contact360.io/admin/apps/roadmap/constants.py` in the same change set.
3. If release taxonomy/policy changes in `docs/version-policy.md`, verify corresponding roadmap/version entries still match.

## Update checklist

- Architecture updates:
  - Update folder/service names and descriptions in `docs/architecture.md`.
  - Mirror those changes in `contact360.io/admin/apps/architecture/constants.py`.
  - Verify data-flow labels still match the architecture narrative.

- Roadmap updates:
  - Update stage details in `docs/roadmap.md` (`status`, `depends_on`, `risk`, `definition_of_done`, `kpi`, `ships_in`).
  - Mirror stage additions/updates in `contact360.io/admin/apps/roadmap/constants.py`.
  - Ensure every stage still maps to a release in `docs/versions.md`.

- Versioning updates:
  - Update policy in `docs/version-policy.md` when versioning rules change.
  - Update release entries in `docs/versions.md` with scope and stage mapping.
  - Confirm cross-links between roadmap and versions remain valid.

## Verification steps (DocsAI UI)

1. Open DocsAI architecture dashboard and confirm structure/service cards reflect the latest `constants.py`.
2. Open DocsAI roadmap dashboard and confirm stage list, statuses, and feature bullets match the roadmap constants.
3. Spot-check at least one updated stage from each of:
   - `1.x` user/billing/credit baseline,
   - `2.x` email system,
   - `3.x` contact and company data (Connectra),
   - `4.x` extension and Sales Navigator,
   - `5.x` AI workflows.
4. If mismatch appears, treat constants files as stale and re-sync before finalizing release docs.

## Release hygiene note

Do not ship docs-only version updates unless roadmap and DocsAI mirrors are synchronized.

## Deep sync workflow for staged execution

For every minor release stage (`X.Y.0`), process docs in this order:

1. Update `docs/roadmap.md` stage metadata and task bullets.
```

```1:50:d:\code\ayan\contact\docs\audit-compliance.md
# Audit, Compliance, and Governance (All Eras: 0.x–10.x)

> **Scope:** This document covers the full era range. Each service section details per-era compliance requirements from `0.x` (foundation) through `10.x` (email campaign). For full RBAC policy and role-enforcement patterns, see **`docs/7. Contact360 deployment/rbac-authz.md`**. For release and governance process, see **`docs/governance.md`**.

## RBAC matrix

| Capability | FreeUser | ProUser | Admin | SuperAdmin |
|---|---|---|---|---|
| Manage webhooks | no | yes | yes | yes |
| Manage integrations | no | yes | yes | yes |
| Create/schedule campaigns | no | yes | yes | yes |
| Approve billing submissions | no | no | yes | yes |

## Audit event schema

- event_id, event_time, actor_user_id, actor_role
- tenant_id, service, action, status
- target_type, target_id, request_id, metadata

## Tenant isolation

- Tenant scoped access required for all mutable resources
- Cross-tenant references return not-found semantics

## Era-specific RBAC and evidence mapping

- `7.x` is the RBAC baseline era and defines role enforcement patterns.
- `8.x` extends controls to partner/public API access and webhook identities.
- `9.x` extends controls to tenant/workspace/admin self-serve governance.
- `10.x` applies compliance controls to campaign consent, suppression, and opt-out audit trails.

## `s3storage` compliance controls by era

- `1.x`: enforce file type and size policy for user/billing artifacts.
- `2.x`: require multipart completion traceability (`uploadId`, part registration, completion evidence).
- `6.x`: require idempotent storage lifecycle operations and reconciliation evidence.
- `7.x`: enforce service-to-service authz for storage endpoints and retention policy controls.
- `8.x`: enforce versioned storage API behavior with compatibility tests.
- `10.x`: enforce immutable campaign compliance artifacts and retention/audit verifiability.

Mandatory evidence pack for storage-impacting releases:

- endpoint contract diff (if changed),
- metadata integrity/reconciliation report,
- access-control validation report,
- retention/deletion policy validation report.

## `logs.api` compliance controls by era

- `1.x`: user and billing event traceability with actor and request identifiers.
```

---

## 3. Files under the requested folders

Paths below use the workspace form `docs\...` (absolute: `d:\code\ayan\contact\docs\...`).

### `docs\analysis\` (41 files)

- `cursor_1_x_x_era_documentation_extracti.md`
- `cursor_2_x_x_era_documentation_extracti.md`
- `cursor_3_x_x_era_codebase_analysis.md`
- `cursor_3_x_x_era_documentation_extracti.md`
- `cursor_4_x_x_era_codebase_analysis.md`
- `cursor_codebase_analysis_content_retrie.md`
- `cursor_codebase_analysis_content_retrie1.md`
- `cursor_codebase_analysis_file_content_r.md`
- `cursor_codebase_analysis_file_contents.md`
- `cursor_contact360_api_documentation_ret.md`
- `cursor_contact360_deployment_documentat.md`
- `cursor_contact360_deployment_documentat1.md`
- `cursor_contact360_documentation_and_cod.md`
- `cursor_contact360_documentation_files_r.md`
- `cursor_contact360_documentation_retriev.md`
- `cursor_contact360_documentation_retriev3.md`
- `cursor_contact360_documentation_summary.md`
- `cursor_contact360_ecosystem_productizat.md`
- `cursor_contact360_email_integration_exp.md`
- `cursor_contact360_email_system_document.md`
- `cursor_documentation_content_retrieval.md`
- `cursor_documentation_content_summary_an.md`
- `cursor_documentation_extraction_for_sta.md`
- `cursor_documentation_folder_inventory.md`
- `cursor_documentation_retrieval_for_user.md`
- `cursor_email_api_system_exploration.md`
- `cursor_email_apis_exploration_and_analy.md`
- `cursor_email_architecture_and_behavior.md`
- `cursor_email_system_architecture_explor.md`
- `cursor_email_system_architecture_explor1.md`
- `cursor_email_system_documentation_enrich.md` (name truncated in index as `cursor_email_system_version_docs_enrich.md` — verify on disk if needed)
- `cursor_email_system_exploration_in_admi.md`
- `cursor_email_system_exploration_in_mono.md`
- `cursor_email_system_exploration_in_mono1.md`
- `cursor_era_mapping_and_execution_queue.md`
- `cursor_file_content_retrieval_and_versi.md`
- `cursor_file_content_structure_overview.md`
- `cursor_file_listing_and_service_name_pr.md`
- `cursor_markdown_file_content_retrieval.md`
- `cursor_mail_vetter_codebase_exploration.md`
- `cursor_reference_documents_for_version.md`

*Correction:* The glob listed `cursor_email_system_version_docs_enrich.md` not `documentation_enrich` — use exact names from disk:

From first glob result for analysis - full exact list:

1. cursor_contact360_documentation_files_r.md
2. cursor_contact360_documentation_and_cod.md
3. cursor_codebase_analysis_file_contents.md
4. cursor_contact360_ecosystem_productizat.md
5. cursor_file_content_structure_overview.md
6. cursor_codebase_analysis_file_content_r.md
7. cursor_codebase_analysis_content_retrie1.md
8. cursor_contact360_api_documentation_ret.md
9. cursor_reference_documents_for_version.md
10. cursor_documentation_extraction_for_sta.md
11. cursor_codebase_analysis_content_retrie.md
12. cursor_contact360_deployment_documentat1.md
13. cursor_contact360_deployment_documentat.md
14. cursor_3_x_x_era_codebase_analysis.md
15. cursor_file_content_retrieval_and_versi.md
16. cursor_3_x_x_era_documentation_extracti.md
17. cursor_4_x_x_era_codebase_analysis.md
18. cursor_contact360_documentation_retriev3.md
19. cursor_1_x_x_era_documentation_extracti.md
20. cursor_documentation_retrieval_for_user.md
21. cursor_contact360_documentation_retriev.md
22. cursor_documentation_content_retrieval.md
23. cursor_2_x_x_era_documentation_extracti.md
24. cursor_contact360_email_system_document.md
25. cursor_documentation_folder_inventory.md
26. cursor_contact360_documentation_summary.md
27. cursor_documentation_content_summary_an.md
28. cursor_file_listing_and_service_name_pr.md
29. cursor_email_system_version_docs_enrich.md
30. cursor_email_system_exploration_in_admi.md
31. cursor_contact360_email_integration_exp.md
32. cursor_email_system_exploration_in_mono1.md
33. cursor_email_architecture_and_behavior.md
34. cursor_email_system_architecture_explor1.md
35. cursor_email_system_architecture_explor.md
36. cursor_email_api_system_exploration.md
37. cursor_email_apis_exploration_and_analy.md
38. cursor_email_system_exploration_in_mono.md
39. cursor_mail_vetter_codebase_exploration.md
40. cursor_era_mapping_and_execution_queue.md
41. cursor_markdown_file_content_retrieval.md

I'll remove the erroneous merged line in the final output and give clean list.

### `docs\plans\` (28 files)

- `0.x_foundation_docs_overhaul_72dbbe14.plan.md`
- `1.x_docs_deep_enrichment_04e0912e.plan.md`
- `1.x_user_billing_era_overhaul_323c67a3.plan.md`
- `2.x_email_docs_enrichment_e426d433.plan.md`
- `3.x_docs_repair_&_enrich_99fbb766.plan.md`
- `4.x_era_docs_enrichment_cf99f7a5.plan.md`
- `4.x_era_docs_fix_0c3c9e91.plan.md`
- `5.x_ai_workflows_docs_fix_fbeb0270.plan.md`
- `6.x_reliability_docs_overhaul_c47b8ea9.plan.md`
- `7.x_deployment_docs_repair_746cb2f6.plan.md`
- `8.x_api_era_docs_overhaul_559bff4d.plan.md`
- `9.x_docs_enrichment_e3f941cd.plan.md`
- `10.x_campaign_docs_overhaul_ad3f11b3.plan.md`
- `add_logger_statements_plan.md`
- `ai_resume_project_43386ce1.plan.md`
- `backend_docs_expansion_e325e51f.plan.md`
- `connectra_integration_implementation_8a2794f9.plan.md`
- `contact360_master_era_plan_6b3b0b54.plan.md`
- `email_lambda_migration_plan_34929bc9.plan.md`
- `email_version_docs_enrichment_2d3a7778.plan.md`
- `foundation_era_docs_overhaul_06254c9e.plan.md`
- `gemini_to_hf_migration_2135cafd.plan.md`
- `gemini_to_hf_migration_f99bfed1.plan.md`
- `graphql_migration_with_uuid_support_2c341fa8.plan.md`
- `logs.api_docs_integration_2d4a412d.plan.md`
- `mailvetter_v1_api_migration_a73fdc25.plan.md`
- `resume_ai_full_build_4a61c2a4.plan.md`
- `version_flowchart_sections_053db1d6.plan.md`

### `docs\ideas\` (2,529 files)

Too many paths to list inline. Top-level includes **`README.md`** and heavy subtrees such as **`admin\`**, **`api\`**, **`app\`**, **`job\`**, **`jobs\`**, **`mailvetter\`** (with nested **`.git`**, **`.ssh`**, **`.docker`**, Go sources), **`resume\`** (multiple nested projects and **`.git`**), **`root\`**, **`s3storage\`**, **`sync\`**, etc. A ripgrep file listing hit a **2,600-result cap** before exhausting the tree.

### `docs\codebases\` (16 files)

- `README.md`
- `admin-codebase-analysis.md`
- `app-codebase-analysis.md`
- `appointment360-codebase-analysis.md`
- `connectra-codebase-analysis.md`
- `contact-ai-codebase-analysis.md`
- `emailapis-codebase-analysis.md`
- `emailcampaign-codebase-analysis.md`
- `email-codebase-analysis.md`
- `extension-codebase-analysis.md`
- `jobs-codebase-analysis.md`
- `logsapi-codebase-analysis.md`
- `mailvetter-codebase-analysis.md`
- `root-codebase-analysis.md`
- `s3storage-codebase-analysis.md`
- `salesnavigator-codebase-analysis.md`

### `docs\frontend\` (65 files)

- `excel\pages_export_2026-03-15 (6) - Dashboard.csv`
- `excel\pages_export_2026-03-15 (6) - Docs.csv`
- `excel\pages_export_2026-03-15 (6) - Marketing.csv`
- `excel\pages_export_2026-03-15 (6) - Product.csv`
- `excel\pages_export_2026-03-15 (6) - Title.csv`
- `excel\README.md`
- `docs\components.md`
- `docs\contact-ai-ui-bindings.md`
- `docs\design-system.md`
- `docs\emailapis-ui-bindings.md`
- `docs\hooks-services-contexts.md`
- `docs\jobs-ui-bindings.md`
- `docs\logsapi-ui-bindings.md`
- `docs\README.md`
- `docs\s3storage-ui-bindings.md`
- `docs\salesnavigator-ui-bindings.md`
- `pages\about_page.json`
- `pages\activities_page.json`
- `pages\admin_page.json`
- `pages\ai_chat_page.json`
- `pages\ai_email_writer_page.json`
- `pages\analytics_page.json`
- `pages\api_docs_page.json`
- `pages\billing_page.json`
- `pages\campaign_builder_page.json`
- `pages\campaigns_page.json`
- `pages\campaign_templates_page.json`
- `pages\careers_page.json`
- `pages\cfo_email_list_page.json`
- `pages\chrome_extension_page.json`
- `pages\companies_page.json`
- `pages\contacts_page.json`
- `pages\dashboard_page.json`
- `pages\dashboard_pageid_page.json`
- `pages\deployment_page.json`
- `pages\docs_page.json`
- `pages\docs_pageid_page.json`
- `pages\email_finder_page.json`
- `pages\email_page.json`
- `pages\email_verifier_page.json`
- `pages\export_page.json`
- `pages\files_page.json`
- `pages\finder_page.json`
- `pages\index.json`
- `pages\integrations_page.json`
- `pages\jobs_page.json`
- `pages\landing_page.json`
- `pages\linkedin_page.json`
- `pages\live_voice_page.json`
- `pages\login_page.json`
- `pages\pages_index.json`
- `pages\privacy_page.json`
- `pages\profile_page.json`
- `pages\prospect_finder_page.json`
- `pages\README.md`
- `pages\refund_page.json`
- `pages\register_page.json`
- `pages\root_page.json`
- `pages\sequences_page.json`
- `pages\settings_page.json`
- `pages\status_page.json`
- `pages\terms_page.json`
- `pages\ui_page.json`
- `pages\usage_page.json`
- `pages\verifier_page.json`

### `docs\backend\` (3,431 files total)

Not practical to list every path here. Breakdown:

| Subfolder | Files | Role |
|-----------|-------|------|
| `postman\` | **3,138** | READMEs, `Contact360 GraphQL API - Complete`, `Connectra API`, `Email Campaign API`, `Resume AI Service1`, many third-party collection folders (e.g. `📌 xAI API`, `📌 Together AI API`, `🛠️ Postman Tool Generation API`), loose `*.postman_collection.json`, etc. |
| `endpoints\` | **197** | `endpoints_index.json`, `*_endpoint_era_matrix.json`, per-operation `*.json` |
| `database\` | **55** | `README.md`, `*_data_lineage.md`, `migrations\`, `tables\`, `table_data\` |
| `apis\` | **38** | Numbered module docs (`01_AUTH_MODULE.md` …), `*_ERA_TASK_PACKS.md`, `README.md` |

---

**Corrections to deliver in final message:**  
1. Fix governance.md block typo (use one-line cite for line 11 or paste correctly).  
2. Fix flowchart.md — the inner ```mermaid broke the outer fence; present flowchart excerpt without triple-nesting or use simplified plain listing for lines 1–50.  
3. Simplify analysis list to the exact 41 from first tool output only.

Let me rewrite section 2 more carefully:
- For flowchart, the file contains ```mermaid which breaks markdown - I'll show lines 1-50 as plain text with "fenced code" noted or skip inner closing fences

I'll read flowchart again lines 1-50 raw
`</think>`
Fixing formatting issues: re-reading `governance.md` line 11 and `flowchart.md` lines 1–50 to provide accurate excerpts.




Below is a cleaned-up report. **Note:** `d:\code\ayan\contact\docs` contains **6,439** files in a recursive index (including `docs\.git` and very large trees under `docs\ideas\` and `docs\backend\postman\`). A full path-by-path tree of every file is too large for a single message; the outline below is the complete *structural* tree; the numbered folders list every file in those era roots that were enumerated.

---

## 1. Complete structural tree (all top-level areas + enumerated subtrees)

```
d:\code\ayan\contact\docs\
├── .git\                                    (Git metadata for docs checkout)
├── analysis\                                → 41 *.md (full list in §3)
├── plans\                                   → 28 *.plan.md (full list in §3)
├── codebases\                               → 16 files (full list in §3)
├── frontend\
│   Excel\, docs\, pages\                   → 65 files total (full list in §3)
├── backend\
│   apis\                                    → 38 files
│   database\                                → 55 files (lineage, migrations, tables\, table_data\)
│   endpoints\                               → 197 *.json
│   postman\                                 → 3,138 files (collections + third-party mirrors)
├── ideas\                                   → 2,529 files (README + nested clones; not all paths listed)
│
├── Canonical root *.md (non-exhaustive): architecture, roadmap, versions, governance, frontend, codebase,
│   backend, flowchart, version-policy, docsai-sync, audit-compliance, …
│
└── Era documentation folders:
    ├── 0. Foundation and pre-product stabilization and codebase setup\        (23 files)
    ├── 1. Contact360 user and billing and credit system\                      (23 files)
    ├── 2. Contact360 email system\                                            (24 files)
    ├── 3. Contact360 contact and company data system\                         (27 files)
    ├── 4. Contact360 Extension and Sales Navigator maturity\                  (27 files)
    ├── 5. Contact360 AI workflows\                                          (24 files)
    ├── 6. Contact360 Reliability and Scaling\                                 (26 files)
    ├── 7. Contact360 deployment\                                            (26 files)
    ├── 8. Contact360 public and private apis and endpoints\                   (27 files)
    ├── 9. Contact360 Ecosystem integrations and Platform productization\      (26 files)
    └── 10. Contact360 email campaign\                                       (28 files)
```

**Scale:** `docs\backend\` ≈ **3,431** files; **`docs\backend\postman\`** alone is **3,138** files. **`docs\ideas\`** is **2,529** files (includes nested **`.git`**, `.ssh`, `.docker`, and source trees).

---

## 2. First 50 lines of each requested file

For files that are plain Markdown, line-range citations are used. **`flowchart.md`** opens a **```mermaid** block on line 4, so lines 1–50 are shown in a **4-backtick** fence so the inner fences stay valid.

```1:50:d:\code\ayan\contact\docs\architecture.md
# Contact360 Architecture

## Overview

**Contact360** is a B2B SaaS platform focused on email discovery and verification. The system uses a Next.js dashboard, a Django DocsAI admin/docs surface, a FastAPI GraphQL gateway (`appointment360`), and multiple backend services for search, verification, AI, scheduling, logging, and file storage.

---

## Repository layout (this monorepo)

Product UI, the GraphQL gateway, Connectra, and the job scheduler live under **`contact360.io/`**. Shared email/log/storage microservices often live under **`lambda/`**. Additional backend checkouts in this workspace use **`backend(dev)/`** (AI, Mailvetter, Sales Navigator, Resume AI). **`docs/`** holds markdown source of truth; **DocsAI** Django constants are under **`contact360.io/admin/`** (not a separate `contact360/docsai/` tree in this layout).

| Path | Purpose |
| --- | --- |
| `contact360.io/app/` | Authenticated dashboard (Next.js; package name `contact360-dashboard`). |
| `contact360.io/root/` | Marketing / public site (Next.js; package name `contact360-marketing`). |
| `contact360.io/admin/` | Django DocsAI — roadmap & architecture mirrors, internal control surfaces. |
| `contact360.io/api/` | **Appointment360** — FastAPI GraphQL gateway (`/graphql`), `sql/apis/*.md`, `app/graphql/modules/*`. |
| `contact360.io/sync/` | **Connectra** — Go search / VQL / Elasticsearch (see service `README.md`). |
| `contact360.io/jobs/` | **TKD Job** — Python scheduler, Kafka consumers, DAG processors (`README.md`). |
| `lambda/` | Deployable email/log/storage services (subset in minimal clones: `emailapis/`, `emailapigo/`, `logs.api/`, `s3storage/`). |
| `backend(dev)/` | Extra service trees when present: `contact.ai/`, `mailvetter/`, `salesnavigator/`, `resumeai/`. |
| `extension/` | Browser extension packages (optional checkout). |
| `docs/` | Product documentation (architecture, roadmap, versioning). |

**Legacy / alternate names (full monorepo or older docs):**

| Older / logical path | Typical role | This workspace |
| --- | --- | --- |
| `contact360/dashboard/` | Dashboard app | `contact360.io/app/` |
| `contact360/marketing/` | Marketing site | `contact360.io/root/` |
| `contact360/docsai/` | Django DocsAI | `contact360.io/admin/` |
| `lambda/appointment360/` | GraphQL gateway | `contact360.io/api/` |
| `lambda/connectra/` | Connectra | `contact360.io/sync/` |
| `lambda/tkdjob/` | Job scheduler | `contact360.io/jobs/` |
| `lambda/mailvetter/` | Verifier | Often `backend(dev)/mailvetter/` here, or `lambda/mailvetter/` in other checkouts |

**Naming note:** historical docs used `extention/contact360` and `extension/contact360`. Current canonical extension package folder is **`extension/contact360/`**.

### `extension/` detail

- `contact360/` — Chrome extension for Sales Navigator workflows.

**Checkout note:** Some clones omit the `extension/` tree (e.g. backend-only worktrees). The **canonical** package path remains `extension/contact360/`; do not introduce new paths under the historical `extention/` spelling.

---

## Dashboard routes (product)

The authenticated dashboard uses the Next.js App Router under `contact360.io/app/app/(dashboard)/`.
```

```1:50:d:\code\ayan\contact\docs\versions.md
# Contact360 Release History

This file tracks meaningful releases only. It does not enumerate empty placeholder versions.

**Planning alignment:** Near-term cuts (`1.x`–`6.x`) are the default execution horizon. Strategic eras (`7.x`–`10.x`) are defined in `docs/roadmap.md` and `docs/architecture.md` (*Planning horizon*). Foundation (`0.x`) minors use `docs/0. Foundation and pre-product stabilization and codebase setup/version_0.*.md`. Other optional per-minor stubs may live under `docs/versions/version_*.md` when that folder is used. A major moving to `in_progress` here should still have matching roadmap stages and owners.

**Documentation index:** `docs/architecture.md` (system boundaries), `docs/codebase.md` (repo map), `docs/backend.md` (gateway + services), `docs/frontend.md` (dashboard, marketing, DocsAI, extension), `docs/flowchart.md` (diagrams), `docs/version-policy.md` (version policy). **Foundation era (`0.x`) minors:** `docs/0. Foundation and pre-product stabilization and codebase setup/version_0.*.md` and `0.x-master-checklist.md` in that folder. Optional generic stubs may also appear as `docs/versions/version_*.md` when present.

**Path convention:** Product code lives under **`contact360.io/`** (e.g. `app/` = dashboard, `api/` = Appointment360, `admin/` = DocsAI). Per-minor stubs may still mention legacy names such as `contact360/dashboard` — treat them as **`contact360.io/app/`** unless a release note says otherwise.

## Unreleased (next cut)

- **Target:** `1.1.0`
- **Status:** in_progress
- **Summary:** Complete bulk validation hardening and billing flow operationalization.
- **Planned stage mapping:** `1.3` (billing), `2.4` (bulk processing)
- **Owner:** Product + Platform Engineering

---

## Release index

| Version | Status | Released/Target | Summary |
| --- | --- | --- | --- |
| `0.1.0` | released | historical | **Monorepo bootstrap** — internal foundation baseline |
| `1.0.0` | released | historical | Contact360 MVP baseline — auth, credits, email core |
| `1.1.0` | in_progress | next cut | Bulk + billing maturity |
| `1.2.0` | planned | upcoming | Analytics, notifications, admin controls, security baseline |
| `2.0.0` | planned | TBD | Email system era — finder, verifier, results, bulk |
| `3.0.0` | planned | TBD | Contact and company data system era |
| `4.0.0` | planned | TBD | Extension and Sales Navigator maturity era |
| `5.0.0` | planned | TBD | AI workflows era |
| `6.0.0` | planned | TBD | Reliability and Scaling era |
| `7.0.0` | planned | TBD | Deployment era |
| `8.0.0` | planned | TBD | Public and private APIs era |
| `9.0.0` | planned | TBD | Ecosystem integrations and Platform productization era |
| `10.0.0` | planned | TBD | Email campaign era |

---

## Release entries

### `0.1.0`

- **Status:** released
- **Released on:** historical
- **Codename:** Monorepo bootstrap
- **Summary:** Initial monorepo, service skeletons, and product foundation setup.
- **Scope:** Base app/service directories, early integration scaffolding, CI pipelines, DocsAI bootstrap, and bootstrapping flows.
- **Roadmap mapping:** pre-v1 foundation work
```

```1:50:d:\code\ayan\contact\docs\roadmap.md
# Contact360 Roadmap

This roadmap defines staged delivery across major versions.  
Stage metadata standard for every stage:

- **Status**
- **Depends on**
- **Risk**
- **Definition of done**
- **KPI**
- **Ships in**

---

## Current focus

Delivery is currently centered on **billing and payments (Stage 1.3)** and **bulk validation hardening (Stage 2.4)**. Core **finder → verifier → results** flows remain the product backbone.

**Planning horizon:** near-term execution is **`1.x`–`6.x`** (this file + `docs/versions.md`). Strategic runway **`7.x`–`10.x`** is detailed in roadmap era sections below and in **`docs/architecture.md`** (*Planning horizon*). Optional per-minor notes: `docs/versions/version_*.md`. Strategic stages do not block current releases.

**Product surfaces:** Dashboard, marketing, DocsAI, and extension entry points are summarized in **`docs/frontend.md`**. Backend service index: **`docs/backend.md`**.

---

## VERSION 1.x — User, Billing and Credit System

### Stage 1.1 - User and Authentication System

**Status:** Completed
**Depends on:** Foundation platform setup  
**Risk:** Session handling regressions across dashboard and extension  
**Definition of done:** User can register, sign in, and begin usage with starter credits  
**KPI:** Successful signup-to-first-action conversion, auth failure rate  
**Ships in:** `1.0.0`

- Email signup and login
- Basic user profile
- Auto credit assignment (50 credits)
- Session management
- **Code pointers:** `contact360.io/app/src/context/RoleContext.tsx`, `contact360.io/api/app/main.py`

---

### Stage 1.2 - Credit Management System (CORE)

**Status:** Completed
**Depends on:** Stage 1.1  
**Risk:** Incorrect deduction and lapse behavior can block valid user actions  
**Definition of done:** Finder deductions and entitlement checks behave correctly under standard flows  
**KPI:** Credit ledger consistency, blocked-request correctness at zero balance  
```

```1:50:d:\code\ayan\contact\docs\governance.md
# Contact360 Docs and Service Governance

This file defines baseline governance for the monorepo and service skeletons.

## Monorepo baseline

- Product surfaces and APIs live under `contact360.io/`.
- Lambda-style services live under `lambda/`.
- Optional backend workspaces live under `backend(dev)/`.
- Browser extension code is canonical in `extension/contact360/`.
- **Frontend page inventory (supplementary):** `docs/frontend/` — JSON page specs under `docs/frontend/pages/`, CSV exports under `docs/frontend/excel/`, overview in `docs/frontend/README.md`. The **canonical live UI map** remains **`docs/frontend.md`** (dashboard `contact360.io/app/`, marketing `root/`, DocsAI `admin/`, extension).

## Mandatory docs synchronization

When editing architecture or roadmap docs, mirror updates in DocsAI constants:

- `docs/architecture.md` -> `contact360.io/admin/apps/architecture/constants.py`
- `docs/roadmap.md` -> `contact360.io/admin/apps/roadmap/constants.py`

Follow the full runbook in `docs/docsai-sync.md`.

## CI baseline

Repo-level checks run via `.github/workflows/ci.yml` to ensure:

- required top-level directories exist,
- DocsAI constants files exist,
- and core docs files are present.

## Release hygiene

- No major/minor stage status transitions without doc + constants sync.
- No new service path aliases unless reflected in architecture docs.

## Version era summary (canonical)

| Version | Theme |
| ------- | ----- |
| `0.x.x` | Foundation and pre-product stabilization and codebase setup |
| `1.x.x` | Contact360 user and billing and credit system |
| `2.x.x` | Contact360 email system |
| `3.x.x` | Contact360 contact and company data system |
| `4.x.x` | Contact360 Extension and Sales Navigator maturity |
| `5.x.x` | Contact360 AI workflows |
| `6.x.x` | Contact360 Reliability and Scaling |
| `7.x.x` | Contact360 deployment |
| `8.x.x` | Contact360 public and private APIs and endpoints |
| `9.x.x` | Contact360 Ecosystem integrations and Platform productization |
| `10.x.x` | Contact360 email campaign |
```

```1:50:d:\code\ayan\contact\docs\frontend.md
# Contact360 frontend map

> **Note:** This file is named `frontend.md` in the repository. It is the **frontend** (product UI) index — dashboard, marketing, DocsAI, and extension.

For **backend** services, see **`docs/backend.md`**. For the full monorepo and per-service code pointers, see **`docs/codebase.md`**. For system boundaries, see **`docs/architecture.md`**.

**Page inventory, component catalog, design system, and hooks/services docs** live under **`docs/frontend/`** (see **`docs/frontend/README.md`**). Canonical app code remains under **`contact360.io/`** below.

---

## Version era → primary UI surfaces (`0.x`–`10.x`)

Themes are defined in **`docs/version-policy.md`**. UI surface coverage at a glance:

| Era | Theme | Primary UI surfaces | Key UI elements introduced |
| --- | --- | --- | --- |
| `0.x` | Foundation | App shell, routing, design tokens | Layout, sidebar, auth shell, global CSS |
| `1.x` | User, billing, credit | Auth, profile, settings, billing, usage, admin | Login/register forms, billing modals, credit display, UPI payment, usage charts |
| `2.x` | Email system | Finder, verifier, results, export, jobs, files | Email input forms, result cards, progress bars, bulk upload, job status indicators |
| `3.x` | Contact & company data | Contacts, companies, search/filter UX | VQL query builder, data tables, filter sidebar, saved searches, company drill-down |
| `4.x` | Extension & Sales Navigator | `extension/contact360/` (Chrome), LinkedIn flows | Extension popup, SN ingestion panels, sync status indicators |
| `5.x` | AI workflows | AI chat, AI-assisted email writer, live voice | Chat message streams, AI confidence badges, streaming progress, AI tool panels |
| `6.x` | Reliability & scaling | Client resilience patterns | Error boundaries, retry UI, loading skeletons, offline banners |
| `7.x` | Deployment | RBAC-sensitive admin surfaces, DocsAI governance | Role-gated UI, feature flags, admin governance screens |
| `8.x` | Public & private APIs | API docs, integrations, analytics/reporting | API key manager, analytics charts, integration cards, reporting tables |
| `9.x` | Ecosystem & productization | Integrations hub, workspace/tenant admin | Integration setup wizards, entitlement indicators, plan upgrade flows |
| `10.x` | Email campaign | Campaign builder, audience, templates, send review | Campaign form, audience picker, email template editor, send progress tracker |

---

## Product applications (`contact360.io/`)

| Path | Role | Stack | Key docs |
| --- | --- | --- | --- |
| `contact360.io/app/` | Authenticated product (GraphQL-only client) | Next.js 16, React 19, modular CSS under `app/css/*` | `contact360.io/app/README.md`, `docs/DESIGN_UX.md`, `docs/API_DASHBOARD_MAPPING.md` |
| `contact360.io/root/` | Public marketing and growth pages | Next.js 16, custom CSS (BEM-like) | `contact360.io/root/README.md`; env: `GRAPHQL_URL`, dashboard URL for auth CTAs |
| `contact360.io/admin/` | Internal docs/admin mirror (roadmap & architecture constants) | Django | `docs/docsai-sync.md`, `contact360.io/admin/deploy/README.md` |

**Gateway contract:** All dashboard API traffic goes through **`contact360.io/api/`** GraphQL (`NEXT_PUBLIC_API_URL` / GraphQL URL in dashboard config).

---

## Browser extension

| Path | Role | Notes |
| --- | --- | --- |
| `extension/contact360/` | Chrome extension (Sales Navigator workflows) | **Canonical** path. Some clones omit `extension/`; see `docs/architecture.md` → *Service register*. Do not use `extention/` spelling for new work. |

Phase **4.x** Extension and Sales Navigator maturity (auth, telemetry, SN ingestion, sync) is tracked in **`docs/roadmap.md`** and **`docs/versions.md`**.
```

```1:50:d:\code\ayan\contact\docs\codebase.md
# Contact360 Codebase Deep Map

**Frontend surfaces (dashboard, marketing, DocsAI, extension):** see **`docs/frontend.md`**. **Backend services:** **`docs/backend.md`**.
**Deep per-service analyses:** see **`docs/codebases/README.md`**.

## Monorepo structure

| Path | Role | Primary tech |
| --- | --- | --- |
| `contact360.io/app/` | Authenticated product (dashboard) | Next.js 16, React 19, TypeScript |
| `contact360.io/root/` | Public marketing site | Next.js |
| `contact360.io/admin/` | DocsAI — internal roadmap/architecture mirrors | Django |
| `contact360.io/api/` | Appointment360 GraphQL gateway | FastAPI, Python |
| `contact360.io/sync/` | Connectra search / VQL | Go, Elasticsearch |
| `contact360.io/jobs/` | TKD Job scheduler and DAG workers | Python, Kafka |
| `lambda/emailapis/` | Finder/verifier orchestration | Python |
| `lambda/emailapigo/` | High-throughput finder (Go workers) | Go |
| `lambda/logs.api/` | Logging/telemetry ingestion | Python, S3 CSV + in-memory cache |
| `lambda/s3storage/` | File lifecycle and object storage | Python, S3 |
| `backend(dev)/mailvetter/` | Verification engine | Go |
| `backend(dev)/contact.ai/` | AI-driven workflows | Python |
| `backend(dev)/salesnavigator/` | Sales Navigator integration backend | Python |
| `backend(dev)/resumeai/` | Resume AI workflows | Python |
| `extension/contact360/` | Browser extension runtime | JS/TS extension stack |

**Legacy aliases:** older docs and full monorepos often use `contact360/dashboard`, `lambda/appointment360`, `lambda/connectra`, `lambda/tkdjob`, and `lambda/mailvetter/` — see **`docs/architecture.md`** → *Legacy / alternate names*.

**Service status:** see `docs/architecture.md` → *Service register (canonical)*.

## Core runtime contracts

- Client surfaces (`contact360.io/app`, extension) call **Appointment360** (`contact360.io/api`) as the primary contract gateway.
- Appointment360 orchestrates service calls to finder, verifier, search, scheduling, and storage services.
- Async flows run through **`contact360.io/jobs`**, with telemetry routed to `lambda/logs.api` and artifacts to `lambda/s3storage`.
- Search and enrichment behavior rely on **Connectra** (`contact360.io/sync`) (query/filter/index contract).

## Deep decomposition framework (how to break work)

Use five task tracks for every roadmap stage:

1. **Contract track**: GraphQL/API/event contract definitions and compatibility.
2. **Service track**: Backend implementation per owning service.
3. **Surface track**: Dashboard/extension/docsai UX and action wiring.
4. **Data track**: Storage, lineage, quality, and reconciliation.
5. **Ops track**: Observability, rollback safety, and release validation.

## `s3storage` focused implementation map

- Primary service: `lambda/s3storage/`
- API entrypoints: `app/api/v1/endpoints/uploads.py`, `files.py`, `schema.py`, `avatars.py`, `buckets.py`
```

```1:50:d:\code\ayan\contact\docs\backend.md
# Contact360 Backend (0.x-10.x)

Backend operating map for APIs, services, data stores, and era-aligned execution.

## Era-by-era backend surface

| Era | Theme | Modules | Tables | Service entrypoints |
|---|---|---|---|---|
| `0.x` | Foundation | auth, health | users, sessions | `api/main.py` |
| `1.x` | User/Billing/Credit | auth, users, billing, usage | users, user_profiles, addon_packages | auth/billing modules |
| `2.x` | Email system | email, jobs | scheduler_jobs, user_activities | email services + mailvetter |
| `3.x` | Contacts/Companies | contacts, companies | saved_searches | connectra + graphql modules |
| `4.x` | Extension/SalesNav | linkedin, sales_navigator | user_scraping | sales navigator service |
| `5.x` | AI workflows | ai_chats | ai_chats, resume_documents | contact.ai + resumeai |
| `6.x` | Reliability | cross-cutting guards | n/a | slo/error budget systems |
| `7.x` | Deployment | admin, governance | activities | deployment and audit controls |
| `8.x` | Public/private APIs | webhooks | webhooks | webhook dispatcher |
| `9.x` | Ecosystem | integrations | integrations | connector framework |
| `10.x` | Email campaign | campaigns, sequences, templates | campaigns, sequences, templates | campaign engine workers |

## Era-to-module additions table

| Era | API modules emphasized | Data emphasis |
| --- | --- | --- |
| `1.x` | auth/users/billing/usage | users, credits, plans, invoices |
| `2.x` | email/jobs/upload | email verification/finder lifecycle |
| `3.x` | contacts/companies/s3 | contacts and companies dual-store lineage |
| `4.x` | linkedin/sales navigator | ingestion and sync integrity |
| `5.x` | ai chats/jobs | AI prompt/result lineage |
| `6.x` | analytics/activities/health | reliability telemetry and RC evidence |
| `7.x` | admin/authz | governance and audit trails |
| `8.x` | webhooks/integrations | public-private contract lineage |
| `9.x` | profile/notifications/2fa | tenant and ecosystem controls |
| `10.x` | campaigns/sequences/templates | campaign execution and compliance |

## `s3storage` backend track by era

| Era | Contract tasks | Service tasks | Data/Ops tasks |
| --- | --- | --- | --- |
| `0.x` | Freeze upload/list/download endpoint contracts | Stabilize S3/filesystem backend parity | Baseline health and smoke checks |
| `1.x` | Define object class policy (`avatar`, `photo`, `resume`) | Validate content type/size per path | Audit fields and abuse monitoring |
| `2.x` | Freeze multipart API contract | Durable multipart session store | Metadata freshness and retry telemetry |
| `3.x` | Define ingestion artifact contract | Robust schema/preview/stats behavior | Lineage for ingest/export artifacts |
| `4.x` | Extension-safe access and TTL policy | Channel-aware access controls | Source provenance in metadata |
| `5.x` | Define AI artifact and retention contract | Policy enforcement for AI artifacts | Sensitive artifact audit trails |
| `6.x` | Define idempotency and SLO contract | Reconciliation and metadata write safety | Error budgets and incident runbooks |
| `7.x` | Define service-to-service auth contract | Endpoint authz and retention hooks | Compliance evidence generation |
| `8.x` | Define versioning/deprecation contract | Storage lifecycle event contracts | Compatibility and partner reliability gates |
| `9.x` | Define entitlement and quota contract | Plan-aware throttling and limits | Tenant cost/residency reporting |
| `10.x` | Define campaign artifact reproducibility contract | Immutable compliance storage paths | Compliance/audit sign-off evidence |
```

```1:50:d:\code\ayan\contact\docs\version-policy.md
# Contact360 Version Policy

## SemVer policy

- **Major (`X.0.0`)**: New product era, major channel expansion, or foundational architecture shift.
- **Minor (`X.Y.0`)**: New feature sets within an existing product era.
- **Patch (`X.Y.Z`)**: Bug fixes and reliability/performance improvements without scope expansion.
- **Ownership**: Product + engineering leads approve version bumps per shipped scope.

## Decision rubric (Contact360 specific)

- Use a **major** bump when introducing a new platform capability family (for example, moving from core user/billing to the email system era, or from email to contact/company data).
- Use a **minor** bump when adding a customer-visible capability in an existing major (for example, new billing flows, analytics panels, extension telemetry).
- Use a **patch** bump for hotfixes, edge-case fixes, retry logic hardening, and non-breaking operational updates.

## Release entry schema

Every release entry in `docs/versions.md` should include:

- `version`
- `status` (`released`, `in_progress`, `planned`)
- `released_on` (or `target_window` if planned)
- `summary`
- `scope`
- `Roadmap mapping` (roadmap stage IDs; canonical display label in `docs/versions.md`, equivalent to `ships_stages`)
- `owner`

## Version hygiene rules

- **Repo paths:** Canonical product and gateway paths are under **`contact360.io/`** (see `docs/architecture.md`). Older stubs may reference `contact360/dashboard` or `lambda/appointment360/` — align to `contact360.io/app/` and `contact360.io/api/` when editing links or code pointers.
- Do not pre-generate placeholder versions.
- Create version entries only when scope is approved (`planned`) or shipped (`released`).
- Keep `docs/versions.md` and `docs/roadmap.md` cross-referenced on every release update.
- Use `Roadmap mapping` as the release-entry field label consistently in `docs/versions.md`.

---

## Major themes (`0.x` to `10.0.0`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- Initial repository setup, service skeletons, CI pipelines, base authentication primitives, DocsAI bootstrap, and internal experiments.
- Core concern: repo hygiene, service wiring, and pre-product foundation readiness.

### `1.x.x` - Contact360 user and billing and credit system

- User authentication and session management, credit lifecycle (deduction, top-up, lapse), billing/payment flows, user-facing analytics, notifications, admin control panel, and basic security baseline.
- Core concern: the end-to-end user account lifecycle and credit economy.

### `2.x.x` - Contact360 email system
```

```1:50:d:\code\ayan\contact\docs\docsai-sync.md
# DocsAI Sync Runbook

## Purpose

DocsAI uses hardcoded constants for architecture and roadmap views. This runbook defines mandatory sync rules between markdown docs and DocsAI constants.

## Sync rules

1. If `docs/architecture.md` changes, update `contact360.io/admin/apps/architecture/constants.py` in the same change set.
2. If `docs/roadmap.md` changes, update `contact360.io/admin/apps/roadmap/constants.py` in the same change set.
3. If release taxonomy/policy changes in `docs/version-policy.md`, verify corresponding roadmap/version entries still match.

## Update checklist

- Architecture updates:
  - Update folder/service names and descriptions in `docs/architecture.md`.

  - Mirror those changes in `contact360.io/admin/apps/architecture/constants.py`.
  - Verify data-flow labels still match the architecture narrative.

- Roadmap updates:
  - Update stage details in `docs/roadmap.md` (`status`, `depends_on`, `risk`, `definition_of_done`, `kpi`, `ships_in`).
  - Mirror stage additions/updates in `contact360.io/admin/apps/roadmap/constants.py`.
  - Ensure every stage still maps to a release in `docs/versions.md`.

- Versioning updates:
  - Update policy in `docs/version-policy.md` when versioning rules change.
  - Update release entries in `docs/versions.md` with scope and stage mapping.
  - Confirm cross-links between roadmap and versions remain valid.

## Verification steps (DocsAI UI)

1. Open DocsAI architecture dashboard and confirm structure/service cards reflect the latest `constants.py`.
2. Open DocsAI roadmap dashboard and confirm stage list, statuses, and feature bullets match the roadmap constants.
3. Spot-check at least one updated stage from each of:
   - `1.x` user/billing/credit baseline,
   - `2.x` email system,
   - `3.x` contact and company data (Connectra),
   - `4.x` extension and Sales Navigator,
   - `5.x` AI workflows.
4. If mismatch appears, treat constants files as stale and re-sync before finalizing release docs.

## Release hygiene note

Do not ship docs-only version updates unless roadmap and DocsAI mirrors are synchronized.

## Deep sync workflow for staged execution

For every minor release stage (`X.Y.0`), process docs in this order:

1. Update `docs/roadmap.md` stage metadata and task bullets.
```

```1:50:d:\code\ayan\contact\docs\audit-compliance.md
# Audit, Compliance, and Governance (All Eras: 0.x–10.x)

> **Scope:** This document covers the full era range. Each service section details per-era compliance requirements from `0.x` (foundation) through `10.x` (email campaign). For full RBAC policy and role-enforcement patterns, see **`docs/7. Contact360 deployment/rbac-authz.md`**. For release and governance process, see **`docs/governance.md`**.

## RBAC matrix

| Capability | FreeUser | ProUser | Admin | SuperAdmin |
|---|---|---|---|---|
| Manage webhooks | no | yes | yes | yes |
| Manage integrations | no | yes | yes | yes |
| Create/schedule campaigns | no | yes | yes | yes |
| Approve billing submissions | no | no | yes | yes |

## Audit event schema

- event_id, event_time, actor_user_id, actor_role
- tenant_id, service, action, status
- target_type, target_id, request_id, metadata

## Tenant isolation

- Tenant scoped access required for all mutable resources
- Cross-tenant references return not-found semantics

## Era-specific RBAC and evidence mapping

- `7.x` is the RBAC baseline era and defines role enforcement patterns.
- `8.x` extends controls to partner/public API access and webhook identities.
- `9.x` extends controls to tenant/workspace/admin self-serve governance.
- `10.x` applies compliance controls to campaign consent, suppression,And opt-out audit trails.

## `s3storage` compliance controls by era

- `1.x`: enforce file type and size policy for user/billing artifacts.
- `2.x`: require multipart completion traceability (`uploadId`, part registration, completion evidence).
- `6.x`: require idempotent storage lifecycle operations and reconciliation evidence.
- `7.x`: enforce service-to-service authz for storage endpoints and retention policy controls.
- `8.x`: enforce versioned storage API behavior with compatibility tests.
- `10.x`: enforce immutable campaign compliance artifacts and retention/audit verifiability.

Mandatory evidence pack for storage-impacting releases:

- endpoint contract diff (if changed),
- metadata integrity/reconciliation report,
- access-control validation report,
- retention/deletion policy validation report.

## `logs.api` compliance controls by era

- `1.x`: user and billing event traceability with actor and request identifiers.
```

**Note:** In `audit-compliance.md`, line 30 should read **“suppression, and opt-out”** (the read merged “and” awkwardly—verify in-editor if needed).

**`flowchart.md` lines 1–50** (four backticks so inner ` ```mermaid ` blocks stay intact):

````markdown
# Contact360 Flowcharts

## Core request flow

```mermaid
flowchart LR
    user["User / Workspace"]
    dash["Dashboard / Extension"]
    mkt["Marketing"]
    gateway["appointment360 GraphQL"]
    finder["emailapis / emailapigo"]
    verify["mailvetter"]
    search["connectra"]
    jobs["tkdjob"]
    files["s3storage"]
    logs["logs.api"]
    ai["contact.ai"]

    user --> dash --> gateway
    user --> mkt
    mkt -->|"reads (GraphQL)"| gateway
    mkt -->|"auth CTAs"| dash
    gateway --> finder
    gateway --> verify
    gateway --> search
    gateway --> jobs
    gateway --> ai
    jobs --> files
    gateway --> logs
    jobs --> logs
```

Marketing is unauthenticated: it may call GraphQL for **read-only** product data where configured, and routes **sign-in / sign-up** flows to the dashboard for authenticated actions.

**Code paths (this monorepo):** GraphQL gateway → `contact360.io/api/`; Connectra → `contact360.io/sync/`; TKD Job → `contact360.io/jobs/`; dashboard → `contact360.io/app/`; marketing → `contact360.io/root/`. Shared email/log/storage services remain under `lambda/*`; Mailvetter and several integrations may live under `backend(dev)/` depending on checkout.

## Stage execution decomposition flow (per minor)

```mermaid
flowchart TD
    stage["Roadmap stage X.Y"]
    contract["Contract tasks"]
    service["Service tasks"]
    surface["Surface tasks"]
    data["Data tasks"]
    ops["Ops tasks"]
    release["Version entry + release gate"]

    stage --> contract
    stage --> service
    stage --> surface
````

(Line 50 in the file is `    stage --> surface`; the second diagram continues after that in the full file.)

**`docsai-sync.md`:** The checklist uses a single bullet “Architecture updates:” with sub-bullets; the excerpt above may have an extra blank line after the first sub-bullet compared to your exact file—compare with ```15:23:d:\code\ayan\contact\docs\docsai-sync.md``` on disk.

---

## 3. Files in `docs\analysis\`, `docs\plans\`, `docs\ideas\`, `docs\codebases\`, `docs\frontend\`, `docs\backend\`

Paths are under `d:\code\ayan\contact\docs\`.

### `analysis\` (41 files)

`cursor_1_x_x_era_documentation_extracti.md`, `cursor_2_x_x_era_documentation_extracti.md`, `cursor_3_x_x_era_codebase_analysis.md`, `cursor_3_x_x_era_documentation_extracti.md`, `cursor_4_x_x_era_codebase_analysis.md`, `cursor_codebase_analysis_content_retrie.md`, `cursor_codebase_analysis_content_retrie1.md`, `cursor_codebase_analysis_file_content_r.md`, `cursor_codebase_analysis_file_contents.md`, `cursor_contact360_api_documentation_ret.md`, `cursor_contact360_deployment_documentat.md`, `cursor_contact360_deployment_documentat1.md`, `cursor_contact360_documentation_and_cod.md`, `cursor_contact360_documentation_files_r.md`, `cursor_contact360_documentation_retriev.md`, `cursor_contact360_documentation_retriev3.md`, `cursor_contact360_documentation_summary.md`, `cursor_contact360_ecosystem_productizat.md`, `cursor_contact360_email_integration_exp.md`, `cursor_contact360_email_system_document.md`, `cursor_documentation_content_retrieval.md`, `cursor_documentation_content_summary_an.md`, `cursor_documentation_extraction_for_sta.md`, `cursor_documentation_folder_inventory.md`, `cursor_documentation_retrieval_for_user.md`, `cursor_email_api_system_exploration.md`, `cursor_email_apis_exploration_and_analy.md`, `cursor_email_architecture_and_behavior.md`, `cursor_email_system_architecture_explor.md`, `cursor_email_system_architecture_explor1.md`, `cursor_email_system_exploration_in_admi.md`, `cursor_email_system_exploration_in_mono.md`, `cursor_email_system_exploration_in_mono1.md`, `cursor_email_system_version_docs_enrich.md`, `cursor_era_mapping_and_execution_queue.md`, `cursor_file_content_retrieval_and_versi.md`, `cursor_file_content_structure_overview.md`, `cursor_file_listing_and_service_name_pr.md`, `cursor_mail_vetter_codebase_exploration.md`, `cursor_markdown_file_content_retrieval.md`, `cursor_reference_documents_for_version.md`

### `plans\` (28 files)

Same alphabetized list as in the draft above (`0.x_foundation_…` through `version_flowchart_sections_…`, including `3.x_docs_repair_&_enrich_99fbb766.plan.md`).

### `ideas\` (2,529 files)

Full path list omitted here. Includes **`ideas\README.md`** and large nested trees (**`admin\`**, **`api\`**, **`app\`**, **`job\`**, **`jobs\`**, **`mailvetter\`**, **`resume\`**, **`root\`**, **`s3storage\`**, **`sync\`**, etc.) with **nested `.git`**, **`.ssh`**, **`.docker`**, and application source. Repository tools cap long file listings (e.g. ripgrep matched at least **2,600** paths before truncation).

### `codebases\` (16 files)

`README.md`, `admin-codebase-analysis.md`, `app-codebase-analysis.md`, `appointment360-codebase-analysis.md`, `connectra-codebase-analysis.md`, `contact-ai-codebase-analysis.md`, `emailapis-codebase-analysis.md`, `emailcampaign-codebase-analysis.md`, `email-codebase-analysis.md`, `extension-codebase-analysis.md`, `jobs-codebase-analysis.md`, `logsapi-codebase-analysis.md`, `mailvetter-codebase-analysis.md`, `root-codebase-analysis.md`, `salesnavigator-codebase-analysis.md`, `s3storage-codebase-analysis.md`

### `frontend\` (65 files)

`excel\` (6 CSV + `README.md`), `docs\` (9 md including `README.md`), `pages\` (49 JSON + `README.md`) — exact names listed in §1 / earlier complete enumeration (`about_page.json` … `verifier_page.json`, `pages_index.json`, `index.json`, etc.).

### `backend\` (3,431 files)

- **`apis\`:** 38 files (`01_AUTH_MODULE.md` … `29_RESUME_AI_REST_SERVICE.md`, `README.md`, `*_ERA_TASK_PACKS.md`).
- **`database\`:** 55 files (`*_data_lineage.md`, `migrations\*.sql`, `tables\*.sql` + `README.md`, `table_data\` CSV/SQL + `README.md`).
- **`endpoints\`:** 197 JSON files (`endpoints_index.json`, era matrices, per-operation specs).
- **`postman\`:** 3,138 files — root `README.md`, product folders (`Contact360 GraphQL API - Complete`, `Connectra API`, `Email Campaign API`, `Resume AI Service1`, …), plus many third-party-style collection trees (e.g. `📌 xAI API`, `📌 Together AI API`) and loose `*.json` / `*.postman_collection.json`.

---

If you need a **single flat export of all 6,439 paths** (or all 2,529 under `ideas\`), say which branch you want and we can do that in Agent mode with a script, since Ask mode avoids generating new files/commands that write to disk.

