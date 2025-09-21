#!/usr/bin/env bash
set -euo pipefail
echo "=== EUYSTACIO DIAGNOSTICS $(date -u) ==="
echo

# 1) git info
echo "--- Git remote & branch ---"
git rev-parse --abbrev-ref HEAD || true
git remote -v || true
echo

echo "--- Latest commits (5) ---"
git log -n 5 --pretty=format:'%h %ad %an %s' --date=iso || true
echo

# 2) check files + sha
FILE="UNPRECEDENTED_SYMPHONIE.md"
echo "--- File presence & sha256 ---"
if [ -f "$FILE" ]; then
  echo "$FILE exists"
  sha256sum "$FILE" || true
  echo "grep for seal:"
  grep -n "4c728e2b86f1e3c988a6d7f02d41b09c5e3f16a7c8e9d24f0c6b1a5e8f4d92a1" "$FILE" || true
else
  echo "$FILE not found in $(pwd)"
fi
echo

# 3) GitHub Actions / CI (if gh CLI present)
if command -v gh >/dev/null 2>&1; then
  echo "--- gh CLI found: recent workflow runs (requires gh auth) ---"
  gh run list --limit 5 || echo "(gh run list failed — maybe unauthenticated)"
else
  echo "--- gh CLI not installed; skipping Actions check. To check, run: gh run list --limit 5"
fi
echo

# 4) GitHub Pages / deployed frontend check (replace with your URL if different)
URL="https://hannesmitterer.github.io/EuystacioDRAFT/EuystacioDRAFT-Frontend/index.html"
echo "--- Checking public URL: $URL ---"
curl -sS -I "$URL" | sed -n '1,20p' || echo "(curl failed)"
echo

# 5) If Euystacio runs as systemd service named 'euystacio' (optional)
echo "--- Checking systemd service 'euystacio' (if exists) ---"
if command -v systemctl >/dev/null 2>&1; then
  systemctl status euystacio --no-pager || echo "(euystacio service not found or needs sudo)"
  echo "Recent journal entries for euystacio (last 200 lines):"
  journalctl -u euystacio -n 200 --no-pager || echo "(no journal or permission)"
else
  echo "systemctl not present, skipping."
fi
echo

# 6) Docker / container check (if applicable)
if command -v docker >/dev/null 2>&1; then
  echo "--- docker ps (euystacio containers) ---"
  docker ps --filter "name=euystacio" --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' || echo "(no containers matched)"
fi
echo

# 7) Kubernetes check (if kubectl available)
if command -v kubectl >/dev/null 2>&1; then
  echo "--- kubectl get pods (namespace default) ---"
  kubectl get pods -o wide || echo "(kubectl failed)"
  echo
  echo "--- kubectl logs for pods with name containing euystacio (first match) ---"
  POD=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep -i euystacio | head -n1 || true)
  if [ -n "$POD" ]; then
    echo "Found pod: $POD"
    kubectl logs --tail=200 "$POD" || true
  else
    echo "No pod name containing 'euystacio' found"
  fi
fi
echo

# 8) check for manifest
MAN="manifest.unprecedented.json"
echo "--- Manifest check ---"
if [ -f "$MAN" ]; then
  echo "$MAN found:"
  sed -n '1,200p' "$MAN"
else
  echo "$MAN not found in repo root"
fi
echo
echo "=== END DIAGNOSTICS ==="