# Contact360 — Database Schema Reference

> **Engine:** PostgreSQL 16 · pgvector 0.7 · Row-Level Security (RLS)
> **Companion file:** `schema.prisma` — Prisma ORM models
> Version 1.0 · April 2026

---

## Table of Contents

1. [Data Architecture Overview](#1-data-architecture-overview)
2. [Core Tenancy & Users](#2-core-tenancy--users)
3. [CRM Core — Contacts & Companies](#3-crm-core--contacts--companies)
4. [Deals / Pipeline](#4-deals--pipeline)
5. [Email System](#5-email-system)
6. [Phone System](#6-phone-system)
7. [Campaign System](#7-campaign-system)
8. [Templates](#8-templates)
9. [File Storage (S3 Metadata)](#9-file-storage-s3-metadata)
10. [Job System](#10-job-system)
11. [VQL Connector (Query Logs)](#11-vql-connector-query-logs)
12. [AI + MCP System](#12-ai--mcp-system)
13. [Integrations](#13-integrations)
14. [Chrome Extension Data](#14-chrome-extension-data)
15. [Redis Design (No Tables)](#15-redis-design-no-tables)
16. [OpenSearch Index Design](#16-opensearch-index-design)
17. [Row-Level Security (RLS)](#17-row-level-security-rls)
18. [Migrations Strategy](#18-migrations-strategy)

---

## 1. Data Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                      CONTACT360 DATA LAYER                         │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                PostgreSQL 16 (Relational Core)               │  │
│  │  organizations · users · contacts · companies · deals        │  │
│  │  campaigns · campaign_events · email_logs · jobs · files     │  │
│  │  ai_queries · ai_actions · audit_logs (append-only)          │  │
│  │                                                              │  │
│  │  + pgvector extension → contact_embeddings (HNSW index)      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌───────────────────────┐   ┌─────────────────────────────────┐  │
│  │  OpenSearch (Search)  │   │  Redis (Cache + Queue)          │  │
│  │  contacts_index       │   │  Job queues (BullMQ)            │  │
│  │  companies_index      │   │  Rate limiting                  │  │
│  │  campaigns_index      │   │  Session cache                  │  │
│  └───────────────────────┘   │  AI approval WebSocket state    │  │
│                               └─────────────────────────────────┘  │
│  ┌───────────────────────┐                                         │
│  │  S3 (Object Storage)  │                                         │
│  │  CSV uploads          │                                         │
│  │  Export files         │                                         │
│  │  Email attachments    │                                         │
│  └───────────────────────┘                                         │
└────────────────────────────────────────────────────────────────────┘
```

### Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Multi-tenancy** | Every table has `org_id` + RLS policy |
| **Soft deletes** | `deleted_at` on contacts (not hard delete) |
| **Append-only audit** | `audit_logs` has `NO UPDATE / NO DELETE` rules |
| **Encrypted PII** | `api_key_enc`, `mfa_secret` AES-256 encrypted at app layer |
| **Idempotency** | `UNIQUE` constraints on `(org_id, email)` throughout |
| **Partitioned events** | `campaign_events` partitioned by `occurred_at` (monthly) |
| **Vector search** | `contact_embeddings` uses HNSW index (pgvector) |

---

## 2. Core Tenancy & Users

### organizations

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | `gen_random_uuid()` |
| `name` | TEXT NOT NULL | Display name |
| `slug` | TEXT UNIQUE | URL-safe identifier |
| `plan` | ENUM | `TRIAL \| STARTER \| PRO \| ENTERPRISE` |
| `credits` | INT | Enrichment credits remaining |
| `settings` | JSONB | Feature flags, preferences |
| `stripe_customer_id` | TEXT | Nullable |
| `trial_ends_at` | TIMESTAMPTZ | Nullable |
| `created_at` | TIMESTAMPTZ | Auto |
| `updated_at` | TIMESTAMPTZ | Auto (trigger) |

---

### users

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `org_id` | UUID FK → organizations | Cascade delete |
| `email` | TEXT | UNIQUE per org |
| `name` | TEXT | |
| `password_hash` | TEXT | NULL if OAuth only |
| `role` | ENUM | `ADMIN \| MANAGER \| USER \| VIEWER` |
| `status` | ENUM | `ACTIVE \| INACTIVE \| SUSPENDED \| INVITED` |
| `mfa_enabled` | BOOLEAN | Default false |
| `mfa_secret` | TEXT | AES-256 encrypted |
| `google_id` | TEXT | OAuth |
| `last_login_at` | TIMESTAMPTZ | |

**Indexes:** `(org_id)`, `(email)`, `UNIQUE(org_id, email)`

---

### api_keys

| Column | Type | Notes |
|--------|------|-------|
| `key_hash` | TEXT | bcrypt hash of raw key |
| `key_preview` | TEXT | First 16 chars + `...` |
| `environment` | TEXT | `live` or `test` |
| `scopes` | TEXT[] | e.g. `["contacts:read","campaigns:write"]` |
| `ip_allowlist` | INET[] | Optional IP whitelist |
| `revoked_at` | TIMESTAMPTZ | Soft revoke |

---

## 3. CRM Core — Contacts & Companies

### companies

| Column | Type | Notes |
|--------|------|-------|
| `domain` | TEXT | UNIQUE per org (nullable) |
| `size_range` | TEXT | `1-10 \| 11-50 \| 51-200 \| 201-1000 \| 1000+` |
| `tags` | TEXT[] | GIN indexed |
| `custom_fields` | JSONB | GIN indexed |

---

### contacts *(most important table)*

| Column | Type | Notes |
|--------|------|-------|
| `email_status` | ENUM | `VALID \| RISKY \| INVALID \| UNKNOWN \| UNVALIDATED` |
| `email_confidence` | INT | 0–100 |
| `phone_dnd` | BOOLEAN | TRAI DND registry flag |
| `status` | ENUM | `LEAD \| PROSPECT \| CUSTOMER \| CHURNED \| UNSUBSCRIBED` |
| `source` | ENUM | `EXTENSION \| IMPORT \| MANUAL \| API \| ENRICHMENT` |
| `lead_score` | INT | 0–100, recalculated on engagement events |
| `tags` | TEXT[] | GIN indexed |
| `custom_fields` | JSONB | GIN indexed |
| `enriched_at` | TIMESTAMPTZ | Last enrichment run |
| `enrichment_score` | INT | 0–100 profile completeness |
| `gdpr_consent` | BOOLEAN | |
| `ccpa_opt_out` | BOOLEAN | |
| `deleted_at` | TIMESTAMPTZ | Soft delete |

**Indexes (7 total):**
```sql
idx_contacts_org          (org_id)
idx_contacts_email        (org_id, email) WHERE email IS NOT NULL
idx_contacts_company      (company_id)    WHERE company_id IS NOT NULL
idx_contacts_tags         GIN(tags)
idx_contacts_custom       GIN(custom_fields)
idx_contacts_lead_score   (org_id, lead_score DESC)
idx_contacts_not_deleted  (org_id) WHERE deleted_at IS NULL
```

---

### contact_embeddings *(pgvector)*

```sql
-- Managed via raw SQL (Prisma doesn't support vector type natively)
CREATE TABLE contact_embeddings (
  id          UUID PRIMARY KEY,
  org_id      UUID NOT NULL,
  contact_id  UUID NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  type        TEXT NOT NULL,  -- 'profile' | 'activity_summary' | 'notes'
  content     TEXT NOT NULL,
  embedding   vector(1536),   -- OpenAI text-embedding-3-small
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index: fast approximate nearest-neighbour search
CREATE INDEX idx_embeddings_hnsw ON contact_embeddings
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

**Query example (RAG retrieval):**
```sql
SELECT id, contact_id, content,
       1 - (embedding <=> $1::vector) AS similarity
FROM contact_embeddings
WHERE org_id = $2
  AND 1 - (embedding <=> $1::vector) > 0.70
ORDER BY similarity DESC
LIMIT 10;
```

---

## 4. Deals / Pipeline

### deals

| Column | Type | Notes |
|--------|------|-------|
| `value` | DECIMAL(14,2) | |
| `currency` | CHAR(3) | Default `INR` |
| `stage` | ENUM | `LEAD → QUALIFIED → PROPOSAL → NEGOTIATION → WON/LOST` |
| `probability` | INT | 0–100 |
| `close_date` | DATE | Expected |
| `closed_at` | TIMESTAMPTZ | Actual close |

---

## 5. Email System

### email_patterns

Stores discovered email format patterns per domain to improve future enrichment accuracy.

| Column | Notes |
|--------|-------|
| `pattern` | e.g. `{first}.{last}@{domain}` |
| `priority` | Higher = tried first |
| `hit_count` | Incremented on successful match |

---

### email_validations

Caches validation results with 30-day TTL (enforced at app layer). Avoids re-validating the same email.

| Column | Notes |
|--------|-------|
| `status` | `VALID \| RISKY \| INVALID \| UNKNOWN` |
| `is_catch_all` | Catch-all domains: treat as RISKY |
| `is_disposable` | Mailinator, 10minutemail, etc. |
| `mx_found` | DNS MX record exists |
| `smtp_verified` | SMTP RCPT TO check passed |
| `score` | 0.0–1.0 composite confidence |

---

### email_logs + email_engagements

`email_logs` records every outbound send event. `email_engagements` tracks open/click/reply per email. One-to-one relationship via `email_log_id`.

---

## 6. Phone System

### phone_validations

| Column | Notes |
|--------|-------|
| `country_code` | E.164 prefix e.g. `+91` |
| `is_dnd` | TRAI Do-Not-Disturb registry |
| `carrier` | e.g. `Jio`, `Airtel` |
| `line_type` | `mobile \| landline \| voip` |

---

## 7. Campaign System

### campaigns

Denormalised `stats` JSONB column is updated by a PostgreSQL trigger on every new `campaign_event` insert — avoids expensive COUNT queries at dashboard load time.

```sql
-- Trigger: auto-increment campaign stats
CREATE OR REPLACE FUNCTION update_campaign_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE campaigns
  SET stats = jsonb_set(
    stats, ARRAY[NEW.event],
    to_jsonb((stats->>NEW.event)::int + 1)
  )
  WHERE id = NEW.campaign_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER campaign_event_stats
  AFTER INSERT ON campaign_events
  FOR EACH ROW EXECUTE FUNCTION update_campaign_stats();
```

---

### campaign_events *(partitioned)*

Partitioned monthly to keep query performance fast as event volume grows:

```sql
CREATE TABLE campaign_events (
  ...
) PARTITION BY RANGE (occurred_at);

-- Auto-create partitions monthly (pg_partman recommended)
CREATE TABLE campaign_events_2026_04 PARTITION OF campaign_events
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
```

---

## 8. Templates

### email_templates

Stores reusable email templates with variable substitution support:
- Variables stored as JSON array: `[{"name":"first_name","required":true}]`
- Body supports Handlebars syntax: `Hello {{first_name}}, ...`

### campaign_templates

Stores multi-step campaign sequences as JSONB:
```json
{
  "steps": [
    { "day": 0, "channel": "email", "templateId": "..." },
    { "day": 3, "channel": "email", "templateId": "..." },
    { "day": 7, "channel": "linkedin", "message": "..." }
  ]
}
```

---

## 9. File Storage (S3 Metadata)

PostgreSQL stores **metadata only** — actual files live in S3.

### files

| Column | Notes |
|--------|-------|
| `s3_key` | S3 object key (not full URL) |
| `s3_bucket` | Bucket name |
| `size_bytes` | BigInt (supports files > 2GB) |
| `row_count` | Populated after parse |
| `status` | `uploaded → parsing → ready → error` |

### file_columns

Stores schema discovered during CSV parse:
- `data_type`: `string`, `email`, `phone`, `number`, `date`
- `mapped_to`: CRM field it maps to (e.g. `contact.email`)
- `sample_data`: JSON array of 5 sample values for column preview

---

## 10. Job System

### jobs

| Column | Notes |
|--------|-------|
| `type` | `IMPORT \| EXPORT \| ENRICH_EMAIL \| ENRICH_PHONE \| VALIDATE_EMAIL` |
| `status` | `PENDING → RUNNING → COMPLETED / FAILED` |
| `progress` | 0–100 (percentage) |
| `metadata` | Input params, filters, etc. |

### job_logs

Structured log stream per job — queryable by level:
```sql
SELECT * FROM job_logs
WHERE job_id = $1 AND level = 'ERROR'
ORDER BY created_at DESC;
```

---

## 11. VQL Connector (Query Logs)

### bql_queries

Every query through the VQL connector is logged for:
- Debugging & replay
- Usage analytics
- AI context (what data was the user looking at?)
- Audit trail

| Column | Notes |
|--------|-------|
| `parsed_ast` | JSONB — parsed VQL AST for replay |
| `result_count` | How many rows returned |
| `duration_ms` | Query execution time |

---

## 12. AI + MCP System

### ai_queries

Full audit trail of every AI interaction including cost tracking:

| Column | Notes |
|--------|-------|
| `session_id` | Groups messages in one conversation |
| `intent` | Classified intent: `search_contacts`, `send_campaign`, etc. |
| `tools_called` | JSON array of tools invoked |
| `prompt_tokens` | OpenAI input tokens |
| `comp_tokens` | OpenAI output tokens |
| `cost_usd` | Calculated cost per query |

### ai_actions

Write actions proposed by the AI go through human approval:

```
AI proposes action → status: PENDING_APPROVAL
User approves      → status: APPROVED → EXECUTING → COMPLETED
User rejects       → status: REJECTED
Timeout (30s)      → status: REJECTED (auto)
```

| Column | Notes |
|--------|-------|
| `action_type` | `send_campaign \| update_contact \| add_to_list` |
| `payload` | Full action arguments as JSONB |
| `preview` | Human-readable action summary |
| `risk_level` | `low \| medium \| high` |

### ai_memories

Long-term memory store for per-org and per-user preferences:

```sql
-- Example entries
INSERT INTO ai_memories (org_id, scope, key, value) VALUES
  ('org_1', 'org',  'preferred_send_day',   'Tuesday'),
  ('org_1', 'org',  'exclude_domains',      '@competitor.com'),
  ('org_1', 'user', 'dashboard_preference', 'compact');
```

---

## 13. Integrations

### integrations

One row per integration type per org. Config stored as encrypted JSONB:

```json
{
  "accessToken": "<encrypted>",
  "refreshToken": "<encrypted>",
  "expiresAt": "2026-06-01T00:00:00Z",
  "scopes": ["mail.read", "mail.send"]
}
```

### provider_accounts

Multiple provider accounts per org (e.g., two SES accounts, primary + backup):
- `api_key_enc`: AES-256-GCM encrypted at application layer
- `is_default`: Only one per `(org_id, provider)` can be default

---

## 14. Chrome Extension Data

### extension_events

Raw scraped data from LinkedIn, Gmail, Sales Navigator lands here first:

```json
{
  "source": "linkedin",
  "rawData": {
    "name": "Rahul Sharma",
    "headline": "CTO at Flipkart",
    "company": "Flipkart",
    "linkedinUrl": "https://www.linkedin.com/in/rahul-sharma",
    "location": "Bengaluru, Karnataka"
  },
  "processed": false
}
```

A background worker processes these events:
1. Deduplicates against existing contacts (`linkedin_url` match)
2. Creates or updates the contact
3. Marks `processed = true`
4. Emits `contact.created` or `contact.updated` Kafka event

---

## 15. Redis Design (No Tables)

Redis is used as **cache + queue** — no persistent data of record.

| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `c360:session:{userId}` | Hash | 2h | Active session data |
| `c360:auth:failures:{ip}` | Counter | 15m | Login rate limiting |
| `c360:contact:lookup:{hash}` | JSON | 5m | Extension lookup cache |
| `c360:org:credits:{orgId}` | Counter | 60s | Credits remaining (fast read) |
| `c360:processed:{eventId}` | String | 24h | Kafka idempotency dedup |
| `c360:ai:approval:{approvalId}` | Hash | 30s | Pending AI action approval |
| `c360:ratelimit:{orgId}:{endpoint}` | Counter | 60s | API rate limit per org |
| `bull:enrich:*` | BullMQ | — | Enrichment job queue |
| `bull:campaign:*` | BullMQ | — | Campaign send queue |
| `bull:import:*` | BullMQ | — | CSV import job queue |

---

## 16. OpenSearch Index Design

### contacts_index

```json
{
  "mappings": {
    "properties": {
      "id":         { "type": "keyword" },
      "org_id":     { "type": "keyword" },
      "full_name":  { "type": "text", "analyzer": "standard", "fields": { "keyword": { "type": "keyword" } } },
      "email":      { "type": "keyword" },
      "phone":      { "type": "keyword" },
      "job_title":  { "type": "text" },
      "company":    { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "status":     { "type": "keyword" },
      "tags":       { "type": "keyword" },
      "lead_score": { "type": "integer" },
      "country":    { "type": "keyword" },
      "source":     { "type": "keyword" },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" }
    }
  },
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "email_analyzer": {
          "tokenizer": "uax_url_email",
          "filter": ["lowercase"]
        }
      }
    }
  }
}
```

### companies_index

```json
{
  "mappings": {
    "properties": {
      "id":       { "type": "keyword" },
      "org_id":   { "type": "keyword" },
      "name":     { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
      "domain":   { "type": "keyword" },
      "industry": { "type": "keyword" },
      "country":  { "type": "keyword" },
      "size_range": { "type": "keyword" }
    }
  }
}
```

### campaigns_index

```json
{
  "mappings": {
    "properties": {
      "id":     { "type": "keyword" },
      "org_id": { "type": "keyword" },
      "name":   { "type": "text" },
      "type":   { "type": "keyword" },
      "status": { "type": "keyword" },
      "stats":  { "type": "object", "enabled": false },
      "created_at": { "type": "date" }
    }
  }
}
```

### Sync Strategy: PostgreSQL → OpenSearch

```
INSERT/UPDATE on contacts (Postgres)
         │
         ▼
Kafka event: contact360.contacts.updated
         │
         ▼
search-sync-worker (consumer group)
         │
         ├── Idempotency check (Redis)
         │
         ▼
OpenSearch bulk upsert
(doc_as_upsert: true, retry_on_conflict: 3)
         │
         ▼
DLQ on failure → alert if > 10 failures in 5 min
```

---

## 17. Row-Level Security (RLS)

All core tables have RLS enabled. The current org is set at connection time via `SET app.current_org_id`:

```sql
-- Enable RLS on all core tables
ALTER TABLE contacts    ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts    FORCE ROW LEVEL SECURITY;
ALTER TABLE companies   ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals       ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns   ENABLE ROW LEVEL SECURITY;
ALTER TABLE files       ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs  ENABLE ROW LEVEL SECURITY;

-- Policy template (identical for all tables)
CREATE POLICY {table}_org_isolation ON {table}
  USING (org_id = current_setting('app.current_org_id')::uuid);

-- NestJS: set before every query
await prisma.$executeRaw`SET app.current_org_id = ${orgId}`;
```

---

## 18. Migrations Strategy

| Tool | Purpose |
|------|---------|
| `prisma migrate dev` | Local dev migrations |
| `prisma migrate deploy` | CI/CD production deploy |
| Raw SQL files in `prisma/migrations/` | Triggers, RLS policies, pgvector indexes |
| `prisma/seed.ts` | Dev seed data |

### Migration Naming Convention

```
YYYYMMDDHHMMSS_description_of_change
20260401120000_add_contact_embeddings_table
20260405090000_add_campaign_events_partitioning
20260410140000_add_rls_policies_all_tables
```

### Raw SQL Migrations (Prisma `$executeRaw`)

For features Prisma doesn't support natively, use raw SQL files:

```
prisma/
├── schema.prisma
├── migrations/
│   ├── 20260401_init/
│   │   └── migration.sql          ← auto-generated by Prisma
│   ├── 20260405_rls/
│   │   └── rls_policies.sql       ← manual raw SQL
│   ├── 20260410_pgvector/
│   │   └── embeddings_hnsw.sql    ← manual raw SQL
│   └── 20260415_triggers/
│       └── updated_at_triggers.sql ← manual raw SQL
└── seed.ts
```
