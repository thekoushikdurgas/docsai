# Era 10 — Testing

**Goal:** Jest + CI hook.

**Checklist**

- [x] `tests/chunk-idempotency.jest.test.js`
- [x] `tests/scaffold.jest.test.js` — side panel files, no `default_popup`, `linkedin.com/search` content match
- [x] `.github/workflows/extension-ci.yml` (monorepo root)

### Rewrite checklist (v2.0)

- [ ] Vitest + Testing Library — `tests/unit/*.test.ts`, `tests/smoke/scaffold.test.ts`, `Button.test.tsx`
- [ ] Remove legacy Jest-only files (`*.jest.test.js`, `hybridFlow.test.js`, standalone `profileMerger.test.js`)
- [ ] Playwright scaffold under `e2e/` (requires `C360_EXTENSION_DIST`)
- [ ] CI runs `typecheck`, `npm test`, `npm run build`, uploads `dist` artifact
