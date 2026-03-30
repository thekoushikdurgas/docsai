# AI workflows (Era 5 — Intelligence layer)

Canonical implementation lives in **`backend(dev)/contact.ai`** (Hugging Face Inference Providers for chat, Gemini-backed utilities where configured). The dashboard API proxies to that service via **`contact360.io/api/app/clients/lambda_ai_client.py`**.

**Endpoint matrix (source of truth):** [`docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`](../backend/endpoints/contact_ai_endpoint_era_matrix.json)  
**GraphQL module:** [`docs/backend/apis/17_AI_CHATS_MODULE.md`](../backend/apis/17_AI_CHATS_MODULE.md)

## Chat (non-streaming)

- **REST (Contact AI):** `POST /api/v1/ai-chats/{chat_id}/message` — appends user + AI messages; uses `HFService` with model fallback chain; **100-message cap** per chat.
- **GraphQL:** `sendMessage` → `LambdaAIClient.send_message` (same REST contract as above).

## Chat (streaming SSE)

- **REST (Contact AI):** `POST /api/v1/ai-chats/{chat_id}/message/stream` — SSE: repeated `data: <chunk>` lines, then `data: [DONE]` (see matrix JSON notes).
- **Gateway client:** `LambdaAIClient.send_message_stream(user_id, chat_id, message, model=None)` parses SSE and yields text chunks. Workers or future GraphQL subscriptions may use this; the dashboard may keep non-streaming `sendMessage` for simplicity until product turns streaming on.

## Model selection

- Contact AI **`ModelSelection`** values are **Hugging Face router model ids** (see `backend(dev)/contact.ai/app/schemas/ai_chat.py`).
- The matrix documents the intended **GraphQL ↔ REST enum mapping** under `model_selection_enum` in [`contact_ai_endpoint_era_matrix.json`](../backend/endpoints/contact_ai_endpoint_era_matrix.json), e.g. `FLASH` → `Qwen/Qwen2.5-7B-Instruct-1M:fastest`, `PRO` → `HuggingFaceH4/zephyr-7b-beta:fastest`, `FLASH_2_0` → `meta-llama/Llama-3.1-8B-Instruct:fastest`, `PRO_2_5` → `mistralai/Mistral-7B-Instruct-v0.3:fastest`.
- GraphQL `ModelSelection` in `app/graphql/modules/ai_chats/types.py` may still list legacy ids — **align enums with Contact AI** before treating `model` overrides as authoritative in production.

## Utility AI (roadmap Stage **5.1** — dashboard journeys; utilities hardened in **5.2**)

These routes live under **`/api/v1/ai/...`** (not `/api/v1/gemini/...`). GraphQL mutations call the same paths via `LambdaAIClient`.

| GraphQL / product | REST (Contact AI) |
| --- | --- |
| `analyzeEmailRisk` | `POST /api/v1/ai/email/analyze` |
| `generateCompanySummary` | `POST /api/v1/ai/company/summary` |
| `parseContactFilters` | `POST /api/v1/ai/parse-filters` |

- **Auth:** utilities use `X-API-Key`; chat routes use `X-API-Key` + `X-User-ID` (see matrix `auth_model`).
- **parse-filters:** response must remain compatible with **Connectra VQL** filter taxonomy (Era `5.x` extension: [`5.10 — Connectra Intelligence.md`](5.10 — Connectra Intelligence.md)).

## Confidence + explainability (roadmap Stage **5.2**)

- **GraphQL `Message`** exposes optional `confidence` and `explanation` (nullable strings). Persisted chat JSON may include these keys on AI messages when the model layer supplies them.

## Cost governance (roadmap Stages **5.3–5.4**)

- Enforce **per-user AI quotas**, **provider cost caps**, and **prompt versioning** in Contact AI + gateway configuration. See [`ai-cost-governance.md`](ai-cost-governance.md) and [`docs/governance.md`](../governance.md).

## Version file index (Era 5 planning)

Canonical roadmap minors and extension slices: [`5.0 — Neural Spine.md`](5.0 — Neural Spine.md)–[`5.10 — Connectra Intelligence.md`](5.10 — Connectra Intelligence.md); era hub [`docs/versions.md`](../versions.md); each `5.N.P — *.md` patch carries **Micro-gate** + **Service task slices** (former task packs merged).
