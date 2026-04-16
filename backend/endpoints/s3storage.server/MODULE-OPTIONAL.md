# s3storage.server — Go module path vs Git remote

- **Module path (go.mod):** `contact360.io/s3storage` — see [`EC2/s3storage.server/go.mod`](../../../../EC2/s3storage.server/go.mod).
- **Common Git remote name in docs:** `https://github.com/thekoushikdurgas/storage.server.git` (repository name `storage.server`).

Renaming the module to match the GitHub path is a **separate migration** (import path updates across internal packages). Until then, treat the module path as the canonical import root for code in this monorepo.

Last updated: 2026-04-15.
