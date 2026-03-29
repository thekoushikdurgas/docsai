# Appointment360 Data Lineage (`contact360.io/api`)

## Service identity

- **Codebase**: `contact360.io/api`
- **Database**: PostgreSQL (async SQLAlchemy + asyncpg)
- **ORM**: Async SQLAlchemy `AsyncSession` with connection pool (size 25, max overflow 50)
- **Migration tool**: Alembic
- **Owns**: Users, auth tokens, credits, billing, activities, AI chats, saved searches, API keys, notifications, events

---

## Table lineage by era

### `users` — Era `0.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Generated on register | Identity for all cross-table FKs |
| `email` | TEXT UNIQUE | register mutation input | Lowercased and trimmed |
| `password_hash` | TEXT | bcrypt on register | Never exposed in GraphQL response |
| `role` | TEXT | Set on create: `user` default | `admin`, `super_admin` via `promoteUser` |
| `is_active` | BOOLEAN | True on create | False on soft delete |
| `created_at` | TIMESTAMPTZ | DB default `now()` | |
| `totp_secret` | TEXT NULL | Set by `enableTwoFactor` mutation | Added `8.x` |

**Lifecycle:** created by `register`, read by `me`/`user(uuid)`, deactivated by `deleteUser`.

---

### `token_blacklist` — Era `0.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `token_hash` | TEXT PK | SHA-256 of JWT string | Hashed to avoid storing sensitive token |
| `expires_at` | TIMESTAMPTZ | JWT `exp` claim | Cleanup job should prune expired rows |

**Lifecycle:** inserted by `logout` mutation; checked on every authenticated request in `get_context()`.

---

### `credits` — Era `1.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `id` | UUID PK | Auto-generated | |
| `user_uuid` | UUID FK → `users.uuid` | Created on subscription/purchase | |
| `feature` | TEXT | `email_finder`, `email_verifier`, `contact_export`, `ai_chat`, etc. | Feature-scoped credit buckets |
| `total` | INTEGER | Set on subscription / top-up | |
| `consumed` | INTEGER | Incremented by credit deduction service | |
| `reset_at` | TIMESTAMPTZ NULL | Billing period end date | Null for one-time credits |

**Lifecycle:** created by billing service on subscribe/addon purchase; read by `usage(feature)` query; incremented by all feature operations (email find, verify, export, AI message, etc.).

---

### `plans` — Era `1.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `id` | TEXT PK | Seed data | e.g. `starter`, `pro`, `enterprise` |
| `name` | TEXT | Seed data | Display name |
| `price` | DECIMAL | Seed data | Monthly price |
| `limits` | JSONB | Seed data | `{ "email_finder": 500, "contacts_export": 1000, ... }` |

**Lifecycle:** seeded at startup; read by `plans` query; used by billing service for limit enforcement.

---

### `subscriptions` — Era `1.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Auto-generated | |
| `user_uuid` | UUID FK → `users.uuid` | `subscribe` mutation | |
| `plan_id` | TEXT FK → `plans.id` | `subscribe` mutation | |
| `status` | TEXT | `active`, `cancelled`, `expired` | |
| `billing_period_start` | TIMESTAMPTZ | Set on subscribe | |
| `billing_period_end` | TIMESTAMPTZ | Set on subscribe | |

---

### `payment_submissions` — Era `1.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Auto-generated | |
| `user_uuid` | UUID FK → `users.uuid` | `submitPaymentProof` mutation | |
| `amount` | DECIMAL | Mutation input | |
| `proof_url` | TEXT | S3 URL of uploaded proof document | |
| `status` | TEXT | `pending`, `approved`, `declined` | |
| `reviewed_by` | UUID NULL FK → `users.uuid` | Admin `approvePayment`/`declinePayment` | |

---

### `activities` — Era `1.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Auto-generated | |
| `user_uuid` | UUID FK → `users.uuid` | All feature operations | |
| `type` | TEXT | `email_find`, `email_verify`, `contact_export`, `campaign_created`, `ai_chat_message`, etc. | |
| `metadata` | JSONB | Feature-specific payload | e.g. `{ "job_id": "...", "count": 100 }` |
| `created_at` | TIMESTAMPTZ | DB default | |

**Lifecycle:** written by all cross-cutting feature operations; read by `activities(limit, offset, type)` query.

---

### `ai_chats` — Era `5.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `createAiChat` mutation | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `title` | TEXT NULL | Derived or user-set | |
| `created_at` | TIMESTAMPTZ | DB default | |

**Note:** actual message content may be stored either in appointment360 DB or delegated entirely to `contact.ai` service. Validate current split before 5.x production.

---

### `ai_chat_messages` — Era `5.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `sendAiMessage` mutation | |
| `chat_uuid` | UUID FK → `ai_chats.uuid` | Mutation input | |
| `role` | TEXT | `user` or `assistant` | |
| `content` | TEXT | Mutation input / LambdaAI response | |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `resumes` — Era `5.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `createResume` mutation | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `content` | JSONB | Resume AI response | Structured resume data |
| `template_id` | TEXT NULL | Input field | |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `saved_searches` — Era `3.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `createSavedSearch` mutation | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `type` | TEXT | `contact` or `company` | |
| `name` | TEXT | Mutation input | |
| `vql_json` | JSONB | Serialized VQLQueryInput | Full VQL query state |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `api_keys` — Era `8.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `createApiKey` mutation | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `key_hash` | TEXT | SHA-256 of raw API key | Raw key shown once at creation only |
| `name` | TEXT | Mutation input | Human-readable label |
| `last_used_at` | TIMESTAMPTZ NULL | Updated on each API key auth | |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `sessions` — Era `8.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Created on login | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `ip` | TEXT | Request IP | |
| `user_agent` | TEXT | Request UA header | |
| `created_at` | TIMESTAMPTZ | DB default | |
| `last_seen_at` | TIMESTAMPTZ | Updated on subsequent requests | |

---

### `notifications` — Era `9.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Notification service | |
| `user_uuid` | UUID FK → `users.uuid` | Target user | |
| `type` | TEXT | `job_complete`, `billing_event`, `campaign_sent`, etc. | |
| `message` | TEXT | Service-generated | |
| `is_read` | BOOLEAN | Default false | |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `events` — Era `9.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | `trackEvent` mutation | |
| `user_uuid` | UUID FK → `users.uuid` | JWT context | |
| `type` | TEXT | Event type string | |
| `metadata` | JSONB | Event payload | |
| `created_at` | TIMESTAMPTZ | DB default | |

---

### `feature_flags` — Era `9.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `feature` | TEXT PK | Seed/admin | Feature name |
| `plan_id` | TEXT FK → `plans.id` | Seed/admin | Minimum plan to access |
| `enabled` | BOOLEAN | Default true | Kill switch |
| `credit_cost` | INTEGER | Seed/admin | Credits consumed per operation |

---

### `workspaces` — Era `9.x`

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `uuid` | UUID PK | Admin create | |
| `name` | TEXT | Input | |
| `owner_uuid` | UUID FK → `users.uuid` | | |
| `plan_id` | TEXT FK → `plans.id` | | |

---

## Cross-service data dependencies

| Appointment360 table / field | Cross-service reference | Notes |
| --- | --- | --- |
| `activities.metadata.job_id` | `contact360.io/jobs` `job_node.uuid` | Job UUID stored for traceability |
| `activities.metadata.campaign_id` | `backend(dev)/email campaign` `campaigns.id` | Campaign ID linked in activity log |
| `ai_chats.uuid` | `backend(dev)/contact.ai` `ai_chats.uuid` | May share table or be mirrored depending on 5.x implementation |
| `saved_searches.vql_json` | Connectra VQL | Must stay compatible with `ConnectraClient` VQL format |
| `credits.feature` | Lambda Email API, Connectra, contact.ai | Feature strings must match client deduction calls |

---

## Era activation summary

| Era | Tables added |
| --- | --- |
| `0.x` | `users`, `token_blacklist` |
| `1.x` | `credits`, `plans`, `subscriptions`, `payment_submissions`, `activities` |
| `3.x` | `saved_searches` |
| `5.x` | `ai_chats`, `ai_chat_messages`, `resumes` |
| `8.x` | `api_keys`, `sessions` (+ `totp_secret` column on `users`) |
| `9.x` | `notifications`, `events`, `feature_flags`, `workspaces` |
| `10.x` | No new appointment360 tables — campaign data lives in campaign service DB |
