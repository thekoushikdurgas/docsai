# Contact360 Roadmap

This roadmap defines staged delivery across major versions.
Stage metadata standard for every stage:

- **Status**
- **Depends on**
- **Risk**
- **Definition of done**
- **KPI**
- **Ships in**

---

## Current focus

Delivery is currently centered on **billing and payments (Stage 1.3)** and **bulk validation hardening (Stage 2.4)**. Core **finder → verifier → results** flows remain the product backbone.

**Planning horizon:** near-term execution is **`1.x`–`6.x`** (this file + `docs/versions.md`). Strategic runway **`7.x`–`10.x`** is detailed in roadmap era sections below and in **`docs/architecture.md`** (*Planning horizon*). Optional per-minor notes: `docs/versions/version_*.md`. Strategic stages do not block current releases.

**Product surfaces:** Dashboard, marketing, DocsAI, and extension entry points are summarized in **`docs/frontend.md`**. Backend service index: **`docs/backend.md`**.

**Backend language runway:** The **main GraphQL backend** stays **Python** (`contact360.io/api`). **Go + Gin** is the default for new satellite services and Python-service rewrites; see **`docs/docs/backend-language-strategy.md`**.

**EC2 Go satellites (in-repo):** `EC2/job.server`, `EC2/s3storage.server`, `EC2/ai.server`, `EC2/log.server`, `EC2/extension.server` — see **`docs/docs/architecture.md`** (*Request paths*) and **`docs/docs/backend-language-strategy.md`** (*Satellite migration inventory*).

---

## VERSION 1.x — User, Billing and Credit System

### Stage 1.1 - User and Authentication System

**Status:** Completed
**Depends on:** Foundation platform setup
**Risk:** Session handling regressions across dashboard and extension
**Definition of done:** User can register, sign in, and begin usage with starter credits
**KPI:** Successful signup-to-first-action conversion, auth failure rate
**Ships in:** `1.0.0`

- Email signup and login
- Basic user profile
- Auto credit assignment (50 credits)
- Session management
- **Code pointers:** `contact360.io/app/src/context/RoleContext.tsx`, `contact360.io/api/app/main.py`

---

### Stage 1.2 - Credit Management System (CORE)

**Status:** Completed
**Depends on:** Stage 1.1
**Risk:** Incorrect deduction and lapse behavior can block valid user actions
**Definition of done:** Finder deductions and entitlement checks behave correctly under standard flows
**KPI:** Credit ledger consistency, blocked-request correctness at zero balance
**Ships in:** `1.0.0`

- Credit balance tracking
- Credit deduction per action: **Finder only** (Verifier is 0 credits per current GraphQL API policy)
- Free credits (50 on signup)
- Credit usage logs (basic)
- Block actions when credits = 0
- Credits lapse when premium pack validity ends
- **Code pointers:** `contact360.io/api/sql/apis/09_USAGE_MODULE.md`, `contact360.io/api/sql/apis/15_EMAIL_MODULE.md`, `contact360.io/app/src/lib/featureAccess.ts`

---

### Stage 1.3 - Billing and Payments

**Status:** In progress
**Depends on:** Stages 1.1, 1.2
**Risk:** Payment confirmation mismatch and delayed credit application
**Definition of done:** Users can purchase packs and receive credits through approved flow
**KPI:** Payment success-to-crediting time, failed payment flow rate
**Ships in:** `1.1.0`

- Credit purchase system
- 2-3 pricing plans for MVP
- Manual payment integration (MVP-appropriate)
- Credit packs without subscription complexity
- **Code pointers:** `contact360.io/app/src/services/graphql/billingService.ts`, `contact360.io/app/src/components/billing/UpiPaymentModal.tsx`, `contact360.io/api/sql/apis/14_BILLING_MODULE.md`

---

### Stage 1.4 - Analytics for the User (Minimal)

**Status:** Planned
**Depends on:** Stages 1.2, 1.3
**Risk:** Usage metrics mismatch with billing/credit records
**Definition of done:** Users can view basic usage and entitlement summary
**KPI:** Dashboard analytics view adoption, usage ledger consistency
**Ships in:** `1.2.0`

- User logs
- Credits used
- Package/expiry display
- **Code pointers:** `contact360.io/api/sql/apis/09_USAGE_MODULE.md`

---

### Stage 1.5 - Notifications (Minimal)

**Status:** Planned
**Depends on:** Stages 1.3, 1.4
**Risk:** False/late notifications reduce trust
**Definition of done:** In-app low-credit and payment-success cues are present and reliable
**KPI:** Notification delivery correctness, low-credit action conversion
**Ships in:** `1.2.0`

- Low credit warning (UI only)
- Payment success message
- No email automation in v1
- **Code pointers:** `contact360.io/app/`

---

### Stage 1.6 - Analytics Admin Panel (Basic Control)

**Status:** Planned
**Depends on:** Stages 1.2, 1.4
**Risk:** Admin actions without audit clarity
**Definition of done:** Admin can audit and adjust core user credit/package state
**KPI:** Admin correction turnaround time, audit completeness
**Ships in:** `1.2.0`

- View users (package and expiry)
- View credits
- Manually adjust credits
- View usage logs
- **Code pointers:** `contact360.io/admin/`, `lambda/logs.api/`

---

### Stage 1.7 - Security (Basic Layer)

**Status:** Planned
**Depends on:** Stage 1.1 and service middleware rollout
**Risk:** Abuse or high-volume spam traffic
**Definition of done:** Baseline throttling and abuse controls active on core APIs
**KPI:** Rate-limited abuse attempts, API error profile stability
**Ships in:** `1.2.0`

- Basic rate limiting
- Prevent spam usage
- **Code pointers:** `contact360.io/api/app/main.py`, service-level middleware/configuration

---

## VERSION 2.x — Email System

### Stage 2.1 - Email Finder Engine

**Status:** Completed
**Depends on:** Stages 1.1, 1.2
**Risk:** Provider inconsistency can reduce candidate quality
**Definition of done:** Finder returns candidates with normalized metadata and logging
**KPI:** Finder success rate, median response latency
**Ships in:** `2.0.0`

- Predefined pattern generation (10 formats)
- Generate possible valid email
- Historical logs on the same page
- High-throughput Go worker path (emailapigo) for heavy workloads
- Provider fallback and normalization
- **Code pointers:** `contact360.io/app/src/services/graphql/emailService.ts`, `contact360.io/app/src/hooks/useEmailFinderSingle.ts`, `lambda/emailapis/`, `lambda/emailapigo/`

---

### Stage 2.2 - Email Verification Engine

**Status:** Completed
**Depends on:** Stage 2.1
**Risk:** External signal variability (DNS/SMTP/provider behavior)
**Definition of done:** Verification returns normalized statuses across single and bulk flows
**KPI:** Verification completion rate, invalid classification precision
**Ships in:** `2.0.0`

- Integrate external verifier provider (Mailvetter and/or configured provider)
- Basic checks: Valid / Delivered-Catchall / Undelivered-Catchall / Invalid / Not Found; confidence when available
- DNS/SMTP/SPF/DMARC-based scoring
- **Code pointers:** `contact360.io/app/src/hooks/useEmailVerifierSingle.ts`, `backend(dev)/mailvetter/`, `contact360.io/api/sql/apis/15_EMAIL_MODULE.md`

---

### Stage 2.3 - Results Engine

**Status:** Completed
**Depends on:** Stages 2.1, 2.2
**Risk:** UI inconsistency in status/confidence representation
**Definition of done:** User sees best result plus auditable activity history
**KPI:** Result view completion rate, user action-to-result latency
**Ships in:** `2.0.0`

- Show best email and status with confidence when available
- Show logs of email validation
- **Code pointers:** `contact360.io/app/src/components/email/EmailFinderSingle.tsx`, `contact360.io/app/src/components/email/EmailVerifierBulkResults.tsx`

---

### Stage 2.4 - Bulk Processing — Validation

**Status:** In progress
**Depends on:** Stages 2.1, 2.2, 2.3
**Risk:** Partial failures in stream processors and resume flows
**Definition of done:** Upload, async processing, checkpoint resume, and output retrieval are reliable
**KPI:** Bulk job success rate, resume success rate, processing throughput
**Ships in:** `2.1.0`

- CSV upload (basic)
- Streaming batch processing with checkpointing and multipart upload
- Current concurrency in processors: finder stream = 3, verifier stream = 5
- **Code pointers:** `contact360.io/app/src/hooks/useNewExport.ts`, `contact360.io/jobs/app/processors/email_finder_export_stream.py`, `contact360.io/jobs/app/processors/email_verify_export_stream.py`, `lambda/s3storage/docs/multipart_upload_guide.md`

---

## VERSION 3.x — Contact and Company Data System

### Stage 3.1 - Advanced search filters (VQL)

**Status:** Planned
**Depends on:** Connectra index quality and VQL parser support
**Risk:** Filter complexity causing query performance regressions
**Definition of done:** Advanced contacts/companies filters are available and stable
**KPI:** Filter query success and latency percentiles
**Ships in:** `3.0.0`

---

### Stage 3.2 - Enrichment and deduplication

**Status:** Planned
**Depends on:** Stage 3.1
**Risk:** Duplicate profiles and confidence mismatch in enrichment
**Definition of done:** Enrichment quality improves with dedupe controls
**KPI:** Duplicate reduction rate, enrichment completeness
**Ships in:** `3.0.0`

---

### Stage 3.3 - Search quality and performance

**Status:** Planned
**Depends on:** Stages 3.1, 3.2
**Risk:** Index refresh and relevance tuning instability
**Definition of done:** Relevance and latency SLO targets are met
**KPI:** Search precision proxy score and P95 response time
**Ships in:** `3.0.0`

---

### Stage 3.4 - Dashboard search UX expansion

**Status:** Planned
**Depends on:** Stages 3.1, 3.3
**Risk:** UI complexity reducing discoverability
**Definition of done:** Advanced filtering flows are available in dashboard UX
**KPI:** Filter usage rate and successful search-to-export conversions
**Ships in:** `3.0.0`

---

## VERSION 4.x — Extension and Sales Navigator Maturity

### Stage 4.1 - Extension auth/session hardening

**Status:** Planned
**Depends on:** Appointment360 auth contracts
**Risk:** Session expiry and token refresh failures in browser context
**Definition of done:** Stable authenticated extension session lifecycle
**KPI:** Extension auth failure rate
**Ships in:** `4.0.0`

---

### Stage 4.2 - Sales Navigator ingestion optimization

**Status:** Planned
**Depends on:** Stage 4.1 and `salesnavigator` backend updates
**Risk:** Source-side data variability
**Definition of done:** Ingestion accuracy and throughput targets are met
**KPI:** Records ingested per run, ingestion error rate
**Ships in:** `4.0.0`

---

### Stage 4.3 - Sync integrity and conflict handling

**Status:** Planned
**Depends on:** Stages 4.1, 4.2
**Risk:** Duplicate writes and state divergence
**Definition of done:** Deterministic sync conflict handling is in place
**KPI:** Sync conflict auto-resolution success rate
**Ships in:** `4.0.0`

---

### Stage 4.4 - Extension telemetry and reliability

**Status:** Planned
**Depends on:** Stage 4.3 and `logs.api` integration
**Risk:** Limited visibility into extension production failures
**Definition of done:** Extension telemetry and error observability are production-ready
**KPI:** Error triage time and telemetry coverage
**Ships in:** `4.0.0`

---

## VERSION 5.x — AI Workflows

### Stage 5.1 - Contact AI integration in dashboard journeys

**Status:** Planned
**Depends on:** `contact.ai` API contracts and dashboard UX slots
**Risk:** UX friction from uncertain AI output quality
**Definition of done:** AI outputs are integrated into core user workflows
**KPI:** AI-assisted action adoption rate
**Ships in:** `5.0.0`

---

### Stage 5.2 - Confidence and explainability controls

**Status:** Planned
**Depends on:** Stage 5.1
**Risk:** Low trust if confidence/explanations are unclear
**Definition of done:** Confidence and explanation metadata are exposed and usable
**KPI:** AI-output acceptance rate
**Ships in:** `5.0.0`

---

### Stage 5.3 - AI usage limits and cost controls

**Status:** Planned
**Depends on:** Stages 1.2, 5.1
**Risk:** Unbounded model usage cost
**Definition of done:** Quotas and spending guardrails enforce expected limits
**KPI:** AI cost per active user and quota breach rate
**Ships in:** `5.0.0`

---

### Stage 5.4 - Prompt/version governance

**Status:** Planned
**Depends on:** Stages 5.1, 5.2
**Risk:** Prompt drift and regressions in production behavior
**Definition of done:** Prompt versioning and rollback governance are documented and operational
**KPI:** Prompt rollback time and AI regression incident count
**Ships in:** `5.0.0`

---

## VERSION 6.x — Reliability and Scaling

### Stage 6.1 - Reliability baseline and SLO definition

**Status:** Planned
**Depends on:** Stable 5.x AI/core APIs
**Risk:** Undefined reliability targets across services
**Definition of done:** SLOs and reliability error budgets are documented and monitored
**KPI:** SLO attainment rate
**Ships in:** `6.1.0`

---

### Stage 6.2 - Idempotency and consistency hardening

**Status:** Planned
**Depends on:** Stage 6.1
**Risk:** Duplicate writes in billing, jobs, and sync paths
**Definition of done:** All critical write paths enforce idempotency keys and reconciliation checks
**KPI:** Duplicate side-effect incident count
**Ships in:** `6.2.0`

---

### Stage 6.3 - Queue and worker resilience

**Status:** Planned
**Depends on:** Stage 6.2
**Risk:** Queue lag and worker poison-message failures
**Definition of done:** DLQ, replay, and retry controls are active for async workloads
**KPI:** Queue lag P95, successful replay rate
**Ships in:** `6.3.0`

---

### Stage 6.4 - Observability and diagnostics maturity

**Status:** Planned
**Depends on:** Stage 6.3
**Risk:** Slow incident triage without end-to-end telemetry
**Definition of done:** Correlated logs/traces/alerts are available across critical paths
**KPI:** Mean time to detect and resolve incidents
**Ships in:** `6.4.0`

---

### Stage 6.5 - Performance optimization wave

**Status:** Planned
**Depends on:** Stage 6.4
**Risk:** Throughput bottlenecks in gateway/search/bulk paths
**Definition of done:** Top latency hotspots are tuned with measurable gains
**KPI:** API P95 latency, throughput at steady load
**Ships in:** `6.5.0`

---

### Stage 6.6 - Storage and artifact lifecycle hardening

**Status:** Planned
**Depends on:** Stage 6.5
**Risk:** Artifact corruption/orphans and retention drift
**Definition of done:** Upload integrity, retention, and cleanup lifecycle are enforced
**KPI:** Artifact integrity success rate
**Ships in:** `6.6.0`

---

### Stage 6.7 - Cost reliability and budget guardrails

**Status:** Planned
**Depends on:** Stage 6.6
**Risk:** Uncontrolled cost growth under traffic spikes
**Definition of done:** Cost guardrails and usage-based throttles are enforced
**KPI:** Cost per active tenant/user
**Ships in:** `6.7.0`

---

### Stage 6.8 - Security and abuse resilience at scale

**Status:** Planned
**Depends on:** Stage 6.7
**Risk:** Abuse and attack amplification as traffic grows
**Definition of done:** Rate-limit and abuse protections are active and monitored
**KPI:** Blocked abuse attempts without false-positive surge
**Ships in:** `6.8.0`

---

### Stage 6.9 - Release candidate hardening for 7.0.0

**Status:** Planned
**Depends on:** Stages 6.1–6.8
**Risk:** Regression risk before deployment era rollout
**Definition of done:** Reliability RC tests and runbooks are signed off
**KPI:** RC defect escape rate
**Ships in:** `6.9.0`

---

## VERSION 7.x — Deployment

### Stage 7.1 - RBAC model and access control foundation

**Status:** Planned
**Depends on:** Stage 6.9
**Risk:** Inconsistent authorization across surfaces
**Definition of done:** Role hierarchy and permission matrix are enforced in gateway and UI
**KPI:** Unauthorized access incident count
**Ships in:** `7.1.0`

---

### Stage 7.2 - Service-level authorization enforcement

**Status:** Planned
**Depends on:** Stage 7.1
**Risk:** Internal service routes bypass policy checks
**Definition of done:** Service-to-service policy checks are standardized
**KPI:** Policy coverage across protected endpoints
**Ships in:** `7.2.0`

---

### Stage 7.3 - Admin governance controls

**Status:** Planned
**Depends on:** Stage 7.2
**Risk:** High-impact admin actions without safeguards
**Definition of done:** Admin approvals/reason codes/audit trails are enforced
**KPI:** Audited admin action coverage
**Ships in:** `7.3.0`

---

### Stage 7.4 - Audit and compliance event model

**Status:** Planned
**Depends on:** Stage 7.3
**Risk:** Missing forensic/compliance evidence
**Definition of done:** Immutable audit event model and query/report flows exist
**KPI:** Compliance evidence completeness
**Ships in:** `7.4.0`

---

### Stage 7.5 - Data governance and lifecycle controls

**Status:** Planned
**Depends on:** Stage 7.4
**Risk:** Retention/deletion policy drift across stores
**Definition of done:** Data classification and lifecycle controls are operational
**KPI:** Policy conformance rate
**Ships in:** `7.5.0`

---

### Stage 7.6 - Tenant and policy isolation

**Status:** Planned
**Depends on:** Stage 7.5
**Risk:** Cross-tenant leakage or policy overlap
**Definition of done:** Tenant isolation and policy scoping are validated end-to-end
**KPI:** Tenant isolation test pass rate
**Ships in:** `7.6.0`

---

### Stage 7.7 - Security posture and secrets hardening

**Status:** Planned
**Depends on:** Stage 7.6
**Risk:** Privileged access and secret management weakness
**Definition of done:** Secret rotation and privileged controls are hardened
**KPI:** Security control coverage
**Ships in:** `7.7.0`

---

### Stage 7.8 - Deployment observability and enterprise reporting

**Status:** Planned
**Depends on:** Stage 7.7
**Risk:** Limited visibility for enterprise admins and support
**Definition of done:** Tenant-aware operational and governance reports are available
**KPI:** Enterprise report completeness
**Ships in:** `7.8.0`

---

### Stage 7.9 - Release candidate hardening for 8.0.0

**Status:** Planned
**Depends on:** Stages 7.1–7.8
**Risk:** Governance regressions before API expansion
**Definition of done:** Deployment era RC validation is complete
**KPI:** RC audit/control failures
**Ships in:** `7.9.0`

---

## VERSION 8.x — Public and Private APIs and Endpoints

### Stage 8.1 - Analytics taxonomy and event instrumentation

**Status:** Planned
**Depends on:** Stage 7.9
**Risk:** Inconsistent metrics semantics across teams
**Definition of done:** Canonical event/metric dictionary is adopted; core journeys emit correlated analytics events
**KPI:** Schema conformance rate, instrumentation coverage on priority flows
**Ships in:** `8.1.0`

---

### Stage 8.2 - Analytics ingestion hardening and data quality

**Status:** Planned
**Depends on:** Stage 8.1
**Risk:** Event loss, duplication, and schema drift
**Definition of done:** Reliable analytics ingestion with dedupe, DLQ, freshness, and quality controls
**KPI:** Event ingestion success rate, data quality score
**Ships in:** `8.2.0`

---

### Stage 8.3 - Private API contracts and service-to-service surface

**Status:** Planned
**Depends on:** Stage 8.2
**Risk:** Internal API drift and undocumented service contracts
**Definition of done:** Private API baseline is documented, versioned, and tested
**KPI:** Contract coverage and drift incidents
**Ships in:** `8.3.0`

---

### Stage 8.4 - Public API minimum surface

**Status:** Planned
**Depends on:** Stage 8.3
**Risk:** Unstable external API behavior
**Definition of done:** Stable read/write public API baseline is published and tested
**KPI:** Public API success rate
**Ships in:** `8.4.0`

---

### Stage 8.5 - API versioning and compatibility policy

**Status:** Planned
**Depends on:** Stage 8.4
**Risk:** Breaking changes reaching partner consumers
**Definition of done:** Versioning policy and deprecation gate are enforced; compatibility test suite is active
**KPI:** Contract regression count per release
**Ships in:** `8.5.0`

---

### Stage 8.6 - Webhook and event delivery platform v1

**Status:** Planned
**Depends on:** Stage 8.5
**Risk:** Delivery failures and replay ambiguity
**Definition of done:** Signed webhooks with retry, DLQ, and delivery tracking are operational
**KPI:** Webhook delivery success rate
**Ships in:** `8.6.0`

---

### Stage 8.7 - Partner identity and tenant-safe access

**Status:** Planned
**Depends on:** Stage 8.6
**Risk:** Over-permissioned or leaked partner credentials
**Definition of done:** Scoped partner auth and tenant isolation controls are live
**KPI:** Unauthorized partner access incidents
**Ships in:** `8.7.0`

---

### Stage 8.8 - Analytics and reporting APIs

**Status:** Planned
**Depends on:** Stage 8.7
**Risk:** Low adoption of analytics features and slow export cycles
**Definition of done:** User analytics views, admin analytics center, and scheduled reporting are operational
**KPI:** Analytics dashboard usage rate and report success rate
**Ships in:** `8.8.0`

---

### Stage 8.9 - Release candidate hardening for 9.0.0

**Status:** Planned
**Depends on:** Stages 8.1–8.8
**Risk:** Breaking changes before ecosystem expansion
**Definition of done:** API and analytics RC validation is complete
**KPI:** RC partner regression count
**Ships in:** `8.9.0`

---

## VERSION 9.x — Ecosystem Integrations and Platform Productization

### Stage 9.1 - Integration contract governance

**Status:** Planned
**Depends on:** Stage 8.9
**Risk:** API contract drift across partners
**Definition of done:** Versioned integration contract governance is adopted
**KPI:** Contract compatibility pass rate
**Ships in:** `9.1.0`

---

### Stage 9.2 - Connector framework baseline

**Status:** Planned
**Depends on:** Stage 9.1
**Risk:** Connector implementations diverge and become brittle
**Definition of done:** Shared connector lifecycle and SDK baseline is defined
**KPI:** Connector onboarding time
**Ships in:** `9.2.0`

---

### Stage 9.3 - Integration observability and commercial controls

**Status:** Planned
**Depends on:** Stage 9.2
**Risk:** Slow partner issue triage and integration overuse without enforcement
**Definition of done:** Integration health views, support actions, and plan quotas are active
**KPI:** Partner issue MTTR, entitlement violation rate
**Ships in:** `9.3.0`

---

### Stage 9.4 - Tenant platform model standardization

**Status:** Planned
**Depends on:** Stage 9.3
**Risk:** Tenant model inconsistencies across services
**Definition of done:** Canonical tenant model and propagation are standardized
**KPI:** Tenant context coverage
**Ships in:** `9.4.0`

---

### Stage 9.5 - Self-serve workspace administration

**Status:** Planned
**Depends on:** Stage 9.4
**Risk:** Support-heavy admin operations
**Definition of done:** Tenant self-serve admin controls are operational
**KPI:** Self-serve admin action completion rate
**Ships in:** `9.5.0`

---

### Stage 9.6 - Plan entitlements and packaging engine

**Status:** Planned
**Depends on:** Stage 9.5
**Risk:** Inconsistent runtime enforcement of product plans
**Definition of done:** Entitlement engine consistently gates capabilities
**KPI:** Entitlement enforcement accuracy
**Ships in:** `9.6.0`

---

### Stage 9.7 - SLA/SLO operations foundation

**Status:** Planned
**Depends on:** Stage 9.6
**Risk:** Inability to prove service commitments
**Definition of done:** SLA/SLO operational reporting and alerting are active
**KPI:** SLA attainment rate
**Ships in:** `9.7.0`

---

### Stage 9.8 - Cost governance and capacity forecasting

**Status:** Planned
**Depends on:** Stage 9.7
**Risk:** Capacity shortfalls and margin degradation
**Definition of done:** Cost attribution and capacity forecasting controls are operational
**KPI:** Forecast accuracy and cost variance
**Ships in:** `9.8.0`

---

### Stage 9.9 - Release candidate hardening for 10.0.0

**Status:** Planned
**Depends on:** Stages 9.1–9.8
**Risk:** Ecosystem regressions before campaign era
**Definition of done:** Ecosystem and productization RC checks are complete
**KPI:** RC production-blocking issues
**Ships in:** `9.9.0`

---

## VERSION 10.x — Email Campaign

### Stage 10.1 - Campaign foundation: entity model, policy gates, suppression, templates

**Status:** Planned
**Depends on:** Stage 9.9
**Risk:** Policy and consent violations from unvalidated campaign sends
**Definition of done:** Campaign and audience entities, consent/region/content/rate-limit policy gates, suppression lists, and template system are operational
**KPI:** Policy gate coverage, suppression list accuracy
**Ships in:** `10.1.0`

---

### Stage 10.2 - Campaign execution engine

**Status:** Planned
**Depends on:** Stage 10.1
**Risk:** Duplicate sends from state machine failures or incomplete idempotency
**Definition of done:** Campaign state machine is stable; idempotent send, retry semantics, and pause/resume are reliable
**KPI:** Duplicate send rate, campaign completion rate
**Ships in:** `10.2.0`

---

### Stage 10.3 - Campaign deliverability and safety

**Status:** Planned
**Depends on:** Stage 10.2
**Risk:** High bounce rates and domain reputation degradation
**Definition of done:** Pre-send verification (Mailvetter), bounce handling, domain warmup, and safety checks are active
**KPI:** Bounce rate, inbox placement rate
**Ships in:** `10.3.0`

---

### Stage 10.4 - Campaign observability, support bundles, and release automation

**Status:** Planned
**Depends on:** Stage 10.3
**Risk:** Low visibility into campaign pipeline health and slow issue triage
**Definition of done:** Campaign metrics, structured logging, feature flags, and canary rollout controls are available
**KPI:** Mean time to detect campaign failures, feature flag coverage
**Ships in:** `10.4.0`

---

### Stage 10.5 - Campaign commercial controls and compliance

**Status:** Planned
**Depends on:** Stage 10.4
**Risk:** Unmetered send costs and PII/consent regulatory exposure
**Definition of done:** Send metering, PII retention policies, opt-out auditing, and contract freeze are enforced
**KPI:** Metering accuracy, opt-out audit completeness
**Ships in:** `10.5.0`

---

### Stage 10.9 - Contract freeze and final campaign release governance

**Status:** Planned
**Depends on:** Stages 10.1–10.5
**Risk:** Late-breaking compliance and contract issues
**Definition of done:** Campaign era governance baseline and long-term release process are signed off
**KPI:** Final release readiness score
**Ships in:** `10.9.0`

---

## Feature-to-service traceability matrix

| Stage | Feature area | Services | UI surface | Data store | Ships in |
| --- | --- | --- | --- | --- | --- |
| 1.1 | Auth and onboarding | `appointment360` | `dashboard`, `extension/contact360` | PostgreSQL | `1.0.0` |
| 1.2 | Credit management | `appointment360` | `dashboard` | PostgreSQL | `1.0.0` |
| 1.3 | Billing and payments | `appointment360` | `dashboard` | PostgreSQL | `1.1.0` |
| 1.4 | User analytics (minimal) | `appointment360`, `logs.api` | `dashboard` | PostgreSQL, S3 (CSV) | `1.2.0` |
| 1.5 | Notifications | `appointment360` | `dashboard` | PostgreSQL | `1.2.0` |
| 1.6 | Admin analytics/control | `docsai`, `logs.api`, `appointment360` | `docsai` | S3 (CSV), PostgreSQL | `1.2.0` |
| 1.7 | Security baseline | `appointment360` and service middleware | `dashboard`, `extension/contact360` | N/A | `1.2.0` |
| 2.1 | Email finder | `emailapis`, `emailapigo`, `appointment360` | `dashboard` | PostgreSQL, S3 | `2.0.0` |
| 2.2 | Email verifier | `mailvetter`, `emailapis`, `appointment360` | `dashboard` | PostgreSQL | `2.0.0` |
| 2.3 | Results engine | `appointment360` | `dashboard` | PostgreSQL | `2.0.0` |
| 2.4 | Bulk processing | `tkdjob`, `s3storage`, `emailapis`, `mailvetter` | `dashboard` | S3, PostgreSQL | `2.1.0` |
| 3.1–3.4 | Contact/company data | `connectra`, `appointment360` | `dashboard` | Elasticsearch, PostgreSQL | `3.0.0` |
| 4.1–4.4 | Extension and Sales Navigator | `salesnavigator`, `appointment360`, `logs.api` | `extension/contact360` | PostgreSQL, Elasticsearch, S3 (CSV) | `4.0.0` |
| 5.1–5.4 | AI workflows | `contact.ai`, `appointment360` | `dashboard` | PostgreSQL | `5.0.0` |
| 6.1–6.9 | Reliability and scaling | `tkdjob`, `logs.api`, `s3storage`, `appointment360`, all core services | `dashboard`, `docsai`, `extension/contact360` | PostgreSQL, S3, Elasticsearch | `6.1.0`–`6.9.0` |
| 7.1–7.9 | Deployment | `appointment360`, `docsai`, `logs.api`, all services | `dashboard`, `docsai`, `extension/contact360` | PostgreSQL, S3 (CSV) | `7.1.0`–`7.9.0` |
| 8.1–8.9 | Public and private APIs | `appointment360`, `tkdjob`, `logs.api`, reporting pipelines | `dashboard`, `docsai`, external API consumers | PostgreSQL, S3, Elasticsearch | `8.1.0`–`8.9.0` |
| 9.1–9.9 | Ecosystem integrations + productization | `appointment360`, `docsai`, entitlement/policy modules, integration adapters, all services | `dashboard`, `docsai`, `extension/contact360`, external consumers | PostgreSQL, S3, Elasticsearch | `9.1.0`–`9.9.0` |
| 10.1–10.9 | Email campaign | `appointment360`, `tkdjob`, `emailapis`, `logs.api` | `dashboard`, `docsai` | PostgreSQL, S3, Elasticsearch | `10.1.0`–`10.9.0` |

---

## Deep execution breakdown (small-task packs)

Execution tracks used across all stages:

- Contract track (API/schema/policy)
- Service track (backend implementation)
- Surface track (dashboard/extension/docsai)
- Data/Ops track (storage, lineage, observability, release safety)

### `1.x` → `2.x` (User, billing, credit → Email system)

- **1.3 Billing**
  - Implement credit pack purchase mutations and payment state machine.
  - Wire payment-proof submission and admin approval flows.
- **1.4–1.7 Analytics/notifications/admin/security**
  - Add user usage view and credit ledger display.
  - Add low-credit warning component and payment success notification.
  - Add admin credit/package management views in DocsAI.
  - Add GraphQL rate-limit middleware for baseline abuse prevention.
- **2.1 Finder**
  - Ensure 10-pattern generation runs correctly and Go path routes heavy workloads.
  - Validate credit deduction per finder call.
- **2.2 Verifier**
  - Ensure Mailvetter integration is reliable; add SPF/DMARC check coverage.
  - Validate status normalization and confidence propagation.
- **2.3 Results**
  - Surface best result prominently with confidence metadata.
  - Verify audit log entries for all verification events.
- **2.4 Bulk**
  - Harden streaming checkpoint and resume logic.
  - Validate multipart S3 upload and output retrieval end-to-end.

### `3.x` → `4.x` (Contact/company data → Extension)

- **3.1 VQL/filters**
  - Freeze filter taxonomy and validate VQL-to-ES query translation.
  - Add performance regression tests for complex filter queries.
- **3.2 Enrichment/dedupe**
  - Tune merge-on-conflict rules and deterministic UUID assignment.
  - Add deduplication quality metrics to observability.
- **3.3 Search quality**
  - Tune index refresh cycle and relevance scoring.
  - Validate P95 latency targets against SLO.
- **3.4 Search UX**
  - Build advanced filter UI with saved-search capability.
  - Add company drill-down and search-to-export conversion tracking.
- **4.1–4.4 Extension**
  - Harden token refresh and session expiry handling in extension context.
  - Validate SN ingestion pipeline with dedup and conflict resolution.
  - Add telemetry error shipping to logs.api and ingestion status UX.

### `5.x` → `6.x` (AI workflows → Reliability)

- **5.1–5.4 AI workflows**
  - Integrate HF streaming client and Gemini utility paths.
  - Add confidence/explanation fields to message contract.
  - Enforce AI quota guardrails and prompt version controls.
- **6.1–6.4 Reliability baseline**
  - Define per-service SLOs and wire RED metrics middleware.
  - Add idempotency keys to billing/bulk/sync write paths.
  - Configure DLQ/replay for async job queues.
  - Add correlated trace IDs and structured log shipping.
- **6.5–6.9 Scaling and RC**
  - Tune P95 latency hotspots; add S3 lifecycle rules.
  - Set cost guardrails and mutation abuse guards.
  - Run reliability RC smoke test suite before 7.0.0.

### `7.x` (Deployment)

- **7.1–7.4 RBAC and governance**
  - Enforce role hierarchy in gateway and UI permission checks.
  - Standardize service-to-service auth controls.
  - Add admin approval flows and audit event emission.
- **7.5–7.9 Security and RC**
  - Enforce data lifecycle and retention policies.
  - Validate tenant isolation end-to-end.
  - Harden secret rotation and privileged access controls.
  - Run deployment RC gate before 8.0.0.

### `8.x` (Public and private APIs)

- **8.1–8.3 Analytics and private API**
  - Freeze event taxonomy and instrument core user journeys.
  - Add analytics ingestion DLQ and quality checks.
  - Document and version internal service API contracts.
- **8.4–8.7 Public APIs and webhooks**
  - Ship public GraphQL/REST endpoints with rate controls.
  - Enforce versioning policy and breaking-change gates.
  - Implement signed webhook delivery and retry.
  - Add partner auth scopes and tenant-safe credentials.
- **8.8–8.9 Analytics APIs and RC**
  - Build analytics views and scheduled reporting endpoints.
  - Run API compatibility and reliability RC tests before 9.0.0.

### `9.x` (Ecosystem integrations + productization)

- **9.1–9.3 Connectors and governance**
  - Define versioned integration contract policy.
  - Build connector SDK and lifecycle validation harness.
  - Add integration health dashboards and quota enforcement.
- **9.4–9.9 Productization**
  - Standardize tenant identity propagation.
  - Build self-serve admin workspace controls.
  - Centralize entitlement engine and plan packaging.
  - Define SLA indicators and operational reporting.
  - Add cost/capacity forecasting controls.
  - Run productization RC gate before 10.0.0.

### `10.x` (Email campaign)

- **10.1–10.2 Campaign foundation and execution**
  - Define campaign/audience entity schemas and policy gate rules.
  - Build suppression list management and template system.
  - Implement campaign state machine with idempotent send and retry.
- **10.3–10.5 Deliverability, observability, and compliance**
  - Integrate Mailvetter pre-send verification and bounce handling.
  - Add campaign metrics, structured logging, and feature flags.
  - Enforce send metering, PII retention, and opt-out auditing.
- **10.9 RC**
  - Freeze campaign contract schemas and compliance controls.
  - Run final governance readiness review and sign-off.

---

*This document is product documentation. The DocsAI roadmap UI uses a hardcoded mirror that must remain synchronized with this file.*


### Stage 10 service-level code pointers
- campaigns
- sequences
- templates
- workers
- analytics

## Documentation completeness gates

For each stage transition to `in_progress` or `completed`, verify all of the following:

- Matching release entry exists in `docs/versions.md` with identical roadmap IDs.
- Matching per-minor file exists in `docs/versions/version_*.md` with the six mandatory scope sections.
- API modules and frontend surfaces in stage text map to `docs/backend/apis/` and `docs/frontend/pages/` inventories.

## `s3storage` cross-era execution stream

Use this stream to keep storage delivery synchronized with major-era goals.

### `0.x` foundation
- Contract: finalize base upload/list/download + analysis endpoint semantics.
- Service: stabilize backend abstraction (`s3` and `filesystem` parity).
- Ops: baseline smoke checks and deployment diagnostics.

### `1.x` user/billing/credit
- Contract: define object-class policies for avatar/photo/proof/resume files.
- Service: enforce per-path content validation and secure defaults.
- Data/Ops: add actor/source fields and upload abuse monitoring.

### `2.x` email system
- Contract: freeze multipart protocol and retry semantics.
- Service: durable multipart session state; retry-safe complete/abort.
- Data/Ops: metadata freshness SLA and bulk-path failure recovery checks.

### `3.x` contact/company data
- Contract: ingestion artifact naming/versioning.
- Service: robust schema/stats/preview behavior for large CSVs.
- Data/Ops: upload-to-ingestion lineage evidence.

### `4.x` extension maturity
- Contract: extension-safe storage policies and URL lifetimes.
- Service: channel-aware access and provenance markers.
- Data/Ops: extension upload reliability telemetry.

### `5.x` AI workflows
- Contract: AI artifact type/retention policy.
- Service: AI artifact guardrails and retrieval constraints.
- Data/Ops: model-run to source-file lineage traceability.

### `6.x` reliability and scaling
- Contract: idempotency and SLO definitions for storage lifecycle.
- Service: metadata write concurrency safety and reconciliation utilities.
- Data/Ops: storage SLO dashboards and incident runbooks.

### `7.x` deployment
- Contract: service authz and retention/deletion policy contract.
- Service: endpoint auth hardening and environment-driven worker routing.
- Data/Ops: compliance evidence and governance controls.

### `8.x` public/private APIs
- Contract: versioned storage endpoint policy and lifecycle event envelope.
- Service: partner-safe event delivery/replay behavior.
- Data/Ops: API compatibility and reliability regression gates.

### `9.x` ecosystem/productization
- Contract: plan entitlements and quota policy for storage operations.
- Service: tenant throttling and quota enforcement.
- Data/Ops: cost attribution and residency overlays.

### `10.x` email campaign
- Contract: campaign artifact reproducibility/compliance contract.
- Service: immutable evidence paths for compliance-critical artifacts.
- Data/Ops: campaign audit bundles and long-term retention checks.

### Era task-pack links
- `docs/0. Foundation and pre-product stabilization and codebase setup/0.5 — Object storage plane.md` (patches `0.5.0`–`0.5.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `s3storage-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `s3storage-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `s3storage-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `s3storage-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `s3storage-ai-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-api-endpoint-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-email-campaign-task-pack.md` merged)

## `logs.api` cross-era execution stream

- `0.x`: bootstrap logging baseline and health contract.
- `1.x`: user, auth, billing, and credit operational event lineage.
- `2.x`: email workflow and bulk processing telemetry at scale.
- `3.x`: data-enrichment/search support diagnostics.
- `4.x`: extension and SN ingestion telemetry provenance.
- `5.x`: AI workflow observability and cost/quality telemetry.
- `6.x`: reliability SLO/error-budget evidence from logging.
- `7.x`: deployment and governance audit trail maturity.
- `8.x`: public/private API observability and compatibility signals.
- `9.x`: ecosystem integration tenant-level governance evidence.
- `10.x`: campaign execution/compliance audit immutability.

Era task-pack links: **8.x** — `docs/8. Contact360 public and private apis and endpoints/` patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-public-private-apis-task-pack.md` merged). **9.x** — `docs/9. Contact360 Ecosystem integrations and Platform productization/` patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-ecosystem-productization-task-pack.md` merged). **10.x** — `docs/10. Contact360 email campaign/` patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `logsapi-email-campaign-task-pack.md` merged). Other eras: see `docs/0...10/*logsapi*-task-pack.md` where published.

## `jobs` cross-era execution stream

- `0.x`: scheduler foundation (API + scheduler + worker baseline).
- `1.x`: billing/credit-aware job governance and ownership checks.
- `2.x`: email finder/verify/pattern stream processors.
- `3.x`: Contact360 import/export stream processors + VQL validation.
- `4.x`: extension/SN provenance and sync jobs.
- `5.x`: AI batch processor and cost-confidence metadata.
- `6.x`: reliability hardening (idempotency, retry/DLQ, stale recovery).
- `7.x`: role-aware authz, retention, and audit controls.
- `8.x`: versioned API and webhook callback maturity.
- `9.x`: tenant quota, isolation, and entitlement scheduling.
- `10.x`: campaign compliance bundles and strict idempotency.

### Era task-pack links

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.6 — Async job spine.md` (patches `0.6.0`–`0.6.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `jobs-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `jobs-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `jobs-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `jobs-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `jobs-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `jobs-email-campaign-task-pack.md` merged)

## `contact.ai` cross-era execution stream

- `0.x`: FastAPI Lambda skeleton + `ai_chats` DDL baseline; health endpoints; CI probe.
- `1.x`: `user_id` FK integrity; user-deletion cascade strategy; IAM hardening.
- `2.x`: `analyzeEmailRisk` contract lock; HF JSON task for email scoring; PII review.
- `3.x`: `parseContactFilters` + `generateCompanySummary` aligned with Connectra VQL taxonomy.
- `4.x`: SN contact object compatibility in `messages.contacts[]` JSONB; extension CSP.
- `5.x`: ALL contact.ai features live — full chat CRUD, sync + SSE message send, all utility endpoints, `ModelSelection` shim.
- `6.x`: SLO tuning, SSE reliability, chat TTL, optimistic lock, distributed tracing.
- `7.x`: RBAC, per-tenant API keys, GDPR erasure cascade, audit log to `logs.api`.
- `8.x`: Rate limit headers, scoped API keys, usage tracking, API quota in settings UI.
- `9.x`: Webhook AI delivery, ecosystem connector adapter, integration panel.
- `10.x`: Campaign AI generation endpoint (`/api/v1/ai/email/generate`), `campaign_ai_log` compliance table.

### Era task-pack links (contact.ai)

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.2 — Schema & migration bedrock.md` / `0.3 — Service mesh contracts.md` / `0.10 — Ship & ops hardening.md` (contact.ai slices per patch)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `contact-ai-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `contact-ai-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `contact-ai-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `contact-ai-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `contact-ai-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `contact-ai-email-campaign-task-pack.md` merged)

## `salesnavigator` cross-era execution stream

- `0.x`: FastAPI+Mangum scaffold; `GET /v1/health`; SAM baseline; UUID5 deterministic contract defined.
- `1.x`: Actor context headers (`X-User-ID`/`X-Org-ID`) pass-through; billing event stub; secret rotation.
- `2.x`: Email/phone field validation; enrichment queue handoff stub; `email_status` preservation.
- `3.x`: Full `mappers.py` locked; provenance fields (`source=sales_navigator`, `lead_id`, `search_id`, `connection_degree`) written to Connectra.
- `4.x`: PRIMARY DELIVERY — HTML extraction hardened; full extension popup UX; docs drift fixed; `data_quality_score`, `recently_hired`, `is_premium` surfaced.
- `5.x`: AI-ready field quality gates (`seniority`, `departments`, `about`); `data_quality_score` indexed for AI VQL filters.
- `6.x`: Rate limiter; chunk idempotency tokens; CORS hardened; `X-Request-ID`; p95 SLO targets; load tests.
- `7.x`: Per-tenant API keys; immutable audit event per save session; GDPR cascade via Connectra; RBAC gates.
- `8.x`: `X-RateLimit-*` headers; `Retry-After`; usage counters in `api_usage`; versioned path alignment.
- `9.x`: Connector adapter layer; webhook delivery of ingest results; tenant-isolated lineage.
- `10.x`: Campaign audience provenance — `lead_id`/`search_id` carried to campaign records; suppression non-overwrite guard.

### Era task-pack links (salesnavigator)

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.9 — Extension channel scaffold.md` (patches `0.9.0`–`0.9.9`)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `salesnavigator-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `salesnavigator-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `salesnavigator-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `salesnavigator-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `salesnavigator-ai-workflows-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-email-campaign-task-pack.md` merged)


---

## Email app era track — `contact360.io/email`

| Era | Email app status |
| --- | --- |
| 0.x | foundation shell and route structure |
| 1.x | auth + profile/account surface live |
| 2.x | core mailbox operations live (folder/detail/imap connect) |
| 3.x | preparatory integration points for contact enrichment |
| 4.x | extension parity hooks pending |
| 5.x | AI assistant UI placeholder present |
| 6.x | reliability hardening backlog (retry/backoff/telemetry) |
| 7.x | deployment and environment hardening required |
| 8.x | endpoint contract formalization in progress |
| 9.x | ecosystem export/integration hooks pending |
| 10.x | campaign handoff pathways pending |

## `mailvetter` cross-era execution stream

- `0.x`: API/worker foundation, Redis+Postgres bootstrap, `/v1` health and auth envelope.
- `1.x`: API key ownership model and plan-based limit governance aligned with billing/credits.
- `2.x`: PRIMARY delivery era — single/bulk verification contracts, async jobs/results lifecycle, scoring model freeze.
- `3.x`: Contact/company linkage for verification lineage and freshness in CRM surfaces.
- `4.x`: Extension and Sales Navigator provenance tagging and burst-safe verification controls.
- `5.x`: AI-ready explainability outputs (`score_details` reason mapping) for assistant surfaces.
- `6.x`: Reliability hardening — distributed limiter, idempotency, retry/DLQ, SLO observability.
- `7.x`: Deployment hardening — migration discipline, deprecation governance, release gates.
- `8.x`: Public/private API formalization — OpenAPI, scoped keys, endpoint governance.
- `9.x`: Ecosystem productization — webhook replay, partner connector reliability, SLA evidence.
- `10.x`: Campaign preflight verification at scale with recipient-level compliance traceability.

### Era task-pack links (mailvetter)

- `docs/0. Foundation and pre-product stabilization and codebase setup/0.2 — Schema & migration bedrock.md` (Mailvetter in patch slices)
- `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `mailvetter-user-billing-task-pack.md` merged)
- `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `mailvetter-email-system-task-pack.md` merged)
- `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `mailvetter-contact-company-task-pack.md` merged)
- `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `mailvetter-extension-sn-task-pack.md` merged)
- `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `mailvetter-ai-task-pack.md` merged)
- `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-reliability-scaling-task-pack.md` merged)
- `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-deployment-task-pack.md` merged)
- `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-public-private-apis-task-pack.md` merged)
- `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-ecosystem-productization-task-pack.md` merged)
- `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-email-campaign-task-pack.md` merged)


## Historical Refactor Plans
- [Contact360 Docs Overhaul Plan 1](plans/contact360_docs_overhaul_1a3fa187.plan.md)
- [Contact360 Docs Overhaul Plan 2](plans/contact360_docs_overhaul_9f8e9039.plan.md)
