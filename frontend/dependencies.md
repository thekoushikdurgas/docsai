# contact360.io/app — key dependencies

| Package | Role |
|--------|------|
| `next` | App Router, standalone output |
| `graphql` / `graphql-request` | GraphQL client |
| `@tanstack/react-virtual` | Long list virtualization |
| `recharts` | Dashboard / analytics charts |
| `@fullcalendar/*` | Calendar views |
| `@tiptap/*` | Rich text where used |
| `lucide-react` | Icons |
| `sonner` | Toasts |
| `framer-motion` | Motion |
| `papaparse` | CSV import |
| `vitest` / `@playwright/test` | Tests |

See `contact360.io/app/package.json` for exact versions.

## Related product / API notes

- Contacts list filters, VQL merge, and `filterData` pagination: [`../docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).
