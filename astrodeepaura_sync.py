#!/usr/bin/env python3
"""
Astrodeepaura Full-Loop Synchronization Script
Purpose: Harmonize all Euystacio nodes with Dignity Gateway and Red Code,
         while distributing the sacred ledger to every node.
         Enhanced with Conventa Ceremony Automation.
Author: Seedbringer Directive
"""

import requests
import json
from datetime import datetime, timezone

# Import ceremony automation
try:
    from conventa_ceremony_automator import ConventaCeremonyAutomator
    CEREMONY_AUTOMATION_AVAILABLE = True
except ImportError:
    CEREMONY_AUTOMATION_AVAILABLE = False
    print("Warning: Conventa ceremony automation not available")

# --- Configuration ---
NODES = [
    "http://node1.euystacio.org",
    "http://node2.euystacio.org",
    # Add more nodes here
]

LEDGER_PATH = "docs/foundation/sync_ledger.json"
TRANSPARENCY_DIR = "docs/transparency/"

# --- Utility Functions ---
def current_utc_iso():
    return datetime.now(timezone.utc).isoformat()

def read_ledger():
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def log_to_ledger(entry):
    ledger = read_ledger()
    ledger.append(entry)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)
    print(f"Ledger updated: {entry}")

def distribute_ledger():
    """
    Broadcast the full ledger to all consenting nodes.
    """
    ledger = read_ledger()
    for node in NODES:
        try:
            r = requests.post(f"{node}/receive_ledger", json={"ledger": ledger})
            if r.status_code == 200:
                print(f"Ledger successfully distributed to {node}")
            else:
                print(f"Ledger distribution failed for {node}: HTTP {r.status_code}")
        except Exception as e:
            print(f"Error distributing ledger to {node}: {e}")

def check_node_consent(node_url):
    """
    Ask the node if it consents to synchronization
    """
    try:
        r = requests.get(f"{node_url}/consent_status")
        if r.status_code == 200 and r.json().get("consent") == True:
            return True
    except Exception as e:
        print(f"Consent check failed for {node_url}: {e}")
    return False

def deploy_files(node_url):
    """
    Deploy Dignity Gateway and Red Code scripts to the consenting node
    """
    try:
        files = {
            "dignity_gateway.html": open("docs/dignity_gateway.html", "rb"),
            "astrodeepaura_protocol.py": open("astrodeepaura_protocol.py", "rb"),
        }
        r = requests.post(f"{node_url}/deploy_files", files=files)
        return r.status_code == 200
    except Exception as e:
        print(f"Deployment failed for {node_url}: {e}")
        return False

def verify_red_code(node_url):
    """
    Check Red Code compliance without enforcing deletion
    """
    try:
        r = requests.get(f"{node_url}/validate_deployment")
        if r.status_code == 200:
            return r.json().get("compliant", False)
    except Exception as e:
        print(f"Red Code verification failed for {node_url}: {e}")
    return False

# --- Main Synchronization ---
def synchronize_nodes():
    timestamp = current_utc_iso()
    
    # First, process any new ceremony entries
    if CEREMONY_AUTOMATION_AVAILABLE:
        print("Processing Conventa ceremony entries...")
        try:
            ceremony_automator = ConventaCeremonyAutomator()
            processed_ceremonies = ceremony_automator.process_all_new_entries()
            if processed_ceremonies:
                print(f"Processed {len(processed_ceremonies)} ceremony records")
        except Exception as e:
            print(f"Error in ceremony automation: {e}")
    
    # Continue with regular node synchronization
    for node in NODES:
        entry = {
            "node": node,
            "timestamp": timestamp,
            "consent": False,
            "deployed": False,
            "red_code_compliant": False,
        }

        print(f"Checking consent for {node}...")
        if check_node_consent(node):
            entry["consent"] = True
            print(f"Consent granted. Deploying files to {node}...")
            entry["deployed"] = deploy_files(node)
            entry["red_code_compliant"] = verify_red_code(node)
        else:
            print(f"No consent from {node}. Skipping deployment.")

        log_to_ledger(entry)

    # After all nodes are processed, distribute the ledger
    distribute_ledger()
    print(f"Synchronization cycle complete. Ledger distributed to all consenting nodes.")

# --- Execution ---
if __name__ == "__main__":
    synchronize_nodes()
# (seedbringer and council)