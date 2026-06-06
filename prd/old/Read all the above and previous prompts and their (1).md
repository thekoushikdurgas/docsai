<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Read all the above and previous prompts and their answers, then I want to create a project called contact360 where we create multiple codebases, some web ui codebase and, some backend codebases, and a database, and give me all docs files an end-to-end flow of this project

Here is a complete, end‑to‑end documentation plan for your **Contact360** project as a real multi-codebase system: web UIs, backend services, and database, all wired together. I’ll give you:

- The **project structure** (codebases).
- The **full docs set** you should have (filenames + purpose).
- The **end‑to‑end flow** of how everything works together.

You can treat this as the blueprint for your actual repo + docs folder.

***

## 1. Project Structure (Multiple Codebases)

Use a monorepo with multiple applications and services:

```text
contact360/
├── apps/
│   ├── web/              # Next.js main customer-facing app (dashboard/CRM)
│   ├── admin/            # Next.js or React admin console (org, billing, feature flags)
│   ├── extension/        # Chrome extension (LinkedIn/Gmail/Sales Navigator)
│   └── mcp-ui/           # Chat/MCP UI (AI assistant console)
│
├── services/
│   ├── api-gateway/      # BFF/API Gateway (REST + GraphQL, routing + aggregation)
│   ├── auth-service/     # Auth, orgs, users, roles, sessions, API keys
│   ├── crm-service/      # Contacts, companies, deals, activities
│   ├── email-service/    # Email pattern/validation/sending
│   ├── phone-service/    # Phone validation, DND, carrier lookup
│   ├── campaign-service/ # Campaigns, audiences, scheduling, events
│   ├── ai-agent-service/ # LangGraph agent, tools, MCP integration
│   ├── analytics-service/# Aggregations, dashboards, reports
│   ├── integration-service/ # Gmail/Outlook/WhatsApp/Slack connectors
│   └── file-service/     # CSV import/export, S3 metadata, job orchestration
│
├── packages/
│   ├── shared-types/     # Typescript types (DTOs, entities, events)
│   ├── shared-db/        # Prisma client, DB helpers, migrations tooling
│   ├── shared-events/    # Kafka event schemas + producers/consumers
│   ├── shared-kafka/     # Kafka client abstraction
│   ├── shared-redis/     # Redis client abstraction
│   └── ui/               # Shared UI components, design system
│
├── infra/
│   ├── k8s/              # Kubernetes manifests/Helm charts
│   ├── terraform/        # AWS: VPC, RDS, MSK, OpenSearch, S3, Redis
│   └── docker/           # Dockerfiles + docker-compose for local dev
│
└── docs/                 # All documentation (see next section)
```

Each folder under `apps/` and `services/` is its **own codebase** with its own dependencies and CI steps, but sharing types, DB client, and events through `packages/`.

***

## 2. Docs Files: Complete Set

Here is the docs tree and what each file should contain:

```text
docs/
├── 01-architecture.md
├── 02-system-diagrams.md
├── 03-database-schema.md
├── 04-api-reference.md
├── 05-event-driven.md
├── 06-ai-architecture.md
├── 07-ai-agent-reasoning.md
├── 08-extension.md
├── 09-testing-qa.md
├── 10-deployment.md
├── 11-onboarding.md
├── 12-vql-language.md
├── 13-runbook.md
└── schema.prisma          # lives alongside as DB schema
```


### 01-architecture.md — High-Level System Architecture

- Describe Contact360 as an **AI-first, multi-tenant CRM**.
- Show the main components:
    - Web UI (Next.js)
    - Admin UI
    - Chrome extension
    - API Gateway
    - Auth, CRM, Email, Phone, Campaign, AI Agent, Analytics, Integration, File services
    - Databases: PostgreSQL + pgvector, OpenSearch, Redis, S3
- Include an ASCII diagram similar to:

```text
Web UI / Admin / MCP / Extension
        │
        ▼
   API Gateway (BFF)
        │
  ┌─────┼─────────────────────────────────────┐
  │     │     │       │        │       │      │
  ▼     ▼     ▼       ▼        ▼       ▼      ▼
 Auth  CRM  Email   Phone  Campaign  AI    Analytics ...
        │                      │
        ▼                      ▼
    PostgreSQL ←→ OpenSearch ←→ Redis ←→ S3
```

- Brief explanation of **why** you chose: microservices, event-driven, AI agent, etc.

***

### 02-system-diagrams.md — Visual Flows

Capture all the diagrams you already outlined:

- **High-Level System Architecture**
- **End-to-End User Flow** (UI → Gateway → Services → DB → AI)
- **AI Agent Flow** (MCP → Agent → Tools → DB/Search → Response)
- **File Storage Flow** (CSV Upload → S3 → Jobs → DB → UI)
- **Email Enrichment Flow** (pattern + validation)
- **Campaign Execution Flow** (multi-channel)
- **VQL Connector Flow** (VQL → Postgres + OpenSearch → merge)
- **Chrome Extension Flow** (LinkedIn/Gmail → extension → API → CRM → OpenSearch)

Each section: ASCII diagram + 1–2 paragraphs of explanation.

***

### 03-database-schema.md — Data Model

- Full PostgreSQL design for:
    - `organizations`, `users`
    - `companies`, `contacts`, `deals`, `contact_activities`
    - `campaigns`, `campaign_targets`, `campaign_messages`, `campaign_events`, `campaign_stats`
    - `email_patterns`, `email_validations`, `email_logs`, `email_engagements`
    - `phone_validations`, `phone_search_logs`
    - `files`, `file_columns`, `file_analysis`
    - `jobs`, `job_logs`
    - `bql_queries`, `bql_exports`
    - `ai_queries`, `ai_actions`, `ai_memories`
    - `integrations`, `provider_accounts`
    - `extension_events`
    - `audit_logs`
    - `contact_embeddings` (pgvector)
- Explain:
    - Multi-tenancy via `org_id` on every table.
    - RLS (Row-Level Security) patterns and `SET app.current_org_id`.
    - Triggers (e.g., auto-updated `updated_at`, `campaigns.stats` updates on events).
    - pgvector index (HNSW) for semantic memory.
- Reference the companion `schema.prisma` file.

***

### schema.prisma — ORM Schema

- Prisma schema mapping all tables and enums.
- DB extensions (uuid-ossp, pgcrypto, vector).
- Ready for use in NestJS services: `shared-db`.

***

### 04-api-reference.md — HTTP API

For each service behind the Gateway:

- Auth:
    - `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/me`
    - `POST /orgs`, `GET /orgs/current`, etc.
- CRM:
    - `GET /contacts`, `GET /contacts/:id`, `POST /contacts`, `PATCH /contacts/:id`, `DELETE /contacts/:id`
    - `GET /companies`, `POST /companies`, `GET /deals`, etc.
- Email/Phone:
    - `POST /email/validate`, `POST /email/find`
    - `POST /phone/validate`, `POST /phone/enrich`
- Campaign:
    - `POST /campaigns`, `GET /campaigns`, `POST /campaigns/:id/send`, `GET /campaigns/:id/analytics`
- File:
    - `POST /files` (upload metadata + pre-signed URL)
    - `GET /files`, `GET /files/:id`
- AI:
    - `POST /ai/query` (chat)
    - `POST /ai/action/:id/approve`, `POST /ai/action/:id/reject`

For each endpoint: method, URL, request body schema, response schema, and sample JSON.

***

### 05-event-driven.md — Kafka \& Events

Define:

- Topics:
    - `contact360.contacts.created/updated/deleted`
    - `contact360.campaigns.scheduled/sending/sent`
    - `contact360.campaign-events.*` (delivered/opened/clicked/replied/bounced/spam)
    - `contact360.emails.enriched/validated`
    - `contact360.ai.action-approved/completed`
    - `contact360.billing.*`
- Event payload schemas.
- Producer/consumer services per topic.
- DLQ strategy and replay.
- Redis Pub/Sub channels for realtime updates.

***

### 06-ai-architecture.md — AI System Overview

- AI stack: LangGraph + OpenAI (GPT‑4o, embeddings), pgvector, OpenSearch.
- RAG pipeline:
    - Semantic search via pgvector (contacts, activities, AI memories).
    - Keyword search via OpenSearch (full-text).
    - RRF merge + re-ranking.
- Tools exposed to the AI agent:
    - `vql.query`, `crm.search_contacts`, `campaign.get_analytics`, `crm.rank_leads`
    - `email.validate`, `campaign.create`, `campaign.send`, `crm.update_contact`, `crm.add_to_list`, `campaign.schedule_followup`
- Human-in-the-loop approval model.
- Model selection (primary vs cost-saving).

***

### 07-ai-agent-reasoning.md — Internal Reasoning Flow

Document how the agent “thinks”:

- Pipeline:
    - User Prompt → Context Builder → Intent Engine → Planner → Tool Selector → Execution Engine → Memory Update → Response Generation.
- Modes:
    - READ (no approval),
    - ACTION (approval gates),
    - AUTOMATION (recurring workflows).
- Detailed example:
    - “Find top 50 CTOs in Bangalore and send them an email campaign”
    - Show detected intents, plan, tools, approvals, and final summary.
- Implementation notes:
    - State shape,
    - LangGraph graph structure,
    - Redis checkpointer for session state.

***

### 08-extension.md — Chrome Extension

- MV3 manifest.
- Content scripts:
    - LinkedIn: scrape name, headline, company, location, LinkedIn URL.
    - Gmail: detect sender, display CRM badge.
- Background service worker:
    - Auth with Contact360 (OAuth / refresh token).
    - Calls to API Gateway → CRM to upsert contacts.
    - Local caching + rate limiting.
- Data path: browser → extension → API → CRM → events → enrichment/search.

***

### 09-testing-qa.md — Testing \& QA Plan

- Unit tests (Jest):
    - Services, domain logic, validators, AI utility functions.
- Integration tests:
    - Service-to-service flows via supertest and testcontainers (Postgres, Redis).
- E2E (Cypress):
    - Flows: login → import contacts → enrich → create campaign → send → view analytics → AI suggestions.
- Load tests (k6):
    - Campaign sending, enrichment endpoints.
- QA checklist:
    - Data accuracy, email validation correctness, campaign delivery, AI response safety.

***

### 10-deployment.md — Deployment \& Environments

- Environment matrix:
    - `local`, `dev`, `staging`, `prod`.
- Infrastructure:
    - AWS: VPC, RDS (Postgres+pgvector), MSK (Kafka), OpenSearch, ElastiCache (Redis), S3, ECS/EKS, ALB, CloudFront.
- Deployment flows:
    - CI/CD pipeline steps per service.
    - Blue/Green or canary deployments.
    - Secrets management.
- Scaling:
    - Horizontal scaling on services based on queue depth / CPU / latency.

***

### 11-onboarding.md — Developer Onboarding

- Prerequisites: Node, pnpm, Docker, Tilt/devcontainers (optional).
- Bootstrap:
    - `pnpm install`
    - `docker-compose up` (Postgres, Redis, local OpenSearch)
    - `pnpm dev` from root.
- How to run:
    - Web app only,
    - Specific service,
    - Full stack.
- How to run tests and apply migrations.

***

### 12-vql-language.md — Query Language

- Purpose: VQL = internal query language for CRM filtering/search, used by AI and UIs.
- Syntax:
    - `FROM contacts WHERE title = 'CTO' AND city = 'Bangalore' LIMIT 50`
    - Filters, projections, order, pagination.
- Mapping to Postgres/OpenSearch.
- Examples and best practices.

***

### 13-runbook.md — Operations \& Incidents

- Playbooks for:
    - High bounce rates,
    - SES suspension,
    - Kafka DLQ spikes,
    - Redis overload,
    - AI budget exhausted.
- How to debug:
    - Log aggregation,
    - Tracing,
    - Metrics dashboards.

***

## 3. End-to-End Flow: How Everything Works Together

Putting it all together:

1. **User logs in** on Web UI → Auth Service issues JWT → Web uses API Gateway for all calls.
2. **Contacts are created** via Web UI, CSV imports, or Chrome extension → CRM Service writes to Postgres → emits Kafka events → enrichment, search, analytics, and AI memory react.
3. **Campaigns are built** in Web UI → Campaign Service defines audience and messages → scheduler + Redis queue manage sending → Email/Phone providers deliver messages → events update Postgres and OpenSearch.
4. **AI Agent** sits on top:
    - Reads from CRM, campaigns, analytics, embeddings, and search.
    - Plans workflows (search, validate, create/send campaigns).
    - Calls tools (microservices) safely with approval gates.
    - Updates memory and provides natural language insight to user.
5. **Developers** work across multiple codebases (UIs, services, shared packages) but share a single source of truth for data (`schema.prisma`, `database-schema.md`) and behavior (`ai-architecture.md`, `event-driven.md`, `ai-agent-reasoning.md`).

***

If you want, next I can:

- Generate a **root `README.md`** that ties all these docs together and explains “how to run Contact360 locally”.
- Or produce the **exact folder + file scaffolding** (bash script/tree) you can paste into your repo to create all these docs and directories.
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: Pasted-text.txt

[^2]: deep-research-report-1.md

