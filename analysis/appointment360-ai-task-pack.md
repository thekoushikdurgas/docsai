# Appointment360 (contact360.io/api) — Era 5.x AI Workflows Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `AIChatQuery { aiChat(uuid), aiChats() }` | P0 |
| Define `AIChatMutation { createAiChat, sendAiMessage, deleteAiChat, generateCompanySummary, analyzeEmailRisk, parseContactFilters }` | P0 |
| Define `ResumeQuery { resumes(), resume(id) }` | P0 |
| Define `ResumeMutation { createResume, updateResume, deleteResume }` | P0 |
| Define `AIChatType`, `AIChatMessageType`, `ResumeType` GraphQL output types | P0 |
| Define `AIChatInput`, `SendAiMessageInput`, `ResumeCreateInput` input types | P0 |
| Document AI chats module in `docs/backend/apis/17_AI_CHATS_MODULE.md` | P1 |
| Document resume module in `docs/backend/apis/18_RESUME_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `LambdaAIClient` in `app/clients/lambda_ai_client.py` | P0 |
| Wire `createAiChat` mutation → `LambdaAIClient.create_chat(...)` | P0 |
| Wire `sendAiMessage` mutation → `LambdaAIClient.send_message(chat_uuid, message)` | P0 |
| Wire `generateCompanySummary` mutation → `LambdaAIClient.generate_company_summary(company_uuid)` | P0 |
| Wire `analyzeEmailRisk` mutation → `LambdaAIClient.analyze_email_risk(email_input)` | P0 |
| Wire `parseContactFilters` mutation → `LambdaAIClient.parse_filters(natural_language_query)` | P0 |
| Implement `ResumeAIClient` in `app/clients/resume_ai_client.py` | P0 |
| Wire `createResume` → `ResumeAIClient.create(...)` + store reference in appointment360 DB | P0 |
| Persist AI chat messages in appointment360 `ai_chats` / `ai_chat_messages` tables (or delegate to contact.ai) | P0 |
| Deduct credits per AI chat message / company summary generation | P0 |

---

## Surface track

| Task | Priority |
| --- | --- |
| AI chat panel (sidebar or modal) → `mutation createAiChat` + `mutation sendAiMessage` | P0 |
| AI chat history panel → `query aiChats()` | P0 |
| Company detail page, AI summary tab → `mutation generateCompanySummary` | P0 |
| Email campaign compose screen, risk analysis → `mutation analyzeEmailRisk` | P1 |
| Filter builder natural-language input → `mutation parseContactFilters` | P1 |
| Resume builder page → `query resumes()` + `mutation createResume` / `updateResume` | P1 |
| SSE / streaming support for `sendAiMessage` (if contact.ai returns chunked response) | P1 |
| Loading skeleton while AI response is streamed | P1 |
| `useAiChat` hook: manage chat state, send message, streaming tokens | P0 |
| `useCompanySummary` hook: trigger + poll generation | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `ai_chats` table: uuid, user_uuid, title, created_at | P0 |
| Create `ai_chat_messages` table: uuid, chat_uuid, role (user/assistant), content, created_at | P0 |
| Create `resumes` table: uuid, user_uuid, content JSON, template_id, created_at | P1 |
| Track AI usage per feature in `credits` table | P0 |
| Store `parseContactFilters` parsed VQL in `saved_searches` if user saves it | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `LAMBDA_AI_API_URL`, `LAMBDA_AI_API_KEY` in `.env.example` | P0 |
| Configure `RESUME_AI_BASE_URL`, `RESUME_AI_API_KEY` | P1 |
| Add AI chat cost estimates to billing plan limits | P0 |
| Write integration test: `createAiChat → sendAiMessage → aiChat(uuid)` round-trip | P1 |
| Write contract test: `generateCompanySummary` → LambdaAI REST call | P1 |

---

## Email app surface contributions (era sync)

- Added `Ask AI` nav placeholder and defined AI-assist task backlog for mailbox operations.
- Planned AI flows: summarize, classify, and reply-assist from email detail context.
