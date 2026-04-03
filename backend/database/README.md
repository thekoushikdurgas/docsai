# Database Schema SQL Files (Contact360 / appointment360)

This directory holds **reference SQL** for the Contact360 stack (user-facing product) and the historical **appointment360** naming used in some paths and docs. The live app database may be provisioned from the same shapes under `backend(dev)/` in the monorepo; treat these files as the **docs-side source of truth** for table layout and seed data.

## CSV seed data (`csv/`)

| File | Typical table | Notes |
|------|----------------|-------|
| `subscription_plans.csv` | `subscription_plans` | Leading `#` column is row index — use `sql load-csv --preset subscription_plans` |
| `subscription_plan_periods.csv` | `subscription_plan_periods` | Same `#` convention |
| `addon_packages.csv` | `addon_packages` | Same `#` convention |
| `user_profiles.csv` | `user_profiles` | No `#` column |

Load from the **docs CLI** (requires `scripts/data` Postgres config):

```bash
cd docs
python cli.py sql load-csv --preset subscription_plans
python cli.py sql load-csv --csv backend/database/csv/user_profiles.csv --table user_profiles
```

## Docs CLI: SQL runner

Run arbitrary SQL files (split is dollar-quote and string aware). Optional **strip comments** then **format** (needs `pip install sqlparse` for `--format-sql`):

```bash
cd docs
python cli.py sql run -f backend/database/extensions.sql
python cli.py sql run --dry-run -f backend/database/enums.sql --strip-comments
python cli.py sql init-schema --dry-run --strip-comments
python cli.py sql run -f backend/database/users.sql --strip-comments --format-sql --write-processed scripts/sql/_out.sql
```

## File Organization

### Core Files

- `extensions.sql` - PostgreSQL extensions (pg_trgm)
- `enums.sql` - All PostgreSQL ENUM type definitions
- `init_schema.sql` - Master initialization script (runs all files in correct order)

### CRUD examples (`crud/`)

- One file per core table: [`crud/README.md`](crud/README.md) — illustrative **SELECT / INSERT / UPDATE / DELETE** patterns (placeholders; not a migration).

### Table Files

Each table lists its primary GraphQL module(s). Full table↔module maps: see [docs/SCHEMA_AND_MODULES.md](../../docs/SCHEMA_AND_MODULES.md).

- `users.sql` - User authentication and account management (auth, users)
- `user_profiles.sql` - Extended user information and billing (auth, users, billing)
- `user_history.sql` - Registration/login events with IP geolocation (auth)
- `user_activities.sql` - LinkedIn/email service activity tracking (activities, jobs, email)
- `feature_usage.sql` - Feature usage tracking per user (usage, jobs)
- `notifications.sql` - User notifications (notifications)
- `subscription_plans.sql` - Subscription plan tiers (billing)
- `subscription_plan_periods.sql` - Pricing periods for subscription plans (billing)
- `addon_packages.sql` - Addon credit packages (billing)
- `performance_metrics.sql` - Frontend performance metrics (analytics)
- `token_blacklist.sql` - Blacklisted refresh tokens (auth)
- `user_scraping.sql` - Sales Navigator scraping metadata per user (sales_navigator)
- `scheduler_jobs.sql` - Gateway-owned job rows (email.server / sync.server); `job_type` TEXT + taxonomy columns; status `retry` when applicable via `jobs.retryJob` (jobs)
- `saved_searches.sql` - Saved search queries with filters and settings (saved_searches)
- `api_keys.sql` - API key management for users (profile)
- `sessions.sql` - User session tracking and management (auth, profile)
- `two_factor.sql` - Two-factor authentication settings and backup codes (two_factor)
- `team_members.sql` - Team management and member invitations (profile)
- `ai_chats.sql` - AI chat threads and message JSON per user (contact.ai / Contact AI Lambda; shares DB with appointment360)
- `resume_documents.sql` - Resume metadata per user; JSON in s3storage under `resume/` (resumeai; GraphQL resume module)
- `payment_settings.sql` - UPI/QR display settings for manual payments (billing)
- `payment_submissions.sql` - Manual payment proof queue (billing)
- `campaign_templates.sql` - Reusable email bodies (campaigns; eras 8.x–10.x)
- `campaigns.sql` - Campaign headers and status (campaigns)
- `campaign_sequences.sql` - Steps per campaign (campaigns)
- `webhooks.sql` - Outbound webhook registrations (integrations)
- `integrations.sql` - Third-party OAuth/integration rows (integrations)
- `s3storage_metadata_jobs.sql` - Async metadata reconciliation queue (s3storage worker)
- `seed_user_profiles.sql` - **Optional** dev seed for `user_profiles` (not run by `init_schema.sql`)
- `migrations/` - One-off ALTER/backfill scripts (e.g. `migrate_resume_documents_to_s3_keys.sql`)

## Execution Order

The files must be executed in the following order due to dependencies:

1. `extensions.sql` - Extensions must be created first
2. `enums.sql` - ENUM types must exist before tables that use them
3. `users.sql` - Base table, referenced by many others
4. `user_profiles.sql` - References users
5. `user_history.sql` - References users
6. `user_activities.sql` - References users
7. `feature_usage.sql` - References users
8. `notifications.sql` - References users
9. `performance_metrics.sql` - References users
10. `token_blacklist.sql` - References users
11. `user_scraping.sql` - References users
12. `scheduler_jobs.sql` - References users; `job_type` TEXT; status uses `scheduler_job_status` ENUM where applicable
13. `saved_searches.sql` - References users
14. `api_keys.sql` - References users
15. `sessions.sql` - References users
16. `two_factor.sql` - References users (one-to-one)
17. `team_members.sql` - References users (owner and member)
18. `ai_chats.sql` - References `users(uuid)`; chat payload for Contact AI service (`backend(dev)/contact.ai`)
19. `resume_documents.sql` - References `users(uuid)`; resume JSON for AI resume editor
20. `subscription_plans.sql` - Base table for billing
21. `subscription_plan_periods.sql` - References subscription_plans
22. `addon_packages.sql` - Independent table
23. `payment_settings.sql` - Manual payment display config
24. `payment_submissions.sql` - References `users`
25. `campaign_templates.sql` - References `users`
26. `campaigns.sql` - References `users`; uses `campaign_status`
27. `campaign_sequences.sql` - References `campaigns`
28. `webhooks.sql` - References `users`
29. `integrations.sql` - References `users`
30. `s3storage_metadata_jobs.sql` - Standalone queue table

## Usage

### Option 1: Use the master initialization script
```bash
psql -U postgres -d appointment360 -f sql/tables/init_schema.sql
```

### Option 2: Execute files individually in order
```bash
psql -U postgres -d appointment360 -f sql/tables/extensions.sql
psql -U postgres -d appointment360 -f sql/tables/enums.sql
# ... continue with remaining files in order
```

### Option 3: Use Python script (recommended)
```bash
python scripts/init_schema.py
```

## Contact AI table

- **`ai_chats`**: created by `ai_chats.sql` (included in `init_schema.sql`). For legacy databases missing the table, run `ai_chats.sql` directly — it is idempotent (`CREATE TABLE IF NOT EXISTS`).
- **ORM reference**: `backend(dev)/contact.ai/app/models/ai_chat.py` (`AIChat`). API identifies chats by **`uuid`**; `id` is the internal primary key.

## Connectra-related data stores

Connectra (`contact360.io/sync`) primarily owns hybrid search lineage:

- PostgreSQL tables: `contacts`, `companies`, `jobs`, `filters`, `filters_data`
- Elasticsearch indices: `contacts_index`, `companies_index`

The gateway modules (`03_CONTACTS_MODULE.md`, `04_COMPANIES_MODULE.md`) consume these via Connectra REST paths. See `docs/backend/database/connectra_data_lineage.md` for era-aware lineage controls.

## Notes

- All SQL files use `IF NOT EXISTS` clauses to be idempotent
- ENUM types use `DO $$ BEGIN ... EXCEPTION WHEN duplicate_object THEN null; END $$;` blocks for idempotency
- Foreign key constraints are included in table definitions
- All indexes are created with `IF NOT EXISTS` for safety
- ENUM types are defined separately to allow easy modification
- The schema is designed for PostgreSQL with asyncpg driver support
- All files can be safely executed multiple times without errors

### Storage, logical buckets, and keys

- The database schema stores a per-user logical bucket id in the `users.bucket` column. By default this is the same as `users.uuid`, but it is persisted explicitly so it can evolve independently.
- Application modules (Jobs, Exports, etc.) reference files by opaque `file_key` strings that are **relative to the logical bucket root**, for example:
  - `avatar/{user_uuid}.jpg` – user avatar image
  - `upload/20260210_120000_contacts.csv` – CSV uploaded by the user
  - `resume/{resume_document_id}.json` – AI resume JSON (resumeai; `resume_documents.resume_data_key`)
- The `s3storage` service maps these logical keys into a single physical S3 bucket by prefixing them with the logical bucket id, e.g. `{bucket_id}/avatar/{user_uuid}.jpg` or `{bucket_id}/upload/20260210_120000_contacts.csv`.
- Actual storage (per-user logical buckets, CSV previews, multipart uploads, avatars) is handled entirely by the `s3storage` service and AWS S3; see [07_S3_MODULE.md](../graphql.modules/07_S3_MODULE.md) and [10_UPLOAD_MODULE.md](../graphql.modules/10_UPLOAD_MODULE.md) for details.

## User deletion cascade

All user-scoped tables reference `users(uuid)` with `ON DELETE CASCADE`. Deleting a user removes rows in: user_profiles, user_history, user_activities, feature_usage, notifications, performance_metrics, token_blacklist, user_scraping, scheduler_jobs, saved_searches, api_keys, sessions, two_factor, team_members, **ai_chats**, **resume_documents**. See [docs/SCHEMA_AND_MODULES.md](../../docs/SCHEMA_AND_MODULES.md#user-deletion-cascade) for the full list.

---

## Naming

- SQL files: `snake_case.sql`; lineage markdown: descriptive names aligned with service + table ownership in [`../README.md`](../README.md).

## Structure contract

- `init_schema.sql` defines execution order; new tables must document GraphQL module mapping (see **Table Files** above).
- Narrative lineage docs in this tree should cross-link `docs/backend/graphql.modules/` and `docs/codebases/*-codebase-analysis.md`.

## File index

- **SQL:** files in this directory per **File Organization** above.
- **CSV:** `csv/*.csv` — billing/user profile seeds; see **CSV seed data** and `sql load-csv --preset`.
- **Lineage / drift:** companion `*.md` files alongside SQL or under sibling folders — see [`../README.md`](../README.md) registry.