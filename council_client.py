import toml
import requests
import json
import time
from typing import Dict, Any, List

# --- IMPORTANT SETUP ---
# NOTE: The Council client needs the core GLA class for direct integrity check.
# In a real setup, ensure LogEntry and GatewayLogAgent are importable.
# from gla_module import GatewayLogAgent
# -----------------------

# Placeholder class for TOML configuration reading
class Config:
    """Simple class to load and access configuration."""
    def __init__(self, path="config.toml"):
        with open(path, 'r') as f:
            self._data = toml.load(f)

    def get(self, section: str, key: str):
        return self._data.get(section, {}).get(key)

def run_council_audit(gla_instance):
    """
    Simulates a Council-level audit process using the configured components.
    
    :param gla_instance: An initialized GatewayLogAgent instance pointing to the ledger.
    """
    config = Config()
    
    print("--- 🛡️ Council Audit Client Initiated ---")
    print(f"Targeting Deployment: {config.get('system', 'deployment_id')}")
    print("-" * 40)

    # --- PART 1: Direct Integrity Check (Highest Trust Level) ---
    # The Council Auditor performs a direct, on-server audit of the ledger file.
    print("1. Direct Log Chain Integrity Check (GLA Internal Audit)")
    
    audit_start_time = time.time()
    is_valid = gla_instance.verify_chain_integrity()
    audit_duration = time.time() - audit_start_time
    
    if is_valid:
        print(f"✅ CHAIN VALID: The entire log chain is cryptographically intact.")
    else:
        print(f"❌ CHAIN BROKEN: Tampering or corruption detected in the log ledger.")
        
    print(f"   Audit Time: {audit_duration:.4f} seconds")
    print("-" * 40)

    # --- PART 2: Read-Only API Query (External Audit) ---
    api_url = config.get('council_api', 'base_url')
    logs_url = api_url + config.get('council_api', 'logs_endpoint')
    proof_base_url = api_url + config.get('council_api', 'proof_endpoint')
    
    print(f"2. Council API External Audit (Querying: {api_url})")

    # a) Fetch the latest entries
    try:
        response = requests.get(logs_url, params={"limit": 3, "offset": 0})
        response.raise_for_status()
        latest_logs: List[Dict[str, Any]] = response.json()
        
        if not latest_logs:
            print("   INFO: No logs found in the ledger to query.")
            return

        print(f"✅ Fetched {len(latest_logs)} latest logs via API.")
        first_entry_hash = latest_logs[0]['current_hash']
        
    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED to connect to Council API at {api_url}. Is the service running?")
        return
    except requests.exceptions.HTTPError as e:
        print(f"❌ API returned an error: {e}")
        return
        
    # b) Request an Audit Proof for the latest entry
    print(f"\n   Requesting Audit Proof for latest entry (Hash: {first_entry_hash[:8]}...)")
    proof_url = f"{proof_base_url}/{first_entry_hash}"

    try:
        proof_response = requests.get(proof_url)
        proof_response.raise_for_status()
        proof_data: Dict[str, Any] = proof_response.json()
        
        entry_integrity = proof_data.get('integrity_status', False)
        prev_hash = proof_data.get('chain_proof', {}).get('previous_hash')

        if entry_integrity:
            print("✅ PROOF VERIFIED: Entry integrity check passed on the API side.")
            print(f"   Previous Hash: {prev_hash[:16]}...")
        else:
            print("❌ PROOF FAILED: API detected tamper (Internal Log Tamper Detected).")

    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to get proof: {proof_response.status_code} - {proof_response.json().get('detail', 'Unknown error')}")
        
    print("-" * 40)

if __name__ == "__main__":
    # --- SIMULATION SETUP ---
    # To run this script, you must ensure:
    # 1. The GatewayLogAgent and its dependencies are importable.
    # 2. A 'gla_ledger.db' exists with data (run the usage_example_gla.py first).
    # 3. The council_api.py service is running (e.g., via `uvicorn council_api:app`).
    
    try:
        # NOTE: Replace with the actual import in your final environment
        # For this context, we assume the class is available
        gla_for_audit = GatewayLogAgent(agent_id="Council-Auditor-Agent")
        
        # This will fail if the DB doesn't exist or isn't populated
        if not os.path.exists(gla_for_audit.DB_PATH):
             print(f"SETUP WARNING: Ledger DB not found at {gla_for_audit.DB_PATH}. Run 'usage_example_gla.py' first.")
             # Still proceed to test the API connection if possible
        
        run_council_audit(gla_for_audit)
        
    except NameError:
        print("\nERROR: Cannot run direct audit. The 'GatewayLogAgent' class must be importable.")
        print("Please ensure your environment is fully set up to test the system.")