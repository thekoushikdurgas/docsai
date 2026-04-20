# Era 0 — Foundation

**Goal:** Repo path, HTTPS defaults, README.

**Checklist**

- [x] `docs/frontend/index.json` → `contact360.extension`, git/deploy
- [x] `manifest.json` → `https://api.contact360.io/*`, `https://logs.api.contact360.io/*`
- [x] `utils/constants.js` → `GRAPHQL_CONFIG.graphqlUrl` HTTPS
- [x] `contact360.extension/README.md`

**Refs:** `docs/backend/endpoints/extension.server/ROUTES.md`

**Note:** Harvest defaults to **`https://api.contact360.io/graphql`** (no satellite base URL in the extension UI for save/scrape).

### Rewrite checklist (v2.0 — Vite + React + CRXJS)

- [ ] `package.json` + `vite.config.ts` + `tsconfig.json` — `npm run build` → `dist/`
- [ ] Root `manifest.json` includes `<all_urls>` content scripts + `c360_optin_hosts` documented in README
- [ ] `contact360.extension/README.md` describes React/Vite layout and load-unpacked from `dist/`
