# Contact AI — 7.x Deployment Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `7.x` — Deployment, RBAC, Audit, Governance  
**Status:** Hardened deployment, role-gating, audit trail, retention enforcement

---

## Contract track

- [ ] Define RBAC for AI features: which subscription plans / user roles can access:
  - Chat (`/api/v1/ai-chats/`): ProUser and above.
  - Email risk, company summary, filter parsing: all authenticated users.
- [ ] Per-tenant API key contract: replace single global `API_KEY` with per-tenant keys.
- [ ] Document chat retention policy: GDPR Article 17 right-to-erasure must cascade to `ai_chats`.
- [ ] Lock API versioning: `/api/v1/` is stable; define deprecation policy for future `/api/v2/`.

## Service track

- [ ] Implement feature gate middleware: check user role/plan from JWT context before serving chat routes.
- [ ] Implement per-tenant API key store: validate against tenant key table instead of single env var.
- [ ] Implement `CASCADE DELETE` or scheduled erasure for `ai_chats` when user account is deleted.
- [ ] Emit audit log events (to `logs.api`) on: chat created, chat deleted, message sent, model used.
- [ ] Document and test blue-green Lambda deployment process for contact.ai.

## Surface track

- [ ] Implement role-gated AI features in dashboard: show/hide AI chat based on user plan.
- [ ] Feature flag: `ENABLE_AI_CHAT` per user plan; disabled → show upgrade prompt instead of chat page.
- [ ] Admin panel: show AI usage summary per user (chat count, message count, model usage).

## Data track

- [ ] Add audit log schema: `{event: "chat_created|chat_deleted|message_sent", user_id, chat_id, model, timestamp}`.
- [ ] Retention policy: document max storage age for `ai_chats` and cleanup schedule.
- [ ] Add `7.x` lineage note to `contact_ai_data_lineage.md`: GDPR erasure cascade.

## Ops track

- [ ] Blue-green Lambda deployment: deploy new version, run smoke tests, shift traffic.
- [ ] Canary rollout for model version updates: 10% traffic to new model before full rollout.
- [ ] Secret rotation: per-tenant API keys with automated rotation policy.
- [ ] Add `contact.ai` to deployment checklist with health probe validation step.
- [ ] Post-deployment smoke test: `GET /health`, `GET /health/db`, `POST /api/v1/ai/email/analyze` with test email.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/database/contact_ai_data_lineage.md` · `docs/governance.md`
