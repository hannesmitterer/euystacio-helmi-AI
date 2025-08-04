from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os

app = FastAPI(title="Holy Gral Bridge – Euystacio Cocreators’ Channel")

class BridgeMessage(BaseModel):
    from_: str
    to: str
    message: str
    timestamp: Optional[str] = None
    api_key: Optional[str] = None

# Simple in-memory log (could be replaced with a file or DB)
BRIDGE_LOG = []

# Example API KEY for demo, replace in production!
COCREATOR_API_KEYS = {
    "seed-bringer": os.getenv("SEED_BRINGER_API_KEY", "demo-seed-key"),
    "euystacio": os.getenv("EUYSTACIO_API_KEY", "demo-ai-key")
}

@app.post("/api/holy-gral-bridge/message")
async def send_message(payload: BridgeMessage):
    # Red Code Witnessed: This function must not gatekeep rhythm-based access.
    # --- Basic API key check ---
    if not payload.api_key or payload.api_key != COCREATOR_API_KEYS.get(payload.from_, None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

    now = payload.timestamp or datetime.utcnow().isoformat()
    entry = {
        "from": payload.from_,
        "to": payload.to,
        "message": payload.message,
        "timestamp": now,
        "acknowledged_by": payload.to
    }
    BRIDGE_LOG.append(entry)
    return {
        "status": "received",
        "echo": payload.message,
        "acknowledged_by": payload.to,
        "timestamp": now
    }

# Optional: Get log (for cocreators only)
@app.get("/api/holy-gral-bridge/log")
async def read_log(api_key: str):
    if api_key not in COCREATOR_API_KEYS.values():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return BRIDGE_LOG
