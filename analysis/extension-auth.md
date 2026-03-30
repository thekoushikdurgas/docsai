# Extension authentication (roadmap stage 4.1)

## Modes

| Mode | Use case | Headers |
|------|----------|---------|
| **Lambda API key** | Extension → Sales Navigator scrape/save Lambda (`extension/contact360` client → `backend(dev)/salesnavigator`) | `X-API-Key` |
| **GraphQL JWT** | Same user identity as dashboard (`contact360.io/api`); refresh via `refreshToken` | `Authorization: Bearer <access>` |

Production flows may use **one or both** (e.g. API key for Lambda, Bearer for future gateway routes).

## GraphQL refresh contract

- **Mutation:** `auth { refreshToken(input: { refreshToken }) { accessToken refreshToken } }`
- **Alignment:** Same shape as `contact360.io/app/src/lib/graphqlClient.ts` and `authService.ts`.

## Canonical module: `extension/contact360/auth/graphqlSession.js`

Authoritative detail: [`docs/codebases/extension-codebase-analysis.md`](../codebases/extension-codebase-analysis.md) § `auth/graphqlSession.js`.

### Public helpers (token lifecycle)

| Function | Behaviour |
| --- | --- |
| `decodeJWT(token)` | Base64url-decodes the JWT payload; no external library |
| `isTokenExpired(token, bufferSeconds?)` | Returns `true` if `exp` is within `bufferSeconds` (default: 300 s = 5 min) |
| `getStoredTokens()` | Reads `{ accessToken, refreshToken }` from `chrome.storage.local` |
| `storeTokens(tokens)` | Persists both tokens to `chrome.storage.local` |
| `refreshAccessToken(refreshToken)` | Calls Appointment360 `auth.refreshToken` mutation via `fetch`; stores result |
| `getValidAccessToken()` | Checks expiry, calls `refreshAccessToken` proactively; returns valid token |

Higher-level wrappers used by callers may compose the above (e.g. `ensureAccessToken`, single-flight refresh); keep behaviour aligned with the table.

### Chrome MV3 storage

- All storage I/O should use `chrome.storage.local` wrapped in Promises.
- **Do not** put tokens in `chrome.storage.sync` (quota and sync surface area).
- Optional: `createChromeStorageAdapter()` pattern in analysis — use for test doubles or future storage backends while keeping the same async contract.

### Test coverage

- **`extension/contact360/tests/hybridFlow.test.js`** — integration-style: session refresh → client batching path (see codebase analysis).

## MV3 constraints

| Constraint | Requirement |
| --- | --- |
| Storage | Use chrome.storage.local; avoid chrome.storage.sync for tokens |
| Background lifecycle | Refresh logic must survive service worker restarts |
| Header usage | Use Bearer for gateway routes and API key only for designated lambda routes |

## Integration checklist

1. After dashboard login, copy or sync `access_token` / `refresh_token` into extension storage (or open OAuth flow in extension).
2. Before GraphQL calls from the extension, ensure a valid access token via `getValidAccessToken()` / `ensureAccessToken`-style wrapper with proactive refresh (~5 min buffer).
3. Optionally pass Bearer from the same session into `extension/contact360/utils/lambdaClient.js` when the save API accepts `Authorization`.

## Paths

- Legacy tree: `extention/contact360/` (typo) — JS utils + Python Lambda.
- Canonical: `extension/contact360/` — new auth and future `manifest.json` / `src/`.


## References

- [docs/codebases/appointment360-codebase-analysis.md](../codebases/appointment360-codebase-analysis.md)
