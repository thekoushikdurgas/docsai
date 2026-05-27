# Adding a feature to Contact360 Admin (Next.js)

1. **Route** — Add to `src/lib/routes.ts` and create `app/(dashboard)/…/page.tsx` (or `app/(auth)/` for public).
2. **GraphQL** — Add operations in `src/graphql/adminOperations.ts` (or domain `*Operations.ts`); run `npm run codegen` when schema changes.
3. **Service** — `src/services/*Service.ts` wrapping `graphqlQuery` / `graphqlMutation`.
4. **Hook** — `src/hooks/useAdmin*.ts` using `useAdminResource` where appropriate.
5. **UI** — Feature client under `src/components/feature/<area>/`; prefer `AdminListPage` / `AdminPageLayout`.
6. **Nav** — `src/lib/navConfig.ts` + command palette index (`ADMIN_NAV_SEARCH_INDEX`).
7. **Auth** — Gate with `useAuth().isSuperAdmin` / `isAdmin`; match Django `@require_super_admin` where applicable.
8. **Parity** — Update matrix: `node scripts/generate-parity-matrix.mjs` and map row in `NEXT_ROUTE_MAP` inside the script.
9. **CI** — `npm run ci` before PR.

## Legacy Django parity

If the feature exists in `contact360.io/1`, link the Django url name in the PR and set parity status in `docs/frontend/pages/admin-parity-matrix.json`.
