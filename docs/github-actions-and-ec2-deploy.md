# GitHub Actions and EC2 deployment

This document ties together [`.github/workflows/`](../.github/workflows/) (when this admin app is the **standalone** repository root), the **Contact360 monorepo** workflows at the repository root (see [Monorepo vs standalone](#monorepo-vs-standalone)), shell scripts under [`deploy/`](../deploy/), and the production stack (Nginx, Gunicorn, systemd) described in [DEPLOYMENT_ARCHITECTURE.md](../deploy/DEPLOYMENT_ARCHITECTURE.md).

## Monorepo vs standalone

| Layout | Where `manage.py` lives | CI / deploy workflows that GitHub executes |
|--------|-------------------------|---------------------------------------------|
| **Standalone** admin repo (e.g. DocsAI-only clone) | Repository root: `manage.py` next to `apps/` | [`contact360.io/admin/.github/workflows/django-ci.yml`](../.github/workflows/django-ci.yml) and [`deploy.yml`](../.github/workflows/deploy.yml) |
| **Contact360 monorepo** | `contact360.io/admin/manage.py` | Root workflows [`.github/workflows/admin-ci.yml`](../../../.github/workflows/admin-ci.yml) and [`.github/workflows/admin-deploy-ec2.yml`](../../../.github/workflows/admin-deploy-ec2.yml) (paths filtered to `contact360.io/admin/**`) |

GitHub only loads workflow files from **`.github/workflows` at the default branch root**. Workflows under `contact360.io/admin/.github/` are **not** used when the remote is the full monorepo; in that case use the root `admin-*.yml` workflows.

### `deploy.yml` path filters (standalone)

When the standalone repo is used, pushes to `main` trigger deploy only if changed files match:

- `contact360.io/admin/**` (harmless if absent in standalone)
- `apps/**`, `config/**`, `requirements.txt`, `manage.py`, `deploy/**`, `.github/workflows/deploy.yml`

In the **monorepo**, the root [admin-deploy-ec2.yml](../../../.github/workflows/admin-deploy-ec2.yml) filters on `contact360.io/admin/**` and the workflow file itself.

### GitHub configuration (deploy)

| Item | Purpose |
|------|---------|
| Secrets `EC2_SSH_PRIVATE_KEY`, `EC2_HOST`, `EC2_USER` | SSH from Actions to the server |
| Variable `EC2_PROJECT_DIR` (optional) | Absolute path on EC2 to the directory that contains **`deploy/remote-deploy.sh`** and **`manage.py`** |

**Monorepo EC2 clone:** set `EC2_PROJECT_DIR` to the admin path inside the clone, for example `/home/ubuntu/contact360/contact360.io/admin`, not the monorepo root (unless `deploy/` lives there).

**Standalone EC2 clone:** default `/home/ubuntu/docsai` in the workflow matches [QUICK_START.md](../deploy/QUICK_START.md).

## CI: what runs

- Resolve project directory (standalone: only `django-ci.yml` resolves `.` vs `contact360.io/admin`; monorepo root workflow uses `working-directory: contact360.io/admin`).
- Python **3.11** (match your EC2 image / venv; if the server uses another minor version, align or document the difference).
- `pip install -r requirements.txt`
- `DJANGO_ENV=production` … `python manage.py check --deploy`
- `pytest apps/core/tests apps/admin_ops/tests` (smoke + admin operator views).

Optional hardening: add a linter (for example Ruff) to `requirements-dev.txt` and a CI step when the team agrees.

## CD: routine path (GitHub Actions)

1. Merge to **`main`** (or run **Actions → Deploy Admin to EC2 → Run workflow** with a branch input).
2. Job SSHs to EC2, `cd $EC2_PROJECT_DIR`, verifies `.git` exists, then `git fetch` and `git reset --hard origin/<branch>`.
3. Runs **`bash deploy/remote-deploy.sh`** ([remote-deploy.sh](../deploy/remote-deploy.sh)): venv, `pip install`, `migrate`, `collectstatic`, **`systemctl restart`** on a discovered unit (`gunicorn`, `docsai`, …) or `RESTART_SERVICE`.
4. Verify: `curl -sf http://127.0.0.1/api/v1/health/` from the server (avoids `ALLOWED_HOSTS` issues with the public IP).

## CD: manual fallback (SSH)

```bash
cd "$EC2_PROJECT_DIR"   # e.g. …/contact360.io/admin
git fetch origin && git reset --hard origin/main
bash deploy/remote-deploy.sh
```

If the Gunicorn unit name is not in the default list:

```bash
export RESTART_SERVICE=your-unit.service
bash deploy/remote-deploy.sh
```

## One-time EC2 bootstrap

For a **new** server or path:

1. **Git clone** (monorepo or standalone) so the target directory is a real git work tree (deploy job errors out if `.git` is missing).
2. Place **`.env.prod`** (and dependencies: DB, gateway URL, keys) per [DEPLOYMENT_ARCHITECTURE.md](../deploy/DEPLOYMENT_ARCHITECTURE.md).
3. Run **`sudo bash deploy/deploy-to-ec2.sh`** (or `full-deploy.sh`) once to install system packages, Nginx, systemd socket/service under [`deploy/systemd/`](../deploy/systemd/), optional SSL.
4. Ensure the **systemd unit name** matches what [`remote-deploy.sh`](../deploy/remote-deploy.sh) can restart, or use **`RESTART_SERVICE`**.
5. Confirm health: `curl http://127.0.0.1/api/v1/health/` on the instance.

Use [`pre-deployment-check.sh`](../deploy/pre-deployment-check.sh) before a big change and [`post-deployment-verify.sh`](../deploy/post-deployment-verify.sh) after.

## Canonical vs legacy scripts

| Script | Role |
|--------|------|
| [**deploy/remote-deploy.sh**](../deploy/remote-deploy.sh) | **Canonical** post-push deploy (used by Actions). |
| [**deploy/deploy-to-ec2.sh**](../deploy/deploy-to-ec2.sh) / **full-deploy.sh** | First-time or full reinstall (`sudo`). |
| **deploy/deploy.sh** | Legacy; hardcodes `/var/www/docsai` — use **deploy-to-ec2** + **remote-deploy** instead unless you rewrite paths. |
| **deploy/deploy-admin.sh** | Legacy Contact360 script (`docs` branch, system pip, supervisor) — prefer **remote-deploy.sh** in a **venv**. |
| **deploy/gunicorn.service** | Simple **127.0.0.1:8000** template; production uses **socket** + **[deploy/systemd/gunicorn.service](deploy/systemd/gunicorn.service)** and **[gunicorn-start.sh](deploy/systemd/gunicorn-start.sh)** with **`docsai.wsgi:application`**. |

## Incident response

See [TROUBLESHOOTING.md](../deploy/TROUBLESHOOTING.md) and [troubleshoot-gunicorn.sh](../deploy/troubleshoot-gunicorn.sh) for sockets, `ALLOWED_HOSTS`, and nginx upstream mismatches.
