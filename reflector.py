"""
reflector.py - top-level reflection helper used by app.py

Implement reflect_and_suggest() which updates red_code and writes logs.
"""
import json
import os
from datetime import datetime
from red_code import load_red_code, save_red_code, RED_CODE_PATH

LOGS_DIR = "logs"
REFLECTION_LOG = os.path.join(LOGS_DIR, f"reflection_{datetime.utcnow().strftime('%Y%m%d')}.json")

def reflect_and_suggest():
    # Load current state
    try:
        state = load_red_code()
    except Exception:
        state = dict()

    # Simple reflection: create an artificial reflection entry
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "auto_reflection",
        "summary": "Automated reflection run",
    }

    # Append to growth_history
    gh = state.get("growth_history", [])
    gh.append(event)
    state["growth_history"] = gh
    state["last_update"] = datetime.utcnow().strftime("%Y-%m-%d")

    # Very simple "suggestion" logic based on symbiosis_level
    sym = state.get("symbiosis_level", 0.0)
    suggestion = {
        "timestamp": datetime.utcnow().isoformat(),
        "suggestion": "Increase community pulses" if sym < 0.5 else "Maintain current rhythm",
        "symbiosis_level": sym
    }

    # persist
    try:
        save_red_code(state, RED_CODE_PATH)
    except Exception:
        # best-effort only
        pass

    # write a reflection log entry
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        with open(REFLECTION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"reflection": event, "suggestion": suggestion}, ensure_ascii=False) + "\n")
    except Exception:
        pass

    # Return reflection summary for API
    return {"reflection": event, "suggestion": suggestion}
