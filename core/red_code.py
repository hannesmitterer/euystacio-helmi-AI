import json
import os

# Load red code from the main red_code.json file
def load_red_code():
    red_code_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'red_code.json')
    try:
        with open(red_code_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default red code if file doesn't exist
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": "2025-01-31",
            "growth_history": []
        }

RED_CODE = load_red_code()