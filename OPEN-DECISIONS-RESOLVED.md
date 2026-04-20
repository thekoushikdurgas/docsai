# Open questions — resolved defaults (slice unblockers)

**Last reviewed:** 2026-04-19  
These are **working decisions** for engineering alignment. Change via ADR + `DECISIONS.md` if product overrides.

| Topic | Decision | Rationale |
| ----- | -------- | --------- |
| **B — PSP** | **Stripe** for global card; **Razorpay** (or regional) for India when billing address is IN; gateway abstracts a single **BillingPort** interface. | Minimizes duplicate webhook logic; hybrid matches common SaaS patterns. |
| **C — Merge vs UUID5** | **UUID5 from normalized identity fields is canonical** for insert; **dedupe/merge** never silently rewrite UUID5 — conflicts surface as merge candidates or manual resolution. | Matches Connectra + extension contract in `DECISIONS.md`. |
| **G — LangGraph / planner runtime** | **Planner + tool orchestration in `ai.server`**; gateway holds **JWT, org context, tool allowlist, approval gates**, and proxies SSE streams. Gateway **does not** embed the full graph runtime. | Keeps heavy deps and scaling on the AI worker pool; gateway stays thin and auditable. |
| **H — CQL vs workflow DSL** | **CQL + campaign.server** is the **only** sequence program for MVP; separate **workflow DSL** (`188-workflows`) remains **future** / experimental behind a flag. | One sequencer reduces duplicate audience + send paths. |
| **I — Public REST shape** | **Gateway-shaped CRM DTOs** (stable JSON:API-style resources), **not** raw Connectra payloads — Connectra remains internal behind gateway. | Partners should not depend on internal satellite schemas. |
