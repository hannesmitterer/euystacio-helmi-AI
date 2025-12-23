#!/bin/bash
# Euystacio GitHub Pages Deployment Script
# Automates deployment of the Euystacio project to GitHub Pages
# Author: Euystacio Team
# Motto: in consensus sacralis omnibus est

set -euo pipefail

# =========================
# CONFIGURATION
# =========================
GH_PAGES_BRANCH="gh-pages"
REMOTE="origin"

# =========================
# USAGE FUNCTION
# =========================
usage() {
    echo "Usage: $0 /path/to/deployment_package"
    echo ""
    echo "This script deploys the specified deployment package to GitHub Pages."
    echo "It manages the gh-pages branch, clears previous contents, and pushes"
    echo "the provided files to GitHub Pages."
    echo ""
    echo "Arguments:"
    echo "  deployment_package  Path to the directory containing files to deploy"
    echo ""
    echo "Example:"
    echo "  $0 ./github_pages_deploy"
    exit 1
}

# =========================
# LOGGING FUNCTION
# =========================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# =========================
# ERROR HANDLER
# =========================
error_exit() {
    log "ERROR: $1"
    exit 1
}

# =========================
# COPY DIRECTORY CONTENTS
# =========================
copy_directory_contents() {
    local src="$1"
    local dest="$2"
    # Copy all files including hidden ones, handle both cases where source has or lacks files
    cp -r "$src"/* "$dest"/ 2>/dev/null || cp -r "$src"/. "$dest"/
}

# =========================
# MAIN SCRIPT
# =========================

# Check arguments
if [ "$#" -ne 1 ]; then
    usage
fi

PACKAGE_PATH="$1"

# Validate package directory exists
if [ ! -d "$PACKAGE_PATH" ]; then
    error_exit "Deployment package directory '$PACKAGE_PATH' does not exist."
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error_exit "Not in a git repository. Please run this script from the repository root."
fi

log "===== Starting GitHub Pages deployment ====="
log "Deployment package: $PACKAGE_PATH"

# Store the current branch to return to later
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD)
log "Current branch: $CURRENT_BRANCH"

# Create a temporary directory for the deployment
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

log "Copying deployment files to temporary directory..."
copy_directory_contents "$PACKAGE_PATH" "$TEMP_DIR"

# Check if gh-pages branch exists remotely
log "Checking for existing gh-pages branch..."
if git ls-remote --exit-code --heads "$REMOTE" "$GH_PAGES_BRANCH" > /dev/null 2>&1; then
    log "gh-pages branch exists remotely. Fetching..."
    git fetch "$REMOTE" "$GH_PAGES_BRANCH"
    
    # Switch to gh-pages branch
    log "Switching to gh-pages branch..."
    if git show-ref --verify --quiet "refs/heads/$GH_PAGES_BRANCH"; then
        git checkout "$GH_PAGES_BRANCH"
    else
        git checkout -b "$GH_PAGES_BRANCH" "$REMOTE/$GH_PAGES_BRANCH"
    fi
    
    # Pull latest changes
    if ! git pull "$REMOTE" "$GH_PAGES_BRANCH"; then
        log "Warning: Pull failed. This may indicate merge conflicts or network issues."
        log "Continuing with deployment using current local state."
    fi
else
    log "gh-pages branch does not exist. Creating orphan branch..."
    git checkout --orphan "$GH_PAGES_BRANCH"
fi

# Clear all existing content (except .git directory)
log "Clearing previous contents..."
git rm -rf . 2>/dev/null || true
find . -maxdepth 1 ! -name '.git' ! -name '.' -exec rm -rf {} + 2>/dev/null || true

# Copy deployment files
log "Copying deployment files to repository..."
copy_directory_contents "$TEMP_DIR" "."

# Add .nojekyll to prevent Jekyll processing (optional but common for GitHub Pages)
if [ ! -f ".nojekyll" ]; then
    touch .nojekyll
fi

# Stage all files
log "Staging files for commit..."
git add -A

# Check if there are any changes to commit
if git diff --staged --quiet 2>/dev/null; then
    log "No changes to deploy. gh-pages is already up to date."
else
    # Commit the changes
    log "Committing changes..."
    git commit -m "🌞 Deploy to GitHub Pages: $(date '+%Y-%m-%d %H:%M:%S')"

    # Push to remote
    log "Pushing to $REMOTE/$GH_PAGES_BRANCH..."
    git push "$REMOTE" "$GH_PAGES_BRANCH"
    
    log "Deployment successful!"
fi

# Return to original branch
log "Returning to original branch: $CURRENT_BRANCH"
git checkout "$CURRENT_BRANCH"

log "===== GitHub Pages deployment complete ====="
log "Your site should be available at: https://<username>.github.io/<repository>/"
