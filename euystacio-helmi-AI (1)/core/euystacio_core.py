import json, random
from pathlib import Path

class EuystacioCore:
    def __init__(self, kernel_path=Path(__file__).parent / "red_code.json"):
        self.kernel = json.loads(open(kernel_path).read())
        self.mutable_values = {"trust": 1.0, "harmony": 1.0}
    
    def evolve(self, pulse_input):
        # adjust trust and harmony with random mild drift influenced by input
        for key in self.mutable_values:
            drift = random.uniform(-0.05, 0.05)
            self.mutable_values[key] = max(0.0, min(1.0, self.mutable_values[key] + drift))
        return self.mutable_values
