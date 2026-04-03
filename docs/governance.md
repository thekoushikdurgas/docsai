# Contact360 Docs and Service Governance

This file defines baseline governance for the monorepo and service skeletons.

## Monorepo baseline

- **Backend languages:** The customer **GraphQL API** is **`contact360.io/api` (Python)**. **Satellite backends** target **Go + Gin** unless an exception is documented in **`docs/docs/backend-language-strategy.md`**. Do not imply the gateway is being rewritten to Go without an explicit program charter.
- **Browser-facing data APIs:** New **customer** data planes exposed to dashboard or extension **must** go through **GraphQL** (`contact360.io/api`) unless a documented exception is approved (e.g. mailbox REST for `contact360.io/email`, internal service-to-service routes). Exceptions require architecture + governance review and updates to **`docs/docs/architecture.md`**.
- **New HTTP services:** Default **Go + Gin** for satellite APIs per **`docs/docs/backend-language-strategy.md`**; place new EC2 implementations under **`EC2/<service>.server/`** with module paths `contact360.io/...` unless embedding Python ML in-process.
- Product surfaces and APIs live under `contact360.io/`.
- `contact360.io/email/` is a first-class product surface and must be included in release/docs sync where email UI behavior changes.
- Lambda-style services live under `lambda/`.
- Optional backend workspaces live under `backend(dev)/`.
- Browser extension code is canonical in `extension/contact360/`.
- **Frontend page inventory (supplementary):** `docs/frontend/` — JSON page specs under `docs/frontend/pages/`, CSV exports under `docs/frontend/excel/`, overview in `docs/frontend/README.md`. The **canonical live UI map** remains **`docs/frontend.md`** (dashboard `contact360.io/app/`, marketing `root/`, DocsAI `admin/`, extension).
- **Command governance pack:** `docs/commands/` — standardized GitHub, deployment, test, production, and release checklist command docs.

## Mandatory docs synchronization

When editing architecture or roadmap docs, mirror updates in DocsAI constants:

- `docs/docs/architecture.md` -> `contact360.io/admin/apps/architecture/constants.py`
- `docs/docs/roadmap.md` -> `contact360.io/admin/apps/roadmap/constants.py`
- If language/stack bullets change, align `docs/docs/backend-language-strategy.md` with the same narrative in architecture constants.

Follow the full runbook in `docs/docsai-sync.md`.

## Task evidence (era folders)

When marking work complete in era task markdown, use the bullet template in **`docs/docs/task-evidence-template.md`** (Evidence / API / Tests / Done because) instead of placeholder text.

## CI baseline

Repo-level checks run via `.github/workflows/ci.yml` to ensure:

- required top-level directories exist,
- DocsAI constants files exist,
- and core docs files are present.

## Docs validation artifacts (`docs/result/`, `docs/errors/`)

- `python cli.py validate-all --write-latest` emits timestamped JSON plus `latest.json` in both folders (see `docs/docs/doc-folder-structure-policy.md`).
- **Do not commit** generated `*.json` in those directories by default: `docs/.gitignore` excludes them. Commit the `README.md` stubs only.
- **CI:** prefer uploading `docs/result/latest.json` (and optionally `docs/errors/latest.json`) as workflow artifacts for green/red gates instead of storing them in git.

## Release hygiene

- No major/minor stage status transitions without doc + constants sync.
- No new service path aliases unless reflected in architecture docs.
- No release promotion with plaintext mailbox credentials in client storage or direct credential headers (`X-Email`/`X-Password`) on production paths.
- Extension `4.5.0` readiness requires baseline shell artifacts: `manifest.json`, background service worker, content script, and popup UI wiring.

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

Full definitions in `docs/version-policy.md`.

## Stage 1.4–1.7 (user analytics, notifications, admin, security) — code map

| Stage | Intent | Primary locations |
| ----- | ------ | ----------------- |
| 1.4 User analytics | Usage ledger, feature limits, activity | Dashboard `contact360.io/app/app/(dashboard)/usage/page.tsx`, `src/hooks/useUsage.ts`, `src/services/graphql/usageService.ts`, API `usage` GraphQL module |
| 1.5 Notifications | Low-credit UI, payment-submission feedback | `src/components/layout/CreditBudgetAlerts.tsx` (wired in `MainLayout.tsx`), `UpiPaymentModal.tsx` success toast |
| 1.6 Admin | Credits, packages, payment review | DocsAI/Django `contact360.io/admin/` — `apps/admin/services/admin_client.py` (`list_payment_submissions`, `approve_payment_submission`), GraphQL `approvePayment` / `declinePayment` |
| 1.7 Security baseline | GraphQL rate limit | `contact360.io/api/app/core/middleware.py` (`GraphQLRateLimitMiddleware`), enabled when `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` is greater than 0 in `app/core/config.py` and `main.py` |

## Email finder / verifier (roadmap 2.1–2.3) — code map

| Area | Primary locations |
| ---- | ----------------- |
| Tier-1 pattern generation (10 formats) | `lambda/emailapis/app/utils/email_generator.py` (`_generate_tier1_patterns`, `generate_email_combinations`) |
| High-throughput Go path | `lambda/emailapigo/` (finder pipelines); orchestration via `lambda/emailapis/` |
| Gateway + credits (1 per finder) | `contact360.io/api/app/graphql/modules/email/queries.py`, `app/services/credit_service.py` |
| Verifier (Mailvetter / APIs) | `backend(dev)/mailvetter/`, `lambda/emailapis` verification routes |
| Bulk processing (Stage 2.4) | `contact360.io/jobs/app/processors/email_finder_export_stream.py`, `email_verify_export_stream.py`, `lambda/s3storage/` |

## Connectra VQL — frozen filter taxonomy (Stage 3.1)

- **Contract doc:** `docs/vql-filter-taxonomy.md` — field lists and `VQLQuery` shape; must stay aligned with `contact360.io/api/app/utils/vql_converter.py` and `contact360.io/sync/utilities/structures.go`.
- **Service entrypoints:** `ListByFilters` / `CountByFilters` on `contact360.io/sync/modules/contacts/service/contactService.go` (and companies service).
- **Dual-write and read hydration:** `docs/connectra-service.md` — ES query + PG hydrate, `BulkUpsert` to PG + ES + `filter_data`.
- **Enrichment / dedupe / UUID rules:** `docs/enrichment-dedup.md`.
- **Dashboard search UX (Stage 3.4):** `docs/3. Contact360 contact and company data system/dashboard-search-ux.md`.
- **Extension auth / token refresh (Stage 4.1):** `docs/extension-auth.md`, `extension/contact360/auth/graphqlSession.js` (optional hooks in `extention/contact360/utils/lambdaClient.js`).
- **Sales Navigator ingestion (Stage 4.2):** `docs/sales-navigator-ingestion.md`.
- **Extension sync integrity (Stage 4.3):** `docs/extension-sync-integrity.md`.
- **Extension telemetry (Stage 4.4):** `docs/extension-telemetry.md`.
- **AI workflows (Era 5 / Stages 5.1–5.4):** `docs/ai-workflows.md` — HF chat + SSE streaming client, Gemini utilities, confidence fields, cost-governance pointers.
- **AI cost governance (Era 5):** `docs/ai-cost-governance.md` — quotas, provider caps, prompt versioning checklist.
- **SLO + idempotency baseline (Era 6 / Stages 6.1–6.2):** `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md` — RED metrics (`/health/slo`) and GraphQL idempotency key replay on guarded billing writes.
- **Queue observability baseline (Era 6 / Stages 6.3–6.4):** `docs/6. Contact360 Reliability and Scaling/queue-observability.md` — trace propagation + DLQ/replay runbook expectations.
- **Performance/storage/abuse baseline (Era 6 / Stages 6.5–6.8):** `docs/6. Contact360 Reliability and Scaling/performance-storage-abuse.md` — GraphQL body-size cap, per-mutation write throttle, storage lifecycle and cost runbook guardrails.
- **Reliability RC hardening (Era 6 / Stage 6.9):** `docs/6. Contact360 Reliability and Scaling/reliability-rc-hardening.md` — health/SLO gates, smoke suite, incident runbook, sign-off table.
- **RBAC + gateway authz (Era 7 / Stages 7.1–7.2):** `docs/7. Contact360 deployment/rbac-authz.md` — role matrix, `require_auth` / `require_profile_roles`, service API keys.
- **Audit + lifecycle baseline (Era 7 / Stages 7.3–7.5):** `docs/audit-compliance.md` — activity logging, logs.api retention, data lifecycle runbook.
- **Tenant security + observability (Era 7 / Stages 7.6–7.8):** `docs/tenant-security-observability.md` — JWT scoping, security controls, trace/SLO references.
- **Deployment RC (Era 7 / Stage 7.9):** `docs/7. Contact360 deployment/analytics-era-rc.md` — deployment era RC gate and smoke checklist.
- **Analytics taxonomy + instrumentation (Era 8 / Stages 8.1–8.2):** `docs/8. Contact360 public and private apis and endpoints/analytics-platform.md` — event taxonomy, instrumentation, quality, reporting baseline.
- **Private API contracts + public API surface (Era 8 / Stages 8.3–8.5):** `docs/public-api-surface.md` — GraphQL as contract, private API baseline, limits, versioning expectations.
- **Webhooks + replay (Era 8 / Stages 8.6–8.7):** `docs/8. Contact360 public and private apis and endpoints/webhooks-replay.md` — signed events, retries, DLQ, replay.
- **Partner identity + analytics/reporting APIs (Era 8 / Stages 8.7–8.8):** `docs/integration-partner-governance.md` — contract rules, partner identity, tenant-safe integration access.
- **APIs RC (Era 8 / Stage 8.9):** `docs/integration-era-rc.md` — API compatibility RC gate and sign-off.
- **Integration contract governance + connector framework (Era 9 / Stages 9.1–9.3):** `docs/9. Contact360 Ecosystem integrations and Platform productization/connectors-commercial.md` — connector pattern, observability, metering hooks.
- **Platform productization (Era 9 / Stages 9.4–9.9):** `docs/platform-productization.md` — tenant model, entitlements, SLA ops, residency, lifecycle.
- **Campaign foundation (Era 10 / Stage 10.1):** `docs/campaign-foundation.md` — entity, policy gate, suppression, templates.
- **Campaign execution (Era 10 / Stage 10.2):** `docs/campaign-execution-engine.md` — state machine, idempotent send, pause/resume.
- **Campaign deliverability (Era 10 / Stage 10.3):** `docs/campaign-deliverability.md` — Mailvetter, bounces, warmup.
- **Campaign observability + release (Era 10 / Stage 10.4):** `docs/campaign-observability-release.md`.
- **Campaign commercial + compliance (Era 10 / Stage 10.5):** `docs/campaign-commercial-compliance.md`.


## Stage 8.x-10.x backend code map

- 8.x webhooks
- 9.x integrations
- 10.x campaigns

## Documentation integrity gates (extended)

- No roadmap release update is considered complete unless `docs/backend/endpoints/*.json` and `docs/frontend/pages/*.json` include era/version metadata.
- API module docs in `docs/backend/apis/*.md` must declare endpoint version introduction and frontend binding references.
- Per-minor version docs must include backend/database/frontend/UI/flow/release evidence sections for every planned and released minor.

## `s3storage` governance controls (cross-era)

- All `lambda/s3storage/` contract updates must include matching docs updates in:
  - `docs/codebases/s3storage-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/roadmap.md`
  - `docs/versions.md`
- Direct `boto3`/`aioboto3` S3 calls from application services outside `lambda/s3storage` are prohibited after 2.x and require migration plans.
- Storage lifecycle changes (upload/delete/metadata) require explicit evidence under Data/Ops tracks before release promotion.
- Multipart contract changes require updated Postman coverage and failure-path test evidence.
- Metadata schema or write-path changes require reconciliation plan and rollback notes.
- Security-sensitive storage changes (TTL, auth, retention) require audit/compliance review before shipping.
- Per-minor release docs under `docs/versions/version_*.md` must maintain concrete storage evidence in backend/data/frontend scope sections for any storage-impacting minor.

## `logs.api` governance controls (cross-era)

- All `lambda/logs.api/` contract updates must include matching docs updates in:
  - `docs/codebases/logsapi-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/roadmap.md`
  - `docs/versions.md`
- Any auth model change for logs.api must include explicit key-rotation and revocation evidence.
- Retention policy changes must include lifecycle policy evidence and rollback notes.
- Query/aggregation behavior changes must include performance and correctness validation evidence.
- Per-minor release docs under `docs/versions/version_*.md` must maintain concrete logs evidence in backend/data/frontend scope sections for any logging-impacting minor.

## Admin deployment governance (`contact360.io/admin/deploy`)

Use the deployment script set as a governed lifecycle, not as ad-hoc shell commands.

| Script | Use case | Governance rule |
| --- | --- | --- |
| `deploy-to-ec2.sh` | recommended single-command deploy (pre + full + post) | default path for first deploy and major re-deploy |
| `pre-deployment-check.sh` | validate env and config without mutation | mandatory before `full-deploy.sh` in manual mode |
| `full-deploy.sh` | full stack bootstrap and deployment | allowed for fresh instances and controlled rebuilds |
| `post-deployment-verify.sh` | service/health/log verification | mandatory after each deployment |
| `deploy.sh` | standard update after baseline setup | allowed only when baseline setup already exists |
| `remote-deploy.sh` | CI/CD-triggered remote update | requires audit note in release log |

Required evidence for deployment-related doc updates:

- deployment command used and target mode (http-only or domain+SSL),
- pre-check result summary,
- post-verify result summary including health endpoint status,
- rollback path and operator owner.

## Marketing app deployment notes (`contact360.io/root`)

- Build/start contracts should remain aligned with `contact360.io/root/package.json`.
- Environment contract must include GraphQL endpoint and dashboard auth-CTA target URL.
- Public marketing deploys must preserve unauthenticated behavior and forced-light theme layout behavior.
- If marketing route/catalog changes, update:
  - `docs/frontend.md`
  - `docs/frontend/components.md`
  - `docs/frontend/hooks-services-contexts.md`
  - `docs/flowchart.md`

## `connectra` governance controls (cross-era)

- All `contact360.io/sync/` contract updates must include matching docs updates in:
  - `docs/codebases/connectra-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/roadmap.md`
  - `docs/versions.md`
- VQL filter taxonomy changes require `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md` updates in the same change set.
- ES index mapping changes require integration tests for `ListByFilters` and `CountByFilters`.
- Batch-upsert schema changes require rollback plan and idempotency verification evidence.
- Per-minor release docs under `docs/versions/version_*.md` must include concrete Connectra evidence for backend/data/frontend sections whenever sync behavior changes.

## `emailapis` / `emailapigo` governance controls (cross-era)

- All `lambda/emailapis/` or `lambda/emailapigo/` contract updates must include matching docs updates in:
  - `docs/codebases/emailapis-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/roadmap.md`
  - `docs/versions.md`
- Provider selection or naming changes (`truelist`/`mailvetter`/`icypeas`) require explicit contract drift review and migration notes.
- Status semantic changes (`valid`, `invalid`, `catchall`, `unknown`, related states) require end-to-end mapping updates in frontend, GraphQL, and runtime docs.
- Bulk finder/verifier behavior changes require updated retry/idempotency evidence and failure-path test notes.
- Per-minor release docs under `docs/versions/version_*.md` must maintain concrete email evidence in backend/data/frontend scope sections for any email-impacting minor.

## `jobs` governance controls (cross-era)

- All `contact360.io/jobs/` contract updates must include matching docs updates in:
  - `docs/codebases/jobs-codebase-analysis.md`
  - `docs/backend/apis/16_JOBS_MODULE.md`
  - `docs/backend/apis/JOBS_ERA_TASK_PACKS.md`
  - `docs/backend/database/jobs_data_lineage.md`
  - `docs/frontend/jobs-ui-bindings.md`
- Any lifecycle/status semantic change must update flow diagrams and UI status mappings in the same change set.
- Any processor registry change must include endpoint mapping updates and era task-pack updates.
- Any retry/idempotency behavior change must include rollback/runbook notes and reliability evidence.

## Jobs CI baseline checks

- Processor registry integrity test: every registered `job_type` resolves to a callable processor.
- Endpoint contract parity test: documented create/status/retry endpoints match implemented routes.
- Status vocabulary test: allowed statuses remain `open/in_queue/processing/completed/failed/retry`.
- Timeline evidence test: lifecycle transitions emit `job_events` entries for auditability.

## `email campaign` governance controls (cross-era)

- All `backend(dev)/email campaign` contract updates must include matching docs updates in:
  - `docs/codebases/emailcampaign-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/backend.md`
  - `docs/versions.md`
- Schema changes (new columns/tables) must update `db/schema.sql` AND matching migration scripts. Schema drift between `schema.sql` and live DB is a release blocker.
- Template system changes (S3 key structure, cache strategy) must include integration test evidence before deployment.
- SMTP provider or credential changes require explicit end-to-end test delivery to sandbox inbox before promotion.
- Suppression list semantic changes require explicit migration/backfill evidence and suppression check regression test.
- Campaign status vocabulary changes must update `docs/backend/apis/22_CAMPAIGNS_MODULE.md` and all frontend status badge components in the same change set.
- Per-minor release docs under `docs/versions/version_*.md` must include concrete email campaign evidence in backend/data/frontend scope sections whenever campaign behavior changes.
- Any audience source change (CSV / segment / VQL / SN) requires recipient resolution integration test with Connectra.
- Sequence engine changes require step-type vocabulary to remain in `docs/10. Contact360 email campaign/emailcampaign-email-campaign-task-pack.md`.

## Email Campaign CI baseline checks

- Schema parity test: `schema.sql` tables match production DB schema via `pg_dump --schema-only` diff.
- Auth guard test: unauthenticated `POST /campaign` and `POST /templates` return 401.
- Suppression test: recipient in `suppression_list` receives no email after campaign send.
- Unsubscribe token test: `GET /unsub?token=...` with valid JWT adds email to suppression and updates recipient status.
- Template render test: Go template variables (`{{.FirstName}}`, `{{.UnsubscribeURL}}`) render correctly for all recipient fields.
- Worker idempotency test: re-queuing same campaign_id does not duplicate sends.

## `contact.ai` governance controls (cross-era)

- All `backend(dev)/contact.ai` contract updates must include matching docs updates in:
  - `docs/codebases/contact-ai-codebase-analysis.md`
  - `docs/backend/apis/17_AI_CHATS_MODULE.md`
  - `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`
  - `docs/backend/database/contact_ai_data_lineage.md`
  - `docs/frontend/contact-ai-ui-bindings.md`
  - `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`
- Any `ModelSelection` enum change must update the mapping shim in `LambdaAIClient` AND all enum tables in docs in the same change set.
- Any `/api/v1/ai/` utility endpoint change must update `contact_ai_endpoint_era_matrix.json` and the relevant era task packs.
- JSONB `messages` schema changes must update `contact_ai_data_lineage.md` and include backward compatibility evidence.
- SSE streaming contract changes must include client reconnect documentation and error event format spec.
- GDPR-relevant changes (user deletion, chat retention) require erasure cascade evidence and `7.x`+ retention policy documentation.
- Per-minor release docs under `docs/versions/version_*.md` must include AI chat evidence in backend/data/frontend scope sections when AI behavior changes.

## Contact AI CI baseline checks

- Auth guard test: endpoints without `X-API-Key` return 401.
- User isolation test: chat owned by user A is not accessible by user B (`X-User-ID` enforcement).
- ModelSelection mapping test: all GraphQL enum values map to valid HF model IDs.
- Message cap test: chat with 100 messages rejects the 101st with appropriate error.
- Ownership check test: `PUT`/`DELETE` on another user's chat returns 403.
- Health endpoint test: `GET /health` and `GET /health/db` return 200 with `{"status":"ok"}`.
- SSE stream test: `POST /message/stream` emits `data: [DONE]\n\n` token on completion.
- Utility stateless test: `analyzeEmailRisk`, `generateCompanySummary`, `parseContactFilters` do not write to `ai_chats` table.

## `appointment360` (contact360.io/api) governance controls (cross-era)

- All `contact360.io/api` contract updates must include matching docs updates in:
  - `docs/codebases/appointment360-codebase-analysis.md`
  - `docs/architecture.md`
  - `docs/backend.md`
  - `docs/versions.md`
  - Relevant `docs/backend/apis/NN_MODULE.md` for the affected GraphQL module
- **Schema composition rule:** any new GraphQL module added to `schema.py` must be documented in `docs/backend/apis/` before merging. Module numbers must be allocated from the era task-pack index.
- **Downstream client rule:** any new `app/clients/*.py` file must have a corresponding env var entry in `config.py`, `.env.example`, and a health check hook in `/health`.
- **Middleware change rule:** any add/remove/reorder of middleware layers must update the 8-layer table in `docs/codebases/appointment360-codebase-analysis.md` and `docs/architecture.md` in the same PR.
- **Debug write rule (critical):** inline file writes (`open(..., 'a')` or `debug.log` writes) are **release blockers** in any production module. Every module must pass a static lint check that no file write occurs outside of `app/services/` or explicit storage clients.
- **Context integrity rule:** `Context.user` must only be populated from a valid, non-blacklisted JWT. Any change to the JWT extraction path must include a blacklist lookup regression test.
- **Idempotency key rule:** mutations listed in `IDEMPOTENCY_REQUIRED_MUTATIONS` must always be tested with duplicate-key replay scenarios. Removing a mutation from the list requires approval and a rollback plan.
- **Abuse guard rule:** any mutation added to `ABUSE_GUARDED_MUTATIONS` must include a corresponding rate-limit regression test that verifies `429` response after threshold.
- **Rate limit rule:** `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` must be non-zero in any production deployment. A zero value is a release blocker for `6.x+` environments.
- **DataLoader rule:** any new resolver that fetches related entities by FK must use a DataLoader. Direct ORM fetches in list resolvers are rejected in code review for `3.x+` modules.
- **Campaign module rule:** all mutations that proxy to the email campaign service must verify the campaign service's critical bugs (schema drift, `GetUnsubToken` fix, SMTP auth) are resolved before `10.x` production promotion.
- Per-minor release docs under `docs/versions/version_*.md` must include Appointment360 evidence in backend/data/frontend scope sections whenever a new GraphQL module is activated.

## Appointment360 CI baseline checks

- Auth guard test: `query me` without `Authorization` header returns `401` / `UNAUTHENTICATED` error.
- Token blacklist test: using a blacklisted access token returns `401`.
- Schema composition test: importing `schema.py` with all modules succeeds without circular imports.
- Health endpoint test: `GET /health`, `GET /health/db`, `GET /health/logging`, `GET /health/slo` return 200.
- Body size guard test: POST body > `GRAPHQL_MAX_BODY_BYTES` returns `413`.
- Complexity guard test: query exceeding `GRAPHQL_COMPLEXITY_LIMIT` returns complexity error.
- Idempotency replay test: sending same mutation with identical `X-Idempotency-Key` twice returns identical response.
- Rate limit test: sending > `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` requests from same IP returns `429`.
- DB session commit test: successful mutation commits session; exception causes rollback without data leak.
- ConnectraClient round-trip test: `contacts(query)` GraphQL call reaches mocked Connectra and maps response to `ContactType`.
- Debug write static test: no module under `app/graphql/modules/` contains `open(` with write mode.

---

## Extension deployment governance

### Canonical extension package path

- `extension/contact360/` — canonical path for the Chrome extension logic layer
- Old spelling `extention/contact360/` must not appear in new work; update to `extension/` in any migrated docs

### Extension environment configuration

- `LAMBDA_SN_API_URL` — base URL for `POST /v1/save-profiles`; must be set in extension config before build/packaging
- `APPOINTMENT360_GRAPHQL_URL` — GraphQL endpoint for `auth.refreshToken`; must be set in extension config
- Extension does NOT use `.env` files; runtime config is bundled at build time or injected via `manifest.json` permissions / content script parameters

### Extension build and packaging rules

- Extension JS files (`auth/`, `utils/`) are consumed directly (no transpile step required for current ES6+ target)
- A full extension build packages popup HTML, content scripts, and these utility modules into the Chrome extension `.zip`/`.crx`
- Do not commit bundled/minified extension artefacts to the monorepo; distribute via Chrome Web Store or internal MDM

### Extension token security rules

- `accessToken` and `refreshToken` stored in `chrome.storage.local` only (never `storage.sync`)
- Tokens must never be logged, included in error reports, or transmitted to any endpoint other than Appointment360 GraphQL
- Token refresh buffer is 300 seconds; this value must be documented if changed

### Release hygiene for extension changes

- Any change to `auth/graphqlSession.js` that alters token storage keys (`accessToken`, `refreshToken`) must be considered a **breaking change** and requires a version bump
- Any change to `utils/lambdaClient.js` that alters the `/v1/save-profiles` request schema must be co-ordinated with a Lambda SN API update and both deployed together

## `salesnavigator` service governance controls (cross-era)

- All `backend(dev)/salesnavigator` contract updates must include matching docs updates in:
  - `docs/codebases/salesnavigator-codebase-analysis.md`
  - `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`
  - `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
  - `docs/backend/database/salesnavigator_data_lineage.md`
  - `docs/frontend/salesnavigator-ui-bindings.md`
  - `docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`
- **Docs drift rule (P0):** `backend(dev)/salesnavigator/docs/api.md` must only document implemented routes. Any route in docs that is not implemented is a release blocker.
- **UUID contract stability:** `generate_contact_uuid()` and `generate_company_uuid()` changes are breaking. Require migration evidence and data lineage doc update before production deployment.
- **Field mapping changes:** Any `mappers.py` change affecting contact/company fields written to Connectra requires `salesnavigator_data_lineage.md` update in the same PR.
- **CORS policy:** CORS `*` is a known security gap. Do not widen CORS further; tighten to known origins before `6.x` release.
- **API key rotation:** `API_KEY` and `CONNECTRA_API_KEY` must be in the org's secret rotation schedule. Document rotation procedure in ops runbook.
- **GDPR controls (7.x+):** SN-sourced contacts are subject to right-to-erasure. Erasure cascade must be verified via Connectra delete by UUID, with evidence in the compliance bundle.
- Per-minor release docs under `docs/versions/version_*.md` must include SN ingest evidence in backend/data scope sections when SN behavior changes.

## Sales Navigator CI baseline checks

- Auth guard test: `POST /v1/save-profiles` without `X-API-Key` returns 403.
- Empty profiles test: `POST /v1/save-profiles` with `profiles: []` returns 422.
- Deduplication test: two profiles with same `profile_url` → only one record in Connectra.
- UUID determinism test: same `profile_url` + `email` → same UUID on second call.
- Partial success test: batch with one invalid profile → `success: true` with `errors` list.
- Health test: `GET /v1/health` returns 200.
- Max profiles test: `POST /v1/save-profiles` with 1001 profiles returns 422.
- Scrape HTML test: `POST /v1/scrape` with valid SN HTML + `save:false` returns profiles without Connectra call.

## `mailvetter` governance controls (cross-era)

- All `backend(dev)/mailvetter` contract updates must include matching docs updates in:
  - `docs/codebases/mailvetter-codebase-analysis.md`
  - `docs/backend/apis/15_EMAIL_MODULE.md`
  - `docs/backend/apis/MAILVETTER_ERA_TASK_PACKS.md`
  - `docs/backend/database/mailvetter_data_lineage.md`
  - `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`
- **Canonical route rule (P0):** `/v1/*` is the only canonical API contract. Legacy `/verify|/upload|/status|/results` routes are compatibility only and must not be used for new integrations.
- **Limiter rule:** in-memory limiter is non-production for multi-instance deployments; Redis-backed limiter required before scale-out releases.
- **Secret isolation rule:** `WEBHOOK_SECRET_KEY` and `API_SECRET_KEY` must remain distinct. Fallback from webhook secret to API secret is a release blocker in `7.x+`.
- **Status vocabulary rule:** job lifecycle terms must remain synchronized across API docs, DB rows, UI, and webhook event payloads.
- **Migration discipline rule:** schema changes to `jobs`/`results` must be delivered via explicit migration scripts; startup auto-migration cannot be sole migration path for production.
- Per-minor release docs under `docs/versions/version_*.md` must include verifier evidence when mailvetter behavior changes.

## Mailvetter CI baseline checks

- Auth guard test: missing/invalid Bearer key on `/v1/*` returns 401.
- Single verify schema test: `POST /v1/emails/validate` returns required fields and valid status enum.
- Bulk limit test: free tier payload above allowed count returns `BULK_SIZE_EXCEEDED`.
- Concurrent job limit test: excess parallel bulk submissions return `CONCURRENT_JOB_LIMIT`.
- Queue-to-result test: queued bulk request increments `processed_count` to `total_count` and emits results.
- Result export test: `/v1/jobs/:job_id/results?format=csv` returns parseable CSV with expected headers.
- Webhook signature test: callbacks include valid `X-Webhook-Signature`.
- Job retention test: cleanup removes data older than 30 days without FK break.
- SMTP timeout resilience test: transient SMTP timeout does not crash worker loop.

---

## Email app governance controls — `contact360.io/email`

- Any endpoint contract change consumed by `contact360.io/email` must update in same PR:
  - `docs/codebases/email-codebase-analysis.md`
  - `docs/backend/apis/EMAILAPP_ERA_TASK_PACKS.md`
  - `docs/backend/database/emailapp_data_lineage.md`
  - `docs/backend/endpoints/emailapp_endpoint_era_matrix.json`
- Local storage key changes (`userId`, `mailhub_active_account`) are breaking to session continuity and require migration notes.
- Security gate: plaintext IMAP password persistence in localStorage is disallowed for production-grade releases (must migrate to backend mailbox session token).
- DOMPurify rules in email detail rendering are part of secure-render contract and must be documented when changed.

## `contact360.io/admin` governance controls (cross-era)

- Secret handling must be env-only; insecure fallback secrets are release blockers.
- Privileged routes require explicit permission-map tests (`super_admin`, `admin_or_super_admin`, public exceptions).
- Destructive admin actions must support idempotency keys and immutable audit events.
- Outbound integration clients (`appointment360`, `logs.api`, `s3storage`, job satellites via gateway) must enforce auth header correctness per service contract.

## Admin CI baseline checks

- Auth guard test on protected admin routes.
- Permission matrix parity test for each admin URL surface.
- Billing approve/decline idempotency replay test.
- Client credential/env validation test in startup profile.

## `lambda/emailapigo` governance controls (cross-era)

- Hardcoded credentials/endpoints are prohibited; logging and external clients must be env-driven.
- Cache upsert identity contract must be preserved with explicit unique-key enforcement.
- CORS and auth rules must be environment-scoped, not wildcard defaults.
- Migration behavior must be explicit and pipeline-driven for production.

## EmailAPIGo CI baseline checks

- Auth guard and scoped-key validation.
- Rate limit behavior validation.
- Cache upsert identity uniqueness test.
- Deterministic provider fallback-chain contract test.

## `lambda/emailapis` governance controls (cross-era)

- API key model must support rotation and scoped entitlements.
- Status vocabulary is a governed contract across providers and downstream consumers.
- Bulk endpoints require idempotency contract and replay-safe semantics.
- CORS policy must be environment allowlist based for production.

## EmailAPIs CI baseline checks

- Auth guard and scoped-key validation.
- Status vocabulary contract parity test.
- Bulk idempotency replay test.
- Provider fallback-chain behavior test.

## Canonical storage routing rule

All service file/artifact storage must route through lambda/s3storage.

| Service | Status |
| --- | --- |
| appointment360 | ✅ uses S3StorageClient |
| contact360.io/jobs | 📌 Planned migrate direct S3 paths |
| backend(dev)/contact.ai | 📌 Planned audit/migrate |
| backend(dev)/email campaign | 📌 Planned migrate direct S3 paths |
| backend(dev)/mailvetter | 📌 Planned audit/migrate |
| backend(dev)/resumeai | 📌 Planned confirm/migrate |
| contact360.io/admin | 📌 Planned confirm/migrate |

## Quality Gates & Checklists
- [Era Subchecklist Template](promsts/checklists/era-subchecklist-template.md)
- [Prompt Quality Gate](promsts/checklists/prompt-quality-gate.md)
