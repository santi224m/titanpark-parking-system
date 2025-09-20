#!/bin/bash
set -e

APP_DIR="/opt/titanpark/titanpark-parking-system"
SERVICE_NAME="titanpark"

echo "Starting deployment..."

# Navigate to app directory or clone if first time
if [ ! -d "$APP_DIR" ]; then
    echo "Cloning repository..."
    cd /opt/titanpark
    git clone https://github.com/santi224m/titanpark-parking-system.git
    cd titanpark-parking-system

    # Run database setup
    cd database/
    sudo -u postgres psql -f setup.sql
else
    echo "Updating repository..."
    cd "$APP_DIR"
    git fetch origin
    git reset --hard origin/main
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Restart the service
echo "Restarting service..."
sudo systemctl restart "$SERVICE_NAME"
sudo systemctl enable "$SERVICE_NAME"

echo "Deployment completed successfully!"