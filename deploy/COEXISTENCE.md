# Django DocsAI + Next Admin coexistence

## Dedicated admin EC2 (current production)

| Service | Port | Hostname | Host |
| ------- | ---- | -------- | ---- |
| **Next admin** | 3000 | `https://admin.contact360.io/` | `18.207.217.168` |
| **API gateway** | — | `https://api.contact360.io/graphql` | separate EC2 |

Nginx: [`ec2-nginx-admin.conf`](./ec2-nginx-admin.conf) → `127.0.0.1:3000`. See [EC2-ADMIN-HOST.md](./EC2-ADMIN-HOST.md).

## Same-host layout (legacy / migration)

During full parity migration, both apps may run on one EC2:

| Service | Port | Hostname / path | PM2 / systemd |
| ------- | ---- | --------------- | ------------- |
| **Next admin** | 3001 | `https://admin.contact360.io/` (if shared with dashboard) | `contact360-admin` |
| **User dashboard** | 3000 | `app.contact360.io` | `contact360-dashboard` |
| **Django DocsAI** | 8000 | `https://docs-admin.contact360.io/` or `/legacy/` proxy | `gunicorn` / `docsai` |
| **API gateway** | 8001 | `https://api.contact360.io/graphql` | separate |

## Recommended nginx layout

1. **Dedicated host:** `admin.contact360.io` → `127.0.0.1:3000` (default in `ec2-nginx-admin.conf`).
2. **Shared host:** change `proxy_pass` to `127.0.0.1:3001` for admin if dashboard uses 3000.
3. **Legacy Django** (until parity matrix complete):
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
