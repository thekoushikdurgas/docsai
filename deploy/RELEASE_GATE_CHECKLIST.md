# Release gate checklist (Era 7.x)

Use before promoting any Contact360 minor across surfaces.

1. **P0 verification** — [docs/codebases/P0_BLOCKERS_VERIFICATION.md](../codebases/P0_BLOCKERS_VERIFICATION.md) still true for the branch.
2. **Health** — Hit `/health` on gateway (`contact360.io/api`) and impacted Go satellites ([EC2_SATELLITE_HEALTH.md](../codebases/EC2_SATELLITE_HEALTH.md)).
3. **Secrets** — No new literals in repo; `.env` / CI secrets aligned with [SECURITY.md](../../SECURITY.md) if present.
4. **RBAC** — Django admin privileged routes still covered by guard tests; API production `DEBUG`, CORS, `TRUSTED_HOSTS` tightened.
5. **Extension** — Chrome package version bumped; `manifest.json` host_permissions match actual Connectra/API URLs.
6. **Docs sync** — `docs/frontend/pages/`, `docs/backend/endpoints/`, `docs/codebases/*-analysis.md`, and [flowchart.md](../docs/flowchart.md) updated for observable behavior changes.
7. **Audit** — From `docs/`: `python cli.py audit-tasks --era N` for the target era.
