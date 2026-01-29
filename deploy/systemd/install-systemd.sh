#!/bin/bash
set -e

PROJECT_DIR="/home/ubuntu/docsai"
SYSTEMD_DIR="/etc/systemd/system"
SOCKET_PATH="/run/gunicorn.sock"

echo "Installing systemd service files..."

if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run as root or with sudo"
    exit 1
fi

# Validate project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory not found: $PROJECT_DIR"
    echo "Please ensure the project is deployed to the correct location"
    exit 1
fi

# Run from project root (required for deploy/systemd/* paths)
cd "$PROJECT_DIR"

# Validate we're in the right location
if [ ! -f "deploy/systemd/gunicorn.service" ]; then
    echo "ERROR: Cannot find deploy/systemd/gunicorn.service"
    echo "Current directory: $(pwd)"
    echo "Expected location: $PROJECT_DIR"
    echo "Please run from project root where deploy/systemd/ exists"
    exit 1
fi

# Validate required files exist
REQUIRED_FILES=(
    "deploy/systemd/gunicorn.service"
    "deploy/systemd/gunicorn.socket"
    "deploy/systemd/gunicorn-start.sh"
    "deploy/systemd/gunicorn.service.simple"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
done

# Validate wrapper script syntax
if ! bash -n deploy/systemd/gunicorn-start.sh 2>/dev/null; then
    echo "ERROR: gunicorn-start.sh has syntax errors"
    bash -n deploy/systemd/gunicorn-start.sh
    exit 1
fi

# Check if services already exist (for upgrade scenario)
if systemctl list-unit-files | grep -q "^gunicorn.service"; then
    echo "INFO: Existing Gunicorn service detected. This will upgrade the configuration."
    echo "Current service status:"
    systemctl status gunicorn.service --no-pager -l || true
    echo ""
fi

# Ensure /run directory exists (systemd creates it, but verify)
if [ ! -d "/run" ]; then
    echo "WARNING: /run directory does not exist. This is unusual on systemd systems."
fi

# Create log directory for Gunicorn
echo "Setting up log directory..."
mkdir -p /var/log/django
chown ubuntu:www-data /var/log/django
chmod 755 /var/log/django

# Verify log directory permissions
if [ ! -w "/var/log/django" ]; then
    echo "WARNING: Cannot write to /var/log/django. Check permissions."
fi

# Fix .env.prod permissions if it exists (must be readable by ubuntu user)
if [ -f "$PROJECT_DIR/.env.prod" ]; then
    chown ubuntu:ubuntu "$PROJECT_DIR/.env.prod"
    chmod 600 "$PROJECT_DIR/.env.prod"
    echo "Fixed permissions for .env.prod"
else
    echo "WARNING: .env.prod not found at $PROJECT_DIR/.env.prod"
    echo "The service may fail to start without proper environment configuration"
fi

# Verify Gunicorn config can be imported
echo "Verifying Gunicorn configuration..."
cd "$PROJECT_DIR"
if [ -d "venv" ]; then
    source venv/bin/activate
    if python -c "import config.gunicorn.production" 2>/dev/null; then
        echo "Gunicorn configuration verified ✓"
    else
        echo "WARNING: Could not import config.gunicorn.production"
        echo "This may cause the service to fail. Checking Python path..."
        python -c "import sys; print('Python path:', sys.path)" || true
    fi
    deactivate
else
    echo "WARNING: Virtual environment not found. Cannot verify Gunicorn config."
fi

# Copy socket file
echo "Installing socket file..."
cp deploy/systemd/gunicorn.socket $SYSTEMD_DIR/
chmod 644 $SYSTEMD_DIR/gunicorn.socket

# Validate socket file was copied
if [ ! -f "$SYSTEMD_DIR/gunicorn.socket" ]; then
    echo "ERROR: Failed to copy socket file to $SYSTEMD_DIR/"
    exit 1
fi

# Ensure wrapper script exists and has correct permissions
if [ -f "deploy/systemd/gunicorn-start.sh" ]; then
    # Script already exists in deploy/systemd/, just ensure permissions
    chmod +x deploy/systemd/gunicorn-start.sh
    chown ubuntu:ubuntu deploy/systemd/gunicorn-start.sh
    echo "Gunicorn wrapper script verified ✓"
else
    echo "ERROR: gunicorn-start.sh not found at deploy/systemd/gunicorn-start.sh"
    echo "Service will fail without this script"
    exit 1
fi

# Detect if Gunicorn supports systemd notify
# Gunicorn 19.7+ has built-in systemd support via sd_notify
# We'll try Type=notify first, but can fallback to Type=simple if it fails
echo "Detecting Gunicorn systemd notify support..."
USE_NOTIFY=true
if [ -d "$PROJECT_DIR/venv" ]; then
    source venv/bin/activate
    # Check Gunicorn version (19.7+ has systemd support)
    GUNICORN_VERSION=$(python -c "import gunicorn; print(gunicorn.__version__)" 2>/dev/null || echo "0.0.0")
    
    # Simple version comparison (major.minor)
    MAJOR=$(echo "$GUNICORN_VERSION" | cut -d. -f1)
    MINOR=$(echo "$GUNICORN_VERSION" | cut -d. -f2)
    
    # Gunicorn 19.7+ has built-in systemd notify support
    if [ "$MAJOR" -gt 19 ] || ([ "$MAJOR" -eq 19 ] && [ "$MINOR" -ge 7 ]) 2>/dev/null; then
        echo "Gunicorn $GUNICORN_VERSION detected (>=19.7) - systemd notify supported ✓"
        USE_NOTIFY=true
    else
        echo "WARNING: Gunicorn version $GUNICORN_VERSION (<19.7) may not fully support systemd notify"
        echo "Using Type=simple for better compatibility"
        USE_NOTIFY=false
    fi
    deactivate
else
    echo "WARNING: Virtual environment not found, cannot detect systemd notify support"
    echo "Defaulting to Type=simple for compatibility"
    USE_NOTIFY=false
fi

# Copy appropriate service file
echo "Installing service file..."
if [ "$USE_NOTIFY" = true ]; then
    cp deploy/systemd/gunicorn.service $SYSTEMD_DIR/
    echo "Using Type=notify service file ✓"
else
    cp deploy/systemd/gunicorn.service.simple $SYSTEMD_DIR/gunicorn.service
    echo "Using Type=simple service file ✓"
fi
chmod 644 $SYSTEMD_DIR/gunicorn.service

# Validate service file was copied
if [ ! -f "$SYSTEMD_DIR/gunicorn.service" ]; then
    echo "ERROR: Failed to copy service file to $SYSTEMD_DIR/"
    exit 1
fi

# Reload systemd to pick up new/updated service files
echo "Reloading systemd daemon..."
if ! systemctl daemon-reload; then
    echo "ERROR: Failed to reload systemd daemon"
    exit 1
fi

# Stop existing services if running (for upgrade scenario)
if systemctl is-active --quiet gunicorn.service 2>/dev/null; then
    echo "Stopping existing Gunicorn service..."
    systemctl stop gunicorn.service || true
fi
if systemctl is-active --quiet gunicorn.socket 2>/dev/null; then
    echo "Stopping existing Gunicorn socket..."
    systemctl stop gunicorn.socket || true
fi

# Enable socket
echo "Enabling Gunicorn socket..."
if ! systemctl enable gunicorn.socket; then
    echo "ERROR: Failed to enable gunicorn.socket"
    exit 1
fi

# Start socket
echo "Starting Gunicorn socket..."
if ! systemctl start gunicorn.socket; then
    echo "ERROR: Failed to start gunicorn.socket"
    echo "Checking socket status..."
    systemctl status gunicorn.socket --no-pager || true
    echo ""
    echo "Checking if socket file exists:"
    ls -la /run/gunicorn.sock || echo "Socket file not found"
    exit 1
fi

# Verify socket was created
sleep 1
if [ ! -S "$SOCKET_PATH" ]; then
    echo "WARNING: Socket file not created at $SOCKET_PATH"
    echo "Checking socket service status..."
    systemctl status gunicorn.socket --no-pager || true
else
    echo "Socket file created successfully ✓"
    ls -la "$SOCKET_PATH"
fi

# Enable service
echo "Enabling Gunicorn service..."
if ! systemctl enable gunicorn.service; then
    echo "ERROR: Failed to enable gunicorn.service"
    exit 1
fi

# Start service
echo "Starting Gunicorn service..."
if ! systemctl start gunicorn.service; then
    echo "ERROR: Failed to start Gunicorn service"
    echo ""
    echo "Checking service status..."
    systemctl status gunicorn.service --no-pager || true
    echo ""
    echo "Recent Gunicorn service logs:"
    journalctl -u gunicorn.service -n 50 --no-pager || true
    echo ""
    echo "Recent Gunicorn socket logs:"
    journalctl -u gunicorn.socket -n 20 --no-pager || true
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check logs: sudo journalctl -u gunicorn -f"
    echo "2. Verify Python path: cd $PROJECT_DIR && source venv/bin/activate && python -c 'import config.gunicorn.production'"
    echo "3. Test Gunicorn manually: cd $PROJECT_DIR && source venv/bin/activate && gunicorn --config config.gunicorn.production config.wsgi:application"
    echo "4. Check socket permissions: ls -la /run/gunicorn.sock"
    echo "5. Verify .env.prod exists and is readable: sudo -u ubuntu test -r $PROJECT_DIR/.env.prod"
    exit 1
fi

# Wait a moment for service to initialize
echo "Waiting for service to initialize..."
sleep 3

# Check status
echo ""
echo "Checking service status..."
if systemctl is-active --quiet gunicorn.service; then
    echo "✓ Gunicorn service is running"
    systemctl status gunicorn.service --no-pager -l | head -15
else
    echo "✗ WARNING: Gunicorn service may not be running properly"
    systemctl status gunicorn.service --no-pager -l || true
    echo ""
    echo "Recent service logs:"
    journalctl -u gunicorn.service -n 30 --no-pager || true
    echo ""
    echo "Attempting to diagnose issue..."
    
    # Check if socket is listening
    if [ -S "$SOCKET_PATH" ]; then
        echo "✓ Socket file exists: $SOCKET_PATH"
        ls -la "$SOCKET_PATH"
    else
        echo "✗ Socket file missing: $SOCKET_PATH"
    fi
    
    # Check if process is running
    if pgrep -f "gunicorn.*config.wsgi" > /dev/null; then
        echo "✓ Gunicorn process is running"
    else
        echo "✗ Gunicorn process not found"
    fi
fi

# Final verification
echo ""
echo "=========================================="
if systemctl is-active --quiet gunicorn.service && systemctl is-active --quiet gunicorn.socket; then
    echo "✓ Systemd services installed and running successfully!"
else
    echo "⚠ Systemd services installed but may need attention"
    echo "Check status with: sudo systemctl status gunicorn"
fi
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  View logs:        sudo journalctl -u gunicorn -f"
echo "  Restart service:  sudo systemctl restart gunicorn"
echo "  Check status:     sudo systemctl status gunicorn"
echo "  Stop service:     sudo systemctl stop gunicorn"
echo ""
