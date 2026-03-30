# Appointment360 (contact360.io/api) — Era 9.x Ecosystem Integrations & Productization Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `NotificationQuery { notifications() }` | P0 |
| Define `NotificationMutation { markNotificationRead(id), markAllRead }` | P0 |
| Define `AnalyticsQuery { analytics(dateRange, granularity, metrics) }` | P0 |
| Define `AnalyticsMutation { trackEvent(type, metadata) }` | P0 |
| Define `AdminQuery { adminStats(), paymentSubmissions(), users() }` (SuperAdmin-only) | P0 |
| Define `AdminMutation { creditUser, adjustCredits, approvePayment, declinePayment }` (SuperAdmin-only) | P0 |
| Define `FeatureOverviewQuery { featureOverview() }` returning era/feature matrix | P1 |
| Define tenant model: `Workspace` / `Organization` type with multi-tenant guards | P1 |
| Document tenant entitlement enforcement contract in `docs/governance.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement notifications service: create, list, mark-read in `app/services/notification.py` | P0 |
| Implement analytics service: aggregate event counts from `events` table | P1 |
| Implement `trackEvent` mutation: write to `events` table with `user_uuid`, `type`, `metadata` | P0 |
| Implement `adminStats()`: aggregated counts (users, contacts, jobs, revenue) for SuperAdmin | P0 |
| Implement `featureOverview()`: return feature flags / credits matrix per plan | P1 |
| Wire notifications polling in background task: dispatch on billing events, job completions | P1 |
| Add `require_super_admin()` guard for all admin mutations | P0 |
| Add plan-based entitlement guard: `require_plan_feature(info, feature)` | P1 |
| Webhook support: outbound webhook on job completion / campaign send | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Notification bell icon → `query notifications()` polling every 30s | P0 |
| Notification drop-down → `mutation markNotificationRead` on click | P0 |
| Analytics dashboard page → `query analytics(...)` with date range picker | P1 |
| Admin panel → `query adminStats()` + `mutation creditUser` | P0 |
| Feature overview page (pricing/plan) → `query featureOverview()` | P1 |
| Plan upgrade modal → triggered by `require_plan_feature` guard response | P1 |
| `useNotifications` hook: polling, badge count, mark-read | P0 |
| `useAdminPanel` hook: manage user credit adjustments, approve payments | P0 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `notifications` table: uuid, user_uuid, type, message, is_read, created_at | P0 |
| Create `events` table: uuid, user_uuid, type, metadata JSON, created_at | P0 |
| Create `feature_flags` table: feature, plan_id, enabled, credit_cost | P1 |
| Create `workspaces` table for multi-tenant model: uuid, name, owner_uuid, plan_id | P1 |
| Run Alembic migration for all 9.x tables | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure webhook secret `WEBHOOK_SECRET` for outbound events | P1 |
| Write test: `trackEvent → query analytics` round-trip | P1 |
| Write test: `notifications()` → `markAllRead` → `notifications() = []` | P1 |
| Load test admin panel with 10,000 user dataset | P1 |
| Document multi-tenant entitlement enforcement in ops runbook | P1 |

---

## Email app surface contributions (era sync)

- Defined ecosystem-level integration backlog for mailbox export and downstream integrations.
- Prepared route and table selection surfaces for integration-driven workflows.
