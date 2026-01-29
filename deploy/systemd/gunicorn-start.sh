#!/bin/bash
# Wrapper script for Gunicorn to ensure proper environment setup
# This script is called by systemd service

set -e

PROJECT_DIR="/home/ubuntu/docsai"
cd "$PROJECT_DIR"

# Activate virtual environment
source venv/bin/activate

# Set environment
export DJANGO_ENV=production
export PYTHONPATH="$PROJECT_DIR"
export PATH="$PROJECT_DIR/venv/bin:$PATH"

# Calculate workers: CPU_COUNT * 2 + 1
WORKERS=$(( $(nproc) * 2 + 1 ))

# Start Gunicorn with all options as command-line arguments
# Note: Not using --pid to avoid permission issues - systemd manages the process
exec gunicorn \
  --workers "$WORKERS" \
  --worker-class sync \
  --timeout 30 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --access-logfile /var/log/django/gunicorn-access.log \
  --error-logfile /var/log/django/gunicorn-error.log \
  --log-level info \
  --bind unix:/run/gunicorn.sock \
  --preload \
  --name docsai-production \
  config.wsgi:application
