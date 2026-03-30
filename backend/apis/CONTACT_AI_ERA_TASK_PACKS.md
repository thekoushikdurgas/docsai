# Contact AI — Cross-Era Task Pack Index

**Service:** `backend(dev)/contact.ai`  
**GraphQL module:** `17_AI_CHATS_MODULE.md`  
**Deep analysis:** `docs/codebases/contact-ai-codebase-analysis.md`  
**Data lineage:** `docs/backend/database/contact_ai_data_lineage.md`  
**UI bindings:** `docs/frontend/contact-ai-ui-bindings.md`  
**Endpoint matrix:** `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`

---

## Purpose

This index links all era-specific task packs for the `contact.ai` service (FastAPI Lambda, Hugging Face LLM, `ai_chats` PostgreSQL table). Each task pack follows the 5-track breakdown standard: **Contract · Service · Surface · Data · Ops**.

---

## Era task-pack files

| Era | Theme | Task pack file |
| --- | --- | --- |
| `0.x` | Foundation | `docs/0. Foundation and pre-product stabilization and codebase setup/contact-ai-foundation-task-pack.md` |
| `1.x` | User/Billing | `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `contact-ai-user-billing-task-pack.md` merged) |
| `2.x` | Email System | `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `contact-ai-email-system-task-pack.md` merged) |
| `3.x` | Contact/Company Data | `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `contact-ai-contact-company-task-pack.md` merged) |
| `4.x` | Extension / SN | `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `contact-ai-extension-sn-task-pack.md` merged) |
| `5.x` | AI Workflows | `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `contact-ai-ai-workflows-task-pack.md` merged) |
| `6.x` | Reliability/Scaling | `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `contact-ai-reliability-scaling-task-pack.md` merged) |
| `7.x` | Deployment | `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `contact-ai-deployment-task-pack.md` merged) |
| `8.x` | Public/Private APIs | `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-public-private-apis-task-pack.md` merged) |
| `9.x` | Ecosystem/Productization | `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-ecosystem-productization-task-pack.md` merged) |
| `10.x` | Email Campaign | `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-email-campaign-task-pack.md` merged) |

---

## Contact AI cross-era execution stream

```
0.x  Service skeleton + ai_chats DDL
  ↓
1.x  user_id FK integrity + IAM baseline
  ↓
2.x  analyzeEmailRisk contract locked
  ↓
3.x  parseContactFilters + companyS ummary + VQL alignment
  ↓
4.x  SN contact objects in messages.contacts JSONB
  ↓
5.x  ★ Full AI workflows live ★ (chat, streaming, all utilities)
  ↓
6.x  SLO, TTL, SSE reliability, tracing
  ↓
7.x  RBAC, audit, retention governance
  ↓
8.x  Public API surface, scoped keys, rate limit headers
  ↓
9.x  Ecosystem connectors, webhook AI delivery
  ↓
10.x Campaign AI generation, compliance evidence
```

---

## API endpoint summary

| Method | Path | Era introduced | Notes |
| --- | --- | --- | --- |
| `GET` | `/api/v1/ai-chats/` | `5.x` | List user chats |
| `POST` | `/api/v1/ai-chats/` | `5.x` | Create chat |
| `GET` | `/api/v1/ai-chats/{id}/` | `5.x` | Get chat |
| `PUT` | `/api/v1/ai-chats/{id}/` | `5.x` | Update chat |
| `DELETE` | `/api/v1/ai-chats/{id}/` | `5.x` | Delete chat |
| `POST` | `/api/v1/ai-chats/{id}/message` | `5.x` | Send message (sync) |
| `POST` | `/api/v1/ai-chats/{id}/message/stream` | `5.x` | Send message (SSE stream) |
| `POST` | `/api/v1/ai/email/analyze` | `2.x` (stub) / `5.x` (live) | Email risk analysis |
| `POST` | `/api/v1/ai/company/summary` | `3.x` (stub) / `5.x` (live) | Company summary |
| `POST` | `/api/v1/ai/parse-filters` | `3.x` (stub) / `5.x` (live) | NL → filter parsing |
| `GET` | `/health` | `0.x` | Liveness |
| `GET` | `/health/db` | `0.x` | DB health |
| `GET` | `/metrics` | `6.x` | Prometheus metrics |

---

## ModelSelection enum (canonical — HF model IDs)

| GraphQL enum | HF model ID |
| --- | --- |
| `FLASH` | `Qwen/Qwen2.5-7B-Instruct-1M:fastest` |
| `PRO` | `HuggingFaceH4/zephyr-7b-beta:fastest` |
| `FLASH_2_0` | `meta-llama/Llama-3.1-8B-Instruct:fastest` |
| `PRO_2_5` | `mistralai/Mistral-7B-Instruct-v0.3:fastest` |

> `LambdaAIClient` must map GraphQL enum strings to HF model IDs before sending to Contact AI.

---

## Data stores

| Store | Table / Resource | Access pattern |
| --- | --- | --- |
| PostgreSQL (shared) | `ai_chats` | CRUD via SQLAlchemy async |
| Hugging Face Inference | External API (stateless) | Chat completions + JSON tasks |
| Gemini API | External API (fallback) | Fallback on HF failure |

---

## Maintenance rules

- Keep `17_AI_CHATS_MODULE.md` aligned with actual Contact AI REST routes.
- Keep `ModelSelection` enum values synchronized between GraphQL schema and HF model IDs.
- Any new utility endpoint must update `contact_ai_endpoint_era_matrix.json`.
- Any JSONB schema change must update `contact_ai_data_lineage.md`.
- Era task packs must be updated when a feature crosses from stub → live.
