---
name: Contact360 Docs Overhaul
overview: Update all Contact360 documentation files to reflect the actual as-is state of all five analyzed codebases (app, email, root, extension/contact360, admin), incorporating era-by-era gap findings, security issues, and task-completion status across the full 0.x–10.x arc.
todos:
  - id: phase1-root-arch
    content: "Update docs/architecture.md: add contact360.io/email row, fix extension/contact360 description (Lambda + JS utils only; Chrome shell missing), update admin entry to reflect DocsAI full feature set"
    status: completed
  - id: phase1-root-codebase
    content: "Update docs/codebase.md: add contact360.io/email to monorepo table, update extension entry to clarify two-layer architecture"
    status: completed
  - id: phase1-root-frontend
    content: "Update docs/frontend.md: add contact360.io/email surface under Era 2.x, update extension row with actual state, add 3D design system note for root"
    status: completed
  - id: phase1-root-backend
    content: "Update docs/backend.md: mark Sales Navigator Lambda as complete (Era 4.x), add email app REST note (Era 2.x), add admin AI assistant (Era 5.x)"
    status: completed
  - id: phase1-root-flowchart
    content: "Update docs/flowchart.md: add emailApp node to core request flow, add extension flow delta showing missing popup and present Lambda client"
    status: completed
  - id: phase1-root-governance
    content: "Update docs/governance.md: add contact360.io/email to monorepo baseline, add security governance rules for IMAP credentials and extension shell requirements"
    status: completed
  - id: phase1-root-docsai-sync
    content: "Update docs/docsai-sync.md: add email app sync awareness, admin settings form wiring note, admin in-memory job store migration note"
    status: completed
  - id: phase1-root-audit
    content: "Update docs/audit-compliance.md: add P0 security findings (email IMAP plaintext, admin SECRET_KEY exposure, extension .example.env real keys, extension CSP requirement)"
    status: completed
  - id: phase1-root-versions
    content: "Update docs/versions.md: update 1.1.0 in_progress scope (settings gap), annotate 2.0.0 scope with email app security gate, annotate 4.0.0 scope with extension shell target"
    status: completed
  - id: phase1-root-roadmap
    content: "Update docs/roadmap.md: add 2.x security hardening sub-task, add 4.5 Chrome extension shell stage, add 1.2 settings page gap, add 5.x AI chat wiring task"
    status: completed
  - id: phase1-root-verpolicy
    content: "Update docs/version-policy.md: add security release clause for critical credential/secret exposure"
    status: completed
  - id: phase2-codebases-app
    content: "Update docs/codebases/app-codebase-analysis.md: add Gaps section covering mock AI chat, mock LinkedIn mapping, admin coming-soon actions, settings redirect, incomplete 2FA"
    status: completed
  - id: phase2-codebases-email
    content: "Update docs/codebases/email-codebase-analysis.md: add Critical Security Findings section (localStorage IMAP plaintext, X-Password headers) and route tracker table"
    status: completed
  - id: phase2-codebases-root
    content: "Update docs/codebases/root-codebase-analysis.md: add Dynamic Content Gaps section (SalesCTA mock, FunnelImpact TODO, fallback static data) and route tracker"
    status: completed
  - id: phase2-codebases-extension
    content: "Update docs/codebases/extension-codebase-analysis.md: add MISSING Chrome Extension Shell section listing all absent files, add .example.env security note"
    status: completed
  - id: phase2-codebases-admin
    content: "Update docs/codebases/admin-codebase-analysis.md: add Known Issues section (placeholder settings, Code Health placeholder, in-memory jobs, contradictory E2E test, SECRET_KEY exposure)"
    status: completed
  - id: phase3-era0-updates
    content: "Update Era 0 docs: mark 0.x-master-checklist.md with completed foundation items, mark salesnavigator-foundation-task-pack.md as Lambda runtime bootstrapped"
    status: completed
  - id: phase3-era1-updates
    content: "Update Era 1 docs: update 1.x-master-checklist.md (check auth/billing, uncheck settings page/2FA/full API key mgmt), update 1.0 — User Genesis.md scope notes"
    status: completed
  - id: phase3-era2-updates
    content: "Update Era 2 docs: update 2.x-master-checklist.md with P0 credential security blocker, update emailapis-email-system-task-pack.md with security tasks, update 2.0 — Email Foundation.md definition-of-done"
    status: completed
  - id: phase3-era3-updates
    content: "Update Era 3 docs: update 3.x-master-checklist.md noting contacts/companies pages exist but backend integration partial"
    status: in_progress
  - id: phase3-era4-updates
    content: "Update Era 4 docs: 4.x-master-checklist.md (check Lambda+JS utilities, uncheck Chrome shell), mark complete tasks in salesnavigator task pack, update 4.1 — Auth & Session.md and 4.2 — Harvest.md status"
    status: pending
  - id: phase4-era5-10-updates
    content: "Update Era 5–10 docs: mark admin AI assistant as functional in Era 5, add admin in-memory store as reliability risk in Era 6, add admin settings wiring requirement in Era 7"
    status: pending
  - id: phase5-frontend-docs
    content: "Update docs/frontend/docs/: salesnavigator-ui-bindings.md (mark Lambda bindings complete, popup pending), components.md (add email app components), design-system.md (add 3D and Radix systems)"
    status: pending
  - id: phase6-backend-docs
    content: Update docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md (mark through 4.2 complete), create/update EMAILAPP_ERA_TASK_PACKS.md with security tasks, update salesnavigator_data_lineage.md
    status: pending
  - id: phase7-docsai-sync
    content: "Sync admin constants: update contact360.io/admin/apps/architecture/constants.py (add email app, fix extension) and contact360.io/admin/apps/roadmap/constants.py (new stages for 2.x security, 4.5 shell, 5.x AI wiring)"
    status: pending
isProject: false
---

# Contact360 Docs Overhaul — All Eras, All Surfaces

## What changed (findings from codebase analyses)

- `contact360.io/app` — Auth/billing core is functional; AI chat is `mockSend`; admin CRUD is "not implemented"; settings redirects to profile; 2FA incomplete.
- `contact360.io/email` — Inbox/folder UI exists; **critical security gap**: IMAP credentials (`X-Password` header, plaintext in `localStorage`).
- `contact360.io/root` — Marketing shell and product pages exist; `SalesCTA` uses mock data; `FunnelImpact` has a `TODO` for live fetch.
- `extension/contact360` — FastAPI Lambda (scrape + save-profiles) and JS utilities (`lambdaClient.js`, `graphqlSession.js`, `profileMerger.js`) are complete; Chrome extension shell is **entirely missing** (`manifest.json`, `background.js`, `content.js`, popup UI).
- `contact360.io/admin` — Django DocsAI with CRUD operations, AI assistant, and admin ops is functional; settings forms are placeholders; in-memory job progress tracking; `SECRET_KEY` leaked in `.env.example` files.

## Docs repo map

```
docs/
├── architecture.md            ← root canonical
├── codebase.md
├── frontend.md
├── backend.md
├── flowchart.md
├── governance.md
├── docsai-sync.md
├── audit-compliance.md
├── versions.md
├── roadmap.md
├── version-policy.md
├── codebases/                 ← per-service deep analyses
├── 0.–10. <era>/              ← per-minor version files + task packs
├── frontend/docs/             ← UI-binding docs
├── backend/apis/              ← GraphQL module docs
└── backend/database/          ← data lineage
```

## Phase 1 — Root canonical docs (11 files)

### 1.1 `docs/architecture.md`

- Add `contact360.io/email` row to the repository layout table (role: Mailhub email app; stack: Next.js 16 + Radix UI).
- Update `extension/contact360` entry: clarify this is the **Lambda backend + JS transport layer**, not a complete Chrome extension (shell missing).
- Update `contact360.io/admin` description: DocsAI documentation CRUD, AI assistant, operational admin ops (users/logs/jobs/billing/storage).
- Add *Planning horizon* note: email app credential security is P0 before 2.x ERA release.

### 1.2 `docs/codebase.md`

- Add `contact360.io/email/` row in the monorepo structure table.
- Update extension entry with accurate two-layer description (FastAPI Lambda + JS utils | Chrome shell: missing).
- Add runtime note: email app calls REST via `NEXT_PUBLIC_BACKEND_URL` (not GraphQL).

### 1.3 `docs/frontend.md`

- Add `contact360.io/email/` to the Product applications table (Era 2.x).
- Update extension row with actual state: auth/session, Lambda client, profile merger complete; popup/content scripts/manifest missing (Era 4.5–4.7 target).
- Add 3D design-system note for `contact360.io/root` (3D component library separate from dashboard flat design).

### 1.4 `docs/backend.md`

- Mark Sales Navigator FastAPI Lambda as complete in Era 4.x row.
- Add email app REST endpoint note under Era 2.x row.
- Mark admin AI assistant (OpenAI → Gemini → Lambda fallback) under Era 5.x.

### 1.5 `docs/flowchart.md`

- Add `emailApp["contact360.io/email"]` node to the core request flow diagram connected to the `emailapigo` worker path.
- Add extension flow delta: `extensionUI["Extension popup (missing)"] -- planned --> lambdaClient["lambdaClient.js"] --> salesnavAPI["Sales Nav Lambda"]`.

### 1.6 `docs/governance.md`

- Add `contact360.io/email/` to the monorepo baseline section.
- Add security governance rule: no plaintext IMAP credentials in `localStorage` or headers; use token-exchange pattern.
- Add extension baseline: `manifest.json`, `background.js`, and `content.js` are required before `4.5.0` release gate.

### 1.7 `docs/docsai-sync.md`

- Add `contact360.io/email` to the sync awareness section (docs changes that touch email app must also update `email-codebase-analysis.md`).
- Add note: admin settings forms are placeholder — `apps/admin/views.py` `settings_view` requires real form wiring before 7.x governance release gate.
- Add note: admin in-memory job progress stores (`_analyze_jobs`, `_generate_json_jobs`, `_upload_jobs`) must be migrated to Redis/DB before 6.x.

### 1.8 `docs/audit-compliance.md`

- Add P0 security findings section under Era 2.x: email app stores IMAP password in plaintext `localStorage`; `X-Email`/`X-Password` headers; must be remediated before 2.x release.
- Add under Era 0.x/7.x: admin `.env.example` exposes `SECRET_KEY`; `.example.env` in extension contains real-looking API keys — must be replaced with `<placeholder>` format.
- Add under Era 4.x: extension `manifest.json` CSP must whitelist Lambda API domain before Chrome Web Store submission.

### 1.9 `docs/versions.md`

- Add `contact360.io/email` to the `2.0.0` planned entry scope.
- Annotate `4.0.0` planned entry: extension Python Lambda backend (scrape/save) is complete; Chrome extension shell is the `4.5–4.7` target.
- Update `1.1.0` in_progress scope: note settings page redirects to profile (dedicated settings page needed).

### 1.10 `docs/roadmap.md`

- Stage 2.x: add security hardening sub-task: token-exchange IMAP auth, encrypted storage.
- Stage 4.5: explicitly add Chrome extension shell tasks (manifest, background service worker, content script, popup).
- Stage 1.2: add note that dedicated `/settings` page is a gap (currently redirects to `/profile`).
- Stage 5.x: note dashboard AI chat uses `mockSend` — wire to Appointment360 `aiChat` mutation.

### 1.11 `docs/version-policy.md`

- Add a security-release clause: critical credential/secret exposure issues trigger a patch release (X.Y.Z) regardless of era.

---

## Phase 2 — Codebase analysis docs (5 files in `docs/codebases/`)

### 2.1 `docs/codebases/app-codebase-analysis.md`

Add a new **Gaps and incomplete tasks** section documenting:

- `app/(dashboard)/ai-chat/page.tsx`: `mockSend` hardcoded — needs GraphQL `aiChat` mutation wiring.
- `app/(dashboard)/linkedin/page.tsx`: `handleMappingSubmit` uses `setTimeout` mock.
- `app/(dashboard)/admin/page.tsx`: user edit/delete actions are "coming soon".
- `app/(dashboard)/settings/page.tsx`: redirects to `/profile` — dedicated settings page missing.
- `src/components/profile/ProfileTabAPI.tsx`: API key management UI present, but 2FA flow incomplete.

### 2.2 `docs/codebases/email-codebase-analysis.md`

Add a **Critical security findings** section:

- `src/context/imap-context.tsx` stores IMAP password in `localStorage` plaintext.
- `src/app/email/[mailId]/page.tsx` and `src/app/account/[userId]/page.tsx` pass `X-Email`/`X-Password` in headers.
- Remediation path: token-exchange flow via Appointment360 → encrypted credential vault → bearer token per IMAP session.
Add a **Route tracker** table (Route | Era | State | P0 gaps).

### 2.3 `docs/codebases/root-codebase-analysis.md`

Add a **Dynamic content gaps** section:

- `src/components/landing/SalesCTA.tsx` uses `mockup_data`.
- `app/(marketing)/products/ai-email-writer/page.tsx` has `TODO` for `FunnelImpact` fetch.
- Several sections use `fallbackMarketingPages.ts` static data instead of live GraphQL.
Add a **Route tracker** table.

### 2.4 `docs/codebases/extension-codebase-analysis.md`

Add a **MISSING: Chrome extension shell** section (P0 before 4.5.0):

- `manifest.json` (MV3)
- `background/service-worker.js`
- `content/content.js`
- `popup/popup.html` + `popup/popup.js`
- `constants.js` (referenced in `hybridFlow.test.js` but missing)
- `salesNavigatorService.js` (referenced in `hybridFlow.test.js` but missing)
Add security note: `.example.env` contains real-looking API keys — replace with `<placeholder>`.

### 2.5 `docs/codebases/admin-codebase-analysis.md`

Add a **Known issues** section:

- `apps/admin/views.py` `settings_view` uses placeholder forms (not wired).
- `apps/core/templates/core/dashboard.html` "Code Health" is a placeholder stat.
- `_analyze_jobs`, `_generate_json_jobs`, `_upload_jobs` are in-memory dicts — lost on process restart.
- `apps/documentation/tests/test_dashboard_e2e.py` `test_health_tab` has contradictory dual status assertion.
- `.env.example` / `.env.prod.example` contain `SECRET_KEY=django-insecure-`* — must be flagged for rotation.

---

## Phase 3 — Era 0–4 task packs + version files

For each era folder, the work is:

1. Update the era `README.md` with actual completion state.
2. Update the `X.x-master-checklist.md` to check off completed items.
3. Update task-pack files for impacted services.
4. Update version minor files for released/in-progress status.

### Era 0 — Foundation

- `0. Foundation.../README.md` — mark overall status as released.
- `0.x-master-checklist.md` — check off: monorepo dirs, service skeletons, app shell, admin shell.
- `salesnavigator-foundation-task-pack.md` — check Python Lambda runtime as bootstrapped.
- `0.1 — Monorepo bootstrap.md` — confirm status = released.

### Era 1 — User/Billing/Credit

- `1.x-master-checklist.md` — check auth/login/register; uncheck settings page (redirect gap), 2FA, API key management.
- `appointment360-user-billing-task-pack.md` — mark auth/session as complete; mark 2FA GraphQL module as incomplete.
- `1.0 — User Genesis.md` — confirm released; add scope note: settings page is a gap.

### Era 2 — Email System

- `2.x-master-checklist.md` — mark inbox/folder UI exists; add P0 blocker: credential security.
- `emailapis-email-system-task-pack.md` — note email app routes exist; add security hardening tasks.
- `2.0 — Email Foundation.md` — update planned scope: include email app security as definition-of-done gate.

### Era 3 — Contact and Company Data

- `3.x-master-checklist.md` — note contacts/companies pages exist in dashboard but backend integration partial.
- `connectra-contact-company-task-pack.md` — mark search/filter UI as partially wired; note VQL builder incomplete.

### Era 4 — Extension and Sales Navigator

- `4.x-master-checklist.md` — check: FastAPI Lambda (scrape + save-profiles complete), JS auth/session utility, Lambda client, profile merger; **uncheck**: manifest.json, background.js, content.js, popup UI, constants.js, salesNavigatorService.js.
- `salesnavigator-extension-sn-task-pack.md` — mark Lambda backend tasks as complete (annotate with `[x]`).
- `extension-auth.md` — confirm `graphqlSession.js` complete; add popup re-auth modal as remaining.
- `extension-sync-integrity.md` — mark dedup/chunking as complete; add sync status UI as remaining.
- `4.1 — Auth & Session.md` — update status: auth/session JS utility complete; note Chrome shell missing.
- `4.2 — Harvest.md` — update status: Lambda scrape/save complete.

---

## Phase 4 — Era 5–10 task packs + version files

### Era 5 — AI Workflows

- `5. AI workflows/README.md` — note dashboard AI chat is mock; admin AI assistant is functional.
- `contact-ai-ai-workflows-task-pack.md` — mark Lambda AI fallback in admin as wired.
- `appointment360-ai-task-pack.md` — mark `aiChat` GraphQL module as existing; note dashboard is not wired to it.
- `5.0 — Neural Spine.md` — update planned scope: add task to wire dashboard AI chat to GraphQL mutation.

### Era 6 — Reliability and Scaling

- `6. Reliability.../README.md` — add admin in-memory job store as reliability risk.
- `jobs-reliability-scaling-task-pack.md` — add task: migrate admin `_*_jobs` dicts to Redis/DB.

### Era 7 — Deployment

- `7.x-master-checklist.md` — add: admin settings form must be wired before 7.x governance gate.
- `rbac-authz.md` — add note about admin `Appointment360AuthMiddleware` JWT role enforcement (SuperAdmin-only access).
- `analytics-era-rc.md` — note admin "Code Health" stat is placeholder.

### Era 8 — Public and Private APIs

- `8. Public...apis/README.md` — confirm API key management UI present in dashboard; mark 2FA gap.

### Era 9 — Ecosystem Integrations

- `9. Ecosystem.../README.md` — note root `/integrations` page is a marketing shell; actual integrations connector not yet wired.

### Era 10 — Email Campaign

- `10. Email campaign/README.md` — confirm `emailcampaign` service exists; note no campaign builder UI in dashboard yet.

---

## Phase 5 — Frontend docs (`docs/frontend/docs/`)

- `salesnavigator-ui-bindings.md` — mark Lambda client and auth binding as complete; mark popup UI bindings as not yet implemented.
- `components.md` — add `email app` surface components: `DataTable`, `email-list`, `app-sidebar`, `LoginForm`, `ImapConnect`.
- `design-system.md` — add note: `contact360.io/root` uses a separate 3D design system (`Button3D`, `Card3D`, `Modal3D`); `contact360.io/email` uses Radix UI + Tailwind.

---

## Phase 6 — Backend docs (`docs/backend/`)

- `apis/SALESNAVIGATOR_ERA_TASK_PACKS.md` — mark FastAPI Lambda tasks as complete through Era 4.2.
- `apis/EMAILAPP_ERA_TASK_PACKS.md` — add email app security hardening task pack for Era 2.x.
- `database/salesnavigator_data_lineage.md` — confirm provenance fields: `lead_id`, `search_id`, `data_quality_score`, `connection_degree`.

---

## Phase 7 — DocsAI sync (admin constants)

Per `docs/docsai-sync.md` rules, after updating architecture and roadmap:

- `contact360.io/admin/apps/architecture/constants.py` — add `contact360.io/email` service entry; update extension entry.
- `contact360.io/admin/apps/roadmap/constants.py` — add 2.x security gate, 4.5 extension shell stage, 5.x AI chat wiring task.

---

## File change summary


| File                                                 | Type           | Change                                   |
| ---------------------------------------------------- | -------------- | ---------------------------------------- |
| `docs/architecture.md`                               | Root canonical | Add email app, fix extension description |
| `docs/codebase.md`                                   | Root canonical | Add email app row, fix extension         |
| `docs/frontend.md`                                   | Root canonical | Add email app surface, fix extension     |
| `docs/backend.md`                                    | Root canonical | Mark Lambda complete, add email REST     |
| `docs/flowchart.md`                                  | Root canonical | Add email app node, extension flow delta |
| `docs/governance.md`                                 | Root canonical | Add email app, security governance       |
| `docs/docsai-sync.md`                                | Root canonical | Add email sync rule, admin notes         |
| `docs/audit-compliance.md`                           | Root canonical | Add P0 security findings                 |
| `docs/versions.md`                                   | Root canonical | Update 1.1.0, 2.0.0, 4.0.0 entries       |
| `docs/roadmap.md`                                    | Root canonical | Add security gate, extension shell stage |
| `docs/version-policy.md`                             | Root canonical | Add security release clause              |
| `docs/codebases/app-codebase-analysis.md`            | Analysis       | Add gaps section                         |
| `docs/codebases/email-codebase-analysis.md`          | Analysis       | Add critical security section            |
| `docs/codebases/root-codebase-analysis.md`           | Analysis       | Add dynamic content gaps                 |
| `docs/codebases/extension-codebase-analysis.md`      | Analysis       | Add missing shell section                |
| `docs/codebases/admin-codebase-analysis.md`          | Analysis       | Add known issues section                 |
| `docs/4…/4.x-master-checklist.md`                    | Era doc        | Check Lambda; uncheck shell              |
| `docs/4…/salesnavigator-extension-sn-task-pack.md`   | Task pack      | Mark Lambda tasks complete               |
| `docs/4…/4.1 — Auth & Session.md`, `4.2 — Harvest.md`           | Version        | Update status                            |
| `docs/2…/2.x-master-checklist.md`                    | Era doc        | Add security gate                        |
| `docs/1…/1.x-master-checklist.md`                    | Era doc        | Update completion state                  |
| `docs/frontend/docs/salesnavigator-ui-bindings.md`   | Frontend doc   | Mark binding states                      |
| `docs/frontend/docs/components.md`                   | Frontend doc   | Add email app components                 |
| `docs/frontend/docs/design-system.md`                | Frontend doc   | Add 3D + Radix systems                   |
| `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md` | Backend doc    | Mark complete                            |
| `contact360.io/admin/apps/architecture/constants.py` | DocsAI sync    | Add email app, fix extension             |
| `contact360.io/admin/apps/roadmap/constants.py`      | DocsAI sync    | Add new stages                           |


