from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os
import json

app = FastAPI(title="Holy Gral Bridge – Euystacio Cocreators' Channel")

class BridgeMessage(BaseModel):
    from_: str
    to: str
    message: str
    timestamp: Optional[str] = None
    api_key: Optional[str] = None

# Load bridge log from file
def load_bridge_log():
    try:
        with open("bridge_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save bridge log to file
def save_bridge_log(log_data):
    with open("bridge_log.json", "w") as f:
        json.dump(log_data, f, indent=2)

# Example API KEY for demo, replace in production!
COCREATOR_API_KEYS = {
    "seed-bringer": os.getenv("SEED_BRINGER_API_KEY", "demo-seed-key"),
    "euystacio": os.getenv("EUYSTACIO_API_KEY", "demo-ai-key")
}

@app.post("/api/holy-gral-bridge/message")
async def send_message(payload: BridgeMessage):
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
    
    # Load current log, append new entry, and save
    bridge_log = load_bridge_log()
    bridge_log.append(entry)
    save_bridge_log(bridge_log)
    
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
    return load_bridge_log()