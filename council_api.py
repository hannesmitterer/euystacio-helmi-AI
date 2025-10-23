import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime
import uvicorn

# --- IMPORTANT SETUP ---
# from your_gla_module import GatewayLogAgent, LogEntry
# from your_key_registry_module import KeyRegistry 

# Define Pydantic Model for structured API responses
class LogEntryModel(BaseModel):
    """Pydantic model that mirrors the LogEntry dataclass for API serialization."""
    timestamp: str
    index: int
    previous_hash: str
    message_id: str
    sender_id: str
    performative: str
    audit_context: Dict[str, Any]
    message_payload_hash: str
    signature_verified: bool
    sender_trust_weight: float
    signature: str
    current_hash: str

class AuditProofModel(BaseModel):
    """Model representing the entry plus context for the Council API."""
    entry: LogEntryModel
    chain_proof: Dict[str, Any]
    integrity_status: bool = True

app = FastAPI(
    title="Council Read-Only Gateway Log Agent API",
    description="Provides auditable and verifiable access to the immutable log ledger."
)

# Initialize the core components (Use the same DB path as your GLA instance)
DB_PATH = "gla_ledger.db" # Make sure this matches the GLA's actual operational DB
try:
    gla = GatewayLogAgent(agent_id="Council-API-Reader")
except NameError:
    # Fallback if GatewayLogAgent is not defined in the scope (for standalone testing)
    print("WARNING: GatewayLogAgent class not found. API endpoints will not be functional.")
    gla = None 

# --- API Endpoints (Council Read-Only Access) ---
@app.get("/logs", response_model=List[LogEntryModel], summary="Retrieve Log Chain Slice")
def get_logs(
    limit: int = Query(100, ge=1, le=500, description="Max number of entries to return."),
    offset: int = Query(0, ge=0, description="Offset for pagination.")
):
    """
    Returns a paginated slice of the log ledger, ordered newest first.
    """
    if gla is None:
         raise HTTPException(status_code=503, detail="GLA Service Unavailable.")
         
    logs = gla.get_log_range(limit=limit, offset=offset)
    
    # The LogEntry dataclass must be converted to the Pydantic model
    return [LogEntryModel(**entry.to_canonical_dict(), current_hash=entry.current_hash, signature=entry.signature) for entry in logs]

@app.get("/log/{entry_hash}", response_model=AuditProofModel, summary="Get Single Entry Proof and Audit Context")
def get_log_by_hash(entry_hash: str):
    """
    Returns a single log entry and critical chain proof context for external auditing.
    """
    if gla is None:
         raise HTTPException(status_code=503, detail="GLA Service Unavailable.")
         
    entry = gla.get_log_by_hash(entry_hash)
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"Log entry with hash {entry_hash[:8]}... not found.")
    
    # --- PROOF GENERATION (Core Governance Requirement) ---
    
    # 1. Recompute hash for integrity check (Should match entry_hash if not tampered)
    recomputed_hash = entry.calculate_entry_hash(entry.to_canonical_dict())
    integrity_check = (recomputed_hash == entry_hash)
    
    # 2. Fetch the previous entry's hash for chain context (the verifier can confirm this hash exists)
    previous_entry = gla.get_log_by_hash(entry.previous_hash)
    previous_entry_exists = previous_entry is not None or entry.previous_hash == gla.GENESIS_HASH

    chain_proof = {
        "verified_entry_hash": recomputed_hash,
        "previous_hash": entry.previous_hash,
        "previous_entry_found": previous_entry_exists,
        "verification_timestamp": datetime.utcnow().isoformat() + "Z"
        # In a complete system, this proof would also include a GLA signature over this JSON object.
    }

    # If the recomputed hash doesn't match the stored hash, the log itself is compromised.
    if not integrity_check:
        raise HTTPException(status_code=500, detail="Internal Log Tamper Detected on Retrieval.")

    return AuditProofModel(
        entry=LogEntryModel(**entry.to_canonical_dict(), current_hash=entry.current_hash, signature=entry.signature),
        chain_proof=chain_proof,
        integrity_status=integrity_check
    )

# --- Run Command Example ---
if __name__ == "__main__":
    # To run this API (assuming all dependencies are met):
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Council API Skeleton ready. Use 'uvicorn council_api:app --reload' to run.")
