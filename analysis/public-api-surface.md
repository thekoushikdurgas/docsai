# Public API Surface (8.x)

## Public Auth Path

`createApiKey` -> `api_keys` table -> `apikey_auth_guard` -> scoped GraphQL operations.

## Module Operations

- `profile`: `apiKeys()`, `sessions()`, `createApiKey`, `deleteApiKey`
- `twoFactor`: `enableTwoFactor`, `verifyTwoFactor`, `disableTwoFactor`
- `savedSearches`: `savedSearch(id)`, `savedSearches(type)`, create/update/delete mutations

## References

- `docs/backend/apis/26_SAVED_SEARCHES_MODULE.md`
- `docs/backend/apis/27_TWO_FACTOR_MODULE.md`
- `docs/backend/apis/28_PROFILE_MODULE.md`

## Postman Validation Checklist

- API key creation and revocation flow
- `X-API-Key` auth on allowed public operations
- forbidden response on out-of-scope operations
- rate-limit headers and `Retry-After` behavior
