#!/bin/bash
# ------------------------------------------------------------------------------
# Remote deploy — run on EC2 after: git fetch && git reset --hard origin/<branch>
# GitHub Actions: ssh … "cd … && bash deploy/remote-deploy.sh"
#
# Resolves app root from this script (deploy/..), so it matches any clone path
# (do not rely on a hardcoded /home/ubuntu/docsai when PROJECT_DIR is not exported).
# ------------------------------------------------------------------------------
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"
export PROJECT_DIR

if [ ! -f "manage.py" ]; then
  echo "Error: manage.py not found in $PROJECT_DIR (wrong directory or incomplete clone)."
  exit 1
fi

if [ ! -d "venv" ]; then
  echo ">>> No venv/ — creating virtualenv (python3 -m venv venv)..."
  python3 -m venv venv || {
    echo "Error: python3 -m venv failed. On Ubuntu: sudo apt-get update && sudo apt-get install -y python3-venv"
    exit 1
  }
fi

echo ">>> Activating venv and installing dependencies..."
# shellcheck disable=SC1091
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ">>> Running migrations..."
python manage.py migrate --noinput

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput

echo ">>> Restarting application server (systemd)..."
# Many installs use different unit names; missing unit must not fail the deploy after migrate/static.
restart_ok=0
found_loaded_unit=0
unit_loaded() {
  local u="$1"
  local state
  state="$(systemctl show -p LoadState --value "${u}.service" 2>/dev/null || true)"
  [ "$state" = "loaded" ]
}

if [ -n "${RESTART_SERVICE:-}" ]; then
  if sudo systemctl restart "$RESTART_SERVICE"; then
    echo ">>> Restarted $RESTART_SERVICE"
    restart_ok=1
  else
    echo "::warning::systemctl restart $RESTART_SERVICE failed."
    sudo systemctl status "$RESTART_SERVICE" --no-pager -l || true
  fi
else
  for unit in gunicorn docsai gunicorn-docsai docsai-gunicorn; do
    if unit_loaded "$unit"; then
      found_loaded_unit=1
      if sudo systemctl restart "${unit}.service"; then
        echo ">>> Restarted ${unit}.service"
        restart_ok=1
        break
      else
        echo "::warning::systemctl restart ${unit}.service failed (unit is loaded)."
        sudo systemctl status "${unit}.service" --no-pager -l || true
        break
      fi
    fi
  done
fi
if [ "$restart_ok" -ne 1 ]; then
  if [ -n "${RESTART_SERVICE:-}" ]; then
    echo "::warning::RESTART_SERVICE=$RESTART_SERVICE did not restart successfully (see status above)."
  elif [ "$found_loaded_unit" -eq 1 ]; then
    echo "::warning::Gunicorn unit is present but restart failed; fix systemd/gunicorn on the server."
  else
    echo "::warning::No loaded systemd unit among gunicorn, docsai, gunicorn-docsai, docsai-gunicorn."
    echo "Install a unit from deploy/systemd/gunicorn.service or deploy/gunicorn.service, then: sudo systemctl daemon-reload && sudo systemctl enable --now gunicorn"
    echo "Override: RESTART_SERVICE=myapp.service bash deploy/remote-deploy.sh"
  fi
  echo "Migrations and static files are already applied."
fi

echo ">>> Done. Verify: curl -s http://127.0.0.1/api/v1/health/ (or your public EC2 URL)"
