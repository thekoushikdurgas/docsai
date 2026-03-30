# Contact AI — 9.x Ecosystem Integrations / Platform Productization Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `9.x` — Ecosystem integrations and Platform productization  
**Status:** AI-powered connectors, webhook delivery, tenant model

---

## Contract track

- [ ] Define Contact AI connector spec for external integration platforms (Zapier, Make, HubSpot).
- [ ] Define webhook contract for async AI results: `{event: "ai_result", chat_id, result, timestamp}`.
- [ ] Document multi-tenant isolation: each tenant's `ai_chats` data is fully isolated by `user_id`/`organization_id`.
- [ ] Define connector auth model: connector keys separate from user keys; documented in API key management.

## Service track

- [ ] Implement webhook delivery: on AI response completion, POST result to registered webhook URL.
- [ ] Implement connector adapter: standardized input/output format for external platform integrations.
- [ ] Implement organization-level AI usage aggregation (for tenant billing/quota).
- [ ] Add `organization_id` to `ai_chats` if multi-tenant isolation requires org-level partitioning.

## Surface track

- [ ] Integration panel in dashboard: AI-powered connectors configuration (webhook URL, trigger events).
- [ ] Connector card: shows AI connector status (active/inactive), last delivery, error rate.
- [ ] Webhook delivery log: show recent deliveries, status codes, retry count per webhook.

## Data track

- [ ] If `organization_id` added: migration file to add column to `ai_chats`; update `contact_ai_data_lineage.md`.
- [ ] Webhook delivery log schema: `{webhook_id, chat_id, payload_hash, status_code, retries, timestamp}`.
- [ ] Connector audit trail: log all connector-initiated AI calls with `source: "connector"` tag.

## Ops track

- [ ] Webhook delivery retry: exponential backoff, max 3 retries, dead-letter queue on final failure.
- [ ] Connector health monitoring: track delivery success rate per connector.
- [ ] Tenant isolation audit: verify no cross-tenant data leakage in AI responses.
- [ ] Add connector endpoints to API rate limit policy.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/database/contact_ai_data_lineage.md`
