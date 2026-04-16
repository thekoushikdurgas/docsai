<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Contact360 — Deep-Dive Implementation Reference

> **Sections covered:** AI Agent Layer (LangGraph + MCP) · Enrichment Pipeline · Campaign System · pgvector RAG Engine

***

## Table of Contents

1. [AI Agent Layer — LangGraph Orchestration](#1-ai-agent-layer)
2. [MCP Server Implementation](#2-mcp-server-implementation)
3. [Email \& Phone Enrichment Pipeline](#3-enrichment-pipeline)
4. [Campaign System — Multi-Channel](#4-campaign-system)
5. [pgvector RAG Engine](#5-pgvector-rag-engine)
6. [Database Schemas (All Sections)](#6-database-schemas)
7. [Algorithm Specifications](#7-algorithm-specifications)
8. [Redis Key Design \& Caching Strategy](#8-redis-key-design)
9. [Kafka Event Contracts](#9-kafka-event-contracts)
10. [End-to-End Flow: Lead Conversion](#10-end-to-end-flow)

***

## 1. AI Agent Layer

### 1.1 LangGraph Supervisor Agent — Python (FastAPI)

```python
# services/ai-service/src/agents/supervisor.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import TypedDict, Annotated, List, Literal
import operator
import asyncio

# ── State Schema ─────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[List, operator.add]   # append-only message history
    org_id: str
    user_id: str
    workflow_id: str
    intent: str                               # classified intent
    context: dict                             # retrieved CRM context
    plan: List[str]                           # formulated action plan
    current_step: int
    tool_results: List[dict]
    requires_approval: bool
    approved: bool
    final_response: str
    error: str | None

# ── LLM Configuration ─────────────────────────────────────────────────────────

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=4096,
)

llm_with_tools = llm.bind_tools([
    search_contacts_tool,
    create_contact_tool,
    update_deal_tool,
    send_email_tool,
    score_lead_tool,
    search_knowledge_tool,
])

# ── Nodes ─────────────────────────────────────────────────────────────────────

async def classify_intent(state: AgentState) -> AgentState:
    """
    Classify incoming message into one of:
    LEAD_SCORING | CONTACT_LOOKUP | DEAL_UPDATE |
    EMAIL_DRAFT | CAMPAIGN_CREATE | KNOWLEDGE_SEARCH | UNKNOWN
    """
    system = SystemMessage(content="""
    You are the intent classifier for Contact360 CRM.
    Classify the user's message into exactly one intent category.
    Return JSON: {"intent": "<CATEGORY>", "confidence": 0.0-1.0, "entities": {}}
    """)
    
    response = await llm.ainvoke([system] + state["messages"])
    
    import json
    parsed = json.loads(response.content)
    
    return {
        **state,
        "intent": parsed["intent"],
        "context": {"entities": parsed.get("entities", {})}
    }


async def retrieve_context(state: AgentState) -> AgentState:
    """
    Retrieve CRM context using pgvector semantic search + structured lookup.
    Hybrid retrieval: pgvector for semantics, PostgreSQL for exact matches.
    """
    from src.db.pgvector import hybrid_search
    from src.db.postgres import get_contact_by_email, get_deal_by_id
    
    entities = state["context"].get("entities", {})
    retrieved = {}
    
    # Semantic search over contact notes, emails, activity history
    query_text = state["messages"][-1].content
    semantic_results = await hybrid_search(
        org_id=state["org_id"],
        query=query_text,
        top_k=5,
        filter={"org_id": state["org_id"]}
    )
    retrieved["semantic_context"] = semantic_results
    
    # Exact structured lookups
    if "email" in entities:
        contact = await get_contact_by_email(entities["email"])
        retrieved["contact"] = contact
    
    if "deal_id" in entities:
        deal = await get_deal_by_id(entities["deal_id"])
        retrieved["deal"] = deal
    
    return {**state, "context": {**state["context"], **retrieved}}


async def formulate_plan(state: AgentState) -> AgentState:
    """
    System 2 reasoning: formulate a multi-step action plan before execution.
    This prevents hallucinated tool calls and enforces sequential safety.
    """
    system = SystemMessage(content=f"""
    You are the Contact360 AI planner. Given the intent "{state['intent']}" and 
    the retrieved context, formulate a step-by-step execution plan.
    
    Available tools: search_contacts, create_contact, update_deal, 
                     send_email, score_lead, search_knowledge
    
    Rules:
    - Maximum 5 steps per plan
    - Financial actions require human approval (set requires_approval=true)
    - External email sends require human approval
    - Data reads never require approval
    
    Return JSON: {{
      "plan": ["step 1 description", "step 2 description"],
      "requires_approval": boolean,
      "approval_reason": "why approval needed or null"
    }}
    
    Context: {state['context']}
    """)
    
    response = await llm.ainvoke([system] + state["messages"])
    import json
    parsed = json.loads(response.content)
    
    return {
        **state,
        "plan": parsed["plan"],
        "requires_approval": parsed["requires_approval"],
        "current_step": 0,
    }


async def execute_tools(state: AgentState) -> AgentState:
    """Execute current plan step via tool calls."""
    step_description = state["plan"][state["current_step"]]
    
    # Feed the step + context to LLM with bound tools
    step_message = HumanMessage(content=f"""
    Execute step {state['current_step'] + 1}: {step_description}
    
    Available context: {state['context']}
    """)
    
    response = await llm_with_tools.ainvoke([step_message])
    
    # Collect tool results
    tool_results = list(state["tool_results"])
    if hasattr(response, "tool_calls") and response.tool_calls:
        for call in response.tool_calls:
            result = await dispatch_tool(call["name"], call["args"])
            tool_results.append({
                "step": state["current_step"],
                "tool": call["name"],
                "args": call["args"],
                "result": result,
            })
    
    return {
        **state,
        "tool_results": tool_results,
        "current_step": state["current_step"] + 1,
        "messages": state["messages"] + [response],
    }


async def request_approval(state: AgentState) -> AgentState:
    """
    Push approval request to Slack. The workflow pauses here until 
    a webhook callback sets state.approved = True/False.
    """
    from src.integrations.slack import send_approval_request
    
    await send_approval_request(
        workflow_id=state["workflow_id"],
        user_id=state["user_id"],
        plan=state["plan"],
        context_summary=state["context"],
    )
    
    # State persisted to PostgreSQL — workflow resumes on webhook
    return {**state, "final_response": "⏳ Awaiting your approval in Slack..."}


async def synthesize_response(state: AgentState) -> AgentState:
    """Synthesize all tool results into a final human-readable response."""
    system = SystemMessage(content="""
    Synthesize the tool execution results into a clear, concise CRM response.
    Format using Slack Block Kit markdown.
    Be specific: include record IDs, field values, and next actions.
    """)
    
    synthesis_prompt = HumanMessage(content=f"""
    Completed plan: {state['plan']}
    Tool results: {state['tool_results']}
    Original request: {state['messages'][^0].content}
    """)
    
    response = await llm.ainvoke([system, synthesis_prompt])
    
    return {**state, "final_response": response.content}


# ── Routing Logic ──────────────────────────────────────────────────────────────

def route_after_plan(state: AgentState) -> Literal["request_approval", "execute_tools"]:
    if state["requires_approval"] and not state["approved"]:
        return "request_approval"
    return "execute_tools"


def route_after_execution(state: AgentState) -> Literal["execute_tools", "synthesize_response"]:
    if state["current_step"] < len(state["plan"]):
        return "execute_tools"
    return "synthesize_response"


# ── Graph Assembly ─────────────────────────────────────────────────────────────

def build_supervisor_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    
    graph.add_node("classify_intent",     classify_intent)
    graph.add_node("retrieve_context",    retrieve_context)
    graph.add_node("formulate_plan",      formulate_plan)
    graph.add_node("execute_tools",       execute_tools)
    graph.add_node("request_approval",    request_approval)
    graph.add_node("synthesize_response", synthesize_response)
    
    graph.set_entry_point("classify_intent")
    
    graph.add_edge("classify_intent",  "retrieve_context")
    graph.add_edge("retrieve_context", "formulate_plan")
    graph.add_conditional_edges("formulate_plan", route_after_plan)
    graph.add_edge("request_approval", END)  # resumes via webhook
    graph.add_conditional_edges("execute_tools", route_after_execution)
    graph.add_edge("synthesize_response", END)
    
    return graph.compile()


supervisor = build_supervisor_graph()
```


### 1.2 AI Service — FastAPI Entrypoint

```python
# services/ai-service/src/main.py

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, UUID4
from src.agents.supervisor import supervisor, AgentState
from src.db.postgres import save_workflow_state, get_workflow_state
import uuid

app = FastAPI(title="Contact360 AI Service", version="1.0.0")

class ChatRequest(BaseModel):
    org_id: UUID4
    user_id: UUID4
    message: str
    workflow_id: UUID4 | None = None

class ApprovalWebhook(BaseModel):
    workflow_id: UUID4
    approved: bool
    approver_id: UUID4

@app.post("/v1/chat")
async def chat(req: ChatRequest, background_tasks: BackgroundTasks):
    workflow_id = req.workflow_id or uuid.uuid4()
    
    initial_state: AgentState = {
        "messages":          [{"role": "user", "content": req.message}],
        "org_id":            str(req.org_id),
        "user_id":           str(req.user_id),
        "workflow_id":       str(workflow_id),
        "intent":            "",
        "context":           {},
        "plan":              [],
        "current_step":      0,
        "tool_results":      [],
        "requires_approval": False,
        "approved":          False,
        "final_response":    "",
        "error":             None,
    }
    
    result = await supervisor.ainvoke(initial_state)
    await save_workflow_state(str(workflow_id), result)
    
    return {
        "workflow_id":    str(workflow_id),
        "response":       result["final_response"],
        "awaiting_approval": result["requires_approval"] and not result["approved"],
        "plan":           result["plan"],
    }


@app.post("/v1/approve")
async def handle_approval(webhook: ApprovalWebhook):
    """Resume paused workflow after Slack approval button click."""
    state = await get_workflow_state(str(webhook.workflow_id))
    if not state:
        raise HTTPException(404, "Workflow not found")
    
    state["approved"] = webhook.approved
    
    if not webhook.approved:
        state["final_response"] = "❌ Action cancelled by user."
        await save_workflow_state(str(webhook.workflow_id), state)
        return {"status": "cancelled"}
    
    # Resume execution from where it paused
    result = await supervisor.ainvoke(state)
    await save_workflow_state(str(webhook.workflow_id), result)
    
    return {
        "workflow_id": str(webhook.workflow_id),
        "response":    result["final_response"],
        "status":      "completed",
    }


@app.get("/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: UUID4):
    state = await get_workflow_state(str(workflow_id))
    if not state:
        raise HTTPException(404, "Workflow not found")
    return {
        "workflow_id":    str(workflow_id),
        "status":         "awaiting_approval" if state.get("requires_approval") else "completed",
        "plan":           state.get("plan", []),
        "current_step":   state.get("current_step", 0),
        "tool_results":   state.get("tool_results", []),
        "final_response": state.get("final_response", ""),
    }
```


***

## 2. MCP Server Implementation

### 2.1 CRM MCP Server (TypeScript / Node.js)

```typescript
// services/ai-service/src/mcp/crm-mcp-server.ts

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { db } from "../db/prisma.js";
import { redis } from "../cache/redis.js";

const server = new Server(
  { name: "contact360-crm", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

// ── Tools ──────────────────────────────────────────────────────────────────────

const tools: Tool[] = [
  {
    name: "search_contacts",
    description: "Full-text + semantic search across CRM contacts",
    inputSchema: {
      type: "object",
      properties: {
        org_id:   { type: "string", description: "Organization UUID" },
        query:    { type: "string", description: "Natural language search query" },
        filters:  {
          type: "object",
          properties: {
            company_id:   { type: "string" },
            source:       { type: "string", enum: ["extension", "import", "manual"] },
            email_status: { type: "string", enum: ["valid", "invalid", "unknown"] },
            created_after: { type: "string", format: "date-time" },
          },
        },
        limit:    { type: "number", default: 10, maximum: 50 },
      },
      required: ["org_id", "query"],
    },
  },
  {
    name: "create_contact",
    description: "Create a new CRM contact with enrichment trigger",
    inputSchema: {
      type: "object",
      properties: {
        org_id:      { type: "string" },
        first_name:  { type: "string" },
        last_name:   { type: "string" },
        email:       { type: "string", format: "email" },
        phone:       { type: "string" },
        company_id:  { type: "string" },
        job_title:   { type: "string" },
        source:      { type: "string", enum: ["extension", "import", "manual", "ai"] },
        trigger_enrichment: { type: "boolean", default: true },
      },
      required: ["org_id", "first_name", "email"],
    },
  },
  {
    name: "update_deal",
    description: "Update an existing deal's stage, value, or close date",
    inputSchema: {
      type: "object",
      properties: {
        org_id:     { type: "string" },
        deal_id:    { type: "string" },
        stage:      { type: "string", enum: ["PROSPECTING","QUALIFICATION","PROPOSAL","NEGOTIATION","CLOSED_WON","CLOSED_LOST"] },
        value:      { type: "number" },
        close_date: { type: "string", format: "date" },
        notes:      { type: "string" },
      },
      required: ["org_id", "deal_id"],
    },
  },
  {
    name: "score_lead",
    description: "Calculate AI lead score for a contact using behavioral + firmographic signals",
    inputSchema: {
      type: "object",
      properties: {
        org_id:     { type: "string" },
        contact_id: { type: "string" },
        signals:    {
          type: "object",
          properties: {
            email_opens:    { type: "number" },
            page_visits:    { type: "number" },
            demo_requested: { type: "boolean" },
            company_size:   { type: "number" },
            industry:       { type: "string" },
          },
        },
      },
      required: ["org_id", "contact_id"],
    },
  },
];

// ── Tool Handler ───────────────────────────────────────────────────────────────

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "search_contacts": {
      // Check cache first (TTL: 60s for search results)
      const cacheKey = `search:${args.org_id}:${args.query}:${JSON.stringify(args.filters)}`;
      const cached = await redis.get(cacheKey);
      if (cached) return { content: [{ type: "text", text: cached }] };

      const contacts = await db.$queryRaw`
        SELECT c.*, comp.name as company_name,
               ts_rank(to_tsvector('english', c.full_name || ' ' || COALESCE(c.email, '') || ' ' || COALESCE(c.job_title, '')),
                       plainto_tsquery('english', ${args.query})) as rank
        FROM contacts c
        LEFT JOIN companies comp ON c.company_id = comp.id
        WHERE c.org_id = ${args.org_id}::uuid
          AND to_tsvector('english', c.full_name || ' ' || COALESCE(c.email, '') || ' ' || COALESCE(c.job_title, ''))
              @@ plainto_tsquery('english', ${args.query})
          ${args.filters?.company_id ? db.$raw`AND c.company_id = ${args.filters.company_id}::uuid` : db.$raw``}
        ORDER BY rank DESC
        LIMIT ${args.limit ?? 10}
      `;

      const result = JSON.stringify({ contacts, total: contacts.length });
      await redis.setex(cacheKey, 60, result);

      return { content: [{ type: "text", text: result }] };
    }

    case "create_contact": {
      const contact = await db.contacts.create({
        data: {
          org_id:     args.org_id,
          first_name: args.first_name,
          last_name:  args.last_name ?? "",
          full_name:  `${args.first_name} ${args.last_name ?? ""}`.trim(),
          email:      args.email,
          phone:      args.phone,
          company_id: args.company_id,
          job_title:  args.job_title,
          source:     args.source ?? "ai",
        },
      });

      // Publish Kafka event — triggers enrichment pipeline
      if (args.trigger_enrichment !== false) {
        await kafka.producer.send({
          topic: "contact.created",
          messages: [{
            key: contact.id,
            value: JSON.stringify({
              event:      "contact.created",
              contact_id: contact.id,
              org_id:     args.org_id,
              email:      args.email,
              phone:      args.phone,
              source:     "ai_agent",
              timestamp:  new Date().toISOString(),
            }),
          }],
        });
      }

      return {
        content: [{
          type: "text",
          text: JSON.stringify({ success: true, contact_id: contact.id, contact }),
        }],
      };
    }

    case "score_lead": {
      const score = await calculateLeadScore(args.org_id, args.contact_id, args.signals);
      await db.contacts.update({
        where: { id: args.contact_id },
        data: { ai_score: score.total, ai_score_updated_at: new Date() },
      });
      return { content: [{ type: "text", text: JSON.stringify(score) }] };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// ── Resources ─────────────────────────────────────────────────────────────────

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "crm://contacts/{contact_id}",
      name: "Contact Profile",
      description: "Full 360-degree contact profile with enrichment data",
      mimeType: "application/json",
    },
    {
      uri: "crm://deals/{deal_id}",
      name: "Deal Record",
      description: "Deal details with activity history and AI score",
      mimeType: "application/json",
    },
    {
      uri: "crm://companies/{company_id}",
      name: "Company Profile",
      description: "Company record with all contacts and deals",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri.startsWith("crm://contacts/")) {
    const contact_id = uri.split("/")[^2];
    const contact = await db.contacts.findUnique({
      where: { id: contact_id },
      include: {
        company: true,
        deals: { orderBy: { created_at: "desc" }, take: 5 },
        email_validations: { orderBy: { checked_at: "desc" }, take: 1 },
        phone_validations: { orderBy: { checked_at: "desc" }, take: 1 },
      },
    });
    return { contents: [{ uri, mimeType: "application/json", text: JSON.stringify(contact) }] };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// ── Start Server ───────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Contact360 CRM MCP Server running on stdio");
}

main().catch(console.error);
```


***

## 3. Enrichment Pipeline

### 3.1 Email Enrichment Worker (TypeScript)

```typescript
// services/email-service/src/workers/enrichment.worker.ts

import { Kafka, Consumer, EachMessagePayload } from "kafkajs";
import { db } from "../db/prisma";
import { redis } from "../cache/redis";
import { HunterClient } from "../providers/hunter";
import { ZeroBounceClient } from "../providers/zerobounce";
import { MillionVerifierClient } from "../providers/millionverifier";
import { RateLimiter } from "../utils/rate-limiter";

interface ContactCreatedEvent {
  event:      "contact.created" | "contact.email_requested";
  contact_id: string;
  org_id:     string;
  email?:     string;
  first_name?: string;
  last_name?:  string;
  domain?:     string;
  phone?:      string;
  source:     string;
  timestamp:  string;
}

// ── Rate Limiters (Redis Token Bucket) ────────────────────────────────────────

const hunterLimiter       = new RateLimiter("hunter",         { requests: 100, windowMs: 60_000 });
const zeroBouncelimiter   = new RateLimiter("zerobounce",     { requests: 200, windowMs: 60_000 });
const millionVerifLimiter = new RateLimiter("millionverif",   { requests: 500, windowMs: 60_000 });

// ── Enrichment Engine ─────────────────────────────────────────────────────────

export async function enrichEmail(event: ContactCreatedEvent): Promise<void> {
  const { contact_id, org_id } = event;

  // Step 1: Check if we already have a validated email
  if (event.email) {
    await validateEmail(contact_id, org_id, event.email);
    return;
  }

  // Step 2: No email — attempt to discover it via pattern matching
  if (!event.first_name || !event.domain) {
    await markEnrichmentFailed(contact_id, "insufficient_data");
    return;
  }

  const discovered = await discoverEmail(
    event.first_name,
    event.last_name ?? "",
    event.domain,
    org_id
  );

  if (!discovered) {
    await markEnrichmentFailed(contact_id, "email_not_found");
    return;
  }

  // Step 3: Validate the discovered email
  await validateEmail(contact_id, org_id, discovered.email, discovered.confidence);
}


// ── Email Discovery ────────────────────────────────────────────────────────────

async function discoverEmail(
  firstName: string,
  lastName: string,
  domain: string,
  orgId: string
): Promise<{ email: string; confidence: number } | null> {
  // Cache check — avoid duplicate API calls for same name+domain
  const cacheKey = `email_discover:${firstName.toLowerCase()}:${lastName.toLowerCase()}:${domain}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Try org-specific email patterns first (no API call needed)
  const orgPatterns = await db.emailPatterns.findMany({
    where: { org_id: orgId },
    orderBy: { priority: "asc" },
  });

  for (const pattern of orgPatterns) {
    const email = applyPattern(pattern.pattern, firstName, lastName, domain);
    const isValid = await quickMxCheck(email);
    if (isValid) {
      await redis.setex(cacheKey, 3600, JSON.stringify({ email, confidence: 0.75 }));
      return { email, confidence: 0.75 };
    }
  }

  // Fallback: Hunter.io API
  if (!(await hunterLimiter.tryConsume(orgId))) {
    throw new RateLimitError("hunter", "Rate limit exceeded for Hunter.io");
  }

  const hunter = new HunterClient(process.env.HUNTER_API_KEY!);
  const result = await hunter.findEmail({ firstName, lastName, domain });

  if (result.data?.email && result.data.confidence >= 70) {
    const discovered = { email: result.data.email, confidence: result.data.confidence / 100 };
    await redis.setex(cacheKey, 3600, JSON.stringify(discovered));
    return discovered;
  }

  return null;
}


// ── Email Validation ───────────────────────────────────────────────────────────

async function validateEmail(
  contactId: string,
  orgId: string,
  email: string,
  priorConfidence: number = 0.5
): Promise<void> {
  // Deduplicate: check if already validated within 7 days
  const existing = await db.emailValidations.findFirst({
    where: {
      org_id: orgId,
      email,
      checked_at: { gte: new Date(Date.now() - 7 * 86400_000) },
    },
  });

  if (existing) {
    await db.contacts.update({
      where: { id: contactId },
      data: {
        email_status:     existing.is_valid ? "VALID" : "INVALID",
        email_confidence: existing.score ?? 0,
      },
    });
    return;
  }

  // Parallel validation using multiple providers
  // Provider priority: ZeroBounce → MillionVerifier → Fallback MX check
  let validationResult = await multiProviderValidate(orgId, email);

  // Persist validation record
  await db.emailValidations.create({
    data: {
      org_id:     orgId,
      email,
      is_valid:   validationResult.is_valid,
      provider:   validationResult.provider,
      score:      validationResult.score,
      checked_at: new Date(),
    },
  });

  // Update contact record
  await db.contacts.update({
    where: { id: contactId },
    data: {
      email_status:     validationResult.is_valid ? "VALID" : "INVALID",
      email_confidence: validationResult.score,
      updated_at:       new Date(),
    },
  });

  // Emit enrichment completed event
  await kafka.producer.send({
    topic: "contact.enriched",
    messages: [{
      key: contactId,
      value: JSON.stringify({
        event:      "contact.email_enriched",
        contact_id: contactId,
        org_id:     orgId,
        email,
        is_valid:   validationResult.is_valid,
        score:      validationResult.score,
        provider:   validationResult.provider,
        timestamp:  new Date().toISOString(),
      }),
    }],
  });
}


async function multiProviderValidate(
  orgId: string,
  email: string
): Promise<{ is_valid: boolean; score: number; provider: string }> {
  // Try ZeroBounce first (highest accuracy)
  if (await zeroBouncelimiter.tryConsume(orgId)) {
    try {
      const zb = new ZeroBounceClient(process.env.ZEROBOUNCE_API_KEY!);
      const result = await zb.validate(email);

      return {
        is_valid: result.status === "valid",
        score:    result.status === "valid" ? 0.95 : 0.1,
        provider: "zerobounce",
      };
    } catch (err) {
      console.warn("ZeroBounce failed, falling back to MillionVerifier", err);
    }
  }

  // Fallback: MillionVerifier
  if (await millionVerifLimiter.tryConsume(orgId)) {
    const mv = new MillionVerifierClient(process.env.MILLIONVERIF_API_KEY!);
    const result = await mv.verify(email);

    return {
      is_valid: result.result === "ok",
      score:    result.result === "ok" ? 0.85 : 0.15,
      provider: "millionverifier",
    };
  }

  // Last resort: MX record check only
  const hasMx = await quickMxCheck(email);
  return { is_valid: hasMx, score: hasMx ? 0.5 : 0.0, provider: "mx_check" };
}


// ── Pattern Engine ─────────────────────────────────────────────────────────────

function applyPattern(pattern: string, firstName: string, lastName: string, domain: string): string {
  const f = firstName.toLowerCase();
  const l = lastName.toLowerCase();
  const fi = f.charAt(0);
  const li = l.charAt(0);

  return pattern
    .replace("{first}",       f)
    .replace("{last}",        l)
    .replace("{first.last}",  `${f}.${l}`)
    .replace("{f.last}",      `${fi}.${l}`)
    .replace("{first.l}",     `${f}.${li}`)
    .replace("{firstlast}",   `${f}${l}`)
    .replace("{domain}",      domain);
}


// ── Rate Limiter (Redis Token Bucket) ─────────────────────────────────────────

export class RateLimiter {
  private key: string;
  private requests: number;
  private windowMs: number;

  constructor(name: string, config: { requests: number; windowMs: number }) {
    this.key       = `rate_limit:${name}`;
    this.requests  = config.requests;
    this.windowMs  = config.windowMs;
  }

  async tryConsume(orgId: string): Promise<boolean> {
    const key = `${this.key}:${orgId}`;
    const windowSec = Math.floor(this.windowMs / 1000);

    // Lua script for atomic token bucket
    const script = `
      local key     = KEYS[^1]
      local limit   = tonumber(ARGV[^1])
      local window  = tonumber(ARGV[^2])
      local current = redis.call('GET', key)
      
      if current == false then
        redis.call('SET', key, 1, 'EX', window)
        return 1
      elseif tonumber(current) < limit then
        redis.call('INCR', key)
        return 1
      else
        return 0
      end
    `;

    const result = await redis.eval(script, 1, key, this.requests, windowSec);
    return result === 1;
  }

  async getRemainingQuota(orgId: string): Promise<number> {
    const key     = `${this.key}:${orgId}`;
    const current = await redis.get(key);
    return this.requests - (current ? parseInt(current) : 0);
  }
}
```


### 3.2 Phone Validation Worker

```typescript
// services/phone-service/src/workers/phone-validator.ts

import { parsePhoneNumber, isValidPhoneNumber, CountryCode } from "libphonenumber-js";
import { TwilioLookup } from "../providers/twilio-lookup";
import { NumverifyClient } from "../providers/numverify";

export async function validatePhone(
  contactId: string,
  orgId:     string,
  rawPhone:  string
): Promise<PhoneValidationResult> {

  // Step 1: Normalize using libphonenumber-js
  let normalized: string;
  let countryCode: string;
  let isStructurallyValid: boolean;

  try {
    const parsed  = parsePhoneNumber(rawPhone, "IN"); // India default
    normalized    = parsed.formatInternational();     // +91 98765 43210
    countryCode   = parsed.country ?? "UNKNOWN";
    isStructurallyValid = isValidPhoneNumber(rawPhone, countryCode as CountryCode);
  } catch {
    // Try with E.164 format
    isStructurallyValid = false;
    normalized  = rawPhone;
    countryCode = "UNKNOWN";
  }

  if (!isStructurallyValid) {
    await persistPhoneValidation(contactId, orgId, normalized, countryCode, false, "invalid_format", null);
    return { is_valid: false, reason: "invalid_format" };
  }

  // Step 2: Carrier lookup via Twilio (most reliable)
  const lookup = new TwilioLookup(process.env.TWILIO_SID!, process.env.TWILIO_AUTH!);

  try {
    const info = await lookup.lookupNumber(normalized);

    const result: PhoneValidationResult = {
      is_valid:    true,
      phone:       normalized,
      country_code: countryCode,
      carrier:     info.carrier?.name ?? null,
      line_type:   info.line_type,  // mobile | landline | voip
      region:      info.country_code,
    };

    await persistPhoneValidation(contactId, orgId, normalized, countryCode, true, info.carrier?.name ?? null, info.line_type);
    return result;

  } catch (err) {
    // Fallback: Numverify
    const nv     = new NumverifyClient(process.env.NUMVERIFY_KEY!);
    const nvResult = await nv.validate(normalized);

    await persistPhoneValidation(contactId, orgId, normalized, countryCode,
      nvResult.valid, nvResult.carrier ?? null, nvResult.line_type ?? null
    );

    return {
      is_valid:     nvResult.valid,
      phone:        normalized,
      country_code: countryCode,
      carrier:      nvResult.carrier ?? null,
      line_type:    nvResult.line_type ?? null,
      region:       nvResult.country_code ?? null,
    };
  }
}
```


***

## 4. Campaign System

### 4.1 Campaign Scheduler (NestJS Service)

```typescript
// services/campaign-service/src/campaign.service.ts

import { Injectable, Logger } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { InjectQueue } from "@nestjs/bull";
import { Queue } from "bull";
import { Campaign, CampaignStatus, CampaignType } from "./entities/campaign.entity";
import { CampaignTarget } from "./entities/campaign-target.entity";
import { RedisService } from "../cache/redis.service";
import { KafkaService } from "../events/kafka.service";
import { CampaignStats } from "./entities/campaign-stats.entity";

@Injectable()
export class CampaignService {
  private readonly logger = new Logger(CampaignService.name);

  constructor(
    @InjectRepository(Campaign)       private campaigns: Repository<Campaign>,
    @InjectRepository(CampaignTarget) private targets:   Repository<CampaignTarget>,
    @InjectRepository(CampaignStats)  private stats:     Repository<CampaignStats>,
    @InjectQueue("campaign-dispatch") private queue:     Queue,
    private redis:  RedisService,
    private kafka:  KafkaService,
  ) {}

  // ── Create Campaign ──────────────────────────────────────────────────────────

  async createCampaign(dto: CreateCampaignDto): Promise<Campaign> {
    const campaign = await this.campaigns.save({
      org_id:       dto.org_id,
      name:         dto.name,
      type:         dto.type,
      status:       "DRAFT",
      scheduled_at: dto.scheduled_at ? new Date(dto.scheduled_at) : null,
    });

    // Bulk insert targets (chunk in batches of 500)
    const chunks = chunkArray(dto.contact_ids, 500);
    for (const chunk of chunks) {
      await this.targets.insert(
        chunk.map(contact_id => ({ campaign_id: campaign.id, contact_id }))
      );
    }

    // Initialize stats row
    await this.stats.insert({
      campaign_id: campaign.id,
      sent: 0, delivered: 0, opened: 0, clicked: 0, replied: 0,
    });

    this.logger.log(`Created campaign ${campaign.id} with ${dto.contact_ids.length} targets`);
    return campaign;
  }

  // ── Launch Campaign ──────────────────────────────────────────────────────────

  async launchCampaign(campaignId: string, orgId: string): Promise<void> {
    const campaign = await this.campaigns.findOneOrFail({
      where: { id: campaignId, org_id: orgId },
    });

    if (!["DRAFT", "PAUSED"].includes(campaign.status)) {
      throw new Error(`Campaign ${campaignId} is not in a launchable state: ${campaign.status}`);
    }

    await this.campaigns.update(campaignId, { status: "RUNNING" });

    // Paginate targets in batches to avoid memory blowout
    const PAGE_SIZE = 100;
    let page        = 0;

    while (true) {
      const batch = await this.targets.find({
        where: { campaign_id: campaignId },
        skip:  page * PAGE_SIZE,
        take:  PAGE_SIZE,
        relations: ["contact"],
      });

      if (batch.length === 0) break;

      // Enqueue each message with delay for rate limiting
      for (let i = 0; i < batch.length; i++) {
        const target = batch[i];
        const delay  = i * this.getDelayMs(campaign.type);  // stagger sends

        await this.queue.add(
          "send_campaign_message",
          {
            campaign_id: campaignId,
            contact_id:  target.contact_id,
            org_id:      orgId,
            type:        campaign.type,
            attempt:     1,
          },
          {
            delay,
            attempts:   3,
            backoff:    { type: "exponential", delay: 5000 },
            removeOnComplete: 500,
            removeOnFail:     100,
          }
        );
      }

      page++;
    }

    await this.kafka.emit("campaign.launched", {
      campaign_id: campaignId,
      org_id:      orgId,
      status:      "RUNNING",
      timestamp:   new Date().toISOString(),
    });
  }

  // ── Delay calculation per channel ────────────────────────────────────────────

  private getDelayMs(type: CampaignType): number {
    // Respect channel rate limits
    switch (type) {
      case "EMAIL":    return 100;   // 10/second
      case "SMS":      return 500;   // 2/second (TRAI compliance)
      case "WHATSAPP": return 1000;  // 1/second (WhatsApp BSP limits)
      default:         return 200;
    }
  }

  // ── Track Engagement ─────────────────────────────────────────────────────────

  async trackEngagement(
    emailLogId: string,
    event: "opened" | "clicked" | "replied",
    metadata?: { url?: string; user_agent?: string }
  ): Promise<void> {
    const now = new Date();

    // Update engagement record
    await this.db.emailEngagements.upsert({
      where: { email_log_id: emailLogId },
      update: {
        [event]:              true,
        [`${event}_at`]:      now,
      },
      create: {
        email_log_id:  emailLogId,
        opened:        event === "opened",
        clicked:       event === "clicked",
        replied:       event === "replied",
        opened_at:     event === "opened"  ? now : null,
        clicked_at:    event === "clicked" ? now : null,
      },
    });

    // Atomically increment campaign stats using Redis HINCRBY
    const log = await this.db.emailLogs.findUnique({ where: { id: emailLogId } });
    if (log?.campaign_id) {
      await this.redis.hincrby(`campaign_stats:${log.campaign_id}`, event, 1);
    }

    // Kafka event for real-time analytics
    await this.kafka.emit("campaign.engagement", {
      email_log_id: emailLogId,
      event,
      metadata,
      timestamp: now.toISOString(),
    });
  }

  // ── Aggregate stats from Redis → PostgreSQL (run every 5 min) ────────────────

  async flushStatsToDb(campaignId: string): Promise<void> {
    const cached = await this.redis.hgetall(`campaign_stats:${campaignId}`);
    if (!cached) return;

    await this.stats.update(
      { campaign_id: campaignId },
      {
        sent:      parseInt(cached.sent ?? "0"),
        delivered: parseInt(cached.delivered ?? "0"),
        opened:    parseInt(cached.opened ?? "0"),
        clicked:   parseInt(cached.clicked ?? "0"),
        replied:   parseInt(cached.replied ?? "0"),
      }
    );
  }
}
```


### 4.2 Bull Queue Processor

```typescript
// services/campaign-service/src/processors/campaign.processor.ts

import { Processor, Process } from "@nestjs/bull";
import { Job } from "bull";
import { SendgridProvider } from "../providers/sendgrid";
import { TwilioProvider } from "../providers/twilio";
import { WhatsAppProvider } from "../providers/whatsapp";

@Processor("campaign-dispatch")
export class CampaignProcessor {

  @Process("send_campaign_message")
  async handleSend(job: Job<CampaignMessageJob>): Promise<void> {
    const { campaign_id, contact_id, org_id, type, attempt } = job.data;

    // Load contact + message template
    const [contact, message] = await Promise.all([
      db.contacts.findUnique({ where: { id: contact_id } }),
      db.campaignMessages.findFirst({ where: { campaign_id, channel: type } }),
    ]);

    if (!contact || !message) {
      throw new Error(`Missing contact or message for campaign ${campaign_id}`);
    }

    // Personalise template with contact data
    const personalizedContent = personalizeTemplate(message.content, {
      first_name:  contact.first_name,
      last_name:   contact.last_name,
      company:     contact.company?.name,
      job_title:   contact.job_title,
    });

    // Dispatch via correct channel
    let providerId: string;
    switch (type) {
      case "EMAIL":
        providerId = await new SendgridProvider().send({
          to:      contact.email!,
          subject: message.subject,
          html:    personalizedContent,
        });
        break;
      case "SMS":
        providerId = await new TwilioProvider().sendSms({
          to:   contact.phone!,
          body: personalizedContent,
        });
        break;
      case "WHATSAPP":
        providerId = await new WhatsAppProvider().sendMessage({
          to:      contact.phone!,
          content: personalizedContent,
        });
        break;
    }

    // Log send event
    await db.emailLogs.create({
      data: {
        org_id,
        contact_id,
        email:       contact.email!,
        campaign_id,
        status:      "SENT",
        provider:    providerId,
        sent_at:     new Date(),
      },
    });

    // Increment Redis stats
    await redis.hincrby(`campaign_stats:${campaign_id}`, "sent", 1);
  }
}


function personalizeTemplate(template: string, vars: Record<string, string | undefined>): string {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key) => vars[key] ?? `{{${key}}}`);
}
```


***

## 5. pgvector RAG Engine

### 5.1 Embedding Service \& Hybrid Search

```python
# services/ai-service/src/db/pgvector.py

import asyncpg
import numpy as np
from openai import AsyncOpenAI
from typing import List, Optional

client   = AsyncOpenAI()
POOL:    asyncpg.Pool = None  # initialized at startup
DIM      = 1536               # text-embedding-3-small dimension

# ── Embedding Generation ───────────────────────────────────────────────────────

async def embed_text(text: str) -> List[float]:
    """Generate embedding using OpenAI text-embedding-3-small."""
    response = await client.embeddings.create(
        model  = "text-embedding-3-small",
        input  = text,
        encoding_format = "float",
    )
    return response.data[^0].embedding


async def upsert_contact_embedding(contact_id: str, org_id: str, text_content: str) -> None:
    """
    Generate and store embedding for a contact.
    text_content should be a concatenation of all relevant fields:
    name + job_title + company + email + notes + activity history
    """
    embedding = await embed_text(text_content)
    embedding_str = f"[{','.join(str(x) for x in embedding)}]"

    async with POOL.acquire() as conn:
        await conn.execute("""
            INSERT INTO contact_embeddings (contact_id, org_id, content_hash, embedding, updated_at)
            VALUES ($1::uuid, $2::uuid, md5($3), $4::vector, NOW())
            ON CONFLICT (contact_id)
            DO UPDATE SET
                embedding    = EXCLUDED.embedding,
                content_hash = EXCLUDED.content_hash,
                updated_at   = NOW()
        """, contact_id, org_id, text_content, embedding_str)


# ── Hybrid Search (Semantic + Keyword) ────────────────────────────────────────

async def hybrid_search(
    org_id:    str,
    query:     str,
    top_k:     int = 10,
    filter:    Optional[dict] = None,
    alpha:     float = 0.7,   # 0 = pure keyword, 1 = pure semantic
) -> List[dict]:
    """
    Hybrid retrieval combining:
    - Semantic search via pgvector cosine similarity (weight: alpha)
    - Full-text search via PostgreSQL tsvector (weight: 1 - alpha)
    
    Results are fused using Reciprocal Rank Fusion (RRF).
    """
    query_embedding = await embed_text(query)
    embedding_str   = f"[{','.join(str(x) for x in query_embedding)}]"

    async with POOL.acquire() as conn:
        rows = await conn.fetch("""
            WITH semantic_results AS (
                SELECT
                    c.id,
                    c.full_name,
                    c.email,
                    c.job_title,
                    comp.name AS company_name,
                    1 - (ce.embedding <=> $1::vector) AS semantic_score,
                    ROW_NUMBER() OVER (ORDER BY ce.embedding <=> $1::vector) AS semantic_rank
                FROM contacts c
                JOIN contact_embeddings ce ON c.id = ce.contact_id
                LEFT JOIN companies comp ON c.company_id = comp.id
                WHERE c.org_id = $2::uuid
                  AND 1 - (ce.embedding <=> $1::vector) > 0.3
                ORDER BY ce.embedding <=> $1::vector
                LIMIT $3 * 2
            ),
            keyword_results AS (
                SELECT
                    c.id,
                    c.full_name,
                    c.email,
                    c.job_title,
                    comp.name AS company_name,
                    ts_rank(
                        to_tsvector('english', c.full_name || ' ' || COALESCE(c.email, '') || ' ' || COALESCE(c.job_title, '')),
                        plainto_tsquery('english', $4)
                    ) AS keyword_score,
                    ROW_NUMBER() OVER (
                        ORDER BY ts_rank(
                            to_tsvector('english', c.full_name || ' ' || COALESCE(c.email, '') || ' ' || COALESCE(c.job_title, '')),
                            plainto_tsquery('english', $4)
                        ) DESC
                    ) AS keyword_rank
                FROM contacts c
                LEFT JOIN companies comp ON c.company_id = comp.id
                WHERE c.org_id = $2::uuid
                  AND to_tsvector('english', c.full_name || ' ' || COALESCE(c.email, '') || ' ' || COALESCE(c.job_title, ''))
                      @@ plainto_tsquery('english', $4)
                LIMIT $3 * 2
            ),
            rrf_fusion AS (
                SELECT
                    COALESCE(s.id, k.id)              AS id,
                    COALESCE(s.full_name, k.full_name) AS full_name,
                    COALESCE(s.email, k.email)         AS email,
                    COALESCE(s.job_title, k.job_title) AS job_title,
                    COALESCE(s.company_name, k.company_name) AS company_name,
                    -- Reciprocal Rank Fusion score
                    (
                        $5 * COALESCE(1.0 / (60 + s.semantic_rank), 0) +
                        (1 - $5) * COALESCE(1.0 / (60 + k.keyword_rank), 0)
                    ) AS rrf_score,
                    COALESCE(s.semantic_score, 0) AS semantic_score,
                    COALESCE(k.keyword_score, 0)  AS keyword_score
                FROM semantic_results s
                FULL OUTER JOIN keyword_results k ON s.id = k.id
            )
            SELECT * FROM rrf_fusion
            ORDER BY rrf_score DESC
            LIMIT $3
        """, embedding_str, org_id, top_k, query, alpha)

        return [dict(row) for row in rows]


# ── HNSW Index Creation ────────────────────────────────────────────────────────
# Run once during migration:
#
# CREATE INDEX CONCURRENTLY idx_contact_embeddings_hnsw
# ON contact_embeddings
# USING hnsw (embedding vector_cosine_ops)
# WITH (m = 16, ef_construction = 64);
#
# Parameters:
#   m              = number of bi-directional links per node (16 = good balance)
#   ef_construction = size of dynamic candidate list during indexing (64 = accurate)
#   vector_cosine_ops = cosine distance (best for normalized text embeddings)
```


***

## 6. Database Schemas

### 6.1 AI \& Agent Tables

```sql
-- ── Contact Embeddings (pgvector) ──────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE contact_embeddings (
    contact_id    UUID PRIMARY KEY REFERENCES contacts(id) ON DELETE CASCADE,
    org_id        UUID NOT NULL REFERENCES organizations(id),
    embedding     vector(1536) NOT NULL,         -- OpenAI text-embedding-3-small
    content_hash  TEXT NOT NULL,                 -- MD5 of source text (deduplicate)
    model_version TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- HNSW index for fast cosine similarity search
CREATE INDEX idx_contact_embeddings_hnsw
ON contact_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- ── AI Workflow State (LangGraph persistence) ──────────────────────────────────
CREATE TABLE ai_workflow_states (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id        UUID NOT NULL REFERENCES organizations(id),
    user_id       UUID NOT NULL REFERENCES users(id),
    state         JSONB NOT NULL,                -- full LangGraph AgentState
    status        TEXT NOT NULL DEFAULT 'running'
                    CHECK (status IN ('running','awaiting_approval','completed','failed','cancelled')),
    intent        TEXT,
    requires_approval BOOLEAN DEFAULT FALSE,
    approved      BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW(),
    completed_at  TIMESTAMPTZ
);

CREATE INDEX idx_workflow_states_org_status ON ai_workflow_states(org_id, status);
CREATE INDEX idx_workflow_states_user ON ai_workflow_states(user_id, created_at DESC);

-- ── Agent Memory (persistent across sessions) ─────────────────────────────────
CREATE TABLE agent_memories (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id        UUID NOT NULL REFERENCES organizations(id),
    user_id       UUID REFERENCES users(id),
    contact_id    UUID REFERENCES contacts(id),
    memory_type   TEXT NOT NULL CHECK (memory_type IN ('interaction','preference','context','fact')),
    content       TEXT NOT NULL,
    embedding     vector(1536),
    importance    FLOAT DEFAULT 0.5,             -- 0-1 importance score for forgetting
    accessed_at   TIMESTAMPTZ DEFAULT NOW(),
    expires_at    TIMESTAMPTZ,                   -- null = never expires
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agent_memories_hnsw
ON agent_memories USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- ── MCP Tool Invocation Audit Log ─────────────────────────────────────────────
CREATE TABLE mcp_invocations (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id        UUID NOT NULL,
    workflow_id   UUID REFERENCES ai_workflow_states(id),
    tool_name     TEXT NOT NULL,
    server_name   TEXT NOT NULL,                 -- which MCP server
    input_args    JSONB,
    output_result JSONB,
    error         TEXT,
    duration_ms   INT,
    invoked_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_mcp_invocations_workflow ON mcp_invocations(workflow_id);
CREATE INDEX idx_mcp_invocations_org_tool ON mcp_invocations(org_id, tool_name, invoked_at DESC);
```


### 6.2 Enrichment Tables (Enhanced)

```sql
-- ── Email Validations ─────────────────────────────────────────────────────────
CREATE TABLE email_validations (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id        UUID NOT NULL REFERENCES organizations(id),
    email         TEXT NOT NULL,
    is_valid      BOOLEAN NOT NULL,
    provider      TEXT NOT NULL CHECK (provider IN ('zerobounce','millionverifier','hunter','mx_check','manual')),
    score         FLOAT CHECK (score >= 0 AND score <= 1),
    mx_record     BOOLEAN,
    smtp_check    BOOLEAN,
    disposable    BOOLEAN DEFAULT FALSE,
    role_account  BOOLEAN DEFAULT FALSE,         -- e.g. info@, admin@
    free_provider BOOLEAN DEFAULT FALSE,         -- e.g. gmail, yahoo
    checked_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_email_validations_email_recent
ON email_validations(email, org_id, (date_trunc('day', checked_at)));

-- ── Phone Validations ─────────────────────────────────────────────────────────
CREATE TABLE phone_validations (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id         UUID NOT NULL REFERENCES organizations(id),
    phone          TEXT NOT NULL,
    normalized     TEXT,                          -- E.164 format: +919876543210
    country_code   TEXT,
    is_valid       BOOLEAN NOT NULL,
    carrier        TEXT,
    line_type      TEXT CHECK (line_type IN ('mobile','landline','voip','unknown')),
    provider       TEXT NOT NULL CHECK (provider IN ('twilio','numverify','libphonenumber')),
    checked_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Email Pattern Discovery ───────────────────────────────────────────────────
CREATE TABLE email_patterns (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id        UUID REFERENCES organizations(id),  -- null = global pattern
    domain        TEXT,                               -- null = applies to all domains
    pattern       TEXT NOT NULL,                      -- e.g. {first.last}@{domain}
    confidence    FLOAT DEFAULT 0.5,
    priority      INT DEFAULT 100,
    source        TEXT CHECK (source IN ('manual','discovered','api')),
    verified_count INT DEFAULT 0,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_email_patterns_domain ON email_patterns(domain, org_id);
```


### 6.3 Campaign Tables (Enhanced)

```sql
-- ── Campaign Events (high-volume engagement tracking) ─────────────────────────
CREATE TABLE campaign_events (
    id            UUID DEFAULT gen_random_uuid(),
    org_id        UUID NOT NULL,
    campaign_id   UUID NOT NULL REFERENCES campaigns(id),
    contact_id    UUID REFERENCES contacts(id),
    email_log_id  UUID REFERENCES email_logs(id),
    event_type    TEXT NOT NULL CHECK (
                    event_type IN ('sent','delivered','bounced','opened','clicked','replied','unsubscribed','complained')
                  ),
    metadata      JSONB,                          -- {url, user_agent, ip_geo, link_id}
    occurred_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (occurred_at);              -- partition by month for performance

-- Create monthly partitions
CREATE TABLE campaign_events_2026_04 PARTITION OF campaign_events
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE campaign_events_2026_05 PARTITION OF campaign_events
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE INDEX idx_campaign_events_campaign ON campaign_events(campaign_id, occurred_at DESC);
CREATE INDEX idx_campaign_events_contact  ON campaign_events(contact_id, occurred_at DESC);

-- ── Campaign Sequences (multi-step drip campaigns) ───────────────────────────
CREATE TABLE campaign_sequences (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id   UUID NOT NULL REFERENCES campaigns(id),
    step_number   INT NOT NULL,
    delay_hours   INT NOT NULL DEFAULT 0,         -- hours after previous step
    condition     JSONB,                           -- {if: "not_opened", action: "send_followup"}
    message_id    UUID REFERENCES campaign_messages(id),
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (campaign_id, step_number)
);

-- ── Contact Campaign State (tracks where each contact is in sequence) ─────────
CREATE TABLE contact_campaign_states (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id     UUID NOT NULL REFERENCES campaigns(id),
    contact_id      UUID NOT NULL REFERENCES contacts(id),
    current_step    INT DEFAULT 0,
    status          TEXT DEFAULT 'active'
                      CHECK (status IN ('active','completed','unsubscribed','bounced')),
    next_send_at    TIMESTAMPTZ,
    last_event      TEXT,
    last_event_at   TIMESTAMPTZ,
    UNIQUE (campaign_id, contact_id)
);
```


***

## 7. Algorithm Specifications

### 7.1 Lead Scoring Algorithm

```typescript
// services/ai-service/src/algorithms/lead-scorer.ts

interface LeadSignals {
  // Behavioral signals
  email_opens:         number;    // count
  email_clicks:        number;    // count
  page_visits:         number;    // count
  demo_requested:      boolean;
  pricing_page_visited: boolean;
  docs_visited:        number;    // count
  
  // Firmographic signals
  company_size:        number;    // employees
  industry:            string;
  annual_revenue?:     number;
  funding_stage?:      string;   // seed, series-a, ...
  
  // Recency signals
  last_activity_days:  number;    // days since last activity
  created_days_ago:    number;    // days since contact created
}

interface LeadScoreBreakdown {
  behavioral_score:   number;   // 0-40
  firmographic_score: number;   // 0-30
  recency_score:      number;   // 0-30
  total:              number;   // 0-100
  grade:              "A" | "B" | "C" | "D";
  explanation:        string[];
}

export function calculateLeadScore(signals: LeadSignals): LeadScoreBreakdown {
  const explanation: string[] = [];

  // ── Behavioral Score (0-40) ─────────────────────────────────────────────────
  let behavioral = 0;

  if (signals.demo_requested) {
    behavioral += 20;
    explanation.push("+20: Demo requested (high intent)");
  }
  if (signals.pricing_page_visited) {
    behavioral += 10;
    explanation.push("+10: Pricing page visited");
  }

  // Email engagement (capped at 8 pts)
  const emailEngagement = Math.min(
    (signals.email_opens * 1.5) + (signals.email_clicks * 3),
    8
  );
  behavioral += emailEngagement;
  if (emailEngagement > 0) explanation.push(`+${emailEngagement.toFixed(1)}: Email engagement`);

  // Page visits (capped at 2 pts)
  const pageScore = Math.min(signals.page_visits * 0.5, 2);
  behavioral += pageScore;

  behavioral = Math.min(behavioral, 40);

  // ── Firmographic Score (0-30) ───────────────────────────────────────────────
  let firmographic = 0;

  // Company size scoring (ICP: 50-500 employees = ideal)
  if (signals.company_size >= 50 && signals.company_size <= 500) {
    firmographic += 15;
    explanation.push("+15: Company size in ICP range (50-500 employees)");
  } else if (signals.company_size > 500) {
    firmographic += 10;
    explanation.push("+10: Enterprise company");
  } else if (signals.company_size >= 10) {
    firmographic += 5;
    explanation.push("+5: SMB company");
  }

  // Industry scoring
  const HIGH_VALUE_INDUSTRIES = ["saas", "fintech", "healthcare", "enterprise_software"];
  const MED_VALUE_INDUSTRIES  = ["retail", "manufacturing", "education", "consulting"];

  if (HIGH_VALUE_INDUSTRIES.includes(signals.industry.toLowerCase())) {
    firmographic += 10;
    explanation.push(`+10: High-value industry (${signals.industry})`);
  } else if (MED_VALUE_INDUSTRIES.includes(signals.industry.toLowerCase())) {
    firmographic += 5;
    explanation.push(`+5: Mid-value industry (${signals.industry})`);
  }

  // Funding stage (for B2B SaaS targeting funded startups)
  const FUNDED_STAGES = ["series-a", "series-b", "series-c", "growth"];
  if (signals.funding_stage && FUNDED_STAGES.includes(signals.funding_stage.toLowerCase())) {
    firmographic += 5;
    explanation.push(`+5: Funded company (${signals.funding_stage})`);
  }

  firmographic = Math.min(firmographic, 30);

  // ── Recency Score (0-30) ────────────────────────────────────────────────────
  let recency = 0;

  if (signals.last_activity_days <= 1) {
    recency += 30;
    explanation.push("+30: Activity within last 24 hours (hot lead)");
  } else if (signals.last_activity_days <= 7) {
    recency += 20;
    explanation.push("+20: Activity within last week");
  } else if (signals.last_activity_days <= 30) {
    recency += 10;
    explanation.push("+10: Activity within last month");
  } else if (signals.last_activity_days <= 90) {
    recency += 5;
    explanation.push("+5: Activity within last quarter");
  }
  // > 90 days = 0 recency score (cold lead)

  const total = behavioral + firmographic + recency;

  const grade = total >= 80 ? "A" :
                total >= 60 ? "B" :
                total >= 40 ? "C" : "D";

  return { behavioral_score: behavioral, firmographic_score: firmographic, recency_score: recency, total, grade, explanation };
}
```


### 7.2 Email Pattern Discovery Algorithm

```python
# services/email-service/src/algorithms/pattern_discovery.py

from collections import Counter
from itertools import combinations
from typing import List, Tuple
import re

PATTERN_TEMPLATES = [
    ("{first}.{last}@{domain}",   lambda f, l: f"{f}.{l}"),
    ("{first}@{domain}",          lambda f, l: f),
    ("{f}{last}@{domain}",        lambda f, l: f"{f[^0]}{l}"),
    ("{first}{l}@{domain}",       lambda f, l: f"{f}{l[^0]}"),
    ("{first}{last}@{domain}",    lambda f, l: f"{f}{l}"),
    ("{last}.{first}@{domain}",   lambda f, l: f"{l}.{f}"),
    ("{f}.{last}@{domain}",       lambda f, l: f"{f[^0]}.{l}"),
]

def discover_pattern(known_emails: List[Tuple[str, str, str]]) -> str | None:
    """
    Discover email pattern from known (first_name, last_name, email) tuples.
    Returns the most common pattern template or None.
    
    known_emails: List of (first_name, last_name, email)
    """
    if len(known_emails) < 3:
        return None
    
    pattern_matches = Counter()
    
    for first, last, email in known_emails:
        f = first.lower().strip()
        l = last.lower().strip()
        
        local_part = email.split("@")[^0].lower()
        
        for template, generator in PATTERN_TEMPLATES:
            expected = generator(f, l)
            if local_part == expected:
                pattern_matches[template] += 1
                break
    
    if not pattern_matches:
        return None
    
    most_common, count = pattern_matches.most_common(1)[^0]


<div align="center">⁂</div>

[^1]: Pasted-text.txt
[^2]: deep-research-report-1.md```

