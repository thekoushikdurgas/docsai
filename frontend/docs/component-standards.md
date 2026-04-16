# Component standards (contact360.io/app)

## Stack

- **Next.js 16** App Router, **React 19**, TypeScript.
- **Styling:** Custom CSS layers (`app/globals.css` → `app/css/*`), **no Tailwind**. Prefer `c360-*` classes and `--c360-*` CSS variables defined in `app/css/core.css` (aligned with `docs/frontend/ideas/Dashboard ui kit`).

## Primitives

- **Buttons / inputs:** `src/components/ui/` — `Button`, `Input`, `Checkbox`, `Radio`, `Modal`, `Tabs`, `Progress`.
- **Feedback:** **Sonner** toasts for API outcomes; see `contact360.io/app/docs/DIALOG-PATTERNS.md` for SweetAlert scope.

## Data

- **GraphQL:** `graphql-request` via `src/lib/graphqlClient.ts`; feature services under `src/services/graphql/`.

## Django admin (`contact360.io/admin`)

- **Stack:** Django templates + WhiteNoise static; **no React**.
- **Tokens / CSS:** See [admin-ui-tokens.md](admin-ui-tokens.md) and `contact360.io/admin/static/admin/css/design-tokens.css`.
- **Feedback:** Django messages + template alerts (`components/alert.html`).

## References

- Inventory: `npm run css:inventory` in `contact360.io/app`.
- Deeper CSS guide: `contact360.io/app/docs/CSS.md` (if present).
