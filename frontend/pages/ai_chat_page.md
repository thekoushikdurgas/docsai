---
title: "AI Chat"
page_id: ai_chat_page
source_json: ai_chat_page.json
generator: json_to_markdown.py
---

# AI Chat

## Overview

- **page_id:** ai_chat_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 5.x, 9.x, 11.x
- **flow_id:** ai_chat
- **_id:** ai_chat_page-001

## Metadata

- **route:** /ai-chat
- **file_path:** contact360.io/app/app/(dashboard)/ai-chat/page.tsx
- **purpose:** NexusAI Pro: Conversational interface for data exploration, company research, and automated workflow triggers.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Gated via DashboardAccessGate (pageId: ai-chat). Pro/Feature.AI_CHAT access required.
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
### uses_endpoints (6)

- `graphql/ListAIChats` — List AI chats via aiChats.chats. Optional filters: search, date range. Via aiChatService.listChats in useAiChat. Limit 25.
- `graphql/GetAIChat` — Get chat by ID via aiChats.chat. Used after WebSocket complete and in streamMessage fallback. Via aiChatService.getChat.
- `graphql/CreateAIChat` — Create new chat via aiChats.createChat. Default title 'New Conversation'. Via aiChatService.createChat.
- `graphql/UpdateAIChat` — Update chat via aiChats.updateChat (title, metadata). Used by service; may be called on send or rename.
- `graphql/DeleteAIChat` — Delete chat via aiChats.deleteChat. Via aiChatService.deleteChat in ChatSidebar and ChatHeader clear.
- `graphql/SendMessage` — Send message via aiChats.sendMessage. Primary for SSE fallback; WebSocket preferred when available. Via aiChatService.sendMessage/streamMessage.

### UI components (metadata)

- **AiChatPage** — `app/(dashboard)/ai-chat/page.tsx`
- **ChatSidebar** — `components/features/ai-chat/ChatSidebar.tsx`
- **ChatHeader** — `components/features/ai-chat/ChatHeader.tsx`
- **ChatMessagesList** — `components/features/ai-chat/ChatMessagesList.tsx`
- **ChatWelcomeOrInput** — `components/features/ai-chat/ChatWelcomeOrInput.tsx`
- **ChatRateLimitAlert** — `components/features/ai-chat/ChatRateLimitAlert.tsx`
- **ChatMobileSidebar** — `components/features/ai-chat/ChatMobileSidebar.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`

- **versions:** []
- **endpoint_count:** 6
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

AI Chat

### description

AI chat assistant (NexusAI Pro) with sidebar (chat list, search), model selector, message streaming via WebSocket or SSE fallback, rate limit handling. Create/delete chats, send messages. Pro/feature access gated.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| sidebar | 2 | Chat Sidebar |
| main | 2 | Main Chat Area |


### subheadings



### era

5.x


### tabs



### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| handleCreateNewChat | Sidebar | new-trace | New Trace | primary | 5.x |
| handleSend | ChatInput | execute-command | Execute neural command | primary | 0.x |
| deleteChat | Sidebar | delete-trace | Delete Trace | ghost | 5.x |
| handleCopy | ChatBubble | copy-message | Copy | ghost | 0.x |
| setIsSidebarOpen(false) | Sidebar | collapse-sidebar | Collapse | ghost | 0.x |
| setUseSearch | ChatHeader | toggle-search | Search | switch | 5.x |
| setIsThinking | ChatHeader | toggle-thinking | Thinking | switch | 5.x |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| react | useState | Manages chat session list and current active chat | 0.x |
| react | useMemo | Filters chat sessions for search functionality | 0.x |
| react | useEffect | Handles auto-scrolling to the latest message | 0.x |
| lib/animationsConfig | getAnimationSrc | Retrieves Lottie animation paths for AI states | 5.x |
| setUseSearch | ChatHeader | toggle-search | Search | switch | 5.x |
| setIsThinking | ChatHeader | toggle-thinking | Thinking | switch | 5.x |


### input_boxes

| component | id | label | placeholder | required | type | era |
| --- | --- | --- | --- | --- | --- | --- |
| ChatInput | neural-command | Execute neural command | Execute neural command... | True | textarea | 0.x |
| Sidebar | trace-search | Search traces | Search traces... | False | search | 5.x |



### text_blocks

| component | content | id | type | era |
| --- | --- | --- | --- | --- |
| EmptyState | Neural Node Ready | node-ready | heading | 5.x |
| EmptyState | Initializing CRM cognitive bridge. | cognitive-bridge | info | 5.x |
| ChatHeader | Feed_Live | live-feed | status | 5.x |
| ChatHeader | G3P_PRE | reasoning-model | badge | 5.x |
| ChatInput | ENC_TUNNEL | encrypted-tunnel | security | 9.x |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ChatWelcomeOrInput | chat-send-flow | Send message flow | ['User types message in textarea (auto-expand)', 'Press Enter or click Send button', 'WebSocket connection used if available, SSE fallback', 'aiChatsService.SendMessage mutation', 'AI tokens stream ba |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/ai-chat/ChatSidebar.tsx | ChatSidebar | Left panel: chat list, search, new chat button |
| components/features/ai-chat/ChatHeader.tsx | ChatHeader | Current chat title + delete/clear + mobile sidebar toggle |
| components/features/ai-chat/ChatMessagesList.tsx | ChatMessagesList | Scrollable message list with user/AI bubble + streaming render |
| components/features/ai-chat/ChatWelcomeOrInput.tsx | ChatWelcomeOrInput | Welcome screen or message input textarea + send button |
| components/features/ai-chat/ChatRateLimitAlert.tsx | ChatRateLimitAlert | Rate limit warning banner with countdown timer |
| components/features/ai-chat/ChatMobileSidebar.tsx | ChatMobileSidebar | Mobile-responsive sidebar drawer |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useAiChat.ts | useAiChat | Chat CRUD, message streaming (WebSocket + SSE fallback), rate limit state |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/aiChatsService.ts | aiChatsService | ['ListAIChats', 'GetAIChat', 'CreateAIChat', 'UpdateAIChat', 'DeleteAIChat', 'SendMessage'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User identity for chat ownership |
| context/RoleContext.tsx | RoleContext | Feature.AI_CHAT gate via DashboardAccessGate |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy individual AI message content |


### ui_components



### endpoints

| hook | method | operation | service | transport |
| --- | --- | --- | --- | --- |
| useAiChat | QUERY | ListAIChats | aiChatsService |  |
| useAiChat | MUTATION | CreateAIChat | aiChatsService |  |
| useAiChat | MUTATION | DeleteAIChat | aiChatsService |  |
| useAiChat | MUTATION | SendMessage | aiChatsService | WebSocket + SSE fallback |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| new-chat | New Chat | primary | aiChatsService.CreateAIChat | ChatSidebar |
| send-message | Send | primary | aiChatsService.SendMessage → WebSocket/SSE stream | ChatWelcomeOrInput |
| stop-stream | Stop | secondary | abort streaming connection | ChatWelcomeOrInput |
| delete-chat | Delete Chat | danger | aiChatsService.DeleteAIChat → ConfirmModal | ChatHeader |
| clear-chat | Clear History | ghost | aiChatsService.DeleteAIChat (current) | ChatHeader |
| copy-message | Copy | icon | clipboard.copyToClipboard(message.content) | ChatMessagesList |
| open-mobile-sidebar | Chats | icon | open ChatMobileSidebar | ChatHeader |


### inputs

| id | label | type | placeholder | required | rows | auto_expand | submit_on_enter | component |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| message-input | Message | textarea | Ask anything about your contacts, companies, or B2B data... | True | 1 | True | True | ChatWelcomeOrInput |
| chat-search | Search chats | search | Search conversations... |  |  |  |  | ChatSidebar |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useAiChat.ts | useAiChat | Chat CRUD, message streaming (WebSocket + SSE fallback), rate limit state |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/aiChatsService.ts | aiChatsService | ['ListAIChats', 'GetAIChat', 'CreateAIChat', 'UpdateAIChat', 'DeleteAIChat', 'SendMessage'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/ListAIChats, graphql/GetAIChat, graphql/CreateAIChat, graphql/UpdateAIChat, graphql/DeleteAIChat, graphql/SendMessage | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: aiChatsService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useAiChat -> aiChatsService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **5.x** — AI workflows — AI chat, live voice, AI email writer product, assistant panels.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/ai-chat`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), `router.push` / `<Link>` from **### buttons** table above.

**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / [register_page.md](register_page.md); product pages on **root** deep-link to app auth.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [contacts_page](contacts_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [profile_page](profile_page.md)
- [register_page](register_page.md)
- [root_page](root_page.md)
- [sequences_page](sequences_page.md)
- [settings_page](settings_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `ListAIChats` | [query_list_ai_chats_graphql.md](../../backend/endpoints/query_list_ai_chats_graphql.md) | QUERY | 5.x |
| `GetAIChat` | [query_get_ai_chat_graphql.md](../../backend/endpoints/query_get_ai_chat_graphql.md) | QUERY | 5.x |
| `CreateAIChat` | [mutation_create_ai_chat_graphql.md](../../backend/endpoints/mutation_create_ai_chat_graphql.md) | MUTATION | 5.x |
| `UpdateAIChat` | [mutation_update_ai_chat_graphql.md](../../backend/endpoints/mutation_update_ai_chat_graphql.md) | MUTATION | 5.x |
| `DeleteAIChat` | [mutation_delete_ai_chat_graphql.md](../../backend/endpoints/mutation_delete_ai_chat_graphql.md) | MUTATION | 5.x |
| `SendMessage` | [mutation_send_message_graphql.md](../../backend/endpoints/mutation_send_message_graphql.md) | MUTATION | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
