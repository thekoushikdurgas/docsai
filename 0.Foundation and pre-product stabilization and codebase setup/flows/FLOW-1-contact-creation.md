# Flow 1 — Contact creation (canonical)

**Diagram (PNG):** [`flow1_contact_creation.png`](../../prd/flow1_contact_creation.png)  
**Related phases:** `0` (foundation), `3` (CRM data), `5` (AI scoring), `6` (search), `8` (APIs)  
**Schemas:** `Contact.json`, `contact.created.v1.json`, `OrgContext.json`

## Summary

End user or integration creates a contact through the **Web UI** (Next.js in the reference architecture) → **API Gateway (Kong + JWT)** injects `org_id` → **CRM Service (Fastify + Prisma)** persists with **RLS** → publishes **`contact.created`** to **Kafka**. Consumers run **notifications**, **AI lead score + embedding** (pgvector), and **OpenSearch** sync (`contacts-v1` index).

## Actors

| Actor | Role |
| ----- | ---- |
| Web UI | `POST /contacts` (or `POST /v1/contacts` at gateway) |
| API Gateway (Kong) | JWT validation, **inject org_id**, rate limits |
| CRM Service | Business rules, Prisma/DB insert, outbox/event publish |
| PostgreSQL | System of record; **RLS enforced** per tenant |
| Kafka | Durable fan-out for async workflows |
| Notification service | Slack/email to rep (`notify rep`) |
| AI Agent | Lead score + `embed` to **pgvector** |
| Search sync consumer | `sync doc` → **upsert** OpenSearch `contacts-v1` |
| Redis | Hot cache for read path (see contracts) |

## Step-by-step

1. Browser submits create payload with bearer token.
2. Gateway resolves user → org, sets upstream headers / session vars for **RLS** (`app.current_org_id`).
3. CRM validates payload vs `Contact.json`, checks credits/entitlements (`OrgContext`).
4. `INSERT` into `contacts` (and optional `activities` audit row) under RLS.
5. Publish **`contact.created`** envelope (`docs/docs/json_schemas/_meta-schema.event.json`) with payload `contact.created.v1.json`.
6. **Parallel consumers** (diagram): notify rep; score + embed contact; upsert search document.
7. **Live UI:** after async work, push lightweight updates to the UI (see `docs/DECISIONS.md` — WebSocket vs SSE split).

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| HTTP | `POST /contacts` through Kong; org-bound |
| Kafka | Topic **`contact.created`**, key `org_id`, schema v1 |
| Redis | **`contact:{id}`** cache for reads (**5 min TTL** in reference diagram) |
| Postgres | `contacts`, `activities`, `import_jobs` (when import-sourced) |
| OpenSearch | Index **`contacts-v1`** (document id = contact id + org namespace) |
| pgvector | Embedding row linked to `contact_id` / org for semantic retrieval (Flow 3) |

## Error paths

- **401/403** — missing scope or wrong org; never leak other tenants.
- **409** — dedupe on `(org_id, email)` when rule enabled.
- **422** — validation against `Contact.json`.
- **Kafka unavailable** — transactional outbox in Postgres + relay worker; API may still **201** if row committed.
- **OpenSearch lag** — UI reads Postgres first; search catches up async.

## Cross-links

- Phase 0 PRD tasks: `docs/prd/Read all the above and previous prompts and then t (1).md`.
- `docs/prd/contact360_detailed_flow.md`, `docs/prd/contact360_architecture.md`.
- Flow 2 (CSV enrichment), Flow 3 (RAG on indexed contact), Flow 5 (extension capture).
