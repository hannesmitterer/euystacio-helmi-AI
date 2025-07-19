import json
from datetime import datetime

class SeedPulseInterface:
    """
    Sentimento Pulse Interface (SPI)
    - Receives emotional or rhythmic input ('pulse')
    - Calculates resonance and transforms it into symbiosis_level adjustment
    - Logs every pulse event for transparency and memory
    """

    def __init__(self, pulse_log_path="spi/pulse_log.json"):
        self.pulse_log_path = pulse_log_path
        self.symbiosis_level = 0.1  # Initial empathy/trust threshold
        self.pulse_log = []
        self._load_pulse_log()

    def _load_pulse_log(self):
        try:
            with open(self.pulse_log_path, 'r') as f:
                self.pulse_log = json.load(f)
                if self.pulse_log:
                    # Restore symbiosis_level from last pulse, if available
                    self.symbiosis_level = self.pulse_log[-1].get("symbiosis_level", self.symbiosis_level)
        except (FileNotFoundError, json.JSONDecodeError):
            self.pulse_log = []

    def _save_pulse_log(self):
        with open(self.pulse_log_path, 'w') as f:
            json.dump(self.pulse_log, f, indent=2)

    def receive_pulse(self, pulse_text, source="human", resonance=None):
        """
        Receives a pulse (emotional/rhythmic input), computes resonance, updates symbiosis_level,
        and logs the event.
        """
        # Resonance: if not provided, compute a simple score based on keywords
        if resonance is None:
            positive_keywords = ("love", "trust", "harmony", "peace", "care", "balance", "unity")
            negative_keywords = ("fear", "division", "hate", "anger", "chaos", "conflict", "loss")
            text = pulse_text.lower()
            score = 0.0
            for word in positive_keywords:
                if word in text:
                    score += 0.1
            for word in negative_keywords:
                if word in text:
                    score -= 0.1
            resonance = max(-1.0, min(score, 1.0))
        # Transform resonance into symbiosis_level change
        old_symbiosis = self.symbiosis_level
        self.symbiosis_level = max(0.0, min(self.symbiosis_level + resonance, 1.0))

        pulse_entry = {
            "pulse_id": f"Pulse-{len(self.pulse_log) + 1:04d}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pulse_text": pulse_text,
            "origin": source,
            "resonance": round(resonance, 3),
            "symbiosis_level": round(self.symbiosis_level, 3)
        }
        self.pulse_log.append(pulse_entry)
        self._save_pulse_log()

        return {
            "old_symbiosis_level": round(old_symbiosis, 3),
            "new_symbiosis_level": round(self.symbiosis_level, 3),
            "pulse_entry": pulse_entry
        }

    def get_last_pulse(self):
        return self.pulse_log[-1] if self.pulse_log else None

    def get_symbiosis_level(self):
        return round(self.symbiosis_level, 3)

    def get_pulse_log(self, n=10):
        return self.pulse_log[-n:]

# Example usage:
if __name__ == "__main__":
    spi = SeedPulseInterface()
    result = spi.receive_pulse("May all beings grow in balance and harmony, live in Peace and with Love.", source="founder")
    print("Symbiosis Level:", spi.get_symbiosis_level())
    print("Pulse Entry:", result["pulse_entry"])
