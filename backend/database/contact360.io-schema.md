# contact360.io/api — Gateway PostgreSQL schema

**Service:** FastAPI + SQLAlchemy (async) + Alembic  
**Database:** PostgreSQL (single logical DB; optional read replica via `DATABASE_REPLICA_URL`)  
**Migrations:** `contact360.io/api/alembic/versions/`

## Alembic revision chain

| Revision | Description |
|----------|-------------|
| `20260326_0001` | Baseline `users`, `token_blacklist` |
| `20260329_0002` | `graphql_idempotency_replays`, `upload_sessions` |
| `20260401_0003` | `graphql_abuse_guard_events` |
| `20260402_0004` | `graphql_audit_events` |
| `20260410_0005` | `scheduler_jobs` job taxonomy columns |
| `20260410_0006` | `users` password reset columns |
| `20260411_0007` | Scheduler job billing columns |

Run: `cd contact360.io/api && alembic upgrade head`

## Core tables (ORM `app/models/`)

| Table | Model | Purpose |
|-------|--------|---------|
| `users` | `User` | Accounts, roles, auth |
| `user_profiles` | `UserProfile` | Profile fields, credits, preferences JSON |
| `user_history` | `UserHistory` | Audit trail |
| `user_activities` | `UserActivity` | Activity feed |
| `feature_usage` | `FeatureUsage` | Feature usage counters |
| `token_blacklist` | `TokenBlacklist` | Revoked JWT hashes |
| `sessions` | `Session` | Refresh / device sessions |
| `api_keys` | `ApiKey` | User API keys for programmatic access |
| `two_factor` | `TwoFactor` | 2FA secrets and backup codes |
| `team_members` | `TeamMember` | Org/workspace team membership |

## Billing & payments

| Table | Model | Purpose |
|-------|--------|---------|
| `subscription_plans` | `SubscriptionPlan` | Plan catalog |
| `subscription_plan_periods` | `SubscriptionPlanPeriod` | Billing periods per plan |
| `addon_packages` | `AddonPackage` | Add-on catalog |
| `payment_settings` | `PaymentSettings` | Org-level payment instructions / UPI |
| `payment_submissions` | `PaymentSubmission` | Manual payment proofs (pending/approved) |

## Jobs & operations

| Table | Model | Purpose |
|-------|--------|---------|
| `scheduler_jobs` | `SchedulerJob` | Long-running export/import jobs (Connectra, email, phone, etc.) |

## Notifications & saved searches

| Table | Model | Purpose |
|-------|--------|---------|
| `notifications` | `Notification` | In-app notifications |
| `saved_searches` | `SavedSearch` | Saved VQL / filter presets |

## GraphQL infrastructure

| Table | Purpose |
|-------|---------|
| `graphql_idempotency_replays` | Idempotent mutation replay cache (POST body hash) |
| `upload_sessions` | Multipart upload session state (JSONB) |
| `graphql_abuse_guard_events` | Per-actor mutation rate limiting |
| `graphql_audit_events` | Optional GraphQL audit events |

## Other

| Table | Model | Purpose |
|-------|--------|---------|
| `performance_metrics` | `PerformanceMetric` | Aggregated performance samples |
| `user_scraping` | `UserScraping` | Scraping / enrichment usage tracking |

## Not stored in gateway Postgres

- **Contacts / companies / VQL index:** Connectra (`EC2/sync.server`)
- **Campaigns / sequences / templates:** campaign.server (`EC2/campaign.server`)
- **Resume documents:** external Resume AI service (`RESUME_AI_BASE_URL`)
- **S3 object bytes:** S3 + s3storage.server metadata
- **Centralized log hot store:** log.server (gateway may push via `LogsServerClient`)

## Row-level security

Application code sets tenant context where applicable; see [`docs/DECISIONS.md`](../../DECISIONS.md) RLS pattern.
