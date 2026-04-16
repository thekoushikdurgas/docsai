# Era 1 — Auth

**Goal:** JWT refresh in service worker before gateway calls.

**Checklist**

- [x] `background.js` imports `auth/graphqlSession.js` + `services/gatewayClient.js`
- [x] `C360Gateway.getBearerFromRefresh` uses `ensureAccessToken` + `c360_graphql_url`
- [x] `docs/backend/endpoints/contact360.io/AUTH-ENV.md` — extension section
