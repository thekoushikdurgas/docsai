# Connectra user-billing task pack (`1.x`)

## Scope

Align Connectra search/export volume with credit and billing contracts.

## Codebase evidence (contact360.io/sync)

- Runtime:
  - Go + Gin HTTP server
  - middleware includes token-bucket rate limiter and API key auth
- Data plane:
  - PostgreSQL (`contacts`, `companies`, `jobs`, `filters`, `filters_data`)
  - Elasticsearch (`contacts_index`, `companies_index`)
- Query mechanics:
  - VQL → ES IDs → PG hydrate → in-memory joins
- Route surface (billing-relevant):
  - `POST /contacts/`, `POST /contacts/count`, `POST /contacts/batch-upsert`
  - `POST /companies/`, `POST /companies/count`, `POST /companies/batch-upsert`
  - `GET|POST /common/:service/filters`, `GET|POST /common/:service/filters/data`
  - `GET /common/upload-url`, `POST /common/jobs`, `POST /common/jobs/create` (job flows)

## Small tasks

- **Contract:** Define credit-aware search/export usage policy and reject semantics when limits are exhausted.
- **Service:** Add gateway-side guardrails before Connectra-heavy queries and export job creation.
- **Database:** Track usage evidence in usage/ledger tables tied to Connectra query and export actions.
- **Flow:** Trace `/contacts` and `/companies` query events through billing and activity logging paths.
- **Release gate evidence:** Quota tests, over-limit behavior snapshots, and audit trail proof for billing reconciliation.

## Billing-relevant mechanics (VQL, guardrails, parallel writes)

- VQL execution modes (request -> ES/PG query shape):
  - `exact` → `match_phrase` (+ optional `slop`)
  - `shuffle` → `match` (fuzzy/operator tuning)
  - `substring` → ngram-backed matching
  - `keyword_match` + `range_query` for exact/numeric/date boundaries
- Gateway guardrails (credit/billing enforcement point):
  - reject before issuing heavy VQL requests when credits are exhausted
  - ensure gateway attaches correlation evidence to usage/activity records
- Appointment360 client:
  - `app/clients/connectra_client.py` (`ConnectraClient`) is the single call site; it should only be invoked after credit/billing pre-checks.
- Parallel write/upsert:
  - bulk upserts execute in parallel (PG + ES stores) inside `BulkUpsertToDb`, so uncontrolled retries can multiply load—credit idempotency and retry-safe behavior must be enforced at the gateway/job layer.

## Root/Admin surface contributions (era sync)

- **`contact360.io/root`**: user/billing CTAs, pricing and auth-form hooks/services (`usePricing`, `useAuthForm`, billing/auth GraphQL services).
- **`contact360.io/admin`**: payment submission review and admin billing controls (approve/decline flows), user-role governance surfaces.

---

## Extension surface contributions (era sync)

### Era 1.x — User/Billing/Credit

**`extension/contact360` auth layer:**
- `auth/graphqlSession.js` — `getValidAccessToken()` and `refreshAccessToken()` fully implemented
- Token lifecycle: `accessToken` + `refreshToken` stored in `chrome.storage.local` only
- `auth.refreshToken` GraphQL mutation on Appointment360 established as the extension auth contract
- `isTokenExpired()` with 300-second buffer prevents mid-scrape token expiry

**Tasks:**
- [ ] Confirm Appointment360 `auth.refreshToken` mutation returns `{ accessToken, refreshToken, expiresIn }`
- [ ] Verify `chrome.storage.local` token keys (`accessToken`, `refreshToken`) are consistent with any future auth refactor
- [ ] Document token security policy (no logging, no sync storage, no third-party transmission) in governance