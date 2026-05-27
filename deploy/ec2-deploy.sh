#!/bin/bash
###############################################################################
# EC2 — deploy Contact360 Admin (PM2 + build). Port 3000.
#
# Run as app user from admin root:
#   bash deploy/ec2-deploy.sh
###############################################################################

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

deploy_resolve_app_dir
cd "$APP_DIR"

echo "=========================================="
echo "Contact360 Admin Application Deployment"
echo "=========================================="
echo ""

step_01_preflight() {
  print_step "01 — Preflight (Node, PM2, package.json, ecosystem)"
  require_command node "Run deploy/ec2-setup.sh on the server first (once per host)."
  require_command npm
  require_command pm2
  if [ ! -f "$APP_DIR/package.json" ]; then
    print_error "package.json not found — wrong directory?"
    exit 1
  fi
  require_ecosystem_or_fail || exit 1
  print_status "Preflight OK."
}

step_02_env_file() {
  print_step "02 — Environment file (.env.production)"
  if [ ! -f "$APP_DIR/.env.production" ]; then
    print_warning ".env.production not found."
    print_warning "Recommended: cp .env.production.example .env.production && nano .env.production"
    read -r -p "Continue without .env.production? (y/N) " -n 1 reply
    echo ""
    if [[ ! ${reply:-} =~ ^[Yy]$ ]]; then
      print_error "Cancelled. Create .env.production then re-run."
      exit 1
    fi
  else
    print_status ".env.production present."
  fi
  load_production_env
  ensure_logs_dir
}

step_03_npm_install() {
  print_step "03 — Install dependencies (npm install)"
  if ! npm install --legacy-peer-deps; then
    print_error "npm install failed."
    exit 1
  fi
}

step_04_clean_build() {
  print_step "04 — Clean .next and build"
  if ! rm -rf .next 2>/dev/null; then
    print_error "Cannot remove .next. Fix: sudo chown -R \"\$(whoami)\" \"$APP_DIR\" && rm -rf .next"
    exit 1
  fi
  if ! npm run build; then
    print_error "next build failed."
    exit 1
  fi
  if [ ! -d ".next" ]; then
    print_error ".next missing after build."
    exit 1
  fi
  print_status "Build OK."
}

step_05_pm2() {
  print_step "05 — PM2 start/restart ($PM2_APP_NAME)"
  if pm2 list 2>/dev/null | grep -q "$PM2_APP_NAME"; then
    print_warning "Stopping existing $PM2_APP_NAME..."
    pm2 stop "$PM2_APP_NAME" || true
    pm2 delete "$PM2_APP_NAME" || true
  fi
  if ! pm2 start ecosystem.config.js --env production; then
    print_error "pm2 start failed."
    exit 1
  fi
  sleep 2
  if ! pm2 list 2>/dev/null | grep "$PM2_APP_NAME" | grep -q online; then
    print_warning "Process may not be online. Recent logs:"
    pm2 logs "$PM2_APP_NAME" --lines 25 --nostream || true
    exit 1
  fi
  pm2 save
  print_status "PM2 OK."
}

step_06_optional_checks() {
  print_step "06 — Optional API health check"
  optional_api_health_check || true
}

step_07_summary() {
  print_status "=========================================="
  print_status "Admin deployment finished."
  print_status "=========================================="
  pm2 list
  print_status "Logs: pm2 logs $PM2_APP_NAME"
  print_status "Local: curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:${PORT:-3000}/login || true"
  print_status "Nginx: install deploy/ec2-nginx-admin.conf for admin.contact360.io"
}

step_01_preflight
step_02_env_file
step_03_npm_install
step_04_clean_build
step_05_pm2
step_06_optional_checks
step_07_summary
