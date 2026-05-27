# Runbook: Decommission Django DocsAI (`contact360.io/1`)

**Prerequisite:** `docs/frontend/pages/admin-parity-matrix.json` has zero production routes with `parity_status` of `missing` or `proxy`.

## Checklist

1. Confirm Next admin serves all operator paths on `admin.contact360.io` (PM2 `contact360-admin`, port **3000** on EC2 `18.207.217.168`).
2. Remove nginx `location /legacy/` or `docs-admin.contact360.io` proxy to Django :8000.
3. Disable GitHub workflow deploy for `contact360.io/1/**` or restrict to archival branch.
4. Export/migrate any Django-only databases (Durgasflow ORM, page_builder specs) to gateway-backed storage.
5. Update [`docs/codebases/admin.md`](../codebases/admin.md) — remove legacy sections.
6. Archive `contact360.io/1` in repo (README banner: archived, use `contact360.io/admin`).

## Rollback

Restore nginx proxy to Django and redeploy from `contact360.io/1` using `deploy/remote-deploy.sh`.
