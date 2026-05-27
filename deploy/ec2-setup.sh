#!/bin/bash
###############################################################################
# EC2 initial server setup — Ubuntu for Contact360 Admin (Next.js, port 3000).
#
# One run per host is enough (same Node/PM2/nginx as the dashboard app).
#   sudo ./deploy/ec2-setup.sh
#
# After setup, clone admin to e.g. /home/ubuntu/contact360-admin, then:
#   cp .env.production.example .env.production
#   bash deploy/ec2-deploy.sh
###############################################################################

set -e

echo "=========================================="
echo "Contact360 Admin EC2 Server Setup"
echo "=========================================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ "$EUID" -ne 0 ]; then
  print_error "Run as root or with sudo."
  exit 1
fi

print_status "Updating system packages..."
apt update && apt upgrade -y

print_status "Installing packages: git, build-essential, ufw, nginx, curl..."
apt install -y git build-essential ufw nginx curl

print_status "Configuring UFW (SSH + Nginx)..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

print_status "Installing Node.js 20.x LTS (NodeSource)..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

command -v node &>/dev/null || { print_error "Node.js failed."; exit 1; }
command -v npm &>/dev/null || { print_error "npm failed."; exit 1; }
print_status "Node $(node -v) | npm $(npm -v)"

print_status "Installing PM2 globally..."
npm install -g pm2
command -v pm2 &>/dev/null || { print_error "PM2 failed."; exit 1; }

print_status "PM2 startup (systemd for ubuntu user)..."
pm2 startup systemd -u ubuntu --hp /home/ubuntu 2>/dev/null | tail -5 || print_warning "Run the printed sudo command manually if needed."

ADMIN_DIR="/home/ubuntu/contact360-admin"
mkdir -p "$ADMIN_DIR/logs"
chown -R ubuntu:ubuntu "$ADMIN_DIR" 2>/dev/null || true

print_status "=========================================="
print_status "Server setup completed."
print_status "Default admin directory: $ADMIN_DIR"
print_status "Next: clone contact360.io/admin, cp .env.production.example, bash deploy/ec2-deploy.sh"
print_status "Nginx: deploy/ec2-nginx-admin.conf → /etc/nginx/sites-available/admin"
print_status "=========================================="
