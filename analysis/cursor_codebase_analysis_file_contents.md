# Codebase analysis file contents
_Exported on 3/26/2026 at 17:11:50 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files and return their full contents (first 80 lines of each):
1. d:\code\ayan\contact\docs\codebases\admin-codebase-analysis.md
2. d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md
3. d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md
4. d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md
5. d:\code\ayan\contact\docs\codebases\emailcampaign-codebase-analysis.md
6. d:\code\ayan\contact\docs\codebases\extension-codebase-analysis.md
7. d:\code\ayan\contact\docs\codebases\logsapi-codebase-analysis.md
8. d:\code\ayan\contact\docs\codebases\root-codebase-analysis.md
9. d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md
10. d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md

Return the first 80 lines of each file showing era mapping and 9.x task breakdown sections.

---

**Cursor**


Reading the first 80 lines of each file in parallel.




Checking which files include a `9.x` task section and where it appears (may be past line 80):




Here is a **coverage summary** for what you asked for (era mapping + **9.x task** style content in the **first 80 lines**), then the **verbatim first 80 lines** of each file.

### Coverage in lines 1–80

| File | Era mapping in 1–80 | `9.x` / task-pack style in 1–80 |
|------|---------------------|----------------------------------|
| `admin-codebase-analysis.md` | Yes — `## Era alignment` (bullet list through `10.x`) | Only a **one-line** `9.x` bullet, not a task subsection |
| `app-codebase-analysis.md` | Same as admin | Same |
| `email-codebase-analysis.md` | Partial — **Era** column in route table only; full `## Era alignment` starts at **line 102** | **No** — `9.x` row is in the era table **after** line 80 |
| `emailapis-codebase-analysis.md` | **No** era bullet list; **Era-by-era task packs** start at **line 70** (only `0.x`–`1.x` in first 80) | **No** — `### 9.x Ecosystem integrations` is at **line 135** |
| `emailcampaign-codebase-analysis.md` | Only **line 6** mentions `10.x`; no era table in first 80 | **No** — `9.x` row in a table around **line 106** |
| `extension-codebase-analysis.md` | **No** in first 80; era-style row for `9.x` around **line 128** | **No** |
| `logsapi-codebase-analysis.md` | **Yes** — `## Era-by-era task packs` from **line 33** through **`6.x` starting line 77** | **No** — `### 9.x Ecosystem integrations` at **line 98** |
| `root-codebase-analysis.md` | Yes — `## Era alignment` | Only **one-line** `9.x` bullet |
| `s3storage-codebase-analysis.md` | Only intro **line 3** mentions `0.x.x`–`10.x.x`; **`## Contact360 era mapping` at line 125** | **No** — **`## 9.x.x` at line 320** |
| `salesnavigator-codebase-analysis.md` | **Lines 6–8** (era + pointer to `SALESNAVIGATOR_ERA_TASK_PACKS.md`) | **No** — `### 9.x — Ecosystem/Productization` around **line 338** |

So **none** of these files fits “full era matrix + full **9.x** task breakdown” entirely inside the **first 80 lines**; several point to **`9.x` only later** or only as a **single bullet** under “Era alignment.”

---

### 1. `d:\code\ayan\contact\docs\codebases\admin-codebase-analysis.md` (lines 1–80)

The tool read shows **79 lines total** for this file (line 80 absent). Content:

```markdown
# contact360.io/admin codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`contact360.io/admin` is the Django-based DocsAI and admin governance surface for Contact360. It provides roadmap and architecture mirrors, operational admin functions, and internal graph/documentation tooling.

## Runtime architecture

- Framework: Django (templates + static assets)
- Base route map: `contact360.io/admin/docsai/urls.py`
- Core auth/dashboard views: `contact360.io/admin/apps/core/views.py`
- Documentation dashboard: `contact360.io/admin/apps/documentation/views/dashboard.py`
- Admin operations views: `contact360.io/admin/apps/admin/views.py`
- Navigation registry: `contact360.io/admin/apps/core/navigation.py` (`SIDEBAR_MENU`)

## UI/UX inventory

### Templates and navigation

- Shared shell: `templates/base.html` with conditional authenticated sidebar/header layout.
- Roadmap view: `templates/roadmap/dashboard.html` with preview/edit tabs, progress bar, radio status filters.
- Architecture view: `templates/architecture/blueprint.html` with preview/edit tabs, readiness progress, radio filters.
- Sidebar groups in `SIDEBAR_MENU`: Documentation, Analysis, AI, Automation, Management, Admin, Tools and Info.

### UI elements and static components

- Buttons: `static/css/components/button.css`
- Input/select/textarea/radio groups: `static/css/components/form-inputs.css`
- Tabs: `static/css/components/tabs.css`
- Progress bars: `static/css/components/progress.css` and `templates/components/progress.html`
- Graph rendering styles: `static/css/components/graph.css`

### Graph and flow components

- Force-directed documentation relationship graph: `static/js/components/relationship-graph-viewer.js` (D3.js)
- Generic graph rendering path: `static/js/components/graph.js` (Cytoscape.js)

## Backend/API/data inventory

### GraphQL clients and service bridge

- Shared Python GraphQL client: `apps/core/services/graphql_client.py` (httpx, retry, exponential backoff, cache)
- Appointment auth/profile bridge: `apps/core/clients/appointment360_client.py`
- Admin operations bridge: `apps/admin/services/admin_client.py`

### Access control

- Decorator-based protection including:
  - `require_super_admin`
  - `require_admin_or_super_admin`

### Data sources

- Local Django persistence (SQLite in local/dev workflows)
- Appointment360 GraphQL APIs for operational data
- S3 indices/artifacts used by documentation dashboards
- Redis cache for selected dashboard aggregation paths

## Era alignment (`0.x`-`10.x`)

- `0.x`: Django shell, auth views, base navigation and template system
- `1.x`: billing/admin payment review and user governance controls
- `2.x`: email documentation and operational controls across finder/verifier areas
- `3.x`: contact/company relationship documentation and graph surfaces
- `4.x`: extension/Sales Navigator governance visibility in docs and admin views
- `5.x`: AI/automation sections and internal AI control panes
- `6.x`: reliability guardrails, health/system views, operational checks
- `7.x`: deployment governance, RBAC hardening, admin operational lifecycle
- `8.x`: API and endpoint documentation, schema and internal public/private API governance
- `9.x`: integrations and platform productization governance views
- `10.x`: campaign governance, release alignment, and compliance-related UI controls

## Key findings and risks

1. Docs currently under-document Django-specific access decorators and view-level RBAC.
2. D3/Cytoscape graph surface is high-impact but thinly mapped in docs.
3. Deployment runbooks in `deploy/` should be reflected in governance and sync docs.
4. SIDEBAR_MENU drift risk exists if navigation constants change without docs updates.
```

---

### 2. `d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md` (lines 1–80)

```markdown
# contact360.io/app codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`contact360.io/app` is the authenticated Contact360 dashboard. It is a Next.js 16 + React 19 + TypeScript app that drives core product workflows (auth, billing/credits, email finder/verifier, contacts/companies, jobs/files, admin, AI, integrations) over GraphQL.

## Runtime architecture

- Root layout and providers: `contact360.io/app/app/layout.tsx`
- Authenticated gate/layout: `contact360.io/app/app/(dashboard)/layout.tsx`
- Core shell: `contact360.io/app/src/components/layout/MainLayout.tsx`, `Sidebar.tsx`
- GraphQL client: `contact360.io/app/src/lib/graphqlClient.ts`
- Config and environment: `contact360.io/app/src/lib/config.ts`
- Contexts: `src/context/AuthContext.tsx`, `RoleContext.tsx`, `ThemeContext.tsx`, `DashboardPageContext.tsx`

## UI/UX inventory

### Pages and route groups

- Auth pages: login/register/session-related routes
- Dashboard pages: billing, usage, contacts, companies, email tools, files, jobs, profile, analytics, admin, AI, integrations
- Layout patterns: `MainLayout`, `DashboardPageLayout`, `DataPageLayout`, `ToolPageLayout`

### UI primitives and controls

- Components exported from `src/components/ui/index.ts`: `Button`, `Input`, `Tabs`, `Badge`, `Modal`, `ConfirmModal`, `Alert`, `Popover`
- Progress bars: upload and usage/credit surfaces (`UploadProgressBar` and layout alerts)
- Checkbox/radio usage: table row selection and profile/settings notification toggles (input type checkboxes; radios in specific forms where applicable)
- Graph/chart UI: Recharts components for dashboard analytics (for example line chart summaries)

## Hooks, services, contexts

### Hooks (major domains)

- Auth/session: `useLoginForm`, `useRegisterForm`, `useSessionGuard`, `useSessions`
- Billing/usage: `useBilling`, `useFeatureOverview`
- Email: `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`
- Data/files: `useFiles`, `useCsvUpload`, `useFilePreview`, `useFileStats`
- Product domains: `useContacts*`, `useCompanies*`, `useLinkedIn`, `useAnalytics`, `useAdmin`, `useTeam`
- UI behavior: modal/sidebar/resizable/debounce and page access helpers

### GraphQL services (`src/services/graphql`)

- Auth/users/profile/two-factor
- Contacts/companies/saved searches
- Billing/usage/notifications/exports
- Email/jobs/s3/upload
- Admin/analytics/pages/linkedin/sales navigator/activities/health

### Contexts

- `AuthContext`: user + token lifecycle + visible pages
- `RoleContext`: feature gates, plan/limits/credits
- `ThemeContext`: global theme behavior
- `DashboardPageContext`: page-level access and data coordination

## Backend API, endpoints, database coupling

- Dashboard uses GraphQL via Appointment360 as the main contract path.
- Page APIs batch GraphQL calls for dashboard routes.
- No direct DB access from the frontend; data ownership remains in backend services.

## Era alignment (`0.x`-`10.x`)

- `0.x`: shell, auth gate, foundational contexts, shared UI primitives
- `1.x`: user, billing, credits, usage and role/plan surfaces
- `2.x`: email finder/verifier workflows and bulk file/job progress UX
- `3.x`: contacts/companies search, tables, filters, saved-search workflows
- `4.x`: extension/Sales Navigator and LinkedIn-integrated surfaces
- `5.x`: AI chat/assistant and AI-assisted workflow surfaces
- `6.x`: reliability patterns (guards, retries, health feedback)
- `7.x`: admin/deployment/governance role-aware dashboard controls
- `8.x`: API/platform analytics and private/public endpoint-aligned product pages
- `9.x`: integrations and ecosystem productization UX
- `10.x`: campaign-oriented product surfaces and supporting controls

## Key findings and risks

1. Dashboard docs are strong but should be represented in the same deep-analysis format as root/admin for consistency.
2. API module mapping is broad; contract drift needs continuous sync with docs/backend module docs.
```

*(File continues after line 80 with more “Key findings” bullets.)*

---

### 3. `d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md` (lines 1–80)

```markdown
# Email App Codebase Analysis — `contact360.io/email`

## Overview

`contact360.io/email` is a Next.js 16 + React 19 frontend surface for Mailhub-style mailbox operations. It is primarily a UI/runtime layer that consumes backend REST endpoints through `NEXT_PUBLIC_BACKEND_URL` and does not own database persistence directly.

Primary concerns:
- Folder mailbox browsing (`inbox`, `sent`, `spam`, `draft`)
- Single email rendering by ID
- Account profile and IMAP account management
- Auth entrypoints (`/auth/login`, `/auth/signup`)

## Stack

| Layer | Technology |
| --- | --- |
| Framework | Next.js 16 (App Router) |
| UI | React 19, Tailwind CSS, Radix UI wrappers |
| State | React local state + Context (`ImapContext`) |
| Table | `@tanstack/react-table` |
| Charts | Recharts wrapper (`ui/chart.tsx`, optional) |
| Security helper | `isomorphic-dompurify` for HTML email body sanitization |
| API transport | native `fetch` |

## Route and page inventory

| Route | File | Purpose | Era |
| --- | --- | --- | --- |
| `/` | `src/app/page.tsx` | Marketing/landing entry | 0.x |
| `/auth/login` | `src/app/auth/login/page.tsx` | Login entry | 1.x |
| `/auth/signup` | `src/app/auth/signup/page.tsx` | Signup entry | 1.x |
| `/inbox` | `src/app/inbox/page.tsx` | Inbox list surface | 2.x |
| `/sent` | `src/app/sent/page.tsx` | Sent folder list | 2.x |
| `/spam` | `src/app/spam/page.tsx` | Spam folder list | 2.x |
| `/draft` | `src/app/draft/page.tsx` | Draft folder list | 2.x |
| `/email/[mailId]` | `src/app/email/[mailId]/page.tsx` | Email body view | 2.x |
| `/account/[userId]` | `src/app/account/[userId]/page.tsx` | Profile + IMAP account settings | 1.x/2.x |

## UI elements and controls

- **Tabs:** `DataTable` uses tabs for `all`, `unread`, `flagged`.
- **Buttons:** global action buttons in nav (`Compose`), row actions (`Reply`, `Mark as read`, `Delete`), profile/account actions.
- **Inputs:** auth forms, account settings, IMAP connect form, table filter input.
- **Text system:** dark-mode typography and status labels (`Success`, `Error`, mailbox hints).
- **Checkboxes:** row selection and select-all in mailbox table.
- **Progress:** spinner/loading states implemented; no dedicated numeric progress bar component yet.
- **Radio buttons:** no dedicated radio flow currently wired in mailbox UI.
- **Graph/chart:** chart primitives exist in `ui/chart.tsx`, not yet integrated into mailbox pages.

## Components and key files

| Component/File | Role |
| --- | --- |
| `components/LayoutClient.tsx` | Route-aware shell (auth/home bypass sidebar; app routes use sidebar) |
| `components/app-sidebar.tsx` | Folder and tool navigation, user fetch |
| `components/nav-main.tsx` | Main nav links + compose quick action |
| `components/nav-user.tsx` | User menu + logout |
| `components/email-list.tsx` | Folder fetch orchestration + loading/error states |
| `components/data-table.tsx` | Table rendering, filters, pagination, row actions |
| `components/login-form.tsx` | Login REST call and local user ID persistence |
| `components/signup-form.tsx` | Signup REST call |
| `context/imap-context.tsx` | Active IMAP account context and localStorage persistence |

## Hooks, contexts, services

- **Contexts**
  - `ImapProvider` stores `activeAccount`, `setActiveAccount`, `isLoading`.
- **Hooks**
  - `useImap()` context accessor.
  - `useIsMobile()` for mobile breakpoint detection.
- **Service pattern**
  - No central service module yet; direct `fetch` inside components/pages.
  - `BACKEND_URL` sourced from `NEXT_PUBLIC_BACKEND_URL`.

## Backend APIs used by this app

| Endpoint | Method | Called from |
| --- | --- | --- |
| `/auth/login` | POST | `login-form.tsx` |
| `/auth/signup` | POST | `signup-form.tsx` |
```

---

### 4. `d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md` (lines 1–80)

```markdown
# emailapis / emailapigo codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`lambda/emailapis` (Python FastAPI) and `lambda/emailapigo` (Go Gin) are Contact360's dual-runtime email execution services for finder, verifier, pattern add, and web-search fallback flows. They sit behind Appointment360 GraphQL and power both interactive and bulk email workloads.

## Runtime architecture

- Python entrypoint: `lambda/emailapis/app/main.py`
- Python router: `lambda/emailapis/app/api/v1/router.py`
- Go entrypoint: `lambda/emailapigo/main.go`
- Go router: `lambda/emailapigo/internal/api/router.go`
- Finder services: `app/services/email_finder_service.py`, `internal/services/email_finder_service.go`
- Verifier services: `app/services/email_verification_service.py`, `internal/services/email_verification_service.go`
- Pattern services: `app/services/email_pattern_service.py`, `internal/services/email_pattern_service.go`
- Data repositories: cache + pattern repositories in both runtimes

## API contract snapshot

- `POST /email/finder/`
- `POST /email/finder/bulk`
- `POST /email/single/verifier/`
- `POST /email/bulk/verifier/`
- `POST /email-patterns/add`
- `POST /email-patterns/add/bulk`
- `POST /web/web-search`
- `GET /health`, `GET /`

## Data model and persistence

### `email_finder_cache`
- Identity keys: `first_name`, `last_name`, `domain` (case-insensitive)
- Result fields: `email_found`, `email_source`
- Constraints: unique identity + lookup index
- Role: short-path cache hit before provider fanout

### `email_patterns`
- Keys: `uuid`, `company_uuid`, `domain`
- Pattern fields: `pattern_format`, `pattern_string`
- Metrics: `contact_count`, `success_rate`, `error_rate`
- Role: learned pattern persistence used by finder flows

## Provider orchestration and behavior

### Finder flow (both runtimes)
1. Cache lookup (`email_finder_cache`)
2. Parallel provider candidates:
   - Connectra
   - Pattern service
   - Generator
3. Race verification of candidates
4. Fallback discovery:
   - Web search
   - IcyPeas
5. Return normalized list and source attribution

### Verifier flow
- Python defaults commonly reference `truelist` + `icypeas`
- Go health and runtime prefer `mailvetter` + `icypeas` (`mailvetter_configured` check)
- Bulk paths use concurrency controls and stagger/timeout behavior

## Key findings and cross-service risks

1. Provider drift risk: Python/docs often reference `truelist`; Go runtime prioritizes `mailvetter`.
2. Status semantic drift risk: `valid`/`invalid`/`catchall`/`unknown` interpretation can differ across app, api, and runtime mapping.
3. Observability gap: correlation across app -> api -> jobs -> lambda is not consistently documented with one trace contract.
4. Contract drift risk: endpoint and payload assumptions in docs may lag runtime changes.
5. Bulk correctness risk: partial-batch error mapping and retry semantics require explicit cross-layer contract tests.

## Era-by-era task packs (Contract / Service / Surface / Data / Ops)

### 0.x Foundation
- Contract: freeze base endpoint envelope and health diagnostics keys.
- Service: stabilize startup/middleware/error translation in both runtimes.
- Surface: document baseline finder/verifier UI states for core shell.
- Data: lock cache/pattern table schema baseline.
- Ops: add smoke checks for Python and Go runtimes.

### 1.x User/Billing/Credit
- Contract: align credit-impact operation contract at GraphQL boundary.
```

---

### 5. `d:\code\ayan\contact\docs\codebases\emailcampaign-codebase-analysis.md` (lines 1–80)

```markdown
# Email Campaign Codebase Analysis (`backend(dev)/email campaign`)

## Purpose and role

`backend(dev)/email campaign` is Contact360's campaign delivery engine. It owns template management, asynchronous bulk email dispatch, SMTP-level send, per-recipient tracking, and unsubscribe/suppression enforcement. It is the `10.x` execution runtime that the planned campaign UI, wizard, and sequence engine will drive through the gateway.

## Current architecture snapshot

- **Runtime:** Go 1.24, Gin HTTP server, Asynq job queue, Redis.
- **Data:** PostgreSQL (`campaigns`, `recipients`, `suppression_list`, `templates`).
- **Storage:** AWS S3 (template HTML files; key `templates/{id}.html`).
- **Two binaries:** API server (`cmd/main.go`) + Asynq worker (`cmd/worker/main.go`).
- **Concurrency model:** 5 goroutines per campaign consume from a buffered channel; `sync.WaitGroup` joins all workers before marking status `completed`.

## Route surface

| Route | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Liveness probe |
| `/campaign` | POST | Enqueue campaign send job (template_id + name + filepath) |
| `/unsub` | GET | JWT-signed unsubscribe (sets suppression + updates recipient status) |
| `/list/mailbox` | GET | IMAP mailbox listing |
| `/list/inbox` | GET | IMAP inbox fetch (latest 10 messages) |
| `/body/:uid` | GET | IMAP fetch email body by UID |
| `/templates` | POST | Create template (upload HTML to S3, insert metadata to DB) |
| `/templates` | GET | List all templates |
| `/templates/:id` | GET | Get single template |
| `/templates/:id` | DELETE | Delete template (S3 + DB + cache invalidation) |
| `/templates/:id/preview` | POST | Render template with sample recipient data |

## Core mechanics

### Campaign send flow

1. `POST /campaign` → saves `campaigns` row, enqueues `campaign:send` task on Asynq/Redis.
2. Asynq worker picks up task → marks status `sending` → fetches template from S3.
3. CSV file loaded from path → goroutine filters suppressed emails → inserts `recipients` rows.
4. 5 concurrent `EmailWorker` goroutines consume recipient channel → render HTML from S3-backed template → SMTP send.
5. Per-recipient: success → `sent` status + `IncrementSent`; failure → `failed` status + `IncrementFailed`.
6. After all workers: campaign status → `completed`.

### Template system

- HTML template stored in S3 under `templates/{id}.html`.
- In-memory cache layer (`Service.cache`) with `sync.RWMutex`; cache miss fetches from S3.
- `RenderString` method supports Go template syntax in subject line (`{{.FirstName}}` etc.).
- `TemplateData` struct: `FirstName`, `LastName`, `Email`, `UnsubscribeURL`.

### Unsubscribe token

- JWT (HS256) signed with `JWT_SECRET`, 30-day expiry.
- Claims: `email`, `campaign_id`.
- `GET /unsub?token=...` validates → inserts `suppression_list` → updates `recipients.status = 'unsubscribed'`.

### Queue architecture

- Primary path: Asynq (built on Redis); task type `campaign:send`.
- Secondary path: Raw Redis list helper (`queue/reddis_queue.go`) — appears to be legacy/experimental parallel path.

## Data model

| Table | Columns | Purpose |
| --- | --- | --- |
| `campaigns` | id, title, status, filepath, total, sent, failed, created_at | Campaign execution record |
| `recipients` | id, campaign_id, email, name, status, error, sent_at, unsub_token | Per-recipient send status |
| `suppression_list` | email, reason, created_at | Global opt-out/bounce list |
| `templates` | id, name, subject, s3_key, created_at, updated_at | Template metadata (HTML in S3) |

## Strengths

- Clean two-binary split (API server + async worker) for independent scaling.
- In-memory template cache avoids S3 round-trip on every recipient.
- Unsubscribe mechanism with JWT-based tamper-proof token.
- Concurrency-safe 5-worker fan-out with WaitGroup synchronization.
- Suppression check before each send prevents emailing opted-out recipients.

## Gaps and risks

| Risk | Severity | Notes |
| --- | --- | --- |
```

---

### 6. `d:\code\ayan\contact\docs\codebases\extension-codebase-analysis.md` (lines 1–80)

```markdown
# Extension Codebase Analysis — `extension/contact360`

## Overview

The `extension/contact360` package is the **logic and transport layer** for the Contact360 Chrome Extension (Sales Navigator integration). It does **not** contain the extension popup UI or HTML content scripts directly — those would live in a separate UI tree. This package provides:

1. **Auth/Session management** (`auth/graphqlSession.js`) — JWT lifecycle, proactive token refresh, `chrome.storage.local` adapter.
2. **Lambda REST client** (`utils/lambdaClient.js`) — production-grade batched HTTP client for `POST /v1/save-profiles`.
3. **Profile merger/dedup** (`utils/profileMerger.js`) — merges duplicate SN profile objects by completeness score.

---

## Stack

| Layer | Technology |
| --- | --- |
| Language | JavaScript (ES6+, no transpile step needed) |
| Extension API | Chrome MV3 (`chrome.storage.local`, `chrome.runtime`) |
| Auth backend | Appointment360 GraphQL (`auth.refreshToken` mutation) |
| Data endpoint | Lambda Sales Navigator API — `POST /v1/save-profiles` |
| Contact sync | Connectra — `POST /contacts/bulk`, `POST /companies/bulk` |
| Testing | Jest (unit tests in `tests/`) |
| Documentation | Markdown (`docs/README.md`, `docs/IMPLEMENTATION_SUMMARY.md`) |

---

## File Map

```
extension/contact360/
├── auth/
│   └── graphqlSession.js          # JWT session lifecycle + token refresh
├── utils/
│   ├── lambdaClient.js            # Batched Lambda REST client
│   └── profileMerger.js           # Profile dedup + merge utilities
├── tests/
│   ├── hybridFlow.test.js         # Integration: session + client flow
│   ├── profileMerger.test.js      # Unit: merge/dedup logic
│   └── lambda-client-test.js     # Unit: lambdaClient retry + batching
├── docs/
│   ├── README.md                  # Sales Navigator API service overview
│   └── IMPLEMENTATION_SUMMARY.md  # Implementation status and file list
└── README.md                      # Package-level service documentation
```

---

## Module Deep Dive

### `auth/graphqlSession.js`

**Purpose:** Manages the GraphQL JWT session for the extension runtime.

**Key functions:**
| Function | Behaviour |
| --- | --- |
| `decodeJWT(token)` | Base64url-decodes the JWT payload; no external library |
| `isTokenExpired(token, bufferSeconds?)` | Returns `true` if `exp` is within `bufferSeconds` (default: 300 s = 5 min) |
| `getStoredTokens()` | Reads `{ accessToken, refreshToken }` from `chrome.storage.local` |
| `storeTokens(tokens)` | Persists both tokens to `chrome.storage.local` |
| `refreshAccessToken(refreshToken)` | Calls Appointment360 `auth.refreshToken` mutation via `fetch`; stores result |
| `getValidAccessToken()` | Checks expiry, calls `refreshAccessToken` proactively; returns valid token |

**Chrome MV3 adapter note:** All storage calls use `chrome.storage.local.get`/`set` wrapped in Promises (no `chrome.storage.sync` to avoid quota issues for tokens).

---

### `utils/lambdaClient.js`

**Purpose:** Production-grade REST client for submitting scraped SN profiles to the Lambda Sales Navigator API.

**Key capabilities:**
| Capability | Implementation |
| --- | --- |
| Batching | Splits profile arrays into chunks (default `BATCH_SIZE = 10`) |
| Retry | Exponential back-off with jitter; configurable `maxRetries` (default 3) |
| Adaptive timeout | Increases timeout per retry to handle slow cold-starts |
| Payload compression | `JSON.stringify` with optional field pruning (strips `null`/`undefined` keys) |
| Request queuing | Serial queue prevents parallel flood; one batch at a time |
| Auth header | Injects `Authorization: Bearer <token>` from `getValidAccessToken()` |
```

---

### 7. `d:\code\ayan\contact\docs\codebases\logsapi-codebase-analysis.md` (lines 1–80)

```markdown
# logs.api codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`lambda/logs.api` is a FastAPI logging service that stores log records in S3 CSV objects and provides CRUD/query/search/statistics endpoints for operational and audit use-cases across Contact360.

## Runtime architecture

- Entrypoint: `lambda/logs.api/app/main.py`
- Routing: `app/api/v1/endpoints/logs.py`, `app/api/v1/endpoints/health.py`
- Service layer: `app/services/log_service.py`
- Data repository: `app/models/log_repository.py`
- Storage client: `app/clients/s3.py`
- Caching and telemetry: `app/utils/query_cache.py`, `query_monitor.py`, `cache_metrics.py`
- Deployment contract: `lambda/logs.api/template.yaml`

## Key findings and risks

1. Documentation drift: multiple docs still describe MongoDB, but implementation is S3 CSV.
2. Security risk: static API key pattern is used across service-to-service calls and examples.
3. Query scalability risk: heavy range scans on CSV objects can become expensive at higher traffic.
4. Cache consistency risk: in-memory cache is per-instance and not globally coherent.
5. Compliance risk: docs and evidence packs must clearly tie retention and audit behavior to deployed policy.

## API contract snapshot

- `POST /logs`, `POST /logs/batch`
- `GET /logs`, `GET /logs/search`, `GET /logs/{log_id}`
- `PUT /logs/{log_id}`, `DELETE /logs/{log_id}`
- `POST /logs/delete`, `DELETE /logs`
- `GET /health`, `GET /health/info`

## Era-by-era task packs (Contract / Service / Surface / Data / Ops)

### 0.x Foundation
- Contract: define health and write/read baseline envelope for logs.api.
- Service: stabilize S3 CSV write/read path and startup health checks.
- Surface: wire baseline health visibility in internal tooling (no user-facing UI dependency).
- Data: define object naming convention, timestamp normalization, and minimal schema.
- Ops: smoke tests and startup checklist for local and Lambda environments.

### 1.x User/Billing/Credit
- Contract: define auth, billing, and credit event logging schema.
- Service: ensure gateway writes user lifecycle events with request/tenant/user IDs.
- Surface: activity indicators for user and billing flows.
- Data: event lineage to billing and usage modules.
- Ops: abuse monitoring for repeated auth/payment failures.

### 2.x Email system
- Contract: email finder/verifier job-event schema and status transitions.
- Service: high-volume batch write path for job progress and completion events.
- Surface: progress bars and job timelines in results/bulk pages.
- Data: retention and query windows for high-throughput logs.
- Ops: alerting for verifier/finder failure spikes.

### 3.x Contacts/Companies
- Contract: contact/company enrichment and dedupe log contract.
- Service: query filters by service, workspace, and operation class.
- Surface: searchable operational log panels for data support flows.
- Data: lineage tie-back to search/enrichment operations.
- Ops: anomaly checks on dedupe/enrichment failure clusters.

### 4.x Extension/Sales Navigator
- Contract: extension ingestion/sync event schema.
- Service: extension source tagging and provenance fields.
- Surface: extension telemetry and sync diagnostics panels.
- Data: source-of-truth tags for extension-generated events.
- Ops: replay diagnostics for ingestion regressions.

### 5.x AI workflows
- Contract: AI prompt, tool, and response telemetry schema.
- Service: log write guards for sensitive payload minimization.
- Surface: AI debug traces and troubleshooting views for internal teams.
- Data: retention segmentation for AI-sensitive telemetry.
- Ops: cost and error anomaly dashboards from logs.api aggregates.

### 6.x Reliability and scaling
- Contract: SLO/error-budget evidence contract from logs.
- Service: optimize query paths, cache metrics, and streaming thresholds.
- Surface: reliability dashboards with log-derived indicators.
```

---

### 8. `d:\code\ayan\contact\docs\codebases\root-codebase-analysis.md` (lines 1–80)

```markdown
# contact360.io/root codebase deep analysis (Contact360 eras 0.x-10.x)

## Service summary

`contact360.io/root` is the public marketing and growth surface for Contact360. It is a Next.js 16 App Router app using React 19 + TypeScript and a custom 3D-styled UI system.

## Runtime architecture

- Entrypoint: `contact360.io/root/app/layout.tsx`
- Marketing shell: `contact360.io/root/app/(marketing)/layout.tsx`
- Landing composition: `contact360.io/root/app/page.tsx`
- Core data client: `contact360.io/root/src/lib/graphqlClient.ts`
- Context providers: `contact360.io/root/src/context/AuthContext.tsx`, `RoleContext.tsx`, `ThemeContext.tsx`

## UI/UX inventory

### Pages and layout

- Public landing, product showcase, pricing, and documentation routes are implemented with App Router.
- `MarketingLayout` enforces light theme and wraps pages with `Navbar` and `Footer`.
- Landing page uses dynamic imports for large sections (hero, pricing, features, finder, AI section).

### 3D UI components (`src/components/ui`)

- `Button3D`, `Input3D`, `Checkbox3D`, `TabGroup`, `Tabs3D`
- `Modal3D`, `Tooltip3D`, `Drawer3D`, `Toast3D`
- `Card3D`, `CardSelect3D`, `Badge3D`, `Icon3D`
- `Table3D`, `ColumnSelector3D`, `ResizeHandle`
- `RangeSlider3D`, `RichSelect3D`, `Select3D`, `MultiSelect3D`, `FilterMultiSelect3D`
- `TiltRow`, `Accordion3D`, `ComingSoonToast`

### Input, checkbox, radio, progress, graph

- Text inputs: `Input3D` and shared form components.
- Checkbox: `Checkbox3D`.
- Radio: implemented in shared config UIs (for example `TextMatchConfig`).
- Progress bar visuals: CSS and usage-credit progress surfaces.
- Graph/chart: `RechartsChart.tsx` (AreaChart-based visual component).

## Hooks, services, contexts

### Hooks

- Content/data: `useMarketingPage`, `useMarketingPages`, `useDocumentation`, `useLandingContent`, `usePricing`, `useUsageTracking`
- Auth/session: `useAuthForm`, `useAuthRedirect`, `useSessionGuard`
- UI behavior: `useForceLightTheme`, `useDebounce`, `useReveal`, `useToast`, `useResizablePanels`, `useInView`, `useFeatureFeedback`

### GraphQL services (`src/services/graphql`)

- `marketingService`, `pagesService`, `documentationService`
- `authService`, `billingService`, `usageService`, `notificationsService`, `exportsService`, `healthService`

### Contexts

- `AuthContext`: token/user/session state
- `RoleContext`: role-sensitive feature visibility
- `ThemeContext`: theme state with forced-light usage on marketing routes

## Backend API, endpoints, database coupling

- Primary backend contract is GraphQL via Appointment360 (`contact360.io/api`).
- Marketing surface does not directly access DB tables.
- Read-mostly API usage; authenticated actions route to dashboard login/signup flows.

## Era alignment (`0.x`-`10.x`)

- `0.x`: foundational shell, App Router, providers, base components
- `1.x`: auth, billing CTA, usage/credit surfaces, role-aware UI
- `2.x`: email-finder/writer marketing narrative and preview interactions
- `3.x`: contact/company and data platform storytelling surfaces
- `4.x`: extension + Sales Navigator value communication
- `5.x`: AI workflow storytelling (AI writer, assistant surfaces)
- `6.x`: resilience messaging and health-awareness touchpoints
- `7.x`: deployment/governance and trust content exposure
- `8.x`: API/platform messaging and docs-related pages
- `9.x`: ecosystem and integrations positioning
- `10.x`: campaign product storytelling surfaces

## Key findings and risks
```

---

### 9. `d:\code\ayan\contact\docs\codebases\s3storage-codebase-analysis.md` (lines 1–80)

```markdown
# Contact360 `lambda/s3storage` Codebase Analysis and Task Decomposition

This document is a deep analysis of the `lambda/s3storage` service in Contact360 and a version-aligned execution breakdown across `0.x.x` to `10.x.x`.

## Purpose and role in Contact360

`s3storage` is the storage control plane for Contact360 file artifacts. It provides:

- bucket namespace initialization
- file upload/download/list/delete APIs
- multipart upload orchestration for large CSV files
- CSV schema/preview/stats analysis
- asynchronous metadata extraction and `metadata.json` maintenance
- avatar/photo/resume storage paths

This service directly supports product flows in dashboard, API gateway, jobs, extension, and future campaign/integration systems.

## Current architecture snapshot

## Service and API layer

- Entrypoint: `lambda/s3storage/app/main.py`
- Framework: FastAPI + Mangum (Lambda adapter)
- Router: `lambda/s3storage/app/api/v1/router.py`
- Endpoint groups:
  - `health`
  - `buckets`
  - `files`
  - `uploads`
  - `analysis` (schema/preview/stats/metadata)
  - `avatars`

## Backend abstraction

- Service facade: `lambda/s3storage/app/services/storage_service.py`
- Concrete backends: `lambda/s3storage/app/services/storage_backends.py`
  - `S3Backend`
  - `FilesystemBackend`
- Config selector:
  - `S3STORAGE_STORAGE_BACKEND=s3|filesystem`
  - loaded through `lambda/s3storage/app/core/config.py`

## Data and key model

Logical bucket model is prefix-based in a single S3 bucket:

- `{bucket_id}/avatar/`
- `{bucket_id}/upload/`
- `{bucket_id}/photo/`
- `{bucket_id}/export/`
- `{bucket_id}/metadata.json`

This model is aligned with Contact360 multi-surface file usage and downstream ingestion.

## Async metadata pipeline

- Upload complete triggers worker lambda invocation:
  - `s3storage-metadata-worker`
- Worker handler:
  - `lambda/s3storage/app/utils/worker.py`
- Metadata computation:
  - `lambda/s3storage/app/utils/metadata_job.py`
- Metadata persistence:
  - `lambda/s3storage/app/utils/update_bucket_metadata.py`

## Deployment

- AWS SAM template:
  - `lambda/s3storage/template.yaml`
- Two lambda functions:
  - API function
  - metadata worker function

## Strengths observed

- Clean backend abstraction (`StorageService` + backend protocol).
- Good endpoint surface coverage for product needs.
- Multipart upload flow exists end-to-end.
- Metadata worker decouples upload path from expensive file analysis.
- CSV analysis endpoints support preview/schema/stats UX.
```

---

### 10. `d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md` (lines 1–80)

```markdown
# Sales Navigator Codebase Deep Analysis

**Service path:** `backend(dev)/salesnavigator/`  
**Runtime:** FastAPI on AWS Lambda (via Mangum adapter)  
**Language:** Python 3.11  
**Era relevance:** `4.x` (primary) — with influence from `0.x` setup through `10.x` campaign audience  
**Era task-pack index:** `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## 1. Stack and dependencies

| Component | Implementation |
| --- | --- |
| HTTP framework | FastAPI (async) |
| Lambda adapter | Mangum |
| HTTP client | `httpx` (async, connection pooling) |
| Retry logic | `tenacity` (exponential backoff, max 3 retries) |
| HTML parsing | BeautifulSoup4 (`html.parser`) |
| Data validation | Pydantic v2 (`pydantic-settings`) |
| Auth | `X-API-Key` header only (global service-to-service key) |
| Rate limiting | **None currently implemented** (noted as gap) |
| CORS | Wide-open (`*`) — service-to-service intent |
| Deployment | AWS SAM (`template.yaml`), 60s timeout, 1024 MB RAM |

---

## 2. Repository structure

```
backend(dev)/salesnavigator/
├── app/
│   ├── main.py                     # FastAPI app, Mangum handler, exception handlers
│   ├── api/
│   │   ├── dependencies.py         # verify_api_key (X-API-Key header)
│   │   ├── router.py               # mounts /v1 sub-router
│   │   └── v1/
│   │       ├── router.py           # mounts scrape + health routers
│   │       └── endpoints/
│   │       ├── scrape.py       # POST /v1/scrape, POST /v1/save-profiles
│   │       └── health.py       # GET /v1/health
│   ├── core/
│   │   ├── config.py               # Settings (API_KEY, CONNECTRA_API_URL, etc.)
│   │   └── exceptions.py           # ConnectraClientError hierarchy, ValidationError
│   ├── services/
│   │   ├── save_service.py         # SaveService + dedup + chunk/parallel logic
│   │   ├── mappers.py              # Profile → Contact/Company field mapping
│   │   └── sales_navigator/
│   │       ├── extraction.py       # HTML DOM extraction (lead cards, metadata)
│   │       ├── parsing.py          # URL/URN parsing (lead ID, company URL)
│   │       ├── utils.py            # UUID gen, name/location/seniority parsing
│   │       └── normalization.py    # Text normalization, PLACEHOLDER_VALUE sentinel
│   ├── clients/
│   │   └── connectra_client.py     # ConnectraClient + ConnectraClientPool (singleton)
│   └── schemas/
│       ├── requests.py             # SaveProfilesRequest, ScrapeHtmlRequest
│       └── responses.py            # SaveProfilesResponse, ScrapeHtmlResponse
├── tests/
│   ├── test_api.py
│   ├── test_save_service.py
│   ├── test_mappers.py
│   ├── test_performance.py
│   ├── test_optimizations.py
│   └── test_load.py
├── docs/
│   ├── api.md                      # REST API reference (HAS DRIFT — see gaps)
│   ├── README.md
│   └── IMPLEMENTATION_SUMMARY.md
├── template.yaml                   # AWS SAM template
├── requirements.txt
└── .example.env
```

---

## 3. API contract (actual implemented routes)

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/` | None | Service info |
```

---

**Note:** For **detailed `9.x` task bullets** (Contract/Service/Surface/Data/Ops), open later lines in `emailapis-codebase-analysis.md` (~135+), `logsapi-codebase-analysis.md` (~98+), `s3storage-codebase-analysis.md` (~320+), `salesnavigator-codebase-analysis.md` (~338+), or the linked `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md` for Sales Navigator.

