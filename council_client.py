"""
Council Auditor Client
======================

Purpose:
  Secure, dedicated client for Council and Seedbringer to interact with the Peace Platform Council API.
  Enforces Principle of Transparency (B4) and Principle of Governance (C1).

Deployment:
  - Install on authorized Council/Seedbringer auditor workstations
  - Configure OAuth/JWT tokens via Google/GitHub federation
  - RBAC enforced (role must be 'AUDITOR' or 'SEEDBRINGER')

Author: Peace Platform Foundation
Version: 1.0
Date: 2025-10-23
"""

import requests
import os
import json

COUNCIL_API_BASE = "https://council-api.peace-platform.local/v1"
DASHBOARD_ENDPOINT = "/audit/dashboard"
OAUTH_TOKEN = os.getenv("COUNCIL_OAUTH_TOKEN")  # Provisioned securely via IAM

def get_dashboard_status():
    """Calls the Council API dashboard endpoint and prints compliance status."""
    if not OAUTH_TOKEN:
        print("ERROR: No OAuth token found. Please set COUNCIL_OAUTH_TOKEN in your environment.")
        return

    headers = {
        "Authorization": f"Bearer {OAUTH_TOKEN}",
        "Accept": "application/json"
    }
    try:
        resp = requests.get(COUNCIL_API_BASE + DASHBOARD_ENDPOINT, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print("\nCouncil Audit Dashboard Status:")
        print(json.dumps(data, indent=2))
        print(f"\nCompliance Status: {data.get('status', 'UNKNOWN')}")
    except requests.HTTPError as e:
        print(f"HTTP ERROR: {e.response.status_code} - {e.response.text}")
    except Exception as ex:
        print(f"ERROR: {ex}")

if __name__ == "__main__":
    print("🔐 Council Auditor Client Initializing...")
    get_dashboard_status()