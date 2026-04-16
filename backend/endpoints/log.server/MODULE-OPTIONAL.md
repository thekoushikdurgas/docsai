# log.server — Go module path vs Git remote

- **Module path (go.mod):** `contact360.io/logsapi`
- **Typical Git remote:** `https://github.com/thekoushikdurgas/contactlogs.git`

Renaming the module to match the GitHub repo name is a **separate migration** (import path updates). Until then, use `contact360.io/logsapi` as the canonical import root.

Last updated: 2026-04-15.
