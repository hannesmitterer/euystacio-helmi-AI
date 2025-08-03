#!/bin/bash
# deploy_setup.sh - SSH setup script for Netlify deployment

set -e

echo "Setting up SSH environment for Netlify deployment..."

# Create SSH directory if it doesn't exist
mkdir -p ~/.ssh

# Copy SSH config and key files to the user SSH directory
if [ -f ".ssh/config" ]; then
    echo "Copying SSH config..."
    cp .ssh/config ~/.ssh/config
fi

if [ -f ".ssh/netlify_deploy_key.pub" ]; then
    echo "Copying Netlify deploy key..."
    cp .ssh/netlify_deploy_key.pub ~/.ssh/netlify_deploy_key.pub
fi

# Set appropriate permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config 2>/dev/null || true
chmod 600 ~/.ssh/netlify_deploy_key.pub 2>/dev/null || true

echo "SSH environment setup completed!"

# Test SSH connection (optional)
if command -v ssh &> /dev/null; then
    echo "Testing SSH connection to GitHub..."
    ssh -T git@github.com -o ConnectTimeout=10 -o StrictHostKeyChecking=no || echo "SSH test completed (exit code expected)"
fi

echo "Running build process..."
python build_static.py