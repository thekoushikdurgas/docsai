# Master plan — minors `5.0`–`5.6` (five-track matrix)

## Dashboard AI chat — production wiring (confirmed)

The app uses **real GraphQL** via `contact360.io/app/src/services/graphql/aiChatService.ts` (`aiChats`, `createAIChat`, **`sendAiMessage`**) and pages such as `app/(dashboard)/ai-chat/page.tsx` — **not** a permanent mock layer. Remaining work is **quality, guardrails, and ops** — not replacing mocks.

| Minor | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| **5.0 Neural Spine** | `17_AI_CHATS_MODULE.md` stable | contact.ai + gateway auth headers | Chat shell loading/error | `ai_chats` table + S3 payloads | Error rate alerts |
| **5.1 Orchestration Live** | Tool-calling contracts (if any) | Timeouts + cancellation | Multi-step UX | Message JSON schema versioned | Trace IDs |
| **5.2 Explainability Plane** | (see `5.2` minor doc) | Logging of prompts/responses policy | UI disclosure | Retention | Audit export |
| **5.3 Spend Guardrails** | Credit deduction per AI op | Hard limits server-side | Low-credit UX | Ledger reconciliation | Fraud alerts |
| **5.4 Prompt Constitution** | Versioned system prompts | Safe templating | Admin edit flow | Prompt store | Change approval |
| **5.5 Signal Enrichment** | Optional context pulls | Rate limits on enrichment | UI toggles | Cache TTL | Cost monitor |
| **5.6 Batch Intelligence** | Bulk AI job semantics | Queue + partial failure | Batch progress UI | Job rows in `scheduler_jobs` | Stuck-job runbook |

**Modules:** [`17_AI_CHATS_MODULE.md`](../backend/graphql.modules/17_AI_CHATS_MODULE.md), [`micro.services.apis/contact.ai.api.md`](../backend/micro.services.apis/contact.ai.api.md) (filename may vary).
