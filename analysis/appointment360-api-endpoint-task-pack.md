# Appointment360 (contact360.io/api) — Era 8.x Public & Private APIs Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `PagesQuery { page(id), pages(type) }` for DocsAI-backed content | P0 |
| Define `SavedSearchQuery { savedSearch(id), savedSearches(type) }` | P0 |
| Define `SavedSearchMutation { createSavedSearch, updateSavedSearch, deleteSavedSearch }` | P0 |
| Define `ProfileQuery { apiKeys(), sessions() }` | P0 |
| Define `ProfileMutation { createApiKey, deleteApiKey, updateProfile }` | P0 |
| Define `TwoFactorQuery { twoFactorStatus() }` | P0 |
| Define `TwoFactorMutation { enableTwoFactor, verifyTwoFactor, disableTwoFactor }` | P0 |
| Define public API key authentication path: `X-API-Key` header → `apikey_auth_guard` | P0 |
| Document public vs private API surface in `docs/backend/apis/08_PUBLIC_API_MODULE.md` | P1 |
| Create API key usage docs for external developers | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `DocsAIClient` in `app/clients/docsai_client.py` | P0 |
| Wire `pages(type)` query → `DocsAIClient.list_pages(type)` | P0 |
| Wire `page(id)` query → `DocsAIClient.get_page(id)` | P0 |
| Set `DOCSAI_ENABLED` flag; pages module gracefully returns empty if disabled | P0 |
| Add `/health` check for DocsAI dependency | P1 |
| Implement `savedSearches` CRUD in `app/repositories/saved_search.py` | P0 |
| Implement `apiKeys` CRUD in `app/repositories/profile.py` | P0 |
| Implement `sessions` list in `app/repositories/profile.py` | P0 |
| Implement TOTP-based 2FA: `pyotp` library, `totp_secret` column in `users` | P1 |
| Implement public API key auth guard: `X-API-Key` → user lookup → `Context.user` | P0 |
| Wire public API key auth through same context layer (bypass JWT) | P0 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Profile page → `query apiKeys()` + `mutation createApiKey` / `deleteApiKey` | P0 |
| Profile page, sessions tab → `query sessions()` | P0 |
| Profile page, 2FA section → `query twoFactorStatus()` + mutations | P1 |
| Saved searches sidebar on `/contacts` and `/companies` → `query savedSearches(type)` | P0 |
| Save search button → `mutation createSavedSearch(name, type, vql_json)` | P0 |
| DocsAI-powered help widget → `query pages(type: "help")` | P1 |
| API key copy button with one-time display + masked subsequent views | P0 |
| `useSavedSearches` hook: load, apply, create, delete | P0 |
| `useApiKeys` hook: create, revoke, list | P0 |
| `useTwoFactor` hook: enable flow, verify OTP, disable | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `api_keys` table: uuid, user_uuid, key_hash, name, last_used_at, created_at | P0 |
| Create `saved_searches` table: uuid, user_uuid, type (contact/company), name, vql_json, created_at | P0 |
| Create `sessions` table: uuid, user_uuid, ip, user_agent, created_at, last_seen_at | P1 |
| Add `totp_secret` column to `users` table for 2FA | P1 |
| Run Alembic migration for all 8.x tables | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `DOCSAI_API_URL`, `DOCSAI_API_KEY`, `DOCSAI_ENABLED` in `.env.example` | P0 |
| Write Postman collection for public API: `X-API-Key` authentication path | P1 |
| Rate-limit public API key requests separately from authenticated user requests | P1 |
| Write test: `createApiKey → query contacts with X-API-Key → verify access` | P1 |
| Document rate limit tiers for public API in developer docs | P1 |

---

## Email app surface contributions (era sync)

- Endpoint consumption matrix locked for auth, mailbox, and account APIs.
- Added consumer-facing endpoint era matrix artifact: `emailapp_endpoint_era_matrix.json`.
