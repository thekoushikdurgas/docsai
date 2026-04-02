# Email App Codebase Analysis (`contact360.io/email`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

`contact360.io/email` is the dedicated mailbox-style frontend surface in Contact360. It provides auth, mailbox folder views, email detail rendering, and account/IMAP management. It is currently a direct REST-consuming UI layer (via `NEXT_PUBLIC_BACKEND_URL`) and does not use the same GraphQL-first service architecture as `contact360.io/app`.

---

## Runtime architecture snapshot

- Framework/runtime: Next.js 16 app-router, React 19, TypeScript.
- UI stack: Tailwind + component wrappers (`button`, `table`, `tabs`, `sidebar`, alerts).
- Data transport: direct `fetch` calls from components/pages.
- Session/account state: mailbox **identity** in `localStorage` (`id`, `provider`, `email` only); **mailbox session token** in `sessionStorage` (not persisted across browser restarts); passwords only sent to backend over HTTPS during connect.
- Mail rendering: HTML body sanitized via `isomorphic-dompurify` before display.

---

## Verified completion status from runtime

- [x] ✅ Mailbox route shell is implemented (`/inbox`, `/sent`, `/spam`, `/draft`).
- [x] ✅ Email detail route exists and renders sanitized HTML (`/email/[mailId]`).
- [x] ✅ Auth pages exist (`/auth/login`, `/auth/signup`) and call backend auth endpoints.
- [x] ✅ Account page supports profile updates and connecting/switching IMAP accounts.
- [x] ✅ Table-level list capabilities exist (selection, pagination, unread tab counts).
- [x] ✅ Basic loading/error empty states exist in mailbox views.

## Active risks and gap map

### Security and credential handling

- [x] ✅ Completed: password is not persisted; `mailhub_active_account` stores only public identity fields; session token uses `sessionStorage`.
- [x] ✅ Completed: mailbox fetches no longer send raw `X-Email`/`X-Password` credentials from client runtime.
- [ ] 🟡 In Progress: auth token strategy is partially commented/implicit in multiple files and not fully standardized.
- [ ] 🟡 In Progress: mailbox session token contract is introduced (`X-Mailbox-Session`) and now needs backend enforcement hardening.

### Product and feature completeness

- [ ] ⬜ Incomplete: compose/send workflow is visually present but not implemented as real send pipeline.
- [ ] ⬜ Incomplete: sidebar secondary links (`Settings`, `Ask AI`, `Get Help`) are placeholders (`url: "#"`) and not productized.
- [ ] 🟡 In Progress: unread filtering is present, but table search input is not wired to active filtering behavior.
- [ ] ⬜ Incomplete: flagged tab behavior is not connected to persisted flag state.

### Reliability and architecture drift

- [ ] 🟡 In Progress: baseline loading/error UI exists, but retry/backoff and request normalization are inconsistent.
- [ ] ⬜ Incomplete: no centralized service client layer (auth/mail/account requests are duplicated across components).
- [ ] ⬜ Incomplete: observability and event telemetry alignment with `logs.api` is not explicit.
- [ ] 📌 Planned: align mail app contract model with Appointment360 governance conventions where applicable.

---

## Cross-service dependency map (release gating)

- [x] ✅ `contact360.io/email` -> backend REST auth/user/mail endpoints (private runtime contract).
- [ ] 🟡 In Progress: define explicit dependency map into central Contact360 service docs and release gates.
- [ ] ⬜ Incomplete: formal dependency bridge to `contact360.io/api` (Appointment360) is missing.
- [ ] 📌 Planned: integrate with campaign and activity services for unified operator workflows.

## Storage-control-plane migration map (`direct S3` -> `s3storage`)

- [x] ✅ No direct browser AWS SDK or raw S3 client usage found in this app.
- [ ] 📌 Planned: when attachments/media upload is added, enforce `s3storage`-only flow via gateway contract.
- [ ] 📌 Planned: add doc gate forbidding new direct storage access patterns in email app.

## Log-unification migration map (`local logs/console` -> `logs.api`)

- [ ] 🟡 In Progress: local `console.error`/`console.warn` remains in auth/sidebar/mail/account flows.
- [ ] ⬜ Incomplete: production-grade frontend action/error telemetry is not routed through canonical `logs.api`.
- [ ] 📌 Planned: introduce unified telemetry adapter (client breadcrumb -> backend/logs.api ingestion).

---

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core REST routes are consumed for auth, user profile, mailbox list/detail, and IMAP account operations.
- [ ] 🟡 In Progress: document and type all request/response DTOs to reduce drift.
- [ ] ⬜ Incomplete: define mailbox session token contract to replace raw credential headers.
- [ ] ⬜ Incomplete: specify campaign-ready email send/sequence contracts for `10.x.x`.
- [ ] 📌 Planned: publish private/public endpoint policy for this app surface.

### Service pack

- [x] ✅ Functional fetch flows exist for login/signup/list/detail/account updates.
- [ ] 🟡 In Progress: create centralized service modules (`authService`, `mailService`, `accountService`) for reuse.
- [ ] ⬜ Incomplete: implement compose/send orchestration and delivery status updates.
- [ ] ⬜ Incomplete: replace localStorage credential model with secure session abstraction.
- [ ] 📌 Planned: add feature flags for phased rollout of campaign/AI capabilities.

### Surface pack

- [x] ✅ Sidebar, mailbox pages, detail view, and account settings UI are established.
- [ ] 🟡 In Progress: wire table search input and flagged state to real filters/state.
- [ ] ⬜ Incomplete: activate placeholder secondary navigation destinations.
- [ ] ⬜ Incomplete: improve cross-page UX consistency (state persistence, toasts, recovery actions).
- [ ] 📌 Planned: campaign operator workspace (compose, schedule, sequence, analytics).

### Data pack

- [x] ✅ Email HTML rendering includes sanitization guardrails.
- [ ] 🟡 In Progress: enforce strict typing and validation for backend payloads.
- [ ] ⬜ Incomplete: eliminate sensitive credential persistence in browser storage.
- [ ] ⬜ Incomplete: define reliable message metadata lineage (read/flag/sent status auditability).
- [ ] 📌 Planned: campaign evidence and compliance retention model.

### Ops pack

- [x] ✅ Basic loading/error handling patterns are present in mailbox and account views.
- [ ] 🟡 In Progress: add request retry/backoff and timeout handling consistently.
- [ ] ⬜ Incomplete: no formal SLO/error-budget instrumentation in frontend runtime.
- [ ] ⬜ Incomplete: release gating checklist for endpoint/auth/config hardening not complete.
- [ ] 📌 Planned: operational dashboards and alert routing for mailbox runtime.

---

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x` - Foundation and pre-product stabilization and codebase setup

- [x] ✅ Next.js mail app scaffold, route shell, and component baseline are implemented.
- [x] ✅ Theme/layout and sidebar patterns are established.
- [ ] 🟡 In Progress: enforce shared code standards and remove stale commented legacy code paths.
- [ ] ⬜ Incomplete: central API service abstraction layer is missing.

### `1.x.x` - Contact360 user and billing and credit system

- [x] ✅ Login/signup and user profile editing flows exist.
- [ ] 🟡 In Progress: standardize auth token/session handling in all calls.
- [ ] ⬜ Incomplete: billing and credit visibility/action surfaces are not integrated here.
- [ ] 📌 Planned: add subscription/credit-aware mail feature gating.

### `2.x.x` - Contact360 email system

- [x] ✅ Folder browsing and email detail views are operational.
- [x] ✅ IMAP account connect/switch UI and backend calls are implemented.
- [ ] 🟡 In Progress: stabilize mailbox fetch behavior and user-state recovery flows.
- [ ] ⬜ Incomplete: compose/send and message action pipelines (flag/move/label) are incomplete.

### `3.x.x` - Contact360 contact and company data system

- [ ] ⬜ Incomplete: no active contact/company enrichment links from mailbox UI.
- [ ] 📌 Planned: add sender-to-contact/company lookup and CRM linkage from messages.
- [ ] 📌 Planned: add save-to-contact/company actions from inbox detail.

### `4.x.x` - Contact360 Extension and Sales Navigator maturity

- [ ] ⬜ Incomplete: no direct extension/Sales Navigator inbox bridge in current runtime.
- [ ] 📌 Planned: map extension-discovered leads into mailbox workflows.
- [ ] 📌 Planned: provide Sales Navigator context panes in relevant email views.

### `5.x.x` - Contact360 AI workflows

- [ ] ⬜ Incomplete: AI navigation exists only as placeholder link (`Ask AI`).
- [ ] 📌 Planned: AI email drafting, summarization, and reply suggestion pipeline.
- [ ] 📌 Planned: AI-assisted triage for spam/risk/prioritization.

### `6.x.x` - Contact360 Reliability and Scaling

- [x] ✅ Basic load/error states are implemented.
- [ ] 🟡 In Progress: normalize error handling and retries for network failures.
- [ ] ⬜ Incomplete: no robust telemetry/SLO instrumentation and limited resilience controls.
- [ ] 📌 Planned: adopt resilient query/cache layer and offline-safe handling.

### `7.x.x` - Contact360 deployment

- [x] ✅ Standard Next.js build/deploy baseline is present.
- [ ] 🟡 In Progress: tighten production env validation and secret hygiene.
- [ ] ⬜ Incomplete: deployment runbook and release safety checks are incomplete.
- [ ] 📌 Planned: progressive rollout controls and feature flags per environment.

### `8.x.x` - Contact360 public and private apis and endpotints

- [x] ✅ Private REST endpoint consumption pattern exists.
- [ ] 🟡 In Progress: formalize endpoint ownership/versioning docs for this app.
- [ ] ⬜ Incomplete: no explicit public/private boundary enforcement in app contract docs.
- [ ] 📌 Planned: endpoint compatibility checks integrated into CI gates.

### `9.x.x` - Contact360 Ecosystem integrations and Platform productization

- [ ] ⬜ Incomplete: ecosystem integrations are minimal in current UI.
- [ ] 📌 Planned: integrate docs/help/automation connectors and external mailbox ecosystems.
- [ ] 📌 Planned: platform-grade integration settings and health surfaces.

### `10.x.x` - Contact360 email campaign

- [ ] ⬜ Incomplete: campaign compose/sequence/scheduling UI is not implemented.
- [ ] ⬜ Incomplete: send pipeline, campaign analytics, and compliance tracking are not implemented.
- [ ] 📌 Planned: campaign control center integrated with contacts, credits, and AI.
- [ ] 📌 Planned: campaign observability and deliverability governance surfaces.

---

## Immediate execution queue (high impact)

- [x] ✅ Completed: remove IMAP password persistence and raw credential headers from client runtime (replace with tokenized mailbox session headers).
- [ ] 🟡 In Progress: centralize API calls into typed service modules and shared error handling.
- [ ] ⬜ Incomplete: wire compose/send flow and replace placeholder tool routes.
- [ ] ⬜ Incomplete: connect table search + flagged behavior to real backend/state model.
- [ ] 📌 Planned: add telemetry adapter for standardized `logs.api` event/error ingestion.

## 2026 Gap Register (actionable)

### P0 - must close for release safety

- [x] ✅ Completed: eliminate client-side credential persistence and raw credential transport.
- [ ] ⬜ Incomplete: enforce secure auth/session handling consistently across all requests.

### P1/P2 - required for maturity

- [ ] 🟡 In Progress: central service abstraction + typed contracts for all endpoints.
- [ ] 🟡 In Progress: complete mailbox UX gaps (search wiring, flagged state, send actions).
- [ ] 📌 Planned: complete observability/logging unification into canonical logging path.

### P3+ - platform productization

- [ ] 📌 Planned: AI-assisted mail workflows and ecosystem integrations.
- [ ] 📌 Planned: full campaign runtime (`10.x.x`) with compliance/analytics controls.
