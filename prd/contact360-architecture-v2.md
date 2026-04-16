# Contact360 — Complete Architecture Blueprint
> AI-Driven, Microservices-Based CRM Platform | v2.0 | April 2026

---

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [Layer 1 — Presentation Layer](#2-presentation-layer)
3. [Layer 2 — API Layer (BFF + GraphQL/REST)](#3-api-layer)
4. [Layer 3 — Microservices Layer](#4-microservices-layer)
5. [Layer 4 — Data Layer](#5-data-layer)
6. [Layer 5 — AI Layer](#6-ai-layer)
7. [Event-Driven Backbone](#7-event-driven-backbone)
8. [MCP — Model Control Panel](#8-mcp-model-control-panel)
9. [Connector Service (VQL)](#9-connector-service-vql)
10. [Multi-Tenant SaaS Design](#10-multi-tenant-saas-design)
11. [Security Architecture](#11-security-architecture)
12. [AWS Infrastructure](#12-aws-infrastructure)
13. [CI/CD & DevOps](#13-cicd--devops)
14. [Observability](#14-observability)
15. [AI Feedback Loop & Continuous Learning](#15-ai-feedback-loop--continuous-learning)
16. [Full Tech Stack](#16-full-tech-stack)

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                                │
│        Next.js Web App │ Admin Panel │ Chrome Extension              │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ HTTPS / WSS / GraphQL
┌───────────────────────────────▼──────────────────────────────────────┐
│                      API LAYER (BFF)                                 │
│        API Gateway │ GraphQL Federation │ REST Proxy                 │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────────┘
   │      │      │      │      │      │      │      │
┌──▼──────▼──────▼──────▼──────▼──────▼──────▼──────▼─────────────────┐
│                    MICROSERVICES LAYER                               │
│  CRM │ Email │ Phone │ Campaign │ Connector(VQL) │ Storage           │
│  AI Agent │ Notification │ Integration │ MCP                        │
└──┬──────┬──────────────────────────────────────────────────────────┘
   │      │           Event Bus (Kafka / Redis Streams)
┌──▼──────▼────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                     │
│   PostgreSQL │ OpenSearch │ Redis │ S3 │ Vector DB (pgvector)        │
└──────────────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                        AI LAYER                                      │
│          LLM (OpenAI/Local) │ Tool Calling │ Workflow Automation     │
└──────────────────────────────────────────────────────────────────────┘
```

### Core Design Principles
| Principle | Implementation |
|-----------|---------------|
| Microservices | Each service independently deployable, versioned, and scaled |
| Event-Driven | Kafka + Redis Streams for async service communication |
| AI-First | AI embedded in every workflow, not bolted on as a feature |
| Multi-Tenant SaaS | org_id isolation via RLS at DB level + JWT claim propagation |
| GraphQL + REST Hybrid | GraphQL for UI data fetching, REST for service-to-service |
| API-First | Every service exposes versioned OpenAPI spec |

---

## 2. Presentation Layer

### 2.1 Next.js Web App (Primary CRM UI)
```
tech:       Next.js 14 (App Router) + React 18 + TailwindCSS
state:      Zustand (local) + React Query (server state + caching)
realtime:   WebSocket (Socket.io) for live deal updates + AI notifications
auth:       NextAuth.js → JWT from auth-service
gql client: Apollo Client (persisted queries + normalized cache)
```

**Key Pages & Views:**
```
/dashboard          → AI Mission Control (Today's priority actions, forecast)
/contacts           → Contact list + AI enrichment status + lead scores
/contacts/[id]      → Contact 360 view (timeline, deals, AI insights)
/deals              → Kanban pipeline + win probability per card
/deals/[id]         → Deal detail + AI next-best-action panel
/campaigns          → Campaign builder + AI audience segmentation
/ai-chat            → Natural Language CRM interface (chatbot)
/analytics          → Dashboards + AI revenue forecast
/settings           → Org settings, integrations, API keys, billing
```

**AI-Native UI Components:**
```typescript
<LeadScoreBadge score={87} grade="A" trend="up" />
<NextBestAction deal={deal} onAccept={handleAction} />
<AIDraftEmail contact={contact} onSend={handleSend} />
<PipelineForecast data={forecast} confidence={0.82} />
<ChurnRiskAlert account={account} riskScore={0.68} />
<ContactTimeSuggestion contact={contact} />
```

### 2.2 Admin Panel (Internal Operations)
```
tech:       Next.js 14 + App Router + TailwindCSS
purpose:    Org management, usage analytics, billing, feature flags
access:     Super-admin only (separate JWT issuer)
features:
  - Tenant management (create, suspend, configure orgs)
  - Usage metrics per org (API calls, AI credits, storage)
  - Model performance monitoring (lead scoring accuracy, NBA hit rate)
  - Feature flag management (LaunchDarkly / custom)
  - Billing & invoice management (Stripe dashboard embed)
  - System health dashboard (all services + DB metrics)
```

### 2.3 Chrome Extension (LinkedIn Enrichment)
```
manifest:   Chrome MV3 (Manifest Version 3)
tech:       TypeScript + Vite + React (sidebar panel)
permissions: activeTab, storage (in-memory only), scripting

Architecture:
  ├── manifest.json          (MV3 config)
  ├── background/
  │   └── service-worker.ts  (API calls, JWT storage, offline queue)
  ├── content/
  │   ├── linkedin.ts        (DOM parser — user triggered only)
  │   └── overlay.ts         (Sidebar injector)
  └── sidebar/
      └── App.tsx            (Enrichment UI, real-time status)

Enrichment Flow:
  1. User clicks "Capture & Enrich" on LinkedIn profile
  2. Content script parses: name, title, company, location (public DOM only)
  3. Service worker POSTs to /api/v1/enrich/contact
  4. Backend enrichment: phone (Apollo → Twilio HLR → DND) + email (pattern → SMTP)
  5. Results stream back via SSE → sidebar updates live (Truecaller-style)
  6. Contact auto-saved to CRM with full audit trail

Legal Compliance:
  - User-triggered ONLY — no auto-scraping
  - Public data only (visible on LinkedIn page)
  - Audit log per capture: userId, sourceUrl, timestamp, dataFields[]
  - GDPR right-to-erasure supported
```

---

## 3. API Layer

### 3.1 API Gateway (Kong)
```yaml
# kong.yml (declarative config)
services:
  - name: auth-service
    url: http://auth-service:3001
    routes:
      - paths: ["/auth"]
  - name: crm-service
    url: http://crm-service:3002
    routes:
      - paths: ["/api/v1/contacts", "/api/v1/deals", "/api/v1/tasks"]
    plugins:
      - jwt          # validate RS256 JWT, inject org_id
      - rate-limiting # 1000 req/min per org
      - request-transformer  # inject X-Org-Id from JWT claims
      - correlation-id       # attach trace ID to every request
      - prometheus    # metrics per route

global_plugins:
  - name: jwt
    config:
      secret_is_base64: false
      key_claim_name: "sub"
  - name: cors
  - name: bot-detection
  - name: ip-restriction
```

### 3.2 GraphQL Federation (BFF Layer)
```
purpose:    Single GraphQL endpoint for all UI clients
tech:       Apollo Federation v2 + Apollo Router
pattern:    BFF (Backend for Frontend) — shaped for UI consumption

Subgraphs:
  ├── crm-subgraph      (contacts, deals, tasks, companies)
  ├── campaign-subgraph  (campaigns, sequences, analytics)
  ├── ai-subgraph        (scores, recommendations, drafts)
  ├── user-subgraph      (users, orgs, roles, settings)
  └── analytics-subgraph (reports, forecasts, KPIs)

Example Query:
  query DealDetail($id: ID!) {
    deal(id: $id) {
      id title value stage
      contact {
        name email phone
        leadScore { score grade trend }
        bestContactTime { time confidence }
      }
      aiInsights {
        winProbability
        nextBestAction { type description cta }
        churnRisk
      }
      activities(last: 10) { type summary createdAt }
    }
  }

Persisted Queries:  enabled (reduces payload, prevents arbitrary queries)
Depth Limit:        10 levels max
Rate Limiting:      100 complex queries/min per org
```

### 3.3 REST API (Service-to-Service)
```
Versioning:     /api/v1/... (URL versioning)
Auth:           Service-to-service via internal JWT (short-lived, 5min)
Format:         JSON, snake_case fields
Pagination:     cursor-based (cursor + limit, no offset)
Error Format:
  {
    "error": {
      "code": "CONTACT_NOT_FOUND",
      "message": "Contact with id abc123 not found",
      "requestId": "req_xyz",
      "timestamp": "2026-04-14T01:05:00Z"
    }
  }
```

---

## 4. Microservices Layer

### 4.1 CRM Service
```
tech:         Node.js 20 + Fastify + Prisma ORM
port:         3002
database:     PostgreSQL (write) + PostgreSQL read replica (queries)
search:       OpenSearch (via search-sync-service consumer)
cache:        Redis (contact detail cache, 5min TTL)

Core Entities:  Contact, Company, Deal, Task, Activity, Note, Pipeline
Key Features:
  - Full CRUD with multi-tenant RLS
  - Pipeline stage management with custom stages per org
  - Activity feed (calls, emails, meetings, notes)
  - Bulk import (CSV via S3) + export (async job)
  - Contact duplicate detection (fuzzy name + email match)
  - Deal merge and contact merge workflows

Kafka Events Published:
  contact.created | contact.updated | contact.deleted | contact.merged
  deal.created    | deal.updated    | deal.stage_changed | deal.closed
  task.created    | task.assigned   | task.completed | task.overdue
  company.created | company.updated
```

### 4.2 Email Service
```
tech:         Node.js 20 + Fastify + BullMQ workers
port:         3003
database:     PostgreSQL (enrichment results, job metadata)
queue:        Redis (BullMQ job queues per tier)

Capabilities:
  A. Email Enrichment
     - Pattern engine: john.doe@, jdoe@, j.doe@, john@... (12 patterns)
     - External APIs: Hunter.io → Apollo → Skrapp (waterfall)
     - Confidence scoring per found email
  B. Email Verification
     - Syntax validation (regex + RFC 5322)
     - Domain MX record check
     - SMTP mailbox check (non-intrusive)
     - ZeroBounce API for catch-all domains
  C. Outbound Email
     - Provider: SendGrid (primary) + AWS SES (fallback)
     - Tracking: open pixel (1x1 img) + click redirect
     - Unsubscribe: one-click (RFC 8058) + list management
  D. Inbound Email Sync
     - Gmail OAuth2 sync (IMAP/Gmail API)
     - Outlook OAuth2 sync (Microsoft Graph API)
     - Auto-link threads to CRM contacts + deals

Rate Limiting (Redis token buckets):
  Hunter.io:     500 req/day
  ZeroBounce:    200 req/day
  SendGrid:      10k emails/day (free tier)
```

### 4.3 Phone Service
```
tech:         Node.js 20 + Fastify + BullMQ workers
port:         3004
database:     PostgreSQL (enrichment results)
queue:        Redis (BullMQ)

Pipeline:
  1. Normalize input → E.164 format (libphonenumber-js)
  2. Apollo / People Data Labs API lookup
  3. Twilio HLR (Home Location Register) — is SIM active?
  4. TRAI DND Registry check (India) via API
  5. Carrier detection (Jio / Airtel / BSNL / Vi)
  6. Line type: mobile / landline / VoIP / toll-free
  7. Write to PostgreSQL with confidence score

DND Compliance:
  - All outbound phone campaigns check dnd_registered flag
  - DND records cached for 24h (Redis) — TRAI updates daily
  - Violations blocked at campaign-service level
```

### 4.4 Campaign Service
```
tech:         Node.js 20 + Express + BullMQ
port:         3005
database:     PostgreSQL (campaigns, sequences, stats)
queue:        Redis (BullMQ scheduled jobs)

Campaign Types:
  - Email campaigns (one-time blast + drip sequences)
  - WhatsApp campaigns (Meta Business API)
  - SMS campaigns (Twilio / MSG91)
  - Multi-channel sequences (email → wait → WhatsApp → wait → SMS)

AI-Powered Features:
  - Audience segmentation: AI suggests best segments for campaign goal
  - Send-time optimization: per-contact best time from ContactTimeOptimizer
  - Subject line A/B testing: AI generates 3 variants, auto-picks winner at 20% open
  - Personalization tokens: {{contact.first_name}}, {{deal.title}}, AI-generated snippets

Sequence Automation:
  trigger: deal.stage_changed OR contact.created OR custom_event
  → Step 1: Send email (day 0)
  → Step 2: Wait 3 days, check: opened? → if NO → send follow-up
  → Step 3: WhatsApp message if no reply in 7 days
  → Step 4: Task for rep to call if no engagement in 14 days
```

### 4.5 Connector Service (VQL)
```
tech:         Node.js 20 + Fastify
port:         3006
purpose:      Business Query Language — unified data access layer

VQL (Business Query Language):
  A custom DSL that translates plain-English-like queries into
  multi-source data fetches across PostgreSQL + OpenSearch + Redis.

  Examples:
    FIND contacts WHERE
      company.industry = "automotive"
      AND lead_score > 70
      AND last_activity > 30.days.ago
      AND NOT dnd_registered
    ORDER BY lead_score DESC
    LIMIT 50

  VQL Query → Connector Service:
    → Parses AST
    → Generates PostgreSQL query (Prisma)
    → Merges with OpenSearch filter for full-text fields
    → Checks Redis cache
    → Returns unified result set

  Used by:
    - AI Agent's search_contacts() tool
    - Campaign Service for audience targeting
    - Analytics Service for custom reports
    - NL Interface (converts LLM output → VQL)
```

### 4.6 Storage Service
```
tech:         Node.js 20 + Express + AWS SDK v3
port:         3007
storage:      AWS S3 (ap-south-1)

Operations:
  - Presigned PUT URLs (CSV uploads, file attachments) — 15min expiry
  - Presigned GET URLs (export downloads) — 15min expiry
  - CDN URL generation (CloudFront for profile avatars)
  - File type validation (magic bytes check, not extension)
  - Virus scanning (ClamAV on upload via Lambda trigger)
  - Lifecycle policies: temp files deleted after 7 days

Folder Structure:
  s3://contact360-prod/
  ├── {org_id}/
  │   ├── imports/         (CSV uploads — deleted after processing)
  │   ├── exports/         (Generated exports — 7 day TTL)
  │   ├── attachments/     (Email/deal file attachments)
  │   └── avatars/         (Contact profile images — CDN served)
  └── system/
      └── logs/            (Audit log exports)
```

### 4.7 AI Agent Service
```
tech:         Python 3.12 + FastAPI + LangGraph + LangChain
port:         3008
LLMs:         OpenAI GPT-4o (primary) | Anthropic Claude 3.5 | Gemini 1.5 Pro
              Local: Ollama (llama3.1 for on-prem deployments)
vector:       pgvector (PostgreSQL extension) + pgvector index
memory:       Redis (short-term session) + pgvector (long-term)

Agent Architecture (LangGraph StatefulGraph):
  ┌──────────────────────────────────────────────┐
  │           CRM AGENT STATE                   │
  │  messages[], context{}, tools[], org_id      │
  │                                              │
  │  Nodes:                                      │
  │  PLAN    → decompose task into steps         │
  │  RETRIEVE → hybrid RAG (OpenSearch+pgvector) │
  │  REASON  → LLM generates action plan         │
  │  ACT     → tool calls with validation        │
  │  REFLECT → self-check output quality         │
  │  RESPOND → structured final answer           │
  │  ESCALATE→ human-in-the-loop if uncertain    │
  └──────────────────────────────────────────────┘

Available Tools:
  search_contacts(query, filters)       → VQL connector
  get_deal_history(deal_id)             → CRM service
  get_activity_timeline(contact_id)     → CRM service
  draft_email(contact_id, goal, tone)   → LLM + CRM context
  create_task(deal_id, title, due_date) → CRM service
  update_deal_stage(deal_id, new_stage) → CRM service [CONFIRM]
  send_email(draft_id)                  → Email service [CONFIRM]
  score_lead(contact_id)                → ML model inference
  find_similar_deals(deal_id)           → pgvector similarity
  get_pipeline_summary(rep_id)          → Analytics service
  search_knowledge_base(query)          → RAG over notes+docs

Human-in-Loop (CONFIRM tagged tools require approval):
  → Agent presents action + asks "Should I proceed?"
  → User approves → action executes
  → User edits → agent adjusts + re-presents
  → User rejects → agent suggests alternatives

ML Models:
  lead_scorer.pkl          XGBoost, retrained weekly
  deal_win_prob.pkl        Gradient Boosted Tree, daily retrain
  churn_predictor.pkl      Random Forest, weekly retrain
  contact_time_model.pkl   Time-series per contact, daily update
  email_subject_opt.pkl    Multi-armed bandit, continuous update
```

### 4.8 Notification Service
```
tech:         Node.js 20 + Express + Socket.io
port:         3009
channels:     SendGrid │ Twilio SMS │ Meta WhatsApp API
              Slack Bolt SDK │ Firebase FCM │ WebSocket (in-app)

Kafka events consumed → notification triggered:
  contact.enriched   → "Your enrichment job completed (247 contacts)"
  deal.assigned      → Slack + email to assigned rep
  task.overdue       → Push + in-app to rep
  campaign.completed → Email summary to manager
  ai.action_ready    → In-app proactive suggestion card
  churn.risk_alert   → Slack channel alert + rep email

In-App Notification (WebSocket):
  Socket.io room per user: room = `user:${userId}`
  Socket.io room per org:  room = `org:${orgId}`
  → Live pipeline updates (deal stage changes)
  → AI recommendation cards (NBA)
  → Enrichment job completions
  → Mention notifications

Notification Preferences:
  Per user: channel preference, quiet hours, digest vs real-time
  Stored: PostgreSQL notifications_preferences table
```

### 4.9 Integration Service
```
tech:         Node.js 20 + Express
port:         3010
purpose:      Third-party system connectors + webhook management

Inbound Webhooks:
  - Zapier, Make.com, n8n triggers
  - Stripe payment events → deal auto-updated
  - Signature verification: HMAC-SHA256 on every webhook
  - Idempotency: deduplicate by event_id (Redis 24h cache)

Outbound Webhooks:
  - Org-configured webhook URLs for any CRM event
  - Retry: exponential backoff (1s, 2s, 4s, 8s, 16s)
  - Dead letter after 5 failures → alert

Third-Party Connectors:
  Gmail / Outlook     OAuth2 token, sync emails to activity feed
  Google Calendar     OAuth2, sync meetings to CRM tasks
  Stripe              API key, payment events → deal stage updates
  Slack               OAuth2 bot, push AI briefs, handle commands
  HubSpot             API key, one-time migration import
  Salesforce          OAuth2, bidirectional sync (premium feature)
  LinkedIn Sales Nav  OAuth2, profile enrichment (premium)
```

### 4.10 MCP — Model Control Panel
```
tech:         Python 3.12 + FastAPI
port:         3011
purpose:      Central registry + lifecycle management for all AI models

Responsibilities:
  A. Model Registry
     - Version control for all ML models (lead scorer, churn, win prob)
     - A/B test new model vs current (traffic split: 10/90 → 50/50 → 100)
     - Rollback to previous version in < 30 seconds
     - Model metadata: accuracy, F1, training date, feature list

  B. LLM Configuration
     - Per-org LLM selection (GPT-4o vs Claude vs local Ollama)
     - System prompt management + versioning
     - Token budget management (per org per day)
     - Fallback chain: GPT-4o → Claude → local Llama

  C. Prompt Management
     - Versioned prompt templates (email draft, NBA, score explanation)
     - A/B test prompts (measure output quality via user feedback)
     - Per-org prompt customization (tone, language, domain-specific)

  D. AI Observability
     - LLM call logs (prompt, response, tokens, latency, model)
     - Model drift detection (alert if accuracy drops > 5%)
     - Hallucination rate tracking (human-feedback flagged)
     - Cost tracking per org (OpenAI / Anthropic token spend)

MCP API:
  GET  /mcp/models               → list all models + status
  POST /mcp/models/{id}/deploy   → deploy new version
  POST /mcp/models/{id}/rollback → rollback to previous
  GET  /mcp/prompts              → list prompt templates
  PUT  /mcp/prompts/{id}         → update prompt template
  GET  /mcp/usage                → token usage per org
  GET  /mcp/ab-tests             → active A/B test results
```

---

## 5. Data Layer

### 5.1 PostgreSQL (Primary DB)
```sql
-- Core schema with multi-tenancy

CREATE TABLE orgs (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name       VARCHAR(255) NOT NULL,
  slug       VARCHAR(100) UNIQUE NOT NULL,
  plan       VARCHAR(50) DEFAULT 'starter',
  settings   JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE contacts (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id          UUID REFERENCES orgs(id),
  first_name      VARCHAR(100) NOT NULL,
  last_name       VARCHAR(100),
  email           VARCHAR(255),
  email_verified  BOOLEAN DEFAULT FALSE,
  email_confidence NUMERIC(3,2),
  phone           VARCHAR(30),
  phone_e164      VARCHAR(20),
  phone_verified  BOOLEAN DEFAULT FALSE,
  dnd_registered  BOOLEAN DEFAULT FALSE,
  carrier         VARCHAR(50),
  lead_score      INTEGER,                  -- 0-100 from ML model
  lead_grade      CHAR(1),                  -- A/B/C/D
  embedding       vector(1536),             -- pgvector for AI similarity
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (multi-tenancy enforcement)
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON contacts
  USING (org_id = current_setting('app.current_org_id')::uuid);

-- pgvector index for AI similarity search
CREATE INDEX contacts_embedding_idx ON contacts
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Other core tables follow same pattern:
-- companies, deals, tasks, activities, notes, campaigns,
-- email_enrichment_results, phone_enrichment_results,
-- notifications, webhook_configs, audit_logs
```

### 5.2 OpenSearch (Search Engine)
```
Cluster:    3 nodes (ap-south-1), 100GB EBS per node
Version:    OpenSearch 2.x

Index Design:
  contacts-v1:
    mappings:
      name:       text (analyzer: standard + ngram for autocomplete)
      email:      keyword
      phone:      keyword
      company:    text + keyword
      lead_score: integer
      org_id:     keyword   ← always filtered, never surfaced
      tags:       keyword[]

  deals-v1:
    mappings:
      title:      text
      stage:      keyword
      value:      double
      win_prob:   double
      owner_id:   keyword
      org_id:     keyword

Search Features:
  - Full-text search across contacts, deals, companies, notes
  - Autocomplete (edge ngram tokenizer)
  - Faceted filtering (by stage, owner, score range, date)
  - Highlight snippets in search results
  - Fuzzy matching (edit distance 1) for typo tolerance

Sync Strategy:
  PostgreSQL → Kafka event → search-sync-service → OpenSearch upsert
  Idempotent: UUID as document _id, upsert not insert
  DLQ: failed syncs → retry queue → alert after 3 failures
```

### 5.3 Redis (Cache + Queue)
```
Version:    Redis 7.x (ElastiCache cluster mode, 3 shards)
Use Cases:

  CACHE (TTL-based):
    contact:{id}         → 5 minutes  (CRM service)
    search:{query_hash}  → 60 seconds (OpenSearch results)
    lead_score:{id}      → 1 hour     (ML inference result)
    best_time:{id}       → 24 hours   (ContactTimeOptimizer)
    org_settings:{id}    → 5 minutes  (config cache)

  QUEUES (BullMQ):
    email-enrichment     → email-service workers
    phone-enrichment     → phone-service workers
    campaign-send        → campaign-service workers
    ai-agent-tasks       → ai-agent-service workers
    notification-send    → notification-service workers

  RATE LIMITING (token buckets):
    ratelimit:{org_id}:{api}  → per org per external API

  SESSION (short-term agent memory):
    agent:{session_id}   → LangGraph checkpoint (30min TTL)

  PUBSUB:
    websocket:org:{id}   → live updates to connected clients
```

### 5.4 S3 (File Storage)
```
Bucket:     contact360-prod (versioning enabled)
Region:     ap-south-1
CDN:        CloudFront (avatars + static assets)

Lifecycle Policies:
  imports/     → delete after 7 days
  exports/     → delete after 7 days
  attachments/ → transition to S3-IA after 90 days
  avatars/     → permanent (CloudFront cached)

Security:
  - Bucket policy: deny public access
  - All access via presigned URLs or CloudFront signed cookies
  - Server-side encryption: SSE-S3
  - Versioning enabled (accidental delete protection)
```

### 5.5 Vector DB (pgvector)
```
Extension:  pgvector on PostgreSQL
Embedding model: OpenAI text-embedding-3-small (1536 dims)

Tables with embeddings:
  contacts.embedding     → contact profile + activity summary
  deals.embedding        → deal notes + email threads summary
  knowledge_base.embedding → org-uploaded docs (SOPs, playbooks)
  email_templates.embedding → past high-performing email drafts

Similarity Search (used by AI Agent RAG):
  SELECT id, first_name, company_name,
    1 - (embedding <=> $query_embedding) AS similarity
  FROM contacts
  WHERE org_id = $org_id
  ORDER BY embedding <=> $query_embedding
  LIMIT 20;

Hybrid RAG (OpenSearch BM25 + pgvector cosine):
  results_bm25    = opensearch.search(query, index="contacts-v1")
  results_vector  = pgvector.similarity_search(query_embedding)
  merged          = reciprocal_rank_fusion(results_bm25, results_vector)
  context_chunks  = merged[:5]  ← top 5 passed to LLM
```

---

## 6. AI Layer

### 6.1 LLM Configuration
```
Primary:    OpenAI GPT-4o      (complex reasoning, email drafts, NL interface)
Secondary:  Anthropic Claude 3.5 Sonnet  (long context, document analysis)
Tertiary:   Google Gemini 1.5 Pro  (multimodal, vision tasks)
Local:      Ollama + Llama 3.1 70B (on-prem / data-residency customers)

Selection Logic (MCP):
  if task.type == "email_draft":        use GPT-4o
  if task.type == "document_analysis":  use Claude (128k context)
  if task.context_length > 50k:         use Gemini (1M context)
  if org.plan == "on_prem":             use local Ollama
  on_failure: fallback to next in chain
```

### 6.2 Tool Calling Architecture
```python
# Tool calling with structured outputs (OpenAI function calling)

tools = [
  {
    "name": "search_contacts",
    "description": "Search CRM contacts using filters",
    "parameters": {
      "type": "object",
      "properties": {
        "query":  {"type": "string"},
        "filters": {
          "type": "object",
          "properties": {
            "lead_score_min": {"type": "integer"},
            "industry":       {"type": "string"},
            "days_since_contact": {"type": "integer"},
            "dnd_registered": {"type": "boolean"}
          }
        },
        "limit": {"type": "integer", "default": 20}
      }
    }
  },
  # ... 11 more tools (see AI Agent Service section)
]

# Agent loop
response = llm.chat(messages, tools=tools)
while response.tool_calls:
  for tool_call in response.tool_calls:
    if tool_call.name in REQUIRES_CONFIRMATION:
      yield HumanApprovalRequest(tool_call)  # pause for human
    else:
      result = await execute_tool(tool_call)
      messages.append(ToolResult(tool_call.id, result))
  response = llm.chat(messages, tools=tools)
```

### 6.3 Workflow Automation
```
Trigger-based automations (no-code, user configurable):

  WHEN  deal.stage_changed TO "proposal"
  DO:
    1. AI: Draft personalized follow-up email
    2. AI: Generate win/loss prediction
    3. Task: "Schedule demo within 3 days" → assigned to rep
    4. Notify: Slack message to rep manager

  WHEN  contact.lead_score DROPS BELOW 40
  DO:
    1. AI: Analyze why score dropped
    2. Alert: Rep assigned to contact
    3. Campaign: Enroll in re-engagement sequence

  WHEN  deal.no_activity FOR 7 DAYS
  DO:
    1. AI: Draft re-engagement email → present to rep
    2. Notify: "Deal going cold" in-app notification
    3. Task: "Follow up" assigned to rep

  Stored as JSON workflow definitions in PostgreSQL
  Executed by workflow-engine inside AI Agent Service
  Versioned + auditable (who created, when changed)
```

---

## 7. Event-Driven Backbone

### 7.1 Kafka Topic Registry
```
Domain          Topic                       Consumers
──────────────────────────────────────────────────────────────────
CRM             crm.contacts.created        search-sync, ai-agent, analytics
CRM             crm.contacts.updated        search-sync, ai-agent
CRM             crm.deals.created           ai-agent, analytics, notification
CRM             crm.deals.stage_changed     ai-agent, campaign, notification
CRM             crm.tasks.overdue           notification
Email           email.enriched              notification, crm (update contact)
Email           email.sent                  analytics
Email           email.opened                campaign (trigger sequences)
Email           email.bounced               email-service (suppress list)
Phone           phone.enriched              notification, crm
Phone           phone.dnd_flagged           crm (update dnd_registered)
Campaign        campaign.completed          analytics, notification
AI              ai.lead_scored              crm (update score), notification
AI              ai.action_recommended       notification (in-app card)
AI              ai.feedback.captured        mcp (model retraining input)
Audit           audit.user_action           audit-log-service
System          system.job.failed           ops-alert-service
```

### 7.2 Redis Streams (Low-Latency Events)
```
Used for: real-time UI updates (< 100ms latency requirement)
  stream:live-updates:{org_id}  → WebSocket push to connected clients
  stream:ai-suggestions:{user_id} → NBA cards in UI

Consumer groups per stream for horizontal scaling
```

### 7.3 Dead Letter Queue Strategy
```
Every Kafka consumer:
  → On failure: retry 3 times (exponential backoff)
  → After 3 failures: publish to {topic}.dlq
  → DLQ consumer: alert Slack ops channel + log to S3
  → Manual replay tool: /admin/dlq/replay/{topic}
  → SLA: DLQ messages reviewed within 4 hours
```

---

## 8. MCP — Model Control Panel

*(See Section 4.10 for full spec)*

**Key Dashboard Metrics:**
```
Model Performance:
  Lead Scorer        Accuracy: 84.2%  ▲ +2.1% vs last week
  Win Probability    MAE: 0.089       ▼ improving
  Churn Predictor    Recall: 0.91     ▲ excellent

LLM Usage (today):
  GPT-4o:            12,400 tokens    $0.37
  Claude 3.5:         3,200 tokens    $0.048
  Total AI spend:     $0.42 / org / day

Active A/B Tests:
  email_draft_v3 vs v4   (38% vs 36% user acceptance, n=312, not significant)
  lead_score_v8 vs v9    (84.2% vs 86.1% accuracy, deploying v9 tomorrow)
```

---

## 9. Connector Service (VQL)

*(See Section 4.5 for full spec)*

**VQL Grammar Reference:**
```
FIND <entity>
  WHERE <field> <op> <value>
  [AND <field> <op> <value>]*
  [ORDER BY <field> ASC|DESC]
  [LIMIT <n>]
  [INCLUDE <related_entity>]

Entities:    contacts | deals | tasks | companies | activities
Operators:   = | != | > | < | >= | <= | IN | NOT IN
             CONTAINS | STARTS_WITH | ENDS_WITH
             IS NULL | IS NOT NULL
Special:     30.days.ago | this.week | this.month
             lead_score.grade = "A"   (derived field)

Examples:
  FIND deals WHERE stage = "negotiation" AND win_prob > 0.6
  FIND contacts WHERE last_activity > 30.days.ago AND lead_score > 70
  FIND companies WHERE industry = "fintech" INCLUDE contacts LIMIT 100
```

---

## 10. Multi-Tenant SaaS Design

### Isolation Architecture
```
Layer               Isolation Method
────────────────────────────────────────────────────────────
Database (PG)       Row Level Security (RLS) on all tables
                    app.current_org_id set at connection level
Search (OpenSearch) org_id filter on every query (mandatory)
Cache (Redis)       Key namespace: {resource}:{org_id}:{id}
Storage (S3)        Path prefix: s3://bucket/{org_id}/...
Kafka               org_id in every event payload
API Gateway         org_id injected from JWT (never trusted from client)
WebSocket           Rooms namespaced per org: org:{org_id}
```

### Tenant Plans
```
Plan        Contacts  Campaigns  AI Credits  Integrations  Price
──────────────────────────────────────────────────────────────────
Starter     1,000     5/month    100/month   Gmail only    Free
Growth      10,000    unlimited  1,000/mo    All standard  ₹2,999/mo
Business    50,000    unlimited  5,000/mo    All + API     ₹7,999/mo
Enterprise  unlimited unlimited  custom      Custom + SSO  Custom
```

---

## 11. Security Architecture

### JWT Strategy
```
Access Token:
  Algorithm:  RS256 (asymmetric — public key in Kong)
  Claims:     { sub: userId, org: orgId, role, plan, exp: now+1h }
  Storage:    memory only (JS variable) — never localStorage
  Refresh:    httpOnly cookie, 30-day rolling expiry

Service-to-Service:
  Algorithm:  HS256 (shared secret per service pair)
  Expiry:     5 minutes
  Scope:      source_service → target_service only
```

### OWASP Mitigations
```
A01 Broken Access Control:
  → RLS on all DB tables, ownership check in service layer
  → IDOR prevention: org_id from JWT, never from request body

A02 Cryptographic Failures:
  → TLS 1.3 everywhere, HSTS
  → RDS encrypted at rest (AES-256), S3 SSE-S3
  → Secrets: AWS Secrets Manager (auto-rotation 30 days)

A03 Injection:
  → Prisma ORM (parameterized queries only)
  → Zod schema validation on all inputs
  → OpenSearch queries use term/match, not raw DSL from user

A07 Auth Failures:
  → Rate limiting on /auth: 5 failed logins → 15min lockout
  → MFA via TOTP (optional, enterprise)
  → Refresh token rotation (new token per use)

A09 Logging Failures:
  → Structured JSON logs, correlation IDs
  → PII masked in logs (email: "r***@m***.com")
  → Audit log: all data mutations to immutable S3 archive
```

---

## 12. AWS Infrastructure

```
Region:   ap-south-1 (Mumbai) — India data residency

VPC Layout:
  CIDR: 10.0.0.0/16
  Public Subnets (10.0.1.0/24, 10.0.2.0/24):
    - Application Load Balancer
    - NAT Gateway
  Private Subnets (10.0.10.0/24, 10.0.11.0/24):
    - ECS Fargate (all microservices)
    - Lambda functions
  Data Subnets (10.0.20.0/24, 10.0.21.0/24):
    - RDS PostgreSQL Multi-AZ
    - ElastiCache Redis cluster
    - MSK Kafka cluster
    - OpenSearch cluster

ECS Fargate Services:
  Service                 CPU    Mem    Min  Max  Scale Trigger
  ─────────────────────────────────────────────────────────────
  auth-service            0.5    1GB    2    10   CPU > 70%
  crm-service             1.0    2GB    3    20   CPU > 70%
  email-service           0.5    1GB    2    8    Queue depth > 100
  phone-service           0.5    1GB    2    8    Queue depth > 100
  ai-agent-service        1.0    4GB    2    6    CPU > 60%
  campaign-service        0.5    1GB    2    8    Queue depth > 50
  notification-service    0.25   512MB  2    10   CPU > 70%
  analytics-service       0.5    2GB    2    6    CPU > 60%
  integration-service     0.25   512MB  2    6    CPU > 70%
  connector-service       0.5    1GB    2    8    CPU > 70%
  storage-service         0.25   512MB  2    4    CPU > 70%
  mcp-service             0.5    2GB    1    4    CPU > 60%
  search-sync-service     0.25   512MB  2    4    Kafka lag > 1000

Lambda Functions:
  csv-validator            (S3 trigger, on upload)
  webhook-processor        (API Gateway, inbound webhooks)
  scheduled-reports        (EventBridge, daily 9 AM IST)
  dnd-registry-updater     (EventBridge, daily 2 AM IST)
  model-retrainer          (EventBridge, weekly Sunday 1 AM IST)

RDS (PostgreSQL 16):
  Instance: db.r6g.large (Multi-AZ)
  Storage:  500GB gp3 (autoscale to 2TB)
  Backup:   Automated daily, 30-day retention
  Read replicas: 2 (for analytics + search-sync read queries)
  pgvector extension enabled

MSK (Kafka):
  Brokers:  3 (msk.m5.large)
  Topics:   auto-create disabled, managed via IaC
  Retention: 7 days

OpenSearch:
  Nodes:    3 (r6g.large.search)
  Storage:  100GB per node (gp3)
  Replicas: 1 per shard

ElastiCache Redis:
  Mode:     Cluster (3 shards, 1 replica each)
  Instance: cache.r6g.large per shard
  Eviction: allkeys-lru
```

---

## 13. CI/CD & DevOps

### GitHub Actions Pipeline
```yaml
# .github/workflows/service-deploy.yml

on:
  push:
    branches: [main]
    paths: ['services/${{ matrix.service }}/**']

jobs:
  ci:
    steps:
      - lint:         ESLint / Ruff
      - unit-tests:   Jest / pytest (threshold: 80% coverage)
      - build:        Docker buildx (multi-arch: amd64 + arm64)
      - scan:         Snyk (block if critical CVE found)
      - push:         ECR (tag: {service}:{sha})

  deploy-staging:
    needs: ci
    steps:
      - update ECS task definition
      - deploy to staging
      - integration tests (Supertest / HTTPx)
      - e2e tests (Playwright)
      - performance test (k6: 500 VUs, p99 < 500ms)
      - quality gate: all pass

  approve:
    needs: deploy-staging
    environment: production   # GitHub environment protection rule
    # → Slack notification to @lead-engineer for approval

  deploy-prod:
    needs: approve
    steps:
      - blue/green: create new task set
      - health check: 5 minutes
      - canary: 10% → 50% → 100% traffic
      - auto-rollback: error_rate > 1% OR p99 > 500ms
      - notify: Slack deploy success
```

### Turborepo (Monorepo Optimization)
```json
{
  "pipeline": {
    "build":   { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "test":    { "dependsOn": ["build"] },
    "lint":    { "outputs": [] },
    "deploy":  { "dependsOn": ["build", "test", "lint"], "cache": false }
  }
}
```
_Only changed services rebuild — saves 70% CI time on large PRs._

---

## 14. Observability

### Three Pillars
```
LOGS (CloudWatch):
  Format:    Structured JSON { timestamp, level, service, requestId, orgId, ... }
  No PII:    email → "r***@m***.com", phone → "+91XXXXXX3456"
  Retention: 90 days live → S3 Glacier archive 2 years
  Alerting:  CloudWatch Alarms → SNS → PagerDuty on-call

METRICS (Prometheus + Grafana):
  RED metrics per service: Rate, Errors, Duration
  Business metrics: deals_created, enrichment_success_rate, ai_response_time
  Infrastructure: CPU, RAM, DB pool, Kafka consumer lag
  SLO dashboards: per-service availability + latency targets

TRACES (OpenTelemetry → AWS X-Ray):
  Trace propagation: W3C TraceContext headers
  Coverage: UI → Gateway → Service → DB query → Kafka publish
  Slow span detection: auto-highlight spans > 100ms

SLOs:
  Auth Service         99.99% availability, p95 < 100ms
  CRM Service          99.95% availability, p95 < 200ms
  AI Agent Service     99.90% availability, p95 < 3s
  Search              99.95% availability, p95 < 150ms
  Enrichment Jobs     99.90% success rate (async)
```

---

## 15. AI Feedback Loop & Continuous Learning

```
User Action                    Signal               Weight
────────────────────────────────────────────────────────────
Sends AI email draft as-is   → strong positive      1.0
Edits draft slightly (<30%)  → weak positive        0.7
Rewrites draft completely    → negative             -0.5
Acts on NBA suggestion       → positive             1.0
Ignores NBA suggestion       → weak negative        -0.3
Lead closes Won              → score was right      +1.0 to lead_scorer
Lead closes Lost             → score was wrong      -1.0 to lead_scorer
Rep overrides AI prediction  → model missed         logged for retraining

All feedback events:
  → Kafka: ai.feedback.captured
  → Stored in PostgreSQL (ai_feedback table)
  → Weekly: batch retraining pipeline (SageMaker)
  → Monthly: A/B test new model vs current (MCP)
  → Quarterly: feature importance review + new feature addition
```

---

## 16. Full Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web UI | Next.js 14, React 18, TailwindCSS, Apollo Client | Primary CRM interface |
| Admin Panel | Next.js 14, App Router | Ops + tenant management |
| Chrome Extension | Chrome MV3, TypeScript, Vite, React | LinkedIn enrichment |
| API Gateway | Kong (declarative) | Routing, JWT, rate limiting |
| GraphQL Federation | Apollo Federation v2, Apollo Router | BFF for UI clients |
| CRM Service | Node.js 20, Fastify, Prisma | Core CRM entities |
| Email Service | Node.js 20, Fastify, BullMQ | Enrichment + sending |
| Phone Service | Node.js 20, Fastify, BullMQ | Enrichment + validation |
| Campaign Service | Node.js 20, Express | Multi-channel campaigns |
| Connector Service | Node.js 20, Fastify | VQL query engine |
| Storage Service | Node.js 20, Express, AWS SDK v3 | S3 file management |
| AI Agent Service | Python 3.12, FastAPI, LangGraph | Orchestration + RAG |
| Notification Service | Node.js 20, Express, Socket.io | All notification channels |
| Integration Service | Node.js 20, Express | 3rd-party connectors |
| MCP | Python 3.12, FastAPI | Model + prompt management |
| ORM | Prisma (Node), SQLAlchemy + Alembic (Python) | DB access |
| Primary DB | PostgreSQL 16 + pgvector (RDS Multi-AZ) | CRM data + embeddings |
| Search | OpenSearch 2.x | Full-text + faceted search |
| Cache + Queues | Redis 7 (ElastiCache cluster) | Cache, BullMQ, sessions |
| File Storage | AWS S3 + CloudFront | Files, exports, avatars |
| Message Broker | Apache Kafka (MSK) | Async event streaming |
| AI: LLMs | OpenAI GPT-4o, Claude 3.5, Gemini 1.5, Ollama | Language generation |
| AI: Orchestration | LangGraph, LangChain | Agent workflows |
| ML Models | XGBoost, scikit-learn, SageMaker | Lead scoring, churn |
| Infrastructure | AWS ECS Fargate, RDS, MSK, ElastiCache | Cloud hosting |
| IaC | Terraform | Infrastructure as code |
| CI/CD | GitHub Actions, Turborepo | Build + deploy pipeline |
| Monitoring | CloudWatch, Prometheus, Grafana, Sentry, X-Ray | Observability |
| Security | AWS Secrets Manager, Kong JWT, ACM | Auth + secrets |

---

*Contact360 Architecture Blueprint v2.0 | April 2026*
*AI-First · Microservices · Event-Driven · Multi-Tenant SaaS*
