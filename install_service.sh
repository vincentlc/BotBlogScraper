#!/bin/bash

# Exit on any error
set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Setup variables
SERVICE_NAME="content-update-bot"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

# Create virtual environment if it doesn't exist
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "${SCRIPT_DIR}/.venv"
fi

# Install package and dependencies
echo "Installing package and dependencies..."
"${SCRIPT_DIR}/.venv/bin/pip" install -e "${SCRIPT_DIR}"

# Copy service file
echo "Installing systemd service..."
cp "${SCRIPT_DIR}/${SERVICE_NAME}.service" "$SERVICE_PATH"

# Reload systemd
systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo "Installation complete! Service status:"
systemctl status "$SERVICE_NAME"