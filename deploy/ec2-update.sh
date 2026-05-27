#!/bin/bash
###############################################################################
# EC2 — update existing Contact360 admin (git pull, build, PM2 reload).
###############################################################################

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

deploy_resolve_app_dir
cd "$APP_DIR"

echo "=========================================="
echo "Contact360 Admin Application Update"
echo "=========================================="
echo ""

load_production_env

if [ ! -f ".env.production" ]; then
  print_warning ".env.production not found — using defaults."
fi

require_ecosystem_or_fail || exit 1

if ! pm2 list 2>/dev/null | grep -q "$PM2_APP_NAME"; then
  print_error "PM2 app '$PM2_APP_NAME' not found. Run bash deploy/ec2-deploy.sh first."
  exit 1
fi

BACKUP_DIR=".next.backup.$(date +%Y%m%d_%H%M%S)"
BACKUP_SUCCESS=false
if [ -d ".next" ]; then
  print_status "Backing up .next → $BACKUP_DIR"
  if cp -r .next "$BACKUP_DIR" 2>/dev/null; then
    BACKUP_SUCCESS=true
  else
    print_warning "Backup failed — continuing."
  fi
fi

print_status "Git pull..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
git pull origin "$CURRENT_BRANCH" 2>/dev/null || git pull origin main 2>/dev/null || {
  print_warning "git pull failed — building current tree."
}

print_status "npm install..."
npm install --legacy-peer-deps || exit 1

print_status "npm run build..."
BUILD_OK=false
if npm run build && [ -d ".next" ]; then
  BUILD_OK=true
fi

if [ "$BUILD_OK" != true ]; then
  print_error "Build failed."
  if [ "$BACKUP_SUCCESS" = true ] && [ -d "$BACKUP_DIR" ]; then
    rm -rf .next && mv "$BACKUP_DIR" .next && print_warning "Restored previous .next"
  fi
  exit 1
fi

ensure_logs_dir

print_status "PM2 reload..."
if pm2 reload ecosystem.config.js --env production 2>/dev/null; then
  print_status "Reload OK."
else
  pm2 restart "$PM2_APP_NAME"
fi

sleep 3
optional_api_health_check || true

pm2 save
pm2 list
print_status "Update complete."
