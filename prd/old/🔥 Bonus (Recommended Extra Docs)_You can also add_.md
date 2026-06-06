<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 🔥 Bonus (Recommended Extra Docs)

You can also add:
ai-architecture.md → AI agent design
database-schema.md → tables + relations
event-driven.md → Kafka / Redis flows
extension.md → Chrome extension logic
and so no

Here are all 4 bonus documents in full — copy each block into its respective file:

***

# 📄 `ai-architecture.md`

```markdown
# Contact360 — AI Architecture

> **Model:** LangGraph agent orchestration · RAG pipeline · Human-in-the-loop
> Version 1.0 · April 2026

---

## Table of Contents
1. [AI System Overview](#1-ai-system-overview)
2. [Agent Orchestration (LangGraph)](#2-agent-orchestration-langgraph)
3. [RAG Pipeline](#3-rag-pipeline)
4. [Tool Registry](#4-tool-registry)
5. [Human-in-the-Loop](#5-human-in-the-loop)
6. [Memory Architecture](#6-memory-architecture)
7. [Model Configuration](#7-model-configuration)
8. [Prompt Engineering](#8-prompt-engineering)
9. [Observability](#9-observability)

---

# 1. AI System Overview

```

User Query
│
▼
┌───────────────────────────────────────────────────────────────┐
│                    AI AGENT SERVICE                           │
│                                                               │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │  Query      │    │  LangGraph   │    │  Tool          │  │
│  │  Classifier │───▶│  Orchestrator│───▶│  Executor      │  │
│  └─────────────┘    └──────────────┘    └────────────────┘  │
│         │                  │                     │           │
│         ▼                  ▼                     ▼           │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │  Intent     │    │  RAG Context │    │  CRM Service   │  │
│  │  Detection  │    │  Retrieval   │    │  Email Service │  │
│  └─────────────┘    └──────────────┘    │  Campaign Svc  │  │
│                            │            └────────────────┘  │
│                            ▼                                 │
│                    ┌──────────────┐                          │
│                    │  pgvector +  │                          │
│                    │  OpenSearch  │                          │
│                    └──────────────┘                          │
└───────────────────────────────────────────────────────────────┘
│
▼
Human Approval Gate (for actions)
│
▼
Response + Action

```

---

# 2. Agent Orchestration (LangGraph)

## Agent Graph Definition

```typescript
// apps/ai-agent-service/src/agents/contact360.agent.ts
import { StateGraph, END } from '@langchain/langgraph';
import { ChatOpenAI } from '@langchain/openai';
import { ToolNode } from '@langchain/langgraph/prebuilt';

export interface AgentState {
  messages:       BaseMessage[];
  orgId:          string;
  userId:         string;
  intent:         string | null;
  context:        RAGContext | null;
  pendingAction:  AgentAction | null;
  actionApproved: boolean;
  iteration:      number;
}

const MAX_ITERATIONS = 10;

// ── Node definitions ──────────────────────────────────────────────
async function classifyIntent(state: AgentState): Promise<Partial<AgentState>> {
  const lastMessage = state.messages.at(-1)?.content as string;
  const intent = await intentClassifier.classify(lastMessage);
  return { intent };
}

async function retrieveContext(state: AgentState): Promise<Partial<AgentState>> {
  if (!state.intent) return {};

  // Hybrid retrieval: pgvector semantic + OpenSearch keyword
  const context = await ragPipeline.retrieve({
    query:  state.messages.at(-1)?.content as string,
    orgId:  state.orgId,
    intent: state.intent,
    topK:   10,
  });

  return { context };
}

async function callModel(state: AgentState): Promise<Partial<AgentState>> {
  const model = new ChatOpenAI({ model: 'gpt-4o', temperature: 0.1 })
    .bindTools(getToolsForIntent(state.intent));

  const systemPrompt = buildSystemPrompt(state.orgId, state.context);
  const response = await model.invoke([
    { role: 'system', content: systemPrompt },
    ...state.messages,
  ]);

  return { messages: [...state.messages, response] };
}

async function prepareAction(state: AgentState): Promise<Partial<AgentState>> {
  const lastMessage = state.messages.at(-1);
  if (!lastMessage?.tool_calls?.length) return {};

  const toolCall = lastMessage.tool_calls;
  if (!REQUIRES_APPROVAL.includes(toolCall.name)) return {};

  return {
    pendingAction: {
      tool:       toolCall.name,
      args:       toolCall.args,
      preview:    await generateActionPreview(toolCall),
      riskLevel:  getRiskLevel(toolCall.name),
    },
  };
}

// ── Routing logic ─────────────────────────────────────────────────
function shouldContinue(state: AgentState): 'tools' | 'prepare_action' | 'end' {
  if (state.iteration >= MAX_ITERATIONS) return 'end';

  const last = state.messages.at(-1);
  if (!last?.tool_calls?.length) return 'end';

  const toolName = last.tool_calls.name;
  return REQUIRES_APPROVAL.includes(toolName) ? 'prepare_action' : 'tools';
}

// ── Graph assembly ────────────────────────────────────────────────
const workflow = new StateGraph<AgentState>({ channels: stateChannels })
  .addNode('classify_intent',  classifyIntent)
  .addNode('retrieve_context', retrieveContext)
  .addNode('call_model',       callModel)
  .addNode('tools',            new ToolNode(ALL_TOOLS))
  .addNode('prepare_action',   prepareAction)

  .addEdge('__start__',        'classify_intent')
  .addEdge('classify_intent',  'retrieve_context')
  .addEdge('retrieve_context', 'call_model')
  .addConditionalEdges('call_model', shouldContinue, {
    tools:          'tools',
    prepare_action: 'prepare_action',
    end:            END,
  })
  .addEdge('tools',            'call_model')
  .addEdge('prepare_action',   END);

export const agent = workflow.compile({ checkpointer: redisCheckpointer });
```


---

# 3. RAG Pipeline

## Hybrid Retrieval Strategy

```typescript
// apps/ai-agent-service/src/rag/rag.pipeline.ts
@Injectable()
export class RAGPipeline {
  async retrieve(params: RetrieveParams): Promise<RAGContext> {
    const [semanticResults, keywordResults] = await Promise.all([
      // Semantic: pgvector cosine similarity
      this.semanticSearch(params.query, params.orgId, params.topK),
      // Keyword: OpenSearch BM25
      this.keywordSearch(params.query, params.orgId, params.topK),
    ]);

    // Reciprocal Rank Fusion (RRF) to merge results
    const merged = this.reciprocalRankFusion(semanticResults, keywordResults);

    // Re-rank top 5 with cross-encoder
    const reranked = await this.reranker.rerank(params.query, merged.slice(0, 5));

    return {
      contacts:    reranked.filter(r => r.type === 'contact'),
      campaigns:   reranked.filter(r => r.type === 'campaign'),
      deals:       reranked.filter(r => r.type === 'deal'),
      activities:  reranked.filter(r => r.type === 'activity'),
      totalTokens: this.estimateTokens(reranked),
    };
  }

  private async semanticSearch(query: string, orgId: string, topK: number) {
    const embedding = await this.embedder.embed(query);  // OpenAI text-embedding-3-small

    return this.prisma.$queryRaw`
      SELECT id, type, content, metadata,
             1 - (embedding <=> ${embedding}::vector) AS similarity
      FROM contact_embeddings
      WHERE org_id = ${orgId}
        AND 1 - (embedding <=> ${embedding}::vector) > 0.7
      ORDER BY similarity DESC
      LIMIT ${topK}
    `;
  }

  private reciprocalRankFusion(semantic: any[], keyword: any[], k = 60) {
    const scores = new Map<string, number>();

    semantic.forEach((doc, rank) => {
      scores.set(doc.id, (scores.get(doc.id) ?? 0) + 1 / (k + rank + 1));
    });
    keyword.forEach((doc, rank) => {
      scores.set(doc.id, (scores.get(doc.id) ?? 0) + 1 / (k + rank + 1));
    });

    const allDocs = [...new Map([...semantic, ...keyword].map(d => [d.id, d])).values()];
    return allDocs.sort((a, b) => (scores.get(b.id) ?? 0) - (scores.get(a.id) ?? 0));
  }
}
```


---

# 4. Tool Registry

## Available Tools

```typescript
// apps/ai-agent-service/src/tools/tool-registry.ts

// READ tools — no approval needed
export const READ_TOOLS = [
  tool({
    name: 'search_contacts',
    description: 'Search contacts by name, email, company, job title, or tags',
    schema: z.object({
      query:   z.string(),
      filters: z.object({ jobTitle: z.string().optional(), company: z.string().optional() }).optional(),
      limit:   z.number().max(50).default(10),
    }),
    func: async ({ query, filters, limit }, { orgId }) =>
      contactsService.search(orgId, query, filters, limit),
  }),

  tool({
    name: 'get_campaign_analytics',
    description: 'Get open rate, click rate, reply rate for a campaign',
    schema: z.object({ campaignId: z.string().optional(), period: z.string().optional() }),
    func: async ({ campaignId, period }, { orgId }) =>
      analyticsService.getCampaignStats(orgId, campaignId, period),
  }),

  tool({
    name: 'rank_leads',
    description: 'Rank contacts by engagement score to find top leads',
    schema: z.object({ listId: z.string().optional(), limit: z.number().default(10) }),
    func: async ({ listId, limit }, { orgId }) =>
      leadScoringService.rankLeads(orgId, listId, limit),
  }),
];

// WRITE tools — REQUIRE human approval
export const WRITE_TOOLS = [
  tool({
    name:        'send_campaign',
    description: 'Send or schedule an email/SMS campaign to a contact list',
    requiresApproval: true,
    riskLevel:   'high',
    schema: z.object({
      name:       z.string(),
      templateId: z.string(),
      audienceId: z.string(),
      schedule:   z.object({ type: z.enum(['now', 'scheduled']), sendAt: z.string().optional() }),
    }),
    func: async (args, { orgId, userId }) =>
      campaignService.create(orgId, userId, args),
  }),

  tool({
    name:        'update_contact',
    description: 'Update a contact\'s fields',
    requiresApproval: true,
    riskLevel:   'medium',
    schema: z.object({
      contactId: z.string(),
      updates:   z.record(z.string(), z.any()),
    }),
    func: async ({ contactId, updates }, { orgId }) =>
      contactsService.update(orgId, contactId, updates),
  }),

  tool({
    name:        'add_to_list',
    description: 'Add contacts to a named list',
    requiresApproval: true,
    riskLevel:   'low',
    schema: z.object({
      contactIds: z.array(z.string()),
      listName:   z.string(),
    }),
    func: async ({ contactIds, listName }, { orgId }) =>
      listsService.addContacts(orgId, listName, contactIds),
  }),
];

// Tools that can NEVER be called by AI (safety hard-block)
export const FORBIDDEN_TOOLS = [
  'delete_all_contacts',
  'change_billing',
  'create_api_key',
  'manage_users',
  'export_all_data',
];
```


---

# 5. Human-in-the-Loop

```typescript
// apps/ai-agent-service/src/approval/approval.gateway.ts
@WebSocketGateway({ namespace: '/ai' })
export class ApprovalGateway {

  // AI pauses and sends action preview to frontend
  async requestApproval(userId: string, action: AgentAction): Promise<boolean> {
    const approvalId = crypto.randomUUID();

    // Push approval request to user's browser via WebSocket
    this.server.to(`user:${userId}`).emit('approval_required', {
      approvalId,
      action: {
        tool:     action.tool,
        preview:  action.preview,
        riskLevel: action.riskLevel,
        affectedCount: action.args.contactIds?.length,
      },
    });

    // Wait for user response (30 second timeout)
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        this.pendingApprovals.delete(approvalId);
        resolve(false);  // Auto-reject on timeout
      }, 30_000);

      this.pendingApprovals.set(approvalId, (approved: boolean) => {
        clearTimeout(timeout);
        resolve(approved);
      });
    });
  }

  @SubscribeMessage('approval_response')
  handleApprovalResponse(
    @MessageBody() data: { approvalId: string; approved: boolean }
  ) {
    const resolver = this.pendingApprovals.get(data.approvalId);
    if (resolver) {
      this.pendingApprovals.delete(data.approvalId);
      resolver(data.approved);
    }
  }
}
```


---

# 6. Memory Architecture

```
SHORT-TERM MEMORY (Redis — session scoped)
  key: contact360:ai:session:{sessionId}
  TTL: 2 hours
  Content: last 20 messages, current context window

LONG-TERM MEMORY (PostgreSQL — org scoped)
  table: ai_memories
  Content: user preferences, past instructions, org facts
  Example: "User prefers Tuesday sends", "Exclude @competitor.com contacts"

VECTOR MEMORY (pgvector — org scoped)
  table: contact_embeddings
  Content: contact profiles, campaign results, activity summaries
  Embed model: text-embedding-3-small (1536 dimensions)
  Index: HNSW (m=16, ef_construction=64)
```


---

# 7. Model Configuration

| Use Case | Model | Temperature | Max Tokens |
| :-- | :-- | :-- | :-- |
| Query understanding + tool calls | GPT-4o | 0.1 | 2,048 |
| Email draft generation | GPT-4o | 0.7 | 1,024 |
| Lead ranking reasoning | GPT-4o-mini | 0.0 | 512 |
| Embeddings | text-embedding-3-small | — | — |
| Re-ranking | cross-encoder/ms-marco | — | — |
| Fallback (cost saving) | GPT-4o-mini | 0.1 | 1,024 |


---

# 8. Prompt Engineering

## System Prompt Template

```typescript
function buildSystemPrompt(orgId: string, context: RAGContext): string {
  return `
You are the Contact360 AI Assistant — a CRM assistant for ${context.orgName}.

## Your capabilities
- Search and analyse contacts, campaigns, deals
- Rank leads by engagement score
- Draft personalised emails and sequences
- Schedule and manage campaigns
- Answer questions about CRM data

## Critical rules
1. NEVER access or mention data from other organisations
2. NEVER take write actions without showing the user a preview first
3. NEVER hallucinate contact details — only use data from tools
4. If unsure, ask a clarifying question — don't guess
5. Keep responses concise — use bullet points for lists

## Current organisation context
- Org: ${context.orgName}
- Plan: ${context.plan}
- Total contacts: ${context.totalContacts}
- Active campaigns: ${context.activeCampaigns}

## Relevant CRM data retrieved
${context.contacts.map(c => `- ${c.name} (${c.email}) — ${c.company}`).join('\n')}

Today is ${new Date().toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata' })} IST.
`.trim();
}
```


---

# 9. Observability

```typescript
// Every AI interaction is traced end-to-end
const trace = langfuse.trace({
  name:     'ai-agent-query',
  userId:   userId,
  metadata: { orgId, intent },
});

// Per-LLM-call span
const span = trace.span({
  name:  'call_model',
  input: { messages: truncate(messages) },
});

// Log token usage + cost per call
span.end({
  output:   response.content,
  usage:    { promptTokens, completionTokens, totalCost },
  metadata: { model: 'gpt-4o', latencyMs },
});
```

**Key AI metrics tracked:**

- Query latency (p50 / p95 / p99)
- Token cost per org per day
- Tool call success/failure rate
- Approval accept vs. reject rate
- Hallucination detection (fact-checking against retrieved context)

```

***

# 📄 `database-schema.md`

```markdown
# Contact360 — Database Schema

> **Engine:** PostgreSQL 16 · pgvector 0.7 · Row-Level Security enabled
> Version 1.0 · April 2026

---

## Entity Relationship Overview

```

organizations ──< users
organizations ──< contacts ──< contact_activities
organizations ──< companies ──< contacts
organizations ──< campaigns ──< campaign_events
contacts ──< deals ──< deal_activities
contacts ──< enrichment_results
contacts ──< contact_embeddings (pgvector)
campaigns ──< campaign_contacts
users ──< audit_logs

```

---

## Core Tables

### organizations

```sql
CREATE TABLE organizations (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT        NOT NULL,
  slug          TEXT        NOT NULL UNIQUE,
  plan          TEXT        NOT NULL DEFAULT 'trial'
                            CHECK (plan IN ('trial','starter','pro','enterprise')),
  credits       INTEGER     NOT NULL DEFAULT 500,
  settings      JSONB       NOT NULL DEFAULT '{}',
  -- Billing
  stripe_id     TEXT,
  trial_ends_at TIMESTAMPTZ,
  -- Metadata
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```


---

### users

```sql
CREATE TABLE users (
  id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id           UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  email            TEXT        NOT NULL,
  name             TEXT        NOT NULL,
  avatar_url       TEXT,
  password_hash    TEXT,        -- NULL if OAuth-only
  roles            TEXT[]      NOT NULL DEFAULT '{"user"}',
  email_verified   BOOLEAN     NOT NULL DEFAULT FALSE,
  mfa_enabled      BOOLEAN     NOT NULL DEFAULT FALSE,
  mfa_secret       TEXT,        -- AES-256 encrypted
  last_login_at    TIMESTAMPTZ,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE (org_id, email)
);

CREATE INDEX idx_users_org     ON users (org_id);
CREATE INDEX idx_users_email   ON users (email);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY users_org_isolation ON users
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### contacts

```sql
CREATE TABLE contacts (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id          UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  owner_id        UUID        REFERENCES users(id) ON DELETE SET NULL,

  -- Identity
  first_name      TEXT,
  last_name       TEXT,
  email           TEXT,
  email_raw       TEXT,        -- AES-256-GCM encrypted
  email_status    TEXT        CHECK (email_status IN ('valid','risky','invalid','unknown','unvalidated')),
  email_confidence INTEGER,    -- 0–100
  phone           TEXT,        -- E.164, plaintext
  phone_raw       TEXT,        -- AES-256-GCM encrypted (provider response)
  phone_dnd       BOOLEAN     NOT NULL DEFAULT FALSE,

  -- Professional
  job_title       TEXT,
  department      TEXT,
  company_id      UUID        REFERENCES companies(id) ON DELETE SET NULL,
  company_name    TEXT,        -- Denormalised for speed
  linkedin_url    TEXT,
  twitter_url     TEXT,
  website         TEXT,

  -- CRM
  lead_score      INTEGER     NOT NULL DEFAULT 0,
  status          TEXT        NOT NULL DEFAULT 'lead'
                              CHECK (status IN ('lead','prospect','customer','churned')),
  source          TEXT,
  tags            TEXT[]      NOT NULL DEFAULT '{}',
  custom_fields   JSONB       NOT NULL DEFAULT '{}',

  -- Enrichment
  enriched_at     TIMESTAMPTZ,
  enrichment_score INTEGER    DEFAULT 0,  -- 0–100 profile completeness

  -- Compliance
  unsubscribed    BOOLEAN     NOT NULL DEFAULT FALSE,
  unsubscribed_at TIMESTAMPTZ,
  gdpr_consent    BOOLEAN     NOT NULL DEFAULT FALSE,
  ccpa_opt_out    BOOLEAN     NOT NULL DEFAULT FALSE,

  -- Audit
  created_by      UUID        REFERENCES users(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ  -- soft delete

);

-- Indexes
CREATE INDEX idx_contacts_org         ON contacts (org_id);
CREATE INDEX idx_contacts_email       ON contacts (org_id, email) WHERE email IS NOT NULL;
CREATE INDEX idx_contacts_company     ON contacts (company_id) WHERE company_id IS NOT NULL;
CREATE INDEX idx_contacts_tags        ON contacts USING GIN (tags);
CREATE INDEX idx_contacts_custom      ON contacts USING GIN (custom_fields);
CREATE INDEX idx_contacts_lead_score  ON contacts (org_id, lead_score DESC);
CREATE INDEX idx_contacts_status      ON contacts (org_id, status);
CREATE INDEX idx_contacts_not_deleted ON contacts (org_id) WHERE deleted_at IS NULL;

-- RLS
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts FORCE ROW LEVEL SECURITY;
CREATE POLICY contacts_org_isolation ON contacts
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### companies

```sql
CREATE TABLE companies (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id        UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name          TEXT        NOT NULL,
  domain        TEXT,
  industry      TEXT,
  size_range    TEXT        CHECK (size_range IN ('1-10','11-50','51-200','201-1000','1000+')),
  country       CHAR(2),     -- ISO 3166 alpha-2
  city          TEXT,
  website       TEXT,
  linkedin_url  TEXT,
  tags          TEXT[]      NOT NULL DEFAULT '{}',
  custom_fields JSONB       NOT NULL DEFAULT '{}',
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_companies_domain ON companies (org_id, domain) WHERE domain IS NOT NULL;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
CREATE POLICY companies_org_isolation ON companies
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### deals

```sql
CREATE TABLE deals (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id        UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  contact_id    UUID        NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  company_id    UUID        REFERENCES companies(id) ON DELETE SET NULL,
  owner_id      UUID        REFERENCES users(id) ON DELETE SET NULL,

  title         TEXT        NOT NULL,
  value         NUMERIC(14,2),
  currency      CHAR(3)     NOT NULL DEFAULT 'INR',
  stage         TEXT        NOT NULL DEFAULT 'lead'
                            CHECK (stage IN ('lead','qualified','proposal','negotiation','won','lost')),
  probability   INTEGER     CHECK (probability BETWEEN 0 AND 100),
  expected_close DATE,
  closed_at     TIMESTAMPTZ,

  notes         TEXT,
  tags          TEXT[]      NOT NULL DEFAULT '{}',
  custom_fields JSONB       NOT NULL DEFAULT '{}',

  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_deals_org     ON deals (org_id, stage);
CREATE INDEX idx_deals_contact ON deals (contact_id);
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
CREATE POLICY deals_org_isolation ON deals
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### campaigns

```sql
CREATE TABLE campaigns (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id          UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  created_by      UUID        REFERENCES users(id),

  name            TEXT        NOT NULL,
  channel         TEXT        NOT NULL CHECK (channel IN ('email','sms','linkedin','whatsapp')),
  status          TEXT        NOT NULL DEFAULT 'draft'
                              CHECK (status IN ('draft','scheduled','sending','sent','paused','cancelled')),
  goal            TEXT,

  -- Audience
  audience_filter JSONB       NOT NULL DEFAULT '{}',
  audience_count  INTEGER,

  -- Template
  subject         TEXT,
  preview_text    TEXT,
  body_html       TEXT,
  body_text       TEXT,
  template_vars   JSONB       NOT NULL DEFAULT '{}',

  -- Scheduling
  scheduled_at    TIMESTAMPTZ,
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ,
  send_rate       INTEGER     DEFAULT 50,  -- emails per hour

  -- Analytics (denormalised for fast reads)
  stats           JSONB       NOT NULL DEFAULT '{
    "sent": 0, "delivered": 0, "opened": 0, "clicked": 0,
    "replied": 0, "bounced": 0, "unsubscribed": 0, "spam": 0
  }',

  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_campaigns_org    ON campaigns (org_id, status);
CREATE INDEX idx_campaigns_sched  ON campaigns (scheduled_at) WHERE status = 'scheduled';
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
CREATE POLICY campaigns_org_isolation ON campaigns
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### campaign_events

```sql
CREATE TABLE campaign_events (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID        NOT NULL,
  campaign_id  UUID        NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  contact_id   UUID        REFERENCES contacts(id) ON DELETE SET NULL,
  event        TEXT        NOT NULL
               CHECK (event IN ('sent','delivered','opened','clicked','replied','bounced','unsubscribed','spam')),
  link_url     TEXT,        -- for click events
  ip_address   INET,
  user_agent   TEXT,
  metadata     JSONB       NOT NULL DEFAULT '{}',
  occurred_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (occurred_at);

-- Monthly partitions
CREATE TABLE campaign_events_2026_04 PARTITION OF campaign_events
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

CREATE INDEX idx_campaign_events_campaign ON campaign_events (campaign_id, event);
CREATE INDEX idx_campaign_events_contact  ON campaign_events (contact_id);
ALTER TABLE campaign_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY campaign_events_org_isolation ON campaign_events
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### enrichment_results

```sql
CREATE TABLE enrichment_results (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id        UUID        NOT NULL,
  contact_id    UUID        NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  type          TEXT        NOT NULL CHECK (type IN ('email','phone','profile','company')),
  provider      TEXT        NOT NULL,  -- 'hunter', 'apollo', 'internal'
  result        JSONB       NOT NULL DEFAULT '{}',  -- AES-256 encrypted via app layer
  confidence    INTEGER,    -- 0–100
  credits_used  NUMERIC(6,2),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_enrichment_contact ON enrichment_results (contact_id);
ALTER TABLE enrichment_results ENABLE ROW LEVEL SECURITY;
CREATE POLICY enrichment_org_isolation ON enrichment_results
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### contact_embeddings (pgvector)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE contact_embeddings (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id      UUID        NOT NULL,
  contact_id  UUID        NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  type        TEXT        NOT NULL,   -- 'profile' | 'activity_summary' | 'notes'
  content     TEXT        NOT NULL,   -- source text that was embedded
  embedding   vector(1536) NOT NULL,  -- OpenAI text-embedding-3-small
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- HNSW index for fast ANN search
CREATE INDEX idx_embeddings_hnsw ON contact_embeddings
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_embeddings_org ON contact_embeddings (org_id);
ALTER TABLE contact_embeddings ENABLE ROW LEVEL SECURITY;
CREATE POLICY embeddings_org_isolation ON contact_embeddings
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### api_keys

```sql
CREATE TABLE api_keys (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  created_by   UUID        REFERENCES users(id),
  name         TEXT        NOT NULL,
  key_hash     TEXT        NOT NULL,   -- bcrypt hash of raw key
  key_preview  TEXT        NOT NULL,   -- first 16 chars + '...'
  environment  TEXT        NOT NULL DEFAULT 'live' CHECK (environment IN ('live','test')),
  scopes       TEXT[]      NOT NULL DEFAULT '{}',
  ip_allowlist INET[],
  last_used_at TIMESTAMPTZ,
  expires_at   TIMESTAMPTZ,
  revoked_at   TIMESTAMPTZ,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_api_keys_org ON api_keys (org_id) WHERE revoked_at IS NULL;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY api_keys_org_isolation ON api_keys
  USING (org_id = current_setting('app.current_org_id')::uuid);
```


---

### audit_logs

```sql
CREATE TABLE audit_logs (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID        NOT NULL REFERENCES organizations(id),
  user_id      UUID        REFERENCES users(id),
  api_key_id   UUID        REFERENCES api_keys(id),
  action       TEXT        NOT NULL,
  resource     TEXT,
  resource_id  TEXT,
  ip_address   INET,
  user_agent   TEXT,
  request_id   UUID,
  severity     TEXT        NOT NULL DEFAULT 'info'
               CHECK (severity IN ('info','warning','high','critical')),
  metadata     JSONB       NOT NULL DEFAULT '{}',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Append-only enforcement
CREATE RULE audit_no_update AS ON UPDATE TO audit_logs DO INSTEAD NOTHING;
CREATE RULE audit_no_delete AS ON DELETE TO audit_logs DO INSTEAD NOTHING;

CREATE INDEX idx_audit_org     ON audit_logs (org_id, created_at DESC);
CREATE INDEX idx_audit_user    ON audit_logs (user_id, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs (resource, resource_id);
```


---

## Database Triggers

```sql
-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER contacts_updated_at  BEFORE UPDATE ON contacts  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER users_updated_at     BEFORE UPDATE ON users     FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER deals_updated_at     BEFORE UPDATE ON deals     FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Increment campaign stats on new event
CREATE OR REPLACE FUNCTION update_campaign_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE campaigns
  SET stats = jsonb_set(
    stats,
    ARRAY[NEW.event],
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

```

***

# 📄 `event-driven.md`

```markdown
# Contact360 — Event-Driven Architecture

> **Broker:** Apache Kafka (MSK) · Redis Pub/Sub for real-time
> Version 1.0 · April 2026

---

## Topic Structure

```

contact360.contacts.created          → Enrichment, Search Sync, AI Memory
contact360.contacts.updated          → Search Sync, Lead Score Recalc
contact360.contacts.deleted          → Search Cleanup, Embedding Delete

contact360.emails.validated          → Contact Status Update, Campaign Guard
contact360.emails.enriched           → Contact Update, Notification
contact360.phones.enriched           → Contact Update, DND Check

contact360.campaigns.scheduled       → Campaign Scheduler (cron trigger)
contact360.campaigns.sending         → Email/SMS Worker, Rate Limiter
contact360.campaigns.sent            → Analytics Aggregation, Notification

contact360.campaign-events.delivered → Stats Update, Activity Feed
contact360.campaign-events.opened    → Stats Update, Lead Score Boost
contact360.campaign-events.clicked   → Stats Update, Lead Score Boost
contact360.campaign-events.replied   → CRM Activity, Follow-up Stop, AI Alert
contact360.campaign-events.bounced   → Contact Bounce Mark, Alert if > 5%
contact360.campaign-events.spam      → Immediate Unsubscribe, Alert if > 0.1%

contact360.ai.action-approved        → AI Tool Executor
contact360.ai.action-completed       → Audit Log, Notification

contact360.billing.plan-upgraded     → Credit Top-up, Feature Unlock
contact360.billing.trial-expiring    → Notification Service (D-3, D-1)

```

---

## Kafka Configuration

```typescript
// packages/shared-kafka/src/kafka.config.ts
export const kafkaConfig: KafkaConfig = {
  clientId: 'contact360-service',
  brokers:  process.env.KAFKA_BROKERS?.split(',') ?? [],
  ssl: {
    ca:   [fs.readFileSync('/certs/ca.pem')],
    cert: fs.readFileSync('/certs/client.pem'),
    key:  fs.readFileSync('/certs/client.key'),
  },
  sasl: {
    mechanism: 'scram-sha-512',
    username:  process.env.KAFKA_USERNAME!,
    password:  process.env.KAFKA_PASSWORD!,
  },
  retry: { initialRetryTime: 100, retries: 10 },
};

// Topic configuration
export const topicConfig = {
  'contact360.contacts.created': {
    numPartitions:     6,
    replicationFactor: 3,
    retention:         '7d',
  },
  'contact360.campaigns.sending': {
    numPartitions:     12,  // Higher partitions for throughput
    replicationFactor: 3,
    retention:         '3d',
  },
  'contact360.campaign-events.*': {
    numPartitions:     12,
    replicationFactor: 3,
    retention:         '30d',
  },
};
```


---

## Event Schemas

```typescript
// packages/shared-events/src/schemas/contact.events.ts

export interface ContactCreatedEvent {
  eventId:    string;    // UUID for idempotency
  eventType:  'contact.created';
  version:    '1.0';
  timestamp:  string;    // ISO 8601
  orgId:      string;
  userId:     string;
  data: {
    contactId:   string;
    name:        string;
    email:       string | null;
    phone:       string | null;
    company:     string | null;
    source:      string;
  };
}

export interface CampaignEventOccurred {
  eventId:    string;
  eventType:  'campaign_event.occurred';
  version:    '1.0';
  timestamp:  string;
  orgId:      string;
  data: {
    campaignId:  string;
    contactId:   string;
    event:       'delivered' | 'opened' | 'clicked' | 'replied' | 'bounced' | 'spam';
    linkUrl:     string | null;
    ipAddress:   string | null;
    metadata:    Record<string, unknown>;
  };
}
```


---

## End-to-End Flow: Contact Created → Enrichment → Campaign

```
1. User uploads CSV
       │
       ▼
2. CRM Service creates contact in PostgreSQL
       │
       ├──▶ Publishes: contact360.contacts.created
       │
       ▼ (consumed by multiple services in parallel)
       │
   ┌───┴──────────────────────────────────────────┐
   │                                              │
   ▼                                              ▼
3a. Enrichment Service                    3b. Search Sync Worker
    ├── Calls Hunter.io API                   ├── Indexes to OpenSearch
    ├── Validates email                        └── Publishes: contact.indexed
    ├── Finds phone (if missing)
    └── Publishes: contact360.emails.enriched
                │
                ▼
4. CRM Service (consumer)
   ├── Updates contact.email_status
   └── Publishes: contact360.contacts.updated
                │
                ▼
5. Campaign Guard checks audience on schedule:
   ├── Reads contacts with email_status = 'valid'
   ├── Excludes unsubscribed / DND
   └── Publishes: contact360.campaigns.sending (per batch)
                │
                ▼
6. Email Worker (consumer, per partition)
   ├── Sends via AWS SES
   ├── Records delivery
   └── Publishes: contact360.campaign-events.delivered
                │
                ▼
7. Analytics Service (consumer)
   ├── Updates campaign.stats JSONB (via DB trigger)
   ├── Updates lead_score on contact
   └── Feeds real-time dashboard via Redis Pub/Sub
```


---

## Dead Letter Queue (DLQ) Handling

```typescript
// packages/shared-kafka/src/dlq.handler.ts
@Injectable()
export class DlqHandler {
  // Failed events go to contact360.{topic}.dlq after 3 retries
  async handleDlqMessage(topic: string, message: KafkaMessage) {
    const failedEvent = JSON.parse(message.value!.toString());

    await this.db.dlqEvent.create({
      data: {
        originalTopic: topic,
        eventId:       failedEvent.eventId,
        payload:       failedEvent,
        errorMessage:  message.headers?.['error-message']?.toString(),
        failedAt:      new Date(),
        retryCount:    parseInt(message.headers?.['retry-count']?.toString() ?? '0'),
      },
    });

    // Alert on DLQ spike (> 10 events in 5 min)
    const recentCount = await this.db.dlqEvent.count({
      where: {
        originalTopic: topic,
        failedAt: { gte: new Date(Date.now() - 5 * 60_000) },
      },
    });

    if (recentCount > 10) {
      await this.alerts.triggerP2(`DLQ spike on ${topic}: ${recentCount} events`);
    }
  }

  // Retry DLQ events manually (via admin UI or scheduled job)
  async replayDlqEvent(dlqEventId: string) {
    const event = await this.db.dlqEvent.findUniqueOrThrow({
      where: { id: dlqEventId }
    });

    await this.kafka.produce(event.originalTopic, event.payload);
    await this.db.dlqEvent.update({
      where: { id: dlqEventId },
      data:  { replayedAt: new Date() },
    });
  }
}
```


---

## Redis Pub/Sub — Real-Time Layer

```typescript
// Used for: live campaign dashboard, AI approval WebSocket, activity feed

// Publisher (Analytics Service)
await redis.publish(
  `contact360:realtime:org:${orgId}:campaign:${campaignId}`,
  JSON.stringify({
    event:    'stats_update',
    stats:    { sent: 500, opened: 160, clicked: 52 },
    openRate: 32.0,
  })
);

// Subscriber (API Gateway → WebSocket → Browser)
redis.subscribe(`contact360:realtime:org:${orgId}:*`, (message, channel) => {
  const parsed = JSON.parse(message);
  wsServer.to(`org:${orgId}`).emit('realtime_update', parsed);
});
```


---

## Idempotency

```typescript
// Every Kafka consumer is idempotent using eventId deduplication

async function processContactCreated(event: ContactCreatedEvent) {
  // Check if already processed
  const alreadyProcessed = await redis.set(
    `contact360:processed:${event.eventId}`,
    '1',
    'EX', 86400,  // 24h TTL
    'NX'          // Only set if NOT exists
  );

  if (!alreadyProcessed) {
    logger.info(`Skipping duplicate event: ${event.eventId}`);
    return;
  }

  // Safe to process — guaranteed exactly-once
  await enrichmentService.enrich(event.data.contactId);
}
```


---

## Consumer Group Strategy

| Consumer Group | Topics | Instances | Parallelism |
| :-- | :-- | :-- | :-- |
| `enrichment-workers` | `contacts.created`, `contacts.updated` | 3 | 6 partitions |
| `search-sync-workers` | `contacts.*`, `campaigns.*` | 2 | 6 partitions |
| `email-workers` | `campaigns.sending` | 5 | 12 partitions |
| `analytics-workers` | `campaign-events.*` | 3 | 12 partitions |
| `ai-memory-workers` | `contacts.*`, `campaign-events.*` | 2 | 6 partitions |
| `notification-workers` | `billing.*`, `campaigns.sent` | 1 | 3 partitions |

```

***

# 📄 `extension.md`

```markdown
# Contact360 — Chrome Extension

> **Platform:** Chrome Manifest V3 · TypeScript · React popup
> Version 1.0 · April 2026

---

## Architecture Overview

```

┌─────────────────────────────────────────────────────────────────┐
│                    CHROME EXTENSION                             │
│                                                                 │
│  ┌────────────────┐   ┌─────────────────┐   ┌───────────────┐ │
│  │  Content       │   │  Service Worker  │   │  React Popup  │ │
│  │  Script        │   │  (Background)    │   │               │ │
│  │                │   │                 │   │  Contact card  │ │
│  │  - DOM scan    │◄──│  - Auth state   │──►│  Enrich btn   │ │
│  │  - Email detect│   │  - API calls    │   │  Add to CRM   │ │
│  │  - LinkedIn    │   │  - Cache mgmt   │   │  AI summary   │ │
│  │    scraping    │   │  - Rate limit   │   │               │ │
│  └───────┬────────┘   └────────┬────────┘   └───────┬───────┘ │
│          │                     │                    │         │
│          └─────────────────────┴────────────────────┘         │
│                      Chrome Message API                        │
└─────────────────────────────────────────────────────────────────┘
│
▼ HTTPS (JWT Auth)
Contact360 API Gateway

```

---

## Manifest V3 Configuration

```json
{
  "manifest_version": 3,
  "name": "Contact360",
  "version": "1.0.0",
  "description": "AI-powered contact enrichment for your CRM",

  "permissions": [
    "storage",
    "tabs",
    "activeTab",
    "scripting"
  ],

  "host_permissions": [
    "https://www.linkedin.com/*",
    "https://mail.google.com/*",
    "https://outlook.live.com/*",
    "https://api.contact360.io/*"
  ],

  "background": {
    "service_worker": "background.js",
    "type": "module"
  },

  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16":  "icons/icon-16.png",
      "48":  "icons/icon-48.png",
      "128": "icons/icon-128.png"
    }
  },

  "content_scripts": [
    {
      "matches": ["https://www.linkedin.com/in/*"],
      "js":      ["content-linkedin.js"],
      "run_at":  "document_idle"
    },
    {
      "matches": ["https://mail.google.com/*"],
      "js":      ["content-gmail.js"],
      "run_at":  "document_idle"
    }
  ],

  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  },

  "web_accessible_resources": [
    {
      "resources": ["sidebar.html", "icons/*"],
      "matches":   ["https://www.linkedin.com/*", "https://mail.google.com/*"]
    }
  ]
}
```


---

## Content Script — LinkedIn Profile Scraper

```typescript
// src/content/content-linkedin.ts
class LinkedInProfileScraper {
  private floatingCard: HTMLElement | null = null;

  init() {
    // Watch for URL changes (LinkedIn is SPA)
    this.observeNavigation();
    if (this.isProfilePage()) this.processProfile();
  }

  private isProfilePage(): boolean {
    return /linkedin\.com\/in\/[^/]+\/?$/.test(window.location.href);
  }

  private observeNavigation() {
    const observer = new MutationObserver(() => {
      if (this.isProfilePage()) this.processProfile();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  private async processProfile() {
    await this.waitForElement('[data-view-name="profile-card"]');

    const profile = this.extractProfileData();
    if (!profile.name) return;

    // Check CRM for existing contact
    const crmData = await chrome.runtime.sendMessage({
      type:    'LOOKUP_CONTACT',
      payload: { linkedinUrl: window.location.href, email: profile.email },
    });

    this.injectFloatingCard(profile, crmData);
  }

  private extractProfileData(): LinkedInProfile {
    const getText = (selector: string) =>
      document.querySelector(selector)?.textContent?.trim() ?? null;

    // Extract visible emails from About section
    const aboutText = getText('.pv-about-section') ?? '';
    const emailMatch = aboutText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);

    return {
      name:        getText('h1.text-heading-xlarge'),
      headline:    getText('.text-body-medium.break-words'),
      company:     getText('[data-field="experience_company_logo"] .t-bold')
                     ?? getText('.pv-text-details__right-panel-item-text'),
      location:    getText('.text-body-small.inline.t-black--light.break-words'),
      linkedinUrl: window.location.href,
      email:       emailMatch?. ?? null,
      avatarUrl:   (document.querySelector('.pv-top-card-profile-picture__image') as HTMLImageElement)?.src ?? null,
    };
  }

  private injectFloatingCard(profile: LinkedInProfile, crmData: ContactLookupResult) {
    this.floatingCard?.remove();

    const card = document.createElement('div');
    card.id = 'contact360-card';
    card.innerHTML = this.renderCard(profile, crmData);
    document.body.appendChild(card);

    this.floatingCard = card;
    this.attachCardEvents(card, profile);
  }

  private renderCard(profile: LinkedInProfile, crm: ContactLookupResult): string {
    const inCRM = !!crm?.contactId;

    return `
      <div class="c360-card">
        <div class="c360-header">
          <img src="${profile.avatarUrl ?? '/icons/avatar-placeholder.png'}"
               class="c360-avatar" alt="${profile.name}" />
          <div class="c360-info">
            ```
            <div class="c360-name">${profile.name}</div>
            ```
            ```
            <div class="c360-title">${profile.headline ?? ''}</div>
            ```
            ```
            <div class="c360-company">${profile.company ?? ''}</div>
            ```
          </div>
        </div>

        <div class="c360-status">
          ${inCRM
            ```
            ? `<span class="c360-badge c360-badge--in-crm">✓ In CRM</span>`
            ```
            ```
            : `<span class="c360-badge c360-badge--new">New contact</span>`
            ```
          }
        </div>

        <div class="c360-actions">
          ${inCRM ? `
            <button class="c360-btn c360-btn--secondary" data-action="view">
              View in CRM →
            </button>
          ` : `
            <button class="c360-btn c360-btn--primary" data-action="add">
              + Add to Contact360
            </button>
          `}
          <button class="c360-btn c360-btn--ghost" data-action="enrich">
            🔍 Find Email
          </button>
          <button class="c360-btn c360-btn--ghost" data-action="ai-summary">
            🤖 AI Summary
          </button>
        </div>
      </div>
    `;
  }

  private attachCardEvents(card: HTMLElement, profile: LinkedInProfile) {
    card.addEventListener('click', async (e) => {
      const action = (e.target as HTMLElement).dataset.action;
      if (!action) return;

      switch (action) {
        case 'add':
          await this.addToCRM(profile);
          break;
        case 'enrich':
          await this.enrichContact(profile);
          break;
        case 'ai-summary':
          await this.getAISummary(profile);
          break;
        case 'view':
          chrome.runtime.sendMessage({ type: 'OPEN_CRM_TAB', payload: { contactId: profile.linkedinUrl } });
          break;
      }
    });
  }

  private async addToCRM(profile: LinkedInProfile) {
    const btn = this.floatingCard?.querySelector('[data-action="add"]') as HTMLButtonElement;
    if (btn) { btn.textContent = 'Adding...'; btn.disabled = true; }

    const result = await chrome.runtime.sendMessage({
      type:    'ADD_CONTACT',
      payload: profile,
    });

    if (result.success) {
      btn.textContent    = '✓ Added!';
      btn.className      = 'c360-btn c360-btn--success';
    } else {
      btn.textContent    = 'Failed — retry';
      btn.disabled       = false;
    }
  }
}

const scraper = new LinkedInProfileScraper();
scraper.init();
```


---

## Service Worker — Background Script

```typescript
// src/background/background.ts
import { AuthManager } from './auth.manager';
import { ApiClient } from './api.client';
import { CacheManager } from './cache.manager';

const auth  = new AuthManager();
const api   = new ApiClient();
const cache = new CacheManager();

// Handle messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender).then(sendResponse);
  return true;  // Keep message channel open for async response
});

async function handleMessage(message: ExtensionMessage, sender: chrome.runtime.MessageSender) {
  const token = await auth.getValidToken();
  if (!token && message.type !== 'AUTH_LOGIN') {
    return { success: false, error: 'Not authenticated' };
  }

  switch (message.type) {
    case 'LOOKUP_CONTACT': {
      const cacheKey = `lookup:${message.payload.linkedinUrl}`;
      const cached = await cache.get(cacheKey);
      if (cached) return cached;

      const result = await api.get('/contacts/lookup', {
        params: message.payload,
        token,
      });

      await cache.set(cacheKey, result, 300);  // 5-min cache
      return result;
    }

    case 'ADD_CONTACT': {
      return api.post('/contacts', message.payload, token);
    }

    case 'ENRICH_CONTACT': {
      return api.post('/email/find', {
        name:       message.payload.name,
        company:    message.payload.company,
        linkedinUrl: message.payload.linkedinUrl,
      }, token);
    }

    case 'AI_SUMMARY': {
      return api.post('/ai/query', {
        query: `Give me a brief profile summary for ${message.payload.name} at ${message.payload.company}`,
      }, token);
    }

    case 'OPEN_CRM_TAB': {
      chrome.tabs.create({
        url: `https://app.contact360.io/contacts?linkedin=${encodeURIComponent(message.payload.linkedinUrl)}`
      });
      return { success: true };
    }
  }
}
```


---

## Auth Manager — OAuth Flow in Extension

```typescript
// src/background/auth.manager.ts
export class AuthManager {
  private tokenCache: { accessToken: string; expiresAt: number } | null = null;

  async getValidToken(): Promise<string | null> {
    // Return cached token if still valid
    if (this.tokenCache && Date.now() < this.tokenCache.expiresAt - 60_000) {
      return this.tokenCache.accessToken;
    }

    // Try refresh token from chrome.storage.local
    const stored = await chrome.storage.local.get(['refreshToken']);
    if (!stored.refreshToken) return null;

    try {
      const response = await fetch('https://api.contact360.io/v1/auth/refresh', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ refreshToken: stored.refreshToken }),
      });

      if (!response.ok) {
        await chrome.storage.local.remove(['refreshToken']);
        return null;
      }

      const { data } = await response.json();
      this.tokenCache = {
        accessToken: data.accessToken,
        expiresAt:   Date.now() + data.expiresIn * 1000,
      };

      // Rotate refresh token
      await chrome.storage.local.set({ refreshToken: data.refreshToken });

      return data.accessToken;
    } catch {
      return null;
    }
  }

  async login(): Promise<boolean> {
    // Use chrome.identity API for OAuth flow
    const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
    authUrl.searchParams.set('client_id', GOOGLE_CLIENT_ID);
    authUrl.searchParams.set('redirect_uri', chrome.identity.getRedirectURL());
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('scope', 'openid email profile');
    authUrl.searchParams.set('access_type', 'offline');

    return new Promise((resolve) => {
      chrome.identity.launchWebAuthFlow(
        { url: authUrl.toString(), interactive: true },
        async (redirectUrl) => {
          if (!redirectUrl) return resolve(false);

          const code = new URL(redirectUrl).searchParams.get('code');
          if (!code) return resolve(false);

          const response = await fetch('https://api.contact360.io/v1/auth/oauth/google/extension', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ code, redirectUri: chrome.identity.getRedirectURL() }),
          });

          const { data } = await response.json();
          await chrome.storage.local.set({ refreshToken: data.refreshToken });
          this.tokenCache = {
            accessToken: data.accessToken,
            expiresAt:   Date.now() + data.expiresIn * 1000,
          };

          resolve(true);
        }
      );
    });
  }
}
```


---

## Popup — React Component

```typescript
// src/popup/App.tsx
import React, { useEffect, useState } from 'react';

export function App() {
  const [auth, setAuth]     = useState<'loading' | 'logged-in' | 'logged-out'>('loading');
  const [contact, setContact] = useState<ContactPreview | null>(null);

  useEffect(() => {
    // Check auth state
    chrome.runtime.sendMessage({ type: 'CHECK_AUTH' }, (res) => {
      setAuth(res.authenticated ? 'logged-in' : 'logged-out');
    });

    // Get contact from current active tab
    chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
      if (tab?.url?.includes('linkedin.com/in/')) {
        chrome.runtime.sendMessage(
          { type: 'LOOKUP_CONTACT', payload: { linkedinUrl: tab.url } },
          (res) => setContact(res?.data ?? null)
        );
      }
    });
  }, []);

  if (auth === 'loading') return <LoadingScreen />;
  if (auth === 'logged-out') return <LoginScreen onLogin={() => setAuth('logged-in')} />;

  return (
    <div className="popup-container">
      <Header />
      {contact ? (
        <ContactCard contact={contact} />
      ) : (
        <EmptyState message="Navigate to a LinkedIn profile to see contact details" />
      )}
      <QuickActions />
    </div>
  );
}
```


---

## Gmail Integration — Email Detection

```typescript
// src/content/content-gmail.ts
class GmailContactDetector {
  init() {
    this.observeEmailOpen();
  }

  private observeEmailOpen() {
    const observer = new MutationObserver(() => {
      const emailHeaders = document.querySelectorAll('[data-message-id]');
      emailHeaders.forEach(header => {
        if (!header.dataset.c360Processed) {
          header.dataset.c360Processed = 'true';
          this.processEmailSender(header);
        }
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  private async processEmailSender(header: Element) {
    const senderEl = header.querySelector('[email]');
    if (!senderEl) return;

    const email   = senderEl.getAttribute('email');
    const name    = senderEl.getAttribute('name');

    if (!email) return;

    const crmData = await chrome.runtime.sendMessage({
      type:    'LOOKUP_CONTACT',
      payload: { email },
    });

    this.injectCRMBadge(senderEl, name, email, crmData);
  }

  private injectCRMBadge(
    el: Element,
    name: string | null,
    email: string,
    crm: ContactLookupResult
  ) {
    const badge = document.createElement('span');
    badge.className = 'c360-gmail-badge';

    if (crm?.contactId) {
      ```
      badge.innerHTML = `<span class="c360-dot c360-dot--green" title="In Contact360 CRM"></span>`;
      ```
      badge.title = `${crm.contactName} — ${crm.company ?? email}`;
    } else {
      ```
      badge.innerHTML = `<span class="c360-dot c360-dot--gray" title="Not in CRM"></span>`;
      ```
      badge.addEventListener('click', () => {
        chrome.runtime.sendMessage({
          type:    'ADD_CONTACT',
          payload: { name: name ?? email, email },
        });
      });
    }

    el.appendChild(badge);
  }
}

new GmailContactDetector().init();
```


---

## Privacy \& Compliance

```typescript
// The extension ONLY collects data that is:
// 1. Publicly visible on the current page
// 2. Explicitly triggered by the user (click "Add to CRM")
// 3. Never collected silently in the background

// What we DO collect (on user action):
//   - Name, headline, company, location (public LinkedIn profile)
//   - Email address (if publicly listed in profile)
//   - Current page URL (LinkedIn profile URL)

// What we NEVER collect:
//   - Private messages or DMs
//   - Connection lists
//   - Analytics data without user action
//   - Data from pages the user hasn't visited

// Storage policy:
//   chrome.storage.local → Only auth tokens (refresh token, encrypted)
//   No PII stored in extension storage — all data lives in Contact360 API

// Permissions justification (required for Chrome Web Store review):
const PERMISSION_JUSTIFICATIONS = {
  'storage':     'Store authentication tokens to keep user logged in',
  'tabs':        'Read current tab URL to detect LinkedIn profiles',
  'activeTab':   'Inject contact card UI on LinkedIn and Gmail',
  'scripting':   'Run content scripts to detect and extract public profile data',
};
```


---

## Build \& Packaging

```bash
# Development build with hot reload
pnpm --filter extension dev

# Production build
pnpm --filter extension build

# Output: apps/extension/dist/
# ├── manifest.json
# ├── background.js
# ├── content-linkedin.js
# ├── content-gmail.js
# ├── popup.html + popup.js
# ├── sidebar.html + sidebar.js
# └── icons/

# Package for Chrome Web Store
cd apps/extension
zip -r contact360-extension-v1.0.0.zip dist/
```

```

***

## All 4 Files — Summary

| File | Size | Key Sections |
|---|---|---|
| `ai-architecture.md` | ~250 lines | LangGraph agent graph, hybrid RAG (RRF fusion), tool registry with safety tiers, HITL WebSocket approval, memory layers, system prompt template |
| `database-schema.md` | ~350 lines | Full DDL for 10 tables, RLS policies on every table, pgvector HNSW index, triggers for `updated_at` + campaign stats, all indexes |
| `event-driven.md` | ~300 lines | 20 Kafka topics, event schema types, full end-to-end flow diagram, DLQ handling + alerting, Redis Pub/Sub real-time layer, idempotency pattern |
| `extension.md` | ~400 lines | MV3 manifest, LinkedIn DOM scraper + floating card injection, Service Worker message bus, OAuth via `chrome.identity`, Gmail sender detection, privacy compliance notes |```

