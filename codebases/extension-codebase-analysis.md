# Extension Codebase Analysis — `extension/contact360`

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Service summary

`extension/contact360` now contains two tightly-coupled surfaces:

- Chrome extension shell/runtime (`manifest.json`, `background.js`, `content.js`, `popup.*`, auth/utils)
- Sales Navigator ingestion API service (FastAPI under `app/`, SAM template, tests)

Together they provide the LinkedIn/Sales Navigator capture channel for Contact360 contact/company ingestion.

## Runtime architecture snapshot

- Extension shell:
  - `manifest.json` (MV3), `background.js`, `content.js`, `popup.html/css/js`
  - auth/session helper: `auth/graphqlSession.js`
  - transport + batching: `utils/lambdaClient.js`
  - dedup/merge: `utils/profileMerger.js`
- Backend service:
  - FastAPI entrypoint: `app/main.py`
  - routes + auth deps: `app/api/**`
  - ingestion/mapping services: `app/services/save_service.py`, `app/services/mappers.py`
  - Sales Navigator helpers: `app/services/sales_navigator/**`
  - deployment: `template.yaml`

## Verified completion status from runtime

- [x] ✅ Extension shell artifacts exist (manifest, background service worker, content script, popup UI).
- [x] ✅ MV3 storage/session path exists for access and refresh token handling.
- [x] ✅ Batched profile submission client exists (`lambdaClient`) with queue/retry/adaptive timeout behavior.
- [x] ✅ Backend API with API-key middleware and save profiles service is implemented.
- [x] ✅ Profile dedup/merge logic exists and test coverage files are present.

## Active risks and gap map

### Security and endpoint scope

- [ ] ⬜ Incomplete: extension `host_permissions` are broad (`https://*/*`, `http://*/*`) and exceed least-privilege needs.
- [ ] ⬜ Incomplete: backend CORS is wildcard in FastAPI service.
- [ ] 🟡 In Progress: API key auth exists but key lifecycle/rotation constraints are not fully governed in docs/runtime checks.

### Contract and product drift

- [ ] ⬜ Incomplete: extension save endpoint contract and backend payload contract still need strict parity tests.
- [ ] 🟡 In Progress: extension runtime references config/constants patterns that need single canonical source.
- [ ] ⬜ Incomplete: trace correlation contract (extension event -> backend ingest -> Connectra write) is not fully formalized.

### Reliability and observability

- [ ] 🟡 In Progress: `lambdaClient` has retry/backoff/queueing, but reliability SLOs and failure budgets are not defined.
- [ ] ⬜ Incomplete: telemetry/log event taxonomy for extension operations is not normalized with `logs.api` conventions.
- [ ] ⬜ Incomplete: content script bootstrap is minimal and lacks hardened extraction/guardrail instrumentation.

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Core save-profiles and auth/session contracts exist.
- [ ] 🟡 In Progress: standardize extension request and backend validation schema for profile payloads.
- [ ] ⬜ Incomplete: define strict idempotency/replay behavior for repeated save batches.
- [ ] ⬜ Incomplete: freeze trace/request/user field contract across extension and backend.
- [ ] 📌 Planned: publish versioned extension-private API contract for `8.x` compatibility.

### Service pack

- [x] ✅ Backend save/mapping pipeline and profile merge utilities are implemented.
- [ ] 🟡 In Progress: harden retry behavior and unauthorized-refresh handling in `lambdaClient`.
- [ ] ⬜ Incomplete: implement stronger extraction and validation guarantees in content/runtime flow.
- [ ] ⬜ Incomplete: enforce stricter host permission and endpoint allowlist policies.
- [ ] 📌 Planned: add queue backpressure controls and adaptive batch sizing based on API health.

### Surface pack

- [x] ✅ Popup status surface and shell wiring are present.
- [ ] 🟡 In Progress: improve user-facing feedback for batch partial-failure and retry states.
- [ ] ⬜ Incomplete: add deterministic UX contract for token-expired/unauthorized flows.
- [ ] 📌 Planned: add extension diagnostics panel for sync status and error triage.

### Data pack

- [x] ✅ Deduplication and URL normalization logic exists in profile mapping services.
- [ ] 🟡 In Progress: align profile schema fields across extension scrape and backend persistence maps.
- [ ] ⬜ Incomplete: add lineage fields linking extension source metadata to downstream contact/company records.
- [ ] 📌 Planned: add campaign-segment compatibility metadata for `10.x` flows.

### Ops pack

- [x] ✅ SAM deployment and service startup/shutdown paths are present.
- [ ] ⬜ Incomplete: replace wildcard CORS and broad host permissions with environment-scoped policies.
- [ ] ⬜ Incomplete: add release gates and smoke tests for extension package + backend API compatibility.
- [ ] 🟡 In Progress: consolidate telemetry/logging behavior with centralized `logs.api` model.
- [ ] 📌 Planned: define extension ingestion SLO dashboards and incident runbooks.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: extension shell and backend API scaffold are present and operational.
- [ ] 🟡 In Progress: close foundational contract drift between extension payload and backend schema.
- [ ] ⬜ Incomplete: enforce least-privilege permissions and baseline security hardening.

### `1.x.x - Contact360 user and billing and credit system`

- [x] ✅ Completed: token/session storage and refresh flow support authenticated extension operation.
- [ ] 🟡 In Progress: standardize credit-impact trace metadata on extension-origin actions.
- [ ] ⬜ Incomplete: define hard auth failure handling for billing-restricted accounts.

### `2.x.x - Contact360 email system`

- [ ] 📌 Planned: bind extension captured profiles more explicitly into email verification/finder pipelines.
- [ ] ⬜ Incomplete: ensure schema compatibility with email-service enrichment contracts.
- [ ] 📌 Planned: add extension-origin email enrichment status surfacing.

### `3.x.x - Contact360 contact and company data system`

- [x] ✅ Completed: profile merge, mapping, and save service core paths support contact/company ingestion.
- [ ] 🟡 In Progress: improve deterministic merge quality and malformed-profile handling.
- [ ] ⬜ Incomplete: add end-to-end lineage evidence from capture to persistence.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [x] ✅ Completed: primary extension/SN integration surface is implemented.
- [ ] 🟡 In Progress: strengthen runtime extraction/orchestration beyond minimal content bootstrap.
- [ ] ⬜ Incomplete: formalize extension support diagnostics and retry UX standards.

### `5.x.x - Contact360 AI workflows`

- [ ] 📌 Planned: define AI enrichment hooks for extension-origin profiles.
- [ ] ⬜ Incomplete: add redaction/safety guards for AI-relevant profile fields.
- [ ] 📌 Planned: track AI decision lineage for extension-origin enrichment.

### `6.x.x - Contact360 Reliability and Scaling`

- [ ] 🟡 In Progress: batching/retries/timeouts exist in `lambdaClient`.
- [ ] ⬜ Incomplete: add SLOs for extension upload latency, success rate, and retry behavior.
- [ ] ⬜ Incomplete: define degradation behavior for backend unavailability and queue saturation.

### `7.x.x - Contact360 deployment`

- [x] ✅ Completed: backend SAM deployment artifacts and extension packaging files are present.
- [ ] ⬜ Incomplete: add signed release workflow and compatibility matrix for extension/backend versions.
- [ ] 🟡 In Progress: deployment environment checks for API keys/URLs and runtime readiness.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 🟡 In Progress: save-profiles endpoint is operational as private API surface.
- [ ] ⬜ Incomplete: publish formal API contract and deprecation/version strategy.
- [ ] 📌 Planned: add partner-safe integration docs for private API consumers.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 📌 Planned: define partner/ecosystem ingestion controls and entitlement policies.
- [ ] ⬜ Incomplete: add tenant-aware throttling/quotas for extension-origin traffic.
- [ ] 📌 Planned: add support evidence bundles for ecosystem incident investigations.

### `10.x.x - Contact360 email campaign`

- [ ] 📌 Planned: use extension-origin profile streams for campaign audience build paths.
- [ ] ⬜ Incomplete: add compliance lineage linking extension source to campaign segment evidence.
- [ ] 📌 Planned: campaign gating with extension data quality thresholds.

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: tighten `manifest.json` host permissions to required domains only.
- [ ] ⬜ Incomplete: replace backend wildcard CORS with explicit environment allowlists.
- [ ] 🟡 In Progress: align extension payload schema and backend validation to one canonical contract.
- [ ] ⬜ Incomplete: add replay/idempotency protection for repeated `save-profiles` submissions.
- [ ] ⬜ Incomplete: expand integration tests that cover extension runtime -> backend -> mapping persistence.
- [ ] 🟡 In Progress: normalize extension telemetry fields and route operational logs through `logs.api`.
- [ ] 📌 Planned: publish extension/backend compatibility release checklist.

## 2026 Gap Register (actionable)

### P0

- [ ] ⬜ Incomplete: `EXT-0.1` Remove over-broad host permissions and enforce least privilege.
- [ ] ⬜ Incomplete: `EXT-0.2` Replace wildcard CORS and tighten API security defaults.
- [ ] ⬜ Incomplete: `EXT-0.3` Lock canonical save payload schema and parity tests.
- [ ] 🟡 In Progress: `EXT-0.4` Normalize extension runtime + backend observability contract.

### P1/P2

- [ ] ⬜ Incomplete: `EXT-1.1` Add idempotency/replay safeguards for profile save batches.
- [ ] 🟡 In Progress: `EXT-1.2` Improve retry/unauthorized recovery UX and user feedback.
- [ ] ⬜ Incomplete: `EXT-2.1` Add trace lineage from extension source to persisted contact/company entities.
- [ ] 📌 Planned: `EXT-2.2` Add extension-specific reliability SLOs and alerting.

### P3+

- [ ] 📌 Planned: `EXT-3.1` Ecosystem/partner controls for extension ingestion channels.
- [ ] 📌 Planned: `EXT-4.1` Campaign audience lineage and compliance evidence integration.
