# Contact AI — UI Binding Matrix

**Service:** `backend(dev)/contact.ai`  
**GraphQL proxy:** `contact360.io/api` (via `LambdaAIClient`)  
**Dashboard app:** `contact360.io/app/`  
**Era relevance:** UI surface introduced `5.x`, grows through `10.x`

---

## Page and tab bindings by era

| Era | Dashboard page / route | Tabs / sections | Contact AI endpoints used |
| --- | --- | --- | --- |
| `0.x` | None (skeleton only) | — | `/health` (CI probe) |
| `1.x` | None | — | — |
| `2.x` | Contact detail page | Email risk inline badge | `POST /api/v1/ai/email/analyze` |
| `3.x` | Contact search page, Company detail | AI filter input, Company summary tab | `POST /api/v1/ai/parse-filters`, `POST /api/v1/ai/company/summary` |
| `4.x` | Extension popup (optional) | AI context panel | `POST /api/v1/ai-chats/{id}/message` |
| `5.x` | `/app/ai-chat` (new page) | Chat list, chat thread, model selector | All `/api/v1/ai-chats/` + utilities |
| `6.x` | `/app/ai-chat` | Error state, retry button, reconnect | All (with reliability wrappers) |
| `7.x` | `/app/ai-chat` + admin | Role-gated AI features | All (RBAC enforcement) |
| `8.x` | `/app/settings/api-keys` | AI API quota display | Rate limit headers |
| `9.x` | `/app/integrations` | AI-powered connector config | Webhook AI result delivery |
| `10.x` | `/app/campaigns/editor` | AI content assistant panel | `POST /api/v1/ai/email/generate` (10.x) |

---

## Component map

### Chat page components (`5.x+`)

| Component | Location (suggested) | API call | Props / state |
| --- | --- | --- | --- |
| `AIChatPage` | `app/(dashboard)/ai-chat/page.tsx` | Renders `ChatList` + `ChatThread` | Selected chat ID |
| `ChatList` | `components/ai-chat/ChatList.tsx` | `GET /api/v1/ai-chats/` | Chats array, pagination, loading |
| `ChatListItem` | `components/ai-chat/ChatListItem.tsx` | — | `uuid`, `title`, `updatedAt` |
| `NewChatButton` | `components/ai-chat/NewChatButton.tsx` | `POST /api/v1/ai-chats/` | `onChatCreated` callback |
| `ChatThread` | `components/ai-chat/ChatThread.tsx` | `GET /api/v1/ai-chats/{id}/` | Messages array, scroll ref |
| `ChatMessage` | `components/ai-chat/ChatMessage.tsx` | — | `sender`, `text`, `contacts[]` |
| `ContactsInMessage` | `components/ai-chat/ContactsInMessage.tsx` | — | Contact list (inline cards) |
| `ChatInput` | `components/ai-chat/ChatInput.tsx` | `POST /api/v1/ai-chats/{id}/message` | Input value, send handler |
| `StreamingText` | `components/ai-chat/StreamingText.tsx` | `POST /message/stream` (SSE) | Token stream, done flag |
| `ModelSelector` | `components/ai-chat/ModelSelector.tsx` | `model` field in send payload | Selected model enum |
| `ChatContextMenu` | `components/ai-chat/ChatContextMenu.tsx` | `PUT` / `DELETE` `/api/v1/ai-chats/{id}/` | Rename, delete actions |
| `AILoadingSpinner` | `components/ai-chat/AILoadingSpinner.tsx` | — | Streaming / loading state |
| `AIErrorState` | `components/ai-chat/AIErrorState.tsx` | — | Error type, retry handler |

### Utility components (inline, cross-page)

| Component | Location (suggested) | API call | Props / state |
| --- | --- | --- | --- |
| `EmailRiskBadge` | `components/contacts/EmailRiskBadge.tsx` | `POST /api/v1/ai/email/analyze` | `email`, risk score, loading |
| `CompanySummaryTab` | `components/companies/CompanySummaryTab.tsx` | `POST /api/v1/ai/company/summary` | `companyName`, `industry`, summary text |
| `AIFilterInput` | `components/contacts/AIFilterInput.tsx` | `POST /api/v1/ai/parse-filters` | NL query, parsed filters output |
| `CampaignAIAssistant` | `components/campaigns/CampaignAIAssistant.tsx` | `POST /api/v1/ai/email/generate` (`10.x`) | Subject/body generation, tone selector |

---

## Hooks

| Hook | Purpose | Wraps |
| --- | --- | --- |
| `useChatList(limit, offset)` | Fetches + paginates chat list | `aiChats` GraphQL query |
| `useChat(chatId)` | Fetches single chat with messages | `aiChat` GraphQL query |
| `useSendMessage(chatId)` | Sends message, returns updated chat | `sendMessage` GraphQL mutation |
| `useStreamMessage(chatId)` | SSE stream, appends tokens to UI state | `POST /message/stream` (direct or via gateway) |
| `useCreateChat()` | Creates new chat | `createAIChat` GraphQL mutation |
| `useDeleteChat()` | Deletes chat | `deleteAIChat` GraphQL mutation |
| `useRenameChat()` | Updates title | `updateAIChat` GraphQL mutation |
| `useEmailRisk(email)` | Analyzes email risk | `analyzeEmailRisk` GraphQL mutation |
| `useCompanySummary(name, industry)` | Generates summary | `generateCompanySummary` GraphQL mutation |
| `useParseFilters(query)` | Parses NL to filters | `parseContactFilters` GraphQL mutation |

---

## Services / contexts

| Service / Context | Purpose |
| --- | --- |
| `AIChatContext` | Global selected chat ID, chat list state, SSE stream state |
| `AIModelContext` | Selected `ModelSelection` enum value; persisted to localStorage |
| `StreamingContext` | Token buffer, stream active flag, reconnect logic |
| `LambdaAIClient` | HTTP client in appointment360 (`app/clients/lambda_ai_client.py`) |

---

## Input box / control bindings

| Control | Type | Bound to | Validation |
| --- | --- | --- | --- |
| Chat message textarea | `<textarea>` | `ChatInput.message` | Min 1 char, max 10 000 chars |
| Model selector | `<select>` / dropdown | `ModelSelector.model` | Enum: FLASH, PRO, FLASH_2_0, PRO_2_5 |
| Chat title (rename) | `<input type="text">` | `ChatContextMenu.title` | Max 255 chars |
| Email risk input | `<input type="email">` | `EmailRiskBadge.email` | Valid email, max 255 chars |
| Company name input | `<input type="text">` | `CompanySummaryTab.companyName` | Max 255 chars |
| Industry input | `<input type="text">` | `CompanySummaryTab.industry` | Max 255 chars |
| NL filter input | `<input type="text">` | `AIFilterInput.query` | Max 1000 chars |
| Pagination (chat list) | Infinite scroll / Load more button | `useChatList` offset | Max 1000 per page |

---

## Progress bars and loading states

| State | Component | Visual |
| --- | --- | --- |
| Chat loading (initial) | `ChatThread` skeleton | Skeleton rows |
| Message sending (sync) | `AILoadingSpinner` | Spinner, disabled input |
| SSE stream in progress | `StreamingText` | Token-by-token text render, cursor blink |
| Email risk loading | `EmailRiskBadge` | Inline spinner on badge |
| Company summary loading | `CompanySummaryTab` | Shimmer placeholder |
| Filter parse loading | `AIFilterInput` | Input disabled + spinner |
| Error state | `AIErrorState` | Red banner + retry button |

---

## Checkboxes and radio buttons

| Control | Usage | Component |
| --- | --- | --- |
| Model radio buttons | Select AI model for send | `ModelSelector` (radio group or segmented control) |
| Include contacts toggle | Toggle contact card display in AI response | `ChatThread` settings |
| Stream vs. sync toggle (dev mode) | Switch between SSE and sync message send | Debug settings only |

---

## Flow and graph

### Chat message flow (frontend)

```
User types message in ChatInput
  → useSendMessage() dispatches sendMessage GraphQL mutation
    → LambdaAIClient.send_message() → POST /api/v1/ai-chats/{id}/message
      → contact.ai appends user message → HF inference → appends AI reply
        → Returns updated AIChat
          → ChatThread re-renders with new messages
            → ContactsInMessage renders embedded contacts
```

### SSE streaming flow (frontend)

```
User types message in ChatInput
  → useStreamMessage() opens SSE connection
    → POST /api/v1/ai-chats/{id}/message/stream (SSE)
      → contact.ai streams tokens via Server-Sent Events
        → StreamingText appends tokens one by one
          → AILoadingSpinner hidden when done flag received
            → Updated chat persisted; ChatThread snapshot updated
```

### Utility AI flow (frontend)

```
User triggers action (hover email, click company tab, type NL query)
  → Hook dispatches GraphQL mutation (analyzeEmailRisk / generateCompanySummary / parseContactFilters)
    → LambdaAIClient → POST /api/v1/ai/{email/analyze | company/summary | parse-filters}
      → contact.ai runs HF JSON task (stateless)
        → Returns structured result
          → Component renders: EmailRiskBadge score, CompanySummaryTab text, AIFilterInput parsed chips
```

---

## Era-by-era UI surface rollout

| Era | UI features introduced |
| --- | --- |
| `0.x` | No UI; health endpoint for CI |
| `1.x` | No UI; billing guard stubs |
| `2.x` | `EmailRiskBadge` on contact email field |
| `3.x` | `CompanySummaryTab`, `AIFilterInput` on search page |
| `4.x` | Optional AI context in extension popup |
| `5.x` | Full `AIChatPage`: `ChatList`, `ChatThread`, `ChatInput`, `StreamingText`, `ModelSelector`, all utility components |
| `6.x` | `AIErrorState`, retry button, SSE reconnect, streaming reliability |
| `7.x` | Role-gated AI feature flags; admin view of AI usage |
| `8.x` | API quota display in settings; rate limit feedback in UI |
| `9.x` | AI-powered integration panel; connector config UI |
| `10.x` | `CampaignAIAssistant` in campaign editor |

---

## References

- `docs/codebases/contact-ai-codebase-analysis.md`
- `docs/backend/apis/17_AI_CHATS_MODULE.md`
- `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`
- `contact360.io/app/app/(dashboard)/` (dashboard routes)
- `contact360.io/api/app/clients/lambda_ai_client.py` (HTTP client)
