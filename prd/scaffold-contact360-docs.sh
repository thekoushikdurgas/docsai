#!/usr/bin/env bash
# =============================================================================
# Contact360 — Full Docs Directory Scaffold
# =============================================================================
# Usage:
#   chmod +x scaffold-contact360-docs.sh
#   ./scaffold-contact360-docs.sh [target-dir]
#
# Default target: ./contact360-docs
# Generates 666 files across 100 directories covering all 18 sections.
# =============================================================================

set -euo pipefail

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()     { echo -e "${GREEN}✔${RESET}  $*"; }
info()    { echo -e "${CYAN}→${RESET}  $*"; }
warn()    { echo -e "${YELLOW}⚠${RESET}  $*"; }
header()  { echo -e "\n${BOLD}${CYAN}$*${RESET}"; }
divider() { echo -e "${CYAN}────────────────────────────────────────────────${RESET}"; }

# ── Target Directory ──────────────────────────────────────────────────────────
BASE="${1:-./contact360-docs}"

if [[ -d "$BASE" ]]; then
  warn "Directory '$BASE' already exists."
  read -rp "  Overwrite? [y/N] " confirm
  [[ "${confirm,,}" == "y" ]] || { echo "Aborted."; exit 0; }
  rm -rf "$BASE"
fi

echo -e "\n${BOLD}Contact360 Docs Scaffold${RESET}"
divider
info "Target: ${BOLD}$BASE${RESET}"
echo ""

mkd() { mkdir -p "$BASE/$1"; }
tch() { touch "$BASE/$1"; }

# Helper: create multiple files in one directory
files_in() {
  local dir="$1"; shift
  for f in "$@"; do tch "$dir/$f"; done
}

# Helper: create a file with content
write() {
  local path="$BASE/$1"; shift
  mkdir -p "$(dirname "$path")"
  cat > "$path"
}

# =============================================================================
# SECTION 00 — OVERVIEW
# =============================================================================
header "00 — Overview"
mkd "00-overview"

write "README.md" << 'EOF'
# Contact360 Documentation

> AI-powered, multi-tenant CRM platform — complete technical reference.

## Quick Navigation

| Section | Description |
|---------|-------------|
| [00-overview](./00-overview/) | Project vision, glossary, principles |
| [01-architecture](./01-architecture/) | System design, diagrams, ADR list |
| [02-services](./02-services/) | Per-service deep dives (11 services) |
| [03-database](./03-database/) | Schemas, migrations, indexes, RLS |
| [04-api](./04-api/) | REST, GraphQL, WebSocket, Webhooks |
| [05-frontend](./05-frontend/) | Web, Admin, Mobile, Components |
| [06-ai-ml](./06-ai-ml/) | Agents, MCP, Embeddings, Models |
| [07-extension](./07-extension/) | Chrome MV3 extension |
| [08-enrichment](./08-enrichment/) | Email & phone enrichment pipelines |
| [09-campaigns](./09-campaigns/) | Multi-channel campaign system |
| [10-integrations](./10-integrations/) | Third-party integrations |
| [11-infra](./11-infra/) | AWS, Kubernetes, Terraform, CI/CD |
| [12-security](./12-security/) | Auth, RBAC, GDPR, TRAI |
| [13-observability](./13-observability/) | Logs, metrics, tracing, alerts |
| [14-testing](./14-testing/) | Unit, integration, E2E, performance |
| [15-guides](./15-guides/) | Onboarding, dev, deploy, troubleshoot |
| [16-runbooks](./16-runbooks/) | Incident response playbooks |
| [17-adrs](./17-adrs/) | Architecture Decision Records |
| [18-changelog](./18-changelog/) | Version history |

## Stack at a Glance

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, TailwindCSS, React Query |
| Backend | NestJS 10 (Node.js 20), FastAPI (Python 3.12) |
| Database | PostgreSQL 16 + pgvector, Redis 7, OpenSearch 2 |
| AI/ML | LangGraph 0.2, OpenAI GPT-4o, Gemini, Ollama |
| Messaging | Apache Kafka 3.7 |
| Infra | AWS ECS Fargate, RDS, ElastiCache, S3, CloudFront |
| Observability | Datadog, Sentry, Jaeger, OpenTelemetry |
EOF

files_in "00-overview" \
  "vision-and-goals.md" \
  "glossary.md" \
  "design-principles.md" \
  "tech-stack-rationale.md" \
  "roadmap.md" \
  "team-structure.md"

log "00-overview (7 files)"

# =============================================================================
# SECTION 01 — ARCHITECTURE
# =============================================================================
header "01 — Architecture"
mkd "01-architecture"

write "01-architecture/system-overview.md" << 'EOF'
# System Overview

Contact360 is a cloud-native, multi-tenant CRM platform built on microservices.
It combines PostgreSQL (relational core), OpenSearch (full-text search),
pgvector (semantic search), and LangGraph agents (AI orchestration).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                  │
│  Web UI (Next.js)  │  Admin (Next.js)  │  Mobile (RN)  │  Slack Bot │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTPS / WSS
┌───────────────────────────────▼─────────────────────────────────────┐
│                      API GATEWAY (Kong)                              │
│          JWT validation · Rate limiting · Request routing            │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────────────────┘
   │      │      │      │      │      │      │      │
 auth   crm   email  phone  camp  analy  notif  ai-svc
:3001  :3002  :3003  :3004  :3005 :3006  :3007  :8000
   │      │      │      │      │      │      │      │
   └──────┴──────┴──────┴──────┴──────┴──────┴──────┘
                          │
              ┌───────────▼──────────┐
              │    Apache Kafka 3.7   │
              └───────────────────────┘
                          │
        ┌─────────────────┼────────────────┐
        ▼                 ▼                ▼
   PostgreSQL 16      OpenSearch 2      Redis 7
   + pgvector         (search layer)    (cache/queues)
```

## Core Design Decisions

1. **Stateless services** — horizontal scaling, state lives in PostgreSQL/Redis
2. **Event-first writes** — every mutation publishes a Kafka event
3. **Row-Level Security** — all tables enforce `org_id` RLS policies
4. **Hybrid retrieval** — pgvector cosine + tsvector fused via RRF
5. **Human-in-the-loop AI** — LangGraph agents pause for Slack approval
EOF

files_in "01-architecture" \
  "microservices-map.md" \
  "data-flow-diagrams.md" \
  "event-driven-architecture.md" \
  "multi-tenancy-design.md" \
  "scalability-strategy.md" \
  "disaster-recovery.md" \
  "network-topology.md" \
  "dependency-graph.md"

log "01-architecture (9 files)"

# =============================================================================
# SECTION 02 — SERVICES  (11 services × 11 files = 121 files)
# =============================================================================
header "02 — Services"

SERVICE_FILES=(
  "README.md"
  "api-reference.md"
  "data-model.md"
  "environment-variables.md"
  "kafka-events.md"
  "error-codes.md"
  "rate-limits.md"
  "testing.md"
  "deployment.md"
  "dependencies.md"
  "changelog.md"
)

SERVICES=(
  "auth-service"
  "crm-service"
  "ai-service"
  "email-service"
  "phone-service"
  "campaign-service"
  "analytics-service"
  "notification-service"
  "integration-service"
  "billing-service"
  "gateway"
)

for svc in "${SERVICES[@]}"; do
  mkd "02-services/$svc"
  for f in "${SERVICE_FILES[@]}"; do
    tch "02-services/$svc/$f"
  done
done

# ── crm-service README ────────────────────────────────────────────────────────
write "02-services/crm-service/README.md" << 'EOF'
# CRM Service

**Runtime:** Node.js 20 + NestJS 10 | **Port:** 3002  
**DB:** PostgreSQL (primary) + OpenSearch (search)

## Responsibilities

- CRUD: Contacts, Companies, Deals, Activities
- Full-text + semantic search
- Lead scoring orchestration
- BQL query execution
- CSV import/export job dispatch
- OpenSearch index sync via Kafka

## Module Structure

```
crm-service/src/
├── contacts/     controller · service · repository
├── companies/    controller · service
├── deals/        controller · service · pipeline.service
├── activities/   controller · service
├── search/       controller · service (OpenSearch client)
├── bql/          parser · executor · validator
├── import/       controller · csv.parser · field.mapper
├── export/       service · csv.serializer
├── kafka/        producer · consumer
└── common/       dto · guards · pipes · interceptors
```

## Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/contacts | List (paginated + filtered) |
| POST | /v1/contacts | Create + trigger enrichment |
| GET | /v1/contacts/:id | 360-view |
| PATCH | /v1/contacts/:id | Update |
| DELETE | /v1/contacts/:id | Soft-delete |
| POST | /v1/contacts/search | Hybrid search |
| GET | /v1/deals | Pipeline view |
| POST | /v1/deals | Create deal |
| PATCH | /v1/deals/:id/stage | Move stage |
| POST | /v1/bql/query | Execute BQL |
| POST | /v1/import | Upload CSV → job |

## Kafka Events Published

| Topic | Trigger |
|-------|---------|
| `contact.created` | New contact saved |
| `contact.updated` | Field changed |
| `deal.created` | New deal created |
| `deal.stage_changed` | Stage moved |
| `import.completed` | CSV job finished |
EOF

# ── ai-service README ─────────────────────────────────────────────────────────
write "02-services/ai-service/README.md" << 'EOF'
# AI Service

**Runtime:** Python 3.12 + FastAPI | **Port:** 8000  
**Stack:** LangGraph 0.2, OpenAI GPT-4o, pgvector, MCP SDK

## Responsibilities

- LangGraph supervisor agent orchestration
- MCP server (CRM tools + resources)
- Hybrid RAG: pgvector cosine + tsvector (RRF fusion)
- Lead scoring algorithm execution
- Workflow state management (pause/resume on approval)
- Agent memory persistence
- Embedding generation and upsert

## Module Structure

```
ai-service/src/
├── agents/       supervisor.py · tools.py · prompts.py
├── mcp/          crm_mcp_server.py · tools_registry.py
├── embeddings/   embed.py · upsert.py · hybrid_search.py
├── scoring/      lead_scorer.py · firmographic.py
├── memory/       agent_memory.py · importance_decay.py
├── workflows/    workflow_state.py · approval.py
├── db/           postgres.py · pgvector.py · redis_client.py
├── kafka/        consumer.py · producer.py
└── main.py
```

## Kafka Events Consumed

| Topic | Handler |
|-------|---------|
| `contact.created` | Trigger embedding generation |
| `contact.updated` | Re-embed if content changed |
| `deal.created` | Score lead, generate next-action |
| `deal.stage_changed` | Update win probability |
EOF

log "02-services (121 files)"

# =============================================================================
# SECTION 03 — DATABASE
# =============================================================================
header "03 — Database"

mkd "03-database/schemas"
mkd "03-database/migrations"
mkd "03-database/indexes"
mkd "03-database/rls-policies"
mkd "03-database/opensearch"
mkd "03-database/redis"

# Schemas
files_in "03-database/schemas" \
  "00-tenancy-users.md" "01-contacts-companies.md" "02-deals-pipeline.md" \
  "03-email-system.md" "04-phone-system.md" "05-campaigns.md" \
  "06-templates.md" "07-files-storage.md" "08-jobs.md" \
  "09-bql-connector.md" "10-ai-mcp.md" "11-integrations.md" \
  "12-extension-data.md" "13-audit-logs.md" "14-billing.md" \
  "15-notifications.md" "FULL-SCHEMA.sql"

# Migrations — 30 versioned files
MIGRATION_NAMES=(
  "V0001__init_extensions.sql"
  "V0002__organizations_users.sql"
  "V0003__contacts_companies.sql"
  "V0004__deals_pipeline.sql"
  "V0005__email_system.sql"
  "V0006__phone_system.sql"
  "V0007__campaigns.sql"
  "V0008__jobs.sql"
  "V0009__ai_mcp.sql"
  "V0010__pgvector_embeddings.sql"
  "V0011__rls_policies.sql"
  "V0012__indexes.sql"
  "V0013__audit_logs.sql"
  "V0014__billing.sql"
  "V0015__integrations.sql"
  "V0016__extension_events.sql"
  "V0017__campaign_events_partitioned.sql"
  "V0018__campaign_sequences.sql"
  "V0019__contact_campaign_states.sql"
  "V0020__agent_memories.sql"
  "V0021__mcp_invocations.sql"
  "V0022__ai_workflow_states.sql"
  "V0023__bql_queries.sql"
  "V0024__provider_accounts.sql"
  "V0025__file_analysis.sql"
  "V0026__email_patterns.sql"
  "V0027__contact_activities.sql"
  "V0028__notification_preferences.sql"
  "V0029__subscription_plans.sql"
  "V0030__feature_flags.sql"
)
for m in "${MIGRATION_NAMES[@]}"; do tch "03-database/migrations/$m"; done

# Write init migration with real content
write "03-database/migrations/V0001__init_extensions.sql" << 'EOF'
-- V0001: Initialize PostgreSQL extensions
-- Run once on fresh database

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Full-text search improvements
CREATE EXTENSION IF NOT EXISTS "unaccent";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Vector similarity search
CREATE EXTENSION IF NOT EXISTS "vector";

-- Stats and hints
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Set default search path
ALTER DATABASE contact360 SET search_path TO public;

-- Set timezone
ALTER DATABASE contact360 SET timezone TO 'UTC';

-- Performance settings (adjust per instance size)
ALTER DATABASE contact360 SET work_mem = '64MB';
ALTER DATABASE contact360 SET maintenance_work_mem = '256MB';
ALTER DATABASE contact360 SET random_page_cost = 1.1; -- SSD optimized
EOF

# Indexes
files_in "03-database/indexes" \
  "contacts-indexes.sql" "deals-indexes.sql" "campaign-indexes.sql" \
  "embeddings-hnsw.sql" "full-text-indexes.sql" "composite-indexes.sql" \
  "partial-indexes.sql" "index-strategy.md"

write "03-database/indexes/embeddings-hnsw.sql" << 'EOF'
-- HNSW index for pgvector cosine similarity search
-- Parameters tuned for 1-10M vectors on db.r6g.xlarge

-- Contact embeddings (primary RAG index)
CREATE INDEX CONCURRENTLY idx_contact_embeddings_hnsw
ON contact_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Agent memory embeddings
CREATE INDEX CONCURRENTLY idx_agent_memories_hnsw
ON agent_memories
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Tune ef_search at query time for recall vs speed trade-off:
-- SET hnsw.ef_search = 100;   -- higher recall, slower
-- SET hnsw.ef_search = 40;    -- default, good balance
EOF

# RLS Policies
files_in "03-database/rls-policies" \
  "contacts-rls.sql" "companies-rls.sql" "deals-rls.sql" \
  "campaigns-rls.sql" "ai-tables-rls.sql" "rls-testing-guide.md"

write "03-database/rls-policies/contacts-rls.sql" << 'EOF'
-- Row-Level Security for contacts table
-- Enforces org_id isolation at the database layer

ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts FORCE ROW LEVEL SECURITY;

-- Policy: users can only see contacts in their org
CREATE POLICY contacts_org_isolation ON contacts
  USING (org_id = current_setting('app.current_org_id')::uuid);

-- Policy: service role bypasses RLS (for background workers)
CREATE POLICY contacts_service_bypass ON contacts
  USING (current_setting('app.role', true) = 'service');

-- NestJS usage:
-- await this.db.$executeRaw`SET app.current_org_id = ${orgId}`;
-- await this.db.$executeRaw`SET app.role = 'user'`;
EOF

# OpenSearch
files_in "03-database/opensearch" \
  "contacts-index-mapping.json" "companies-index-mapping.json" \
  "deals-index-mapping.json" "activities-index-mapping.json" \
  "index-lifecycle-policy.json" "sync-worker.md" \
  "query-examples.md" "analyzer-config.json"

write "03-database/opensearch/contacts-index-mapping.json" << 'EOF'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "contact_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "stop"]
        },
        "autocomplete_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "edge_ngram_filter"]
        }
      },
      "filter": {
        "edge_ngram_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id":           { "type": "keyword" },
      "org_id":       { "type": "keyword" },
      "full_name":    { "type": "text", "analyzer": "contact_analyzer",
                        "fields": { "autocomplete": { "type": "text", "analyzer": "autocomplete_analyzer" },
                                    "keyword": { "type": "keyword" } } },
      "email":        { "type": "keyword" },
      "phone":        { "type": "keyword" },
      "job_title":    { "type": "text", "analyzer": "contact_analyzer" },
      "company_name": { "type": "text", "analyzer": "contact_analyzer",
                        "fields": { "keyword": { "type": "keyword" } } },
      "source":       { "type": "keyword" },
      "email_status": { "type": "keyword" },
      "ai_score":     { "type": "float" },
      "created_at":   { "type": "date" },
      "updated_at":   { "type": "date" }
    }
  }
}
EOF

# Redis
files_in "03-database/redis" \
  "key-design.md" "ttl-strategy.md" "cache-invalidation.md" \
  "rate-limiter-design.md" "bull-queue-config.md" "lua-scripts.md"

write "03-database/redis/key-design.md" << 'EOF'
# Redis Key Design

## Naming Convention

```
{namespace}:{entity}:{id}[:{subkey}]
```

## Key Catalogue

### Caching
| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `contact:{id}` | STRING | 5min | Full contact JSON |
| `search:{org}:{hash}` | STRING | 60s | Search results |
| `company:{id}` | STRING | 10min | Company profile |
| `user_session:{id}` | HASH | 24h | Session metadata |
| `org_settings:{org_id}` | HASH | 30min | Org config |

### Rate Limiting (Token Bucket)
| Key Pattern | Type | TTL | Limit |
|-------------|------|-----|-------|
| `rate_limit:hunter:{org_id}` | STRING | 60s | 100/min |
| `rate_limit:zerobounce:{org_id}` | STRING | 60s | 200/min |
| `rate_limit:twilio:{org_id}` | STRING | 60s | 30/min (TRAI) |
| `rate_limit:ai_chat:{user_id}` | STRING | 60s | 20/min |
| `rate_limit:api:{org_id}` | STRING | 60s | 1000/min |

### Campaign Buffers
| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `campaign_stats:{id}` | HASH | none | {sent, delivered, opened, clicked} |

### AI Workflows
| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `workflow:pending:{id}` | STRING | 24h | Paused AgentState |
| `workflow:approved:{id}` | STRING | 5min | Approval flag |

### Distributed Locks
| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `lock:enrich:{contact_id}` | STRING | 30s | Prevent duplicate enrichment |
| `lock:campaign_launch:{id}` | STRING | 60s | Prevent double-launch |
| `lock:flush_stats:{id}` | STRING | 10s | Prevent concurrent stat flush |
EOF

log "03-database (71 files)"

# =============================================================================
# SECTION 04 — API
# =============================================================================
header "04 — API"

# REST resources
REST_DIRS=(
  "04-api/rest/auth"
  "04-api/rest/contacts"
  "04-api/rest/companies"
  "04-api/rest/deals"
  "04-api/rest/activities"
  "04-api/rest/email"
  "04-api/rest/phone"
  "04-api/rest/campaigns"
  "04-api/rest/ai"
  "04-api/rest/analytics"
  "04-api/rest/files"
  "04-api/rest/jobs"
  "04-api/rest/integrations"
  "04-api/rest/users"
  "04-api/rest/organizations"
  "04-api/rest/bql"
  "04-api/rest/templates"
)
for d in "${REST_DIRS[@]}"; do mkd "$d"; done

files_in "04-api/rest/auth"          "authentication.md" "authorization.md" "oauth2.md" "jwt-tokens.md"
files_in "04-api/rest/contacts"      "list-contacts.md" "create-contact.md" "get-contact.md" \
                                     "update-contact.md" "delete-contact.md" "search-contacts.md" \
                                     "import-contacts.md" "export-contacts.md" "bulk-operations.md"
files_in "04-api/rest/companies"     "list-companies.md" "create-company.md" "get-company.md" \
                                     "update-company.md" "merge-companies.md"
files_in "04-api/rest/deals"         "list-deals.md" "create-deal.md" "get-deal.md" \
                                     "update-deal.md" "move-stage.md" "pipeline-view.md"
files_in "04-api/rest/activities"    "list-activities.md" "create-activity.md" "activity-types.md"
files_in "04-api/rest/email"         "validate-email.md" "discover-email.md" "bulk-validate.md"
files_in "04-api/rest/phone"         "validate-phone.md" "lookup-phone.md" "bulk-validate.md"
files_in "04-api/rest/campaigns"     "list-campaigns.md" "create-campaign.md" "launch-campaign.md" \
                                     "pause-campaign.md" "campaign-stats.md" "add-targets.md"
files_in "04-api/rest/ai"            "chat.md" "score-lead.md" "approve-workflow.md" "workflow-status.md"
files_in "04-api/rest/analytics"     "dashboard.md" "pipeline-report.md" "campaign-report.md"
files_in "04-api/rest/files"         "upload-file.md" "list-files.md" "analyze-file.md"
files_in "04-api/rest/jobs"          "list-jobs.md" "job-status.md" "cancel-job.md"
files_in "04-api/rest/integrations"  "list-integrations.md" "connect.md" "disconnect.md"
files_in "04-api/rest/users"         "list-users.md" "invite-user.md" "update-role.md"
files_in "04-api/rest/organizations" "get-org.md" "update-org.md" "billing.md"
files_in "04-api/rest/bql"           "execute-query.md" "query-syntax.md" "export-results.md"
files_in "04-api/rest/templates"     "list-templates.md" "create-template.md" "preview-template.md"
files_in "04-api/rest"               "openapi-spec.yaml" "error-reference.md" "pagination.md" \
                                     "rate-limiting.md" "versioning.md"

# Write create-contact endpoint doc
write "04-api/rest/contacts/create-contact.md" << 'EOF'
# POST /v1/contacts — Create Contact

Creates a new CRM contact and optionally triggers the enrichment pipeline.

## Request

```http
POST /v1/contacts
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "first_name": "Priya",
  "last_name": "Sharma",
  "email": "priya.sharma@acme.com",
  "phone": "+919876543210",
  "company_id": "uuid",
  "job_title": "VP Engineering",
  "source": "manual",
  "trigger_enrichment": true
}
```

## Response `201 Created`

```json
{
  "id": "uuid",
  "org_id": "uuid",
  "full_name": "Priya Sharma",
  "email": "priya.sharma@acme.com",
  "email_status": "UNKNOWN",
  "phone": "+919876543210",
  "job_title": "VP Engineering",
  "source": "manual",
  "created_at": "2026-04-14T13:00:00Z",
  "enrichment_job_id": "uuid"
}
```

## Validation Rules

| Field | Rule |
|-------|------|
| `first_name` | Required, 1-100 chars |
| `email` | Valid email format, unique per org |
| `phone` | E.164 or local format |
| `source` | Enum: `extension`, `import`, `manual`, `ai`, `api` |

## Error Responses

| Code | Error | Description |
|------|-------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid field values |
| 409 | `DUPLICATE_EMAIL` | Email already exists in org |
| 429 | `RATE_LIMIT` | Too many requests |

## Kafka Events Emitted

`contact.created` → triggers email enrichment, phone validation, embedding generation.
EOF

# GraphQL, WebSocket, Webhooks
mkd "04-api/graphql"
mkd "04-api/websocket"
mkd "04-api/webhooks"
files_in "04-api/graphql"   "schema.graphql" "queries.md" "mutations.md" "subscriptions.md" \
                             "fragments.md" "directives.md" "error-handling.md" "pagination.md"
files_in "04-api/websocket" "connection-protocol.md" "events-reference.md" "rooms-and-channels.md" \
                             "authentication.md" "reconnection-strategy.md" "client-examples.md"
files_in "04-api/webhooks"  "webhook-overview.md" "event-catalog.md" "signature-verification.md" \
                             "retry-policy.md" "testing-webhooks.md" "payload-reference.md"

log "04-api (80 files)"

# =============================================================================
# SECTION 05 — FRONTEND
# =============================================================================
header "05 — Frontend"

mkd "05-frontend/web"
mkd "05-frontend/admin"
mkd "05-frontend/mobile"
mkd "05-frontend/components"

files_in "05-frontend/web" \
  "README.md" "folder-structure.md" "routing.md" "state-management.md" \
  "react-query-patterns.md" "form-handling.md" "auth-flow.md" "theming.md" \
  "performance-optimization.md" "error-boundaries.md" "testing.md" \
  "storybook.md" "accessibility.md" "i18n.md" "build-and-deploy.md"

files_in "05-frontend/admin" \
  "README.md" "admin-roles.md" "data-tables.md" "analytics-views.md" \
  "user-management.md" "org-settings.md" "billing-ui.md"

files_in "05-frontend/mobile" \
  "README.md" "navigation.md" "offline-sync.md" "push-notifications.md" \
  "biometric-auth.md" "camera-integration.md" "deep-linking.md" "app-store-deploy.md"

files_in "05-frontend/components" \
  "design-system.md" "contact-card.md" "deal-card.md" "pipeline-board.md" \
  "data-table.md" "search-bar.md" "ai-chat-widget.md" "email-composer.md" \
  "campaign-builder.md" "analytics-charts.md" "file-uploader.md" \
  "activity-feed.md" "notification-bell.md" "command-palette.md" "kanban-board.md"

log "05-frontend (45 files)"

# =============================================================================
# SECTION 06 — AI / ML
# =============================================================================
header "06 — AI/ML"

mkd "06-ai-ml/agents"
mkd "06-ai-ml/mcp"
mkd "06-ai-ml/embeddings"
mkd "06-ai-ml/models"
mkd "06-ai-ml/prompts"

files_in "06-ai-ml/agents" \
  "supervisor-agent.md" "tool-definitions.md" "state-schema.md" \
  "graph-topology.md" "approval-flow.md" "memory-system.md" \
  "agent-evaluation.md" "streaming-responses.md"

files_in "06-ai-ml/mcp" \
  "mcp-server-overview.md" "crm-mcp-server.md" "tool-catalog.md" \
  "resource-catalog.md" "transport-layer.md" "testing-mcp.md" "adding-new-tools.md"

files_in "06-ai-ml/embeddings" \
  "embedding-strategy.md" "hybrid-search.md" "rrf-algorithm.md" \
  "hnsw-index-config.md" "embedding-pipeline.md" "chunking-strategy.md" \
  "model-selection.md" "benchmarks.md"

files_in "06-ai-ml/models" \
  "lead-scoring-model.md" "win-probability.md" "churn-prediction.md" \
  "email-sentiment.md" "next-best-action.md" "model-training.md" \
  "feature-engineering.md" "model-evaluation.md"

files_in "06-ai-ml/prompts" \
  "system-prompts.md" "intent-classification.md" "plan-formulation.md" \
  "synthesis-prompts.md" "few-shot-examples.md" "prompt-versioning.md" "prompt-testing.md"

log "06-ai-ml (40 files)"

# =============================================================================
# SECTION 07 — EXTENSION
# =============================================================================
header "07 — Chrome Extension"

mkd "07-extension/chrome"
mkd "07-extension/content-scripts"
mkd "07-extension/background"

files_in "07-extension/chrome" \
  "README.md" "architecture.md" "manifest-v3.md" "permissions.md" \
  "store-listing.md" "privacy-policy.md" "legal-compliance.md" \
  "publishing.md" "auto-update.md"

files_in "07-extension/content-scripts" \
  "linkedin-scraper.md" "email-detector.md" "phone-detector.md" \
  "contact-overlay.md" "dom-traversal.md" "mutation-observer.md" "data-sanitization.md"

files_in "07-extension/background" \
  "service-worker.md" "message-routing.md" "api-client.md" \
  "auth-token-manager.md" "queue-manager.md" "sync-engine.md"

log "07-extension (22 files)"

# =============================================================================
# SECTION 08 — ENRICHMENT
# =============================================================================
header "08 — Enrichment"

mkd "08-enrichment/email"
mkd "08-enrichment/phone"
mkd "08-enrichment/providers"

files_in "08-enrichment/email" \
  "enrichment-overview.md" "pattern-discovery.md" "validation-pipeline.md" \
  "deduplication.md" "confidence-scoring.md" "bulk-enrichment.md" \
  "webhook-callbacks.md" "enrichment-metrics.md"

files_in "08-enrichment/phone" \
  "validation-overview.md" "e164-normalization.md" "carrier-lookup.md" \
  "line-type-detection.md" "bulk-validation.md" "india-compliance.md"

files_in "08-enrichment/providers" \
  "hunter-io.md" "zerobounce.md" "millionverifier.md" "twilio-lookup.md" \
  "numverify.md" "clearbit.md" "provider-fallback.md" "cost-optimization.md"

log "08-enrichment (22 files)"

# =============================================================================
# SECTION 09 — CAMPAIGNS
# =============================================================================
header "09 — Campaigns"

mkd "09-campaigns/email"
mkd "09-campaigns/sms"
mkd "09-campaigns/whatsapp"
mkd "09-campaigns/sequences"

files_in "09-campaigns/email" \
  "email-campaign-guide.md" "sendgrid-integration.md" "smtp-setup.md" \
  "deliverability.md" "bounce-handling.md" "spam-score-check.md" \
  "unsubscribe-management.md" "open-tracking.md" "click-tracking.md"

files_in "09-campaigns/sms" \
  "sms-campaign-guide.md" "twilio-sms.md" "dlt-registration.md" \
  "trai-compliance.md" "opt-out-handling.md" "sms-templates.md"

files_in "09-campaigns/whatsapp" \
  "whatsapp-guide.md" "whatsapp-bsp.md" "template-approval.md" \
  "message-types.md" "media-messages.md" "whatsapp-compliance.md"

files_in "09-campaigns/sequences" \
  "drip-sequences.md" "sequence-conditions.md" "a-b-testing.md" \
  "sequence-analytics.md" "pause-resume.md" "contact-exit-rules.md"

log "09-campaigns (27 files)"

# =============================================================================
# SECTION 10 — INTEGRATIONS
# =============================================================================
header "10 — Integrations"

mkd "10-integrations/gmail"
mkd "10-integrations/slack"
mkd "10-integrations/whatsapp"
mkd "10-integrations/salesforce"
mkd "10-integrations/hubspot"
mkd "10-integrations/webhooks"

files_in "10-integrations/gmail"      "gmail-setup.md" "oauth2-flow.md" "email-sync.md" "sent-tracking.md" "gmail-labels.md"
files_in "10-integrations/slack"      "slack-app-setup.md" "slash-commands.md" "block-kit-messages.md" \
                                       "approval-buttons.md" "slack-agent-flow.md" "notifications.md"
files_in "10-integrations/whatsapp"   "whatsapp-bsp-setup.md" "webhook-config.md" "template-management.md" \
                                       "opt-in-flow.md" "chatbot-responses.md"
files_in "10-integrations/salesforce" "salesforce-setup.md" "field-mapping.md" "bidirectional-sync.md" \
                                       "conflict-resolution.md" "salesforce-oauth.md"
files_in "10-integrations/hubspot"    "hubspot-setup.md" "contact-sync.md" "deal-sync.md" "hubspot-oauth.md"
files_in "10-integrations/webhooks"   "webhook-overview.md" "registering-webhooks.md" "signature-validation.md" \
                                       "retry-mechanism.md" "webhook-testing.md"

log "10-integrations (30 files)"

# =============================================================================
# SECTION 11 — INFRA
# =============================================================================
header "11 — Infrastructure"

mkd "11-infra/aws"
mkd "11-infra/kubernetes"
mkd "11-infra/terraform"
mkd "11-infra/docker"
mkd "11-infra/cicd"

files_in "11-infra/aws" \
  "vpc-design.md" "ecs-fargate-setup.md" "rds-configuration.md" \
  "elasticache-setup.md" "s3-buckets.md" "alb-configuration.md" \
  "cloudfront-cdn.md" "iam-roles.md" "secrets-manager.md" \
  "cost-optimization.md" "multi-az.md" "auto-scaling.md"

files_in "11-infra/kubernetes" \
  "cluster-setup.md" "namespace-strategy.md" "deployments.md" \
  "services.md" "ingress.md" "configmaps.md" "secrets.md" \
  "hpa.md" "pdb.md" "network-policies.md" "rbac.md" \
  "helm-charts.md" "kustomize.md"

files_in "11-infra/terraform" \
  "modules-overview.md" "vpc-module.md" "ecs-module.md" "rds-module.md" \
  "state-backend.md" "workspaces.md" "variable-conventions.md" \
  "terraform-plan.md" "drift-detection.md"

files_in "11-infra/docker" \
  "dockerfile-conventions.md" "multi-stage-builds.md" "docker-compose-local.md" \
  "image-tagging.md" "base-images.md" "layer-caching.md"

files_in "11-infra/cicd" \
  "github-actions-overview.md" "build-pipeline.md" "test-pipeline.md" \
  "deploy-staging.md" "deploy-production.md" "rollback.md" \
  "canary-deploy.md" "secrets-in-ci.md" "branch-strategy.md"

log "11-infra (49 files)"

# =============================================================================
# SECTION 12 — SECURITY
# =============================================================================
header "12 — Security"
mkd "12-security"

files_in "12-security" \
  "auth-overview.md" "jwt-implementation.md" "oauth2-providers.md" \
  "rbac-model.md" "mfa-setup.md" "session-management.md" \
  "api-key-management.md" "secrets-rotation.md" "penetration-testing.md" \
  "owasp-mitigations.md" "gdpr-compliance.md" "trai-compliance.md" \
  "data-retention.md" "incident-response.md" "security-headers.md" \
  "rate-limiting.md" "ip-allowlisting.md" "audit-logging.md"

write "12-security/rbac-model.md" << 'EOF'
# RBAC Model

Contact360 uses a flat 4-role RBAC model enforced at the API gateway (JWT claims)
and database layer (PostgreSQL RLS).

## Roles

| Role | Description |
|------|-------------|
| `admin` | Full org access, user management, billing, integrations |
| `manager` | All CRM data, campaigns, reports; cannot manage users or billing |
| `user` | Own contacts/deals, view team data, send campaigns |
| `readonly` | View-only across all CRM entities |

## Permission Matrix

| Resource | admin | manager | user | readonly |
|----------|-------|---------|------|----------|
| Contacts (own) | ✅ | ✅ | ✅ | 👁 |
| Contacts (all) | ✅ | ✅ | 👁 | 👁 |
| Deals | ✅ | ✅ | ✅ | 👁 |
| Campaigns | ✅ | ✅ | create/own | 👁 |
| Analytics | ✅ | ✅ | own | 👁 |
| Users | ✅ | ❌ | ❌ | ❌ |
| Billing | ✅ | ❌ | ❌ | ❌ |
| Integrations | ✅ | view | ❌ | ❌ |
| AI workflows | ✅ | ✅ | own | ❌ |

## JWT Payload

```json
{
  "sub": "user-uuid",
  "org_id": "org-uuid",
  "role": "manager",
  "email": "user@acme.com",
  "iat": 1744636800,
  "exp": 1744723200
}
```

## Enforcement Layers

1. **API Gateway** — validates JWT, rejects expired/tampered tokens
2. **NestJS Guards** — `@Roles('admin', 'manager')` decorator on controllers
3. **PostgreSQL RLS** — `SET app.current_org_id` enforced at DB level
EOF

log "12-security (18 files)"

# =============================================================================
# SECTION 13 — OBSERVABILITY
# =============================================================================
header "13 — Observability"

mkd "13-observability/logging"
mkd "13-observability/metrics"
mkd "13-observability/tracing"
mkd "13-observability/alerts"

files_in "13-observability/logging" \
  "logging-strategy.md" "log-levels.md" "structured-logging.md" \
  "log-aggregation.md" "log-retention.md" "log-querying.md"

files_in "13-observability/metrics" \
  "metrics-overview.md" "service-slos.md" "custom-metrics.md" \
  "dashboard-setup.md" "alerting-rules.md" "capacity-planning.md"

files_in "13-observability/tracing" \
  "distributed-tracing.md" "trace-sampling.md" "span-conventions.md" \
  "jaeger-setup.md" "performance-profiling.md"

files_in "13-observability/alerts" \
  "alert-runbook.md" "pagerduty-setup.md" "escalation-policy.md" \
  "alert-fatigue.md" "on-call-schedule.md"

write "13-observability/metrics/service-slos.md" << 'EOF'
# Service SLOs

## SLO Targets

| Service | Availability | p50 Latency | p99 Latency | Error Rate |
|---------|-------------|-------------|-------------|------------|
| API Gateway | 99.95% | <20ms | <100ms | <0.1% |
| CRM Service | 99.9% | <50ms | <200ms | <0.5% |
| AI Service | 99.5% | <500ms | <5s | <1% |
| Email Service | 99.9% | <100ms | <500ms | <0.5% |
| Campaign Dispatch | 99.5% | — | — | <1% |
| Enrichment Pipeline | 99% | <2s | <30s | <2% |

## SLA Breach Alerts

Alerts fire when 5-minute rolling error rate exceeds SLO threshold.
See `alerts/alerting-rules.md` for Prometheus rule definitions.
EOF

log "13-observability (22 files)"

# =============================================================================
# SECTION 14 — TESTING
# =============================================================================
header "14 — Testing"

mkd "14-testing/unit"
mkd "14-testing/integration"
mkd "14-testing/e2e"
mkd "14-testing/performance"

files_in "14-testing/unit" \
  "unit-test-strategy.md" "jest-config.md" "pytest-config.md" \
  "mocking-patterns.md" "test-utilities.md" "coverage-requirements.md"

files_in "14-testing/integration" \
  "integration-strategy.md" "testcontainers.md" "kafka-testing.md" \
  "postgres-fixtures.md" "api-integration-tests.md" "seed-data.md"

files_in "14-testing/e2e" \
  "e2e-strategy.md" "playwright-setup.md" "test-scenarios.md" \
  "test-accounts.md" "visual-regression.md" "ci-e2e.md"

files_in "14-testing/performance" \
  "load-testing.md" "k6-scripts.md" "baseline-metrics.md" \
  "bottleneck-analysis.md" "stress-testing.md"

log "14-testing (23 files)"

# =============================================================================
# SECTION 15 — GUIDES
# =============================================================================
header "15 — Guides"

mkd "15-guides/onboarding"
mkd "15-guides/development"
mkd "15-guides/deployment"
mkd "15-guides/troubleshooting"

write "15-guides/onboarding/new-developer-setup.md" << 'EOF'
# New Developer Setup

Get from zero to a running local stack in under 30 minutes.

## Prerequisites

- Docker Desktop 4.x
- Node.js 20.x (`nvm install 20`)
- Python 3.12 (`pyenv install 3.12`)
- pnpm 9.x (`npm install -g pnpm`)
- AWS CLI v2

## 1. Clone

```bash
git clone git@github.com:your-org/contact360.git
cd contact360
pnpm install
pip install uv && uv sync
```

## 2. Start Local Stack

```bash
docker compose -f docker/docker-compose.local.yml up -d
# Starts: PostgreSQL 16, Redis 7, OpenSearch 2, Kafka 3.7, LocalStack
```

## 3. Environment Variables

```bash
cp .env.example .env
# Edit .env — minimum required:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contact360
# REDIS_URL=redis://localhost:6379
# OPENAI_API_KEY=sk-...
```

## 4. Database Setup

```bash
cd services/crm-service
pnpm prisma migrate dev
pnpm prisma db seed
```

## 5. Start All Services

```bash
# Terminal 1 — Node.js services
pnpm dev

# Terminal 2 — Python AI service
cd services/ai-service
uv run uvicorn src.main:app --reload --port 8000
```

## 6. Verify

| Service | URL | Expected |
|---------|-----|----------|
| Web UI | http://localhost:3000 | Login page |
| CRM API | http://localhost:3002/health | `{"status":"ok"}` |
| AI Service | http://localhost:8000/docs | Swagger UI |

## Demo Login

```
Email:    demo@contact360.io
Password: Demo@1234
```
EOF

files_in "15-guides/onboarding" \
  "first-pr.md" "local-stack.md" "environment-variables.md" \
  "seed-database.md" "ide-setup.md" "debugging-guide.md"

files_in "15-guides/development" \
  "coding-standards.md" "git-workflow.md" "pr-template.md" \
  "code-review-guide.md" "api-design-guide.md" "db-migration-guide.md" \
  "adding-a-service.md" "adding-a-kafka-topic.md" "feature-flags.md"

files_in "15-guides/deployment" \
  "deploy-to-staging.md" "deploy-to-production.md" "rollback-procedure.md" \
  "database-migration-deploy.md" "blue-green-deploy.md" \
  "canary-release.md" "hotfix-procedure.md"

files_in "15-guides/troubleshooting" \
  "common-errors.md" "kafka-issues.md" "postgres-issues.md" \
  "redis-issues.md" "ai-service-issues.md" "enrichment-failures.md" \
  "campaign-delivery-issues.md" "performance-debugging.md"

log "15-guides (31 files)"

# =============================================================================
# SECTION 16 — RUNBOOKS
# =============================================================================
header "16 — Runbooks"
mkd "16-runbooks"

RUNBOOKS=(
  "database-failover.md"
  "service-restart.md"
  "kafka-consumer-lag.md"
  "redis-cache-flush.md"
  "disk-space-cleanup.md"
  "ssl-certificate-renewal.md"
  "rate-limit-incident.md"
  "ai-service-degradation.md"
  "campaign-stuck.md"
  "import-job-failure.md"
  "opensearch-reindex.md"
  "postgres-vacuum.md"
)
for r in "${RUNBOOKS[@]}"; do tch "16-runbooks/$r"; done

write "16-runbooks/kafka-consumer-lag.md" << 'EOF'
# Runbook: Kafka Consumer Lag

**Severity:** P2 | **Owner:** Platform Team | **Est. Resolution:** 15-30 min

## Symptoms

- `kafka_consumer_lag` metric > 10,000 in Datadog
- `contact.enriched` events delayed > 5 minutes
- Users report enrichment not completing

## Diagnosis

```bash
# Check consumer group lag
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group enrichment-worker

# Check which partitions are lagging
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group enrichment-worker | grep -v "0   0"
```

## Resolution Steps

### Step 1: Check worker health
```bash
kubectl get pods -n contact360 -l app=email-enrichment-worker
kubectl logs -l app=email-enrichment-worker --tail=100
```

### Step 2: Scale up consumers (if lag is due to volume spike)
```bash
kubectl scale deployment email-enrichment-worker --replicas=6
```

### Step 3: If consumer is in error loop, restart
```bash
kubectl rollout restart deployment/email-enrichment-worker
```

### Step 4: If DLQ is filling up, inspect failed messages
```bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic contact.enrichment.dlq \
  --from-beginning --max-messages 10
```

## Post-Incident

- Update consumer lag alert threshold if this was expected volume growth
- Document root cause in #incidents Slack channel
EOF

log "16-runbooks (12 files)"

# =============================================================================
# SECTION 17 — ADRs
# =============================================================================
header "17 — Architecture Decision Records"
mkd "17-adrs"

ADRS=(
  "ADR-001-microservices-vs-monolith.md"
  "ADR-002-postgresql-as-primary-db.md"
  "ADR-003-kafka-for-events.md"
  "ADR-004-langgraph-for-agents.md"
  "ADR-005-mcp-protocol.md"
  "ADR-006-pgvector-vs-pinecone.md"
  "ADR-007-nestjs-for-backend.md"
  "ADR-008-fastapi-for-ai-service.md"
  "ADR-009-opensearch-vs-elasticsearch.md"
  "ADR-010-monorepo-structure.md"
  "ADR-011-jwt-vs-session-auth.md"
  "ADR-012-redis-for-queues.md"
  "ADR-013-multi-tenancy-rls.md"
  "ADR-014-chrome-extension-mv3.md"
  "ADR-015-hybrid-search-rrf.md"
)
for a in "${ADRS[@]}"; do tch "17-adrs/$a"; done

write "17-adrs/ADR-006-pgvector-vs-pinecone.md" << 'EOF'
# ADR-006: pgvector vs Pinecone for Vector Storage

**Status:** Accepted | **Date:** 2026-02-12

## Context

Contact360 requires semantic similarity search over contact profiles, emails,
notes, and activity history for the RAG pipeline and agent memory.

## Options Considered

| Criteria | pgvector | Pinecone |
|----------|----------|----------|
| Hosting | Self-managed (RDS) | Fully managed |
| p99 Latency | 5-20ms (HNSW) | 5-15ms |
| SQL joins | Native | App-layer only |
| RLS / multi-tenancy | Native PostgreSQL RLS | Custom namespace per org |
| Cost (1M vectors) | ~$0 (existing RDS) | ~$70/mo (Starter) |
| Hybrid search | tsvector + vector (one query) | Two separate systems |

## Decision: pgvector

1. **Single transaction** — contacts and embeddings in the same PostgreSQL ACID transaction
2. **Native RLS** — `org_id` isolation enforced automatically at the DB layer
3. **Hybrid search** — one SQL query combines cosine similarity + `ts_rank` via RRF
4. **Zero marginal cost** — stored on existing RDS instances
5. **HNSW accuracy** — `m=16, ef_construction=64` achieves <20ms p99 at 10M vectors

## Consequences

- HNSW index build time is O(n log n) — bulk imports require background indexing
- At >50M vectors, re-evaluate Pinecone or pgvector + dedicated instance
- Must manage `pgvector` extension upgrades via RDS parameter groups

## Implementation

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX CONCURRENTLY idx_contact_embeddings_hnsw
ON contact_embeddings USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```
EOF

write "17-adrs/ADR-004-langgraph-for-agents.md" << 'EOF'
# ADR-004: LangGraph for AI Agent Orchestration

**Status:** Accepted | **Date:** 2026-01-28

## Context

The AI agent must: execute multi-step CRM workflows, pause for Slack approval,
resume from persisted state, handle tool failures with retries, and maintain
full audit trails.

Options evaluated: LangGraph, AutoGen, CrewAI, custom FSM, Temporal.

## Decision: LangGraph

1. **Graph control flow** — nodes + conditional edges map exactly to CRM workflows
2. **Native pause/resume** — `StateGraph` interrupt-and-resume via persisted `AgentState`
3. **Streaming** — `astream_events()` enables real-time token streaming to UI
4. **Tool inspection** — every call captured in state → `mcp_invocations` audit log
5. **LangSmith** — production tracing without custom instrumentation

## Consequences

- Python-only runtime (FastAPI, not NestJS) for the AI service
- State serialization to PostgreSQL JSONB adds ~5ms per graph step
- LangGraph 0.2.x API pinned — upgrade requires migration testing
EOF

log "17-adrs (15 files)"

# =============================================================================
# SECTION 18 — CHANGELOG
# =============================================================================
header "18 — Changelog"
mkd "18-changelog"

write "18-changelog/CHANGELOG.md" << 'EOF'
# Changelog

All notable changes to Contact360 are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

## [Unreleased]
### In Progress
- WhatsApp BSP integration
- Churn prediction model
- Chrome extension v2

## [1.0.0] — 2026-04-14
### Added
- Full CRM core: Contacts, Companies, Deals, Activities
- Email enrichment pipeline (Hunter + ZeroBounce + MillionVerifier)
- Phone validation (Twilio Lookup + libphonenumber)
- Multi-channel campaigns (Email, SMS, WhatsApp)
- LangGraph AI agent with Slack approval flow
- MCP server with 4 CRM tools + 3 resources
- pgvector HNSW hybrid search (RRF fusion)
- Chrome MV3 extension (LinkedIn scraping)
- Multi-tenant PostgreSQL with RLS
- OpenSearch sync pipeline via Kafka
- AWS ECS Fargate deployment with Terraform

## [0.9.0] — 2026-03-01
### Added
- Auth service (JWT + OAuth2 Google/GitHub)
- CRM service foundation
- PostgreSQL schema v1 (20 tables)
- Redis caching layer
- Kafka event bus
EOF

files_in "18-changelog" \
  "v1.0.0.md" "v0.9.0.md" "v0.8.0.md" \
  "v0.7.0.md" "v0.6.0.md" "migration-guide.md"

log "18-changelog (7 files)"

# =============================================================================
# FINAL SUMMARY
# =============================================================================
divider
TOTAL_FILES=$(find "$BASE" -type f | wc -l)
TOTAL_DIRS=$(find "$BASE" -type d | wc -l)

echo -e "\n${BOLD}${GREEN}✅  Scaffold complete!${RESET}\n"
printf "  ${BOLD}%-20s${RESET} %s\n" "Target directory:" "$BASE"
printf "  ${BOLD}%-20s${RESET} %s\n" "Total files:"      "$TOTAL_FILES"
printf "  ${BOLD}%-20s${RESET} %s\n" "Total directories:" "$TOTAL_DIRS"
echo ""
echo -e "  ${CYAN}Files with full written content:${RESET}"
echo "  ✅  README.md"
echo "  ✅  01-architecture/system-overview.md"
echo "  ✅  02-services/crm-service/README.md"
echo "  ✅  02-services/ai-service/README.md"
echo "  ✅  03-database/migrations/V0001__init_extensions.sql"
echo "  ✅  03-database/indexes/embeddings-hnsw.sql"
echo "  ✅  03-database/rls-policies/contacts-rls.sql"
echo "  ✅  03-database/redis/key-design.md"
echo "  ✅  03-database/opensearch/contacts-index-mapping.json"
echo "  ✅  04-api/rest/contacts/create-contact.md"
echo "  ✅  12-security/rbac-model.md"
echo "  ✅  13-observability/metrics/service-slos.md"
echo "  ✅  15-guides/onboarding/new-developer-setup.md"
echo "  ✅  16-runbooks/kafka-consumer-lag.md"
echo "  ✅  17-adrs/ADR-004-langgraph-for-agents.md"
echo "  ✅  17-adrs/ADR-006-pgvector-vs-pinecone.md"
echo "  ✅  18-changelog/CHANGELOG.md"
echo ""
echo -e "  ${YELLOW}Next steps:${RESET}"
echo "  1. cd $BASE"
echo "  2. Open in VS Code: code ."
echo "  3. Fill remaining stubs with: pnpm run docs:generate"
divider
