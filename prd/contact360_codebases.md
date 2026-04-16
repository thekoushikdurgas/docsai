# Contact360 — Codebase Map (All 15 Repositories)

> **Monorepo strategy:** Turborepo root with 15 `apps/` workspaces + shared `packages/`
> **Container strategy:** Each codebase = one Docker image → deployed as ECS Fargate task
> **Language matrix:** TypeScript (Next.js, Node services) · Python (AI Agent, MCP) · Go (API Gateway)

---

## Repo Overview

```
contact360/
├── apps/
│   ├── web/                   # 01 — Web App (Next.js)
│   ├── admin/                 # 02 — Admin Panel (Next.js)
│   ├── extension/             # 03 — Chrome Extension (MV3)
│   ├── api-gateway/           # 04 — API Gateway (Go + Kong)
│   ├── crm-service/           # 05 — CRM Service (NestJS)
│   ├── email-service/         # 06 — Email Service (NestJS)
│   ├── phone-service/         # 07 — Phone Service (NestJS)
│   ├── campaign-service/      # 08 — Campaign Service (NestJS)
│   ├── connector-service/     # 09 — Connector / BQL (NestJS)
│   ├── storage-service/       # 10 — Storage Service (Fastify)
│   ├── ai-agent-service/      # 11 — AI Agent Service (Python/FastAPI)
│   ├── notification-service/  # 12 — Notification Service (NestJS)
│   ├── integration-service/   # 13 — Integration Service (NestJS)
│   ├── mcp/                   # 14 — MCP Control Panel (NestJS)
│   └── ai-mcp/                # 15 — AI MCP Chat Interface (Python/FastAPI)
├── packages/
│   ├── types/                 # Shared TypeScript types (Contact, Deal, Job…)
│   ├── ui/                    # Shared React component library
│   ├── config/                # ESLint, TSConfig, Prettier presets
│   ├── kafka/                 # Typed Kafka producer/consumer wrapper
│   ├── auth/                  # JWT validation middleware (all services)
│   ├── logger/                # Pino structured logging
│   └── errors/                # Standard error codes + HTTP responses
├── infra/
│   ├── terraform/             # AWS VPC, ECS, RDS, Redis, MSK
│   ├── k8s/                   # Kubernetes manifests (alt deployment)
│   └── docker-compose.yml     # Local full-stack dev
├── docs/
│   ├── architecture.md
│   ├── data-flows.md
│   ├── frontend.md
│   └── codebases.md           # ← this document
├── turbo.json
├── pnpm-workspace.yaml
└── .github/workflows/
    ├── ci.yml                 # Turborepo affected build + test
    └── deploy.yml             # Per-service ECS deploy on merge to main
```

---

## Shared Packages

```ts
// packages/types  — used by all TS codebases
export interface Contact { id: string; orgId: string; name: string; email?: string; ... }
export interface Job     { id: string; type: JobType; status: JobStatus; progress: number; ... }
export interface Campaign { id: string; steps: Step[]; status: CampaignStatus; ... }

// packages/kafka  — typed wrapper around kafkajs
export const producer = createProducer<ContactCreatedEvent>('contact.created');
export const consumer = createConsumer<ContactCreatedEvent>('contact.created', handler);

// packages/auth   — shared JWT middleware
export const withAuth = (roles?: Role[]) => NestJS guard | Fastify preHandler | Go middleware
```

---

## 01 — Web App

**Path:** `apps/web/`
**Framework:** Next.js 15 (App Router) · Tailwind v4 · TypeScript
**Port:** 3000

> Full architecture documented in `docs/frontend.md`

### Key Responsibilities
- Primary user-facing CRM interface (9 pages)
- BFF thin layer via Next.js Route Handlers
- SSE proxy to backend job streams
- Auth via NextAuth (JWT → API Gateway)

### External Dependencies
```
→ api-gateway          (all data mutations + queries)
→ ai-agent-service     (AI insight panel, streaming)
→ ai-mcp               (⌘K /ask queries)
→ storage-service      (presigned S3 URLs for CSV upload)
```

### Build
```bash
pnpm --filter web dev       # :3000
pnpm --filter web build
pnpm --filter web type-check
```

---

## 02 — Admin Panel

**Path:** `apps/admin/`
**Framework:** Next.js 15 · Tailwind · TypeScript
**Port:** 3001
**Access:** Internal only (VPN + IP allowlist)

### Key Responsibilities
- Super-admin org management (create, suspend, billing)
- User management across all orgs
- Feature flag control per org
- System-wide audit log viewer
- Provider quota override
- Background job monitoring (all orgs)
- Data export (GDPR delete requests)

### Pages
```
/orgs              Org list + create + suspend
/orgs/[id]         Org detail: users, usage, billing, limits
/users             Global user search + impersonate
/jobs              All background jobs (all orgs)
/flags             Feature flags (LaunchDarkly-style, DB-backed)
/audit             Global audit trail
/system            Health dashboard: all services
/billing           Stripe subscription management
```

### External Dependencies
```
→ api-gateway      (admin-scoped endpoints, role=super_admin)
→ crm-service      (org data)
→ notification-service (broadcast announcements)
```

### Build
```bash
pnpm --filter admin dev     # :3001
```

---

## 03 — Chrome Extension

**Path:** `apps/extension/`
**Framework:** Manifest V3 · React · TypeScript · Tailwind
**Build Tool:** Vite + CRXJS plugin
**Target:** Chrome 120+

### Key Responsibilities
- LinkedIn profile DOM parsing (content script)
- Real-time enrichment sidebar (React panel)
- Save-to-CRM flow
- SSE-based live enrichment feedback (Truecaller-style)
- JWT auth via chrome.storage.local (no localStorage)

### File Structure
```
apps/extension/
├── manifest.json
├── src/
│   ├── background/
│   │   └── service-worker.ts    # Handles auth, API calls, SSE relay
│   ├── content/
│   │   ├── linkedin.ts          # DOM parser for LinkedIn profiles
│   │   ├── injector.ts          # Injects sidebar into page
│   │   └── parsers/
│   │       ├── profile.ts       # Name, title, company, connections
│   │       ├── email.ts         # Visible email extraction
│   │       └── phone.ts         # Visible phone extraction
│   ├── sidebar/
│   │   ├── App.tsx              # React sidebar root
│   │   ├── components/
│   │   │   ├── ContactCard.tsx
│   │   │   ├── EnrichProgress.tsx  # Live waterfall steps
│   │   │   ├── SaveButton.tsx
│   │   │   └── TagSelector.tsx
│   │   └── hooks/
│   │       ├── useEnrich.ts        # Calls backend + streams SSE
│   │       └── useAuth.ts          # JWT from chrome.storage
│   ├── popup/
│   │   └── Popup.tsx            # Extension popup: login / status
│   └── options/
│       └── Options.tsx          # Settings: API key, theme, shortcuts
├── public/
│   └── icons/
└── vite.config.ts
```

### Permissions (manifest.json)
```json
{
  "permissions": ["storage", "activeTab", "identity"],
  "host_permissions": ["https://www.linkedin.com/*", "https://api.contact360.io/*"],
  "content_scripts": [{ "matches": ["https://www.linkedin.com/*"], "js": ["content/linkedin.js"] }]
}
```

### Build
```bash
pnpm --filter extension dev     # hot-reload via CRXJS
pnpm --filter extension build   # outputs dist/ → load in chrome://extensions
```

---

## 04 — API Gateway

**Path:** `apps/api-gateway/`
**Framework:** Go 1.22 + Gin · Kong Gateway (deployed separately)
**Port:** 8000 (public) · 8001 (Kong admin)

### Key Responsibilities
- Single public entry point for all clients
- JWT validation + org_id injection
- Rate limiting per org (Redis token bucket)
- Request routing to downstream services
- Response caching (Redis, GET endpoints)
- CORS, TLS termination
- API versioning (/v1, /v2)
- OpenAPI spec aggregation

### File Structure
```
apps/api-gateway/
├── main.go
├── cmd/
│   └── server.go
├── internal/
│   ├── middleware/
│   │   ├── auth.go          # JWT validation (RS256)
│   │   ├── ratelimit.go     # Redis sliding window
│   │   ├── cors.go
│   │   └── logging.go       # Structured request logs
│   ├── proxy/
│   │   ├── router.go        # Route table → upstream URLs
│   │   ├── crm.go           # /v1/contacts, /v1/deals, /v1/tasks
│   │   ├── email.go         # /v1/email/*
│   │   ├── phone.go         # /v1/phone/*
│   │   ├── campaign.go      # /v1/campaigns/*
│   │   ├── storage.go       # /v1/files/*
│   │   ├── ai.go            # /v1/ai/*
│   │   └── admin.go         # /v1/admin/* (role=super_admin)
│   ├── cache/
│   │   └── redis.go         # GET response cache
│   └── health/
│       └── handler.go       # /health, /ready
├── config/
│   └── config.go            # env-based config (viper)
└── Dockerfile
```

### Route Table
```
POST   /v1/auth/login          → auth-service
GET    /v1/contacts            → crm-service:3010
POST   /v1/contacts            → crm-service:3010
GET    /v1/contacts/:id/enrich → email-service:3020 + phone-service:3030
POST   /v1/campaigns           → campaign-service:3040
POST   /v1/email/generate      → ai-agent-service:8100 (stream)
GET    /v1/files/presign       → storage-service:3060
POST   /v1/ai/query            → ai-mcp:8200 (stream)
GET    /v1/jobs/:id/stream     → SSE proxy → storage-service/crm-service
```

---

## 05 — CRM Service

**Path:** `apps/crm-service/`
**Framework:** NestJS 10 · TypeScript · Prisma ORM
**Port:** 3010
**DB:** PostgreSQL (primary) · Redis (cache) · OpenSearch (search sync)

### Key Responsibilities
- Full CRUD for: Contacts, Companies, Deals, Tasks, Notes, Tags, Activities
- Multi-tenant data isolation via Prisma Row-Level Security
- Kafka event publishing on all mutations
- OpenSearch sync via Kafka consumer
- BQL query execution (delegated to connector-service)
- GraphQL API for frontend (nested relational data)
- Webhooks for outbound integrations

### File Structure
```
apps/crm-service/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── contacts/
│   │   ├── contacts.module.ts
│   │   ├── contacts.controller.ts   # REST endpoints
│   │   ├── contacts.resolver.ts     # GraphQL resolvers
│   │   ├── contacts.service.ts      # Business logic
│   │   ├── contacts.repository.ts   # Prisma queries
│   │   └── dto/
│   │       ├── create-contact.dto.ts
│   │       ├── update-contact.dto.ts
│   │       └── filter-contact.dto.ts
│   ├── companies/
│   ├── deals/
│   ├── tasks/
│   ├── notes/
│   ├── tags/
│   ├── activities/
│   ├── search/
│   │   └── opensearch.service.ts    # Sync + query OpenSearch
│   ├── kafka/
│   │   ├── producer.service.ts      # Publishes contact.created etc.
│   │   └── consumers/
│   │       └── enrich-result.consumer.ts
│   ├── graphql/
│   │   └── schema.gql
│   ├── prisma/
│   │   └── schema.prisma
│   └── common/
│       ├── guards/org-rls.guard.ts  # Injects orgId from JWT
│       └── interceptors/cache.interceptor.ts
├── test/
│   ├── contacts.e2e.spec.ts
│   └── contacts.service.spec.ts
└── Dockerfile
```

### Kafka Events Published
```
contact.created       { contactId, orgId, data }
contact.updated       { contactId, orgId, changes }
contact.deleted       { contactId, orgId }
deal.stage_changed    { dealId, from, to, orgId }
activity.logged       { activityId, contactId, orgId }
```

---

## 06 — Email Service

**Path:** `apps/email-service/`
**Framework:** NestJS 10 · TypeScript · BullMQ
**Port:** 3020
**Queue:** Redis (BullMQ) · External: Hunter.io, Apollo, ZeroBounce

### Key Responsibilities
- Email address generation (12 pattern engine)
- Waterfall enrichment: Pattern → Hunter → Apollo → SMTP verify → ZeroBounce
- Bulk CSV enrichment (BullMQ job batching)
- Email validation + confidence scoring
- Template management (CRUD)
- AI email generation (delegates to ai-agent-service)
- Transactional email sending (SendGrid/SES)
- Kafka consumer: `contact.created` → auto-enrich

### File Structure
```
apps/email-service/
├── src/
│   ├── enrichment/
│   │   ├── enrichment.service.ts
│   │   ├── waterfall.service.ts         # Orchestrates provider chain
│   │   ├── confidence-scorer.service.ts
│   │   └── providers/
│   │       ├── pattern-engine.provider.ts   # 12 email patterns
│   │       ├── hunter.provider.ts
│   │       ├── apollo.provider.ts
│   │       ├── smtp-verify.provider.ts
│   │       └── zerobounce.provider.ts
│   ├── validation/
│   │   ├── validation.service.ts
│   │   └── mx-check.service.ts
│   ├── templates/
│   │   ├── templates.controller.ts
│   │   └── templates.service.ts
│   ├── bulk/
│   │   ├── bulk.processor.ts        # BullMQ processor
│   │   └── bulk.service.ts
│   ├── sending/
│   │   └── sendgrid.service.ts      # Transactional emails
│   ├── kafka/
│   │   └── contact-created.consumer.ts
│   └── jobs/
│       └── jobs.controller.ts       # SSE stream endpoint
├── queues/
│   └── email-enrichment.queue.ts
└── Dockerfile
```

### API Endpoints
```
POST /email/enrich              → enrich single contact email
POST /email/bulk                → enqueue CSV enrichment job
GET  /email/jobs/:id/stream     → SSE job progress
POST /email/validate            → validate email address
GET  /email/templates           → list templates
POST /email/generate            → AI email generation (proxy to ai-agent)
POST /email/send                → transactional send (SendGrid/SES)
```

---

## 07 — Phone Service

**Path:** `apps/phone-service/`
**Framework:** NestJS 10 · TypeScript · BullMQ
**Port:** 3030
**External:** Truecaller API, NumVerify, Twilio Lookup, MSG91, TRAI DND Registry

### Key Responsibilities
- Phone number discovery from name + company
- Number validation (format, carrier, line type)
- DND registry check (TRAI India — cached 24h in Redis)
- Bulk phone validation (BullMQ)
- SMS sending (Twilio / MSG91)
- WhatsApp sending (Meta Business API)
- Kafka consumer: `contact.created` → auto phone enrich

### File Structure
```
apps/phone-service/
├── src/
│   ├── discovery/
│   │   ├── discovery.service.ts
│   │   └── providers/
│   │       ├── truecaller.provider.ts
│   │       └── numverify.provider.ts
│   ├── validation/
│   │   ├── validation.service.ts
│   │   └── dnd-check.service.ts     # TRAI DND (Redis cache 24h)
│   ├── lookup/
│   │   └── twilio-lookup.service.ts # Carrier + line type
│   ├── sending/
│   │   ├── sms.service.ts           # Twilio / MSG91
│   │   └── whatsapp.service.ts      # Meta Business API
│   ├── bulk/
│   │   └── bulk.processor.ts
│   └── kafka/
│       └── contact-created.consumer.ts
└── Dockerfile
```

---

## 08 — Campaign Service

**Path:** `apps/campaign-service/`
**Framework:** NestJS 10 · TypeScript · BullMQ (cron scheduler)
**Port:** 3040

### Key Responsibilities
- Campaign CRUD (name, goal, steps, audience, schedule)
- Step sequencer with delay + conditional branching
- BQL audience evaluation (delegates to connector-service)
- BullMQ cron job creation per campaign
- Step dispatch: routes to email-service / phone-service per channel
- Engagement tracking aggregation
- Campaign analytics (open, click, reply, bounce rates)
- A/B test variant management
- Pause / resume / cancel

### File Structure
```
apps/campaign-service/
├── src/
│   ├── campaigns/
│   │   ├── campaigns.controller.ts
│   │   ├── campaigns.service.ts
│   │   └── campaigns.repository.ts
│   ├── sequence/
│   │   ├── sequence.service.ts      # Step tree evaluation
│   │   └── step-dispatcher.service.ts  # Routes step to right channel
│   ├── scheduler/
│   │   ├── cron.service.ts          # BullMQ repeatable jobs
│   │   └── send-window.service.ts   # 08:00–18:00 Mon–Fri logic
│   ├── audience/
│   │   └── audience.service.ts      # Calls connector-service BQL
│   ├── tracking/
│   │   ├── tracking.controller.ts   # Webhook inbound (open/click/reply)
│   │   └── tracking.service.ts
│   ├── analytics/
│   │   └── analytics.service.ts
│   └── kafka/
│       ├── email-opened.consumer.ts
│       ├── email-clicked.consumer.ts
│       └── email-replied.consumer.ts
└── Dockerfile
```

---

## 09 — Connector Service (BQL)

**Path:** `apps/connector-service/`
**Framework:** NestJS 10 · TypeScript
**Port:** 3050
**Also known as:** BQL Engine (Business Query Language)

### Key Responsibilities
- Parse + execute BQL (Contact360's SQL-like query DSL)
- Multi-source query fan-out: PostgreSQL + OpenSearch + Redis + pgvector
- Audience segmentation for campaigns
- Data export query execution
- Schema introspection endpoint (frontend query builder)
- Result caching (Redis, 5 min TTL)

### BQL Grammar (sample)
```sql
SELECT contacts
WHERE company = "Acme"
  AND email.verified = true
  AND deal.stage IN ("proposal", "negotiation")
  AND lastActivity.date > NOW() - 30d
  AND enrichmentScore > 70
ORDER BY enrichmentScore DESC
LIMIT 500
```

### File Structure
```
apps/connector-service/
├── src/
│   ├── bql/
│   │   ├── parser.ts              # PEG.js grammar → AST
│   │   ├── planner.ts             # AST → execution plan
│   │   └── executor.ts            # Execute plan across sources
│   ├── sources/
│   │   ├── postgres.source.ts     # Prisma read replica
│   │   ├── opensearch.source.ts   # ES query builder
│   │   ├── redis.source.ts        # Cached aggregates
│   │   └── vector.source.ts       # pgvector similarity
│   ├── schema/
│   │   └── introspect.service.ts  # Returns available fields
│   ├── export/
│   │   └── export.service.ts      # BQL → CSV/JSON export
│   └── cache/
│       └── result-cache.service.ts
└── Dockerfile
```

---

## 10 — Storage Service

**Path:** `apps/storage-service/`
**Framework:** Fastify 4 · TypeScript
**Port:** 3060
**Storage:** AWS S3 · PostgreSQL (file metadata)

### Key Responsibilities
- Presigned URL generation (PUT for upload, GET for download)
- File metadata persistence (name, size, type, orgId, userId)
- Lambda trigger integration (S3 → validate → enqueue)
- Column mapping detection from CSV headers
- File preview (first 10 rows)
- File deletion + S3 cleanup
- SSE job result streaming

### File Structure
```
apps/storage-service/
├── src/
│   ├── app.ts
│   ├── routes/
│   │   ├── presign.ts         # GET /files/presign → S3 presigned PUT
│   │   ├── files.ts           # CRUD file metadata
│   │   ├── preview.ts         # GET /files/:id/preview → first 10 rows
│   │   └── stream.ts          # GET /files/:id/stream → SSE job progress
│   ├── services/
│   │   ├── s3.service.ts      # AWS S3 SDK wrapper
│   │   ├── metadata.service.ts
│   │   ├── csv-parser.service.ts    # Column detection + preview
│   │   └── lambda.service.ts        # Trigger Lambda for validation
│   └── db/
│       └── schema.ts          # Drizzle ORM schema (files table)
└── Dockerfile
```

---

## 11 — AI Agent Service

**Path:** `apps/ai-agent-service/`
**Framework:** Python 3.12 · FastAPI · LangGraph · LangChain
**Port:** 8100
**Models:** OpenAI GPT-4o · Anthropic Claude 3.5 · Google Gemini 1.5 Pro

### Key Responsibilities
- Hybrid RAG: BM25 (OpenSearch) + cosine (pgvector) merged via RRF
- LangGraph agent orchestration (multi-step reasoning loops)
- AI email generation (streamed, grounded in contact context)
- Lead scoring model (ML inference)
- Embedding generation for new contacts/documents
- Daily dashboard AI digest generation
- Contact AI context summary (for profile page)
- Tool-use agent: can query CRM, send emails, schedule follow-ups

### File Structure
```
apps/ai-agent-service/
├── main.py
├── app/
│   ├── api/
│   │   ├── query.py           # POST /ai/query — RAG endpoint
│   │   ├── email.py           # POST /ai/email/generate — streaming
│   │   ├── score.py           # POST /ai/score — lead scoring
│   │   ├── embed.py           # POST /ai/embed — generate embedding
│   │   ├── context.py         # GET  /ai/context/:contactId
│   │   └── digest.py          # GET  /ai/digest — daily summary
│   ├── agents/
│   │   ├── rag_agent.py       # LangGraph RAG pipeline
│   │   ├── email_agent.py     # Email generation chain
│   │   └── tools/
│   │       ├── crm_tool.py    # Query CRM service via REST
│   │       ├── search_tool.py # OpenSearch BM25 queries
│   │       ├── vector_tool.py # pgvector cosine search
│   │       └── send_tool.py   # Trigger email send
│   ├── retrieval/
│   │   ├── bm25_retriever.py
│   │   ├── vector_retriever.py
│   │   └── rrf_fusion.py      # Reciprocal Rank Fusion merger
│   ├── models/
│   │   ├── lead_scorer.py     # scikit-learn pipeline
│   │   └── embedder.py        # text-embedding-3-small wrapper
│   ├── memory/
│   │   └── agent_memory.py    # pgvector conversation memory
│   └── config/
│       └── settings.py        # pydantic-settings
├── tests/
│   └── test_rag_agent.py
└── Dockerfile
```

### LangGraph Flow
```python
# Simplified agent loop
graph = StateGraph(AgentState)
graph.add_node("plan",     plan_action)       # classify intent
graph.add_node("retrieve", hybrid_retrieve)   # BM25 + vector
graph.add_node("fuse",     rrf_fusion)        # merge results
graph.add_node("generate", llm_generate)      # grounded response
graph.add_node("tools",    tool_executor)     # CRM actions
graph.add_edge("plan",     "retrieve")
graph.add_conditional_edges("generate", should_use_tools,
                             {"yes": "tools", "no": END})
```

---

## 12 — Notification Service

**Path:** `apps/notification-service/`
**Framework:** NestJS 10 · TypeScript
**Port:** 3070

### Key Responsibilities
- In-app notifications (SSE push to frontend)
- Email notifications (job done, campaign live)
- Slack webhooks (per org configurable)
- Push notifications (FCM for mobile)
- Notification preference management
- Kafka consumer: listens to all `*.created`, `job.done`, `campaign.*` events
- Digest scheduling (daily/weekly summaries)
- Notification read/unread state

### Kafka Topics Consumed
```
contact.created      → "New contact saved: John Doe"
job.done             → "Enrichment complete: 1,200/1,240 found"
job.failed           → "Enrichment failed: Rate limit hit on Hunter.io"
campaign.sent        → "Campaign Q2 fired: 500 emails sent"
deal.stage_changed   → "Deal moved to Proposal: Acme Inc"
```

---

## 13 — Integration Service

**Path:** `apps/integration-service/`
**Framework:** NestJS 10 · TypeScript
**Port:** 3080

### Key Responsibilities
- Third-party CRM sync (HubSpot, Salesforce, Pipedrive)
- OAuth 2.0 connection management (store + refresh tokens)
- Bidirectional field mapping engine
- Webhook ingestion from external CRMs
- Contact deduplication on import
- Zapier / n8n webhook endpoint
- API key management for external providers
- Sync job scheduling (incremental + full)
- Provider health monitoring

### Supported Integrations
```
CRM Sync:    HubSpot · Salesforce · Pipedrive · Zoho
Enrichment:  Hunter.io · Apollo.io · ZeroBounce · Clearbit
Messaging:   SendGrid · AWS SES · Twilio · Meta Business API · MSG91
Automation:  Zapier · n8n · Make (Integromat)
```

### File Structure
```
apps/integration-service/
├── src/
│   ├── connections/
│   │   ├── connections.controller.ts   # OAuth flow endpoints
│   │   └── oauth.service.ts
│   ├── sync/
│   │   ├── sync.service.ts
│   │   └── field-mapper.service.ts
│   ├── providers/
│   │   ├── hubspot/
│   │   ├── salesforce/
│   │   ├── pipedrive/
│   │   └── base.provider.ts          # Abstract provider interface
│   ├── webhooks/
│   │   └── inbound.controller.ts     # Receives events from 3rd party CRMs
│   └── dedup/
│       └── dedup.service.ts          # Contact deduplication logic
└── Dockerfile
```

---

## 14 — MCP (Model Context Protocol / Control Panel)

**Path:** `apps/mcp/`
**Framework:** NestJS 10 · TypeScript
**Port:** 3090

### Key Responsibilities
- Route AI queries to correct LLM model based on intent classification
- Manage LLM provider configuration per org (model, temperature, max tokens)
- System prompt management (per org customizable)
- Token usage tracking + budget enforcement
- Conversation session management
- Tool registry (which tools each org can use)
- Rate limiting per org for AI calls
- A/B testing between LLM providers

### File Structure
```
apps/mcp/
├── src/
│   ├── routing/
│   │   ├── router.service.ts         # Intent → model selection
│   │   └── intent-classifier.ts      # Fast classification (GPT-3.5)
│   ├── config/
│   │   ├── provider-config.service.ts # Per-org LLM settings
│   │   └── system-prompt.service.ts
│   ├── sessions/
│   │   └── session.service.ts        # Conversation history (Redis)
│   ├── tools/
│   │   └── tool-registry.service.ts  # Available tools per org
│   ├── usage/
│   │   └── token-tracker.service.ts  # Cost tracking per org
│   └── ratelimit/
│       └── ai-ratelimit.service.ts   # Tokens/min per org
└── Dockerfile
```

### Routing Logic
```ts
// Intent → LLM model routing
const ROUTING = {
  "crm_query":       "gpt-4o",          // complex CRM reasoning
  "email_generate":  "gpt-4o",          // quality email writing
  "lead_score":      "gpt-3.5-turbo",   // fast classification
  "summarize":       "claude-3-haiku",  // cost-effective summary
  "code":            "claude-3-5-sonnet", // code/structured output
  "vision":          "gemini-1-5-pro",  // image + doc understanding
};
```

---

## 15 — AI MCP (Chat Interface)

**Path:** `apps/ai-mcp/`
**Framework:** Python 3.12 · FastAPI · LangChain · WebSocket
**Port:** 8200

### Key Responsibilities
- Conversational AI interface for Contact360 (chat-based)
- Multi-turn conversation with persistent memory (pgvector)
- Tool-use: query contacts, create deals, send emails, schedule campaigns
- Streaming responses (token-by-token via WebSocket / SSE)
- Context-aware using full Customer 360 data
- Human-in-the-loop: flags actions for approval before executing
- Proactive suggestions ("3 deals haven't been updated in 14 days")
- Voice input support (Whisper transcription)
- Multi-modal: understands uploaded documents and images

### File Structure
```
apps/ai-mcp/
├── main.py
├── app/
│   ├── api/
│   │   ├── chat.py            # POST /chat, WS /chat/stream
│   │   ├── history.py         # GET /chat/history
│   │   └── proactive.py       # GET /chat/suggestions
│   ├── agent/
│   │   ├── chat_agent.py      # Multi-turn LangGraph agent
│   │   ├── memory.py          # pgvector + Redis conversation memory
│   │   └── planner.py         # Tool selection + approval gating
│   ├── tools/
│   │   ├── contact_tools.py   # search_contacts, get_contact, create_contact
│   │   ├── deal_tools.py      # create_deal, update_stage, list_deals
│   │   ├── campaign_tools.py  # list_campaigns, launch_campaign
│   │   ├── email_tools.py     # draft_email, send_email
│   │   └── analytics_tools.py # get_kpis, pipeline_summary
│   ├── approval/
│   │   └── approval_gate.py   # HITL: pause + ask user before exec
│   ├── proactive/
│   │   └── suggestions.py     # Daily proactive push via cron
│   └── voice/
│       └── transcribe.py      # OpenAI Whisper integration
├── tests/
│   └── test_chat_agent.py
└── Dockerfile
```

### Tool Schema Example
```python
create_deal = StructuredTool(
    name="create_deal",
    description="Create a new deal for a contact in the CRM pipeline",
    args_schema=CreateDealInput,
    func=lambda x: requests.post(f"{CRM_SERVICE}/deals", json=x.dict()).json(),
    return_direct=False,
)

# HITL approval gate
if tool.requires_approval:
    yield ApprovalRequest(tool=tool.name, args=tool.args, message="Shall I create this deal?")
    approval = await wait_for_human_approval()
    if not approval: return "Cancelled."
```

---

## Inter-Service Communication Map

```
┌─────────────────────────────────────────────────────────────────────┐
│  CLIENT LAYER                                                       │
│  web:3000  admin:3001  extension (MV3)                             │
└───────────────────────────┬─────────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  api-gateway:8000  (Go · Kong · JWT validation · rate limit)        │
└──┬────┬────┬────┬────┬────┬────┬────┬────┬─────────────────────────┘
   │    │    │    │    │    │    │    │    │  REST (internal VPC)
   ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
  CRM  EML  PHN  CMP  CON  STG  AIA  NOT  INT
 3010 3020 3030 3040 3050 3060 8100 3070 3080

   ▲──────────────── Kafka (MSK) ────────────────▶
   All services produce/consume events async

   ▲────────── MCP:3090 ──────────▶ ai-agent-service:8100
   ▲────────── AI MCP:8200 ───────▶ all services (tool calls)

   Shared stores:
   PostgreSQL  ← CRM, Storage, Notification, Integration
   Redis       ← All services (cache, BullMQ, rate limit, session)
   OpenSearch  ← CRM (write), Connector (read)
   pgvector    ← AI Agent, AI MCP (embeddings + memory)
   S3          ← Storage Service
   Kafka (MSK) ← All services (events)
```

---

## Docker Compose (Local Dev)

```yaml
# docker-compose.yml (root)
services:
  postgres:    image: postgres:16      ports: ["5432:5432"]
  redis:       image: redis:7-alpine   ports: ["6379:6379"]
  opensearch:  image: opensearch:2.11  ports: ["9200:9200"]
  kafka:       image: bitnami/kafka    ports: ["9092:9092"]
  zookeeper:   image: bitnami/zookeeper

  # All 15 apps (via Turborepo dev)
  # pnpm dev  →  starts all apps with hot reload
```

---

## CI/CD Per Service

```yaml
# .github/workflows/ci.yml
- uses: actions/checkout with fetch-depth=0
- run: pnpm turbo run test lint type-check --filter=[HEAD^1]
  # Turborepo detects which of 15 apps changed → only runs affected

# .github/workflows/deploy.yml (on merge to main)
- build Docker image for changed service
- push to ECR
- update ECS task definition
- blue/green deploy (0-downtime)
- rollback on health check failure
```

---

## Summary Table

| # | Codebase              | Framework        | Lang   | Port | Key DB/Queue        |
|---|-----------------------|------------------|--------|------|---------------------|
| 1 | web                   | Next.js 15       | TS     | 3000 | —                   |
| 2 | admin                 | Next.js 15       | TS     | 3001 | —                   |
| 3 | extension             | MV3 + React      | TS     | —    | chrome.storage      |
| 4 | api-gateway           | Go + Gin         | Go     | 8000 | Redis               |
| 5 | crm-service           | NestJS + Prisma  | TS     | 3010 | PG · Redis · OS     |
| 6 | email-service         | NestJS + BullMQ  | TS     | 3020 | Redis (queue)       |
| 7 | phone-service         | NestJS + BullMQ  | TS     | 3030 | Redis (queue+DND)   |
| 8 | campaign-service      | NestJS + BullMQ  | TS     | 3040 | PG · Redis          |
| 9 | connector-service     | NestJS           | TS     | 3050 | PG · OS · pgvector  |
|10 | storage-service       | Fastify          | TS     | 3060 | S3 · PG             |
|11 | ai-agent-service      | FastAPI          | Python | 8100 | pgvector · OS       |
|12 | notification-service  | NestJS           | TS     | 3070 | Redis · PG          |
|13 | integration-service   | NestJS           | TS     | 3080 | PG · Redis          |
|14 | mcp                   | NestJS           | TS     | 3090 | Redis               |
|15 | ai-mcp                | FastAPI          | Python | 8200 | pgvector · Redis    |

---

*Document version: v1.0 | April 2026 | Contact360 Codebase Map*
