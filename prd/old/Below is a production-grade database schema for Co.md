<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Below is a production-grade database schema for Contact360 (AI CRM).

This is designed for PostgreSQL + OpenSearch + Redis + S3 metadata and supports:
Multi-tenancy
CRM (contacts, companies, deals)
Email + Phone enrichment
Campaigns (multi-channel)
Jobs (CSV import/export)
AI + MCP
Extension data ingestion
🧠 1. CORE TENANCY \& USERS
-- Organizations (Multi-tenant)
CREATE TABLE organizations (
id UUID PRIMARY KEY,
name TEXT,
plan TEXT,
created_at TIMESTAMP,
updated_at TIMESTAMP
);

-- Users
CREATE TABLE users (
id UUID PRIMARY KEY,
org_id UUID REFERENCES organizations(id),
name TEXT,
email TEXT UNIQUE,
password_hash TEXT,
role TEXT, -- admin, user, manager
status TEXT,
created_at TIMESTAMP,
updated_at TIMESTAMP
);

👥 2. CRM CORE (CONTACTS \& COMPANIES)
CREATE TABLE companies (
id UUID PRIMARY KEY,
org_id UUID,
name TEXT,
domain TEXT,
industry TEXT,
size INT,
linkedin_url TEXT,
created_at TIMESTAMP,
updated_at TIMESTAMP
);

CREATE TABLE contacts (
id UUID PRIMARY KEY,
org_id UUID,
company_id UUID REFERENCES companies(id),
first_name TEXT,
last_name TEXT,
full_name TEXT,
email TEXT,
phone TEXT,
job_title TEXT,
linkedin_url TEXT,
address TEXT,
city TEXT,
country TEXT,
source TEXT, -- extension, import, manual
created_at TIMESTAMP,
updated_at TIMESTAMP
);

📊 3. DEALS / PIPELINE
CREATE TABLE deals (
id UUID PRIMARY KEY,
org_id UUID,
contact_id UUID REFERENCES contacts(id),
company_id UUID REFERENCES companies(id),
title TEXT,
value NUMERIC,
stage TEXT,
status TEXT,
close_date DATE,
created_at TIMESTAMP,
updated_at TIMESTAMP
);

📧 4. EMAIL SYSTEM
-- Email Patterns
CREATE TABLE email_patterns (
id UUID PRIMARY KEY,
org_id UUID,
pattern TEXT, -- e.g. [first.last@domain.com](mailto:first.last@domain.com)
priority INT,
created_at TIMESTAMP
);

-- Email Validations
CREATE TABLE email_validations (
id UUID PRIMARY KEY,
org_id UUID,
email TEXT,
is_valid BOOLEAN,
provider TEXT,
score FLOAT,
checked_at TIMESTAMP
);

-- Email Logs
CREATE TABLE email_logs (
id UUID PRIMARY KEY,
org_id UUID,
contact_id UUID,
email TEXT,
campaign_id UUID,
status TEXT, -- sent, failed
provider TEXT,
sent_at TIMESTAMP
);

-- Email Engagement
CREATE TABLE email_engagements (
id UUID PRIMARY KEY,
email_log_id UUID,
opened BOOLEAN,
clicked BOOLEAN,
replied BOOLEAN,
opened_at TIMESTAMP,
clicked_at TIMESTAMP
);

📱 5. PHONE SYSTEM
CREATE TABLE phone_validations (
id UUID PRIMARY KEY,
org_id UUID,
phone TEXT,
country_code TEXT,
is_valid BOOLEAN,
carrier TEXT,
checked_at TIMESTAMP
);

CREATE TABLE phone_search_logs (
id UUID PRIMARY KEY,
org_id UUID,
contact_id UUID,
query TEXT,
result TEXT,
created_at TIMESTAMP
);

📣 6. CAMPAIGN SYSTEM
CREATE TABLE campaigns (
id UUID PRIMARY KEY,
org_id UUID,
name TEXT,
type TEXT, -- email, sms, whatsapp
status TEXT,
scheduled_at TIMESTAMP,
created_at TIMESTAMP
);

CREATE TABLE campaign_targets (
id UUID PRIMARY KEY,
campaign_id UUID,
contact_id UUID
);

CREATE TABLE campaign_messages (
id UUID PRIMARY KEY,
campaign_id UUID,
channel TEXT,
template_id UUID,
content TEXT
);

CREATE TABLE campaign_stats (
id UUID PRIMARY KEY,
campaign_id UUID,
sent INT,
delivered INT,
opened INT,
clicked INT,
replied INT
);

🧾 7. TEMPLATES
CREATE TABLE email_templates (
id UUID PRIMARY KEY,
org_id UUID,
name TEXT,
subject TEXT,
body TEXT,
created_at TIMESTAMP
);

CREATE TABLE campaign_templates (
id UUID PRIMARY KEY,
org_id UUID,
name TEXT,
structure JSONB, -- sequence of messages
created_at TIMESTAMP
);

📂 8. FILE STORAGE (S3 METADATA)
CREATE TABLE files (
id UUID PRIMARY KEY,
org_id UUID,
user_id UUID,
file_name TEXT,
file_type TEXT,
s3_url TEXT,
row_count INT,
column_count INT,
status TEXT,
created_at TIMESTAMP
);

CREATE TABLE file_columns (
id UUID PRIMARY KEY,
file_id UUID,
column_name TEXT,
data_type TEXT
);

CREATE TABLE file_analysis (
id UUID PRIMARY KEY,
file_id UUID,
summary JSONB
);

⚙️ 9. JOB SYSTEM (IMPORT / EXPORT)
CREATE TABLE jobs (
id UUID PRIMARY KEY,
org_id UUID,
type TEXT, -- import, export, enrich
status TEXT,
progress INT,
file_id UUID,
created_at TIMESTAMP,
completed_at TIMESTAMP
);

CREATE TABLE job_logs (
id UUID PRIMARY KEY,
job_id UUID,
message TEXT,
level TEXT,
created_at TIMESTAMP
);

🔎 10. CONNECTOR (VQL QUERY LOGS)
CREATE TABLE bql_queries (
id UUID PRIMARY KEY,
org_id UUID,
user_id UUID,
query TEXT,
executed_at TIMESTAMP
);

CREATE TABLE bql_exports (
id UUID PRIMARY KEY,
query_id UUID,
file_id UUID,
created_at TIMESTAMP
);

🤖 11. AI + MCP SYSTEM
CREATE TABLE ai_queries (
id UUID PRIMARY KEY,
org_id UUID,
user_id UUID,
query TEXT,
response TEXT,
created_at TIMESTAMP
);

CREATE TABLE ai_actions (
id UUID PRIMARY KEY,
org_id UUID,
action_type TEXT,
payload JSONB,
status TEXT,
created_at TIMESTAMP
);

🔌 12. INTEGRATIONS
CREATE TABLE integrations (
id UUID PRIMARY KEY,
org_id UUID,
type TEXT, -- gmail, whatsapp, etc
config JSONB,
status TEXT,
created_at TIMESTAMP
);

CREATE TABLE provider_accounts (
id UUID PRIMARY KEY,
org_id UUID,
provider TEXT,
api_key TEXT,
config JSONB
);

🧩 13. EXTENSION DATA (SCRAPED)
CREATE TABLE extension_events (
id UUID PRIMARY KEY,
org_id UUID,
user_id UUID,
source TEXT,
raw_data JSONB,
processed BOOLEAN,
created_at TIMESTAMP
);

⚡ 14. REDIS USAGE (NO TABLE, BUT DESIGN)
Used for:
Job queues
Campaign scheduling
Rate limiting
Caching contact queries
🔍 15. OPENSEARCH INDEX DESIGN
contacts_index
{
"id": "uuid",
"name": "text",
"email": "keyword",
"company": "text",
"job_title": "text"
}

companies_index
{
"id": "uuid",
"name": "text",
"domain": "keyword",
"industry": "text"
}

🧠 FINAL DATA MODEL INSIGHT
Your system is:
Relational Core (Postgres) → structured CRM
Search Layer (OpenSearch) → fast querying
Cache/Queue (Redis) → performance
Storage (S3) → files
AI Layer (Vector DB optional) → intelligence
🚀 If you want next level
I can now:
Draw ER Diagram (visual)
Create Prisma schema / ORM models
Design VQL query language syntax
Generate real backend starter code (NestJS/Go)
Just tell me 👍

Two production-ready files generated — **952 lines** of Prisma schema and **673 lines** of schema documentation.

***

## What's Inside

### `schema.prisma` — Drop-in Ready for NestJS

The Prisma schema covers all 15 domains from your design with several production upgrades:

**Enums (fully typed):**
All status fields converted to Prisma enums — `OrgPlan`, `UserRole`, `UserStatus`, `ContactStatus`, `EmailStatus`, `DealStage`, `CampaignType`, `JobType`, `AiActionStatus`, and 6 more. No more raw strings in the DB.

**Key upgrades over your raw SQL:**

- `email_status` + `email_confidence` added directly on `contacts` (denormalised for fast filtering)
- `campaign_events` gets a dedicated model with proper indexes
- `ai_memories` model added (long-term agent memory)
- `contact_activities` model added (CRM activity feed)
- `audit_logs` fully modelled with append-only enforcement
- `provider_accounts.api_key_enc` marked as encrypted field
- All `updatedAt` fields use `@updatedAt` (auto-managed by Prisma)

**pgvector note:** The `contact_embeddings` model in Prisma manages metadata — the actual `vector(1536)` column and HNSW index are in a raw SQL migration file (Prisma doesn't yet natively support the `vector` type).

***

### `database-schema.md` — Full Reference Doc

18 sections covering every layer of your stack:


| Section | Highlights |
| :-- | :-- |
| **Architecture Overview** | ASCII diagram of all 4 data layers |
| **RLS Policies** | SQL + NestJS `$executeRaw` pattern |
| **Redis Key Design** | 9 key patterns with TTLs and purpose |
| **OpenSearch Mappings** | Full JSON mappings for 3 indexes |
| **Sync Strategy** | Postgres → Kafka → OpenSearch flow |
| **Migrations Strategy** | Naming convention + raw SQL file layout |
| **pgvector Query** | RAG retrieval SQL with cosine similarity |
| **Campaign Trigger** | Auto-increment stats JSONB trigger |


***

## What's Next

Your docs folder now has **8 core files**. The two highest-value additions remaining:

```
docs/
├── ✅ architecture.md
├── ✅ testing-qa.md
├── ✅ ai-architecture.md
├── ✅ database-schema.md      ← updated now
├── ✅ event-driven.md
├── ✅ extension.md
├── ✅ prisma-schema.prisma    ← new
│
├── 🔴 api-reference.md        ← all endpoints + request/response schemas
└── 🔴 deployment.md           ← K8s manifests + ECS task definitions
```

Say **"generate api-reference.md"** or **"generate deployment.md"** and I'll build it immediately!

