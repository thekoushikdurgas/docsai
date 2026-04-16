<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Contact360 Architecture Overview

## System Type

AI-driven, microservices-based CRM platform

## Core Layers

### 1. Presentation Layer

- Next.js Web App
- Admin Panel
- Chrome Extension


### 2. API Layer

- API Gateway (BFF)
- GraphQL + REST hybrid


### 3. Microservices Layer

- CRM Service
- Email Service
- Phone Service
- Campaign Service
- Connector Service (BQL)
- Storage Service
- AI Agent Service
- Notification Service
- Integration Service
- MCP (Control Panel)


### 4. Data Layer

- PostgreSQL (Primary DB)
- OpenSearch (Search Engine)
- Redis (Caching + Queue)
- S3 (File Storage)
- Vector DB (AI context)


### 5. AI Layer

- LLM (OpenAI / local)
- Tool calling
- Workflow automation

---

## Key Principles

- Microservices architecture
- Event-driven (Kafka / Redis streams)
- Multi-tenant SaaS
- AI-first workflows

Your complete **Contact360 Architecture Blueprint v2.0** has been generated as a downloadable file — 1,190 lines covering every layer you outlined.

Here's a precise breakdown of what was documented for each layer you specified:

***

## What's Covered Per Layer

### Presentation Layer

```
All three clients are fully spec'd — **Next.js Web App** (with every route, AI-native components like `<LeadScoreBadge />`, `<NextBestAction />`, `<AIDraftEmail />`), **Admin Panel** (tenant management, model monitoring, feature flags), and **Chrome Extension** (MV3 architecture, Truecaller-style enrichment flow, GDPR compliance framework). 
```


### API Layer — GraphQL + REST Hybrid

The BFF pattern is fully designed: **Kong** handles JWT validation, rate limiting, and `org_id` injection from claims; **Apollo Federation v2** exposes a single GraphQL endpoint with 5 subgraphs (crm, campaign, ai, user, analytics); **REST** handles service-to-service calls with cursor-based pagination and structured error formats.

### Microservices — All 10 Services

Every service has port, tech stack, responsibilities, Kafka events, and DB choice. Two new additions beyond the previous version:

- **Connector Service (BQL)** — a custom Business Query Language DSL that translates plain-language queries into multi-source fetches across PostgreSQL + OpenSearch + Redis, used by the AI Agent, Campaign, and Analytics services
- **MCP (Model Control Panel)** — central registry for all ML models, LLM config per org, prompt versioning, A/B testing, and AI cost tracking


### Data Layer — All 5 Stores

PostgreSQL schema with full RLS, pgvector index, and multi-tenant isolation; OpenSearch index mappings with sync strategy; Redis key namespaces for cache/queues/sessions; S3 folder structure with lifecycle policies; and hybrid RAG design using Reciprocal Rank Fusion (pgvector + OpenSearch merged results).

### AI Layer — LLM + Tool Calling + Workflow Automation

LLM selection logic (GPT-4o → Claude → Gemini → local Ollama fallback chain), complete tool calling implementation with Human-in-the-Loop for destructive actions, and no-code workflow automation triggers with JSON workflow definitions stored in PostgreSQL.[^1][^2]

***

## Key Architectural Decisions Worth Noting

| Decision | Rationale |
| :-- | :-- |
| **BQL Connector Service** | Single query surface for AI Agent + campaigns + analytics — avoids N service calls from one agent action [^2] |
| **MCP as separate service** | Model drift detection, A/B testing, and LLM cost control need a dedicated control plane [^3] |
| **Apollo Federation** | GraphQL subgraphs let each service own its schema without a monolithic GraphQL server |
| **Hybrid RAG (BM25 + pgvector)** | Keyword search catches exact matches, vector search catches semantic intent — combined via RRF gives best recall [^4] |
| **Kafka + Redis Streams dual bus** | Kafka for durable async events (enrichment, campaigns), Redis Streams for sub-100ms real-time UI updates [^5] |
| **Continuous feedback loop to MCP** | Every user action (accept/edit/ignore AI output) feeds model retraining — the system improves automatically [^3][^6] |

<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.pluralsight.com/resources/blog/ai-and-data/architecting-microservices-agentic-ai

[^2]: https://www.klover.ai/the-ultimate-guide-to-integrating-ai-agents-into-microservice-ecosystems/

[^3]: https://web.superagi.com/the-ultimate-guide-to-implementing-ai-driven-crm-a-step-by-step-roadmap-for-large-enterprises/

[^4]: https://wjaets.com/node/754

[^5]: https://www.confluent.io/blog/event-driven-multi-agent-systems/

[^6]: https://sales-mind.ai/blog/ai-crm-integration-best-practices

[^7]: https://software.iquasar.com/blog/ai/integrating-ai-in-crm-best-practices-and-strategies/

[^8]: https://www.itransition.com/ai/crm

[^9]: https://wjaets.com/content/ai-driven-crm-solutions-cloud-architecture-and-process-automation-comprehensive-analysis

[^10]: https://www.linkedin.com/pulse/implementing-ai-powered-crm-best-practices-sentia-ai-xbopc

[^11]: https://www.riministreet.com/blog/5-best-practices-for-ai-crm-readiness/

[^12]: https://appstekcorp.com/blog/design-patterns-for-agentic-ai-and-multi-agent-systems/

[^13]: https://www.abbacustechnologies.com/how-to-build-an-ai-powered-crm-system/

[^14]: https://www.linkedin.com/pulse/ai-agents-microservices-drawing-parallels-system-design-shakirov-w2cbe

[^15]: https://www.microsoft.com/en-us/dynamics-365/blog/business-leader/2024/03/04/ai-in-crm-and-erp-systems-2024-trends-innovations-and-best-practices/

[^16]: https://blog.devgenius.io/design-patterns-for-agentic-ai-systems-89457710f19b

[^17]: https://www.ijisrt.com/intelligent-automation-in-crm-leveraging-einstein-bots-for-enhanced-customer-support

[^18]: https://ijsrcseit.com/index.php/home/article/view/CSEIT251112213

[^19]: https://wjaets.com/node/561

[^20]: https://jier.org/index.php/journal/article/view/3504

[^21]: https://ijsrcseit.com/index.php/home/article/view/CSEIT251117132

[^22]: https://www.ijaidr.com/research-paper.php?id=1692

[^23]: https://ijaems.com/detail/integrating-ai-driven-automated-code-review-in-agile-development-benefits-challenges-and-best-practices/

[^24]: https://www.allmultidisciplinaryjournal.com/search?q=F-24-295\&search=search

[^25]: https://www.ijraset.com/best-journal/implementing-ai-driven-efficiency-best-practices-for-intelligent-order-processing-in-sap

[^26]: https://www.emerald.com/insight/content/doi/10.1108/JBIM-07-2021-0332/full/pdf?title=artificial-intelligence-in-customer-relationship-management-literature-review-and-future-research-directions

[^27]: https://arxiv.org/html/2411.02305v1

[^28]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11382090/

[^29]: https://e-jurnal.lppmunsera.org/index.php/jsii/article/download/8282/2989

[^30]: https://universepg.com/public/storage/journal-pdf/The impact of artificial intelligence (AI) on customer relationship management.pdf

[^31]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11784820/

[^32]: http://pen.ius.edu.ba/index.php/pen/article/view/539

[^33]: https://arxiv.org/pdf/2208.11404.pdf

