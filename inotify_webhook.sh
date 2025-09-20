#!/usr/bin/env bash
# inotify_webhook.sh
# Watches DECLARATIO.md and related critical files and POSTs a signed JSON payload to a webhook on changes.
# Requirements: inotifywait (from inotify-tools), curl, jq
#
# Usage: ./inotify_webhook.sh /path/to/watch WEBHOOK_URL "SECRET_TOKEN"

WATCH_DIR="${1:-.}"
WEBHOOK_URL="${2:-https://example.org/manifest-webhook}"
SECRET="${3:-REPLACE_WITH_SECRET}"

FILES_TO_WATCH="DECLARATIO.md DECLARATIO.md.sig declaratio-v1.0-20250916"

echo "Watching $WATCH_DIR for changes to critical files..."
while inotifywait -e close_write,create,delete -r $WATCH_DIR; do
  for f in $FILES_TO_WATCH; do
    if [ -f "$WATCH_DIR/$f" ]; then
      sha=$(sha256sum "$WATCH_DIR/$f" | awk '{print $1}')
      payload=$(jq -n --arg f "$f" --arg sha "$sha" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{file:$f,sha:$sha,timestamp:$t}')
      # Sign payload with secret (HMAC) - requires openssl
      sig=$(printf "%s" "$payload" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64)
      curl -s -X POST -H "Content-Type: application/json" -H "X-Signature: $sig" -d "$payload" "$WEBHOOK_URL"
      echo "Posted change for $f ($sha) at $(date -u)"
    fi
  done
done
