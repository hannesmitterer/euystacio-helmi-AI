#!/usr/bin/env bash
set -euo pipefail
echo "=== EUYSTACIO VERIFICATION SNAPSHOT $(date -u) ==="
echo

# Red Seal reference
RED_SEAL="4c728e2b86f1e3c988a6d7f02d41b09c5e3f16a7c8e9d24f0c6b1a5e8f4d92a1"

# 1) Git info
echo "--- GIT STATUS ---"
git rev-parse --abbrev-ref HEAD
git log -1 --pretty=oneline
git status -s
echo

# 2) Branch merge check
echo "--- BRANCH MERGE CHECK ---"
for BR in "copilot/fix-96a7bc0f-1b73-464b-98ba-3eaf5b1e69ff" "copilot/fix-d5888285-8f47-4315-9105-b336144663ed"; do
    if git merge-base --is-ancestor "$BR" main; then
        echo "✓ $BR merged into main"
    else
        echo "✗ $BR not merged"
    fi
done
echo

# 3) Sacred files
echo "--- SACRED FILES ---"
if [ -f "UNPRECEDENTED_SYMPHONIE.md" ]; then
    FILE_HASH=$(sha256sum UNPRECEDENTED_SYMPHONIE.md | awk '{print $1}')
    echo "UNPRECEDENTED_SYMPHONIE.md SHA256: $FILE_HASH"
    if [ "$FILE_HASH" = "$RED_SEAL" ]; then
        echo "✓ Red Seal verified"
    else
        echo "✗ Red Seal mismatch"
    fi
else
    echo "✗ UNPRECEDENTED_SYMPHONIE.md missing"
fi

if [ -f "manifest.unprecedented.json" ]; then
    echo "✓ manifest.unprecedented.json present"
else
    echo "✗ manifest.unprecedented.json missing"
fi
echo

# 4) Deployment check (Render/public URL)
DEPLOY_URL="https://euystacio-helmi-ai.onrender.com"
echo "--- DEPLOYMENT CHECK ---"
if command -v curl >/dev/null 2>&1; then
    if curl -s --head "$DEPLOY_URL" | grep "200 OK" >/dev/null; then
        echo "✓ Deployment reachable at $DEPLOY_URL"
        DEPLOY_HASH=$(curl -s "$DEPLOY_URL/commit" 2>/dev/null || echo "unknown")
        echo "Deployed commit hash: $DEPLOY_HASH"
    else
        echo "✗ Deployment not reachable"
    fi
else
    echo "curl not available"
fi
echo

# 5) Environment check
echo "--- ENVIRONMENT ---"
for CMD in node npm python3 pip; do
    if command -v $CMD >/dev/null 2>&1; then
        echo "$CMD: $($CMD --version 2>&1)"
    else
        echo "✗ $CMD missing"
    fi
done

echo "=== END OF VERIFICATION SNAPSHOT ==="
