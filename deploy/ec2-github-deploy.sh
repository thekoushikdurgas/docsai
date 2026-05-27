#!/usr/bin/env bash
###############################################################################
# Non-interactive deploy for GitHub Actions → EC2 (PM2 + npm, port 3001).
###############################################################################

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

export CI=1
export HUSKY=0

run_docker() {
  if command -v docker >/dev/null 2>&1; then
    docker "$@"
  elif [ -x /usr/bin/docker ]; then
    /usr/bin/docker "$@"
  elif sudo test -x /usr/bin/docker 2>/dev/null; then
    sudo /usr/bin/docker "$@"
  else
    return 0
  fi
}

deploy_resolve_app_dir
cd "$APP_DIR" || exit 1

echo "=========================================="
echo "Contact360 admin — GitHub/PM2 deploy"
echo "APP_DIR=$APP_DIR"
echo "=========================================="

load_production_env

if [ -f "$APP_DIR/docker-compose.prod.yml" ]; then
  print_step "Stopping Docker Compose stack (if any)…"
  run_docker compose -f "$APP_DIR/docker-compose.prod.yml" down --remove-orphans 2>/dev/null || true
fi

free_admin_port
sleep 1

print_step "Fix ownership of app directory"
if ! sudo chown -R "$(id -un):$(id -gn)" "$APP_DIR"; then
  print_error "sudo chown failed."
  exit 1
fi

print_step "Preflight (Node, npm, PM2, ecosystem)"
require_command node "Install Node and run app or admin deploy/ec2-setup.sh once."
require_command npm
require_command pm2 "npm i -g pm2 && pm2 startup"
require_ecosystem_or_fail || exit 1

if [ ! -f "$APP_DIR/.env.production" ]; then
  print_warning ".env.production not found — ensure CI writes it or copy .env.production.example."
fi

load_production_env
ensure_logs_dir

print_step "npm ci (legacy peer deps)"
if ! npm ci --ignore-scripts --legacy-peer-deps; then
  print_error "npm ci failed."
  exit 1
fi

print_step "Clean + next build"
rm -rf "$APP_DIR/.next"
if ! npm run build; then
  print_error "next build failed."
  exit 1
fi

print_step "PM2 start/restart ($PM2_APP_NAME)"
if pm2 list 2>/dev/null | grep -q "$PM2_APP_NAME"; then
  pm2 stop "$PM2_APP_NAME" || true
  pm2 delete "$PM2_APP_NAME" || true
fi
if ! pm2 start ecosystem.config.js --env production; then
  print_error "pm2 start failed."
  exit 1
fi
sleep 2
if ! pm2 list 2>/dev/null | grep "$PM2_APP_NAME" | grep -q online; then
  pm2 logs "$PM2_APP_NAME" --lines 25 --nostream || true
  exit 1
fi
pm2 save || true

optional_api_health_check || true

print_status "Deploy finished. curl: curl -sf http://127.0.0.1:${PORT:-3001}/login"
