"""
Red Code - Core values and dynamic configuration for Euystacio
"""
import json
import os

RED_CODE_PATH = "red_code.json"

def load_red_code():
    """Load the red code from JSON file"""
    try:
        with open(RED_CODE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default red code if file doesn't exist
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": "2025-07-13",
            "growth_history": [],
            "recent_pulses": []
        }

# Load the red code on import
RED_CODE = load_red_code()

def save_red_code(code):
    """Save the red code to JSON file"""
    with open(RED_CODE_PATH, 'w') as f:
        json.dump(code, f, indent=2)

def update_red_code(updates):
    """Update the red code with new values"""
    global RED_CODE
    RED_CODE.update(updates)
    save_red_code(RED_CODE)