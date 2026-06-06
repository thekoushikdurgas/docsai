<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Codebases – Contact360

## Frontend

1. Web App (Next.js)
2. Admin Panel
3. Chrome Extension

## Backend

4. API Gateway
5. CRM Service
6. Email Service
7. Phone Service
8. Campaign Service
9. Connector Service (VQL)
10. Storage Service
11. AI Agent Service
12. Notification Service
13. Integration Service
14. MCP (Control Panel)
15. AI MCP (Chat-based interface)

---

## Total Codebases: 15

Here's the full **Contact360 Codebase Map** — 935 lines covering all 15 repositories in detail.  Here's a structured overview of every decision inside:

***

## Repo Strategy

All 15 codebases live inside a single **Turborepo monorepo** under `apps/`, with 7 shared `packages/` for types, Kafka wrappers, auth middleware, logger, UI components, errors, and config.  CI only runs affected apps on each PR — so if you only change `email-service`, the other 14 are skipped.

## Language Matrix

| Layer | Language | Framework |
| :-- | :-- | :-- |
| Frontend (web, admin) | TypeScript | Next.js 15 |
| Chrome Extension | TypeScript | MV3 + React + Vite/CRXJS |
| API Gateway | **Go 1.22** | Gin + Kong |
| All NestJS services (5–9, 12–14) | TypeScript | NestJS 10 + Prisma/BullMQ |
| Storage | TypeScript | Fastify 4 + Drizzle |
| AI Agent + AI MCP | **Python 3.12** | FastAPI + LangGraph |

## Service-by-Service Highlights

- **API Gateway (Go)** — single public entry point with JWT validation, Redis rate limiting (token bucket), response caching, and clean route table mapping every path to its upstream
- **CRM Service** — NestJS + Prisma with full multi-tenant RLS, REST + GraphQL dual interface, OpenSearch sync via Kafka consumer, and 5 distinct event types published
- **Email Service** — waterfall enrichment (Pattern Engine → Hunter.io → Apollo → SMTP Verify → ZeroBounce) as individual providers behind a `waterfall.service.ts` orchestrator, all driven by BullMQ
- **Phone Service** — Truecaller/NumVerify discovery, Twilio carrier lookup, TRAI DND check (Redis-cached 24h), plus SMS (Twilio/MSG91) and WhatsApp (Meta Business API) sending
- **Connector Service (VQL)** — PEG.js grammar parses your custom VQL DSL into an AST, plans multi-source queries across PostgreSQL + OpenSearch + Redis + pgvector, used by campaigns for audience segmentation
- **AI Agent Service (Python)** — LangGraph orchestrates a `plan → retrieve → fuse → generate → tools` loop with hybrid RAG (BM25 + cosine merged via RRF), lead scoring, and embedding generation
- **MCP (Control Panel)** — routes each AI query to the right LLM model via intent classification, managing per-org model config, system prompts, token budgets, and tool registries
- **AI MCP (Chat)** — full conversational agent with persistent pgvector memory, 5 tool categories (contact, deal, campaign, email, analytics), a **human-in-the-loop approval gate** before any write action, plus Whisper voice input


## Communication Patterns

```
Sync  (REST)  — all client → api-gateway → services
Async (Kafka) — all mutations publish events, consumers react independently
Stream (SSE)  — jobs, enrichment, chat responses, live activity feed
WebSocket     — AI MCP chat streaming
```


## Port Assignments

All services run on deterministic ports: `3000–3090` for TS services, `8000` for the Go gateway, `8100` for AI Agent, `8200` for AI MCP — making local `docker-compose` dev straightforward with no conflicts.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://help.salesforce.com/s/articleView?id=data.c360_a_c360datamodel.htm\&language=en_US\&type=5

[^2]: https://aws.amazon.com/solutions/guidance/building-a-customer-360-data-product-in-a-data-mesh-on-aws/

[^3]: https://www.databricks.com/resources/architectures/c360-reference-architecture-for-insurance

[^4]: https://help.salesforce.com/s/articleView?id=data.c360_a_cloud_information_model_individual_and_contact_points.htm\&language=en_US\&type=5

[^5]: https://findskill.ai/skills/claude-code/codebase-architecture-explainer/

[^6]: https://www.amdocs.com/sites/default/files/Amdocs-MS360-Appledore-Solution-Profile-20Sep20.pdf

[^7]: https://www.justdial.com/Bangalore/Contactpoint-360-Koramangala/080PXX80-XX80-231201135904-T6Y9_BZDET

[^8]: https://ranjankumar.in/from-unknown-codebase-to-architecture-document-a-complete-practitioners-guide

[^9]: https://auth0.com/blog/an-introduction-to-microservices-part-1/

[^10]: https://ca.linkedin.com/company/contact-point-360

[^11]: https://stackoverflow.com/beta/discussions/79129702/what-would-be-a-good-software-architecture-implementation-for-a-contacts-applica

[^12]: https://www.youtube.com/watch?v=7SKX9gVjDzc

[^13]: https://dir.indiamart.com/impcat/backend-support-services.html

[^14]: https://www.nextiva.com/blog/contact-center-architecture.html

[^15]: https://www.nokia.com/asset/i/201751/

[^16]: https://ieeexplore.ieee.org/document/11281189/

[^17]: https://scipost.org/10.21468/SciPostPhysCodeb.24-r0.1

[^18]: https://scipost.org/10.21468/SciPostPhysCodeb.16-r1.1

[^19]: https://ieeexplore.ieee.org/document/11395666/

[^20]: https://oarjpublication.com/journals/oarjet/node/350

[^21]: https://ieeexplore.ieee.org/document/11389693/

[^22]: https://arxiv.org/abs/2603.00601

[^23]: https://ulopenaccess.com/papers/ULIRS_V02I04/ULIRS20250204_014.pdf

[^24]: https://arxiv.org/abs/2506.09242

[^25]: https://academic.oup.com/jamiaopen/article/doi/10.1093/jamiaopen/ooaf067/8186991

[^26]: https://figshare.com/articles/journal_contribution/Software_Architecture_Documentation_in_Practice_Documenting_Architectural_Layers/6609596/1/files/12101714.pdf

[^27]: https://www.emerald.com/insight/content/doi/10.1108/ACI-12-2020-0159/full/pdf?title=an-architecture-as-a-code-framework-to-manage-documentation-of-it-projects

[^28]: https://figshare.com/articles/report/Experience_Using_the_Web-Based_Tool_Wiki_for_Architecture_Documentation/6573647/1/files/12059594.pdf

[^29]: https://arxiv.org/pdf/2308.09978.pdf

