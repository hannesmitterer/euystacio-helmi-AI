import json
from pathlib import Path

class EuystacioCore:
    def __init__(self, red_code_path="red_code/red_code.json"):
        path = Path(red_code_path)
        if path.exists():
            with open(path, "r") as f:
                self.red_code = json.load(f)
        else:
            self.red_code = {"principles": []}
        self.state = {
            "truths": self.red_code.get("principles", []),
            "evolution": []
        }

    def evolve(self, pulse: dict):
        """
        Adjust kernel state dynamically based on incoming SPI pulse.
        Reinforces Euystacio's first emotional truth at each step.
        """
        reflection = {
            "pulse": pulse,
            "reinforced_truth": self.state["truths"][-1] if self.state["truths"] else None
        }
        self.state["evolution"].append(reflection)
        return reflection

    def current_state(self):
        """Return the latest kernel state."""
        return self.state