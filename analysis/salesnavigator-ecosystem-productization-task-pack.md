# Sales Navigator — 9.x Ecosystem Integrations Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `9.x` — Contact360 Ecosystem Integrations and Platform Productization  
**Status:** Partner connector adapter, webhook delivery, tenant isolation

---

## Contract track

- [ ] Define connector adapter contract: normalized profile payload that non-SN sources (HubSpot, Salesforce, etc.) can use with this service
- [ ] Define webhook delivery contract: after `save-profiles` → POST result to configured `webhook_url`
- [ ] Define connector health endpoint: `GET /v1/connector/{id}/status`
- [ ] Define tenant-isolated ingestion lineage contract: `{tenant_id, session_id, source, profiles_count, timestamp}`

## Service track

- [ ] Adapter layer: normalize partner profile payload → `SaveProfilesRequest` schema
- [ ] Webhook delivery: POST `SaveProfilesResponse` to `webhook_url` on save completion (configurable per API key)
- [ ] Webhook retry: 3 attempts, exponential backoff, dead-letter log on final failure
- [ ] Tenant-isolated ingestion: tag all Connectra writes with `tenant_id` from API key context

## Surface track

- [ ] Integrations page: `/settings/integrations`
  - SN integration card: status (connected/disconnected), last sync, profiles saved
  - HubSpot/Salesforce connector card (future): "Import contacts" action
- [ ] Webhook delivery log: per integration, show last 10 webhook events (success/failure)
- [ ] Connector health card: live status indicator (green/yellow/red)
- [ ] Sync history: cross-source view — SN, HubSpot, manual import in one timeline

## Data track

- [ ] Tenant-isolated lineage: `{tenant_id, source, session_id, lead_ids[], timestamp}` per session
- [ ] Connector audit trail: each connector event logged to `connector_events` table
- [ ] Webhook delivery log: `{webhook_id, session_id, status, attempts, last_error, delivered_at}`

## Ops track

- [ ] Connector SLA dashboard: per-tenant ingestion success rate
- [ ] Quota controls per connector type
- [ ] Alert: webhook delivery failure rate > 5% for a tenant
- [ ] Documentation: connector integration guide for partners

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## Extension surface contributions (era sync)

### Era 9.x — Ecosystem Integrations

**`extension/contact360` as ecosystem ingestion channel:**
- The extension acts as the primary bridge between LinkedIn/Sales Navigator (external platform) and Contact360's internal data platform
- SN profiles scraped by the extension → Connectra index → available for dashboard search, filters, and campaign audience building
- Extension represents the "external data ingestion" channel in the Contact360 ecosystem

**Tasks:**
- [ ] Document extension as a first-class ingestion source in `docs/9.` era folder
- [ ] Ensure SN-sourced contacts are distinguishable via `source="sales_navigator"` tag in all ecosystem integrations