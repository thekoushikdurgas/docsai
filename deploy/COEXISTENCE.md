# Django DocsAI + Next Admin coexistence

During full parity migration, both apps run on the same EC2 host:

| Service | Port | Hostname / path | PM2 / systemd |
| ------- | ---- | --------------- | ------------- |
| **Next admin** | 3001 | `https://admin.contact360.io/` (primary) | `contact360-admin` |
| **Django DocsAI** | 8000 | `https://docs-admin.contact360.io/` or `/legacy/` proxy | `gunicorn` / `docsai` |
| **API gateway** | 8001 | `https://api.contact360.io/graphql` | separate |

## Recommended nginx layout

1. **`admin.contact360.io`** → `127.0.0.1:3001` (Next) — see [`ec2-nginx-admin.conf`](./ec2-nginx-admin.conf).
2. **Legacy Django** (until parity matrix complete):
   - **Option A:** Separate server block `docs-admin.contact360.io` → `127.0.0.1:8000`
   - **Option B:** On admin host, `location /legacy/ { proxy_pass http://127.0.0.1:8000/; }` (strip prefix in Django `FORCE_SCRIPT_NAME` if needed)

Commented examples for Option B are in `ec2-nginx-admin.conf`.

## Environment (Next)

| Variable | Purpose |
| -------- | ------- |
| `NEXT_PUBLIC_LEGACY_DOCSAI_URL` | Base URL for “Open legacy DocsAI” link (e.g. `https://docs-admin.contact360.io`) |
| `DOCSAI_INTERNAL_URL` | Server-side BFF target (e.g. `http://127.0.0.1:8000`) — not exposed to browser |

## Sessions

Short term: operators may have separate Django session and Next JWT. Both use gateway login for GraphQL. Long term: single Next console + BFF only.

## Decommission

When `docs/frontend/pages/admin-parity-matrix.json` shows no `missing` / `proxy` rows for production paths, remove Django proxy and archive deploy for `contact360.io/1`. See [`docs/runbooks/decommission-django-docsai.md`](../../../docs/runbooks/decommission-django-docsai.md).
