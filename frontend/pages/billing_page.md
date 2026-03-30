# Billing

## Overview

- **page_id:** billing_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 1.x, 8.x
- **flow_id:** billing
- **_id:** billing_page-001

## Metadata

- **route:** /billing
- **file_path:** contact360.io/app/app/(dashboard)/billing/page.tsx
- **purpose:** Central financial governance hub. Manages subscription lifecycles, credit allocations, payment instrumentation, and invoice auditing.
- **s3_key:** data/pages/billing_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Admin tab (System Management) restricted to `admin` / `superAdmin` roles.
- **page_state:** production
- **last_updated:** 2026-03-29T00:00:00.000000+00:00

### uses_endpoints (15)

- `graphql/GetBilling` — Aggregated billing data (credits, subscription, status).
- `graphql/GetPlans` — Available public subscription tiers.
- `graphql/GetAddons` — Credit pack offerings.
- `graphql/GetInvoices` — Historical transaction records.
- `graphql/Subscribe` — Plan transition mutation.
- `graphql/PurchaseAddon` — One-time credit acquisition.
- `graphql/CancelSubscription` — Termination flow mutation.
- `graphql/CreatePlan` — Admin: Defined new subscription tier.
- `graphql/UpdatePlan` — Admin: Modify existing tier parameters.

### UI components (metadata)

- **BillingPage** — `app/(dashboard)/billing/page.tsx`
- **UpiPaymentModal** — `components/billing/UpiPaymentModal.tsx`
- **Button** — `components/ui/Button.tsx`
- **Badge** — `components/ui/Badge.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **Check** — `lucide-react` (icon)
- **CreditCard** — `lucide-react` (icon)
- **Crown** — `lucide-react` (icon)
- **Wallet** — `lucide-react` (icon)
- **ShoppingCart** — `lucide-react` (icon)
- **FeatureIcons** — `lucide-react` (Crown, Wallet, CreditCard, etc.)
- **AdminBillingView** — `components/features/billing/AdminBillingView.tsx` (System-wide plan configuration)

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/billing/UpiPaymentModal.tsx | UpiPaymentModal | UPI payment flow integration |
| components/shared/LoadingSpinner.tsx | LoadingSpinner | Application-wide loading state |
| components/shared/ErrorState.tsx | ErrorState | Generic error handling view |
| components/ui/Button.tsx | Button | Action trigger |
| components/ui/Badge.tsx | Badge | Status/label indicator |

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| title | 1 | Billing |
| sub | 2 | Subscription Plan |
| hist | 2 | Invoice History |

### tabs

| id | label | visibility | era |
| --- | --- | --- | --- |
| sub | Subscription | always | 1.x |
| inv | Invoices | always | 1.x |
| cred | Credits | always | 1.x |
| admin | System | adminOnly | 1.x |

### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useBilling.ts | useBilling | Subscription and transaction management |
| hooks/useRole.ts | useRole | Permission and limit synchronization |

### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| open UpgradeModal | SubscriptionPlans | upgrade | Upgrade | primary | 1.x |
| open AddCreditsModal | CurrentSubscription | add-credits | Add Credits | secondary | 1.x |
| trigger cancel | CurrentSubscription | cancel | Cancel | danger | 1.x |
| download PDF | InvoiceHistory | download | Download | icon | 1.x |

### progress_bars

| component | id | label | color_logic |
| --- | --- | --- | --- |
| CurrentSubscription | usage | Credit Usage | Green > 50% |

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [H:HeroCard] + [K:BalanceCard] + [Q:PlansGrid] + [A:AddonsGrid] + [T:HistoryTable] -> {useBilling, useRole}

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)

**Typical inbound:** Sidebar, [profile_page.md](profile_page.md).
**Typical outbound:** [usage_page.md](usage_page.md), [dashboard_page.md](dashboard_page.md).

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetBilling` | [get_billing_graphql.md](../../backend/endpoints/get_billing_graphql.md) | QUERY | 1.x |
| `GetPlans` | [query_get_plans_graphql.md](../../backend/endpoints/query_get_plans_graphql.md) | QUERY | 1.x |
| `GetAddons` | [query_get_addons_graphql.md](../../backend/endpoints/query_get_addons_graphql.md) | QUERY | 1.x |
| `GetInvoices` | [query_get_invoices_graphql.md](../../backend/endpoints/query_get_invoices_graphql.md) | QUERY | 1.x |
| `Subscribe` | [mutation_subscribe_graphql.md](../../backend/endpoints/mutation_subscribe_graphql.md) | MUTATION | 1.x |
| `PurchaseAddon` | [mutation_purchase_addon_graphql.md](../../backend/endpoints/mutation_purchase_addon_graphql.md) | MUTATION | 1.x |
| `CancelSubscription` | [mutation_cancel_subscription_graphql.md](../../backend/endpoints/mutation_cancel_subscription_graphql.md) | MUTATION | 1.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetBilling` | [get_billing_graphql.md](../../backend/endpoints/get_billing_graphql.md) | QUERY | 1.x |
| `GetPlans` | [query_get_plans_graphql.md](../../backend/endpoints/query_get_plans_graphql.md) | QUERY | 1.x |
| `GetAddons` | [query_get_addons_graphql.md](../../backend/endpoints/query_get_addons_graphql.md) | QUERY | 0.x |
| `GetInvoices` | [query_get_invoices_graphql.md](../../backend/endpoints/query_get_invoices_graphql.md) | QUERY | 1.x |
| `Subscribe` | [mutation_subscribe_graphql.md](../../backend/endpoints/mutation_subscribe_graphql.md) | MUTATION | 1.x |
| `PurchaseAddon` | [mutation_purchase_addon_graphql.md](../../backend/endpoints/mutation_purchase_addon_graphql.md) | MUTATION | 1.x |
| `CancelSubscription` | [mutation_cancel_subscription_graphql.md](../../backend/endpoints/mutation_cancel_subscription_graphql.md) | MUTATION | 0.x |
| `CreatePlan` | [mutation_create_plan_graphql.md](../../backend/endpoints/mutation_create_plan_graphql.md) | MUTATION | 1.x |
| `UpdatePlan` | [mutation_update_plan_graphql.md](../../backend/endpoints/mutation_update_plan_graphql.md) | MUTATION | 1.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
