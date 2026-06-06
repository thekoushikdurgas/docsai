<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Read all the above and previous prompts and then think about my contact360 project in under 1.x.x - Contact360 user and billing and credit system , break into x.y and x.y.z with unique file name , Learn, understand, and analyse this deeply, and then break your tasks into smaller tasks.

Here is a **1.x.x roadmap** for your **Contact360 user, billing, and credit system**, broken into:

- **1.x** phases (major themes),
- **1.x.y** milestones,
- **1.x.y.z** granular tasks with **unique filenames** for your docs.

This sits on top of the 0.x.x foundation you already defined.

***

## 1.x.x – Contact360 User, Billing, and Credit System

### 1.1.x – Identity, Accounts, and Plans

#### 1.1.0 – User \& Org Identity Model

- **1.1.0.1 – Refine org/user/role model (multi‑tenant)**
File: `docs/20-accounts/01-org-user-role-model.md`
- **1.1.0.2 – Account lifecycle states (trial, active, suspended, closed)**
File: `docs/20-accounts/02-account-lifecycle-states.md`
- **1.1.0.3 – User onboarding \& invitation flows**
File: `docs/20-accounts/03-user-onboarding-and-invitations.md`


#### 1.1.1 – Plan \& Feature Model

- **1.1.1.1 – Plan catalog (FREE, STARTER, PRO, ENTERPRISE)**
File: `docs/20-accounts/04-plan-catalog-and-features.md`
- **1.1.1.2 – Feature flags \& entitlements per plan**
File: `docs/20-accounts/05-feature-entitlements-by-plan.md`
- **1.1.1.3 – Pricing units (seats, contacts, emails, AI credits)**
File: `docs/20-accounts/06-pricing-units-and-meters.md`

***

### 1.2.x – Billing Engine \& Invoicing

#### 1.2.0 – Billing Data Model

- **1.2.0.1 – Billing entities (subscription, invoice, charge, payment)**
File: `docs/21-billing/01-billing-entities-schema.md`
- **1.2.0.2 – Subscription lifecycle (trial → active → past_due → canceled)**
File: `docs/21-billing/02-subscription-lifecycle-model.md`
- **1.2.0.3 – Tax, currency, and region handling (IN/global)**
File: `docs/21-billing/03-tax-currency-and-region-handling.md`


#### 1.2.1 – Payment Provider Integration

- **1.2.1.1 – Choose provider (Stripe/Razorpay/etc.) and architecture**
File: `docs/21-billing/04-payment-provider-architecture.md`
- **1.2.1.2 – Checkout \& subscription creation flows**
File: `docs/21-billing/05-checkout-and-subscription-flows.md`
- **1.2.1.3 – Webhook handling (invoice.paid, payment_failed, subscription_updated)**
File: `docs/21-billing/06-billing-webhooks-and-events.md`


#### 1.2.2 – Invoices \& Receipts

- **1.2.2.1 – Invoice generation rules \& line item structure**
File: `docs/21-billing/07-invoice-generation-rules.md`
- **1.2.2.2 – PDF/HTML invoice templates**
File: `docs/21-billing/08-invoice-rendering-templates.md`
- **1.2.2.3 – Email notifications for billing events**
File: `docs/21-billing/09-billing-email-notifications.md`

***

### 1.3.x – Credits, Usage Metering, and Limits

#### 1.3.0 – Credit Model

- **1.3.0.1 – Define credit types (email, phone, AI, enrichment, jobs)**
File: `docs/22-credits/01-credit-types-and-definitions.md`
- **1.3.0.2 – Org credit balances \& refill policy**
File: `docs/22-credits/02-credit-balance-and-refill-policy.md`
- **1.3.0.3 – Daily/periodic AI budget \& downgrade behavior**
File: `docs/22-credits/03-ai-budget-and-downgrade-rules.md`


#### 1.3.1 – Usage Metering Design

- **1.3.1.1 – Meters per feature (emails sent, validations, AI tokens, imports)**
File: `docs/22-credits/04-usage-meters-and-signals.md`
- **1.3.1.2 – Usage recording pipeline (sync vs async, idempotency)**
File: `docs/22-credits/05-usage-recording-pipeline.md`
- **1.3.1.3 – Usage aggregation for billing \& analytics**
File: `docs/22-credits/06-usage-aggregation-and-rollups.md`


#### 1.3.2 – Limits \& Enforcement

- **1.3.2.1 – Per‑plan hard \& soft limits (seats, emails/mo, AI prompts/day)**
File: `docs/22-credits/07-plan-limits-and-thresholds.md`
- **1.3.2.2 – Enforcement patterns (blocking, throttling, degradation)**
File: `docs/22-credits/08-limit-enforcement-strategy.md`
- **1.3.2.3 – Grace behavior \& overage handling**
File: `docs/22-credits/09-grace-periods-and-overages.md`

***

### 1.4.x – Integration with Core Contact360 Flows

#### 1.4.0 – Auth \& Access Control Integration

- **1.4.0.1 – Map billing state to auth (suspended, read‑only, locked)**
File: `docs/23-integration/01-auth-billing-state-mapping.md`
- **1.4.0.2 – Tenant isolation in billing queries (org_id everywhere)**
File: `docs/23-integration/02-billing-tenant-isolation-rules.md`
- **1.4.0.3 – Role‑based access to billing screens \& APIs**
File: `docs/23-integration/03-billing-rbac-and-permissions.md`


#### 1.4.1 – AI Agent × Credits Integration

- **1.4.1.1 – Credit check in AI tool calls (pre‑execution)**
File: `docs/23-integration/04-ai-tools-credit-checks.md`
- **1.4.1.2 – AI usage logging (tokens, tool calls, costs per org)**
File: `docs/23-integration/05-ai-usage-logging-and-metrics.md`
- **1.4.1.3 – AI behavior when out of credits (fallbacks \& messaging)**
File: `docs/23-integration/06-ai-behavior-on-credit-exhaustion.md`


#### 1.4.2 – Campaign \& Enrichment × Credits Integration

- **1.4.2.1 – Email campaign credits consumption rules**
File: `docs/23-integration/07-email-campaign-credit-consumption.md`
- **1.4.2.2 – Phone \& enrichment credit consumption rules**
File: `docs/23-integration/08-phone-enrichment-credit-consumption.md`
- **1.4.2.3 – Pre‑flight checks before large operations (imports/campaigns)**
File: `docs/23-integration/09-prefight-credit-checks-large-ops.md`

***

### 1.5.x – UX \& Self‑Service Billing Experience

#### 1.5.0 – Billing UI in Web/Admin Apps

- **1.5.0.1 – Billing overview page (current plan, usage, invoices)**
File: `docs/24-billing-ui/01-billing-overview-page-spec.md`
- **1.5.0.2 – Plan upgrade/downgrade flows (including prorations)**
File: `docs/24-billing-ui/02-plan-change-flows-spec.md`
- **1.5.0.3 – Credit balance \& usage visualizations**
File: `docs/24-billing-ui/03-credit-usage-visualizations-spec.md`


#### 1.5.1 – Notifications \& Lifecycle UX

- **1.5.1.1 – Low credit / approaching limit notifications**
File: `docs/24-billing-ui/04-low-credit-notifications-spec.md`
- **1.5.1.2 – Payment failure \& dunning UX flows**
File: `docs/24-billing-ui/05-dunning-and-payment-failure-ux.md`
- **1.5.1.3 – Trial expiry \& upgrade nudges**
File: `docs/24-billing-ui/06-trial-expiry-and-upgrade-ux.md`

***

### 1.6.x – Observability, Finance Ops, and Safeguards

#### 1.6.0 – Monitoring \& Alerts

- **1.6.0.1 – Billing \& credit SLOs (accuracy, timeliness, failures)**
File: `docs/25-billing-ops/01-billing-and-credit-slos.md`
- **1.6.0.2 – Alerting rules (over‑billing, under‑billing, missed events)**
File: `docs/25-billing-ops/02-billing-alerts-and-anomalies.md`
- **1.6.0.3 – Audit logs for billing and credit operations**
File: `docs/25-billing-ops/03-billing-audit-log-design.md`


#### 1.6.1 – Reconciliation \& Finance Workflows

- **1.6.1.1 – Daily/weekly reconciliation with payment provider**
File: `docs/25-billing-ops/04-provider-reconciliation-workflow.md`
- **1.6.1.2 – Dispute \& refund handling process**
File: `docs/25-billing-ops/05-disputes-and-refunds-process.md`
- **1.6.1.3 – Reporting for finance (MRR, churn, ARPU, credit burn)**
File: `docs/25-billing-ops/06-finance-reporting-and-metrics.md`

***

If you’d like, the next step can be:

- a **bash script** to scaffold this `docs/` structure and empty files, or
- taking one slice (e.g. **1.3.x Credits \& Usage Metering**) and turning it into a detailed, implementation‑ready checklist for your codebases.
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: Pasted-text.txt

[^2]: deep-research-report-1.md

