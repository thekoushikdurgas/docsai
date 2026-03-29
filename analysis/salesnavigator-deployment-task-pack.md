# Sales Navigator — 7.x Deployment & Governance Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `7.x` — Contact360 Deployment  
**Status:** Governance, RBAC, audit events, GDPR controls

---

## Contract track

- [ ] Define role-based access for SN ingestion:
  - `admin`: bulk save, access to ingestion history
  - `member`: save own profiles (up to N per day)
  - `read_only`: no save access
- [ ] Define scoped service key contract: per-environment key (dev/staging/prod) replacing single global key
- [ ] Define immutable audit event schema: `{event: sn_save, user_id, org_id, profiles_submitted, saved_count, failed_count, session_id, timestamp, source_ip}`
- [ ] Define GDPR right-to-erasure cascade: SN-sourced contact deletion → Connectra delete by UUID

## Service track

- [ ] Replace single global `API_KEY` with per-environment/per-tenant scoped keys
- [ ] Emit immutable audit event on each `save-profiles` call (event bus or PostgreSQL audit log)
- [ ] Implement RBAC check on `save-profiles`: validate role from `X-User-Role` or token claims
- [ ] Add `org_id` to Connectra contact metadata for tenant isolation

## Surface track

- [ ] Role-gated save actions: `SNSaveButton` disabled for `read_only`; `member` follows quota and `admin` has full access.
- [ ] Admin-only: bulk export / full SN session history visible only to admin
- [ ] Audit log view: `/settings/audit-log` shows SN save events with actor, count, timestamp
- [ ] GDPR delete request: SN-sourced contacts eligible for erasure via Connectra cascade

## Data track

- [ ] Immutable audit event per save session: written to `audit_events` table or event bus
- [ ] GDPR: SN contact provenance tracked in Connectra (`source=sales_navigator`, `lead_id`, `search_id`) for selective erasure
- [ ] Data retention: define retention policy for SN-sourced contacts (default: follow org retention settings)
- [ ] Blue-green deploy: confirm SAM `--no-fail-on-empty-changeset` allows zero-downtime swap

## Ops track

- [ ] Blue-green Lambda deployment via SAM alias + traffic shifting
- [ ] Canary: 10% traffic to new version → validate CloudWatch metrics before 100% shift
- [ ] Environment-specific `template.yaml` param overrides for staging vs. production
- [ ] Secret rotation schedule: `API_KEY`, `CONNECTRA_API_KEY` rotated quarterly
- [ ] Runbook: procedure for emergency key rotation without downtime

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- `docs/governance.md`
- `docs/audit-compliance.md`

---

## Extension surface contributions (era sync)

### Era 7.x — Deployment

**`extension/contact360` deployment notes:**
- Extension JS modules (`auth/`, `utils/`) are consumed by the Chrome extension build pipeline
- Extension does not use SAM or EC2 deployment — distributed via Chrome Web Store or internal MDM
- Lambda SN API (`POST /v1/save-profiles`) backend is deployed via SAM (see `salesnavigator` SAM template)
- Extension build artefacts (`.zip`/`.crx`) must not be committed to the monorepo

**Tasks:**
- [ ] Document extension build + packaging workflow in `docs/7.` era folder
- [ ] Confirm Lambda SN API URL is injected into extension build config (not hardcoded)
- [ ] Define extension version bump process and changelog format