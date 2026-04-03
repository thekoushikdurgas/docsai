# Extension GraphQL Session Contract (`graphqlSession.js`)

Describes the JWT access + refresh token lifecycle implemented in `contact360.extension/auth/graphqlSession.js` (Stage 3.1).

## Overview

The extension maintains a two-token session that mirrors the dashboard (`app.contact360.io`) semantics:

| Token | Storage key | Purpose |
|---|---|---|
| Access JWT | `c360_extension_access_token` | Bearer token for GraphQL requests |
| Refresh JWT | `c360_extension_refresh_token` | Used to obtain a new access token when expiring |

Both tokens are persisted in **`chrome.storage.local`** (Manifest V3 background + popup).

---

## Token Lifecycle State Machine

```
Not authenticated → [user logs in via dashboard/OAuth]
        ↓
AUTHENTICATED   (access JWT valid, exp > now + 60 s buffer)
        ↓ (exp approaching)
EXPIRING_SOON  (access JWT < 60 s from expiry, refresh token present)
        ↓ (access JWT expired, refresh token still present)
REFRESH_ONLY   (no valid access token, refresh token still valid)
        ↓ (ensureAccessToken called)
AUTHENTICATED  (new access + refresh pair written to chrome.storage.local)
        ↓ (refresh fails / no refresh token)
UNAUTHENTICATED
```

### State display (popup.js badge)

| State | Badge variant | Label |
|---|---|---|
| AUTHENTICATED | `ok` | "Authenticated" |
| EXPIRING_SOON | `warn` | "Access expiring (refresh available)" |
| REFRESH_ONLY | `warn` | "Refresh token only" |
| UNAUTHENTICATED | `bad` | "Not authenticated" |

---

## Refresh Contract

### GraphQL mutation (called by `refreshWithGraphQL`)

```graphql
mutation RefreshToken($input: RefreshTokenInput!) {
  auth {
    refreshToken(input: $input) {
      accessToken
      refreshToken
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "refreshToken": "<current_refresh_jwt>"
  }
}
```

**Success response shape:**

```json
{
  "data": {
    "auth": {
      "refreshToken": {
        "accessToken": "<new_access_jwt>",
        "refreshToken": "<new_refresh_jwt>"
      }
    }
  }
}
```

**Error response:**

```json
{
  "errors": [{ "message": "<error string>" }]
}
```

If `accessToken` or `refreshToken` is missing from the success payload, the refresh throws `"Invalid refresh response"` and the extension falls back to `UNAUTHENTICATED`.

### Refresh trigger — `ensureAccessToken`

Called before every GraphQL request originating from the extension (background service worker or content script). The buffer is **60 000 ms (1 min)** before JWT `exp`.

```js
// Pseudocode call site (background.js):
const token = await ensureAccessToken({
  graphqlUrl: GRAPHQL_URL,
  loadTokens: adapter.loadTokens,   // reads chrome.storage.local
  saveTokens: adapter.saveTokens,   // writes chrome.storage.local
});
if (!token) throw new Error("Not authenticated");
```

### Chrome storage adapter

| Method | chrome.storage keys read/written |
|---|---|
| `loadTokens()` | `c360_extension_access_token`, `c360_extension_refresh_token` |
| `saveTokens(access, refresh)` | `c360_extension_access_token`, `c360_extension_refresh_token` |

---

## Global export (non-module context)

```js
globalThis.Contact360GraphQLSession = {
  isAccessTokenExpired,   // (token, bufferMs?) → boolean
  refreshWithGraphQL,     // ({ graphqlUrl, refreshToken }) → { accessToken, refreshToken }
  ensureAccessToken,      // (opts) → Promise<string|null>
  createChromeStorageAdapter, // () → { loadTokens, saveTokens }
  STORAGE_ACCESS,         // "c360_extension_access_token"
  STORAGE_REFRESH,        // "c360_extension_refresh_token"
};
```

---

## Related documentation

| Doc | Purpose |
|---|---|
| [salesnavigator.api.md](salesnavigator.api.md) | Extension server / harvest flows |
| [extension-telemetry-schema.md](extension-telemetry-schema.md) | Telemetry log event schema |
| [logsapi.api.md](logsapi.api.md) | Logs API service contract |
| [salesnavigator_endpoint_era_matrix.md](../endpoints/salesnavigator_endpoint_era_matrix.md) | Extension HTTP route inventory |
| [mutation_create_log_graphql.md](../endpoints/mutation_create_log_graphql.md) | CreateLog mutation (auth path used by extension) |

---

## Era traceability

| Era | Milestone |
|---|---|
| 0.x | Chrome storage adapter wired; `ensureAccessToken` called from background |
| 4.x | Popup displays auth state machine badge; tab-switch UI added |
| 6.x | Telemetry events keyed to token state transitions |
