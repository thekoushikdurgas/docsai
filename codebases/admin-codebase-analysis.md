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
- [x] ✅ Idempotency guard tests exist for destructive delete flows in admin views.
- [x] ✅ Permission-map tests validate route inventory coverage against URL patterns.

## Active risks and gap map

### Security and configuration drift

- [ ] ⬜ Incomplete: `LOGS_API_KEY` still has an insecure default fallback in settings.
- [ ] ⬜ Incomplete: `S3StorageClient` path notes "No API key required" and needs alignment with stricter storage auth policy.
- [ ] 🟡 In Progress: env validation exists, but secret hygiene in examples and production defaults remains uneven.

### Contract and governance drift

- [ ] 🟡 In Progress: route inventory and decorators are tested, but full RBAC evidence mapping to docs is partial.
- [ ] ⬜ Incomplete: some admin settings flows remain placeholder-oriented and not backed by durable config operations.
- [ ] ⬜ Incomplete: docs/graph/navigation drift risk remains when constants and sidebar registry change.

### Reliability and operations gaps

- [ ] ⬜ Incomplete: documentation operations jobs use in-memory tracking maps and are not resilient across restarts.
- [ ] 🟡 In Progress: logs and storage admin surfaces exist but cross-client trace propagation is not fully normalized.
- [ ] ⬜ Incomplete: consolidated SLO/error-budget dashboards for admin-critical dependencies are not complete.

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core admin route inventory and permission scopes are formalized.
- [ ] 🟡 In Progress: align RBAC and governance docs with decorator-enforced runtime behavior.
- [ ] ⬜ Incomplete: define idempotency contract for all destructive admin mutations (not just deletes).
- [ ] 📌 Planned: publish explicit public/private admin API boundary rules for `8.x`.

### Service pack

- [x] ✅ Client bridges for GraphQL/logs/storage/jobs are active in admin views.
- [ ] 🟡 In Progress: unify service client auth/error envelopes for consistent operator behavior.
- [ ] ⬜ Incomplete: replace placeholder settings workflows with durable validated config pipelines.
- [ ] ⬜ Incomplete: migrate volatile in-memory job tracking to persistent task backend.
- [ ] 📌 Planned: add policy-aware controls for ecosystem and campaign operations.

### Surface pack

- [x] ✅ Billing/users/logs/storage/jobs screens are present and routed.
- [ ] 🟡 In Progress: strengthen operational health panels beyond placeholders.
- [ ] ⬜ Incomplete: add richer provider/retry/failure visibility for email and ingestion operations.
- [ ] 📌 Planned: campaign and integration control consoles for later eras.

### Data pack

- [x] ✅ Graph/documentation repositories and admin data reads are wired.
- [ ] 🟡 In Progress: improve actor/diff lineage fields for billing and privileged actions.
- [ ] ⬜ Incomplete: enforce trace ID continuity across GraphQL/logs/storage/job client hops.
- [ ] 📌 Planned: compliance evidence overlays for campaign and ecosystem operations.

### Ops pack

- [x] ✅ Route guard tests and idempotency tests exist for key admin delete paths.
- [ ] ⬜ Incomplete: remove insecure secret defaults and tighten environment validation gates.
- [ ] ⬜ Incomplete: add resilience tests for job-tracking restart scenarios and dependency outages.
- [ ] 🟡 In Progress: standardize observability hooks to `logs.api` and dependency health panels.
- [ ] 📌 Planned: enforce release gates requiring admin governance evidence in each minor.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: Django shell, auth decorators, base views, and navigation system are established.
- [ ] 🟡 In Progress: lock foundational docs/runtime parity for route inventory and governance maps.
- [ ] ⬜ Incomplete: remove insecure fallback defaults from baseline environment config.

### `1.x.x - Contact360 user and billing and credit system`

- [x] ✅ Completed: billing review and payment action views are implemented with privileged guards.
- [ ] 🟡 In Progress: improve credit-change audit evidence (actor + reason + diff timeline).
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

- [ ] ⬜ Incomplete: remove insecure `LOGS_API_KEY` fallback default and enforce secret-required startup checks.
- [ ] ⬜ Incomplete: align admin `S3StorageClient` auth model with canonical `s3storage` API-key policy.
- [ ] 🟡 In Progress: close route/RBAC docs parity and generate evidence mapping from route inventory tests.
- [ ] ⬜ Incomplete: replace in-memory operation job tracking with durable backend storage/queue.
- [ ] ⬜ Incomplete: finalize non-placeholder settings workflows with validation and audit logging.
- [ ] 🟡 In Progress: normalize cross-client trace fields for logs/storage/jobs/GraphQL operations.
- [ ] 📌 Planned: add SLO dashboard and error-budget release gate for admin dependency health.

## 2026 Gap Register (actionable)

### P0

- [ ] ⬜ Incomplete: `ADM-0.1` Remove insecure secret fallback defaults (`LOGS_API_KEY` and similar).
- [ ] 🟡 In Progress: `ADM-0.3` Permission-map test coverage for privileged routes (baseline done, extend to all critical actions).
- [ ] ⬜ Incomplete: `ADM-0.4` Idempotency contract for all destructive admin actions.
- [ ] ⬜ Incomplete: `ADM-0.5` Durable persistence for documentation operation jobs.

### P1/P2

- [ ] ⬜ Incomplete: `ADM-1.1` Credit-change audit timeline with actor and diff evidence.
- [ ] ⬜ Incomplete: `ADM-2.1` Email operations panel expansion (provider/failure/retry visibility).
- [ ] 🟡 In Progress: `ADM-5.1` AI workflow governance panel completion.
- [ ] ⬜ Incomplete: `ADM-6.2` Cross-client trace ID propagation.

### P3/P4

- [ ] 📌 Planned: `ADM-8.1` Explicit public/private API boundary and versioning governance.
- [ ] 📌 Planned: `ADM-9.1` Ecosystem partner operations and SLA evidence console.
- [ ] 📌 Planned: `ADM-10.1` Campaign ops console and incident tooling.
