# Appointment360 (contact360.io/api) — Era 1.x User, Billing & Credit Task Pack

## Codebase reference (appointment360 GraphQL gateway)

- GraphQL runtime is composed in a single endpoint: `/graphql` with `Query`/`Mutation` roots and module namespaces (auth, email, jobs, usage, billing, admin, twoFactor, etc.).
- Request lifecycle middleware classes (relevant to billing/credit correctness):
  - `GraphQLIdempotencyMiddleware` (replays by `X-Idempotency-Key`),
  - `GraphQLMutationAbuseGuardMiddleware` (high-risk mutation throttling),
  - `GraphQLRateLimitMiddleware` (per-IP `/graphql` throttling),
  - `DatabaseCommitMiddleware` (ensures DB commits after each request),
  - request/trace propagation (`RequestIdMiddleware`, `TraceIdMiddleware`).
- Core guards/errors/context:
  - auth + access control: `app/core/security.py` (`require_auth`, `require_admin`),
  - per-request context: `app/graphql/context.py` (`Context.user_uuid`, `dataloaders`),
  - error handling: `app/graphql/errors.py`.
- Module paths (1.x scope):
  - Auth: `app/graphql/modules/auth/`,
  - Usage: `app/graphql/modules/usage/`,
  - Billing: `app/graphql/modules/billing/`,
  - Admin: `app/graphql/modules/admin/`,
  - Email finder/verifier: `app/graphql/modules/email/`.
- External clients used in 1.x flows:
  - Email provider calls: `app/clients/LambdaEmailClient`,
  - Storage proof calls: `app/clients/LambdaS3StorageClient`,
  - Billing/audit logs: `app/clients/LambdaLogsClient`,
  - Connectra search/provider sources: `app/clients/ConnectraClient`.

## Contract track

| Task | Priority |
| --- | --- |
| Define `AuthQuery { me }` returning `UserType` with all profile fields | P0 |
| Define `AuthMutation { login, register, logout, refreshToken }` with typed inputs/outputs | P0 |
| Define `BillingQuery { billingInfo, plans, invoices }` | P0 |
| Define `BillingMutation { subscribe, purchaseAddon, submitPaymentProof, approvePayment, declinePayment }` | P0 |
| Define `UsageQuery { usage(feature) }` returning credits remaining / consumed | P0 |
| Define `UserQuery { user(uuid), users(), userStats() }` with admin-guarded overloads | P0 |
| Define `UserMutation { updateUser, deleteUser, promoteUser }` | P0 |
| Document all auth types in `docs/backend/apis/01_AUTH_MODULE.md` | P1 |
| Document all billing types in `docs/backend/apis/10_BILLING_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `login` mutation: validate credentials, issue HS256 JWT access + refresh tokens | P0 |
| Implement `register` mutation: hash password, create user, issue tokens | P0 |
| Implement `logout` mutation: insert token into `token_blacklist` table | P0 |
| Implement `refreshToken` mutation: validate refresh token, issue new access token | P0 |
| Implement `me` query: extract `user` from `Context`, return `UserType` | P0 |
| Implement `require_auth(info)` guard in `core/security.py` | P0 |
| Implement `require_admin(info)` guard for admin-only mutations | P0 |
| Implement credit deduction service: `deduct_credit(user_uuid, feature, amount)` | P0 |
| Implement `usage(feature)` query: read credit totals from `credits` table | P0 |
| Implement billing service: plan lookup, subscription creation, add-on purchase | P1 |
| Implement `submitPaymentProof` + admin `approvePayment`/`declinePayment` flow | P1 |
| Wire `idempotency` middleware to `subscribe`, `purchaseAddon`, `submitPaymentProof` mutations | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| `/login` page → `mutation login` binding in `authService.ts` | P0 |
| `/register` page → `mutation register` binding | P0 |
| User profile page → `query me` + `mutation updateProfile` binding | P0 |
| Billing page → `query billingInfo` + `query plans` + `mutation subscribe` binding | P1 |
| Credits counter component (header bar) → `query usage` polling on route change | P0 |
| Admin user list page → `query users` + `mutation promoteUser` bindings | P1 |
| `useAuth` hook: login, logout, refresh token auto-retry on 401 | P0 |
| `useBilling` hook: subscribe, purchase add-on, submit payment proof | P1 |
| `useCredits` hook: poll credits, show low-credit warning modal | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `credits` table: user_uuid, feature, total, consumed, reset_at | P0 |
| Create `plans` table: id, name, price, limits JSON | P0 |
| Create `subscriptions` table: user_uuid, plan_id, status, billing_period_start, billing_period_end | P0 |
| Create `token_blacklist` table: token_hash, expires_at | P0 |
| Create `payment_submissions` table: uuid, user_uuid, amount, proof_url, status, reviewed_by | P1 |
| Create `activities` table: uuid, user_uuid, type, metadata JSON, created_at | P0 |
| Run Alembic migration for all 1.x tables | P0 |
| Seed plans table with starter/pro/enterprise tiers | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `ACCESS_TOKEN_EXPIRE_MINUTES` (30) and `REFRESH_TOKEN_EXPIRE_DAYS` (7) | P0 |
| Add `SECRET_KEY` rotation procedure to ops runbook | P0 |
| Wire GraphQL `Idempotency-Key` to billing mutations in Postman collection | P1 |
| Write test: `login → me → logout → me → error` flow | P1 |
| Write test: `register → consume credit → query usage → low-credit guard` | P1 |

---

## Email app surface contributions (era sync)

- Implemented login/signup page flows and account profile management route.
- Added logout flow and user fetch (`/auth/user/{id}`) in sidebar/account surfaces.
