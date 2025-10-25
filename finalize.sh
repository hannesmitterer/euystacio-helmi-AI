#!/bin/bash
# finalize.sh - Constitutional Local Integrity Check and Deployment Ready Script

echo "--- EUYSTACIO: URGENT LOCAL FINALIZATION PROCESS ---"

# 1. Check for Critical Files
if [ ! -f "index.html" ] || [ ! -f "GOVERNANCE.MD" ] || [ ! -f "FINANCE_EQUITY_PROTOCOL.JSON" ]; then
    echo "❌ ERROR: Critical constitutional files are missing. Aborting."
    exit 1
fi

# 2. Verify Wallet Address in index.html (Primary ST Endpoint)
if grep -q "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b" index.html; then
    echo "✅ INDEX.HTML: MetaMask ST Address VERIFIED."
else
    echo "❌ ERROR: ST Address not found in index.html. TAMPERING DETECTED."
    exit 1
fi

# 3. Verify Red Shield Echo (RSE) Integration
if grep -q "Red Shield Echo (RSE) Radar Feed" index.html; then
    echo "✅ RSE: Red Shield Echo integration VERIFIED."
else
    echo "❌ ERROR: RSE integration not confirmed. Defense is incomplete."
    exit 1
fi

# 4. Git Status Check (Ensure all changes are staged/committed)
echo "--- Checking Git Status ---"
if [[ -z $(git status -s) ]]; then
    echo "✅ GIT STATUS: Working directory is CLEAN. Ready for push."
else
    echo "⚠️ WARNING: Unstaged changes detected. RUN 'git add .' and 'git commit -m \"Final SRGB-CC RSE Launch\"' before pushing."
fi

echo "--- LOCAL FINALIZATION SUCCESSFUL. DEPLOYMENT READY. ---"
