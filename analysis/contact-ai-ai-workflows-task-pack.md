# Contact AI — 5.x AI Workflows Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `5.x` — AI workflows (PRIMARY era for contact.ai)  
**Status:** All contact.ai features go live

---

## Contract track

- [ ] Lock full REST API contract: all `/api/v1/ai-chats/` and `/api/v1/ai/` paths.
- [ ] Fix `ModelSelection` enum mapping shim: GraphQL enum values (`FLASH`, `PRO`, etc.) must map to HF model IDs in `LambdaAIClient` or Contact AI service.
- [ ] Align `LambdaAIClient` paths to `/api/v1/ai/…` — remove any legacy `/gemini/…` references.
- [ ] Lock `SendMessageInput.model` contract: accepted values and mapping documented in `17_AI_CHATS_MODULE.md`.
- [ ] Document `POST /api/v1/ai-chats/{id}/message/stream` SSE event format: `data: <token>\n\n`, `data: [DONE]\n\n`.
- [ ] Define API versioning strategy: all routes under `/api/v1/`; no unversioned routes in production.

## Service track

- [ ] Complete all chat CRUD endpoints: `GET/POST /api/v1/ai-chats/`, `GET/PUT/DELETE /api/v1/ai-chats/{id}/`.
- [ ] Implement `POST /api/v1/ai-chats/{id}/message` (sync) with full `AIChatService` orchestration.
- [ ] Implement `POST /api/v1/ai-chats/{id}/message/stream` (SSE streaming) via `HFService` async generator.
- [ ] Implement `HFService` model routing: `ModelSelection` enum → HF model ID; default from `HF_CHAT_MODEL` env.
- [ ] Implement Gemini fallback: if HF inference fails after N retries, call Gemini API.
- [ ] Enforce 100-message-per-chat cap in `AIChatService`.
- [ ] All utility endpoints fully implemented and tested: `analyzeEmailRisk`, `generateCompanySummary`, `parseContactFilters`.
- [ ] Implement `messages` JSONB strict validation (max text length, valid sender values, max contacts).

## Surface track

- [ ] Build `AIChatPage` (`/app/ai-chat`): `ChatList` + `ChatThread` layout.
- [ ] Implement `ChatList` with pagination: uses `useChatList` hook.
- [ ] Implement `ChatThread` with message rendering: `ChatMessage` + `ContactsInMessage`.
- [ ] Implement `ChatInput` textarea with send button; disabled while streaming.
- [ ] Implement `StreamingText`: token-by-token rendering via SSE; cursor blink during stream.
- [ ] Implement `ModelSelector` dropdown with all 4 model options; persist choice in `AIModelContext`.
- [ ] Implement `NewChatButton`: creates chat and redirects to `ChatThread`.
- [ ] Implement `ChatContextMenu`: rename (PUT) and delete (DELETE) chat actions.
- [ ] Wire `EmailRiskBadge`, `CompanySummaryTab`, `AIFilterInput` to live endpoints.
- [ ] Loading states: skeleton for chat list, spinner for send, shimmer for utilities.

## Data track

- [ ] Validate `messages` JSONB schema in `AIChatService` before persist: max 100 messages, valid sender, max text length.
- [ ] Add `model_version` field to AI message metadata in JSONB (for reproducibility).
- [ ] Confirm `user_id` ownership check on every read/write/delete operation.
- [ ] Test concurrent message send (two requests to same `chat_id`): document behavior; add optimistic lock if needed.

## Ops track

- [ ] Lambda provisioned concurrency for chat paths to reduce cold-start latency.
- [ ] Prometheus metrics wired: request count, latency histogram, error rate per endpoint.
- [ ] Alert on `503` / `429` rate spike from HF API.
- [ ] Update contact.ai Postman collection with all live endpoints and SSE streaming examples.
- [ ] Add contact.ai to production deployment checklist.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/apis/17_AI_CHATS_MODULE.md` · `docs/frontend/contact-ai-ui-bindings.md` · `docs/backend/database/contact_ai_data_lineage.md`
