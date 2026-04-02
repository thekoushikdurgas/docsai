# contact360.io/admin codebase deep analysis (Contact360 eras 0.x-10.x)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

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

## Verified completion status from runtime

- [x] ✅ Django admin/governance surface is fully wired with route inventory and template-based UI shells.
- [x] ✅ Privileged route access decorators are in place (`require_super_admin`, `require_admin_or_super_admin`).
- [x] ✅ Admin operations integrate with `logs.api`, `s3storage`, `tkdjob`, and Appointment360 GraphQL clients.
- [x] ✅ Idempotency guard tests exist for destructive/retry admin actions (logs delete, storage delete, billing approve/decline, job retry).
- [x] ✅ Permission-map tests validate route inventory coverage against URL patterns.

## Active risks and gap map

### Security and configuration drift

- [x] ✅ Completed: insecure `LOGS_API_KEY` default fallback removed; key now requires explicit environment injection.
- [x] ✅ Completed: baked-in external defaults for `LOGS_API_URL` and `LAMBDA_AI_API_URL` removed; endpoints are now env-explicit.
- [x] ✅ Completed: `S3StorageClient` auth is aligned to API-key policy (`X-API-Key`, `S3STORAGE_API_KEY` required with URL).
- [x] ✅ Completed: env example templates now avoid secret-like placeholder defaults and explicitly include paired URL/API-key entries for logs, scheduler, and storage integrations.

### Contract and governance drift

- [x] ✅ Completed: route inventory/decorator evidence now includes both `apps/admin/route_inventory.py` parity tests and cross-surface critical route scope checks in `apps/admin/tests/test_privileged_route_scopes.py`.
- [x] ✅ Completed: settings surface now routes writable config changes through validated billing workflow with audit events (`billing_settings_view`) and runtime snapshot-only general settings page.
- [x] ✅ Completed: navigation drift guard test now validates sidebar `app_name:url_name` entries resolve at runtime (`apps/core/tests/test_navigation_integrity.py`).

### Reliability and operations gaps

- [x] ✅ Completed: documentation operations background jobs now persist runtime state in `OperationLog.metadata` (DB-backed), with in-memory fallback only.
- [x] ✅ Completed: logs/storage/jobs/GraphQL paths now share `X-Request-ID` propagation for cross-client trace continuity.
- [x] ✅ Completed: operations dashboard now exposes a dependency release gate (weighted uptime policy + block/pass state) for basic SLO/error-budget enforcement.

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core admin route inventory and permission scopes are formalized.
- [x] ✅ Completed: RBAC/governance docs aligned with decorator-enforced runtime behavior and test evidence (`test_admin_guards.py`, `test_privileged_route_scopes.py`).
- [x] ✅ Completed: idempotency contract extended across destructive/retry mutations (`test_admin_guards.py`) including billing approve/decline and job retry noop handling.
- [ ] 📌 Planned: publish explicit public/private admin API boundary rules for `8.x`.

### Service pack

- [x] ✅ Client bridges for GraphQL/logs/storage/jobs are active in admin views.
- [ ] 🟡 In Progress: unify service client auth/error envelopes for consistent operator behavior.
- [x] ✅ Completed: replaced placeholder settings workflow with validated billing settings pipeline (+ audit logging + tests) and non-writable runtime snapshot at `/admin/settings/`.
- [x] ✅ Completed: migrated docs operation background job state from volatile in-memory maps to DB-backed runtime persistence in `apps/documentation/views/operations.py`.
- [ ] 📌 Planned: add policy-aware controls for ecosystem and campaign operations.

### Surface pack

- [x] ✅ Billing/users/logs/storage/jobs screens are present and routed.
- [x] ✅ Operational health panel now consumes real probe-derived statuses and probe-weighted uptime (not static placeholder uptime).
- [ ] ⬜ Incomplete: add richer provider/retry/failure visibility for email and ingestion operations.
- [ ] 📌 Planned: campaign and integration control consoles for later eras.

### Data pack

- [x] ✅ Graph/documentation repositories and admin data reads are wired.
- [x] ✅ Completed: billing approve/decline paths now emit structured actor/reason/status transition lineage evidence.
- [x] ✅ Completed: trace ID continuity enforced across GraphQL/logs/storage/job client hops (`X-Request-ID` propagation plus tests in `apps/admin/tests/test_trace_propagation.py`).
- [ ] 📌 Planned: compliance evidence overlays for campaign and ecosystem operations.

### Ops pack

- [x] ✅ Route guard tests and idempotency tests exist for key admin delete paths.
- [ ] 🟡 In Progress: remove insecure secret defaults and tighten environment validation gates (service URL/API-key startup validation now enforced for logs, scheduler, storage, and Lambda AI).
- [x] ✅ Completed: resilience tests now cover dependency outages and restart-safe docs job polling (`apps/operations/tests/test_operations_resilience.py`, `apps/documentation/tests/test_operations_runtime_job_persistence.py`).
- [ ] 🟡 In Progress: standardize observability hooks to `logs.api` and dependency health panels (scheduler health probe now runtime-checked, not config-only).
- [ ] 📌 Planned: enforce release gates requiring admin governance evidence in each minor.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: Django shell, auth decorators, base views, and navigation system are established.
- [x] ✅ Completed: lock foundational docs/runtime parity for route inventory and governance maps with route-inventory tests plus sidebar navigation resolve guard.
- [x] ✅ Completed: remove insecure fallback defaults from baseline environment templates (`.env.example`, `.env.prod.example`, `env.example`) and align key-pair contracts.

### `1.x.x - Contact360 user and billing and credit system`

- [x] ✅ Completed: billing review and payment action views are implemented with privileged guards.
- [x] ✅ Completed: credit-change/payment review timeline now emits actor + reason + status transition + timestamp evidence.
- [ ] ⬜ Incomplete: strengthen durable workflow backing for billing settings and QR flows.

### `2.x.x - Contact360 email system`

- [ ] 🟡 In Progress: admin logs and service visibility for email operations are partially available.
- [ ] ⬜ Incomplete: expand provider/failure/retry panels for email finder/verifier monitoring.
- [ ] 📌 Planned: add explicit email-ops governance dashboards with actionable remediation controls.

### `3.x.x - Contact360 contact and company data system`

- [x] ✅ Completed: relationship/docs dashboards and graph surfaces support contact/company governance.
- [ ] 🟡 In Progress: improve lineage visibility from ingestion to contact/company outcomes.
- [ ] ⬜ Incomplete: add stronger drift detection between documented and runtime enrichment behavior.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [ ] 🟡 In Progress: extension/Sales Navigator surfaces are represented in architecture/docs views.
- [ ] ⬜ Incomplete: add dedicated admin diagnostics for extension ingestion and failure replay.
- [ ] 📌 Planned: add governance controls for extension channel policy and support workflows.

### `5.x.x - Contact360 AI workflows`

- [ ] 🟡 In Progress: AI sections/views exist in app structure.
- [ ] ⬜ Incomplete: complete AI workflow governance panels and policy enforcement UX.
- [ ] 📌 Planned: add AI risk/compliance evidence surfaces tied to runtime telemetry.

### `6.x.x - Contact360 Reliability and Scaling`

- [ ] 🟡 In Progress: health/system status and logs surfaces provide baseline reliability signals.
- [ ] ⬜ Incomplete: define and enforce admin dependency SLO/error-budget dashboards.
- [ ] ⬜ Incomplete: persist async operation tracking state beyond process memory.

### `7.x.x - Contact360 deployment`

- [x] ✅ Completed: deployment and environment validation commands/views are present.
- [ ] ⬜ Incomplete: tighten secret management defaults and deployment hard gates.
- [ ] 🟡 In Progress: align production runbooks and governance docs with actual deploy paths.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 🟡 In Progress: API metadata and health views are available for admin operators.
- [ ] ⬜ Incomplete: define explicit public/private boundary and versioning governance in admin UX.
- [ ] 📌 Planned: add partner-safe access governance and incident playbooks.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 📌 Planned: add workspace/integration governance controls and tenant-safe operation panels.
- [ ] ⬜ Incomplete: add cross-service trace correlation for partner investigations.
- [ ] 📌 Planned: produce SLA evidence views for ecosystem support and audits.

### `10.x.x - Contact360 email campaign`

- [ ] 📌 Planned: campaign ops governance console and controls.
- [ ] ⬜ Incomplete: campaign compliance/incident tooling and evidence mapping.
- [ ] 📌 Planned: release gating views for deliverability/compliance readiness.

## Immediate execution queue (high impact)

- [x] ✅ Completed: insecure `LOGS_API_KEY` fallback default removed; secret-required startup checks now validate URL/API-key pairs for logs, scheduler, storage, and Lambda AI dependencies.
- [x] ✅ Completed: align admin `S3StorageClient` auth model with canonical `s3storage` API-key policy.
- [x] ✅ Completed: close route/RBAC docs parity and map evidence from route inventory + critical cross-surface guard tests.
- [x] ✅ Completed: replace in-memory docs operation job tracking with durable DB-backed runtime state (`OperationLog`) while preserving existing API contract.
- [x] ✅ Completed: finalize non-placeholder settings workflows with validation and audit logging.
- [x] ✅ Completed: normalize cross-client trace fields for logs/storage/jobs/GraphQL operations using per-request `X-Request-ID` propagation.
- [x] ✅ Completed: add SLO/error-budget release gate for admin dependency health in operations dashboard context/UI.

## 2026 Gap Register (actionable)

### P0

- [x] ✅ Completed: `ADM-0.1` `LOGS_API_KEY` fallback removed and startup now enforces URL/API-key pairing across core dependency services.
- [x] ✅ Completed: `ADM-0.3` Permission-map test coverage now includes admin route inventory parity plus critical non-admin super-admin route scope assertions.
- [x] ✅ Completed: `ADM-0.4` Idempotency contract expanded beyond delete flows to billing approval/decline and job retry conflict/noop scenarios.
- [x] ✅ Completed: `ADM-0.5` Durable persistence added for docs background analyze/generate/upload job state via `OperationLog` metadata.

### P1/P2

- [x] ✅ Completed: `ADM-1.1` Credit-change audit timeline now emits actor_user_id/reason/status transition/timestamp/request-id evidence from billing review actions.
- [ ] ⬜ Incomplete: `ADM-2.1` Email operations panel expansion (provider/failure/retry visibility).
- [ ] 🟡 In Progress: `ADM-5.1` AI workflow governance panel completion.
- [x] ✅ Completed: `ADM-6.2` Cross-client trace ID propagation across admin GraphQL/logs/storage/job client calls.

### P3/P4

- [ ] 📌 Planned: `ADM-8.1` Explicit public/private API boundary and versioning governance.
- [ ] 📌 Planned: `ADM-9.1` Ecosystem partner operations and SLA evidence console.
- [ ] 📌 Planned: `ADM-10.1` Campaign ops console and incident tooling.
