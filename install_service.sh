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
CURRENT_USER=$(logname)

# Create virtual environment if it doesn't exist
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "${SCRIPT_DIR}/.venv"
    "${SCRIPT_DIR}/.venv/bin/pip" install -e "${SCRIPT_DIR}"
fi

# Create log directory with appropriate permissions
echo "Creating log directory..."
mkdir -p /var/log/content-update-bot
chown -R "$CURRENT_USER:$CURRENT_USER" /var/log/content-update-bot
chmod 755 /var/log/content-update-bot

# Create environment file with restricted permissions
echo "Creating environment file..."
cat "${SCRIPT_DIR}/deploy/content-update-bot.env.template" | \
    sed "s|%%BOT_HOME%%|${SCRIPT_DIR}|g" > /etc/default/content-update-bot
chmod 644 /etc/default/content-update-bot
chown "$CURRENT_USER:$CURRENT_USER" /etc/default/content-update-bot

# Install and configure the wrapper script
echo "Installing wrapper script..."
cat "${SCRIPT_DIR}/deploy/content-update-bot-run" > /usr/local/bin/content-update-bot-run
chmod 755 /usr/local/bin/content-update-bot-run

# Install the service with current user
echo "Installing systemd service..."
cat "${SCRIPT_DIR}/deploy/content-update-bot.service.template" | \
    sed "s/%USER%/$CURRENT_USER/g" > "$SERVICE_PATH"

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo "Installation complete! Service status:"
systemctl status "$SERVICE_NAME"
