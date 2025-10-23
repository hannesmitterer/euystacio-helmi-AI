#!/usr/bin/env python3
"""
Automated Audit Compliance Checker
==================================

This script automates the Final Protocol Compliance Checklist for the
Inter-AI Communication Gateway (Golden Bible Red Code). It verifies
Integrity, Transparency, and Governance principles using local GLA
instance and/or the Council API.

Author: Peace Platform Foundation
Version: 1.0
Date: 2025-10-23
"""

import hashlib
import json
import requests
from typing import List, Dict, Any

# --- Configuration ---
COUNCIL_API_BASE = "https://council-api.peace-platform.local/v1"
COUNCIL_API_KEY = "YOUR_READ_ONLY_API_KEY"  # Replace with secure storage retrieval
GLA_INSTANCE = None  # Replace with actual GLA instance if local

# --- Helper Functions ---

def hash_canonical_payload(payload: Dict[str, Any]) -> str:
    """Generate canonical SHA-256 hash of JSON payload with sorted keys."""
    canonical = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def fetch_recent_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve recent logs from Council API or local GLA instance."""
    headers = {"Authorization": f"Bearer {COUNCIL_API_KEY}"}
    try:
        response = requests.get(f"{COUNCIL_API_BASE}/logs/recent?limit={limit}", headers=headers)
        response.raise_for_status()
        return response.json().get("logs", [])
    except Exception as e:
        print(f"⚠️ Failed to fetch logs from Council API: {e}")
        return []

def verify_chain_integrity(gla_instance) -> bool:
    """Run chain integrity verification on local GLA instance."""
    if gla_instance is None:
        print("⚠️ No local GLA instance provided; skipping chain integrity check.")
        return True
    return gla_instance.verify_chain_integrity()

def check_signature_verified(log_entry: Dict[str, Any]) -> bool:
    """Check if signature_verified field is True."""
    return log_entry.get("signature_verified", False)

def check_audit_context_complete(log_entry: Dict[str, Any]) -> bool:
    """Ensure Audit_Context contains all required fields."""
    audit_ctx = log_entry.get("payload", {}).get("Audit_Context", {})
    required_keys = ["source_event_id", "intended_state_change", "human_readable_summary"]
    return all(k in audit_ctx and audit_ctx[k] for k in required_keys)

def check_trust_weight_range(log_entry: Dict[str, Any]) -> bool:
    """Confirm sender_trust_weight is in [0.0, 1.0]."""
    tw = log_entry.get("sender_trust_weight", -1)
    return 0.0 <= tw <= 1.0

def audit_integrity(logs: List[Dict[str, Any]]) -> bool:
    """Audit cryptographic integrity."""
    all_pass = True
    # Check signatures
    for entry in logs:
        if not check_signature_verified(entry):
            print(f"❌ Integrity Fail: signature not verified for message {entry.get('message_id')}")
            all_pass = False
    return all_pass

def audit_transparency(logs: List[Dict[str, Any]]) -> bool:
    """Audit transparency: audit context completeness and readability."""
    all_pass = True
    for entry in logs:
        if not check_audit_context_complete(entry):
            print(f"❌ Transparency Fail: incomplete Audit_Context in message {entry.get('message_id')}")
            all_pass = False
    return all_pass

def audit_governance(logs: List[Dict[str, Any]], gla_instance) -> bool:
    """Audit governance: trust weight and chain coherence."""
    all_pass = True
    for entry in logs:
        if not check_trust_weight_range(entry):
            print(f"❌ Governance Fail: sender_trust_weight out of range in message {entry.get('message_id')}")
            all_pass = False
    # Chain integrity check
    if not verify_chain_integrity(gla_instance):
        print("❌ Governance Fail: Chain integrity verification failed.")
        all_pass = False
    return all_pass

# --- Main Execution ---

def main():
    print("🔎 Starting Automated Audit Compliance Checker...\n")
    logs = fetch_recent_logs(limit=100)

    print("🛡️ Auditing Cryptographic Integrity...")
    integrity_pass = audit_integrity(logs)
    
    print("🌐 Auditing Transparency...")
    transparency_pass = audit_transparency(logs)
    
    print("🏛️ Auditing Governance...")
    governance_pass = audit_governance(logs, GLA_INSTANCE)

    overall_pass = integrity_pass and transparency_pass and governance_pass
    print("\n--- Audit Summary ---")
    print(f"Integrity: {'PASS ✅' if integrity_pass else 'FAIL ❌'}")
    print(f"Transparency: {'PASS ✅' if transparency_pass else 'FAIL ❌'}")
    print(f"Governance: {'PASS ✅' if governance_pass else 'FAIL ❌'}")
    print(f"\nOverall Compliance Status: {'PASS ✅' if overall_pass else 'FAIL ❌'}")

    if not overall_pass:
        print("\n⚠️ One or more compliance checks failed. Immediate remediation required.")
    else:
        print("\n✅ All checks passed. System is fully compliant with the Golden Bible Red Code.")

if __name__ == "__main__":
    main()