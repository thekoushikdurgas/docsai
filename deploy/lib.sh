#!/bin/bash
# shellcheck shell=bash
###############################################################################
# Shared helpers for Contact360 admin EC2 deploy scripts.
###############################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

deploy_resolve_app_dir() {
  local lib_dir
  lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  APP_DIR="$(cd "$lib_dir/.." && pwd)"
  export APP_DIR
}

PM2_APP_NAME_DEFAULT="${PM2_APP_NAME:-contact360-admin}"

load_production_env() {
  PM2_APP_NAME="${PM2_APP_NAME:-$PM2_APP_NAME_DEFAULT}"
  export PORT="${PORT:-3000}"
  if [ -f "$APP_DIR/.env.production" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$APP_DIR/.env.production" 2>/dev/null || true
    set +a
  fi
  PM2_APP_NAME="${PM2_APP_NAME:-$PM2_APP_NAME_DEFAULT}"
  export PM2_APP_NAME
  export PORT
}

ensure_logs_dir() {
  mkdir -p "$APP_DIR/logs"
}

require_command() {
  local cmd="$1"
  local hint="$2"
  if ! command -v "$cmd" &>/dev/null; then
    print_error "Required command not found: $cmd"
    [ -n "$hint" ] && print_error "$hint"
    return 1
  fi
}

require_ecosystem_or_fail() {
  if [ ! -f "$APP_DIR/ecosystem.config.js" ]; then
    print_error "ecosystem.config.js not found in $APP_DIR"
    return 1
  fi
}

optional_api_health_check() {
  load_production_env
  local base="${API_HEALTH_URL:-}"
  if [ -z "$base" ] && [ -n "${NEXT_PUBLIC_API_URL:-}" ]; then
    base="${NEXT_PUBLIC_API_URL%/}/health"
  fi
  if [ -z "$base" ]; then
    print_warning "Skipping API health check (set API_HEALTH_URL or NEXT_PUBLIC_API_URL in .env.production)."
    return 0
  fi
  print_step "Checking API health: $base"
  if curl -sfS --max-time 15 "$base" >/dev/null; then
    print_status "API health check OK."
  else
    print_warning "API health check failed or unreachable (deploy continues)."
  fi
}

free_admin_port() {
  local port="${PORT:-3000}"
  if command -v fuser >/dev/null 2>&1; then
    sudo fuser -k "${port}/tcp" >/dev/null 2>&1 || true
  elif command -v lsof >/dev/null 2>&1; then
    for p in $(sudo lsof -t -iTCP:"${port}" -sTCP:LISTEN 2>/dev/null || true); do
      [ -n "${p:-}" ] || continue
      sudo kill -TERM "$p" 2>/dev/null || true
    done
    sleep 2
    for p in $(sudo lsof -t -iTCP:"${port}" -sTCP:LISTEN 2>/dev/null || true); do
      [ -n "${p:-}" ] || continue
      sudo kill -KILL "$p" 2>/dev/null || true
    done
  fi
}
