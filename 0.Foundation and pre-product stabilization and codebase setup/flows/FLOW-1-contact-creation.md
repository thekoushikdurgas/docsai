# Flow 1 — Contact creation (canonical)

**Diagram (PNG):** [`flow1_contact_creation.png`](../../prd/flow1_contact_creation.png)  
**Related phases:** `0` (foundation), `3` (CRM data), `5` (AI scoring), `6` (search), `8` (APIs)  
**Schemas:** `Contact.json`, `contact.created.v1.json`, `OrgContext.json`

## Summary

End user or integration creates a contact through the **Web UI** (Next.js dashboard) → **`POST /graphql` on the gateway** (`contact360.io/api`, Strawberry) with **JWT**; the gateway resolves org context and sets **`SET LOCAL app.current_org_id`** for **RLS** on gateway Postgres where applicable, and forwards CRM reads/writes to **Connectra** (`sync.server`) via **`ConnectraClient`** with **`X-API-Key`**. Optional async fan-out: **`contact.created`** (or equivalent) to **Kafka** for notifications, **AI lead score + embedding** (pgvector), and **OpenSearch** sync (`contacts-v1` index on Connectra).

## Actors

| Actor | Role |
| ----- | ---- |
| Web UI | GraphQL mutations / queries via **`POST /graphql`** (see gateway schema) |
| API Gateway (`contact360.io/api`) | JWT validation, **RLS session** (`app.current_org_id`), rate limits, satellite keys |
| Connectra (`sync.server`) | System of record for contacts/companies; HTTP + **`X-API-Key`** from gateway |
| PostgreSQL | System of record; **RLS enforced** per tenant |
| Kafka | Durable fan-out for async workflows |
| Notification service | Slack/email to rep (`notify rep`) |
| AI Agent | Lead score + `embed` to **pgvector** |
| Search sync consumer | `sync doc` → **upsert** OpenSearch `contacts-v1` |
| Redis | Hot cache for read path (see contracts) |

## Step-by-step

1. Browser submits create payload with bearer token to **`POST /graphql`**.
2. Gateway resolves user → org, sets **`SET LOCAL app.current_org_id`** for **RLS** on tenant tables it owns.
3. Gateway validates business rules vs `Contact.json`, checks credits/entitlements (`OrgContext`) where enforced.
4. Persist via **Connectra** HTTP (`POST /contacts/` or batch upsert paths) — **not** a separate “Fastify CRM” service in the current architecture.
5. Publish **`contact.created`** envelope (`docs/docs/json_schemas/_meta-schema.event.json`) with payload `contact.created.v1.json`.
6. **Parallel consumers** (diagram): notify rep; score + embed contact; upsert search document.
7. **Live UI:** after async work, push lightweight updates to the UI (see `docs/DECISIONS.md` — WebSocket vs SSE split).

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| HTTP | GraphQL through gateway; Connectra REST from gateway with org-scoped calls |
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

- **Architecture:** [`docs/DECISIONS.md`](../../DECISIONS.md) (gateway, Connectra, RLS).
- **Foundation v0 (detailed slice):** [`0.Foundation…/08-flows/02-contact-create-flow-v0.md`](../08-flows/02-contact-create-flow-v0.md) and [`03-contact-list-flow-v0.md`](../08-flows/03-contact-list-flow-v0.md).
- **Connectra / VQL spine:** [`3.Contact360 contact and company data system/50-connectra-vql-spine.md`](../../3.Contact360%20contact%20and%20company%20data%20system/50-connectra-vql-spine.md).
- **Flowchart:** [`docs/flowchart/`](../../flowchart/) — contacts/VQL diagrams where applicable.
- Phase 0 PRD tasks: `docs/prd/Read all the above and previous prompts and then t (1).md`.
- `docs/prd/contact360_detailed_flow.md`, `docs/prd/contact360_architecture.md`.
- Flow 2 (CSV enrichment), Flow 3 (RAG on indexed contact), Flow 5 (extension capture).
