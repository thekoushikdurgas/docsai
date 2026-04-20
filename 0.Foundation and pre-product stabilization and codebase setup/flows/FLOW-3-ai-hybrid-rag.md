# Flow 3 — AI query (hybrid RAG) (canonical)

**Diagram (PNG):** [`flow3_ai_query.png`](../../prd/flow3_ai_query.png)  
**Related phases:** `5` (AI), `3` (CRM), `6` (reliability), `8` (APIs)  
**Schemas:** `ai.query.completed.v1.json`, `OrgContext.json`

## Summary

User asks a **natural-language** question. **Gateway** authenticates JWT and enforces org + tool policy; **`ai.server`** (Go + Asynq) runs the **planner / LangGraph-style** orchestration and fans out retrieval: **OpenSearch BM25** keyword hits, **pgvector cosine** semantic hits, **structured CRM** reads via **Connectra/VQL**, and optional connectors. **BM25 + vector run in parallel** and merge via **RRF (Reciprocal Rank Fusion)** into **top-K context** for the configured model **grounded generation** plus **tool calls** → **structured response + citations** back to client. Token stream uses **SSE** (see [`DECISIONS.md`](../../DECISIONS.md)); cost/token metering ties to the **credit ledger** (Slice B).

## Actors

- **User** — NL question
- **Gateway** — JWT, org isolation, tool allowlist, approval gates for writes
- **ai.server** — orchestration, LangGraph-style planner, workers
- **OpenSearch** — BM25 keyword search on CRM index (Connectra)
- **pgvector** — cosine similarity on embeddings
- **Connectra** — authoritative structured rows + VQL
- **VQL** — structured queries via gateway converter (`vql_converter.py`) → Connectra `where` JSON
- **RRF fusion** — rank merge of parallel retrievers
- **LLM** — grounded answer + optional tools
- **Kafka** — `ai.query.completed` for metering

## Step-by-step

1. Client uses **product GraphQL** or **`ai.server` HTTP** behind gateway (see `AIServerClient` / Phase 5 docs) with prompt + optional entity scope.
2. Load **OrgContext**; enforce model tier, token budget, tool allowlist.
3. **Parallel retrieve:** BM25 (OpenSearch), vectors (pgvector), SQL/CRM summaries, BQL if configured.
4. **RRF** merge hit lists → `top_k` context bundle with provenance for citations.
5. LLM **grounded gen**; emit tool calls to gated executors when needed.
6. Stream tokens over **SSE** to web client.
7. Persist `ai_queries` + usage; emit **`ai.query.completed`**.

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| Kafka | `ai.query.completed` |
| Redis | `ai:session:{session_id}`, `ratelimit:ai:{org_id}` |
| Postgres | `ai_queries`, `ai_memories` (optional), `contacts` / `companies` reads |
| OpenSearch | CRM / knowledge indices for BM25 |
| pgvector | Embedding tables keyed by org + entity |

## Error paths

- **429** — org or global model quota exceeded.
- **Retriever partial failure** — degrade to available sources; annotate response.
- **Tool denied** — return explanation + safe fallback answer.
- **Hallucination guard** — require citations tied to retrieved chunk ids.

## Cross-links

- **Decisions:** [`docs/DECISIONS.md`](../../DECISIONS.md) § AI satellite; **runtime split:** [`OPEN-DECISIONS-RESOLVED.md`](../../OPEN-DECISIONS-RESOLVED.md).
- Phase 5 vertical: [`../5.Contact360 AI workflows/AI-AGENT-VERTICAL-MVP.md`](../../5.Contact360%20AI%20workflows/AI-AGENT-VERTICAL-MVP.md).
- `docs/prd/Contact360 — AI Agent Internal Reasoning & Impleme.md`, `ai-agent-reasoning.md`.
- Phase 5 PRD: `docs/prd/Read all the above and previous prompts and then t (6).md`.
- Flow 1 (embeddings on new contacts), Flow 4 (AI-assisted campaign copy).
