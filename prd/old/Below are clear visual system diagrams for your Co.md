<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Below are clear visual system diagrams for your Contact360 AI-driven CRM. These are structured so you can directly convert them into tools like draw.io, Lucidchart, or Excalidraw.

🧠 1. High-Level System Architecture
┌──────────────────────────┐
│     Web UI (Next.js)     │
│ Admin + User Dashboard   │
└───────────┬──────────────┘
│
┌───────────▼──────────────┐
│     API Gateway (BFF)    │
│   REST + GraphQL Layer   │
└───────────┬──────────────┘
┌──────────────┬───────────────┼───────────────┬──────────────┐
│              │               │               │              │
┌────▼────┐   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐  ┌─────▼─────┐
│ CRM     │   │ Email     │   │ Phone     │   │ Campaign  │  │ AI Agent  │
│ Service │   │ Service   │   │ Service   │   │ Service   │  │ Service   │
└────┬────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘  └─────┬─────┘
│              │               │               │              │
└──────────────┴──────┬────────┴───────────────┴──────────────┘
│
┌────────▼────────┐
│  Event Bus      │
│ (Kafka/Redis)   │
└────────┬────────┘
│
┌──────────────┬──────┴───────────────┬──────────────┐
│              │                      │              │
┌────▼────┐   ┌─────▼─────┐        ┌──────▼──────┐  ┌─────▼─────┐
│Postgres │   │OpenSearch │        │Redis Cache  │  │   S3      │
│(DB)     │   │(Search)   │        │+ Queue      │  │ Storage   │
└─────────┘   └───────────┘        └─────────────┘  └───────────┘

🔄 2. End-to-End User Flow
User → Web UI
→ API Gateway
→ CRM Service (fetch contacts)
→ Email/Phone Services (enrichment)
→ Campaign Service (create campaign)
→ Scheduler triggers campaign
→ Email/SMS/WhatsApp Providers
→ Engagement Tracking
→ Data stored in DB
→ AI analyzes results
→ Insights shown to user

🤖 3. AI Agent (MCP) Flow
User (Chat UI / MCP)
│
▼
AI MCP Service
│
▼
AI Agent Layer (LLM)
│
┌──────┼───────────────┐
│      │               │
▼      ▼               ▼
CRM   Campaign       Connector (VQL)
Service Service        Service
│      │               │
▼      ▼               ▼
Postgres / OpenSearch / Vector DB
│
▼
AI Response
│
▼
User (Natural Language Output)

📂 4. File Storage + Processing Flow
User Upload CSV
│
▼
Storage Service
│
▼
S3 Bucket (Store File)
│
▼
Background Job (Redis Queue)
│
▼
File Parser
│
┌──────┼──────────────┐
│      │              │
▼      ▼              ▼
Row Count   Column Detect   Data Analysis
│
▼
Metadata DB (Postgres)
│
▼
UI (File Dashboard)

📧 5. Email Enrichment + Validation Flow
Input:
First Name + Last Name + Domain
│
▼
Email Service
│
▼
Pattern Engine
(generates possible emails)
│
▼
Validation Engine
(SMTP / API)
│
▼
Valid Email Output
│
▼
Stored in DB + Returned to User

📣 6. Campaign Execution Flow (Multi-channel)
User Creates Campaign
│
▼
Campaign Service
│
▼
Scheduler (Cron / Queue)
│
▼
Channel Router
┌────────────┬────────────┬────────────┬────────────┐
│            │            │            │            │
▼            ▼            ▼            ▼
Email      WhatsApp     SMS        Telegram
Service     API         API         API
│            │            │            │
▼            ▼            ▼            ▼
Delivery    Delivery    Delivery    Delivery
│
▼
Tracking Service
(Open / Click / Reply)
│
▼
Analytics + AI Insights

🔎 7. Connector (VQL) Query Flow
User Query (VQL)
│
▼
Connector Service
│
┌──────┼──────────────┐
│      │              │
▼      ▼              ▼
Postgres Query   OpenSearch Query   Merge Results
│
▼
Unified Response
│
▼
Export / UI Display

🧩 8. Chrome Extension Flow
User opens Sales Navigator
│
▼
Chrome Extension Triggered
│
▼
Content Script Scrapes Data
│
▼
Background Script
│
▼
Send Data → API Gateway
│
▼
CRM Service → Store in DB
│
▼
OpenSearch Index Updated
│
▼
UI Overlay Shows Data

🧠 Final Mental Model
┌───────────────┐
│   User        │
└──────┬────────┘
▼
┌────────────────────┐
│   AI + UI Layer    │
└────────┬───────────┘
▼
┌────────────────────────┐
│   Microservices Layer  │
└────────┬───────────────┘
▼
┌────────────────────────────┐
│ Data + Search + Storage    │
└────────────────────────────┘

🚀 If you want next step
I can convert these into:
🎨 Draw.io / Excalidraw diagrams (ready file)
🧱 Kubernetes deployment diagram
🧠 AI agent internal reasoning flow
📊 Database ER diagram
Just tell me what you want next.

These diagrams are a solid visual blueprint for Contact360! Here's a structured breakdown of each diagram and what they represent architecturally, plus recommendations for your next steps.

***

## Diagram Analysis

### 🧠 1. High-Level System Architecture

This is your **north-star diagram** — it correctly shows the 3-tier separation: UI → Services → Data. One addition worth making: place **Auth Service** and **Notification Service** as siblings to the existing 5 services under the API Gateway, since both are cross-cutting concerns that every service depends on.

### 🔄 2. End-to-End User Flow

This is a clean **happy-path narrative** — great for onboarding new devs. Consider adding a **branch at the Campaign step** showing the async path (Kafka event → Worker → Provider) vs. the sync path (UI polling for status), since those are fundamentally different in your architecture.

### 🤖 3. AI Agent (MCP) Flow

Strong. The **LLM → Tool → DB** pattern is exactly right. The `VQL Connector Service` branch is a smart addition — it means the AI can query data without direct DB access. You should rename it to **"Connector Service (VQL/RAG)"** to reflect that it also handles vector retrieval, not just structured queries.

### 📂 4. File Storage Flow

Accurate. One improvement: add a **Validation Step** between `File Parser` and `Metadata DB` — this is where you reject malformed rows, enforce column type checks, and emit a `import.validated` Kafka event before writing to Postgres.

### 📧 5. Email Enrichment Flow

This maps perfectly to what's in `ai-architecture.md`. A useful addition: show the **confidence scoring step** between `Validation Engine` and `Valid Email Output`, since your system stores a confidence score (0–100) alongside every email result.

### 📣 6. Campaign Execution Flow

Well structured. Add a **DLQ (Dead Letter Queue)** branch off each Channel API — if WhatsApp or SMS delivery fails after retries, it should land in the DLQ for alerting and manual replay, as documented in `event-driven.md`.

### 🔎 7. VQL Query Flow

Correct. The `Merge Results` node is the key insight here — this is where **Reciprocal Rank Fusion (RRF)** happens (combining Postgres + OpenSearch scores), as defined in the RAG pipeline. Worth labelling it `RRF Merge` for technical accuracy.

### 🧩 8. Chrome Extension Flow

Clean and accurate. One missing step: between **Background Script** and **Send Data → API Gateway**, add a **Rate Limiter / Cache Check** node — the extension should check its local cache (5-min TTL) before making an API call, especially on LinkedIn where you might visit the same profile repeatedly.

***

## Recommended Priority for Next Docs

Here's what would complete your Contact360 documentation suite:


| Priority | Document | Why It Matters |
| :-- | :-- | :-- |
| 🔴 High | `api-reference.md` | Every endpoint, request/response schema, error codes — needed before any external integration |
| 🔴 High | `deployment.md` | Kubernetes manifests, ECS task definitions, environment variable table — needed for DevOps handoff |
| 🟡 Medium | `onboarding.md` | Local dev setup, `docker-compose` bootstrap, seed scripts — needed for new team members |
| 🟡 Medium | `vql-query-language.md` | VQL syntax spec, query examples, error handling — needed before AI agent uses it |
| 🟢 Low | `runbook.md` | Incident playbooks: high bounce rate, DLQ spike, SES suspension, DB failover |
| 🟢 Low | `changelog.md` | Versioned release notes starting from v0.1 (MVP) |


***

## Files You Now Have ✅

Based on everything generated so far, your Contact360 docs folder should look like:

```
docs/
├── architecture.md          ✅ Generated
├── testing-qa.md            ✅ Generated
├── ai-architecture.md       ✅ Generated
├── database-schema.md       ✅ Generated
├── event-driven.md          ✅ Generated
├── extension.md             ✅ Generated
├── system-diagrams.md       ✅ This document (your diagrams)
│
├── api-reference.md         ← 🔴 Recommended next
├── deployment.md            ← 🔴 Recommended next
├── onboarding.md            ← 🟡 After that
├── vql-query-language.md    ← 🟡 After that
└── runbook.md               ← 🟢 When going to prod
```

Just say **"generate `api-reference.md`"** or **"generate `deployment.md`"** and I'll produce the full file for you right away!

