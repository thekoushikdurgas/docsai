<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Create a single consolidated mega-markdown (0.x.x–11.x.x)

Here’s a consolidated mega-markdown spec for Contact360 covering sections **0.x.x–11.x.x**.

```markdown
# Contact360 — Mega Architecture & Design Spec (0.x.x–11.x.x)

> Consolidated technical vision, architecture, data model, services, AI layer, and operational model for the Contact360 AI CRM platform.

---

## 0.x.x — Vision, Principles & High-Level Scope

### 0.1.0 Vision

Contact360 is an **AI-first, multi-tenant CRM** that unifies structured CRM data (contacts, companies, deals) with unstructured signals (emails, calls, notes, web data) and **agentic workflows**. Instead of being just a system of record, it acts as a **system of action**: it not only stores customer information but also **recommends and executes next best actions** with human-in-the-loop controls.

Key ideas:
- **Single pane of glass for GTM teams**: sales, success, and marketing share one truth for contacts, companies, deals, and communication history.
- **AI-native from day one**: semantic memory, retrieval-augmented generation (RAG), and agent graphs are first-class, not bolted on.
- **Event-driven core**: every meaningful change (contact created, deal stage moved, campaign launched) emits events to Kafka for downstream consumers.
- **Multi-surface UX**: Web app, admin console, Chrome extension, Slack bot, and APIs all operate on the same canonical data model.

### 0.2.0 Design Principles

1. **API-first**: every capability is exposed via stable, versioned APIs; UI is a privileged client.
2. **Multi-tenancy by default**: `org_id` is present on all business tables and enforced via PostgreSQL Row-Level Security (RLS).
3. **Event-driven architecture**: writes go to PostgreSQL and emit Kafka events; derived views (OpenSearch, analytics, AI caches) subscribe.
4. **AI as orchestrator, not oracle**: agents plan, call tools, and propose actions; humans approve.
5. **Operational excellence baked in**: observability, SLOs, and runbooks are first-class documentation.

---

## 1.x.x — System Architecture Overview

### 1.1.0 High-Level Architecture

**Clients**
- Web UI (Next.js)
- Admin Console (Next.js)
- Mobile (React Native)
- Chrome Extension (MV3)
- Slack Bot

**Edge & Gateway**
- Kong API Gateway
  - JWT validation
  - Rate limiting
  - Request routing
  - Path-based service dispatch

**Backend Services (microservices)**
- Auth Service
- CRM Service
- Campaign Service
- Email Service
- Phone Service
- AI Service
- Analytics Service
- Notification Service
- Integration Service
- Billing Service
- API Gateway / BFF layer (where needed)

**Data & Infra**
- PostgreSQL 16 (+ `pgvector`, `pg_trgm`, `unaccent`)
- OpenSearch 2.x (search indices)
- Redis 7 (cache, queues, rate limits)
- Kafka 3.7 (event bus)
- S3-compatible object storage (files, exports)
- AWS ECS Fargate / Kubernetes for compute
- Datadog, Sentry, OpenTelemetry for observability

### 1.2.0 Multi-Tenancy Model

- Every row in business tables includes `org_id UUID`.
- PostgreSQL RLS enforces per-tenant isolation:
  - `ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;`
  - Policy uses `current_setting('app.current_org_id')`.
- API layer sets:
  - `SET app.current_org_id = <org_id>`
  - `SET app.role = 'user' | 'service'`
- Background services use `app.role = 'service'` policies for controlled bypass.

### 1.3.0 Stateless Services

- All services are **stateless**: no local disk state, no in-memory-only durable state.
- State is in PostgreSQL, Redis, and Kafka streams.
- Horizontal scaling via ECS/K8s (CPU/memory auto-scaling based on metrics).

---

## 2.x.x — Data Model & Storage (PostgreSQL, Redis, OpenSearch, pgvector)

### 2.1.0 Core Tenancy & Users

**organizations**
- `id UUID PK`
- `name TEXT`
- `plan TEXT` (or enum: `free`, `pro`, `enterprise`)
- `created_at`, `updated_at`

**users**
- `id UUID PK`
- `org_id UUID` → `organizations(id)`
- `name`, `email UNIQUE`, `password_hash`
- `role TEXT` (`admin`, `manager`, `user`, `readonly`)
- `status TEXT` (`active`, `invited`, `suspended`)
- Timestamps

### 2.2.0 CRM Core (Contacts & Companies)

**companies**
- `id UUID PK`, `org_id UUID`
- `name`, `domain`, `industry`, `size INT`
- `linkedin_url`, other social fields
- `created_at`, `updated_at`

**contacts**
- `id UUID PK`, `org_id UUID`
- `company_id UUID` → `companies(id)`
- `first_name`, `last_name`, `full_name`
- `email`, `phone`, `job_title`, `linkedin_url`
- `address`, `city`, `country`
- `source TEXT` (`extension`, `import`, `manual`, `ai`, `api`)
- Enrichment-related fields:
  - `email_status` (`unknown`, `valid`, `invalid`, `catch_all`, `accept_all`)
  - `email_confidence NUMERIC`
- `created_at`, `updated_at`

### 2.3.0 Deals & Pipeline

**deals**
- `id UUID PK`, `org_id UUID`
- `contact_id`, `company_id`
- `title TEXT`
- `value NUMERIC`
- `stage TEXT` (or reference to `deal_stages`)
- `status TEXT` (`open`, `won`, `lost`, `on_hold`)
- `close_date DATE`
- `created_at`, `updated_at`

Optional supporting tables:
- `deal_stages` (per-org configurable pipeline stages)
- `deal_stage_history` (auditable stage transitions)

### 2.4.0 Email System

**email_patterns**
- Inferred email patterns per domain for discovery.

**email_validations**
- Validation provider responses, including `is_valid`, `score`.

**email_logs**
- Outbound email send logs (per campaign, provider, status).

**email_engagements**
- Engagement events linked to `email_logs`:
  - `opened`, `clicked`, `replied`, plus timestamps.

### 2.5.0 Phone System

**phone_validations**
- Normalized phone validation responses:
  - `is_valid`, `carrier`, `line_type`, `country_code`.

**phone_search_logs**
- Logs of phone lookups (e.g., via Truecaller-style integration).

### 2.6.0 Campaigns & Templates

**campaigns**
- `id`, `org_id`
- `name`, `type` (`email`, `sms`, `whatsapp`)
- `status` (`draft`, `scheduled`, `running`, `paused`, `completed`)
- `scheduled_at`, `created_at`

**campaign_targets**
- `campaign_id`, `contact_id`

**campaign_messages**
- `campaign_id`, `channel`, `template_id`, `content`

**campaign_stats**
- Counters: `sent`, `delivered`, `opened`, `clicked`, `replied`

**email_templates**, **campaign_templates**
- Store subject/body and multi-step sequence definitions (JSONB).

### 2.7.0 Files, Jobs, BQL

**files**
- S3 metadata:
  - `file_name`, `file_type`, `s3_url`, `row_count`, `column_count`, `status`.

**file_columns**
- Column metadata: `column_name`, `data_type`.

**file_analysis**
- `summary JSONB` with profiling info.

**jobs**
- `type TEXT` (`import`, `export`, `enrich`)
- `status`, `progress`, `file_id`, timestamps.

**job_logs**
- Append-only logs for job progress and failures.

**bql_queries**, **bql_exports**
- BQL query text, execution metadata, and links to exported files.

### 2.8.0 AI, MCP, Integrations, Extension Data

**ai_queries**
- User queries and AI responses (auditable).

**ai_actions**
- Actions suggested or taken by agents:
  - `action_type`, `payload JSONB`, `status`.

**ai_memories**
- Long-term agent memory with embeddings (vector columns).

**integrations**
- Enabled integrations per org (`type`, `config JSONB`).

**provider_accounts**
- API keys and configs, ideally encrypted at rest.

**extension_events**
- Raw scraped data and normalized processing status.

### 2.9.0 Redis Design

Key patterns (examples):
- `contact:{id}` → cached contact JSON (TTL 5min)
- `search:{org}:{hash}` → search results cache (TTL 60s)
- `rate_limit:hunter:{org}` → per-org provider limits
- `workflow:pending:{id}` → serialized AI workflow state
- `lock:enrich:{contact_id}` → distributed lock to avoid duplicate enrichment

### 2.10.0 OpenSearch Indices

**contacts_index**
- Full-text fields: `full_name`, `company_name`, `job_title`.
- Keyword fields: `id`, `org_id`, `email`, `phone`, `email_status`.
- Custom analyzers for contact search and autocomplete.

**companies_index**
- `name`, `domain`, `industry`, with keyword and text fields.

**deals_index**, **activities_index**
- Optimized for timeline and reporting queries.

---

## 3.x.x — Microservices & Responsibilities

### 3.1.0 Auth Service

- JWT issuance, refresh, revocation.
- OAuth2 with providers (Google, GitHub).
- Tenant and role resolution from JWT claims.
- Session and token security (rotation, blacklisting).

### 3.2.0 CRM Service

- CRUD and search for:
  - Contacts, companies, deals, activities.
- BQL parsing and execution.
- Import/export pipelines (CSV via `files` + `jobs`).
- OpenSearch syncing for search indices.
- Kafka events:
  - `contact.created`, `contact.updated`, `deal.created`, `deal.stage_changed`, etc.

### 3.3.0 Email Service

- Email validation via providers (Hunter, ZeroBounce, etc.).
- Outbound sending via SMTP / SendGrid-like providers.
- Engagement tracking and writes into `email_logs` and `email_engagements`.
- Campaign dispatch for email channel.

### 3.4.0 Phone Service

- Validation and normalization using libphonenumber and providers (Twilio, NumVerify).
- TRAI-compliant handling for Indian numbers.
- Logging into `phone_validations` and `phone_search_logs`.

### 3.5.0 Campaign Service

- Multi-channel campaign orchestration.
- Drip sequences, A/B tests, and conditions.
- Coordination with Email and Phone services.
- Stats aggregation and writing to `campaign_stats`.

### 3.6.0 AI Service

- LangGraph-based agent orchestration.
- MCP server exposing CRM tools.
- Embeddings generation, RAG retrieval, scoring models.
- Kafka consumers for CRM events (e.g., lead scoring on `deal.created`).

### 3.7.0 Analytics, Notification, Integration, Billing

- **Analytics**:
  - Consumes Kafka topics to build analytical views.
  - Provides reporting APIs.
- **Notification**:
  - Sends email, Slack, in-app notifications.
- **Integration**:
  - Manages external connectors (Gmail, Slack, Salesforce, HubSpot, WhatsApp).
  - Webhook ingestion and normalization.
- **Billing**:
  - Tracks usage, plans, and invoices.
  - Integrates with Stripe or equivalent.

---

## 4.x.x — API Layer

### 4.1.0 REST API

- Versioning: `/v1/...`
- Standard conventions:
  - Pagination: `page`, `limit`, `cursor`.
  - Filtering: `filter[field]=value`, `filter[stage]=open`, etc.
  - Sorting: `sort=created_at:desc`.
- Error handling:
  - `{ "error": { "code": "ERROR_CODE", "message": "...", "details": {...} } }`.

Example: `POST /v1/contacts` (create contact) with enrichment trigger.

### 4.2.0 GraphQL

- Schema exposing:
  - `Contact`, `Company`, `Deal`, `Campaign`, etc.
- Queries for dashboards and 360 views.
- Mutations for updates and actions.
- Subscriptions for real-time updates.

### 4.3.0 WebSocket

- Channels:
  - `pipeline:{org_id}`, `contact:{id}`, `campaign:{id}`.
- Messages for:
  - Status updates, AI streaming tokens, activity feed updates.

### 4.4.0 Webhooks

- Outbound events:
  - `contact.created`, `deal.won`, `campaign.sent`, etc.
- Security:
  - HMAC signatures.
  - Timestamps and replay protection.
- Retry semantics:
  - Exponential backoff with max attempts.

---

## 5.x.x — Frontend (Web, Admin, Mobile, Components)

### 5.1.0 Web App (Next.js)

- Pages:
  - `/contacts`, `/contacts/[id]`
  - `/companies`, `/companies/[id]`
  - `/deals`, `/deals/board`
  - `/campaigns`
- State management via React Query / TanStack Query.
- URL-driven filters and views.

### 5.2.0 Admin Console

- Org-wide settings:
  - Users, roles, and invitations.
  - Billing and subscription.
  - Integration setup.

### 5.3.0 Mobile App

- Core capability:
  - View and edit contacts, companies, deals.
  - Log activities on the go.
  - Receive push notifications (e.g., deal won, assigned tasks).

### 5.4.0 Shared Components

- Design system:
  - Buttons, inputs, dropdowns, modals.
- Complex components:
  - Contact card, deal card, pipeline board, data table.
  - AI chat widget, file uploader, activity feed, analytics charts.

---

## 6.x.x — AI, MCP & Embeddings

### 6.1.0 Agent Architecture

- LangGraph `StateGraph` with:
  - Supervisor node orchestrating tool-calling nodes.
  - Tools for CRM operations:
    - `get_contact`, `create_contact`, `update_deal`, `create_task`, `send_email`, etc.
- Human-in-the-loop:
  - Agents pause when actions are high-impact.
  - Slack approval via buttons; resume on approval.

### 6.2.0 MCP (Model Context Protocol)

- CRM MCP server:
  - Tools: `search_contacts`, `get_deal`, `update_pipeline_stage`, `create_campaign`.
  - Resources: read-only views on CRM data.
- LLMs use MCP tools rather than raw HTTP calls.

### 6.3.0 RAG & Embeddings

- `pgvector` for:
  - Contact embeddings, long-form notes, email threads, documents.
- HNSW indexes:
  - `m = 16`, `ef_construction = 64`.
- Hybrid retrieval:
  - Combine pgvector cosine similarity with OpenSearch `ts_rank`.
  - Rank Fusion (RRF) for final scoring.

### 6.4.0 Models & Scoring

- Lead scoring:
  - Inputs: firmographics (company size, industry), behavior (opens, clicks), pipeline history.
- Win probability:
  - Based on stage, activity, deal value, and historical patterns.
- Churn prediction & email sentiment:
  - For customer success workflows and prioritization.

### 6.5.0 Prompting

- System prompts:
  - Agent role, safety boundaries, data access rules.
- Few-shot examples:
  - For rewriting emails, summarizing accounts, generating follow-up plans.
- Prompt versioning:
  - Each prompt has an ID and version; stored and auditable.

---

## 7.x.x — Browser Extension & Ingestion

### 7.1.0 Chrome Extension (MV3)

- **Content scripts**:
  - LinkedIn profile scraper.
  - Gmail context reading (subject, participants) respecting user privacy and scopes.
- **Background service worker**:
  - Auth token management.
  - API calls to Contact360.
  - Queues and retries when offline.

### 7.2.0 Data Ingestion Flow

1. User triggers extension on a page (e.g., LinkedIn profile).
2. Content script extracts relevant fields safely.
3. Background script posts to backend:
   - `POST /v1/extension/events`
4. Backend normalizes:
   - Creates/updates contacts, companies.
   - Schedules enrichment jobs.
5. Extension UI shows contact existence and status.

---

## 8.x.x — Enrichment Pipelines

### 8.1.0 Email Enrichment

- Pattern discovery:
  - Infer company email pattern from known addresses.
- Provider chaining:
  - Hunter → ZeroBounce → fallback providers.
- Confidence scoring:
  - Combination of provider scores and pattern confidence.
- Deduplication:
  - Avoid repeated provider calls by caching in Redis.

### 8.2.0 Phone Validation

- Normalization:
  - Convert to E.164 using libphonenumber.
- Validation and enrichment:
  - Country, carrier, line type (mobile, landline, VoIP).
- Compliance:
  - TRAI rules for Indian SMS and WhatsApp sending.
  - Respect opt-in/opt-out flags.

---

## 9.x.x — Campaigns & Automation

### 9.1.0 Email Campaigns

- Template system:
  - Personalized templates with merge fields.
- Deliverability:
  - Warm-up guidance, bounce handling, spam scoring.
- Tracking:
  - Pixel-based open tracking.
  - Click tracking via redirect links.

### 9.2.0 SMS & WhatsApp

- SMS:
  - Via Twilio or equivalent.
  - DLT registration and template rules for India.
- WhatsApp:
  - BSP integration (e.g., Twilio/360dialog).
  - Approved templates and session messages.

### 9.3.0 Sequences & Automation

- Drip sequences:
  - Multi-step flows across channels.
- Conditions:
  - Trigger next step based on opens, clicks, replies.
- A/B tests:
  - Subject/body variants and path variants.
- Exit rules:
  - Stop sequences on reply, unsubscribe, or conversion.

---

## 10.x.x — Integrations, Infra & Security

### 10.1.0 Integrations

- **Gmail**:
  - OAuth2 and email sync.
- **Slack**:
  - Commands, notifications, and agent interfaces.
- **WhatsApp BSP**:
  - Template management, inbound/outbound messages.
- **Salesforce & HubSpot**:
  - Field mapping and bidirectional sync.
- **Custom Webhooks**:
  - Extensible event delivery to third-party systems.

### 10.2.0 Infrastructure

- AWS VPC with public/private subnets.
- ECS Fargate (or Kubernetes) for microservices.
- RDS for PostgreSQL, ElastiCache for Redis.
- S3 for file storage, CloudFront for CDN.
- Terraform modules for infrastructure.

### 10.3.0 Security & Compliance

- Auth:
  - JWT, OAuth2, optional MFA.
- RBAC:
  - `admin`, `manager`, `user`, `readonly`.
- OWASP:
  - Input validation, CSRF mitigation, secure headers.
- Compliance:
  - GDPR: data export/delete, DPA, regional data handling.
  - TRAI: SMS and WhatsApp compliance for Indian numbers.
- Audit logging:
  - Critical actions and security events.

---

## 11.x.x — Observability, Testing, Runbooks, ADRs

### 11.1.0 Observability

- Logging:
  - Structured logs (JSON) including `org_id`, `user_id`, `request_id`.
- Metrics:
  - Service SLOs (availability, latency, error rate).
- Tracing:
  - OpenTelemetry spans across gateway, services, and DB.

### 11.2.0 Testing Strategy

- **Unit tests**:
  - Business logic and pure functions.
- **Integration tests**:
  - Testcontainers for PostgreSQL, Redis, Kafka.
- **E2E tests**:
  - Playwright for UI + API interaction.
- **Performance tests**:
  - k6 scripts for API load and bottleneck analysis.

### 11.3.0 Runbooks & Incident Management

- Runbooks for:
  - Kafka consumer lag.
  - DB failover.
  - Campaign dispatch issues.
  - AI service degradation.
- On-call:
  - PagerDuty (or similar) integration.
  - Escalation policies and SLO-driven alerts.

### 11.4.0 Architecture Decision Records (ADRs)

- Microservices vs Monolith.
- PostgreSQL as primary DB.
- Kafka for event bus.
- LangGraph for agent orchestration.
- pgvector vs Pinecone for embeddings.
- MCP protocol adoption for tool abstraction.
- Monorepo structure for services and docs.

---
```

If you want, I can now split this into numbered files (e.g. `0-overview.md` … `11-observability-testing.md`) or extend it up through 18.x.x (infra, security, runbooks, ADRs, changelog).

