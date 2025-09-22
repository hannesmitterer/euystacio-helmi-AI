#!/usr/bin/env bash
# euystacio-verify.sh

set -e

echo "🔐 Verifying Euystacio kernel covenant..."

for f in *.sha256; do
  sha256sum -c "$f" || {
    echo "❌ Verification failed for $f"
    exit 1
  }
done

echo "✅ All covenant files verified (Euystacio kernel intact)."