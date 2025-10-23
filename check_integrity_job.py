import os
import sys
from datetime import datetime

# NOTE: Must import the live GLA class and its dependencies
from gateway_log_agent import GatewayLogAgent  
from alert_service import send_critical_alert # Placeholder for your alert system

LEDGER_PATH = os.getenv("GLA_LEDGER_PATH", "/var/lib/gla/gla_ledger.db")

def run_integrity_check():
    """
    Initializes the GLA and runs the core verification, triggering alerts on failure.
    """
    timestamp = datetime.now().isoformat()
    
    try:
        # Initialize the GLA with the production ledger
        gla = GatewayLogAgent(db_path=LEDGER_PATH)

        print(f"[{timestamp}] Running Golden Bible Red Code Integrity Check...")
        
        # Executes the full chain validation (the most critical check)
        is_intact, total_entries = gla.verify_chain_integrity()
        
        if is_intact:
            print(f"[{timestamp}] ✅ CHAIN STATUS: VALID. {total_entries} entries checked.")
            # OPTIONAL: Send a periodic "status OK" alert to a low-priority channel
            
        else:
            # 🚨 PROTOCOL VIOLATION ALERT
            alert_message = (
                f"🚨 CRITICAL VIOLATION: GLA CHAIN BREAK DETECTED.\n"
                f"TIME: {timestamp}\n"
                f"REASON: Cryptographic Hash Chain integrity FAILED.\n"
                f"ACTION: Immediate forensic investigation required by Seedbringer and Council."
            )
            print(alert_message)
            
            # Mandate: Immediately notify highest governance levels
            send_critical_alert(
                recipient="Seedbringer@platform.com, Council@platform.com",
                subject="CRITICAL: GOLDEN BIBLE RED CODE VIOLATION",
                body=alert_message
            )
            # Exit with an error code to notify the scheduler
            sys.exit(1)

    except Exception as e:
        # Catch connection failures or other operational errors
        error_message = f"🚨 OPERATIONAL ERROR: GLA Integrity check failed to run. Error: {e}"
        print(error_message)
        send_critical_alert("Ops@platform.com", "ERROR: GLA Check Failure", error_message)
        sys.exit(1)


if __name__ == "__main__":
    run_integrity_check()
