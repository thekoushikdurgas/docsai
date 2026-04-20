# Era 1 — Auth

**Goal:** JWT refresh in service worker before GraphQL save/scrape calls; sign-in and sign-out in the side panel.

**Checklist**

- [x] `background.js` imports `auth/graphqlSession.js` + `services/gatewayClient.js`
- [x] `C360_AUTH_LOGIN` / `C360_AUTH_LOGOUT` — `auth.login` / `auth.logout` via GraphQL; tokens in `chrome.storage.local`
- [x] `services/gatewayClient.js` uses `ensureAccessToken` + `c360_graphql_url` for Bearer on `POST /graphql`
- [x] `graphqlSession.js` — failed refresh clears stored tokens
- [x] Side panel — email/password, Sign in / Sign out; 2FA accounts get a toast (use web app or future `completeTwoFactorLogin`)
- [x] `docs/backend/endpoints/contact360.io/AUTH-ENV.md` — extension section

### Rewrite checklist (v2.0)

- [ ] `src/services/graphqlSession.ts` + `AuthContext` / `useAuth` + `LoginModal` / `AccountChip` / `AccountPopover`
- [ ] Optional `Query.auth.me` ping after login when gateway exposes it
- [ ] Two-factor path surfaces toast pointing to web `/login`
