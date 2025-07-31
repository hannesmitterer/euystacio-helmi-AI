import json
import os

def load_red_code():
    """Load the red code from the JSON file"""
    red_code_path = "red_code.json"
    if os.path.exists(red_code_path):
        with open(red_code_path, 'r') as f:
            return json.load(f)
    return {
        "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
        "sentimento_rhythm": True,
        "symbiosis_level": 0.1,
        "guardian_mode": False,
        "last_update": "2025-07-13",
        "growth_history": []
    }

# Export the RED_CODE constant
RED_CODE = load_red_code()