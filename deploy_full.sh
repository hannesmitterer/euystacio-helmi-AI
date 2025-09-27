#!/bin/bash
# Euystacio Full Fail-Safe Deployment Package
# Author: Seedbringer
# Date: 2025-09-27
# Motto: in consensus sacralis omnibus est

set -euo pipefail

# =========================
# CONFIGURATION
# =========================
APP_NAME="euystacio"
DEPLOY_DIR="/opt/$APP_NAME"
BACKUP_DIR="/opt/${APP_NAME}_backup_$(date +%Y%m%d%H%M%S)"
LOG_FILE="/var/log/${APP_NAME}_deploy.log"
GIT_REPO="https://github.com/hannesmitterer/euystacio-helmi-AI.git"
BRANCH="main"
HEALTH_URL="http://localhost:8080/health"
USE_DOCKER=true
DOCKER_IMAGE="euystacio:latest"
TMP_DIR=$(mktemp -d)

# =========================
# LOGGING FUNCTION
# =========================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "===== Starting fail-safe deployment for $APP_NAME ====="

# =========================
# BACKUP CURRENT DEPLOYMENT
# =========================
if [ -d "$DEPLOY_DIR" ]; then
    log "Backing up current deployment to $BACKUP_DIR..."
    cp -r "$DEPLOY_DIR" "$BACKUP_DIR"
fi

# =========================
# ENVIRONMENT SETUP
# =========================
log "Setting up environment..."
mkdir -p "$DEPLOY_DIR"
# Optional: create virtualenv or dependencies here
# python3 -m venv "$DEPLOY_DIR/venv"
# source "$DEPLOY_DIR/venv/bin/activate"
# pip install -r requirements.txt

# =========================
# CLONE NEW RELEASE
# =========================
log "Cloning new release from branch $BRANCH..."
git clone --branch "$BRANCH" "$GIT_REPO" "$TMP_DIR"

# =========================
# DOCKER OPTION
# =========================
if [ "$USE_DOCKER" = true ]; then
    log "Building Docker image $DOCKER_IMAGE..."
    docker build -t "$DOCKER_IMAGE" "$TMP_DIR"
    log "Stopping existing Docker container if exists..."
    docker rm -f "$APP_NAME" || true
    log "Starting new Docker container..."
    docker run -d --name "$APP_NAME" -p 8080:8080 "$DOCKER_IMAGE"
else
    # =========================
    # STANDARD DEPLOYMENT
    # =========================
    log "Deploying new release to $DEPLOY_DIR..."
    rm -rf "$DEPLOY_DIR"
    mv "$TMP_DIR" "$DEPLOY_DIR"

    log "Setting permissions..."
    chown -R www-data:www-data "$DEPLOY_DIR"
    chmod -R 755 "$DEPLOY_DIR"

    log "Restarting service..."
    systemctl restart "$APP_NAME"
fi

# =========================
# HEALTH CHECK AND ROLLBACK
# =========================
log "Verifying deployment..."
if curl -sf "$HEALTH_URL" >/dev/null; then
    log "Health check passed. Deployment successful."
else
    log "Health check failed. Rolling back..."
    if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$DEPLOY_DIR"
        mv "$BACKUP_DIR" "$DEPLOY_DIR"
        if [ "$USE_DOCKER" = true ]; then
            docker rm -f "$APP_NAME" || true
            docker run -d --name "$APP_NAME" -p 8080:8080 "$DOCKER_IMAGE"
        else
            systemctl restart "$APP_NAME"
        fi
    fi
    log "Rollback completed due to failed health check."
    exit 1
fi

log "===== Deployment process completed successfully ====="