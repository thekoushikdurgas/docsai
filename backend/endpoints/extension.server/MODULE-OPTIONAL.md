# extension.server — module path vs Git remote

| | Value |
|---|--------|
| **Go module path** | `contact360.io/extension` (see [`go.mod`](../../../../EC2/extension.server/go.mod)) |
| **Git remote** | `https://github.com/thekoushikdurgas/extension.server.git` |

The module path is a vanity import path; it does not need to match the GitHub org name. Clone from **`extension.server.git`**, not `contactlogs.git` (that remote is used by **log.server**).

Last updated: 2026-04-15.
