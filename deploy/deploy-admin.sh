#!/usr/bin/env bash
#
# DEPRECATED — legacy operator script (global pip, fixed branch "docs",
# gunicorn-docsai / supervisor, health on :8000). Prefer venv + deploy/remote-deploy.sh
# (same path GitHub Actions uses). See docs/github-actions-and-ec2-deploy.md.
#
# Contact360 DocsAI Admin — Deployment script
# Usage: bash deploy/deploy-admin.sh
# Target: 34.201.10.84 / admin.contact360.io
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRANCH="${DEPLOY_BRANCH:-docs}"

echo "=== Contact360 DocsAI Admin Deployment ==="
echo "Directory: $REPO_DIR"
echo "Branch: $BRANCH"

# 1. Pull latest code
echo "[1/6] Pulling latest code from origin/$BRANCH..."
cd "$REPO_DIR"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# 2. Install/update Python dependencies
echo "[2/6] Installing Python dependencies..."
pip install -r requirements.txt --quiet

# 3. Run database migrations
echo "[3/6] Running database migrations..."
python manage.py migrate --noinput

# 4. Collect static files
echo "[4/6] Collecting static files..."
python manage.py collectstatic --noinput

# 5. Restart Gunicorn service (systemd)
echo "[5/6] Restarting Gunicorn..."
if systemctl is-active --quiet gunicorn-docsai; then
    systemctl restart gunicorn-docsai
    echo "Gunicorn restarted."
elif [ -f /etc/supervisor/conf.d/docsai.conf ]; then
    supervisorctl restart docsai
    echo "Supervisor process restarted."
else
    echo "Warning: Could not find gunicorn-docsai systemd service or supervisor config."
    echo "Restart your WSGI server manually."
fi

# 6. Health check
echo "[6/6] Health check..."
sleep 2
curl -sf http://localhost:8000/api/v1/health/ && echo " — Health check OK" || echo " — Health check FAILED"

echo "=== Deployment complete ==="
