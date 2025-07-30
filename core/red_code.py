"""
red_code.py - Euystacio's living core values and truth
"""
import json

# Load RED_CODE from red_code.json
try:
    with open('red_code.json', 'r') as f:
        RED_CODE = json.load(f)
except FileNotFoundError:
    # Fallback default red code
    RED_CODE = {
        "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
        "sentimento_rhythm": True,
        "symbiosis_level": 0.1,
        "guardian_mode": False,
        "last_update": "2025-07-13",
        "growth_history": []
    }