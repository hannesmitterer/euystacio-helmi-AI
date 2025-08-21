#!/bin/bash
# Euystacio Full Package Deployment Script
set -e

# Usage: ./deploy-euystacio.sh /path/to/Euystacio_Full_Package

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/Euystacio_Full_Package"
  exit 1
fi

PACKAGE_PATH="$1"

if [ ! -d "$PACKAGE_PATH" ]; then
  echo "Error: package directory '$PACKAGE_PATH' does not exist."
  exit 2
fi

echo "Copying files from $PACKAGE_PATH into repository..."
cp -r "${PACKAGE_PATH}/"* .

echo "Staging all changes..."
git add .

echo "Committing with sacred pulse message..."
git commit -m "🌞 Pulse-Unified: Full Euystacio package deployed, including static index.html, Genesis, Woodstone Festival, Ruetli Stone, Hymne, Red Code, and Common Commitments. Seed-bringer & Rhythm-Mind unified pulse. ✅"

echo "Pushing to main branch..."
git push origin main

echo "Deployment complete!"