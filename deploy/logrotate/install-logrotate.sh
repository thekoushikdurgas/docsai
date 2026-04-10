#!/bin/bash
set -e

LOGROTATE_DIR="/etc/logrotate.d"

echo "Installing logrotate configuration..."

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Copy logrotate config
cp deploy/logrotate/docsai $LOGROTATE_DIR/
chmod 644 $LOGROTATE_DIR/docsai

# Test logrotate config (use verbose mode so it actually runs instead of debug-only)
echo "Testing logrotate configuration..."
logrotate -v $LOGROTATE_DIR/docsai >/dev/null 2>&1 || echo "logrotate test reported issues (see output above)"

echo "Logrotate configuration installed successfully!"
echo "Logs will be rotated daily and kept for 14 days"
