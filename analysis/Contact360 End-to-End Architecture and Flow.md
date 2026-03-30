# Contact360 End-to-End Architecture and Flow

## Executive Summary

Contact360 is a multi-phase SaaS product that evolves from a solid foundation and codebase setup (0.x.x) into a full platform covering user/billing, email, contact/company data, extensions, AI workflows, reliability, deployment, APIs, ecosystem integrations, and campaigns. The architecture should support this roadmap while letting the team start lean (few deployable units) and gradually separate concerns into independently scalable services.[^1]

The recommended approach is a TypeScript/Next.js frontend plus Python/FastAPI backends with PostgreSQL and Redis, organized as a monorepo with multiple logical codebases (packages/services) for web UIs and backends, and a shared infrastructure layer. This report describes the codebase layout, data model boundaries, request and data flows, and how they map onto the Contact360 phases.

## High-Level System Architecture

The core of Contact360 is a multi-tenant SaaS system with workspaces, users, billing/credits, email infrastructure, and contact/company records that are reused across features. Initial architecture should favor a modular monolith pattern inside a single backend codebase, but structured so that core domains (Auth/Billing, Email, Contacts, AI workflows) can become separate services later without major rewrites.[^2][^3]

At a high level, the system consists of:

- Web application frontend (Next.js) for the main app UI plus a marketing site and admin console.
- Backend API layer (FastAPI) exposing authenticated REST/JSON endpoints and webhooks.
- Asynchronous workers/queues for email sending, tracking, enrichment, and heavy jobs.
- PostgreSQL as the primary relational database for strong consistency and relational queries.
- Redis for caching, rate limiting, task queues, and ephemeral state (sessions, locks).
- Object storage (e.g., S3-compatible) for assets like email templates, exports, and attachments.

## Codebase and Repository Layout

The recommended structure is a single Git repository (monorepo) with multiple top-level packages that behave like independent codebases but share tooling and CI/CD. This matches the roadmap’s emphasis on a strong Phase 0 foundation and makes it easier to evolve to services as scale grows.[^3]

A suggested layout:

- `/apps/web-frontend` – Next.js (TypeScript) app
  - Marketing pages, main dashboard, contacts UI, email campaign builder
- `/apps/admin-frontend` – Optional separate Next.js app for internal admin/ops
- `/apps/browser-extension` – Extension UI (e.g., for LinkedIn/Sales Navigator later in Phase 4)
- `/services/core-api` – FastAPI backend (modular monolith) with domain modules
  - `auth_billing` – User, workspace, subscription, credits
  - `email_engine` – Templates, providers, send queues
  - `contacts` – Contact/company data, segmentation, search
  - `workflows` – Orchestration and AI workflows (Phase 5)
- `/services/email-worker` – Worker service (FastAPI/Celery/RQ) consuming queues
- `/services/integration-gateway` – Webhook receiver and third-party integrations (Phase 8–9)
- `/infra` – Infrastructure as code (Terraform/CDK), Dockerfiles, Kubernetes manifests
- `/packages/shared` – Shared libraries (Pydantic models, TypeScript SDK, design system components)

This layout gives clear separation between UIs, core API, background processing, and infra, while still letting the team share types, DTOs, and patterns.[^2]

## Database and Data Model Boundaries

The primary database is a single PostgreSQL cluster with schemas grouped by bounded contexts: `auth_billing`, `email`, `contacts`, `workflows`, etc. Within each schema, tables are designed for multi-tenancy (workspace_id / organization_id) and extensibility via custom fields and JSONB for flexible attributes.[^4][^5]

Key entities:

- User, Workspace/Account, Role/Permission (Phase 1).
- Subscription, Plan, Invoice, Payment, CreditLedger (Phase 1).
- EmailTemplate, EmailMessage, ProviderConfig, SendingJob, BounceEvent, OpenEvent, ClickEvent (Phase 2).
- Contact, Company, List/Segment, ImportJob, EnrichmentResult (Phase 3).
- Workflow, Node, Execution, LogEntry (Phase 5).

This structure maps directly to the phase breakdowns already defined for user/billing, email system, and contact/company management, keeping write paths localized while allowing cross-domain reads via joins or views.[^5][^2][^4]

## Core Request and Data Flows

### 1. User Onboarding and Workspace Setup (Phase 1)

1. A visitor lands on the marketing site, clicks “Get Started,” and is redirected to the app domain (Next.js app).[^2]
2. Frontend collects email, password, and workspace details, then calls `POST /auth/register` on `core-api`.
3. Core API creates User, Workspace, and initial Subscription records, assigning a plan and seeding CreditLedger entries (monthly credits).[^2]
4. An email verification message is enqueued; the email-worker picks it up and sends via configured provider.[^5]
5. Once the email link is clicked, the verification endpoint marks the user as verified and logs an audit event.

Data moves from frontend to `core-api`, into PostgreSQL, and then out to the email provider via the worker’s queue.[^5][^2]

### 2. Billing, Payments, and Credits (Phase 1)

1. From the billing page, the frontend fetches current subscription and usage via `GET /billing/summary`.
2. To upgrade, the frontend creates a checkout session via `POST /billing/checkout` which calls Stripe and returns a hosted checkout URL.[^2]
3. Stripe webhooks hit the `integration-gateway` (or a dedicated billing endpoint in core-api), which validates signatures and updates Subscription, Invoice, and CreditLedger.[^2]
4. Credit grants (monthly resets) run via scheduled jobs in the worker service, updating balances based on active plans.

This flow ensures all money and credit movements are centrally recorded, satisfying audit and reliability needs from day one.[^3][^2]

### 3. Email Composition, Sending, and Tracking (Phase 2)

1. The user creates a new campaign or single email from the frontend, which calls `POST /email/campaigns` or `POST /email/send`.
2. Core API validates template variables, checks credits, and persists EmailTemplate, EmailMessage, and SendingJob records.[^5]
3. Email-worker polls the sending queue, batches messages per provider, enforces rate limits, and calls providers’ APIs.
4. Providers send events (delivery, bounce, complaint, open, click) back via webhooks to integration endpoints, which update events tables and denormalized metrics on EmailMessage.[^5]
5. Frontend dashboards read aggregated statistics (open rate, click-through, bounce rate) using optimized queries and materialized views.

This end-to-end loop—from campaign creation through sending and tracking—forms the backbone of later features like contact engagement scores and AI workflows.[^5]

### 4. Contact and Company Management (Phase 3)

1. CSV import: The user uploads a CSV; frontend calls `POST /contacts/import` to create an ImportJob and uploads the file to object storage.[^4]
2. Worker reads the file in chunks, normalizes emails, validates data, and upserts Contact and Company records with proper workspace scoping.[^4]
3. The system builds search indexes (PostgreSQL full-text or trigram) and segment membership based on filters.[^4]
4. Email engagement metrics from Phase 2 are periodically rolled up into contacts (opens, clicks, replies), enabling scoring and segmentation.[^4][^5]

The contact/company domain acts as a central CRM-like hub that every feature in later phases can rely on.[^4]

### 5. Workflows and Automation (Phase 5)

1. The user designs workflows via a visual builder in the frontend, which saves a Workflow graph (nodes, edges, conditions) to the workflows schema.
2. Trigger events (e.g., new contact, email opened) are produced into a queue or event log.
3. Worker instances evaluate workflows, schedule actions (send email, update field, call external API), and push tasks to the email engine or integration gateway.

AI-specific nodes (enrichment, scoring, text generation) can be added using the same execution engine, abstracting underlying model providers.

## Environments and Deployment Flow

Given the multi-phase roadmap, environments should be locked in during Phase 0 so that future work is consistent and safe.[^3]

Recommended environments:

- `dev` – Local development with Docker Compose for all services (frontend, core-api, worker, PostgreSQL, Redis, mail sandbox).
- `staging` – Single-region, production-like environment for QA and manual testing before releases.
- `prod` – Production environment with autoscaling for core-api and workers, managed PostgreSQL, managed Redis, and provider credentials.

Deployment pipeline:

1. Developer pushes to feature branches; CI runs tests and type checks across all apps and services.
2. Merge to `main` triggers build artifacts (Docker images) for frontend and backends.
3. Tagged releases (e.g., `v1.2.0`) trigger staged deployments: first to staging, then to prod after smoke tests.
4. Database migrations are run via a controlled process (e.g., Alembic for FastAPI) and rolled out per environment.

This flow aligns with the Phase 7 “Contact360 deployment” focus while ensuring earlier phases already benefit from consistent delivery.[^3]

## Observability, Security, and Reliability

From Phase 0 and 6, the system must incorporate observability, security, and reliability primitives that scale with additional domains.[^3]

Key practices:

- Centralized logging and tracing across frontend, core-api, and workers.
- Metrics on queues, success/failure rates, provider-level email performance, and billing events.
- Strong authentication (JWT or session-based), role-based access control, and workspace isolation baked into every API call.[^2]
- Secrets management via environment-specific vaults; no secrets in code or configs.

These cross-cutting concerns underpin later phases such as ecosystem integrations and email campaigns without requiring major rework.

## Mapping Architecture to Roadmap Phases

- Phase 0 – Set up monorepo, base Next.js and FastAPI skeletons, PostgreSQL/Redis infra, CI/CD, and observability.
- Phase 1 – Flesh out `auth_billing` module, Stripe integration, credit ledger, and basic user/workspace UIs.[^2]
- Phase 2 – Implement `email_engine` module, worker service, provider integrations, and dashboards.[^5]
- Phase 3 – Build `contacts` module, CSV imports, enrichment hooks, search, and contact UI.[^4]
- Phase 4 – Add browser extension app, integration gateway endpoints for external data sources.
- Phase 5 – Introduce `workflows` engine and AI nodes using existing email and contacts domains.
- Phase 6–10 – Hardening, scaling, deployment refinements, public APIs, integrations, and campaign sophistication, largely reusing the same architectural spine.

This phase mapping ensures that each new capability builds on existing domains, keeping the architecture coherent and avoiding one-off systems that are hard to maintain.[^1]

## Conclusion

Contact360’s end-to-end architecture should be designed as a modular, multi-tenant SaaS backbone that can start as a monorepo-based modular monolith and evolve into a more distributed system as scale and complexity grow. Clear separation of UI apps, core API, workers, and infrastructure, combined with well-defined data model boundaries and request flows, will support the full 0.x.x–10.x.x roadmap without structural rewrites.[^3]

---

## References

1. [my contact360 project 
0.x.x - Foundation and pre-product stabilization and codebase setup
1.x.x - Contact360 user and billing and credit system
2.x.x - Contact360 email system
3.x.x - Contact360 contact and company data system
4.x.x - Contact360 Ext...

... AI workflows
6.x.x - Contact360 Reliability and Scaling
7.x.x - Contact360 deployment
8.x.x - Contact360 public and private apis and endpotints 
9.x.x - Contact360 Ecosystem integrations and Platform productization
10.x.x - Contact360 email campaign](https://www.perplexity.ai/search/4e088799-5113-4402-baae-4a09d1e2e81f) - Perfect! I've created a comprehensive roadmap document for your Contact360 project. Here's what I've...

2. [Break down Phase 1 Contact360 user and billing and credit system tasks](https://www.perplexity.ai/search/f5548baa-5c5c-46fc-9b86-41297701a68e) - Perfect! I've created a comprehensive Phase 1 breakdown document with detailed task lists for the Us...

3. [Break down Phase 0 Foundation and pre-product stabilization and codebase setup tasks](https://www.perplexity.ai/search/9a704036-c048-4c5b-9719-2ac1541ca448) - Phase 0 is where you make Contact360 “production-ready to build on” by locking in architecture, repo...

4. [Break down Phase 3 Contact360 contact and company data system  tasks](https://www.perplexity.ai/search/7083c925-0dde-4b96-8d1b-fb19983efee1) - Perfect! I've created a comprehensive Phase 3 Contact & Company Management breakdown for Contact360....

5. [Break down Phase 2 Contact360 email system tasks](https://www.perplexity.ai/search/12d32546-85de-406b-b9f0-496989bb9029) - I've created a comprehensive Phase 2 email system breakdown for Contact360. It covers all 7 major se...

