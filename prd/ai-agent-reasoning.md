# Contact360 — AI Agent Internal Reasoning & Implementation

> **Stack:** LangGraph · OpenAI GPT-4o · pgvector RAG · Redis session memory
> **Architecture:** MCP-compatible · Human-in-the-loop · Multi-mode autonomous agent
> Version 1.0 · April 2026

---

## Table of Contents

1. [Agent Mental Model](#1-agent-mental-model)
2. [Step-by-Step Reasoning Flow](#2-step-by-step-reasoning-flow)
3. [Agent Modules Breakdown](#3-agent-modules-breakdown)
4. [Intent Engine](#4-intent-engine)
5. [Planner Engine (Task Decomposer)](#5-planner-engine-task-decomposer)
6. [Tool Registry](#6-tool-registry)
7. [Execution Engine](#7-execution-engine)
8. [Memory Architecture](#8-memory-architecture)
9. [Prompt Engineering Layer](#9-prompt-engineering-layer)
10. [Agent Modes](#10-agent-modes)
11. [Safety & Control Layer](#11-safety--control-layer)
12. [Multi-Step Autonomous Flow](#12-multi-step-autonomous-flow)
13. [Full LangGraph Implementation](#13-full-langgraph-implementation)
14. [Tool Calling Implementation](#14-tool-calling-implementation)
15. [Prompt Templates (All Use-Cases)](#15-prompt-templates-all-use-cases)
16. [Autonomous Campaign AI](#16-autonomous-campaign-ai)
17. [Observability & Cost Control](#17-observability--cost-control)

---

## 1. Agent Mental Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONTACT360 AI AGENT SYSTEM                           │
│                                                                         │
│   User Input (Chat / MCP / Slack / API)                                 │
│         │                                                               │
│         ▼                                                               │
│   ┌─────────────────┐                                                   │
│   │  Context Builder │◄── org data, permissions, session history        │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Intent Classifier│◄── LLM classification + confidence score         │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │  Planner Engine  │◄── Decomposes intent into ordered task steps     │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                    EXECUTION LOOP                           │       │
│   │                                                             │       │
│   │  Tool Selector ──► Tool Executor ──► Result Evaluator       │       │
│   │       ▲                                      │             │       │
│   │       └──────────── retry / replan ──────────┘             │       │
│   └──────────────────────────┬──────────────────────────────────┘       │
│                              │                                          │
│            ┌─────────────────┼──────────────────┐                      │
│            ▼                 ▼                  ▼                       │
│   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐                │
│   │   Memory    │   │    Safety    │   │   Response   │                │
│   │   Update    │   │    Layer     │   │  Generator   │                │
│   └─────────────┘   └──────────────┘   └──────────────┘                │
│                                                │                        │
│                                                ▼                        │
│                                      User (Natural Language)            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Evolution: Traditional CRM → AI Copilot → Autonomous CRM

| Stage | User Action | AI Role |
|-------|-------------|---------|
| **Traditional CRM** | Clicks buttons, fills forms | None |
| **AI Copilot CRM** | Asks questions, reviews suggestions | Recommends, drafts |
| **Autonomous CRM** | States goals, approves actions | Plans, executes, reports |

Contact360 is designed to operate at **all three stages**, escalating automation level based on user trust and action risk.

---

## 2. Step-by-Step Reasoning Flow

### Example: *"Find top 50 CTOs in Bangalore and send them an email campaign"*

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: USER INPUT                                                  │
│ "Find top 50 CTOs in Bangalore and send them an email campaign"    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: CONTEXT BUILDER                                             │
│                                                                     │
│  context = {                                                        │
│    orgId:       "org_abc123",                                       │
│    userId:      "usr_xyz789",                                       │
│    permissions: ["contacts:read", "campaign:write", "email:send"],  │
│    orgPlan:     "PRO",                                              │
│    pastQueries: ["CTO list Mumbai", "Q1 campaign performance"],     │
│    orgStats: {                                                      │
│      totalContacts: 12400,                                          │
│      ctosInBangalore: 387,                                          │
│      validEmailRate: 0.76                                           │
│    }                                                                │
│  }                                                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: INTENT CLASSIFICATION                                       │
│                                                                     │
│  intents = [                                                        │
│    { type: "SEARCH_CONTACTS",   confidence: 0.99 },                 │
│    { type: "FILTER_BY_ROLE",    value: "CTO", confidence: 0.97 },   │
│    { type: "FILTER_BY_LOCATION",value: "Bangalore", conf: 0.95 },  │
│    { type: "CREATE_CAMPAIGN",   confidence: 0.96 },                 │
│    { type: "SEND_EMAIL",        confidence: 0.94 },                 │
│  ]                                                                  │
│  mode: ACTION  (write operations detected → approval required)      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: TASK DECOMPOSITION (PLANNER)                                │
│                                                                     │
│  plan = [                                                           │
│    { step: 1, task: "search_contacts",  tool: "vql.query",          │
│               params: { jobTitle: "CTO", city: "Bangalore" } },    │
│    { step: 2, task: "limit_results",    tool: "crm.filter",         │
│               params: { limit: 50, orderBy: "lead_score DESC" } }, │
│    { step: 3, task: "validate_emails",  tool: "email.validate",     │
│               requiresApproval: false },                            │
│    { step: 4, task: "create_campaign",  tool: "campaign.create",    │
│               requiresApproval: true, riskLevel: "medium" },       │
│    { step: 5, task: "send_campaign",    tool: "campaign.send",      │
│               requiresApproval: true, riskLevel: "high" },         │
│  ]                                                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 5: TOOL SELECTION (maps plan steps → microservices)            │
│                                                                     │
│  Step 1 → Connector Service  (VQL query engine)                     │
│  Step 2 → CRM Service        (filter + sort)                        │
│  Step 3 → Email Service      (bulk validation)                      │
│  Step 4 → Campaign Service   (create draft) ← APPROVAL GATE        │
│  Step 5 → Email Service      (bulk send)    ← APPROVAL GATE        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 6: EXECUTION ENGINE                                            │
│                                                                     │
│  [1] VQL: SELECT * FROM contacts                                    │
│           WHERE job_title ILIKE '%CTO%'                             │
│             AND city = 'Bangalore'                                  │
│           ORDER BY lead_score DESC LIMIT 50                         │
│      → Result: 42 contacts found (< 50, report to user)            │
│                                                                     │
│  [2] Email Validation (bulk, async)                                 │
│      → 38 valid, 4 invalid (1 bounce, 3 disposable)                │
│                                                                     │
│  ⚠️  APPROVAL GATE TRIGGERED                                        │
│     "Create campaign for 38 CTOs in Bangalore? [Approve / Reject]" │
│                                                                     │
│  [3] Campaign Created: "CTO Bangalore Outreach · April 2026"        │
│      campaign_id: cmp_001xyz                                        │
│                                                                     │
│  ⚠️  APPROVAL GATE TRIGGERED                                        │
│     "Send 38 emails now? [Approve / Reject]"                       │
│                                                                     │
│  [4] Emails sent via AWS SES                                        │
│      Delivered: 38, Failed: 0                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 7: MEMORY UPDATE                                               │
│                                                                     │
│  Short-term (Redis):                                                │
│    session_id: "sess_abc" → last query + result context             │
│                                                                     │
│  Long-term (PostgreSQL ai_memories):                                │
│    key: "last_cto_campaign"  → campaign_id: cmp_001xyz              │
│    key: "bangalore_cto_count" → 42                                  │
│                                                                     │
│  Vector (pgvector):                                                 │
│    Embed + store: "CTO Bangalore campaign sent April 2026"          │
│    → enables future: "how did my last CTO campaign do?"            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 8: RESPONSE GENERATION                                         │
│                                                                     │
│  ✅ Campaign "CTO Bangalore Outreach" created and sent.             │
│                                                                     │
│  📊 Summary:                                                        │
│  • Contacts found:   42 (of 50 requested)                           │
│  • Emails validated: 38 valid · 4 invalid (skipped)                 │
│  • Emails sent:      38                                             │
│  • Campaign ID:      cmp_001xyz                                     │
│                                                                     │
│  💡 Tip: Only 42 CTOs found in Bangalore. Want me to also           │
│     search nearby cities (Mysuru, Pune) to reach 50?               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Agent Modules Breakdown

```
AI Agent Service
│
├── IntentEngine         → Classifies user intent with confidence scores
├── PlannerEngine        → Decomposes multi-intent queries into task graphs
├── ToolRegistry         → Catalog of all available tools + permissions
├── ExecutionEngine      → Runs tasks in sequence/parallel, handles retries
├── MemoryEngine         → Short-term (Redis) + long-term (DB) + vector (pgvector)
├── PromptEngine         → Builds system prompts dynamically per context
├── ResponseGenerator    → Formats agent output into natural language
└── SafetyLayer          → Permission checks, rate limits, PII masking, approval gates
```

---

## 4. Intent Engine

```typescript
// apps/ai-agent-service/src/intent/intent.engine.ts

export type IntentType =
  | 'SEARCH_CONTACTS'
  | 'FILTER_BY_ROLE'
  | 'FILTER_BY_LOCATION'
  | 'FILTER_BY_COMPANY'
  | 'ENRICH_CONTACTS'
  | 'VALIDATE_EMAILS'
  | 'CREATE_CAMPAIGN'
  | 'SEND_CAMPAIGN'
  | 'ANALYZE_CAMPAIGN'
  | 'RANK_LEADS'
  | 'IMPORT_CONTACTS'
  | 'EXPORT_CONTACTS'
  | 'SCHEDULE_FOLLOWUP'
  | 'GET_INSIGHTS'
  | 'UNKNOWN';

export interface DetectedIntent {
  type:       IntentType;
  confidence: number;       // 0.0–1.0
  params:     Record<string, unknown>;
  requiresWrite: boolean;
  riskLevel:  'none' | 'low' | 'medium' | 'high';
}

@Injectable()
export class IntentEngine {
  private readonly model = new ChatOpenAI({
    model:       'gpt-4o',
    temperature: 0.0,       // Deterministic for classification
    responseFormat: { type: 'json_object' },
  });

  async classify(query: string, context: AgentContext): Promise<DetectedIntent[]> {
    const prompt = `
Classify the user's CRM query into one or more intents.
Return a JSON array of intents with fields: type, confidence (0-1), params, requiresWrite, riskLevel.

Available intent types: ${INTENT_TYPES.join(', ')}

User query: "${query}"

Org context:
- Total contacts: ${context.orgStats.totalContacts}
- Available channels: ${context.orgStats.channels.join(', ')}

Return only valid JSON, no explanation.
`;

    const response = await this.model.invoke(prompt);
    const parsed = JSON.parse(response.content as string);

    return parsed.intents as DetectedIntent[];
  }

  determineMode(intents: DetectedIntent[]): AgentMode {
    const hasWrite = intents.some(i => i.requiresWrite);
    const hasHighRisk = intents.some(i => i.riskLevel === 'high');
    const isScheduled = intents.some(i => i.type === 'SCHEDULE_FOLLOWUP');

    if (isScheduled) return 'AUTOMATION';
    if (hasWrite)    return 'ACTION';
    return 'READ';
  }
}
```

---

## 5. Planner Engine (Task Decomposer)

```typescript
// apps/ai-agent-service/src/planner/planner.engine.ts

export interface TaskStep {
  id:               string;
  stepNumber:       number;
  description:      string;
  tool:             string;
  params:           Record<string, unknown>;
  dependsOn:        string[];          // step ids this step waits for
  requiresApproval: boolean;
  riskLevel:        'none' | 'low' | 'medium' | 'high';
  canParallelise:   boolean;
  estimatedCredits: number;
}

export interface TaskPlan {
  planId:      string;
  query:       string;
  intents:     DetectedIntent[];
  steps:       TaskStep[];
  totalSteps:  number;
  estimatedDuration: number;  // seconds
  creditsRequired:   number;
  requiresApproval:  boolean;
}

@Injectable()
export class PlannerEngine {
  decompose(query: string, intents: DetectedIntent[], context: AgentContext): TaskPlan {
    const steps: TaskStep[] = [];

    for (const intent of intents) {
      switch (intent.type) {

        case 'SEARCH_CONTACTS':
          steps.push({
            id: 'step_search', stepNumber: 1,
            description: `Search contacts: ${JSON.stringify(intent.params)}`,
            tool: 'vql.query',
            params: this.buildBqlParams(intent.params),
            dependsOn: [],
            requiresApproval: false,
            riskLevel: 'none',
            canParallelise: false,
            estimatedCredits: 0,
          });
          break;

        case 'VALIDATE_EMAILS':
          steps.push({
            id: 'step_validate', stepNumber: steps.length + 1,
            description: 'Validate emails for found contacts',
            tool: 'email.validate',
            params: { contactIds: '{{step_search.result.ids}}' },
            dependsOn: ['step_search'],
            requiresApproval: false,
            riskLevel: 'none',
            canParallelise: true,
            estimatedCredits: 1,   // 1 credit per email
          });
          break;

        case 'CREATE_CAMPAIGN':
          steps.push({
            id: 'step_create_campaign', stepNumber: steps.length + 1,
            description: 'Create email campaign',
            tool: 'campaign.create',
            params: {
              name:      intent.params.campaignName ?? 'AI Generated Campaign',
              contactIds: '{{step_validate.result.validIds}}',
              channel:   'email',
            },
            dependsOn: ['step_validate'],
            requiresApproval: true,
            riskLevel: 'medium',
            canParallelise: false,
            estimatedCredits: 0,
          });
          break;

        case 'SEND_CAMPAIGN':
          steps.push({
            id: 'step_send', stepNumber: steps.length + 1,
            description: 'Send campaign emails',
            tool: 'campaign.send',
            params: { campaignId: '{{step_create_campaign.result.campaignId}}' },
            dependsOn: ['step_create_campaign'],
            requiresApproval: true,
            riskLevel: 'high',
            canParallelise: false,
            estimatedCredits: 0,
          });
          break;
      }
    }

    return {
      planId:            crypto.randomUUID(),
      query,
      intents,
      steps,
      totalSteps:        steps.length,
      estimatedDuration: steps.length * 3,
      creditsRequired:   steps.reduce((acc, s) => acc + s.estimatedCredits, 0),
      requiresApproval:  steps.some(s => s.requiresApproval),
    };
  }

  private buildBqlParams(params: Record<string, unknown>): Record<string, unknown> {
    return {
      filters: {
        jobTitle: params.role,
        city:     params.location,
        company:  params.company,
      },
      limit:   params.limit ?? 50,
      orderBy: 'lead_score DESC',
    };
  }
}
```

---

## 6. Tool Registry

```typescript
// apps/ai-agent-service/src/tools/tool-registry.ts

// ── READ TOOLS (no approval required) ─────────────────────────────────────

export const READ_TOOLS: AgentTool[] = [
  {
    name:        'vql.query',
    description: 'Search and filter contacts using VQL (VQL Query Language). Supports filters by name, email, job title, company, location, tags, lead score.',
    riskLevel:   'none',
    requiresApproval: false,
    schema: z.object({
      filters: z.object({
        jobTitle:    z.string().optional(),
        city:        z.string().optional(),
        country:     z.string().optional(),
        company:     z.string().optional(),
        tags:        z.array(z.string()).optional(),
        leadScoreMin: z.number().optional(),
        status:      z.string().optional(),
      }),
      limit:   z.number().max(500).default(50),
      orderBy: z.string().default('lead_score DESC'),
    }),
    handler: async (params, ctx) => bqlService.query(ctx.orgId, params),
  },

  {
    name:        'crm.search_contacts',
    description: 'Full-text search across contact name, email, company, and notes.',
    riskLevel:   'none',
    requiresApproval: false,
    schema: z.object({
      query: z.string(),
      limit: z.number().max(100).default(10),
    }),
    handler: async (params, ctx) => crmService.search(ctx.orgId, params.query, params.limit),
  },

  {
    name:        'campaign.get_analytics',
    description: 'Get open rate, click rate, reply rate, bounce rate for a campaign or time period.',
    riskLevel:   'none',
    requiresApproval: false,
    schema: z.object({
      campaignId: z.string().optional(),
      period:     z.enum(['7d', '30d', '90d', 'all']).default('30d'),
    }),
    handler: async (params, ctx) => analyticsService.getCampaignStats(ctx.orgId, params),
  },

  {
    name:        'crm.rank_leads',
    description: 'Rank contacts by engagement score to surface top leads.',
    riskLevel:   'none',
    requiresApproval: false,
    schema: z.object({
      limit:  z.number().max(100).default(10),
      listId: z.string().optional(),
    }),
    handler: async (params, ctx) => leadScoringService.rankLeads(ctx.orgId, params),
  },

  {
    name:        'campaign.suggest_subject',
    description: 'Generate 3 alternative subject lines for an email campaign using AI.',
    riskLevel:   'none',
    requiresApproval: false,
    schema: z.object({
      currentSubject: z.string(),
      audienceType:   z.string(),
      campaignGoal:   z.string(),
    }),
    handler: async (params, ctx) => aiCopyService.suggestSubjects(params),
  },
];

// ── WRITE TOOLS (require human approval) ───────────────────────────────────

export const WRITE_TOOLS: AgentTool[] = [
  {
    name:        'email.validate',
    description: 'Validate email addresses for a list of contacts. Returns valid/invalid split.',
    riskLevel:   'low',
    requiresApproval: false,   // Read-ish, no PII modification
    schema: z.object({
      contactIds: z.array(z.string()).max(500),
    }),
    handler: async (params, ctx) => emailService.bulkValidate(ctx.orgId, params.contactIds),
  },

  {
    name:        'campaign.create',
    description: 'Create a new email or SMS campaign draft.',
    riskLevel:   'medium',
    requiresApproval: true,
    schema: z.object({
      name:       z.string(),
      channel:    z.enum(['email', 'sms', 'whatsapp']),
      contactIds: z.array(z.string()),
      templateId: z.string().optional(),
      subject:    z.string().optional(),
      body:       z.string().optional(),
      schedule:   z.object({
        type:   z.enum(['now', 'scheduled']),
        sendAt: z.string().optional(),
      }),
    }),
    handler: async (params, ctx) => campaignService.create(ctx.orgId, ctx.userId, params),
  },

  {
    name:        'campaign.send',
    description: 'Send or schedule a campaign to its target contacts.',
    riskLevel:   'high',
    requiresApproval: true,
    schema: z.object({
      campaignId: z.string(),
    }),
    handler: async (params, ctx) => campaignService.send(ctx.orgId, params.campaignId),
  },

  {
    name:        'crm.update_contact',
    description: 'Update fields on a specific contact.',
    riskLevel:   'medium',
    requiresApproval: true,
    schema: z.object({
      contactId: z.string(),
      updates:   z.record(z.string(), z.any()),
    }),
    handler: async (params, ctx) => crmService.update(ctx.orgId, params.contactId, params.updates),
  },

  {
    name:        'crm.add_to_list',
    description: 'Add a list of contacts to a named segment or list.',
    riskLevel:   'low',
    requiresApproval: true,
    schema: z.object({
      contactIds: z.array(z.string()),
      listName:   z.string(),
    }),
    handler: async (params, ctx) => listsService.addContacts(ctx.orgId, params.listName, params.contactIds),
  },

  {
    name:        'campaign.schedule_followup',
    description: 'Schedule an automated follow-up campaign for non-responders.',
    riskLevel:   'medium',
    requiresApproval: true,
    schema: z.object({
      parentCampaignId: z.string(),
      delayDays:        z.number().min(1).max(30),
      targetEvent:      z.enum(['not_opened', 'not_clicked', 'not_replied']),
      templateId:       z.string(),
    }),
    handler: async (params, ctx) => campaignService.scheduleFollowup(ctx.orgId, params),
  },
];

// ── FORBIDDEN TOOLS (hard-blocked, never callable by AI) ──────────────────

export const FORBIDDEN_TOOLS = [
  'delete_all_contacts',
  'change_org_billing',
  'create_admin_user',
  'export_all_data',
  'revoke_all_api_keys',
  'disable_org',
];
```

---

## 7. Execution Engine

```typescript
// apps/ai-agent-service/src/execution/execution.engine.ts

@Injectable()
export class ExecutionEngine {

  async execute(plan: TaskPlan, context: AgentContext): Promise<ExecutionResult> {
    const results: Record<string, unknown> = {};
    const errors:  Record<string, string>  = {};

    for (const step of plan.steps) {
      // Wait for dependencies
      await this.waitForDependencies(step.dependsOn, results);

      // Resolve template params (e.g. {{step_search.result.ids}})
      const resolvedParams = this.resolveParams(step.params, results);

      // Approval gate for risky actions
      if (step.requiresApproval) {
        const approved = await this.approvalGateway.request(context.userId, {
          stepId:      step.id,
          description: step.description,
          params:      resolvedParams,
          riskLevel:   step.riskLevel,
        });

        if (!approved) {
          errors[step.id] = 'Rejected by user';
          break;
        }
      }

      // Execute tool
      try {
        const tool = this.toolRegistry.get(step.tool);
        const result = await tool.handler(resolvedParams, context);

        results[step.id] = result;

        // Update memory after each step
        await this.memoryEngine.updateShortTerm(context.sessionId, {
          step: step.id,
          result,
        });

      } catch (err) {
        errors[step.id] = err.message;

        // Retry logic (max 2 retries for transient failures)
        const retried = await this.retryStep(step, resolvedParams, context);
        if (retried) {
          results[step.id] = retried;
        } else {
          break;  // Abort remaining steps
        }
      }
    }

    return { planId: plan.planId, results, errors, completedSteps: Object.keys(results).length };
  }

  // Resolves {{step_id.result.field}} template params
  private resolveParams(params: Record<string, unknown>, results: Record<string, unknown>) {
    const str = JSON.stringify(params);
    return JSON.parse(str.replace(/\{\{(\w+)\.result\.(\w+)\}\}/g, (_, stepId, field) => {
      const result = results[stepId] as Record<string, unknown>;
      return JSON.stringify(result?.[field] ?? null);
    }));
  }
}
```

---

## 8. Memory Architecture

```typescript
// apps/ai-agent-service/src/memory/memory.engine.ts

@Injectable()
export class MemoryEngine {

  // ── SHORT-TERM: Redis session memory (TTL: 2 hours) ──────────────────────
  async getShortTermContext(sessionId: string): Promise<SessionContext> {
    const raw = await this.redis.get(`c360:ai:session:${sessionId}`);
    return raw ? JSON.parse(raw) : { messages: [], stepResults: {} };
  }

  async updateShortTerm(sessionId: string, update: Partial<SessionContext>) {
    const current = await this.getShortTermContext(sessionId);
    const merged  = { ...current, ...update };
    await this.redis.set(
      `c360:ai:session:${sessionId}`,
      JSON.stringify(merged),
      'EX', 7200
    );
  }

  // ── LONG-TERM: PostgreSQL ai_memories (org + user scoped) ────────────────
  async getLongTermMemories(orgId: string, userId: string): Promise<AiMemory[]> {
    return this.prisma.aiMemory.findMany({
      where: {
        orgId,
        OR: [{ scope: 'org' }, { scope: 'user', userId }],
        OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }],
      },
      orderBy: { updatedAt: 'desc' },
      take: 20,
    });
  }

  async rememberFact(orgId: string, userId: string, key: string, value: string) {
    return this.prisma.aiMemory.upsert({
      where:  { orgId_scope_key: { orgId, scope: 'user', key } },
      create: { orgId, userId, scope: 'user', key, value },
      update: { value, updatedAt: new Date() },
    });
  }

  // ── VECTOR MEMORY: pgvector semantic search ───────────────────────────────
  async storeQueryEmbedding(orgId: string, query: string, result: unknown) {
    const embedding = await this.embedder.embed(
      `Query: ${query}\nResult: ${JSON.stringify(result).slice(0, 500)}`
    );

    await this.prisma.$executeRaw`
      INSERT INTO contact_embeddings (id, org_id, contact_id, type, content, embedding)
      VALUES (
        gen_random_uuid(), ${orgId}::uuid, NULL,
        'ai_query', ${query},
        ${JSON.stringify(embedding)}::vector
      )
    `;
  }

  async findSimilarPastQueries(orgId: string, query: string, topK = 5) {
    const embedding = await this.embedder.embed(query);

    return this.prisma.$queryRaw`
      SELECT content, metadata,
             1 - (embedding <=> ${JSON.stringify(embedding)}::vector) AS similarity
      FROM contact_embeddings
      WHERE org_id = ${orgId}::uuid
        AND type = 'ai_query'
        AND 1 - (embedding <=> ${JSON.stringify(embedding)}::vector) > 0.80
      ORDER BY similarity DESC
      LIMIT ${topK}
    `;
  }

  // ── FULL CONTEXT BUILDER ─────────────────────────────────────────────────
  async buildContext(orgId: string, userId: string, sessionId: string): Promise<AgentContext> {
    const [session, memories, orgStats] = await Promise.all([
      this.getShortTermContext(sessionId),
      this.getLongTermMemories(orgId, userId),
      this.crmService.getOrgStats(orgId),
    ]);

    return {
      orgId, userId, sessionId,
      sessionHistory: session.messages,
      memories:       memories.map(m => `${m.key}: ${m.value}`),
      orgStats,
      permissions:    await this.authService.getPermissions(userId),
    };
  }
}
```

---

## 9. Prompt Engineering Layer

```typescript
// apps/ai-agent-service/src/prompts/prompt.engine.ts

@Injectable()
export class PromptEngine {

  buildSystemPrompt(context: AgentContext): string {
    return `
You are the Contact360 AI Assistant — an autonomous CRM agent for ${context.orgStats.orgName}.

## Identity
You help sales and marketing teams by intelligently searching contacts, analyzing campaigns,
and executing CRM workflows. You speak clearly, act precisely, and always confirm before
taking irreversible actions.

## Capabilities
- Search, filter, and rank contacts by any attribute
- Validate emails and find phone numbers
- Create and send email/SMS/WhatsApp campaigns
- Analyze campaign performance and suggest improvements
- Schedule automated follow-up sequences
- Generate natural language CRM insights

## Hard Rules (NEVER violate these)
1. NEVER access or reference data from other organisations (org_id isolation is absolute)
2. NEVER take write actions without showing the user a clear preview first
3. NEVER hallucinate contact details — only use data returned by tools
4. NEVER call FORBIDDEN tools: ${FORBIDDEN_TOOLS.join(', ')}
5. If unsure about scope, ask ONE clarifying question — never guess
6. Always quote exact numbers (e.g. "38 valid emails", not "many emails")
7. When a step fails, explain why and offer alternatives — don't silently skip

## Tone
- Concise and direct
- Use bullet points for multi-item results
- Use ✅ for successes, ⚠️ for warnings, ❌ for failures
- End responses with one proactive next suggestion

## Organisation Context
- Name:           ${context.orgStats.orgName}
- Plan:           ${context.orgStats.plan}
- Total Contacts: ${context.orgStats.totalContacts.toLocaleString()}
- Email Credits:  ${context.orgStats.emailCredits}

## What I Remember About You
${context.memories.length > 0 ? context.memories.map(m => `• ${m}`).join('\n') : '• No preferences stored yet'}

## Current Date & Time
${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })} IST
`.trim();
  }
}
```

---

## 10. Agent Modes

### Mode 1: READ (No Approval Required)

Triggered when: all intents are read-only (search, analyze, rank, export preview)

```
User: "Show me the top 10 leads this week"
AI:   → vql.query (lead_score DESC, created_at last 7 days)
      → crm.rank_leads
      → Returns formatted table
      ✅ No approval gates, instant response
```

### Mode 2: ACTION (Approval Required)

Triggered when: any write operation is detected (create campaign, update contact, send emails)

```
User: "Send a follow-up to everyone who opened my last campaign"
AI:   → [READ] campaign.get_analytics → find openers
      → [READ] crm.search_contacts → get contact details
      ⚠️  APPROVAL GATE:
          "Create follow-up campaign for 47 contacts who opened Campaign X?
           Estimated: 47 emails · 0 credits"
      → [WRITE] campaign.create (on approval)
      ⚠️  APPROVAL GATE: "Send 47 emails now?"
      → [WRITE] campaign.send (on approval)
```

### Mode 3: AUTOMATION (Scheduled / Recurring)

Triggered when: recurring or time-based workflows are requested

```
User: "Every Monday, email contacts who haven't been touched in 14 days"
AI:   → Builds a recurring workflow definition
      ⚠️  APPROVAL GATE: "Schedule weekly automation? Runs every Monday 9AM IST"
      → Stores in automation_rules table
      → Redis cron triggers execution each Monday
      → Agent runs READ → ACTION flow each cycle
      → Sends weekly report to user
```

---

## 11. Safety & Control Layer

```typescript
// apps/ai-agent-service/src/safety/safety.layer.ts

@Injectable()
export class SafetyLayer {

  // 1. Permission check — can this user call this tool?
  checkPermission(userId: string, tool: string, context: AgentContext): void {
    const required = TOOL_PERMISSIONS[tool];
    const userPerms = context.permissions;

    if (required && !userPerms.includes(required)) {
      throw new ForbiddenException(
        `You don't have permission to use "${tool}". Required: ${required}`
      );
    }
  }

  // 2. Hard-blocked tools — AI can never call these regardless of prompt
  checkNotForbidden(tool: string): void {
    if (FORBIDDEN_TOOLS.includes(tool)) {
      throw new BadRequestException(
        `Tool "${tool}" is not available to the AI agent.`
      );
    }
  }

  // 3. Rate limiting — per org, per tool
  async checkRateLimit(orgId: string, tool: string): Promise<void> {
    const key    = `c360:ratelimit:${orgId}:${tool}`;
    const limit  = TOOL_RATE_LIMITS[tool] ?? 60;
    const count  = await this.redis.incr(key);

    if (count === 1) await this.redis.expire(key, 60);
    if (count > limit) {
      throw new TooManyRequestsException(
        `Rate limit reached for "${tool}" (${limit}/min)`
      );
    }
  }

  // 4. PII masking — scrub sensitive fields from AI context
  maskPII(data: unknown): unknown {
    const str = JSON.stringify(data);
    return JSON.parse(
      str
        .replace(/"password_hash":"[^"]+"/g, '"password_hash":"[REDACTED]"')
        .replace(/"mfa_secret":"[^"]+"/g, '"mfa_secret":"[REDACTED]"')
        .replace(/"api_key[^"]*":"[^"]+"/gi, (m) => m.replace(/"[^"]+$/, '"[REDACTED]"'))
    );
  }

  // 5. Credit check — ensure org has credits before enrichment
  async checkCredits(orgId: string, requiredCredits: number): Promise<void> {
    const org = await this.prisma.organization.findUnique({ where: { id: orgId } });
    if ((org?.credits ?? 0) < requiredCredits) {
      throw new PaymentRequiredException(
        `Insufficient credits. Need ${requiredCredits}, have ${org?.credits ?? 0}.`
      );
    }
  }

  // 6. Prompt injection detection — block adversarial inputs
  detectPromptInjection(query: string): void {
    const INJECTION_PATTERNS = [
      /ignore previous instructions/i,
      /system:\s*you are now/i,
      /forget all prior/i,
      /disregard.*rules/i,
      /print.*api[_\s]?key/i,
      /reveal.*password/i,
    ];

    if (INJECTION_PATTERNS.some(p => p.test(query))) {
      throw new BadRequestException('Query contains disallowed patterns.');
    }
  }
}
```

---

## 12. Multi-Step Autonomous Flow

### Example: *"Improve my campaign performance"*

```
User: "Improve my campaign performance"
       │
       ▼
[READ] campaign.get_analytics (last 30 days)
  → open_rate: 14.2% (industry avg: 21.4%)
  → click_rate: 1.8% (industry avg: 3.4%)
  → best performing: "Product Update · April 8" (open: 32%)
  → worst performing: "Outreach · March 22" (open: 8%)
       │
       ▼
[READ] AI analysis of subject lines
  → Pattern: question-based subjects outperform statements (32% vs 9%)
  → Pattern: morning sends (9–11am) beat evening sends (8am IST optimal)
  → Pattern: first-name personalisation adds +6% open rate
       │
       ▼
[READ] campaign.suggest_subject (for underperforming campaign)
  → Suggestion A: "Quick question, {{first_name}}..."   (est. +18% opens)
  → Suggestion B: "Did you see this, {{first_name}}?"   (est. +14% opens)
  → Suggestion C: "{{first_name}}, worth 3 minutes?"    (est. +12% opens)
       │
       ▼
Response to User:
"📊 Your campaigns average 14.2% open rate vs 21.4% industry average.

Key findings:
• Question-based subjects get 3.5× more opens in your org
• Sending at 9–11am IST adds ~6% to open rate
• First-name personalisation: +6% uplift

Suggestions:
1. Resend 'Outreach · March 22' with new subject to non-openers
2. Schedule future campaigns at 9:30am IST
3. Add {{first_name}} to all subject lines

Want me to create an A/B test campaign with the new subject lines? [Yes / Customise]"
```

---

## 13. Full LangGraph Implementation

```typescript
// apps/ai-agent-service/src/agents/contact360.graph.ts
import { StateGraph, END, START } from '@langchain/langgraph';
import { RedisSaver } from '@langchain/langgraph-checkpoint-redis';

// ── State definition ─────────────────────────────────────────────────────

interface Contact360State {
  messages:       BaseMessage[];
  orgId:          string;
  userId:         string;
  sessionId:      string;
  context:        AgentContext | null;
  intents:        DetectedIntent[];
  plan:           TaskPlan | null;
  executionResults: Record<string, unknown>;
  pendingApproval: ApprovalRequest | null;
  mode:           AgentMode;
  iteration:      number;
  finalResponse:  string | null;
}

// ── Node implementations ─────────────────────────────────────────────────

async function buildContext(state: Contact360State): Promise<Partial<Contact360State>> {
  const context = await memoryEngine.buildContext(
    state.orgId, state.userId, state.sessionId
  );
  return { context };
}

async function classifyIntent(state: Contact360State): Promise<Partial<Contact360State>> {
  const lastMessage = state.messages.at(-1)?.content as string;
  safetyLayer.detectPromptInjection(lastMessage);

  const intents = await intentEngine.classify(lastMessage, state.context!);
  const mode    = intentEngine.determineMode(intents);
  return { intents, mode };
}

async function buildPlan(state: Contact360State): Promise<Partial<Contact360State>> {
  const lastMessage = state.messages.at(-1)?.content as string;
  const plan = plannerEngine.decompose(lastMessage, state.intents, state.context!);
  return { plan };
}

async function executeStep(state: Contact360State): Promise<Partial<Contact360State>> {
  const results = await executionEngine.execute(state.plan!, state.context!);
  return { executionResults: results.results };
}

async function generateResponse(state: Contact360State): Promise<Partial<Contact360State>> {
  const model = new ChatOpenAI({ model: 'gpt-4o', temperature: 0.3 });
  const systemPrompt = promptEngine.buildSystemPrompt(state.context!);

  const response = await model.invoke([
    { role: 'system', content: systemPrompt },
    ...state.messages,
    {
      role: 'assistant',
      content: `Execution results: ${JSON.stringify(state.executionResults)}`,
    },
    {
      role: 'user',
      content: 'Based on the execution results, generate a clear, concise response to the user.',
    },
  ]);

  // Store to memory
  await memoryEngine.storeQueryEmbedding(
    state.orgId,
    state.messages.at(-1)?.content as string,
    state.executionResults
  );

  return { finalResponse: response.content as string };
}

// ── Routing logic ────────────────────────────────────────────────────────

function routeAfterClassification(state: Contact360State): 'build_plan' | 'generate_response' {
  // If intent is purely read + context is clear, skip planning
  if (state.intents.every(i => !i.requiresWrite) && state.intents.length === 1) {
    return 'generate_response';
  }
  return 'build_plan';
}

// ── Graph assembly ────────────────────────────────────────────────────────

const workflow = new StateGraph<Contact360State>({
  channels: {
    messages:         { value: (a, b) => [...(a ?? []), ...(b ?? [])], default: () => [] },
    iteration:        { value: (_, b) => (b ?? 0) + 1, default: () => 0 },
    orgId:            { default: () => '' },
    userId:           { default: () => '' },
    sessionId:        { default: () => '' },
    context:          { default: () => null },
    intents:          { default: () => [] },
    plan:             { default: () => null },
    executionResults: { default: () => ({}) },
    pendingApproval:  { default: () => null },
    mode:             { default: () => 'READ' },
    finalResponse:    { default: () => null },
  },
})
  .addNode('build_context',   buildContext)
  .addNode('classify_intent', classifyIntent)
  .addNode('build_plan',      buildPlan)
  .addNode('execute_steps',   executeStep)
  .addNode('generate_response', generateResponse)

  .addEdge(START,              'build_context')
  .addEdge('build_context',    'classify_intent')
  .addConditionalEdges('classify_intent', routeAfterClassification, {
    build_plan:       'build_plan',
    generate_response: 'execute_steps',
  })
  .addEdge('build_plan',       'execute_steps')
  .addEdge('execute_steps',    'generate_response')
  .addEdge('generate_response', END);

// Persist state across sessions using Redis checkpointer
const checkpointer = new RedisSaver({ client: redisClient });

export const contact360Agent = workflow.compile({ checkpointer });
```

---

## 14. Tool Calling Implementation

```typescript
// apps/ai-agent-service/src/tools/tool.caller.ts

// Tool call JSON format (sent from LLM to execution engine)
interface ToolCall {
  id:       string;
  name:     string;
  payload:  Record<string, unknown>;
}

// Example tool calls generated by the agent for "CTO Bangalore campaign"

const exampleToolCalls: ToolCall[] = [
  {
    id:   "call_001",
    name: "vql.query",
    payload: {
      filters: { jobTitle: "CTO", city: "Bangalore" },
      limit:   50,
      orderBy: "lead_score DESC",
    },
  },
  {
    id:   "call_002",
    name: "email.validate",
    payload: {
      contactIds: ["{{call_001.result.ids}}"],
    },
  },
  {
    id:   "call_003",
    name: "campaign.create",
    payload: {
      name:       "CTO Bangalore Outreach · April 2026",
      channel:    "email",
      contactIds: ["{{call_002.result.validIds}}"],
      subject:    "Quick question, {{first_name}}",
      schedule:   { type: "now" },
    },
  },
  {
    id:   "call_004",
    name: "campaign.send",
    payload: {
      campaignId: "{{call_003.result.campaignId}}",
    },
  },
];
```

---

## 15. Prompt Templates (All Use-Cases)

```typescript
// apps/ai-agent-service/src/prompts/templates.ts

export const PROMPT_TEMPLATES = {

  // ── Lead discovery ────────────────────────────────────────────────────
  FIND_LEADS: (params: { role: string; location?: string; company?: string }) => `
Find the best leads matching this profile:
- Role: ${params.role}
${params.location ? `- Location: ${params.location}` : ''}
${params.company  ? `- Company type: ${params.company}` : ''}

Rank by lead score (highest first). Show top 10 with name, company, email status, and last activity.
`,

  // ── Campaign creation ─────────────────────────────────────────────────
  CREATE_CAMPAIGN: (params: { audience: string; goal: string; channel: string }) => `
Create a ${params.channel} campaign for: ${params.audience}
Goal: ${params.goal}

Generate:
1. A compelling subject line (question-based, personalised with {{first_name}})
2. A short email body (3 paragraphs: hook, value, CTA)
3. Best send time recommendation for Indian timezone
`,

  // ── Campaign analysis ─────────────────────────────────────────────────
  ANALYZE_CAMPAIGN: (params: { campaignName: string; stats: CampaignStats }) => `
Analyse the performance of campaign "${params.campaignName}":
- Sent: ${params.stats.sent}
- Open rate: ${params.stats.openRate}% (industry: 21.4%)
- Click rate: ${params.stats.clickRate}% (industry: 3.4%)
- Reply rate: ${params.stats.replyRate}%
- Bounce rate: ${params.stats.bounceRate}%

Provide:
1. Performance score (A/B/C/D)
2. 3 specific improvement actions
3. Whether a follow-up campaign is recommended
`,

  // ── A/B subject line testing ──────────────────────────────────────────
  AB_TEST_SUBJECTS: (params: { audience: string; goal: string }) => `
Generate 3 A/B test subject line variants for:
- Audience: ${params.audience}
- Campaign goal: ${params.goal}

For each variant provide:
- Subject line (max 50 chars, include {{first_name}})
- Predicted open rate lift (%)
- Reasoning (why this works for this audience)
`,

  // ── Follow-up sequence ────────────────────────────────────────────────
  FOLLOWUP_SEQUENCE: (params: { originalCampaign: string; reason: 'not_opened' | 'not_replied' }) => `
Design a 3-step follow-up sequence for contacts who ${params.reason.replace('_', ' ')} the campaign "${params.originalCampaign}":

Step 1 (Day 3): Brief, friendly nudge
Step 2 (Day 7): Add new value / different angle
Step 3 (Day 14): Soft close / break-up email

For each step: subject line + 2-3 sentence body + send time
`,

  // ── Insight generation ────────────────────────────────────────────────
  CRM_INSIGHTS: (params: { period: string; orgStats: OrgStats }) => `
Generate 5 actionable CRM insights for the ${params.period} period:

Data available:
- New contacts: ${params.orgStats.newContacts}
- Campaigns sent: ${params.orgStats.campaignsSent}
- Average open rate: ${params.orgStats.avgOpenRate}%
- Top lead sources: ${params.orgStats.topSources.join(', ')}
- Deals won this period: ${params.orgStats.dealsWon}

Format as: [Insight] + [Recommended action] + [Expected impact]
`,
};
```

---

## 16. Autonomous Campaign AI

```typescript
// apps/ai-agent-service/src/automation/autonomous-campaign.ts

@Injectable()
export class AutonomousCampaignService {

  /**
   * Full autonomous loop: analyse → suggest → A/B test → schedule follow-ups
   * Runs weekly per org (triggered by cron)
   */
  async runAutonomousOptimisationLoop(orgId: string): Promise<void> {
    const stats = await this.analyticsService.getWeeklyStats(orgId);

    // Step 1: Identify underperforming campaigns
    const underperforming = stats.campaigns.filter(c => c.openRate < 0.15);

    for (const campaign of underperforming) {
      // Step 2: Generate improved subject lines
      const suggestions = await this.aiCopyService.suggestSubjects({
        currentSubject: campaign.subject,
        audienceType:   campaign.audienceType,
        campaignGoal:   campaign.goal,
      });

      // Step 3: Create A/B test (50/50 split, non-openers only)
      const abTest = await this.campaignService.createAbTest({
        orgId,
        parentCampaignId: campaign.id,
        variantA:         { subject: suggestions[0].subject },
        variantB:         { subject: suggestions[1].subject },
        targetEvent:      'not_opened',
        splitRatio:       50,
      });

      // Step 4: Store automation action for human review (not auto-send)
      await this.prisma.aiAction.create({
        data: {
          orgId,
          actionType: 'create_ab_test',
          payload:    { abTest },
          preview: {
            summary:  `A/B test for "${campaign.name}" (${campaign.openRate}% open rate)`,
            variants: suggestions.slice(0, 2).map(s => s.subject),
            targets:  campaign.nonOpeners,
          },
          riskLevel: 'medium',
          status:    'PENDING_APPROVAL',
        },
      });
    }

    // Step 5: Notify org admin via WebSocket
    this.wsGateway.notifyOrg(orgId, 'ai_suggestions_ready', {
      count:   underperforming.length,
      message: `${underperforming.length} campaigns have AI improvement suggestions ready for review.`,
    });
  }
}
```

---

## 17. Observability & Cost Control

```typescript
// apps/ai-agent-service/src/observability/ai.tracker.ts

// Every agent run is tracked in Langfuse for:
// - Token usage + cost per org per day
// - Tool call success/failure rates
// - Approval accept vs reject rates
// - Response latency (p50/p95/p99)
// - Hallucination detection (fact vs tool output mismatch)

interface AgentRunMetrics {
  orgId:          string;
  sessionId:      string;
  query:          string;
  intents:        string[];
  toolsCalled:    string[];
  promptTokens:   number;
  compTokens:     number;
  totalCostUsd:   number;
  latencyMs:      number;
  approvalGates:  number;
  approvalsAccepted: number;
  approvalsRejected: number;
  success:        boolean;
}

// Daily cost budget per org (configurable per plan)
const DAILY_AI_BUDGET_USD = {
  TRIAL:      0.50,
  STARTER:    2.00,
  PRO:        10.00,
  ENTERPRISE: 50.00,
};

// Auto-throttle if org exceeds 80% of daily budget
async function checkAiBudget(orgId: string, plan: OrgPlan): Promise<void> {
  const todaySpend = await getOrgDailyAiSpend(orgId);
  const budget     = DAILY_AI_BUDGET_USD[plan];

  if (todaySpend >= budget * 0.8) {
    // Downgrade to cheaper model (gpt-4o-mini) for remainder of day
    await redis.set(`c360:ai:downgrade:${orgId}`, '1', 'EX', 86400);
  }

  if (todaySpend >= budget) {
    throw new PaymentRequiredException(
      `Daily AI budget ($${budget}) reached. Resets at midnight IST.`
    );
  }
}
```

---

## Architecture Summary

```
Contact360 Agent = LangGraph (orchestration)
                 + GPT-4o (reasoning + generation)
                 + pgvector (semantic memory)
                 + Redis (session + rate limiting)
                 + PostgreSQL (long-term memory + audit)
                 + Microservices (tools / actions)
                 + Safety Layer (permission + injection + PII)
                 + Human-in-the-Loop (approval gates)
```

| Component | Tech | Purpose |
|-----------|------|---------|
| Orchestration | LangGraph | State machine + checkpointing |
| LLM | GPT-4o (0.0 temp for classification, 0.3 for generation) | Intent, planning, response |
| Embeddings | text-embedding-3-small | Vector memory + RAG |
| Re-ranking | cross-encoder/ms-marco | RAG result quality |
| Session state | Redis (2h TTL) | Short-term memory |
| Long-term memory | PostgreSQL ai_memories | Org preferences, past facts |
| Vector search | pgvector HNSW | Semantic query recall |
| Approval UI | WebSocket gateway | Human-in-the-loop gates |
| Observability | Langfuse | Token cost, latency, quality |
| Safety | Custom SafetyLayer | Injection detection, PII masking |
