"""
red_code.py - top-level RED_CODE state and helpers

This provides a default RED_CODE structure and a helper to ensure
red_code.json exists (used by app.py and by euystacio_core/reflection).
"""
import json
import os
from datetime import datetime

RED_CODE = {
    "symbiosis_level": 0.0,
    "growth_history": [],
    "recent_pulses": [],
    "last_update": datetime.utcnow().strftime("%Y-%m-%d"),
    "meta": {"created_by": "euystacio", "created_at": datetime.utcnow().isoformat()}
}

RED_CODE_PATH = "red_code.json"

def ensure_red_code(path=RED_CODE_PATH):
    """
    Create red_code.json from the default RED_CODE if the file is missing or invalid.
    """
    try:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(RED_CODE, f, indent=2, ensure_ascii=False)
            return True
        # try to load it to ensure valid JSON
        with open(path, "r", encoding="utf-8") as f:
            _ = json.load(f)
        return True
    except Exception:
        # attempt to (re)write a safe default
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(RED_CODE, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

def load_red_code(path=RED_CODE_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_red_code(data, path=RED_CODE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
